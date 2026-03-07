# Workflow Index Template

Use as baseline for `agent-output/ops/workflow-index.md`.

```markdown
# Active Workflows (Graph Index)

> [!INFO] Managed Index
> Regenerate this file with:
> `node vs-code-agents/skills/obsidian-workflow/scripts/migrate-workflow-notes.mjs --workspace-root . --write-index-only`

## Workflow Links
- [[workflows/WF-1|WF-1]]
- [[workflows/WF-2|WF-2]]

## Validation
- Run `node vs-code-agents/skills/obsidian-workflow/scripts/verify-obsidian-graph.mjs --workspace-root .`
```