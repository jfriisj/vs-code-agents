#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.append(str(SCRIPT_DIR))

from mcp_client import MCPClient, MCPError


STATUS_LIST_ORDER = ["Planned", "In Progress", "Delivered", "Deferred", "Closed"]

STATUS_ALIASES = {
    "planned": "Planned",
    "in progress": "In Progress",
    "in-progress": "In Progress",
    "delivered": "Delivered",
    "deferred": "Deferred",
    "closed": "Closed",
}

PRIORITY_COLORS = {
    "P0": "berry-red",
    "P1": "pumpkin-orange",
    "P2": "sunny-grass",
    "P3": "light-concrete",
}

RELEASE_COLOR_CYCLE = [
    "antique-blue",
    "lagoon-blue",
    "navy-blue",
    "midnight-blue",
    "morning-sky",
    "orange-peel",
    "tank-green",
    "light-concrete",
]

RE_RELEASE = re.compile(r"^##\s+Release\s+(v[^\s]+)\s*-\s*(.+?)\s*$")
RE_EPIC = re.compile(r"^###\s+Epic\s+([0-9]+(?:\.[0-9]+)?)\s*:\s*(.+?)\s*$")
RE_PRIORITY = re.compile(r"^\*\*Priority\*\*:\s*([Pp][0-9]+)")
RE_STATUS = re.compile(r"^\*\*Status\*\*:\s*(.+?)\s*$")
RE_TARGET_DATE = re.compile(r"^\*\*Target Date\*\*:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})\s*$")

DEFAULT_TASK_LISTS = [
    "Acceptance Criteria",
    "Analysis & Spikes",
    "Architecture & Design",
    "Security & Compliance",
    "Implementation",
    "Code Review",
    "QA & Testing",
    "UAT & Acceptance",
    "Release & Deployment",
    "Retrospective & Learnings",
]


@dataclass(frozen=True)
class EpicRecord:
    release_version: str
    release_title: str
    epic_id: str
    epic_title: str
    target_date: str | None
    priority: str
    status: str
    status_line_index: int | None
    markdown_block: str

    @property
    def card_name(self) -> str:
        return f"Epic {self.epic_id}: {self.epic_title}"


def normalize_name(value: str) -> str:
    return " ".join(value.strip().lower().split())


def to_list(payload: Any) -> list[Any]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("items", "data", "projects", "boards", "lists", "cards", "labels"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def safe_id(payload: Any) -> str | None:
    if isinstance(payload, dict):
        value = payload.get("id")
        if value is not None:
            return str(value)
    return None


def has_content(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, set, dict)):
        return len(value) > 0
    return True


def normalize_due_date(raw: Any) -> str | None:
    if raw is None:
        return None

    value = str(raw).strip()
    if not value:
        return None

    if re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        return f"{value}T23:59:59.000Z"

    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return value

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    utc_value = parsed.astimezone(timezone.utc)
    return utc_value.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def desired_due_date(target_date: str | None) -> str | None:
    if not target_date:
        return None
    return normalize_due_date(target_date)


def normalize_status(raw: str, warnings: list[str], epic_ref: str) -> str:
    collapsed = " ".join(raw.strip().split())
    bracket_cut = collapsed.split("[", 1)[0].strip()
    canonical = STATUS_ALIASES.get(bracket_cut.lower())
    if canonical:
        return canonical
    warnings.append(f"Unknown status '{raw}' on {epic_ref}; defaulted to Planned")
    return "Planned"


def normalize_priority(raw: str | None) -> str:
    if not raw:
        return "P2"
    normalized = raw.strip().upper()
    if re.fullmatch(r"P[0-9]", normalized):
        return normalized
    return "P2"


