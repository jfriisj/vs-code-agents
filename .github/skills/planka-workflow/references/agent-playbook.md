# Agile Agent Playbook (01 → 13)

This playbook defines the **visual, status-driven** Agile Epic operations for each agent.

**The Triad of Truth:**
1. **Markdown**: The source of truth (`agent-output/`).
2. **Obsidian**: The memory graph (`workflows/WF-XXX.md`).
3. **Planka**: Live, visual execution tracking via **Native MCP Tools**.

---

## Global Conventions (Native MCP)

For daily operations, agents MUST use direct Planka MCP tool calls instead of terminal scripts. This saves tokens and ensures structured JSON responses.

**Agent Workflow Steps (Always follow this order):**
1. **Update Markdown**: Save your work in `agent-output/`.
2. **Update Obsidian**: Update or create your `WF-[ID]` node.
3. **Start Time**: Call `update_card` to start the stopwatch on the Epic card.
4. **Task Lists**: Call `create_task_list` (if missing) and `create_task` / `update_task` to generate a visual Progress Bar.
5. **Labels**: Keep release + priority labels consistent. Add status/verdict labels via `add_label_to_card` only when needed. 
6. **Handoff & Artifacts**: Call `add_comment` to leave a verdict. **CRITICAL**: You must include a link to your final markdown artifact AND your Obsidian node (e.g., `[[WF-NNN-Feature]]`).
7. **Stop Time**: Call `update_card` to stop the stopwatch.

### Native Tool Calling Templates

Instead of bash scripts, agents use these exposed Planka tools directly:

* **Stopwatch:** Use `update_card` to start/stop time tracking.
* **Task Lists (Progress Bar):**
  * `create_task_list` (args: `cardId`, `name`)
  * `create_task` (args: `taskListId`, `name`)
  * `update_task` (args: `taskId`, `isCompleted: true`)
* **Labels (Visual Status):**
  * `create_label` (args: `boardId`, `name`, `color`)
  * `add_label_to_card` (args: `cardId`, `labelId`)
* **Handoff (The Triad bridge):**
  * `add_comment` (args: `cardId`, `text: "Review complete. See [[WF-080-QA]] and agent-output/qa/..."`)

---

## Agent Operations Reference

### 01-Roadmap (The Exception)
- **Role**: Epic Creator & Status Manager
- **Action**: Uses the terminal! Reconciles **all roadmap epics** to Project/Board (`Epics`) in one pass using the Python bulk script (`python .github/skills/planka-workflow/scripts/sync_roadmap_epics.py`).
- **Metadata**: Syncs card due dates from roadmap release `**Target Date**` and keeps card descriptions aligned.
- **Task Lists**: Can bootstrap baseline agile task-list scaffolding on every epic card via `--ensure-task-lists`.

### 02-Planner
- **Workspace**: `Acceptance Criteria` (Task List)
- **Action**: Extracts acceptance criteria from the Epic description. Calls `create_task_list` and `create_task` for actionable items.
- **Artifact**: Calls `add_comment` with Plan link and `[[WF-ID]]`.

### 03-Analyst
- **Workspace**: `Analysis & Spikes` (Task List)
- **Action**: Creates tasks for technical investigations.
- **Label**: Calls `add_label_to_card` for `Analysis Complete`.
- **Artifact**: Calls `add_comment` with Analysis doc link and `[[WF-ID]]`.

### 04-Architect
- **Workspace**: `Architecture & Design` (Task List)
- **Action**: Adds architectural constraints as tasks.
- **Label**: Calls `add_label_to_card` for `Architecture Approved` (Green) or `Architecture Rejected` (Red).
- **Artifact**: Calls `add_comment` with Findings doc link and `[[WF-ID]]`.

### 05-Security
- **Workspace**: `Security & Compliance` (Task List)
- **Action**: Adds security checks as tasks. Checks them off via `update_task`.
- **Label**: Calls `add_label_to_card` for `Security Passed` (Green) or `Security Blocked` (Red).

### 06-Critic
- **Workspace**: `Plan Review & Critique` (Task List)
- **Label**: Calls `add_label_to_card` for `Plan Approved` or `Revision Required`.

### 07-Implementer
- **Action**: Marks tasks in the `Acceptance Criteria` and `Architecture & Design` lists as completed (`isCompleted=true` via `update_task`) to fill the Planka Progress Bar!
- **Label**: Calls `add_label_to_card` for `In Implementation` or `Ready for Code Review`.

### 08-Code Reviewer
- **Workspace**: `Code Review` (Task List)
- **Label**: Calls `add_label_to_card` for `Code Review Passed` (Green) or `Code Review Failed` (Red).

### 09-QA
- **Workspace**: `QA & Testing` (Task List)
- **Action**: Creates testing tasks (e.g., E2E, Unit) via `create_task` and marks them completed.
- **Label**: Calls `add_label_to_card` for `QA Passed` (Green) or `QA Failed` (Red).

### 10-UAT
- **Workspace**: `UAT & Acceptance` (Task List)
- **Action**: Verifies business value.
- **Label**: Calls `add_label_to_card` for `UAT Approved` (Green) or `UAT Failed` (Red).

### 11-DevOps
- **Workspace**: `Release & Deployment` (Task List)
- **Action**: Executes pre-flight deployment tasks.
- **Move (CRITICAL)**: Calls `move_card` to shift the Epic Card to the `Delivered` list upon successful production release.
- **Label**: Calls `add_label_to_card` for `Released vX.Y.Z`.

### 12-Retrospective & 13-Process Improvement
- **Workspace**: `Retrospective & Learnings` / `Process Improvement` (Task Lists)
- **Action**: Adds process improvements as tasks and checks them off when agent instructions are updated.
- **Artifact**: Calls `add_comment` with Retrospective doc link and `[[WF-ID]]`.