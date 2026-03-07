# Planka Workflow Index Template

Use as baseline for `agent-output/planka/workflow-index.md`.

````markdown
# Planka Workflow Index

Markdown source-of-truth mapping between workflow IDs and Planka entities.
Use this file for cross-instance recovery and reconciliation.

```json
{
  "workflows": {
    "000-example": {
      "boardId": "<board-id>",
      "boardName": "<board-name>",
      "cardId": "<card-id>",
      "cardTitle": "<card-title>",
      "currentAgent": "01-Roadmap",
      "currentStatus": "Planned",
      "lastSyncedAt": "YYYY-MM-DDTHH:mm:ssZ",
      "origin": "000-example",
      "primaryArtifact": "agent-output/planning/NNN-plan.md",
      "projectId": "<project-id>",
      "projectName": "<project-name>",
      "workflowId": "000-example"
    }
  }
}
```
````
