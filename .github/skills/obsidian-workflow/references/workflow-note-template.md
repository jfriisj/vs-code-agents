# Workflow Note Template

Use as baseline for `agent-output/workflows/WF-[ID]-[slug].md`.

```markdown
---
workflow_id: WF-[ID]
project_name: "<Project Name>"
type: [Epic | Plan | Analysis]
parent: "[[WF-XXX]]" # use "none" for root epic nodes
status: Planned
owner: 01-Roadmap
last_updated: YYYY-MM-DD
---

## Summary
- [One-line workflow summary]

## Relations
- **Depends On**: [[WF-XXX]] or none
- **Blocks**: [[WF-YYY]], [[WF-ZZZ]] or none

## Decisions
- [Decision 1]

## Constraints
- [Constraint 1]

## Artifacts
- [[planning/002-sample-plan|Primary plan artifact]]
- [[implementation/002-sample-implementation|Implementation artifact]]

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

Validation gate:
- Run `node .github/skills/obsidian-workflow/scripts/verify-obsidian-graph.mjs` before handoff when frontmatter/headings/links were edited.