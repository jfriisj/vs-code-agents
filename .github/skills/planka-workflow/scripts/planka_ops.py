#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.append(str(SCRIPT_DIR))

from mcp_client import MCPClient

PHASE_CLOSE_MARKER = "[PHASE_CLOSE]"


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
    "tasklist:ensure": OperationSpec("get_card", ("cardId", "name"), "Task lists & tasks", adapter="tasklist_ensure", description="Ensure checklist exists by name"),
    "task:create": OperationSpec("create_task", ("taskListId", "name"), "Task lists & tasks", description="Create task"),
    "task:update": OperationSpec("update_task", ("taskId",), "Task lists & tasks", description="Update task"),
    "task:delete": OperationSpec("delete_task", ("taskId",), "Task lists & tasks", description="Delete task"),
    "task:ensure": OperationSpec("get_card", ("cardId", "taskListId", "name"), "Task lists & tasks", adapter="task_ensure", description="Ensure task exists by name"),

    "comments:get": OperationSpec("get_comments", ("cardId",), "Comments", description="Get comments"),
    "comment:add": OperationSpec("add_comment", ("cardId", "text"), "Comments", description="Add comment"),
    "comment:ensure-phase": OperationSpec("get_comments", ("cardId", "phase", "agent", "artifact"), "Comments", adapter="comment_ensure_phase", description="Ensure a single structured phase comment"),
    "comment:delete": OperationSpec("delete_comment", ("commentId",), "Comments", description="Delete comment"),

    "phase:close": OperationSpec("get_card", ("cardId", "phase", "agent", "artifact"), "Workflow", adapter="phase_close", description="Complete tasks, add structured comment, and verify phase close"),

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


def parse_value(raw: str, key: str | None = None) -> Any:
    # Planka IDs are numeric strings: cardId, projectId, boardId, etc.
    # We MUST NOT convert them to int/float.
    if key and (key.endswith("Id") or key in {"groupId", "fieldId", "userId", "attachmentId"}):
        return raw

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

    # Numeric conversion if not an ID
    if raw.isdigit() or (raw.startswith("-") and raw[1:].isdigit()):
        try:
            return int(raw)
        except ValueError:
            pass

    try:
        return float(raw)
    except ValueError:
        return raw


def parse_key_value_args(entries: list[str]) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    for entry in entries:
        if "=" not in entry:
            raise ValueError(f"Invalid --arg '{entry}'. Expected key=value")
        key, value = entry.split("=", 1)
        parsed[key] = parse_value(value, key.strip())
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


def _safe_id(payload: Any) -> str | None:
    if isinstance(payload, dict):
        value = payload.get("id")
        if value is not None:
            return str(value)
    return None


