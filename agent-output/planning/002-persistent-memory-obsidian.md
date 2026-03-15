---
ID: 2
Origin: 2
UUID: b2c4d5e6
Status: UAT Approved
Target Release: v0.1.0
handoff_id: "[[WF-2]]"
---

# 002-persistent-memory-obsidian-implementation

**Value Statement and Business Objective**:
As a developer, I want my project's context and decisions to persist across chat sessions via Obsidian, so that the AI doesn't forget previous architectural choices and can navigate the implementation history through a relational graph.

## Objective
Establish the automated "Memory Pillar" using Obsidian `WF-*` nodes. This plan focuses on standardizing the creation, linking, and lazy-loading of these nodes during the agent lifecycle.

## Assumptions
- Agents have access to the `obsidian-workflow` skill.
- The `agent-output/workflows/` directory is the canonical location for memory nodes.
- Dataview or similar indexing will be used by humans, but agents rely on direct `read_note` on concrete IDs.

## Plan

### Milestone 1: Memory Node Template & ID Standardization
1. Define the internal `WF-<concrete-id>-<slug>.md` template with mandatory frontmatter (`type`, `parent`, `Planka-Card`, `handoff_id`).
2. Establish the deterministic ID contract:
   - `WF-E<epic-id>` for Epics.
   - `WF-P<plan-id>` for Plans.
   - `WF-<PHASE>-<plan-id>` for lifecycle phases (QA, UAT, etc., e.g., `WF-AR-002`, `WF-S-002`).
3. Update `agent-output/.next-id` handling to ensure uniqueness across all artifact types.

### Milestone 2: Automated Linking & Upward Edges
1. Implement the "Parent Edge" requirement: every child node MUST point to its logical parent.
2. Define the "Summary Node" pattern (The 10-Line Rule):
   - Max 3 bullet points per summary.
   - Direct wikilinks to `agent-output/` artifacts.
3. Establish the "Retrieval Gate": Agents must read the `WF-` node *before* deep-diving into artifacts.
   - **Enforcement**: Update `.instructions.md` for Planner, Implementer, and QA roles to include a strict pre-flight check of the `WF-` node linked in context.
4. Define the **"Den Gyldne Rengøringsregel"** for memory: agents must archive or delete temporary `WF-` nodes that are no longer part of the active decision path to prevent graph entropy.
5. Implement **Broken Link Detection**: Add a task to Milestone 2 to develop a high-level verification procedure (e.g., regex check for wikilink validity) to ensure memory nodes point to existing Markdown artifacts.

### Milestone 3: Operational Integration (Hand-off Chain) & Security Controls
1. Standardize the final chat handoff message to include the concrete `[[WF-...]]` link.
2. Integrate Planka-Obsidian cross-linking: update Planka descriptions to include the `Obsidian Root Node` link.
3. Define the **System Integrity Check** (QA Gate): verify that `WF-` summaries match the source artifact content.
4. Implement the **Zero-Trust Retrieval Gate**: Agents must only access `WF-` nodes for which they have a valid logical parent in the current active scope.
5. Define the "Closed" lifecycle for memory nodes:
   - **Idempotent Closure**: Implement state-aware replacement for node status (`Active` -> `Closed`) rather than opportunistic appends to avoid frontmatter corruption.
   - Use the `handoff_id` as the locking key to prevent concurrent agent closure conflicts.
6. Enforce Node Integrity: Update `CHANGELOG.md` upon v0.1.0 release to reflect the finalized Memory Pillar structure.

## Testing Strategy
- **Unit**: Verify node creation with correct frontmatter using `filesystem` tools.
- **Integration**: Verify that a "Plan" node correctly links to an "Epic" node and that `read_note` succeeds across the link.
- **Validation**: Ensure no placeholders (`WF-[ID]`) exist in generated files.

## Risks
- **Context Bloat**: If notes exceed 10 lines, they degrade performance. (Mitigation: Strict 10-Line Rule).
- **ID Collisions**: Using different numbering systems for different artifact types. (Mitigation: Centralized `.next-id`).
- **Context Poisoning**: Malicious agents could feed the graph with false summaries. (Mitigation: System Integrity Checks).
- **Information Disclosure**: Unrestricted graph traversal. (Mitigation: Zero-Trust Retrieval Gate).

## Version Management
- Update `agent-output/.next-id` to `3`.
- Add entry to `CHANGELOG.md` (if exists) or roadmap for Epic 1.2 initiation.
