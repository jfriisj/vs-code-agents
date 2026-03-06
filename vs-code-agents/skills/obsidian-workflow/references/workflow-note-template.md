# Workflow Note Template

Use as baseline for `agent-output/workflows/WF-[ID]-[slug].md`.

```markdown
---
workflow_id: WF-[ID]
type: [Epic | Plan | Analysis]
parent: "[[WF-XXX]]"
status: Planned
owner: 01-Roadmap
last_updated: YYYY-MM-DD
---

## Summary
- [One-line workflow summary]

## Relations
- **Depends On**: 
- **Blocks**: 

## Decisions
- [Decision 1]

## Constraints
- [Constraint 1]

## Artifacts
- Source: agent-output/[path]/[file].md

## Handoffs
### YYYY-MM-DD HH:mm [Agent]
- Status: [One-line status]
- Decisions: [max 2 concise bullets]
- Changes: [what changed]
- Next Owner: [agent]
- Open Risks: [none or concise]
- Artifacts: [relative paths or [[WF-YYY]] node links]

## Next
- [Next owner/action and acceptance gate]