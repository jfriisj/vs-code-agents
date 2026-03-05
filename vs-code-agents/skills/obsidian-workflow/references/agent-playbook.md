# Obsidian Agent Playbook (01 → 13)

This playbook defines concise, low-token Obsidian operations for each agent.

Rule: `agent-output/` is source of truth. Obsidian is an execution context mirror.

## Global Conventions

- Workflow note key: `WF-[ID]`
- Index note: `ops/workflow-index.md`
- Workflow note path: `workflows/WF-[ID]-[slug].md`

## Mandatory Turn Sequence

1. Update canonical markdown in `agent-output/`.
2. Resolve workflow note via `WF-[ID]` (index lookup).
3. Read only required context (`Next`, latest handoff, constraints).
4. Patch only relevant heading(s): `Decisions`, `Artifacts`, `Next`.
5. Append one handoff block under `Handoffs`.
6. Update frontmatter (`owner`, `status`, `last_updated`).

## Token Budget Discipline

- Max 1 targeted search.
- Max 2 focused reads.
- Max 2 writes.
- One escalation read allowed only when required context is missing (must be noted in handoff).

## Guardrails

- Link-first only; never duplicate full sections from `agent-output` into Obsidian.
- No broad vault scans.
- No full-note rewrites for small updates.

## Tool Mapping (BitBonsai MCP-Obsidian)

- Discovery: `search_notes`
- Retrieval: `read_note` / `read_multiple_notes`
- Section updates: `patch_note`
- Handoff append: `write_note` with `mode: append`
- Frontmatter ownership updates: `update_frontmatter`

## Agent Operations Reference

### 01-Roadmap
- Creates workflow index entry and initial workflow note.
- Sets initial `owner` and `status`.

### 02-Planner
- Updates `Summary` and `Next` with executable acceptance path.
- Adds handoff block to Implementer.

### 03-Analyst
- Adds concise findings in `Decisions` and `Constraints`.
- Links analysis artifact path under `Artifacts`.

### 04-Architect
- Adds architecture verdict in `Decisions`.
- States design constraints and non-negotiables in `Constraints`.

### 05-Security
- Adds security verdict and blocking issues in `Decisions`.
- Adds remediations and verification target in `Next`.

### 06-Critic
- Adds plan quality verdict and required revisions.
- Sets next owner based on approval state.

### 07-Implementer
- Adds implementation scope actually completed.
- Links implementation artifact and test evidence paths.

### 08-Code Reviewer
- Adds review verdict and required code changes.
- Hands off to Implementer or QA.

### 09-QA
- Adds validation verdict and failing/passing scope.
- Hands off to UAT or back to Implementer.

### 10-UAT
- Adds business acceptance verdict.
- Hands off to DevOps when approved.

### 11-DevOps
- Records release/deployment outcome.
- Sets terminal state when delivered.

### 12-Retrospective
- Adds concise learnings and process friction.
- Links retrospective artifact.

### 13-Process Improvement
- Adds action items to `Next`.
- Updates ownership for process follow-up.

## Handoff Quality Gate

A handoff is valid only if it contains:
- Current status in one line.
- At least one concrete decision or verification result.
- Explicit next owner.
- Artifact links (or `none`).

Avoid long narrative text. If details are needed, link artifact files instead.
