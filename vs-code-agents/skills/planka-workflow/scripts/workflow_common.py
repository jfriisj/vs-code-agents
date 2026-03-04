#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REQUIRED_LISTS = [
    "01-Roadmap",
    "02-Planner",
    "03-Analyst",
    "04-Architect",
    "05-Security",
    "06-Critic",
    "07-Implementer",
    "08-Code Reviewer",
    "09-QA",
    "10-UAT",
    "11-DevOps",
    "12-Retrospective",
    "13-Process Improvement",
    "Blocked",
    "Closed",
]


DEFAULT_WORKFLOW_STATE_FILE = "agent-output/planka/workflow-index.md"


AGENT_ALIASES = {
    "01-roadmap": "01-Roadmap",
    "roadmap": "01-Roadmap",
    "02-planner": "02-Planner",
    "planner": "02-Planner",
    "03-analyst": "03-Analyst",
    "analyst": "03-Analyst",
    "04-architect": "04-Architect",
    "architect": "04-Architect",
    "05-security": "05-Security",
    "security": "05-Security",
    "06-critic": "06-Critic",
    "critic": "06-Critic",
    "07-implementer": "07-Implementer",
    "implementer": "07-Implementer",
    "08-code reviewer": "08-Code Reviewer",
    "08-code-reviewer": "08-Code Reviewer",
    "code reviewer": "08-Code Reviewer",
    "reviewer": "08-Code Reviewer",
    "09-qa": "09-QA",
    "qa": "09-QA",
    "10-uat": "10-UAT",
    "uat": "10-UAT",
    "11-devops": "11-DevOps",
    "devops": "11-DevOps",
    "12-retrospective": "12-Retrospective",
    "retrospective": "12-Retrospective",
    "13-process improvement": "13-Process Improvement",
    "13-pi": "13-Process Improvement",
    "pi": "13-Process Improvement",
    "process improvement": "13-Process Improvement",
    "blocked": "Blocked",
    "closed": "Closed",
}


def normalize_agent_list(value: str) -> str:
    cleaned = value.strip()
    if cleaned in REQUIRED_LISTS:
        return cleaned

    alias = AGENT_ALIASES.get(cleaned.lower())
    if alias:
        return alias

    raise ValueError(
        f"Unknown agent/list '{value}'. Expected one of {REQUIRED_LISTS} or known aliases."
    )


def now_iso() -> str:
    return datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat()


def slugify(value: str, limit: int = 40) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    if not normalized:
        normalized = "workflow"
    return normalized[:limit].rstrip("-")


def build_workflow_description(
    workflow_id: str,
    origin: str,
    uuid: str,
    artifact: str,
    status: str,
    agent: str,
    synced_at: str,
) -> str:
    return "\n".join(
        [
            f"ID: {workflow_id}",
            f"Origin: {origin}",
            f"UUID: {uuid}",
            f"Primary Markdown Artifact: {artifact}",
            f"Current Status: {status}",
            f"Current Agent: {agent}",
            f"Last Synced At: {synced_at}",
        ]
    )


def upsert_description_field(description: str, field: str, value: str) -> str:
    line_prefix = f"{field}:"
    lines = description.splitlines() if description else []

    for index, line in enumerate(lines):
        if line.startswith(line_prefix):
            lines[index] = f"{line_prefix} {value}"
            return "\n".join(lines)

    lines.append(f"{line_prefix} {value}")
    return "\n".join(lines).strip()


def extract_project_id(board: dict[str, Any]) -> str | None:
    project_id = board.get("projectId")
    if project_id:
        return str(project_id)

    project = board.get("project")
    if isinstance(project, dict) and project.get("id"):
        return str(project["id"])

    return None


def load_workflow_index(state_file: str | Path) -> dict[str, dict[str, str]]:
    path = Path(state_file)
    if not path.exists():
        return {}

    content = path.read_text(encoding="utf-8").strip()
    if not content:
        return {}

    match = re.search(r"```json\s*(\{.*?\})\s*```", content, re.DOTALL)
    if not match:
        raise ValueError(f"Workflow index markdown is malformed: {path}")

    payload = json.loads(match.group(1))
    workflows = payload.get("workflows", {}) if isinstance(payload, dict) else {}
    if not isinstance(workflows, dict):
        raise ValueError(f"Workflow index payload is malformed: {path}")

    normalized: dict[str, dict[str, str]] = {}
    for workflow_id, mapping in workflows.items():
        if not isinstance(mapping, dict):
            continue
        normalized[str(workflow_id)] = {
            str(key): "" if value is None else str(value)
            for key, value in mapping.items()
        }

    return normalized


def save_workflow_index(state_file: str | Path, workflows: dict[str, dict[str, str]]) -> None:
    path = Path(state_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = {"workflows": workflows}
    content = "\n".join(
        [
            "# Planka Workflow Index",
            "",
            "Markdown source-of-truth mapping between workflow IDs and Planka entities.",
            "Use this file for cross-instance recovery and reconciliation.",
            "",
            "```json",
            json.dumps(payload, indent=2, sort_keys=True),
            "```",
            "",
        ]
    )
    path.write_text(content, encoding="utf-8")


def get_workflow_mapping(state_file: str | Path, workflow_id: str) -> dict[str, str] | None:
    workflows = load_workflow_index(state_file)
    mapping = workflows.get(str(workflow_id))
    if not mapping:
        return None
    return dict(mapping)


def upsert_workflow_mapping(
    state_file: str | Path,
    workflow_id: str,
    mapping: dict[str, Any],
) -> dict[str, str]:
    workflows = load_workflow_index(state_file)
    current = workflows.get(str(workflow_id), {})
    updated: dict[str, str] = dict(current)

    for key, value in mapping.items():
        updated[str(key)] = "" if value is None else str(value)

    updated["workflowId"] = str(workflow_id)
    workflows[str(workflow_id)] = updated
    save_workflow_index(state_file, workflows)
    return updated