def parse_roadmap_epics(roadmap_path: Path) -> tuple[list[EpicRecord], list[str]]:
    lines = roadmap_path.read_text(encoding="utf-8").splitlines()
    warnings: list[str] = []
    epics: list[EpicRecord] = []

    current_release_version: str | None = None
    current_release_title: str | None = None
    current_release_target_date: str | None = None

    index = 0
    while index < len(lines):
        line = lines[index].rstrip()
        release_match = RE_RELEASE.match(line)
        if release_match:
            current_release_version = release_match.group(1).strip()
            current_release_title = release_match.group(2).strip()
            current_release_target_date = None
            index += 1
            continue

        target_date_match = RE_TARGET_DATE.match(line)
        if target_date_match and current_release_version:
            current_release_target_date = target_date_match.group(1).strip()
            index += 1
            continue

        epic_match = RE_EPIC.match(line)
        if epic_match and current_release_version and current_release_title:
            block_start = index
            next_index = index + 1
            while next_index < len(lines):
                candidate = lines[next_index].rstrip()
                if RE_RELEASE.match(candidate) or RE_EPIC.match(candidate):
                    break
                next_index += 1

            block_lines = lines[block_start:next_index]
            priority_value: str | None = None
            status_value: str | None = None
            status_line_index: int | None = None
            for offset, block_line in enumerate(block_lines):
                stripped = block_line.strip()
                priority_match = RE_PRIORITY.match(stripped)
                if priority_match:
                    priority_value = priority_match.group(1)

                status_match = RE_STATUS.match(stripped)
                if status_match:
                    status_value = status_match.group(1)
                    status_line_index = block_start + offset

            epic_id = epic_match.group(1).strip()
            epic_title = epic_match.group(2).strip()
            epic_ref = f"Epic {epic_id}: {epic_title}"
            canonical_status = normalize_status(status_value or "Planned", warnings, epic_ref)
            canonical_priority = normalize_priority(priority_value)

            epics.append(
                EpicRecord(
                    release_version=current_release_version,
                    release_title=current_release_title,
                    epic_id=epic_id,
                    epic_title=epic_title,
                    target_date=current_release_target_date,
                    priority=canonical_priority,
                    status=canonical_status,
                    status_line_index=status_line_index,
                    markdown_block="\n".join(block_lines).strip(),
                )
            )

            index = next_index
            continue

        index += 1

    return epics, warnings


class SyncRunner:
    def __init__(self, client: MCPClient, dry_run: bool) -> None:
        self.client = client
        self.dry_run = dry_run
        self.synthetic_counter = 1
        self.actions: list[dict[str, Any]] = []

    def _next_synthetic_id(self, prefix: str) -> str:
        value = f"{prefix}-dryrun-{self.synthetic_counter}"
        self.synthetic_counter += 1
        return value

    def read(self, tool: str, arguments: dict[str, Any] | None = None) -> Any:
        return self.client.call_tool(tool, arguments or {})

    def write(self, tool: str, arguments: dict[str, Any]) -> dict[str, Any]:
        preview: dict[str, Any] = {}
        for key, value in arguments.items():
            if isinstance(value, str) and len(value) > 180:
                preview[key] = f"<{len(value)} chars>"
            else:
                preview[key] = value
        self.actions.append({"tool": tool, "arguments": preview})

        if self.dry_run:
            if tool in {"create_project", "create_board", "create_list", "create_card", "create_label"}:
                return {"id": self._next_synthetic_id(tool)}
            return {}

        result = self.client.call_tool(tool, arguments)
        if isinstance(result, dict):
            return result
        return {}


def find_by_name(items: list[dict[str, Any]], name: str) -> dict[str, Any] | None:
    wanted = normalize_name(name)
    for item in items:
        item_name = str(item.get("name") or "").strip()
        if normalize_name(item_name) == wanted:
            return item
    return None


