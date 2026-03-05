# Planka Agile Feature Coverage Matrix

This matrix defines the **Visual Agile** operational contract for Planka MCP. Markdown remains the source of truth; Planka provides live, visual execution tracking through native Kanban features.

| Agile Feature | MCP / Script Surface | Required Usage |
|---|---|---|
| **Bulk Epic Sync** | `sync_roadmap_epics.py`, `project:create`, `board:create`, `list:create`, `card:create`, `card:update`, `card:move` | Roadmap agent reconciles all roadmap epics in one run, not only the current epic. |
| **Lifecycle Movement** | `card:move` | Move Epic card across status lists (`Planned` → `In Progress` → `Delivered`). |
| **Roadmap Due Dates** | `card:update` (`dueDate`) | Sync card due date from roadmap release `**Target Date**` for delivery visibility. |
| **Task-List Scaffolding** | `get_card`, `tasklist:create` | Optional bootstrap mode (`--ensure-task-lists`) to ensure baseline agile task lists exist on every epic card before agent execution starts. |
| **Progress Tracking** | `tasklist:create`, `task:create`, `task:update` | Agents create Task Lists for their domains and check off tasks (`isCompleted=true`) to drive the visual Progress Bar. |
| **Release/Priority Taxonomy** | `label:create`, `label:add`, `label:remove` | Every epic card carries `Release vX.Y.Z` + `Priority PX` labels for roadmap overview. |
| **Roadmap Traceability** | `sync_roadmap_epics.py` status write-back | Persist `CardID` and `BoardID` in each epic `**Status**` line (default on) for low-token downstream lookups. |
| **Visual Status** | `label:create`, `label:add`, `label:remove` | Use additional color-coded status labels (e.g., "QA Passed", "Blocked") only when they add operational clarity. |
| **Single Source of Truth** | `card:update` (description) | Agents append links to their generated markdown artifacts in the card description. |
| **Time Tracking** | `stopwatch:start`, `stopwatch:stop` | Track active execution time per agent phase. |
| **Audit Trail** | `comment:add` | Add concise handoff summaries, verdicts, and key decisions. |
| **Token Efficiency** | `get_board` + local diff + minimal writes | One board snapshot per run; write only changed entities; allow targeted `get_card` reads only when needed (task-list bootstrap or missing metadata). |

## Deprecated Features (Do Not Use)
- Moving cards between agent-specific lists (e.g., from a "Planner" list to an "Analyst" list).
- The `bootstrap_workflow_board.py` and `sync_workflow_handoff.py` scripts (replaced completely by `planka_ops.py run --op ...`).

## Validation Rule
Before claiming lifecycle sync is complete, verify:
1. Every agent (01→13) interacts with the Epic Card using `planka_ops.py`.
2. Roadmap reconciliation covers all epics in `product-roadmap.md`, not only active ones.
3. Every epic card includes release and priority labels.
4. The board uses Task Lists, Labels, and Description updates for visibility rather than comment-spam or list-bouncing.