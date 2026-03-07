---
ID: 2
Origin: 2
UUID: a4f9e1c2
Status: UAT Approved
Target Release: v0.2.0
Epic Alignment: "Epic 2.1: End-to-End Workflow Confidence Across Planka, Obsidian, and Memory"
---

# Plan-2: Workflow Rehearsal and Cross-Tool Analysis

## Changelog
| Date & Time | Change | Rationale | Plan/Epic |
|-------------|--------|-----------|-----------|
| 2026-03-07 07:45 | Initial Plan Creation | Promoted Epic 2.1 to In Progress and defined rehearsal scope. | Plan-2 / Epic 2.1 |
| 2026-03-07 08:35 | Architectural Hardening | Incorporated AR-1, AR-2, and ADR-002 linkage requirements. | Plan-2 / Epic 2.1 |
| 2026-03-07 09:05 | Security Hardening | Integrated SEC-001 sanitization and memory privacy controls. | Plan-2 / Epic 2.1 |
| 2026-03-07 09:40 | Critique Refinement | Added Discovery phase for Planka and URI-style naming for Memory. | Plan-2 / Epic 2.1 |
| 2026-03-07 11:30 | Code Review Approved | Reviewed implementation 008; confirmed AR-1/AR-2/SEC-001 alignment. | Plan-2 / Epic 2.1 |
| 2026-03-07 12:15 | UAT Approved | Verified cross-tool consistency and established Release Readiness Rule. | Plan-2 / Epic 2.1 |

## Value Statement and Business Objective
**As an** automated coding agent,
**I want to** execute a complete, end-to-end workflow rehearsal that spans all integrated tools (Roadmap, Planka, Obsidian, Memory),
**so that** the engineering team has empirical evidence of system consistency before the v0.2.0 release.

## Objective
The objective of this plan is to systematically test the "Golden Path" of the agent ecosystem. We will move from roadmap promotion to detailed planning, task synchronization, obsidian graph linkage, and memory persistence, while measuring for any data drift or orphaned artifacts.

## Assumptions
- The Planka MCP is correctly auth-configured and reachable.
- The Obsidian vault is local and accessible via the `mcp-obsidian` server.
- The Memory graph is initialized and holds the previous sync relations from Epic 1.1.
- All 13 agent instruction files were correctly hardened in the previous phase.

## Plan

### Milestone 1: Requirement Analysis & Baseline (Analyst Role)
1. **[COMPLETED]**: Verify existing Planka card `1725312215600334607` contains the required task lists. Documentation of any missing standard lists.
2. **[COMPLETED]**: Verify the Obsidian node `WF-21-cross-tool-workflow-confidence.md` exists and contains the correct `parent` link to the v0.2.0 Roadmap node.
3. **[COMPLETED]**: Compare the "Epic Readiness Matrix" in the roadmap with the actual state of linked artifacts.
   - **Finding**: Identified drift in the "Active Release Tracker" table vs. Epic header status.

### Milestone 2: Process Execution (Planner/Implementer Role)
1. **Remediate Roadmap Drift [AR-1]**: Update the `Active Release Tracker` table in `product-roadmap.md` to show Epic 2.1 as `In Progress` to match header status.
2. **Populate Planka Acceptance Criteria [SEC-001]**: 
   - **Discovery**: Run `planka_get_board` to identify the specific `taskListId` for "Acceptance Criteria".
   - **Execution**: Manually create individual `tasks` (checkboxes) within that list.
   - **CRITICAL**: Sanitize all descriptions to remove local paths (e.g., `/home/jonfriis/`) or sensitive environment metadata. Use placeholders like `<WORKSPACE_ROOT>`.
3. Update the Obsidian `workflow-index.md` to include a clear entry for this Plan (Plan-2) linked to WF-21 (using `migrate-workflow-notes.mjs`).
4. **Establish Memory Relations [AR-2]**: 
   - Verify/Create entity `Roadmap v0.2.0` (using URI-style identifier: `roadmap://v0.2.0`).
   - Establish 3-way graph relations: `Roadmap v0.2.0` -> `Epic 2.1` -> `Plan-2`. Ensure entity metadata is reference-based and contains no sensitive path information.

### Milestone 3: Verification & Safeguards (QA Role)
1. **ADR-002 Verification**: Run `verify-obsidian-graph.mjs` and provide the output as proof of zero-regression and valid node linkage.
2. **Standardized YAML Verifier**: Explicitly check for the mandatory "Security" field in any new implementation artifacts to ensure auditability.
3. Verify that `agent-output/.next-id` is correctly being honored and incremented.
4. Confirm that no placeholder leakage (e.g., `[[WF-[ID]]]`) exists in any newly generated artifacts.

### Milestone 4: Version Management & Release Readiness
1. Update `CHANGELOG.md` to reflect the transition of Epic 2.1 into the active testing phase.
2. Ensure plan artifacts match the target release version (v0.2.0) in all headers.

## Testing Strategy
- **Integration Test**: Direct tool-to-tool synchronization (Roadmap → Planka).
- **Graph Test**: Linkage verification in Obsidian via the zero-dependency verifier script.
- **Relational Test**: Search queries in Memory to confirm entity-relation persistence.

## Validation / Success Criteria
- [ ] Roadmap "Active Release Tracker" is synchronized with Epic headers.
- [ ] Planka card reflects all roadmap acceptance criteria as checklist items.
- [ ] Obsidian verifier returns success for all 11+ workflow notes.
- [ ] Memory graph persists the relation `Epic 2.1 -> validated by -> Plan-2`.

## Risks
- **Roadmap Desynchronization**: Manual updates to the tracker table are error-prone; mitigation: eventually automate table generation from headers.
- **Planka Task List ID discovery**: Tool `get_card` is missing task list IDs in summary; mitigation: use `get_board` if needed to find task list IDs.
- **Schema Drift**: New agents might use old templates; mitigation: `verify-obsidian-graph.mjs` gate.
