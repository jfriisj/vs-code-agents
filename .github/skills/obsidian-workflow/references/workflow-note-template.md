# Workflow Note Template

Use as baseline for `agent-output/workflows/WF-[ID]-[slug].md`.

```markdown
---
workflow_id: WF-[ID]
project_name: "<Project Name>"
type: [Epic | Plan | Analysis | Architecture | Security | Critique | Implementation]
parent: "[[WF-XXX]]" # use "none" for root epic nodes
status: Planned
owner: 01-Roadmap
last_updated: YYYY-MM-DD
Planka-Card: "[cardId]"
---

## Summary
- [One-line workflow summary]
- [Key constraint, decision, or blocked reason]

## Artifacts
- [[agent-output/planning/002-sample-plan.md|Primary artifact]]

```