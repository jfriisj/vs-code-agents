# Planka Board Template (Per Workflow Process)

Use one board per workflow process (`WF-[ID]-[short-title]`).

## Lists

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

## Primary Workflow Card

**Title**: `WF-[ID] [Plan/Topic Title]`

**Description template**:

```markdown
ID: [NNN]
Origin: [NNN]
UUID: [8-char]
Primary Markdown Artifact: agent-output/[domain]/[file].md
Current Status: [Active/In Progress/QA Complete/UAT Approved/Released/etc]
Current Agent: [Agent Name]
Last Synced At: [ISO-8601]
```

## Standard Metadata and Control Features

Use these Planka features on the primary workflow card:

- **Labels**: At least one status/risk label (e.g., `Blocked`, `Needs Review`, `Ready for Release`)
- **Task list**: `Workflow Checklist` with phase-completion tasks
- **Comments**: Use handoff template for each agent transition
- **Attachments**: Add evidence artifacts (logs, screenshots, reports)
- **Card members**: Assign active owner(s)
- **Stopwatch**: Start/stop for effort tracking on active execution phases
- **Custom fields**: Maintain structured fields for Workflow ID, Artifact, Status, Current Agent
- **Subscribe**: Active owner subscribed; unsubscribe when handoff complete

## Handoff Comment Template

```markdown
Handoff From: [Agent A]
Handoff To: [Agent B]
Updated Artifacts:
- agent-output/[domain]/[file].md
Summary:
- [one-line outcome]
Next:
- [next expected action]
```
