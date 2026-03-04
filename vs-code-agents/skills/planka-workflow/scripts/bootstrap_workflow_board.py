#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.append(str(SCRIPT_DIR))

from mcp_client import MCPClient
from workflow_common import (
    DEFAULT_WORKFLOW_STATE_FILE,
    REQUIRED_LISTS,
    build_workflow_description,
    extract_project_id,
    get_workflow_mapping,
    normalize_agent_list,
    now_iso,
    slugify,
    upsert_workflow_mapping,
)


def find_by_name(items: list[dict[str, Any]], name: str) -> dict[str, Any] | None:
    for item in items:
        if item.get("name") == name:
            return item
    return None


def extract_active_lists(board: dict[str, Any]) -> list[dict[str, Any]]:
    return [entry for entry in board.get("lists", []) if entry.get("type") == "active"]


def ensure_project(
    client: MCPClient,
    project_id: str | None,
    project_name: str,
    create_if_missing: bool,
) -> dict[str, Any]:
    if project_id:
        projects = client.call_tool("list_projects", {})
        for project in projects:
            if project.get("id") == project_id:
                return project
        raise RuntimeError(f"Project id '{project_id}' was not found")

    projects = client.call_tool("list_projects", {})
    match = find_by_name(projects, project_name)
    if match:
        return match

    if not create_if_missing:
        raise RuntimeError(
            f"Project '{project_name}' not found. Re-run with --create-project-if-missing."
        )

    created = client.call_tool("create_project", {"name": project_name})
    if not isinstance(created, dict):
        raise RuntimeError(f"Unexpected create_project response: {created}")
    return created


def ensure_board(
    client: MCPClient,
    project_id: str,
    board_name: str,
    board_id: str | None,
) -> dict[str, Any]:
    if board_id:
        board = client.call_tool("get_board", {"boardId": board_id})
        resolved_project_id = extract_project_id(board)
        if resolved_project_id and resolved_project_id != project_id:
            raise RuntimeError(
                f"Board '{board_id}' belongs to project '{resolved_project_id}', "
                f"expected '{project_id}'"
            )
        return board

    boards = client.call_tool("list_boards", {"projectId": project_id})
    match = find_by_name(boards, board_name)
    if match:
        return match

    created = client.call_tool("create_board", {"projectId": project_id, "name": board_name})
    if not isinstance(created, dict):
        raise RuntimeError(f"Unexpected create_board response: {created}")
    return created


def ensure_lists(client: MCPClient, board_id: str) -> dict[str, str]:
    board = client.call_tool("get_board", {"boardId": board_id})
    active_lists = extract_active_lists(board)

    by_name = {entry.get("name"): entry for entry in active_lists if entry.get("name")}

    for index, list_name in enumerate(REQUIRED_LISTS, start=1):
        if list_name not in by_name:
            client.call_tool(
                "create_list",
                {"boardId": board_id, "name": list_name, "position": index},
            )

    board = client.call_tool("get_board", {"boardId": board_id})
    active_lists = extract_active_lists(board)
    by_name = {entry.get("name"): entry for entry in active_lists if entry.get("name")}

    for index, list_name in enumerate(REQUIRED_LISTS, start=1):
        list_entry = by_name.get(list_name)
        if not list_entry:
            raise RuntimeError(f"List '{list_name}' missing after creation")
        current_position = list_entry.get("position")
        if current_position != index:
            client.call_tool(
                "update_list", {"listId": list_entry["id"], "position": index}
            )

    board = client.call_tool("get_board", {"boardId": board_id})
    active_lists = extract_active_lists(board)
    return {entry["name"]: entry["id"] for entry in active_lists if entry.get("name")}


