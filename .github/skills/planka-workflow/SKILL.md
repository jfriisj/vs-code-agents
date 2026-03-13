---
name: planka-workflow
description: Agile Epic Management and synchronization contract for Planka MCP. Markdown remains the source of truth; Planka provides live agile execution visibility via Native MCP Tools exclusively. Python scripts are strictly forbidden.
license: MIT
metadata:
  author: groupzer0
  version: "4.0"
---

# Planka Workflow (Agile Epic Management)

Unified Agile workflow tracking with Planka boards.

Use this skill when:
- Synchronizing Epics from the project roadmap to Planka.
- Breaking down Acceptance Criteria into actionable Tasks.
- Executing cross-functional work (Analysis, Architecture, Security, QA) on a shared Epic.
- Tracking execution time and status transitions.

---

## 1. The Triad of Truth Architecture

Our system strictly follows a three-pillar architecture for state, context, and execution:

1. **Markdown (`agent-output/`)**: "What" and "Why". The canonical source of truth.
2. **Obsidian Graph (`workflows/`)**: "How it connects". Our memory graph using `mcp-obsidian/*` tools (10-Line Rule).
3. **Planka Board**: "Who does what and status". The live operational Agile Kanban view using **Native Planka MCP Tools**.

**When conflicts occur:**
1. Trust the Markdown artifacts in `agent-output/` first.
2. Ensure the Obsidian `WF-[ID]` node correctly points to the artifact.
3. Update Planka to match the Markdown/Obsidian state.
4. Add a comment on the Planka card detailing the reconciliation.

---

## 2. Board & Card Structure

**Project**: Use the project name derived from the first `#` heading in `agent-output/roadmap/product-roadmap.md`.
**Board**: `Epics`

**Status Lists (Lifecycle):**
1. `Planned`
2. `In Progress`
3. `Delivered`
4. `Deferred`
5. `Closed`

**The Epic Card:**
- **Title**: `Epic [X.Y]: [Title]`
- **Description**: Contains User Story, Business Value, Dependencies, Acceptance Criteria, and the `**Obsidian Root Node**: [[WF-Epic-ID]]`.
- **Labels**: `Release vX.Y.Z`, `Priority P0|P1|P2|P3`, plus specific status labels (e.g., `QA Passed`).

---

## 3. Agent Workspaces (Task Lists)

Instead of moving cards between columns, the card stays in its Status List. Agents create and manage their own **Task Lists** inside the Epic card:

- `Acceptance Criteria` (Planner)
- `Analysis & Spikes` (Analyst)
- `Architecture & Design` (Architect)
- `Security & Compliance` (Security)
- `Implementation` (Implementer)
- `Code Review` (Code Reviewer)
- `QA & Testing` (QA)
- `UAT & Acceptance` (UAT)
- `Release & Deployment` (DevOps)
- `Retrospective & Learnings` (Retrospective/PI)

---

## 4. Operational Guidance (Strictly Native MCP)

**CRITICAL RULE**: Terminal CLI wrappers and Python scripts (like `sync_roadmap_epics.py` or `planka_ops.py`) are **strictly forbidden**. All agents MUST use Native MCP Tools.

### Native Tool Calling:
* **Discovery**: `list_projects`, `list_boards`, `get_board`, `get_card`
* **Card & List management**: `create_card`, `update_card`, `move_card`
* **Task management**: `create_task_list`, `create_task`, `update_task` (set `isCompleted: true` to drive progress bar)
* **Visual Status**: `create_label`, `add_label_to_card`
* **Audit trail & Triad Bridge**: `add_comment` (must include `[[WF-ID]]` and artifact link)
* **Time tracking**: `update_card` (modifying the stopwatch field)

---

## 5. Agent Workflow Playbook

When an agent works on an Epic, they **MUST** follow this execution order:

1. **Update Markdown**: Save work in `agent-output/`.
2. **Update Obsidian**: Create/update the `WF-[ID]` node (10-Line Rule).
3. **Start Time**: Call `update_card` to start the stopwatch.
4. **Task Lists**: Call `create_task_list` (if missing) and log actionable items via `create_task`. Complete them via `update_task`.
5. **Labels**: Apply visual status labels via `add_label_to_card`.
6. **Handoff & Artifacts**: Call `add_comment` to leave a verdict. Include links to the markdown artifact and the `[[WF-ID]]` node.
7. **Stop Time**: Call `update_card` to stop the stopwatch.

---

## 6. Workflow Index

For cross-instance recovery, agents should maintain `agent-output/planka/workflow-index.md` as a JSON block mapping the Triad:

```json
{
  "workflows": {
    "WF-000-example": {
      "boardId": "<board-id>",
      "cardId": "<card-id>",
      "currentAgent": "01-Roadmap",
      "currentStatus": "Planned",
      "primaryArtifact": "agent-output/planning/NNN-plan.md",
      "obsidianNode": "[[WF-000-example]]"
    }
  }
}