def ensure_project(
    runner: SyncRunner,
    project_name: str,
    board_name: str,
    allow_create: bool,
    warnings: list[str],
) -> str:
    projects = to_list(runner.read("list_projects", {}))
    projects = [entry for entry in projects if isinstance(entry, dict)]

    direct = find_by_name(projects, project_name)
    if direct:
        project_id = safe_id(direct)
        if project_id:
            return project_id

    for project in projects:
        project_id = safe_id(project)
        if not project_id:
            continue
        boards = to_list(runner.read("list_boards", {"projectId": project_id}))
        boards = [entry for entry in boards if isinstance(entry, dict)]
        if find_by_name(boards, board_name):
            project_label = str(project.get("name") or project_id)
            warnings.append(
                f"Project '{project_name}' not found; using existing project '{project_label}' because it already contains board '{board_name}'"
            )
            return project_id

    if not allow_create:
        raise RuntimeError(f"Project '{project_name}' was not found and --no-create-project was set")

    created = runner.write("create_project", {"name": project_name})
    created_id = safe_id(created)
    if not created_id:
        raise RuntimeError(f"Could not determine id for created project '{project_name}'")
    return created_id


def ensure_board(runner: SyncRunner, project_id: str, board_name: str) -> str:
    boards = to_list(runner.read("list_boards", {"projectId": project_id}))
    boards = [entry for entry in boards if isinstance(entry, dict)]

    existing = find_by_name(boards, board_name)
    if existing:
        board_id = safe_id(existing)
        if board_id:
            return board_id

    created = runner.write("create_board", {"projectId": project_id, "name": board_name})
    created_id = safe_id(created)
    if not created_id:
        raise RuntimeError(f"Could not determine id for created board '{board_name}'")
    return created_id


def ensure_lists(runner: SyncRunner, board_id: str) -> tuple[dict[str, Any], dict[str, str]]:
    board = runner.read("get_board", {"boardId": board_id})
    lists = to_list(board.get("lists") if isinstance(board, dict) else None)
    existing_by_name: dict[str, dict[str, Any]] = {}
    for entry in lists:
        if isinstance(entry, dict):
            name = str(entry.get("name") or "").strip()
            if name:
                existing_by_name[normalize_name(name)] = entry

    created_any = False
    for position, list_name in enumerate(STATUS_LIST_ORDER, start=1):
        if normalize_name(list_name) in existing_by_name:
            continue
        runner.write("create_list", {"boardId": board_id, "name": list_name, "position": position})
        created_any = True

    if created_any:
        board = runner.read("get_board", {"boardId": board_id})

    lists = to_list(board.get("lists") if isinstance(board, dict) else None)
    list_id_by_name: dict[str, str] = {}
    for entry in lists:
        if not isinstance(entry, dict):
            continue
        name = str(entry.get("name") or "").strip()
        list_id = safe_id(entry)
        if name and list_id:
            list_id_by_name[normalize_name(name)] = list_id

    missing = [value for value in STATUS_LIST_ORDER if normalize_name(value) not in list_id_by_name]
    if missing:
        raise RuntimeError(f"Missing required lists after reconciliation: {', '.join(missing)}")

    return board if isinstance(board, dict) else {}, list_id_by_name


def iter_cards(board: dict[str, Any]) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    seen: set[str] = set()

    top_level_cards = to_list(board.get("cards"))
    for card in top_level_cards:
        if not isinstance(card, dict):
            continue
        card_id = safe_id(card)
        if card_id and card_id in seen:
            continue
        if card_id:
            seen.add(card_id)
        cards.append(card)

    for list_entry in to_list(board.get("lists")):
        if not isinstance(list_entry, dict):
            continue
        for card in to_list(list_entry.get("cards")):
            if not isinstance(card, dict):
                continue
            card_id = safe_id(card)
            if card_id and card_id in seen:
                continue
            if card_id:
                seen.add(card_id)
            if "listId" not in card:
                list_id = safe_id(list_entry)
                if list_id:
                    card["listId"] = list_id
            cards.append(card)

    return cards