def locate_primary_card(board: dict[str, Any], card_title: str) -> dict[str, Any] | None:
    for board_list in extract_active_lists(board):
        for card in board_list.get("cards", []):
            if card.get("name") == card_title:
                return card
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap or reconcile a workflow board in Planka")
    parser.add_argument("--mcp-url", default="http://localhost:25478/mcp")
    parser.add_argument("--project-id")
    parser.add_argument("--project-name")
    parser.set_defaults(create_project_if_missing=True)
    parser.add_argument(
        "--create-project-if-missing",
        dest="create_project_if_missing",
        action="store_true",
        help="Create Planka project if missing (default: enabled)",
    )
    parser.add_argument(
        "--no-create-project-if-missing",
        dest="create_project_if_missing",
        action="store_false",
        help="Fail instead of creating project when project name is missing",
    )
    parser.add_argument("--workflow-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--board-id")
    parser.add_argument("--board-name")
    parser.add_argument("--card-title")
    parser.add_argument("--artifact", default="agent-output/planning/NNN-plan-name.md")
    parser.add_argument("--origin")
    parser.add_argument("--uuid", default="")
    parser.add_argument("--status", default="Active")
    parser.add_argument("--agent", default="01-Roadmap")
    parser.add_argument("--state-file", default=DEFAULT_WORKFLOW_STATE_FILE)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    workflow_mapping = get_workflow_mapping(args.state_file, args.workflow_id) or {}

    if args.project_id and workflow_mapping.get("projectId") and args.project_id != workflow_mapping.get("projectId"):
        raise RuntimeError(
            f"Workflow {args.workflow_id} is already mapped to project "
            f"'{workflow_mapping.get('projectId')}', not '{args.project_id}'"
        )

    if args.board_id and workflow_mapping.get("boardId") and args.board_id != workflow_mapping.get("boardId"):
        raise RuntimeError(
            f"Workflow {args.workflow_id} is already mapped to board "
            f"'{workflow_mapping.get('boardId')}', not '{args.board_id}'"
        )

    project_id = args.project_id or workflow_mapping.get("projectId")
    project_name = (
        args.project_name
        or workflow_mapping.get("projectName")
        or "Universal Speech Translation Platform"
    )

    agent_list = normalize_agent_list(args.agent)
    short_slug = slugify(args.title)
    board_name = args.board_name or workflow_mapping.get("boardName") or f"WF-{args.workflow_id}-{short_slug}"
    card_title = args.card_title or workflow_mapping.get("cardTitle") or f"WF-{args.workflow_id} {args.title}"
    origin = args.origin or workflow_mapping.get("origin") or args.workflow_id
    synced_at = now_iso()

    client = MCPClient(args.mcp_url)
    client.initialize()

    project = ensure_project(
        client,
        project_id=project_id,
        project_name=project_name,
        create_if_missing=args.create_project_if_missing,
    )

    board = ensure_board(
        client,
        project_id=project["id"],
        board_name=board_name,
        board_id=args.board_id or workflow_mapping.get("boardId"),
    )
    list_name_to_id = ensure_lists(client, board_id=board["id"])

    board_data = client.call_tool("get_board", {"boardId": board["id"]})
    primary_card = locate_primary_card(board_data, card_title)

    if primary_card is None:
        created = client.call_tool(
            "create_card",
            {
                "listId": list_name_to_id[agent_list],
                "name": card_title,
            },
        )
        if not isinstance(created, dict):
            raise RuntimeError(f"Unexpected create_card response: {created}")
        card_id = created["id"]
        card_list_id = created.get("listId", list_name_to_id[agent_list])
    else:
        card_id = primary_card["id"]
        card_list_id = primary_card.get("listId")

    if card_list_id != list_name_to_id[agent_list]:
        client.call_tool(
            "move_card",
            {
                "cardId": card_id,
                "listId": list_name_to_id[agent_list],
            },
        )

    description = build_workflow_description(
        workflow_id=args.workflow_id,
        origin=origin,
        uuid=args.uuid,
        artifact=args.artifact,
        status=args.status,
        agent=agent_list,
        synced_at=synced_at,
    )
    client.call_tool("update_card", {"cardId": card_id, "description": description})

    mapping = upsert_workflow_mapping(
        args.state_file,
        args.workflow_id,
        {
            "origin": origin,
            "projectId": project["id"],
            "projectName": project.get("name") or project_name,
            "boardId": board["id"],
            "boardName": board.get("name") or board_name,
            "cardId": card_id,
            "cardTitle": card_title,
            "primaryArtifact": args.artifact,
            "currentStatus": args.status,
            "currentAgent": agent_list,
            "lastSyncedAt": synced_at,
        },
    )

    summary = {
        "projectId": project["id"],
        "projectName": project.get("name"),
        "boardId": board["id"],
        "boardName": board.get("name"),
        "cardId": card_id,
        "cardTitle": card_title,
        "currentAgentList": agent_list,
        "status": args.status,
        "syncedAt": synced_at,
        "stateFile": args.state_file,
        "workflowMapping": mapping,
    }

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
