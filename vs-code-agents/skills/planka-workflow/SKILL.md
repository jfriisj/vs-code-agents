````skill
---
name: planka-workflow
description: Operational synchronization contract for agent lifecycle tracking in Planka MCP. Markdown remains source of truth; Planka + Memory provide live workflow visibility.
license: MIT
metadata:
  author: groupzer0
  version: "1.1"
---

# Planka Workflow

Unified operational workflow tracking with Planka boards.

Use this skill when:
- Starting or continuing any agent workflow process
- Handing work between agents
- Reconciling lifecycle status across Markdown, Planka, and Memory

---

## Source of Truth Model

**Canonical source**: Markdown artifacts in `agent-output/`.

Planka and Memory are synchronized operational views:
- **Planka**: live execution board (who is working now, what stage is active)
- **Memory**: durable context for decisions, constraints, and mappings
- **Workflow index markdown**: `agent-output/planka/workflow-index.md` stores workflow↔project↔board↔card mappings for backup and cross-instance recovery

When conflicts occur:
1. Trust Markdown first
2. Update Planka to match Markdown
3. Store reconciliation context in Memory

Project isolation rule:
- Agents MUST operate only within the mapped workflow project (`projectId`) from `agent-output/planka/workflow-index.md`.
- Agents MUST NOT scan or operate across unrelated Planka projects/boards.

---

## Board Granularity

**Rule**: One board per workflow process.

A workflow process is one cross-agent lifecycle chain (typically one shared document ID).

Recommended board naming:
- `WF-[ID]-[short-title]`
- Example: `WF-042-audio-session-hotfix`

The board reflects the **currently active agent** by card placement.

---

## Required Board Structure

Create lists in this exact order:
1. `01-Roadmap`
2. `02-Planner`
3. `03-Analyst`
4. `04-Architect`
5. `05-Security`
6. `06-Critic`
7. `07-Implementer`
8. `08-Code Reviewer`
9. `09-QA`
10. `10-UAT`
11. `11-DevOps`
12. `12-Retrospective`
13. `13-Process Improvement`
14. `Blocked`
15. `Closed`

---

## Full Feature Utilization Requirement

This workflow MUST leverage the full Planka capability surface across lifecycle operations.

Required feature categories:
- Projects — list/get/create/update/delete
- Boards — list/get/create/update/delete
- Lists — create/update/delete
- Cards — get/create/update/move/delete
- Labels — create/add/remove
- Task lists & tasks — checklist creation, updates, completion tracking
- Comments — get/add/delete
- Attachments — upload (base64) and delete
- Card members — add/remove ownership participants
- Stopwatch — start/stop work timing
- Custom fields — groups, fields, values
- Subscribe — subscribe/unsubscribe notifications

Operational rule:
- Use the smallest feature set needed for each step, but maintain capability coverage in tooling and workflow playbooks.
- For destructive actions (delete operations), require explicit user intent.

---

## Card Model

Each workflow board MUST include one primary workflow card:
- Title: `WF-[ID] [Plan/Topic Title]`
- Description fields (minimum):
  - `ID`
  - `Origin`
  - `UUID`
  - `Primary Markdown Artifact`
  - `Current Status`
  - `Current Agent`
  - `Last Synced At`

Optional supporting cards can be used for substreams, but the primary card remains authoritative for active ownership.

---

## Synchronization Protocol

### On Session Start (agent begins work)
1. Resolve workflow ID from active artifact
2. **MUST execute bootstrap command** to reconcile/create project+board+card:

   ```bash
   python .github/skills/planka-workflow/scripts/bootstrap_workflow_board.py \
     --workflow-id <workflow-id> \
     --title "<workflow-title>" \
     --agent "<agent-name>" \
     --status "<status>" \
     --artifact "<primary-artifact-path>" \
     --project-name "Universal Speech Translation Platform" \
     --state-file "agent-output/planka/workflow-index.md" \
     --create-project-if-missing
   ```

3. Move card to current agent list (if not already there)
4. Update card description/status metadata
5. Store/update board+card mapping in Memory
6. Persist/update workflow mapping in `agent-output/planka/workflow-index.md`

If bootstrap fails, stop lifecycle sync actions and explicitly report the failure.

### During Work
- Keep Markdown updates first
- Reflect state transitions in Planka after Markdown updates
- Record key decisions/constraints in Memory

### On Handoff
1. Ensure Markdown artifacts are saved/updated
2. **MUST execute handoff sync command**:

   ```bash
   python .github/skills/planka-workflow/scripts/sync_workflow_handoff.py \
     --project-id <project-id> \
     --workflow-id <workflow-id> \
     --from-agent "<from-agent>" \
     --to-agent "<to-agent>" \
     --status "<status>" \
     --artifact "<primary-artifact-path>" \
     --summary "<handoff-summary>" \
     --next "<next-step>" \
     --state-file "agent-output/planka/workflow-index.md"
   ```

