Det er helt perfekt. Jeg har nu læst dokumentationen for `@bitbonsai/mcpvault`. Det bekræfter, at vi har alle de nødvendige native tools (`write_note`, `read_note`, `update_frontmatter`, `patch_note`) til at administrere grafen 100% token-effektivt uden eksterne scripts.

Her er den fuldstændigt rensede version 3.0 af `SKILL.md` for `obsidian-workflow`. Den fjerner script-overhead, fjerner duplikeret status/owner-håndtering (som hører til i Planka) og forbyder manuel indeksering.

### Den endelige `SKILL.md` (obsidian-workflow v3.0)

```markdown
---
name: obsidian-workflow
description: The core memory graph for the agent workflow using native mcpvault tools. Enforces the strict "10-Line Summary Node" rule to maintain extreme token-efficiency.
license: MIT
metadata:
  author: groupzer0
  version: "3.0"
---

# Obsidian Workflow (The Memory Graph)

Obsidian acts as the **Relational Memory Graph** for the multi-agent system. It is NOT for storing full documents or tracking execution status (Planka handles status). It relies on extremely lightweight "Summary Nodes" (the 10-Line Rule) to map how work flows from Epics to Plans to Implementations.

Use this skill whenever you start a task, complete a task, or hand off to another agent.

---

## The Triad of Truth
1. **Markdown (`agent-output/`)**: The actual content/artifacts (WHAT and WHY).
2. **Obsidian Graph (`workflows/`)**: The relational context and pointers (HOW things connect).
3. **Planka Board**: The execution status and task assignment (WHO and WHEN).

---

## The 10-Line Rule (Summary Nodes)

To prevent context window bloat, every Obsidian note MUST be extremely concise. Do not store `status`, `owner`, or `last_updated` in Obsidian—that is Planka's job.

**Node Structure Requirement**:
Every `WF-` node you create or patch (`workflows/WF-[ID]-[slug].md`) must strictly follow this minimalist template:

```markdown
---
type: [Epic | Plan | Analysis | Architecture | Security | Critique | Implementation]
parent: "[[WF-Parent-ID]]" # Use "none" for Root Epics
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

## Token-Budgeted Operations (Native MCP Tools)

You MUST use native tools for all vault operations. **Terminal scripts are strictly forbidden.**
**Strict Budget**: 0 Searches, Max 2 Reads, Max 2 Writes.

### 1. Context Retrieval (Lazy Loading)

* **Do NOT use `search_notes**` to scan the vault.
* When an agent hands a task to you, they will provide a `[[WF-[ID]]]` link in the chat.
* Use `read_note` on that specific `WF-` note.
* Read the frontmatter to find the `parent:` link or `Planka-Card`.
* Only read the full artifact (from `agent-output/`) if the 3-bullet summary doesn't contain the specific constraints you need.

### 2. Updating / Creating Nodes

* **New Task**: Use `write_note` to create a new node following the 10-Line Rule. Ensure `parent:` correctly points upward in the graph.
* **Progressing a Task**: Use `patch_note` to add a new bullet point to the summary if a major decision is made.
* **Adding an edge**: If you depend on another node, inject `**Blocks**: [[WF-XXX]]` into your summary.

### 3. Automated Indexing (Do NOT edit indices)

* Do NOT attempt to update `ops/workflow-index.md` or any other index file. Obsidian Dataview handles this dynamically based on your `WF-` nodes.

### 4. The Critical Handoff

Before concluding your turn and stopping execution, you **MUST** output a final message in the chat stating exactly where the next agent should start:

> *"Handoff Ready. Parent Node context for the next agent is [[WF-[ID]]] (Planka Card: [Card-ID])."*