def _to_list(payload: Any) -> list[Any]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("items", "data", "cards", "taskLists", "task_lists", "tasks", "comments"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def _normalize_name(value: str) -> str:
    return " ".join(value.strip().lower().split())


def _as_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes", "y", "on"}:
            return True
        if lowered in {"false", "0", "no", "n", "off"}:
            return False
        return default
    return bool(value)


def _parse_task_ids(raw: Any) -> list[str]:
    if raw is None:
        return []
    if isinstance(raw, list):
        return [str(item).strip() for item in raw if str(item).strip()]
    if isinstance(raw, (int, float)):
        return [str(raw)]
    if isinstance(raw, str):
        text = raw.strip()
        if not text:
            return []
        if "," in text:
            return [part.strip() for part in text.split(",") if part.strip()]
        return [text]
    raise ValueError("taskIds must be a list, comma-separated string, or scalar")


def _task_lists_from_card(card: dict[str, Any]) -> list[dict[str, Any]]:
    direct = card.get("taskLists")
    if isinstance(direct, list):
        return [item for item in direct if isinstance(item, dict)]

    snake = card.get("task_lists")
    if isinstance(snake, list):
        return [item for item in snake if isinstance(item, dict)]

    return []


def _tasks_from_task_list(task_list: dict[str, Any]) -> list[dict[str, Any]]:
    tasks = task_list.get("tasks")
    if isinstance(tasks, list):
        return [item for item in tasks if isinstance(item, dict)]
    return []


def _find_task_list(card: dict[str, Any], name: str) -> dict[str, Any] | None:
    wanted = _normalize_name(name)
    for task_list in _task_lists_from_card(card):
        current_name = str(task_list.get("name") or "")
        if _normalize_name(current_name) == wanted:
            return task_list
    return None


def _find_task(card: dict[str, Any], task_list_id: str, name: str) -> dict[str, Any] | None:
    wanted = _normalize_name(name)
    wanted_list_id = str(task_list_id)

    for task in _to_list(card.get("tasks")):
        if not isinstance(task, dict):
            continue
        current_list_id = task.get("taskListId")
        if current_list_id is None:
            continue
        if str(current_list_id) != wanted_list_id:
            continue
        task_name = str(task.get("name") or "")
        if _normalize_name(task_name) == wanted:
            return task

    for task_list in _task_lists_from_card(card):
        current_list_id = _safe_id(task_list)
        if current_list_id != wanted_list_id:
            continue
        for task in _tasks_from_task_list(task_list):
            task_name = str(task.get("name") or "")
            if _normalize_name(task_name) == wanted:
                return task
    return None


def _collect_tasks(card: dict[str, Any]) -> dict[str, dict[str, Any]]:
    tasks_by_id: dict[str, dict[str, Any]] = {}

    for task in _to_list(card.get("tasks")):
        if not isinstance(task, dict):
            continue
        task_id = _safe_id(task)
        if task_id:
            tasks_by_id[task_id] = task

    for task_list in _task_lists_from_card(card):
        for task in _tasks_from_task_list(task_list):
            task_id = _safe_id(task)
            if task_id:
                tasks_by_id[task_id] = task

    return tasks_by_id


def _phase_comment_key(args: dict[str, Any]) -> str:
    explicit = str(args.get("key") or "").strip()
    if explicit:
        return explicit
    agent = str(args.get("agent") or "").strip()
    phase = str(args.get("phase") or "").strip()
    artifact = str(args.get("artifact") or "").strip()
    return f"{agent}|{phase}|{artifact}"


def _build_phase_comment(args: dict[str, Any]) -> str:
    key = _phase_comment_key(args)
    agent = str(args.get("agent") or "").strip()
    phase = str(args.get("phase") or "").strip()
    status = str(args.get("status") or "COMPLETE").strip()
    verdict = str(args.get("verdict") or "COMPLETE").strip()
    artifact = str(args.get("artifact") or "").strip()
    next_owner = str(args.get("next") or "n/a").strip() or "n/a"
    summary = str(args.get("summary") or "").strip()

    lines = [
        PHASE_CLOSE_MARKER,
        f"Key: {key}",
        f"Agent: {agent}",
        f"Phase: {phase}",
        f"Status: {status}",
        f"Verdict: {verdict}",
        f"Artifact: {artifact}",
        f"Next: {next_owner}",
    ]
    if summary:
        lines.append(f"Summary: {summary}")
    return "\n".join(lines)


def _ensure_task_list(args: dict[str, Any], client: MCPClient) -> dict[str, Any]:
    card_id = str(args["cardId"])
    name = str(args["name"]).strip()
    if not name:
        raise ValueError("tasklist:ensure requires a non-empty name")

    card = client.call_tool("get_card", {"cardId": card_id})
    if not isinstance(card, dict):
        raise ValueError("tasklist:ensure expected get_card to return an object")

    task_lists = _task_lists_from_card(card)
    existing = _find_task_list(card, name)
    if existing:
        return {
            "id": _safe_id(existing),
            "cardId": card_id,
            "name": str(existing.get("name") or name),
            "created": False,
            "verification": "name-matched",
        }

    explicit_task_list_id = str(args.get("taskListId") or "").strip()
    if explicit_task_list_id:
        return {
            "id": explicit_task_list_id,
            "cardId": card_id,
            "name": name,
            "created": False,
            "verification": "explicit-taskListId",
        }

    if not task_lists:
        raise RuntimeError(
            "PLANKA_SYNC_BLOCKED: tasklist:ensure cannot verify checklist names because get_card payload "
            "does not include taskLists for this board. Use tasklist:create, or pass --arg taskListId=<known_id>."
        )

    created = client.call_tool("create_task_list", {"cardId": card_id, "name": name})
    return {
        "id": _safe_id(created),
        "cardId": card_id,
        "name": name,
        "created": True,
        "verification": "created",
    }


def _ensure_task(args: dict[str, Any], client: MCPClient) -> dict[str, Any]:
    card_id = str(args["cardId"])
    task_list_id = str(args["taskListId"])
    name = str(args["name"]).strip()
    if not name:
        raise ValueError("task:ensure requires a non-empty name")

    card = client.call_tool("get_card", {"cardId": card_id})
    if not isinstance(card, dict):
        raise ValueError("task:ensure expected get_card to return an object")

    existing = _find_task(card, task_list_id, name)
    if existing:
        return {
            "id": _safe_id(existing),
            "taskListId": task_list_id,
            "name": str(existing.get("name") or name),
            "created": False,
        }

    payload: dict[str, Any] = {"taskListId": task_list_id, "name": name}
    if "position" in args:
        payload["position"] = args["position"]
    created = client.call_tool("create_task", payload)
    return {
        "id": _safe_id(created),
        "taskListId": task_list_id,
        "name": name,
        "created": True,
    }


def _ensure_phase_comment(args: dict[str, Any], client: MCPClient) -> dict[str, Any]:
    card_id = str(args["cardId"])
    key = _phase_comment_key(args)
    comment_text = str(args.get("text") or "").strip() or _build_phase_comment(args)

    comments = client.call_tool("get_comments", {"cardId": card_id})
    for comment in _to_list(comments):
        if not isinstance(comment, dict):
            continue
        text = str(comment.get("text") or "")
        if PHASE_CLOSE_MARKER in text and f"Key: {key}" in text:
            return {
                "id": _safe_id(comment),
                "cardId": card_id,
                "key": key,
                "created": False,
            }

    created = client.call_tool("add_comment", {"cardId": card_id, "text": comment_text})
    return {
        "id": _safe_id(created),
        "cardId": card_id,
        "key": key,
        "created": True,
    }


def _phase_close(args: dict[str, Any], client: MCPClient) -> dict[str, Any]:
    card_id = str(args["cardId"])
    task_ids = _parse_task_ids(args.get("taskIds"))
    strict = _as_bool(args.get("strict"), default=True)

    updated_task_ids: list[str] = []
    for task_id in task_ids:
        client.call_tool("update_task", {"taskId": task_id, "isCompleted": True})
        updated_task_ids.append(task_id)

    comment_info = _ensure_phase_comment(args, client)
    card = client.call_tool("get_card", {"cardId": card_id})
    if not isinstance(card, dict):
        raise ValueError("phase:close expected get_card to return an object")

    task_map = _collect_tasks(card)
    missing_task_ids = [task_id for task_id in updated_task_ids if task_id not in task_map]
    incomplete_task_ids = [
        task_id
        for task_id in updated_task_ids
        if task_id in task_map and not _as_bool(task_map[task_id].get("isCompleted"), default=False)
    ]

    verification_ok = not missing_task_ids and not incomplete_task_ids
    if strict and not verification_ok:
        raise RuntimeError(
            "PLANKA_SYNC_BLOCKED: phase close verification failed "
            f"(missing={missing_task_ids}, incomplete={incomplete_task_ids})"
        )

    return {
        "cardId": card_id,
        "agent": str(args.get("agent") or "").strip(),
        "phase": str(args.get("phase") or "").strip(),
        "updatedTaskIds": updated_task_ids,
        "comment": comment_info,
        "verification": {
            "ok": verification_ok,
            "missingTaskIds": missing_task_ids,
            "incompleteTaskIds": incomplete_task_ids,
            "listId": str(card.get("listId")) if card.get("listId") is not None else None,
        },
    }


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


def execute_operation(op: str, spec: OperationSpec, args: dict[str, Any], client: MCPClient) -> Any:
    _require(args, spec.required, op)

    if spec.adapter == "tasklist_ensure":
        return _ensure_task_list(args, client)
    if spec.adapter == "task_ensure":
        return _ensure_task(args, client)
    if spec.adapter == "comment_ensure_phase":
        return _ensure_phase_comment(args, client)
    if spec.adapter == "phase_close":
        return _phase_close(args, client)

    payload = build_payload(op, args, client)
    return client.call_tool(spec.tool, payload)


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
        _require(loaded_args, spec.required, op)

        if args.dry_run:
            if spec.adapter in {"tasklist_ensure", "task_ensure", "comment_ensure_phase", "phase_close"}:
                preview_payload = dict(loaded_args)
                if spec.adapter in {"comment_ensure_phase", "phase_close"} and "text" not in preview_payload:
                    preview_payload["text"] = _build_phase_comment(loaded_args)
                if spec.adapter == "phase_close":
                    preview_payload["taskIds"] = _parse_task_ids(loaded_args.get("taskIds"))
            else:
                preview_payload = build_payload(op, loaded_args, client)

            preview = {
                "operation": op,
                "tool": spec.tool,
                "adapter": spec.adapter,
                "payload": preview_payload,
            }
            print(json.dumps(preview, indent=2))
            return

        result = execute_operation(op, spec, loaded_args, client)
        print(json.dumps(result, indent=2))
        return

    raise RuntimeError(f"Unknown command {args.command}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # SEC-001: Redact sensitive environment variables from error logs
        msg = str(e)
        sensitive_keys = ["PLANKA_TOKEN", "ACCESS_KEY", "SECRET_KEY", "API_KEY"]
        for key in sensitive_keys:
            val = os.environ.get(key)
            if val and len(val) > 4:
                msg = msg.replace(val, "[REDACTED]")
        
        print(json.dumps({"error": msg}, indent=2), file=sys.stderr)
        sys.exit(1)