3. Add short handoff note on card (what changed, what is next)
4. Move card to receiving agent list
5. Store handoff relation in Memory

### On Terminal Status
When workflow reaches terminal lifecycle status (`Committed`, `Released`, `Resolved`, `Abandoned`, `Deferred`, `Superseded`):
1. Close/move Markdown artifact per `document-lifecycle`
2. Move primary card to `Closed`
3. Add terminal status note + timestamp on card
4. Store final state in Memory

---

## Drift Detection and Reconciliation

Drift example: card in `09-QA` while plan status is `In Progress` with implementer active.

Reconciliation order:
1. Confirm latest Markdown status + changelog
2. Correct Planka list/metadata to match
3. Add reconciliation comment to card
4. Persist drift context in Memory

---

## Failure Mode

If Planka MCP is unavailable:
1. Continue workflow using Markdown + Memory (do not block delivery)
2. Add a “Planka desync” note in active artifact changelog
3. Reconcile board state when Planka is restored

---

## Tool Usage Guidance

Use Planka MCP operations for:
- Project and board discovery (`list_projects`, `list_boards`, `get_board`)
- Board/list setup (`create_board`, `create_list`, `update_list`)
- Workflow card management (`create_card`, `update_card`, `move_card`, `get_card`)
- Handoff audit trail (`add_comment`, `get_comments`)
- Optional metadata (`create_custom_field_group`, `create_custom_field`, `set_custom_field_value`)
- Full feature operations (`planka_ops.py`) spanning all categories above

Prefer idempotent actions:
- List/find before create
- Update/move only when state differs

---

## Script Helpers

Use these scripts for structured operations:

- `scripts/bootstrap_workflow_board.py`
  - bootstrap/reconcile project + board + required lists + primary workflow card
- `scripts/sync_workflow_handoff.py`
  - move card across agent lists, update card metadata, add handoff comment
- `scripts/planka_ops.py`
  - full-feature operations CLI for all Planka feature categories

---

## Agent-by-Agent Execution Playbook

Use the canonical 01→13 workflow runbook for `start`, `handoff`, and `close` operation sets:

- `references/agent-playbook.md`
- `references/feature-coverage-matrix.md`

This playbook defines exactly which `planka_ops.py` / sync commands each agent executes and includes full feature-category coverage across the lifecycle.

Quick examples:

```bash
# Full catalog (all feature categories)
python .github/skills/planka-workflow/scripts/planka_ops.py catalog

# Run any operation by alias
python .github/skills/planka-workflow/scripts/planka_ops.py run \
  --op project:create --arg name="Workflow Operations"

# Labels
python .github/skills/planka-workflow/scripts/planka_ops.py run \
  --op label:create --arg boardId=<board-id> --arg name=Blocked --arg color=berry-red

# Tasks/checklist + completion
python .github/skills/planka-workflow/scripts/planka_ops.py run \
  --op tasklist:create --arg cardId=<card-id> --arg name="Acceptance Checklist"
python .github/skills/planka-workflow/scripts/planka_ops.py run \
  --op task:update --arg taskId=<task-id> --arg isCompleted=true

# Attachment from local file
python .github/skills/planka-workflow/scripts/planka_ops.py run \
  --op attachment:upload-file --arg cardId=<card-id> --arg path=./evidence.log

# Card member + subscribe + stopwatch
python .github/skills/planka-workflow/scripts/planka_ops.py run \
  --op member:add --arg cardId=<card-id> --arg userId=<user-id>
python .github/skills/planka-workflow/scripts/planka_ops.py run \
  --op subscribe:set --arg cardId=<card-id> --arg enabled=true
python .github/skills/planka-workflow/scripts/planka_ops.py run \
  --op stopwatch:start --arg cardId=<card-id>
python .github/skills/planka-workflow/scripts/planka_ops.py run \
  --op stopwatch:stop --arg cardId=<card-id>

# Custom fields
python .github/skills/planka-workflow/scripts/planka_ops.py run \
  --op customgroup:create --arg boardId=<board-id> --arg name="Workflow Metadata"
python .github/skills/planka-workflow/scripts/planka_ops.py run \
  --op customvalue:set --arg cardId=<card-id> --arg groupId=<group-id> --arg fieldId=<field-id> --arg content="In Progress"
```

---

## Quick Mapping

| Artifact Status / Stage | Agent List | Planka Action |
|---|---|---|
| Planning started | `02-Planner` | Move card to planner list |
| Implementation started | `07-Implementer` | Move card to implementer list |
| Testing in progress | `09-QA` | Move card to QA list |
| UAT validation | `10-UAT` | Move card to UAT list |
| Release execution | `11-DevOps` | Move card to DevOps list |
| Terminal lifecycle | `Closed` | Move card to Closed + add terminal note |

````
