---
name: obsidian-workflow
description: Token-budgeted Obsidian workflow contract for agent handoffs. Markdown remains source of truth; Obsidian provides low-cost context retrieval and concise write-back.
license: MIT
metadata:
  author: groupzer0
  version: "1.1"
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

Template sources (skill-owned):
- `references/workflow-index-template.md`
- `references/workflow-note-template.md`

Each workflow note must contain:
- Frontmatter fields: `workflow_id`, `project_name`, `type`, `parent`, `status`, `owner`, `last_updated`
- Headings: `Summary`, `Relations`, `Decisions`, `Constraints`, `Artifacts`, `Handoffs`, `Next`

Workflow ID rules:
- `workflow_id` must start with `WF-` and match the note filename prefix.
- Never use placeholders such as `WF-[ID]`, `WF-Plan-ID`, or `WF-Calling-ID` in note content.
- `parent` must be `none` or a single wikilink that resolves to an existing note.

---

## Context Budget Contract (Graph-Optimized)

Default hard budget per agent turn:
- **Searches**: 0 (Avoid `search_notes` unless recovering from a broken link).
- **Reads**: max 2 focused reads (Read active `WF-[ID]` note + follow 1 graph link via `parent` or `Depends On`).
- **Writes**: max 2 targeted writes (heading patch + handoff append).

Escalation rule:
- If required context is not in the active note or its immediate parent, allow one extra read. Record why escalation was needed.

Validation rule:
- When frontmatter/headings/wikilinks are changed, run:
  - `node vs-code-agents/skills/obsidian-workflow/scripts/verify-obsidian-graph.mjs --workspace-root .`

## Synchronization Protocol
*Use `#tool:mcp-obsidian/*` for all operations below.*

### 1. Workflow bootstrap (Roadmap/Planner/Analyst)
- Create or update `workflows/WF-[ID]-[slug].md` with required frontmatter and headings.
- Establish graph edges with concrete IDs from upstream handoff context only. Do not invent alias IDs.
- Set `parent` using exactly one upstream node (`none` only for root nodes).

### 2. Active execution & Traversal
- Resolve active context by reading the assigned `WF-[ID]`.
- If broader context is needed, use `read_note` strictly on the wikilink found in the `parent:` or `Relations` field.
- Write concise updates to `Decisions` / `Artifacts` / `Next`.

### 3. Ownership transition & Graph Patching
- Update `owner` and `status` in frontmatter.
- If delegating to a sub-agent (e.g., Planner -> Analyst), patch `Relations` with concrete child links in `**Blocks**`.
- In your final chat message before handoff, output the concrete node ID in the form:
  - `Handoff Ready. Parent Node context for the next agent is [[WF-123]].`

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

## Index Management

`agent-output/ops/workflow-index.md` is managed in-repo. Regenerate it when notes change:

- `node vs-code-agents/skills/obsidian-workflow/scripts/migrate-workflow-notes.mjs --workspace-root . --write-index-only`

The index must include one explicit `[[workflows/...]]` entry per workflow note so graph verification can run without Dataview.

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