def merge_cards(existing: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    merged = dict(existing)

    for key, value in candidate.items():
        if key not in merged or not has_content(merged.get(key)):
            merged[key] = value

    for preferred_key in (
        "description",
        "labels",
        "labelIds",
        "listId",
        "dueDate",
        "due_date",
        "taskLists",
        "task_lists",
    ):
        if has_content(candidate.get(preferred_key)):
            merged[preferred_key] = candidate.get(preferred_key)

    return merged


def index_cards_by_name(board: dict[str, Any]) -> dict[str, dict[str, Any]]:
    cards_by_name: dict[str, dict[str, Any]] = {}
    for card in iter_cards(board):
        card_name = str(card.get("name") or "").strip()
        if not card_name:
            continue
        key = normalize_name(card_name)
        if key not in cards_by_name:
            cards_by_name[key] = dict(card)
        else:
            cards_by_name[key] = merge_cards(cards_by_name[key], card)
    return cards_by_name


def index_labels(board: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    labels_by_name: dict[str, dict[str, Any]] = {}
    labels_by_id: dict[str, dict[str, Any]] = {}

    for label in to_list(board.get("labels")):
        if not isinstance(label, dict):
            continue
        label_id = safe_id(label)
        label_name = str(label.get("name") or "").strip()
        if not label_id or not label_name:
            continue
        labels_by_name[normalize_name(label_name)] = label
        labels_by_id[label_id] = label

    for card in iter_cards(board):
        for label in to_list(card.get("labels")):
            if not isinstance(label, dict):
                continue
            label_id = safe_id(label)
            label_name = str(label.get("name") or "").strip()
            if not label_id or not label_name:
                continue
            labels_by_name.setdefault(normalize_name(label_name), label)
            labels_by_id.setdefault(label_id, label)

    return labels_by_name, labels_by_id


def release_color(version: str) -> str:
    index = sum(ord(character) for character in version) % len(RELEASE_COLOR_CYCLE)
    return RELEASE_COLOR_CYCLE[index]


def ensure_label(
    runner: SyncRunner,
    board_id: str,
    labels_by_name: dict[str, dict[str, Any]],
    labels_by_id: dict[str, dict[str, Any]],
    label_name: str,
    color: str,
    created_counter: dict[str, int],
) -> str:
    existing = labels_by_name.get(normalize_name(label_name))
    if existing:
        existing_id = safe_id(existing)
        if existing_id:
            return existing_id

    created = runner.write("create_label", {"boardId": board_id, "name": label_name, "color": color})
    created_id = safe_id(created)
    if not created_id:
        raise RuntimeError(f"Could not determine id for label '{label_name}'")

    created_label = {"id": created_id, "name": label_name, "color": color}
    labels_by_name[normalize_name(label_name)] = created_label
    labels_by_id[created_id] = created_label
    created_counter["labels"] += 1
    return created_id


def card_list_id(card: dict[str, Any]) -> str | None:
    direct = card.get("listId")
    if direct is not None:
        return str(direct)
    snake_case = card.get("list_id")
    if snake_case is not None:
        return str(snake_case)
    nested = card.get("list")
    if isinstance(nested, dict):
        nested_id = safe_id(nested)
        if nested_id:
            return nested_id
    return None


def card_label_ids(card: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    label_ids = card.get("labelIds")
    if isinstance(label_ids, list):
        for item in label_ids:
            ids.add(str(item))

    labels = card.get("labels")
    if isinstance(labels, list):
        for item in labels:
            if isinstance(item, dict):
                item_id = safe_id(item)
                if item_id:
                    ids.add(item_id)
            elif isinstance(item, (str, int)):
                ids.add(str(item))

    card_labels = card.get("cardLabels")
    if isinstance(card_labels, list):
        for item in card_labels:
            if not isinstance(item, dict):
                continue
            label_id = item.get("labelId")
            if label_id is not None:
                ids.add(str(label_id))

    return ids


def card_due_date(card: dict[str, Any]) -> str | None:
    direct = card.get("dueDate")
    if direct is not None:
        return normalize_due_date(direct)

    snake_case = card.get("due_date")
    if snake_case is not None:
        return normalize_due_date(snake_case)

    return None


def task_lists_from_card(card: dict[str, Any]) -> list[dict[str, Any]]:
    direct = card.get("taskLists")
    if isinstance(direct, list):
        return [entry for entry in direct if isinstance(entry, dict)]

    snake_case = card.get("task_lists")
    if isinstance(snake_case, list):
        return [entry for entry in snake_case if isinstance(entry, dict)]

    return []


def read_card_details(runner: SyncRunner, card_id: str, warnings: list[str]) -> dict[str, Any]:
    try:
        payload = runner.read("get_card", {"cardId": card_id})
    except (RuntimeError, MCPError, ValueError, json.JSONDecodeError) as error:
        warnings.append(f"Could not inspect card details for card {card_id}: {error}")
        return {}

    if isinstance(payload, dict):
        return payload
    return {}


def ensure_task_lists(
    runner: SyncRunner,
    card_id: str,
    cached_card: dict[str, Any],
    card_details: dict[str, Any] | None,
) -> int:
    existing_names: set[str] = set()

    for task_list in task_lists_from_card(cached_card):
        task_list_name = str(task_list.get("name") or "").strip()
        if task_list_name:
            existing_names.add(normalize_name(task_list_name))

    if isinstance(card_details, dict):
        for task_list in task_lists_from_card(card_details):
            task_list_name = str(task_list.get("name") or "").strip()
            if task_list_name:
                existing_names.add(normalize_name(task_list_name))

    created = 0
    for task_list_name in DEFAULT_TASK_LISTS:
        normalized = normalize_name(task_list_name)
        if normalized in existing_names:
            continue
        runner.write("create_task_list", {"cardId": card_id, "name": task_list_name})
        existing_names.add(normalized)
        created += 1

    return created


def render_description(epic: EpicRecord) -> str:
    return "\n".join(
        [
            f"**Release**: {epic.release_version} - {epic.release_title}",
            f"**Priority**: {epic.priority}",
            f"**Status (Roadmap)**: {epic.status}",
            "**Roadmap Source**: `agent-output/roadmap/product-roadmap.md`",
            "",
            "---",
            "",
            epic.markdown_block.strip(),
        ]
    ).strip()


def render_status_line(status: str, card_id: str, board_id: str) -> str:
    return f"**Status**: {status} [CardID: {card_id}] [BoardID: {board_id}]"


def update_roadmap_status_ids(
    roadmap_path: Path,
    epics: list[EpicRecord],
    epic_cards: list[dict[str, str]],
    apply_changes: bool,
    warnings: list[str],
) -> int:
    original_text = roadmap_path.read_text(encoding="utf-8")
    lines = original_text.splitlines()
    had_trailing_newline = original_text.endswith("\n")

    card_map: dict[tuple[str, str], dict[str, str]] = {}
    for entry in epic_cards:
        epic_name = str(entry.get("epic") or "").strip()
        release = str(entry.get("release") or "").strip()
        if not epic_name or not release:
            continue
        card_map[(normalize_name(epic_name), release)] = entry

    changed = 0
    for epic in epics:
        if epic.status_line_index is None:
            warnings.append(f"No **Status** line found for {epic.card_name}; skipped roadmap id write-back")
            continue

        if epic.status_line_index < 0 or epic.status_line_index >= len(lines):
            warnings.append(f"Status line index out of range for {epic.card_name}; skipped roadmap id write-back")
            continue

        mapped = card_map.get((normalize_name(epic.card_name), epic.release_version))
        if not mapped:
            warnings.append(f"No card mapping found for {epic.card_name}; skipped roadmap id write-back")
            continue

        card_id = str(mapped.get("cardId") or "").strip()
        board_id = str(mapped.get("boardId") or "").strip()
        if not card_id or not board_id:
            warnings.append(f"Missing cardId/boardId for {epic.card_name}; skipped roadmap id write-back")
            continue

        existing = lines[epic.status_line_index]
        prefix = existing[: len(existing) - len(existing.lstrip())]
        desired = f"{prefix}{render_status_line(epic.status, card_id, board_id)}"
        if existing != desired:
            lines[epic.status_line_index] = desired
            changed += 1

    if changed > 0 and apply_changes:
        updated = "\n".join(lines)
        if had_trailing_newline:
            updated += "\n"
        roadmap_path.write_text(updated, encoding="utf-8")

    return changed


def parse_args() -> argparse.Namespace:
    repo_root = SCRIPT_DIR.parents[3]
    parser = argparse.ArgumentParser(description="Synchronize all roadmap epics to Planka board cards")
    parser.add_argument("--mcp-url", default="http://localhost:25478/mcp")
    parser.add_argument("--roadmap", default=str(repo_root / "agent-output/roadmap/product-roadmap.md"))
    parser.add_argument("--project-name", default="Product Roadmap")
    parser.add_argument("--board-name", default="Epics")
    parser.add_argument("--no-create-project", action="store_true")
    parser.add_argument(
        "--no-write-roadmap-status",
        action="store_true",
        help="Do not persist [CardID]/[BoardID] metadata back into roadmap epic status lines",
    )
    parser.add_argument(
        "--ensure-task-lists",
        action="store_true",
        help="Ensure default agile task lists exist on each epic card (bootstrap mode)",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    roadmap_path = Path(args.roadmap).resolve()

    if not roadmap_path.exists():
        raise RuntimeError(f"Roadmap file not found: {roadmap_path}")

    epics, parse_warnings = parse_roadmap_epics(roadmap_path)
    if not epics:
        raise RuntimeError(f"No epics were parsed from roadmap: {roadmap_path}")

    client = MCPClient(args.mcp_url)
    client.initialize()
    runner = SyncRunner(client=client, dry_run=bool(args.dry_run))

    warnings: list[str] = list(parse_warnings)
    created_counter = {"labels": 0}
    stats = {
        "epics_parsed": len(epics),
        "cards_created": 0,
        "cards_moved": 0,
        "cards_updated": 0,
        "task_lists_created": 0,
        "labels_created": 0,
        "labels_added": 0,
        "labels_removed": 0,
    }
    epic_cards: list[dict[str, str]] = []

    project_id = ensure_project(
        runner=runner,
        project_name=args.project_name,
        board_name=args.board_name,
        allow_create=not args.no_create_project,
        warnings=warnings,
    )
    board_id = ensure_board(runner=runner, project_id=project_id, board_name=args.board_name)
    board, list_id_by_name = ensure_lists(runner=runner, board_id=board_id)

    labels_by_name, labels_by_id = index_labels(board)
    cards_by_name = index_cards_by_name(board)

    for epic in epics:
        target_list_id = list_id_by_name[normalize_name(epic.status)]
        key = normalize_name(epic.card_name)
        card = cards_by_name.get(key)

        if not card:
            created_card = runner.write("create_card", {"listId": target_list_id, "name": epic.card_name})
            card_id = safe_id(created_card)
            if not card_id:
                raise RuntimeError(f"Could not determine id for created card '{epic.card_name}'")
            card = {
                "id": card_id,
                "name": epic.card_name,
                "listId": target_list_id,
                "description": "",
                "labels": [],
            }
            cards_by_name[key] = card
            stats["cards_created"] += 1

        card_id = safe_id(card)
        if not card_id:
            raise RuntimeError(f"Card without id encountered for '{epic.card_name}'")

        card_details = read_card_details(runner=runner, card_id=card_id, warnings=warnings)
        if card_details:
            card = merge_cards(card, card_details)
            cards_by_name[key] = card

        existing_list_id = card_list_id(card)
        if existing_list_id != target_list_id:
            runner.write("move_card", {"cardId": card_id, "listId": target_list_id})
            card["listId"] = target_list_id
            stats["cards_moved"] += 1

        desired_description = render_description(epic)
        current_description = str(card.get("description") or "")
        expected_due_date = desired_due_date(epic.target_date)
        current_due_date = card_due_date(card)

        card_update: dict[str, Any] = {"cardId": card_id}
        if current_description.strip() != desired_description.strip():
            card_update["description"] = desired_description

        if expected_due_date and current_due_date != expected_due_date:
            card_update["dueDate"] = expected_due_date

        if len(card_update) > 1:
            runner.write("update_card", card_update)
            if "description" in card_update:
                card["description"] = desired_description
            if "dueDate" in card_update:
                card["dueDate"] = expected_due_date
            stats["cards_updated"] += 1

        release_label_name = f"Release {epic.release_version}"
        priority_label_name = f"Priority {epic.priority}"
        release_label_id = ensure_label(
            runner=runner,
            board_id=board_id,
            labels_by_name=labels_by_name,
            labels_by_id=labels_by_id,
            label_name=release_label_name,
            color=release_color(epic.release_version),
            created_counter=created_counter,
        )
        priority_label_id = ensure_label(
            runner=runner,
            board_id=board_id,
            labels_by_name=labels_by_name,
            labels_by_id=labels_by_id,
            label_name=priority_label_name,
            color=PRIORITY_COLORS.get(epic.priority, "light-concrete"),
            created_counter=created_counter,
        )

        required_labels = {release_label_id, priority_label_id}
        current_labels = card_label_ids(card)

        removable_labels: list[str] = []
        for label_id in current_labels:
            label = labels_by_id.get(label_id)
            label_name = str(label.get("name") if isinstance(label, dict) else "")
            if label_name.startswith("Release ") or label_name.startswith("Priority "):
                if label_id not in required_labels:
                    removable_labels.append(label_id)

        for label_id in sorted(removable_labels):
            runner.write("remove_label_from_card", {"cardId": card_id, "labelId": label_id})
            current_labels.discard(label_id)
            stats["labels_removed"] += 1

        for label_id in sorted(required_labels - current_labels):
            runner.write("add_label_to_card", {"cardId": card_id, "labelId": label_id})
            current_labels.add(label_id)
            stats["labels_added"] += 1

        if args.ensure_task_lists:
            stats["task_lists_created"] += ensure_task_lists(
                runner=runner,
                card_id=card_id,
                cached_card=card,
                card_details=card_details,
            )

        card["labelIds"] = sorted(current_labels)
        epic_cards.append(
            {
                "epic": epic.card_name,
                "release": epic.release_version,
                "status": epic.status,
                "priority": epic.priority,
                "cardId": card_id,
                "boardId": board_id,
            }
        )

    stats["labels_created"] = created_counter["labels"]
    roadmap_apply = not args.no_write_roadmap_status and not args.dry_run
    stats["roadmap_status_lines_updated"] = update_roadmap_status_ids(
        roadmap_path=roadmap_path,
        epics=epics,
        epic_cards=epic_cards,
        apply_changes=roadmap_apply,
        warnings=warnings,
    )

    output = {
        "mode": "dry-run" if args.dry_run else "apply",
        "roadmap": str(roadmap_path),
        "roadmapStatusWrite": "disabled" if args.no_write_roadmap_status else ("applied" if roadmap_apply else "preview"),
        "projectId": project_id,
        "boardId": board_id,
        "stats": stats,
        "warnings": warnings,
        "epicCards": epic_cards,
        "operations": runner.actions,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, MCPError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"error": str(error)}, indent=2), file=sys.stderr)
        sys.exit(1)