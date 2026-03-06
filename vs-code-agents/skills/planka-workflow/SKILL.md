---
name: planka-workflow
description: Agile Epic Management and synchronization contract for Planka MCP. Markdown remains the source of truth; Planka provides live agile execution visibility.
license: MIT
metadata:
  author: groupzer0
  version: "2.0"
---

# Planka Workflow (Agile Epic Management)

Unified Agile workflow tracking with Planka boards.

Use this skill when:
- Synchronizing Epics from the Product Roadmap to Planka.
- Breaking down Acceptance Criteria into actionable Tasks.
- Executing cross-functional work (Analysis, Architecture, Security, QA) on a shared Epic.
- Tracking execution time and status transitions.

---

## Source of Truth Model

**Canonical source**: Markdown artifacts in `agent-output/` (specifically `product-roadmap.md` and individual planning/domain docs).

Planka is the synchronized operational execution view:
- **Planka**: Live Agile board tracking Epics, Tasks, and delivery status.
- **Memory**: Durable context for decisions, constraints, and IDs.

When conflicts occur:
1. Trust the Markdown artifacts first.
2. Update Planka to match the Markdown state.
3. Add a comment on the Planka card detailing the reconciliation.

---

## Board Granularity & Structure

**Rule**: One master Project for the Roadmap, containing an "Epics" board.

**Project**: `Product Roadmap`
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
- **Description**: Contains the full Epic Markdown Template from the Roadmap (User Story, Business Value, Dependencies, Acceptance Criteria, Constraints).

### Task Lists (Agent Workspaces)
Instead of moving cards between agent-specific lists, the card stays in its Status List (e.g., `In Progress`). Agentes create and manage their own **Task Lists** inside the Epic card:

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
- Reconcile **all releases and all epics** to Planka in one pass (not only the currently-started epic).
- Ensure Project, Board, and Status Lists exist (`project:create`, `board:create`, `list:create`).
- Ensure every roadmap epic exists as a card, is in the matching lifecycle list, and has updated description + due date (from release `**Target Date**` when available).
- Ensure labels for release and priority are present on each epic card.
- Optionally bootstrap default agile task lists on each epic card (`--ensure-task-lists`) so downstream agents can execute directly in Planka.

### Label Taxonomy (Portfolio Overview)
- `Release vX.Y.Z` label on every epic for release grouping.
- `Priority P0|P1|P2|P3` label on every epic for criticality overview.
- Keep labels stable and reused by name; do not create duplicates with variant naming.

### 2. Task Breakdown (Planner Agent)
When planning an Epic:
- Read the Epic Card's description to fetch Acceptance Criteria.
- Create a Task List for the Acceptance Criteria (`tasklist:create`).
- Add individual execution Tasks (`task:create`).

### 3. Active Execution (All specialized agents)
When an agent (Analyst, Architect, Security, Implementer, QA, Code Reviewer) works on an Epic:
- **Start Stopwatch**: `stopwatch:start` to track time spent.
- **Create Workspace**: If missing, create your specific Task List (`tasklist:create`).
- **Log Tasks**: Add tasks for the specific checks, code, or validations you perform (`task:create`).
- **Complete Work**: Stop the stopwatch (`stopwatch:stop`).
- **Handoff / Report**: Add a comment summarizing the findings/verdict and link to your generated markdown artifact (`comment:add`).

### 4. Terminal Lifecycle (DevOps & UAT)
When an Epic is deployed:
- DevOps moves the Epic Card to the `Delivered` list (`card:move`).
- UAT and DevOps leave final approval and deployment comments.

---

## Script Helpers

The primary engine for Planka operations is `planka_ops.py`. 
*Note: The old `bootstrap_workflow_board.py` and `sync_workflow_handoff.py` are legacy scripts from the "Status-Only" model and should generally be avoided in favor of direct Agile operations via `planka_ops.py`.*

For roadmap-level synchronization, prefer `sync_roadmap_epics.py`:

```bash
# Parse roadmap and preview all required changes
python .github/skills/planka-workflow/scripts/sync_roadmap_epics.py --dry-run

# Apply full reconciliation (all epics, lists, labels, descriptions, due dates)
python .github/skills/planka-workflow/scripts/sync_roadmap_epics.py

# Optional: do not write [CardID]/[BoardID] metadata back to roadmap Status lines
python .github/skills/planka-workflow/scripts/sync_roadmap_epics.py --no-write-roadmap-status

# Optional bootstrap: auto-create default agile task lists on each epic card
python .github/skills/planka-workflow/scripts/sync_roadmap_epics.py --ensure-task-lists
```

By default, `sync_roadmap_epics.py` also writes `CardID` and `BoardID` into each epic's roadmap `**Status**` line for downstream agent traceability.

For cross-instance mapping, keep `agent-output/planka/workflow-index.md` aligned to `references/workflow-index-template.md`.

**Usage Example:**
```bash
# Create Task List
python .github/skills/planka-workflow/scripts/planka_ops.py run \
  --op tasklist:create --arg cardId=<id> --arg name="QA & Testing"

# Add Task
python .github/skills/planka-workflow/scripts/planka_ops.py run \
  --op task:create --arg taskListId=<id> --arg name="Test edge case X"

# Add Comment (Handoff/Verdict)
python .github/skills/planka-workflow/scripts/planka_ops.py run \
  --op comment:add --arg cardId=<id> --arg text="QA Passed. Ready for UAT."

# Move Card (Change Status)
python .github/skills/planka-workflow/scripts/planka_ops.py run \
  --op card:move --arg cardId=<id> --arg listId=<delivered_list_id>
```

---

## Tool Usage Guidance

Use Planka MCP operations (`planka_ops.py`) for:
- Discovery (`list_projects`, `list_boards`, `get_board`, `get_card`)
- Card & List management (`create_card`, `update_card`, `move_card`)
- Task management (`create_task_list`, `create_task`, `update_task`)
- Audit trail (`add_comment`)
- Time tracking (`stopwatch:start`, `stopwatch:stop`)

Prefer idempotent actions:
- List/find before create.
- Update/move only when state differs.

## Token & Quality Optimization Contract

For high-quality low-token operation:
- Do one board snapshot (`get_board`) per reconciliation run and compute diffs locally.
- Allow targeted per-card fetch (`get_card`) only for task-list hydration and when board payload lacks required fields.
- Write only changed entities (create missing cards/lists/labels, move status drift, update changed descriptions/due dates; create task-lists only when `--ensure-task-lists` is enabled).
- Reuse existing labels by canonical names (`Release vX.Y.Z`, `Priority PX`) and remove obsolete release/priority labels from cards when needed.
- Keep comments sparse and meaningful; description + labels + tasks should carry primary operational state.