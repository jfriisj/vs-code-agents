````markdown
# Agent Playbook (01 → 13)

This playbook defines exactly which `planka_ops.py` and sync scripts each agent executes at **start**, **handoff**, and **close**.

## Global Conventions

- `PLANKA_OPS="python .github/skills/planka-workflow/scripts/planka_ops.py run"`
- `SYNC="python .github/skills/planka-workflow/scripts/sync_workflow_handoff.py"`
- `BOOTSTRAP="python .github/skills/planka-workflow/scripts/bootstrap_workflow_board.py"`
- `STATE_FILE="agent-output/planka/workflow-index.md"`
- Append `--state-file "$STATE_FILE"` to every `BOOTSTRAP` and `SYNC` command.
- Every **Start** stage must begin with bootstrap/reconcile:
  - `$BOOTSTRAP --workflow-id <workflow-id> --title "<title>" --agent "<agent-name>" --status "<status>" --artifact "<primary-artifact-path>" --project-name "Universal Speech Translation Platform" --create-project-if-missing --state-file "$STATE_FILE"`
- Always update Markdown first, then sync Planka.
- Destructive operations (`*delete`) require explicit user confirmation.

Required placeholders:
- `<workflow-id>`, `<project-id>`, `<board-id>`, `<card-id>`, `<from-agent>`, `<to-agent>`

Operation-level coverage source:
- `references/feature-coverage-matrix.md` (maps every list/get/create/update/delete and advanced operation alias)

---

## 01-Roadmap

**Start**
- Bootstrap workflow board/card:
  - `$BOOTSTRAP --workflow-id <workflow-id> --title "<title>" --agent "01-Roadmap" --status "Planned" --artifact "agent-output/roadmap/product-roadmap.md" --project-name "Universal Speech Translation Platform" --create-project-if-missing --state-file "$STATE_FILE"`
- Set metadata foundation:
  - `$PLANKA_OPS --op customgroup:create --arg boardId=<board-id> --arg name="Workflow Metadata"`
  - `$PLANKA_OPS --op label:create --arg boardId=<board-id> --arg name="Feature" --arg color=bright-moss`

**Handoff**
- Transfer ownership to planner:
  - `$SYNC --project-id <project-id> --workflow-id <workflow-id> --from-agent "01-Roadmap" --to-agent "02-Planner" --status "Planned" --artifact "agent-output/planning/<plan>.md" --summary "Roadmap alignment complete" --next "Create implementation-ready plan"`

**Close**
- If deferred/abandoned at strategy stage:
  - `$PLANKA_OPS --op label:add --arg cardId=<card-id> --arg labelId=<deferred-label-id>`
  - `$SYNC --project-id <project-id> --workflow-id <workflow-id> --from-agent "01-Roadmap" --to-agent "Closed" --status "Deferred" --summary "Roadmap deferred by user"`

---

## 02-Planner

**Start**
- Subscribe + assign active ownership:
  - `$PLANKA_OPS --op subscribe:set --arg cardId=<card-id> --arg enabled=true`
  - `$PLANKA_OPS --op member:add --arg cardId=<card-id> --arg userId=<planner-user-id>`
- Create planning checklist:
  - `$PLANKA_OPS --op tasklist:create --arg cardId=<card-id> --arg name="Planning Checklist"`
  - `$PLANKA_OPS --op task:create --arg taskListId=<tasklist-id> --arg name="Value statement drafted"`

**Handoff**
- Move to analyst or critic:
  - `$SYNC --project-id <project-id> --workflow-id <workflow-id> --from-agent "02-Planner" --to-agent "03-Analyst" --status "Analysis Requested" --artifact "agent-output/analysis/<analysis>.md" --summary "Research questions identified" --next "Investigate unknowns"`

**Close**
- Mark checklist completion before leaving planning stage:
  - `$PLANKA_OPS --op task:update --arg taskId=<task-id> --arg isCompleted=true`

---

## 03-Analyst

**Start**
- Track active investigation time:
  - `$PLANKA_OPS --op stopwatch:start --arg cardId=<card-id>`
- Attach investigation artifacts:
  - `$PLANKA_OPS --op attachment:upload-file --arg cardId=<card-id> --arg path=./agent-output/analysis/<evidence-file>`

**Handoff**
- Stop timer and transfer:
  - `$PLANKA_OPS --op stopwatch:stop --arg cardId=<card-id>`
  - `$SYNC --project-id <project-id> --workflow-id <workflow-id> --from-agent "03-Analyst" --to-agent "02-Planner" --status "Analysis Complete" --artifact "agent-output/analysis/<analysis>.md" --summary "Findings documented with confidence levels" --next "Incorporate into plan"`

**Close**
- Remove sensitive temporary evidence when required:
  - `$PLANKA_OPS --op attachment:delete --arg attachmentId=<attachment-id>`

---

## 04-Architect

