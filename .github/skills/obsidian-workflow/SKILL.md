---
name: obsidian-workflow
description: Relational memory graph workflow using native Obsidian MCP tools with strict token-efficient WF node conventions.
license: MIT
metadata:
  author: groupzer0
  version: "3.1"
---

# Obsidian Workflow (Memory Graph)

Obsidian is the relational memory layer for this multi-agent workflow.
It does **not** replace `agent-output/*` artifacts and it does **not** own execution status.

## Triad of Truth
1. **Markdown (`agent-output/`)**: Canonical artifacts (full detail)
2. **Obsidian (`workflows/`)**: Relational context and handoff pointers
3. **Planka**: Live execution status and ownership

## WF Node Contract (10-Line Rule)

Use concise `WF-*` notes only. Do not duplicate full artifact content.

```markdown
---
type: [Epic | Plan | Analysis | Architecture | Security | Critique | Implementation | QA | UAT | Deployment | Retrospective | ProcessImprovement]
parent: "[[WF-Parent-ID]]" # use "none" only for root epic nodes
Planka-Card: "[cardId]"
---

## Summary
- [Max 3 bullets: key decision/constraint/outcome]

## Artifacts
- [[agent-output/path/to/artifact.md]]
```

## Allowed Operations (Native MCP Only)
- Use `read_note`, `write_note`, `patch_note`, and frontmatter update tools.
- Do not use terminal scripts for graph operations.
- Do not manually maintain index files.

## Retrieval Discipline
- Start from provided `[[WF-ID]]` handoff note.
- Follow only `parent:` if broader context is required.
- Read full artifacts only when summary bullets are insufficient.

## Handoff Contract
Before concluding, output:

> "Handoff Ready. Parent Node context for the next agent is [[WF-[ID]]] (Planka Card: [Card-ID])."

## Token Budget Guidance
- 0 broad vault searches
- Max 2 note reads
- Max 2 note writes/patches
- Keep notes link-first and minimal
