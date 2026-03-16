---
ID: 2
Origin: 2
UUID: b2c4d5e6
Status: Released
Target Release: v0.1.0
handoff_id: "[[WF-2]]"
---

# 002-persistent-memory-obsidian-implementation

## Change Log
| Date | Change | Rationale |
|------|--------|-----------|
| 2026-03-16 | UAT Approved | Plan implementation delivers value, security hardened. |
| 2026-03-15 | v1.1 Revision | Add security gate HALT (F1), Hash Update (F2), and Permissions (F3). |
| 2026-03-13 | v1.0 Initial | Baseline planning for Epic 1.2. |

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
1. Define the internal `WF-<concrete-id>-<slug>.md` template with mandatory frontmatter (`type`, `parent`, `Planka-Card`, `handoff_id`). **SECURITY**: Add `artifact_hash` field to frontmatter for future integrity verification.
2. Establish the deterministic ID contract:
   - `WF-E<epic-id>` for Epics.
   - `WF-P<plan-id>` for Plans.
   - `WF-<PHASE>-<plan-id>` for lifecycle phases (QA, UAT, etc., e.g., `WF-AR-002`, `WF-S-002`).
3. Update `agent-output/.next-id` handling to ensure uniqueness across all artifact types.
4. **REMEDIATION (INJ-001)**: Refactor `scripts/memory_utils.py` to implement strict path sanitization. All `node_id` and `slug` inputs MUST be passed through `os.path.basename()` before path joining. Validate that the final resolved path is strictly contained within the `agent-output/workflows/` directory.

### Milestone 2: Automated Linking & Upward Edges
1. Implement the "Parent Edge" requirement: every child node MUST point to its logical parent.
2. Define the "Summary Node" pattern (The 10-Line Rule):
   - Max 3 bullet points per summary.
   - Direct wikilinks to `agent-output/` artifacts.
3. Establish the "Retrieval Gate": Agents must read the `WF-` node *before* deep-diving into artifacts.
   - **Enforcement**: Update `.instructions.md` for Planner, Implementer, and QA roles to include a strict pre-flight check of the `WF-` node linked in context.
   - **FAILURE MODE (CRITICAL - F1)**: If the memory node is missing, inaccessible, or its `artifact_hash` mismatching, the agent MUST **HALT** immediately and request human intervention. Proceeding with unverified context is strictly forbidden.
4. **REMEDIATION (INTEGRITY-001)**: Implement SHA-256 integrity verification in `scripts/memory_utils.py`. The node manager must automatically calculate the hash of the linked artifact upon creation/update and verify it during subsequent reads to prevent "Context Poisoning."
   - **HASH UPDATE POLICY (F2)**: Any agent modifying a canonical artifact MUST invoke `scripts/memory_utils.py --update-hash <node_id>` as the final step of their closure procedure to maintain synchronicity.
5. Define the **"Den Gyldne Rengøringsregel"** for memory: agents must archive or delete temporary `WF-` nodes that are no longer part of the active decision path to prevent graph entropy.
6. Implement **Broken Link Detection**: Add a task to Milestone 2 to develop a high-level verification procedure (e.g., regex check for wikilink validity) to ensure memory nodes point to existing Markdown artifacts.

### Milestone 3: Operational Integration (Hand-off Chain) & Security Hardening
1. Standardize the final chat handoff message to include the concrete `[[WF-...]]` link.
2. Integrate Planka-Obsidian cross-linking: update Planka descriptions to include the `Obsidian Root Node` link.
3. Define the **System Integrity Check** (QA Gate): verify that `WF-` summaries match the source artifact content. **HARDENING**: Implementation must include a cryptographic hash check or strict schema validation between the `WF-` node and the source `agent-output/` artifact (Mitigate DATA-001).
4. Implement the **Zero-Trust Retrieval Gate**: Agents must only access `WF-` nodes for which they have a valid logical parent in the current active scope. **ENFORCEMENT**: Update `.instructions.md` for all roles to explicitly forbid out-of-scope graph traversal (Mitigate IAM-001).
5. Define the "Closed" lifecycle for memory nodes:
   - **Idempotent Closure**: Implement state-aware replacement for node status (`Active` -> `Closed`) rather than opportunistic appends to avoid frontmatter corruption.
   - Use the `handoff_id` as the locking key to prevent concurrent agent closure conflicts.
6. Enforce Node Integrity: Update `CHANGELOG.md` upon v0.1.0 release to reflect the finalized Memory Pillar structure.
7. **Workspace Security (F3)**: Implement strict filesystem permission enforcement in Milestone 3. Define specific permission targets (e.g., `chmod 600` for `agent-output/workflows/*.md` and `.next-id`) to prevent unauthorized cross-agent access. Ensure the workspace `.gitignore` prevents exposure of memory artifacts (Mitigate CONFIG-001).

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
