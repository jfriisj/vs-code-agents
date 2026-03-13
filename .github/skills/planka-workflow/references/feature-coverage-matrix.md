# Planka Agile Feature Coverage Matrix

This matrix defines the **Visual Agile** operational contract for Planka MCP. It strictly adheres to the **Triad of Truth**: Markdown (What/Why), Obsidian (Memory/Context), and Planka (Execution/Status).

| Agile Feature | Native MCP Tool / Script | Required Usage |
|---|---|---|
| **Bulk Epic Sync** | `sync_roadmap_epics.py` (Terminal Script) | Roadmap agent reconciles all roadmap epics in one run, not only the current epic. |
| **Lifecycle Movement** | `move_card` | Move Epic card across status lists (`Planned` → `In Progress` → `Delivered`). |
| **Roadmap Due Dates** | `update_card` (`dueDate`) | Sync card due date from roadmap release `**Target Date**` for delivery visibility. |
| **Task-List Scaffolding** | `create_task_list` | Optional bootstrap mode (`--ensure-task-lists` in sync script) or created dynamically by agents before execution starts. |
| **Progress Tracking** | `create_task_list`, `create_task`, `update_task` | Agents create Task Lists for their domains and check off tasks (`isCompleted: true`) to drive the visual Progress Bar. |
| **Release/Priority Taxonomy** | `create_label`, `add_label_to_card`, `remove_label_from_card` | Every epic card carries `Release vX.Y.Z` + `Priority PX` labels for roadmap overview. |
| **Visual Status** | `create_label`, `add_label_to_card` | Use additional color-coded status labels (e.g., "QA Passed", "Blocked") only when they add operational clarity. |
| **The Triad Bridge** | `update_card` (description) or `add_comment` | Agents MUST append links to their generated markdown artifacts (`agent-output/...`) AND their Obsidian nodes (`[[WF-NNN]]`). |
| **Time Tracking** | `update_card` (stopwatch) | Track active execution time per agent phase by starting and stopping the card's stopwatch. |
| **Audit Trail** | `add_comment` | Add concise handoff summaries, verdicts, and key decisions (always including the `[[WF-ID]]` link). |

## Deprecated Features (Do Not Use)
- **Terminal CLI Wrappers**: Using `planka_ops.py run --op ...` or `$PLANKA_OPS` in the terminal is deprecated for standard agents. Agents must use **Native MCP Tool calls** (e.g., `call_tool("add_comment", {...})`) to save tokens and ensure structured JSON responses.
- Moving cards between agent-specific lists (e.g., from a "Planner" list to an "Analyst" list). The card stays in the lifecycle status list, and agents use Task Lists.
- The `bootstrap_workflow_board.py` and `sync_workflow_handoff.py` scripts.

## Validation Rule
Before claiming lifecycle sync is complete, verify:
1. Every agent (01→13) interacts with the Epic Card using **Native Planka MCP Tools** (except Roadmap agent, which uses the bulk sync script).
2. Every handoff comment or description update includes a link to the corresponding Obsidian `[[WF-ID]]` node.
3. Roadmap reconciliation covers all epics in `product-roadmap.md`.
4. The board uses Task Lists, Labels, and Description updates for visibility rather than comment-spam or list-bouncing.