**Start**
- Retrieve board/card context + apply architecture label:
  - `$PLANKA_OPS --op board:get --arg boardId=<board-id>`
  - `$PLANKA_OPS --op label:add --arg cardId=<card-id> --arg labelId=<architecture-label-id>`

**Handoff**
- Transfer to planner/critic after review:
  - `$SYNC --project-id <project-id> --workflow-id <workflow-id> --from-agent "04-Architect" --to-agent "02-Planner" --status "Architecture Reviewed" --artifact "agent-output/architecture/<findings>.md" --summary "Architecture constraints updated" --next "Revise plan accordingly"`

**Close**
- Remove temporary architecture label if resolved:
  - `$PLANKA_OPS --op label:remove --arg cardId=<card-id> --arg labelId=<architecture-label-id>`

---

## 05-Security

**Start**
- Apply risk labels and assign reviewer:
  - `$PLANKA_OPS --op label:create --arg boardId=<board-id> --arg name="Urgent/Bug" --arg color=berry-red`
  - `$PLANKA_OPS --op label:add --arg cardId=<card-id> --arg labelId=<risk-label-id>`

**Handoff**
- Transfer with risk summary:
  - `$SYNC --project-id <project-id> --workflow-id <workflow-id> --from-agent "05-Security" --to-agent "07-Implementer" --status "Security Fix Required" --artifact "agent-output/security/<audit>.md" --summary "Blocking security findings identified" --next "Implement remediation"`

**Close**
- Remove risk label on remediation completion:
  - `$PLANKA_OPS --op label:remove --arg cardId=<card-id> --arg labelId=<risk-label-id>`

---

## 06-Critic

**Start**
- Subscribe and review context:
  - `$PLANKA_OPS --op subscribe:set --arg cardId=<card-id> --arg enabled=true`
  - `$PLANKA_OPS --op comments:get --arg cardId=<card-id>`

**Handoff**
- Transfer to planner/implementer:
  - `$SYNC --project-id <project-id> --workflow-id <workflow-id> --from-agent "06-Critic" --to-agent "02-Planner" --status "Plan Revision Needed" --artifact "agent-output/critiques/<critique>.md" --summary "Critical findings logged" --next "Address open issues"`

**Close**
- Unsubscribe when critique resolved:
  - `$PLANKA_OPS --op subscribe:set --arg cardId=<card-id> --arg enabled=false`

---

## 07-Implementer

**Start**
- Start execution timer + assign implementer:
  - `$PLANKA_OPS --op member:add --arg cardId=<card-id> --arg userId=<implementer-user-id>`
  - `$PLANKA_OPS --op stopwatch:start --arg cardId=<card-id>`
- Create implementation checklist:
  - `$PLANKA_OPS --op tasklist:create --arg cardId=<card-id> --arg name="Implementation Checklist"`

**Handoff**
- Stop timer and move to code review:
  - `$PLANKA_OPS --op stopwatch:stop --arg cardId=<card-id>`
  - `$SYNC --project-id <project-id> --workflow-id <workflow-id> --from-agent "07-Implementer" --to-agent "08-Code Reviewer" --status "Implemented" --artifact "agent-output/implementation/<implementation>.md" --summary "Implementation complete, ready for review" --next "Code quality gate"`

**Close**
- Remove implementation-only member if needed:
  - `$PLANKA_OPS --op member:remove --arg cardId=<card-id> --arg userId=<implementer-user-id>`

---

## 08-Code Reviewer

**Start**
- Pull review context and comment:
  - `$PLANKA_OPS --op card:get --arg cardId=<card-id>`
  - `$PLANKA_OPS --op comment:add --arg cardId=<card-id> --arg text="Code review started"`

**Handoff**
- Route based on verdict:
  - Pass: `$SYNC --project-id <project-id> --workflow-id <workflow-id> --from-agent "08-Code Reviewer" --to-agent "09-QA" --status "Code Review Approved" --artifact "agent-output/code-review/<review>.md" --summary "Approved for QA" --next "Execute QA tests"`
  - Fail: `$SYNC --project-id <project-id> --workflow-id <workflow-id> --from-agent "08-Code Reviewer" --to-agent "07-Implementer" --status "Code Review Rejected" --artifact "agent-output/code-review/<review>.md" --summary "Fixes required" --next "Address findings"`

**Close**
- Delete accidental duplicate reviewer comments if needed:
  - `$PLANKA_OPS --op comment:delete --arg commentId=<comment-id>`

---

## 09-QA

**Start**
- Create QA checklist and scenarios:
  - `$PLANKA_OPS --op tasklist:create --arg cardId=<card-id> --arg name="QA Scenarios"`
  - `$PLANKA_OPS --op task:create --arg taskListId=<tasklist-id> --arg name="Critical path passes"`

**Handoff**
- Attach QA evidence and move to UAT:
  - `$PLANKA_OPS --op attachment:upload-file --arg cardId=<card-id> --arg path=./agent-output/qa/<qa-report>.md`
  - `$SYNC --project-id <project-id> --workflow-id <workflow-id> --from-agent "09-QA" --to-agent "10-UAT" --status "QA Complete" --artifact "agent-output/qa/<qa>.md" --summary "QA passed" --next "Validate business value"`

