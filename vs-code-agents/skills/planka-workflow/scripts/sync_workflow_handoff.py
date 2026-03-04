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
    extract_project_id,
    get_workflow_mapping,
    normalize_agent_list,
    now_iso,
    upsert_workflow_mapping,
    upsert_description_field,
)


def extract_active_lists(board: dict[str, Any]) -> list[dict[str, Any]]:
    return [entry for entry in board.get("lists", []) if entry.get("type") == "active"]


def resolve_board_id(
    client: MCPClient,
    board_id: str | None,
    project_id: str,
    board_name: str | None,
    workflow_id: str,
) -> tuple[str, str]:
    if board_id:
        board = client.call_tool("get_board", {"boardId": board_id})
        resolved_project_id = extract_project_id(board)
        if resolved_project_id and resolved_project_id != project_id:
            raise RuntimeError(
                f"Board '{board_id}' belongs to project '{resolved_project_id}', "
                f"expected '{project_id}'"
            )
        return board["id"], board.get("name", "")

    boards = client.call_tool("list_boards", {"projectId": project_id})

    if board_name:
        for board in boards:
            if board.get("name") == board_name:
                return board["id"], board["name"]
        raise RuntimeError(f"Board '{board_name}' not found in project {project_id}")

    prefix = f"WF-{workflow_id}-"
    for board in boards:
        name = board.get("name", "")
        if name.startswith(prefix):
            return board["id"], name

    raise RuntimeError(
        f"No board found with prefix '{prefix}' in project {project_id}. Use --board-name or --board-id."
    )


def locate_card(
    board: dict[str, Any],
    workflow_id: str,
    card_id: str | None,
    card_title: str | None,
) -> dict[str, Any]:
    for board_list in extract_active_lists(board):
        for card in board_list.get("cards", []):
            if card_id and card.get("id") == card_id:
                return card
            if card_title and card.get("name") == card_title:
                return card
            if not card_id and not card_title:
                if card.get("name", "").startswith(f"WF-{workflow_id} "):
                    return card

    raise RuntimeError("Primary workflow card not found on board")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync workflow handoff between agent lists in Planka")
    parser.add_argument("--mcp-url", default="http://localhost:25478/mcp")
    parser.add_argument("--workflow-id", required=True)
    parser.add_argument("--board-id")
    parser.add_argument("--project-id")
    parser.add_argument("--board-name")
    parser.add_argument("--card-id")
    parser.add_argument("--card-title")
    parser.add_argument("--from-agent", required=True)
    parser.add_argument("--to-agent", required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--artifact", default="")
    parser.add_argument("--summary", required=True)
    parser.add_argument("--next", dest="next_step", default="")
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

    if args.card_id and workflow_mapping.get("cardId") and args.card_id != workflow_mapping.get("cardId"):
        raise RuntimeError(
            f"Workflow {args.workflow_id} is already mapped to card "
            f"'{workflow_mapping.get('cardId')}', not '{args.card_id}'"
        )

    project_id = args.project_id or workflow_mapping.get("projectId")
    if not project_id:
        raise RuntimeError(
            "Workflow project is undefined. Run bootstrap first or pass --project-id."
        )

    board_id = args.board_id or workflow_mapping.get("boardId")
    board_name = args.board_name or workflow_mapping.get("boardName")
    card_id = args.card_id or workflow_mapping.get("cardId")
    card_title = args.card_title or workflow_mapping.get("cardTitle")

    from_list_name = normalize_agent_list(args.from_agent)
    to_list_name = normalize_agent_list(args.to_agent)
    synced_at = now_iso()

    client = MCPClient(args.mcp_url)
    client.initialize()

    board_id, resolved_board_name = resolve_board_id(
        client,
        board_id=board_id,
        project_id=project_id,
        board_name=board_name,
        workflow_id=args.workflow_id,
    )

    board = client.call_tool("get_board", {"boardId": board_id})
    resolved_project_id = extract_project_id(board)
    if resolved_project_id and resolved_project_id != project_id:
        raise RuntimeError(
            f"Board '{board_id}' belongs to project '{resolved_project_id}', "
            f"expected '{project_id}'"
        )

    active_lists = extract_active_lists(board)
    list_map = {entry.get("name"): entry for entry in active_lists if entry.get("name")}

    missing = [name for name in REQUIRED_LISTS if name not in list_map]
    if missing:
        raise RuntimeError(
            f"Board '{resolved_board_name}' missing required lists: {', '.join(missing)}"
        )

    card = locate_card(
        board,
        workflow_id=args.workflow_id,
        card_id=card_id,
        card_title=card_title,
    )

    if card.get("listId") != list_map[to_list_name]["id"]:
        client.call_tool(
            "move_card",
            {
                "cardId": card["id"],
                "listId": list_map[to_list_name]["id"],
            },
        )

    description = card.get("description") or ""
    description = upsert_description_field(description, "Current Status", args.status)
    description = upsert_description_field(description, "Current Agent", to_list_name)
    description = upsert_description_field(description, "Last Synced At", synced_at)
    if args.artifact:
        description = upsert_description_field(
            description,
            "Primary Markdown Artifact",
            args.artifact,
        )

    client.call_tool(
        "update_card",
        {
            "cardId": card["id"],
            "description": description,
        },
    )

    comment_lines = [
        f"Handoff From: {from_list_name}",
        f"Handoff To: {to_list_name}",
    ]
    if args.artifact:
        comment_lines.extend(["Updated Artifacts:", f"- {args.artifact}"])
    comment_lines.extend(["Summary:", f"- {args.summary}"])
    if args.next_step:
        comment_lines.extend(["Next:", f"- {args.next_step}"])
    comment_lines.extend(["Timestamp:", f"- {synced_at}"])

    comment_text = "\n".join(comment_lines)
    client.call_tool(
        "add_comment",
        {
            "cardId": card["id"],
            "text": comment_text,
        },
    )

    project_name = workflow_mapping.get("projectName", "")
    board_project = board.get("project")
    if isinstance(board_project, dict) and board_project.get("name"):
        project_name = str(board_project.get("name"))

    mapping = upsert_workflow_mapping(
        args.state_file,
        args.workflow_id,
        {
            "projectId": project_id,
            "projectName": project_name,
            "boardId": board_id,
            "boardName": resolved_board_name,
            "cardId": card["id"],
            "cardTitle": card.get("name") or card_title or "",
            "primaryArtifact": args.artifact or workflow_mapping.get("primaryArtifact", ""),
            "currentStatus": args.status,
            "currentAgent": to_list_name,
            "lastSyncedAt": synced_at,
        },
    )

    result = {
        "projectId": project_id,
        "boardId": board_id,
        "boardName": resolved_board_name,
        "cardId": card["id"],
        "cardName": card.get("name"),
        "from": from_list_name,
        "to": to_list_name,
        "status": args.status,
        "syncedAt": synced_at,
        "stateFile": args.state_file,
        "workflowMapping": mapping,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
