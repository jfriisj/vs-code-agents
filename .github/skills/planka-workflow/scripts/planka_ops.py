#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.append(str(SCRIPT_DIR))

from mcp_client import MCPClient


@dataclass(frozen=True)
class OperationSpec:
    tool: str
    required: tuple[str, ...]
    category: str
    adapter: str | None = None
    description: str = ""


OPS: dict[str, OperationSpec] = {
    "projects:list": OperationSpec("list_projects", tuple(), "Projects", description="List all projects"),
    "project:get": OperationSpec("get_project", ("projectId",), "Projects", description="Get one project"),
    "project:create": OperationSpec("create_project", ("name",), "Projects", description="Create project"),
    "project:update": OperationSpec("update_project", ("projectId", "name"), "Projects", description="Rename project"),
    "project:delete": OperationSpec("delete_project", ("projectId",), "Projects", description="Delete project"),

    "boards:list": OperationSpec("list_boards", ("projectId",), "Boards", description="List boards in project"),
    "board:get": OperationSpec("get_board", ("boardId",), "Boards", description="Get board details"),
    "board:create": OperationSpec("create_board", ("projectId", "name"), "Boards", description="Create board"),
    "board:update": OperationSpec("update_board", ("boardId",), "Boards", description="Update board"),
    "board:delete": OperationSpec("delete_board", ("boardId",), "Boards", description="Delete board"),

    "list:create": OperationSpec("create_list", ("boardId", "name"), "Lists", description="Create list"),
    "list:update": OperationSpec("update_list", ("listId",), "Lists", description="Update list"),
    "list:delete": OperationSpec("delete_list", ("listId",), "Lists", description="Delete list"),

    "card:get": OperationSpec("get_card", ("cardId",), "Cards", description="Get card details"),
    "card:create": OperationSpec("create_card", ("listId", "name"), "Cards", description="Create card"),
    "card:update": OperationSpec("update_card", ("cardId",), "Cards", description="Update card"),
    "card:move": OperationSpec("move_card", ("cardId", "listId"), "Cards", description="Move card"),
    "card:delete": OperationSpec("delete_card", ("cardId",), "Cards", description="Delete card"),

    "label:create": OperationSpec("create_label", ("boardId", "name", "color"), "Labels", description="Create label"),
    "label:add": OperationSpec("add_label_to_card", ("cardId", "labelId"), "Labels", description="Add label to card"),
    "label:remove": OperationSpec("remove_label_from_card", ("cardId", "labelId"), "Labels", description="Remove label from card"),

    "tasklist:create": OperationSpec("create_task_list", ("cardId", "name"), "Task lists & tasks", description="Create checklist"),
    "tasklist:update": OperationSpec("update_task_list", ("taskListId",), "Task lists & tasks", description="Update checklist"),
    "tasklist:delete": OperationSpec("delete_task_list", ("taskListId",), "Task lists & tasks", description="Delete checklist"),
    "task:create": OperationSpec("create_task", ("taskListId", "name"), "Task lists & tasks", description="Create task"),
    "task:update": OperationSpec("update_task", ("taskId",), "Task lists & tasks", description="Update task"),
    "task:delete": OperationSpec("delete_task", ("taskId",), "Task lists & tasks", description="Delete task"),

    "comments:get": OperationSpec("get_comments", ("cardId",), "Comments", description="Get comments"),
    "comment:add": OperationSpec("add_comment", ("cardId", "text"), "Comments", description="Add comment"),
    "comment:delete": OperationSpec("delete_comment", ("commentId",), "Comments", description="Delete comment"),

    "attachment:upload": OperationSpec("upload_attachment", ("cardId", "filename", "fileContent"), "Attachments", description="Upload attachment from base64 content"),
    "attachment:upload-file": OperationSpec("upload_attachment", ("cardId", "path"), "Attachments", adapter="attachment_upload_file", description="Upload attachment from local file path"),
    "attachment:delete": OperationSpec("delete_attachment", ("attachmentId",), "Attachments", description="Delete attachment"),

    "member:add": OperationSpec("add_card_member", ("cardId", "userId"), "Card members", description="Add member to card"),
    "member:remove": OperationSpec("remove_card_member", ("cardId", "userId"), "Card members", description="Remove member from card"),

    "stopwatch:start": OperationSpec("update_card", ("cardId",), "Stopwatch", adapter="stopwatch_start", description="Start stopwatch"),
    "stopwatch:stop": OperationSpec("update_card", ("cardId",), "Stopwatch", adapter="stopwatch_stop", description="Stop stopwatch"),

    "subscribe:set": OperationSpec("update_card", ("cardId", "enabled"), "Subscribe", adapter="subscribe_set", description="Subscribe/unsubscribe card"),

    "customgroup:create": OperationSpec("create_custom_field_group", ("boardId", "name"), "Custom fields", description="Create custom field group"),
    "customgroup:update": OperationSpec("update_custom_field_group", ("groupId",), "Custom fields", description="Update custom field group"),
    "customgroup:delete": OperationSpec("delete_custom_field_group", ("groupId",), "Custom fields", description="Delete custom field group"),
    "customfield:create": OperationSpec("create_custom_field", ("groupId", "name"), "Custom fields", description="Create custom field"),
    "customfield:update": OperationSpec("update_custom_field", ("fieldId",), "Custom fields", description="Update custom field"),
    "customfield:delete": OperationSpec("delete_custom_field", ("fieldId",), "Custom fields", description="Delete custom field"),
    "customvalue:set": OperationSpec("set_custom_field_value", ("cardId", "groupId", "fieldId", "content"), "Custom fields", description="Set custom field value"),
    "customvalue:delete": OperationSpec("delete_custom_field_value", ("cardId", "groupId", "fieldId"), "Custom fields", description="Delete custom field value"),
}


