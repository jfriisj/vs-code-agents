---
name: planka-workflow
description: Agile Epic Management and synchronization contract for Planka MCP. Markdown remains the source of truth; Planka provides live agile execution visibility via Native MCP Tools.
license: MIT
metadata:
  author: groupzer0
  version: "3.0"
---

# Planka Workflow (Agile Epic Management)

Unified Agile workflow tracking with Planka boards.

Use this skill when:
- Synchronizing Epics from the project roadmap to Planka.
- Breaking down Acceptance Criteria into actionable Tasks.
- Executing cross-functional work (Analysis, Architecture, Security, QA) on a shared Epic.
- Tracking execution time and status transitions.

---

## The Triad of Truth Architecture

Our system strictly follows a three-pillar architecture for state, context, and execution:

1. **Markdown (`agent-output/`)**: "What" and "Why". The canonical source of truth containing full artifacts (plans, ADRs, analyses).
2. **Obsidian Graph (`workflows/`)**: "How it connects". Our memory graph using `mcp-obsidian/*` tools. Follows the strict "10-Line Rule" (`WF-[ID]` nodes with YAML frontmatter, `## Summary`, and `## Artifacts`).
3. **Planka Board**: "Who does what and status". The live operational Agile Kanban view tracking Epics, Tasks, time, and delivery state using **Native Planka MCP Tools**.

When conflicts occur:
1. Trust the Markdown artifacts in `agent-output/` first.
2. Ensure the Obsidian `WF-[ID]` node correctly points to the artifact.
3. Update Planka to match the Markdown/Obsidian state.
4. Add a comment on the Planka card detailing the reconciliation.

---

## Board Granularity & Structure

**Rule**: One master Project for the Roadmap, containing an "Epics" board.

**Project**: Use the actual project name (derived from the first `#` heading in `agent-output/roadmap/product-roadmap.md`, before ` - Product Roadmap`, or set explicitly with `--project-name`).
**Board**: `Epics`

Create lists in this exact order to represent the Epic Lifecycle:
1. `Planned` (Backlog and upcoming Epics)
2. `In Progress` (Actively being planned, developed, or tested)
3. `Delivered` (Successfully deployed to production)
4. `Deferred` (Paused or waived)
5. `Closed` (Terminal state)

---

## Card Model (The Epic)

Each Card represents a single **Epic**.
- **Card Name**: `Epic [X.Y]: [Title]`
- **Description**: Contains the full Epic Markdown Template from the Roadmap (User Story, Business Value, Dependencies, Acceptance Criteria, Constraints), plus a link to the root Obsidian Epic node (`**Obsidian Root Node**: [[WF-Epic-ID]]`).

### Task Lists (Agent Workspaces)
Instead of moving cards between agent-specific lists, the card stays in its Status List (e.g., `In Progress`). Agents create and manage their own **Task Lists** inside the Epic card:

- `Acceptance Criteria` (Managed by Planner)
- `Analysis & Spikes` (Managed by Analyst)
- `Architecture & Design` (Managed by Architect)
- `Security & Compliance` (Managed by Security)
- `Implementation` (Managed by Implementer)
- `Code Review` (Managed by Code Reviewer)
- `QA & Testing` (Managed by QA)
- `UAT & Acceptance` (Managed by UAT)
- `Release & Deployment` (Managed by DevOps)
- `Retrospective & Learnings` (Managed by Retrospective/PI)

---

## Synchronization Protocol

### 1. Portfolio Reconciliation (Roadmap Agent)
Whenever the roadmap changes in `product-roadmap.md`:
- Reconcile **all releases and all epics** to Planka in one pass using the `sync_roadmap_epics.py` script.
- Ensure Project, Board, and Status Lists exist.
- Ensure every roadmap epic exists as a card, is in the matching lifecycle list, and has updated description + due date (from release `**Target Date**` when available).
- Ensure labels for release and priority are present on each epic card.

### Label Taxonomy (Portfolio Overview)
- `Release vX.Y.Z` label on every epic for release grouping.
- `Priority P0|P1|P2|P3` label on every epic for criticality overview.
- Keep labels stable and reused by name; do not create duplicates with variant naming.

### 2. Task Breakdown (Planner Agent)
When planning an Epic:
- Read the Epic Card's description to fetch Acceptance Criteria.
- Create a Task List for the Acceptance Criteria (`create_task_list` tool).
- Add individual execution Tasks (`create_task` tool).

### 3. Active Execution (All specialized agents)
When an agent (Analyst, Architect, Security, Implementer, QA, Code Reviewer) works on an Epic, they MUST use **Native MCP Tools** (e.g., `call_tool`), NOT terminal scripts:
- **Start Stopwatch**: Call `update_card` to track time spent.
- **Create Workspace**: If missing, call `create_task_list` to create your specific Task List.
- **Log Tasks**: Add tasks via `create_task` and mark complete via `update_task` (`isCompleted: true`).
- **Complete Work**: Stop the stopwatch via `update_card`.
- **Handoff / Report**: Call `add_comment` summarizing findings. **CRITICAL**: You must include a link to your generated Markdown artifact AND your Obsidian workflow node (e.g., `[[WF-NNN-Feature]]`) to bridge the Planka execution board with our Obsidian memory graph.

### 4. Terminal Lifecycle (DevOps & UAT)
When an Epic is deployed:
- DevOps moves the Epic Card to the `Delivered` list (`move_card` tool).
- UAT and DevOps leave final approval and deployment comments (linking to final release nodes).

---

## Operational Guidance

### 1. Bulk Roadmap Synchronization (Python CLI)
Only the `01-Roadmap` agent uses the terminal for bulk synchronization via `sync_roadmap_epics.py`:

```bash
# Parse roadmap and preview all required changes
python .github/skills/planka-workflow/scripts/sync_roadmap_epics.py --dry-run

# Apply full reconciliation
python .github/skills/planka-workflow/scripts/sync_roadmap_epics.py

# Optional bootstrap: auto-create default agile task lists on each epic card
python .github/skills/planka-workflow/scripts/sync_roadmap_epics.py --ensure-task-lists

```

### 2. Daily Agent Operations (Native MCP)

**CRITICAL**: Do NOT use bash or `planka_ops.py` for daily operations. Use the exposed native Planka tools directly.

* **Discovery**: `list_projects`, `list_boards`, `get_board`, `get_card`
* **Card & List management**: `create_card`, `update_card`, `move_card`
* **Task management**: `create_task_list`, `create_task`, `update_task`
* **Audit trail & Triad Bridge**: `add_comment` (must include `[[WF-ID]]` and artifact link)
* **Time tracking**: `update_card` (modifying the stopwatch field)
* **Visual Status**: `create_label`, `add_label_to_card`

Prefer idempotent actions:

* List/find before create.
* Update/move only when state differs.
* Keep comments sparse and meaningful; description + labels + tasks should carry primary operational state.