**Close**
- Remove obsolete QA checklist items if refined:
  - `$PLANKA_OPS --op task:delete --arg taskId=<task-id>`

---

## 10-UAT

**Start**
- Subscribe + review QA context:
  - `$PLANKA_OPS --op subscribe:set --arg cardId=<card-id> --arg enabled=true`
  - `$PLANKA_OPS --op comments:get --arg cardId=<card-id>`

**Handoff**
- Pass to DevOps or return to planner:
  - Approved: `$SYNC --project-id <project-id> --workflow-id <workflow-id> --from-agent "10-UAT" --to-agent "11-DevOps" --status "UAT Approved" --artifact "agent-output/uat/<uat>.md" --summary "Approved for release" --next "Prepare release"`
  - Not approved: `$SYNC --project-id <project-id> --workflow-id <workflow-id> --from-agent "10-UAT" --to-agent "02-Planner" --status "UAT Failed" --artifact "agent-output/uat/<uat>.md" --summary "Value gaps found" --next "Re-plan work"`

**Close**
- Unsubscribe after handoff:
  - `$PLANKA_OPS --op subscribe:set --arg cardId=<card-id> --arg enabled=false`

---

## 11-DevOps

**Start**
- Add release label and release metadata:
  - `$PLANKA_OPS --op label:add --arg cardId=<card-id> --arg labelId=<ready-release-label-id>`
  - `$PLANKA_OPS --op customvalue:set --arg cardId=<card-id> --arg groupId=<group-id> --arg fieldId=<release-field-id> --arg content="vX.Y.Z"`

**Handoff**
- On release completion, move to retrospective:
  - `$SYNC --project-id <project-id> --workflow-id <workflow-id> --from-agent "11-DevOps" --to-agent "12-Retrospective" --status "Released" --artifact "agent-output/deployment/<version>.md" --summary "Release executed" --next "Capture lessons learned"`

**Close**
- Optionally remove release label and retain closed state metadata:
  - `$PLANKA_OPS --op label:remove --arg cardId=<card-id> --arg labelId=<ready-release-label-id>`

---

## 12-Retrospective

**Start**
- Pull comments and add retrospective note:
  - `$PLANKA_OPS --op comments:get --arg cardId=<card-id>`
  - `$PLANKA_OPS --op comment:add --arg cardId=<card-id> --arg text="Retrospective analysis started"`

**Handoff**
- Transfer to process-improvement:
  - `$SYNC --project-id <project-id> --workflow-id <workflow-id> --from-agent "12-Retrospective" --to-agent "13-Process Improvement" --status "Retrospective Complete" --artifact "agent-output/retrospectives/<retro>.md" --summary "Process lessons documented" --next "Apply process improvements"`

**Close**
- Remove non-essential duplicate retro comments if needed:
  - `$PLANKA_OPS --op comment:delete --arg commentId=<comment-id>`

---

## 13-Process Improvement

**Start**
- Update custom workflow status and ownership:
  - `$PLANKA_OPS --op customvalue:set --arg cardId=<card-id> --arg groupId=<group-id> --arg fieldId=<status-field-id> --arg content="Process Improvement In Progress"`

**Handoff**
- Return to planner/new cycle or close:
  - `$SYNC --project-id <project-id> --workflow-id <workflow-id> --from-agent "13-Process Improvement" --to-agent "02-Planner" --status "Ready for Next Cycle" --summary "Instruction updates complete" --next "Start next plan"`

**Close**
- Controlled cleanup operations (explicit user approval required):
  - Card cleanup: `$PLANKA_OPS --op card:delete --arg cardId=<card-id>`
  - List cleanup: `$PLANKA_OPS --op list:delete --arg listId=<list-id>`
  - Task cleanup: `$PLANKA_OPS --op tasklist:delete --arg taskListId=<tasklist-id>`
  - Custom metadata cleanup:
    - `$PLANKA_OPS --op customvalue:delete --arg cardId=<card-id> --arg groupId=<group-id> --arg fieldId=<field-id>`
    - `$PLANKA_OPS --op customfield:delete --arg fieldId=<field-id>`
    - `$PLANKA_OPS --op customgroup:delete --arg groupId=<group-id>`
  - Board/project cleanup after retention:
    - `$PLANKA_OPS --op board:delete --arg boardId=<board-id>`
    - `$PLANKA_OPS --op project:delete --arg projectId=<project-id>`

---

## Full Coverage Verification (Operational)

Run these checks before declaring lifecycle-complete setup:

1. `python .github/skills/planka-workflow/scripts/planka_ops.py catalog`
2. Confirm all required categories appear:
   - Projects, Boards, Lists, Cards, Labels, Task lists & tasks, Comments, Attachments, Card members, Stopwatch, Custom fields, Subscribe
3. Confirm each agent (01→13) has start/handoff/close execution in this playbook.

````
