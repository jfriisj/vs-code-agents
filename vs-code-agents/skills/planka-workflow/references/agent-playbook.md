# Agile Agent Playbook (01 → 13)

This playbook defines the **visual, status-driven** Agile Epic operations for each agent.
**Rule:** Markdown is the source of truth. Planka provides live, visual execution tracking.

## Global Conventions

- `PLANKA_OPS="python .github/skills/planka-workflow/scripts/planka_ops.py run"`
- All operations target the Epic Card using its `cardId`.

**Agent Workflow Steps (Always follow this order):**
1. **Update Markdown**: Save your work in `agent-output/`.
2. **Start Time**: Start the stopwatch on the Epic card.
3. **Task Lists**: Create your agent-specific Task List (if missing) and add/check off Tasks to generate a visual Progress Bar.
4. **Labels**: Keep release + priority labels consistent (`Release vX.Y.Z`, `Priority PX`) and add status/verdict labels only when needed. Remove old conflicting labels.
5. **Single Source of Truth**: Update the Epic Card's description to append a link to your final markdown artifact (do not spam the comments).
6. **Stop Time**: Stop the stopwatch.

### Command Templates

**Stopwatch:**
```bash
$PLANKA_OPS --op stopwatch:start --arg cardId=<card-id>
$PLANKA_OPS --op stopwatch:stop --arg cardId=<card-id>
```

**Task Lists (Progress Bar):**
```bash
$PLANKA_OPS --op tasklist:create --arg cardId=<card-id> --arg name="[Agent Workspace]"
$PLANKA_OPS --op task:create --arg taskListId=<id> --arg name="[Task name]"
$PLANKA_OPS --op task:update --arg taskId=<id> --arg isCompleted=true
```

**Labels (Visual Status):**
```bash
$PLANKA_OPS --op label:create --arg boardId=<id> --arg name="[Status]" --arg color="[hex]"
$PLANKA_OPS --op label:add --arg cardId=<card-id> --arg labelId=<id>
```

**Description / Due Date Update:**
```bash
$PLANKA_OPS --op card:update --arg cardId=<card-id> --arg description="[Original Description] \n\n**Artifacts:**\n- agent-output/domain/file.md"
$PLANKA_OPS --op card:update --arg cardId=<card-id> --arg dueDate="2026-03-31T23:59:59.000Z"
```

---

## Agent Operations Reference

### 01-Roadmap
- **Role**: Epic Creator & Status Manager
- **Action**: Reconciles **all roadmap epics** to Project/Board (`Epics`) in one pass; creates missing cards and keeps lifecycle lists synchronized.
- **Metadata**: Syncs card due dates from roadmap release `**Target Date**` and keeps card descriptions aligned.
- **Task Lists**: Can bootstrap baseline agile task-list scaffolding on every epic card via `--ensure-task-lists`.
- **Labels**: Ensures `Release vX.Y.Z` and `Priority PX` labels on every epic card for portfolio visibility.
- **Move**: Moves the Epic Card between Status Lists as the lifecycle progresses.

### 02-Planner
- **Workspace**: `Acceptance Criteria` (Task List)
- **Action**: Extracts acceptance criteria from the Epic description and creates actionable Tasks for the Implementer/QA.
- **Artifact**: Appends Plan link to Epic description.

### 03-Analyst
- **Workspace**: `Analysis & Spikes` (Task List)
- **Action**: Creates tasks for technical investigations.
- **Label**: Adds `Analysis Complete` label.
- **Artifact**: Appends Analysis doc link to Epic description.

### 04-Architect
- **Workspace**: `Architecture & Design` (Task List)
- **Action**: Adds architectural constraints as tasks.
- **Label**: Adds `Architecture Approved` (Green) or `Architecture Rejected` (Red) label.
- **Artifact**: Appends Findings doc link to Epic description.

### 05-Security
- **Workspace**: `Security & Compliance` (Task List)
- **Action**: Adds security checks as tasks. Checks them off.
- **Label**: Adds `Security Passed` (Green) or `Security Blocked` (Red) label.

### 06-Critic
- **Workspace**: `Plan Review & Critique` (Task List)
- **Label**: Adds `Plan Approved` or `Revision Required`.

### 07-Implementer
- **Action**: Marks tasks in the `Acceptance Criteria` and `Architecture & Design` lists as completed (`isCompleted=true`) to fill the Planka Progress Bar!
- **Label**: Adds `In Implementation` or `Ready for Code Review` label.

### 08-Code Reviewer
- **Workspace**: `Code Review` (Task List)
- **Label**: Adds `Code Review Passed` (Green) or `Code Review Failed` (Red) label.

### 09-QA
- **Workspace**: `QA & Testing` (Task List)
- **Action**: Creates testing tasks (e.g., E2E, Unit) and marks them completed.
- **Label**: Adds `QA Passed` (Green) or `QA Failed` (Red) label.

### 10-UAT
- **Workspace**: `UAT & Acceptance` (Task List)
- **Action**: Verifies business value.
- **Label**: Adds `UAT Approved` (Green) or `UAT Failed` (Red).

### 11-DevOps
- **Workspace**: `Release & Deployment` (Task List)
- **Action**: Executes pre-flight deployment tasks.
- **Move (CRITICAL)**: Moves the Epic Card to the `Delivered` list upon successful production release.
- **Label**: Adds `Released vX.Y.Z` label.

### 12-Retrospective & 13-Process Improvement
- **Workspace**: `Retrospective & Learnings` / `Process Improvement` (Task Lists)
- **Action**: Adds process improvements as tasks and checks them off when agent instructions are updated.
- **Artifact**: Appends Retrospective doc link to Epic description.