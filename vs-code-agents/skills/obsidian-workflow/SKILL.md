---
name: obsidian-workflow
description: Token-budgeted Obsidian workflow contract for agent handoffs. Markdown remains source of truth; Obsidian provides low-cost context retrieval and concise write-back.
license: MIT
metadata:
  author: groupzer0
  version: "1.0"
---

# Obsidian Workflow (Token-Budgeted Agent Context)

Unified Obsidian workflow for concise agent handoffs with strict token discipline.

Use this skill when:
- Maintaining workflow context in Obsidian across multiple agents.
- Recording decisions and ownership transitions with minimal prompt payload.
- Synchronizing execution state without re-reading full documents.

---

## Source of Truth Model

**Canonical source**: Markdown artifacts in `agent-output/`.

Obsidian is the synchronized operational context layer:
- **Obsidian**: Fast lookup and concise handoff log for active workflows.
- **Memory**: Durable mapping for IDs, constraints, and prior decisions.

When conflicts occur:
1. Trust `agent-output/` Markdown first.
2. Update Obsidian notes to match Markdown state.
3. Record reconciliation in the workflow handoff block.

---

## Vault Topology (Required)

Use these stable paths in the Obsidian vault:
- `ops/workflow-index.md` (global lookup table)
- `workflows/WF-[ID]-[slug].md` (one workflow note per chain)

Each workflow note must contain:
- Frontmatter fields: `workflow_id`, `status`, `owner`, `last_updated`
- Headings: `Summary`, `Decisions`, `Constraints`, `Artifacts`, `Handoffs`, `Next`

---

## Context Budget Contract

Default hard budget per agent turn:
- **Searches**: max 1 targeted search (must include `WF-[ID]` or exact note path)
- **Reads**: max 2 focused reads (index note + workflow note)
- **Writes**: max 2 targeted writes (heading patch + handoff append)

Escalation rule:
- If information is missing, allow one extra read.
- Record why escalation was needed in the handoff block.

Forbidden patterns:
- Broad vault exploration without workflow ID.
- Full-note rewrites for small updates.
- Copying long markdown sections from `agent-output/` into Obsidian.

---

## Synchronization Protocol

### 1. Workflow bootstrap (Roadmap/Planner)
- Create or update `ops/workflow-index.md` entry.
- Create `workflows/WF-[ID]-[slug].md` with required headings.

### 2. Active execution (All specialized agents)
- Resolve workflow note from index using `WF-[ID]`.
- Read only relevant headings (`Next`, `Constraints`, latest `Handoffs`).
- Write concise updates to `Decisions` / `Artifacts` / `Next`.
- Append one timestamped handoff block.

### 3. Ownership transition
- Update `owner` and `status` in frontmatter.
- In `Next`, specify exact handoff target agent and acceptance gate.

### 4. Terminal lifecycle
- Mark final state in frontmatter (`Delivered`, `Deferred`, `Closed`).
- Keep note immutable except for explicit reconciliation corrections.

---

## Handoff Block Template (Mandatory)

Append under `Handoffs`:

```markdown
### [YYYY-MM-DD HH:mm] [Agent]
- Status: [one line]
- Decisions: [max 2 bullets, concrete]
- Changes: [what changed in code/docs]
- Next Owner: [agent]
- Open Risks: [none or concise]
- Artifacts: [relative paths]
```

Keep each bullet concise and concrete. Do not include full analysis text.

---

## Obsidian MCP Usage Guidance

Use Obsidian operations for:
- Targeted lookup (`search_notes` with `WF-[ID]` and low `limit`)
- Focused reads (`read_note` or `read_multiple_notes` for index + workflow note)
- Structured section updates (`patch_note` with exact string replacement)
- Handoff logging (`write_note` with `mode: append`)
- Ownership/frontmatter updates (`update_frontmatter` with `merge: true`)

Prefer idempotent actions:
- Find before create.
- Patch specific heading sections instead of replacing whole note content.

---

## Interoperability with Planka

When both workflows are active:
- Planka tracks visual execution status and task progress.
- Obsidian stores concise narrative context and handoff rationale.
- `agent-output/` remains the authoritative artifact source.

Avoid duplicate verbose status logging across Planka comments and Obsidian handoffs.
