---
name: obsidian-workflow
description: The core memory graph for the agent workflow. Enforces the strict "10-Line Summary Node" rule to maintain extreme token-efficiency during agent handoffs.
license: MIT
metadata:
  author: groupzer0
  version: "2.0"
---

# Obsidian Workflow (The Memory Graph)

Obsidian acts as the **Relational Memory Graph** for the multi-agent system. It is NOT for storing full documents. It relies on extremely lightweight "Summary Nodes" (the 10-Line Rule) to map how work flows from Epics to Plans to Implementations.

Use this skill whenever you start a task, complete a task, or hand off to another agent.

---

## The Triad of Truth
1. **Markdown (`agent-output/`)**: The actual content/artifacts (WHAT and WHY).
2. **Obsidian Graph (`workflows/`)**: The relational context and pointers (HOW things connect).
3. **Planka Board**: The execution status and task assignment (WHO and WHEN).

---

## The 10-Line Rule (Summary Nodes)

To prevent context window bloat, every Obsidian note MUST be extremely concise. 

**Vault Topology**:
- `ops/workflow-index.md` (Auto-generated Dataview table - DO NOT EDIT)
- `workflows/WF-[ID]-[slug].md` (The active summary nodes)

**Node Structure Requirement**:
Every `WF-` node you create or patch must strictly follow this minimalist template:

```markdown
---
workflow_id: WF-[ID]
project_name: "<Project Name>"
type: [Epic | Plan | Analysis | Architecture | Security | Critique | Implementation]
parent: "[[WF-Parent-ID]]" # "none" for Root Epics
status: [Planned | Active | Blocked | Resolved | Closed]
owner: [Agent Name]
last_updated: YYYY-MM-DD
Planka-Card: "[cardId]"
---

## Summary
- [Max 3 bullet points summarizing the core decision, constraint, or outcome.]
- [If blocked, state exactly why.]

## Artifacts
- [[agent-output/path/to/artifact.md]]

```

*(Do not add `Handoffs`, `Constraints`, or `Decisions` headings. Put the absolute core essence into the 3 `Summary` bullets and let the Artifact markdown file do the heavy lifting).*

---

## Token-Budgeted Operations (MCP Tools)

You must use `#tool:mcp-obsidian/*` for vault operations. **Strict Budget**: 0 Searches, Max 2 Reads, Max 2 Writes.

### 1. Context Retrieval (Lazy Loading)

* **Do NOT use `search_notes**` to scan the vault.
* When an agent hands a task to you, they will provide a `[[WF-[ID]]]` link in the chat.
* Use `read_note` on that specific `WF-` note.
* Read the frontmatter to find the `parent:` link or `Planka-Card`.
* Only read the full artifact (from `agent-output/`) if the 3-bullet summary doesn't contain the specific constraints you need.

### 2. Updating / Creating Nodes

* **New Task**: Use `write_note` to create a new node following the 10-Line Rule. Ensure `parent:` correctly points upward in the graph.
* **Progressing a Task**: Use `update_frontmatter` to change `status` or `owner`.
* **Adding an edge**: If you depend on another node, inject `**Blocks**: [[WF-XXX]]` into your summary, or update frontmatter.

### 3. The Critical Handoff

Before concluding your turn and stopping execution, you **MUST** output a final message in the chat stating exactly where the next agent should start:

> *"Handoff Ready. Parent Node context for the next agent is [[WF-[ID]]] (Planka Card: [Card-ID])."*

---

## Validation Gate

Whenever you create or modify the headings/frontmatter of a workflow note, you MUST run the validation script before handing off:

```bash
node .github/skills/obsidian-workflow/scripts/verify-obsidian-graph.mjs

```