def parse_value(raw: str) -> Any:
    lowered = raw.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none"}:
        return None

    if raw.startswith("{") or raw.startswith("["):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass

    try:
        if raw.isdigit() or (raw.startswith("-") and raw[1:].isdigit()):
            return int(raw)
        return float(raw)
    except ValueError:
        return raw


def parse_key_value_args(entries: list[str]) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    for entry in entries:
        if "=" not in entry:
            raise ValueError(f"Invalid --arg '{entry}'. Expected key=value")
        key, value = entry.split("=", 1)
        parsed[key] = parse_value(value)
    return parsed


def load_args(raw_json: str | None, json_file: str | None, kv_entries: list[str]) -> dict[str, Any]:
    merged: dict[str, Any] = {}

    if json_file:
        data = json.loads(Path(json_file).read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("--args-file must contain a JSON object")
        merged.update(data)

    if raw_json:
        data = json.loads(raw_json)
        if not isinstance(data, dict):
            raise ValueError("--args-json must be a JSON object")
        merged.update(data)

    merged.update(parse_key_value_args(kv_entries))
    return merged


def now_iso() -> str:
    return datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat()


def _require(args: dict[str, Any], fields: tuple[str, ...], op: str) -> None:
    missing = [field for field in fields if field not in args]
    if missing:
        raise ValueError(f"Operation '{op}' missing required args: {', '.join(missing)}")


def _attachment_upload_file(args: dict[str, Any]) -> dict[str, Any]:
    card_id = str(args["cardId"])
    source_path = Path(str(args["path"]))
    if not source_path.exists() or not source_path.is_file():
        raise ValueError(f"Attachment path does not exist or is not a file: {source_path}")

    filename = str(args.get("filename") or source_path.name)
    mime_type = args.get("mimeType")
    if not mime_type:
        guessed, _ = mimetypes.guess_type(str(source_path))
        mime_type = guessed

    content_b64 = base64.b64encode(source_path.read_bytes()).decode("ascii")

    payload: dict[str, Any] = {
        "cardId": card_id,
        "filename": filename,
        "fileContent": content_b64,
    }
    if mime_type:
        payload["mimeType"] = str(mime_type)

    return payload


def _subscribe_set(args: dict[str, Any]) -> dict[str, Any]:
    enabled = args["enabled"]
    if isinstance(enabled, str):
        enabled = parse_value(enabled)
    if not isinstance(enabled, bool):
        raise ValueError("subscribe:set requires enabled=true|false")
    return {"cardId": str(args["cardId"]), "isSubscribed": enabled}


def _stopwatch_start(args: dict[str, Any]) -> dict[str, Any]:
    total = int(args.get("total", 0))
    return {
        "cardId": str(args["cardId"]),
        "stopwatch": {
            "startedAt": now_iso(),
            "total": total,
        },
    }


def _parse_iso_datetime(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def _stopwatch_stop(args: dict[str, Any], client: MCPClient) -> dict[str, Any]:
    card_id = str(args["cardId"])
    if "total" in args:
        total = int(args["total"])
    else:
        card = client.call_tool("get_card", {"cardId": card_id})
        stopwatch = card.get("stopwatch") or {}
        total = int(stopwatch.get("total") or 0)
        started_at = stopwatch.get("startedAt")
        if started_at:
            started = _parse_iso_datetime(str(started_at))
            elapsed = int((datetime.now(tz=timezone.utc) - started).total_seconds())
            if elapsed > 0:
                total += elapsed

    return {
        "cardId": card_id,
        "stopwatch": {
            "startedAt": None,
            "total": total,
        },
    }


def build_payload(op: str, args: dict[str, Any], client: MCPClient) -> dict[str, Any]:
    spec = OPS[op]
    _require(args, spec.required, op)

    if spec.adapter == "attachment_upload_file":
        return _attachment_upload_file(args)
    if spec.adapter == "subscribe_set":
        return _subscribe_set(args)
    if spec.adapter == "stopwatch_start":
        return _stopwatch_start(args)
    if spec.adapter == "stopwatch_stop":
        return _stopwatch_stop(args, client)

    return args


def catalog_payload() -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for op, spec in OPS.items():
        grouped.setdefault(spec.category, []).append(
            {
                "operation": op,
                "tool": spec.tool,
                "required": list(spec.required),
                "description": spec.description,
            }
        )

    for category in grouped:
        grouped[category] = sorted(grouped[category], key=lambda item: item["operation"])

    return grouped


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Planka MCP operations CLI")
    parser.add_argument("--mcp-url", default="http://localhost:25478/mcp")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("catalog", help="Print operation catalog grouped by feature category")
    subparsers.add_parser("list-tools", help="List tools exposed by active MCP server")

    run_parser = subparsers.add_parser("run", help="Run an operation alias")
    run_parser.add_argument("--op", required=True, choices=sorted(OPS.keys()))
    run_parser.add_argument("--args-json", help="JSON object string with operation arguments")
    run_parser.add_argument("--args-file", help="Path to JSON file with operation arguments")
    run_parser.add_argument("--arg", action="append", default=[], help="key=value argument (repeatable)")
    run_parser.add_argument("--dry-run", action="store_true", help="Print resolved tool+payload without executing")

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.command == "catalog":
        print(json.dumps(catalog_payload(), indent=2))
        return

    client = MCPClient(args.mcp_url)
    client.initialize()

    if args.command == "list-tools":
        tools = client.list_tools()
        print(json.dumps(tools, indent=2))
        return

    if args.command == "run":
        op = args.op
        spec = OPS[op]
        loaded_args = load_args(args.args_json, args.args_file, args.arg)
        payload = build_payload(op, loaded_args, client)

        if args.dry_run:
            preview = {
                "operation": op,
                "tool": spec.tool,
                "payload": payload,
            }
            print(json.dumps(preview, indent=2))
            return

        result = client.call_tool(spec.tool, payload)
        print(json.dumps(result, indent=2))
        return

    raise RuntimeError(f"Unknown command {args.command}")


if __name__ == "__main__":
    main()
