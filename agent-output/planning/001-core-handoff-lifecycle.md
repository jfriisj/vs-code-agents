---
ID: 1
Origin: 1
UUID: 7a82b9c1
Target Release: v0.1.0
Status: UAT Approved
Epic: "Epic 1.1: Core Handoff Synchronization"
Planka: "http://localhost:25478/card/1724973066225714708"
---

# Plan-1: Core Handoff Lifecycle Verification

**Changelog**:
- 2026-03-06: UAT Complete (Product Owner). Implementation delivers expected business value, unblocking automated agent operations.
- 2026-03-06: QA Complete (qa). Logic and security tests passed. Integration with Planka verified.
- 2026-03-06: Code Review Approved (08-Code-Reviewer). Final validation of code quality issues addressed.
- 2026-03-06: Code Review Approved (08-Code-Reviewer). Implementation verified against DD-001. Hardening SEC-001/SEC-002 validated.
- 2026-03-06: Implementation complete (07-Implementer).
- 2026-03-06: Plan-1 V1.1 established (02-Planner).

**Value Statement and Business Objective**:
As a developer, I want to execute the full agent lifecycle (Roadmap -> Planning -> Architect -> Implement -> QA -> DevOps) for Epic 1.1, so that I can verify the "optimized" agent instruction set is functional and integrated.

**Objective**:
Complete a verifiable "round-trip" of the agent ecosystem using the newly optimized `.agent.md` files.

**Assumptions**:
- Planka MCP server is running and accessible.
- Roadmap agent has already synced Epic 1.1 to the Planka board.
- The `planka_ops.py` script bug is bypassed by direct MCP calls if needed.

**Testing Strategy**:
- **Integration**: Verify data flow from Roadmap artifact to Planka card to Planning artifact.
- **Verification**: Check if each agent can read/write to their intended `agent-output/` subfolders.
- **Validation**: User Acceptance Test (UAT) of the final "Done" status on the Planka card.

## Plan

### Milestone 1: Architect Review
1. Architect (04) reviews this plan for structural integrity and alignment with Epic 1.1.
2. Architect updates `agent-output/architecture/system-architecture.md` (if required) or status in Planka.
   - **Acceptance**: Architecture analysis confirmed; Planka card updated to "Doing".

### Milestone 2: Technical Analysis (Analyst)
1. **COMPLETED**: Analyst (03) investigated the `planka_ops.py` `isdigit()` bug in `.github/skills/planka-workflow/scripts/planka_ops.py`.
2. **COMPLETED**: Analyst (03) investigated the `card:move` failure (Analysis-3).
   - **Root Cause**: Verified that `move_card` also fails due to numeric string type-casting.
   - **Bypass**: Manually moved Card-1724973066225714708 to "In Progress".
3. Analyst documented findings in `analysis/002-planka-ops-fix-analysis.md` and `analysis/003-planka-move-failure-analysis.md`.

### Milestone 3: Implementation (Implementer)
1. **Context-Aware Parsing Fix**: Modify `parse_key_value_args` and `parse_value` in `.github/skills/planka-workflow/scripts/planka_ops.py` to accept the key name for context-aware type mapping.
2. **Security Hardening (SEC-001/SEC-003)**:
    - Implement a `TYPE_MAP` allowlist for known numeric fields (e.g., `position`, `total`) and boolean fields (`isCompleted`).
    - Use an ID exclusion list (keys ending in `Id`) to enforce `string` type for all IDs.
    - Default all other fields to `string` to prevent accidental type-sniffing and injection.
    - Implement a depth limit for JSON parsing.
3. **Log Sanitization (SEC-002)**:
    - Implement a utility to sanitize script output/stderr.
    - Redact sensitive strings (e.g., `PLANKA_TOKEN`, `ACCESS_KEY`, `Authorization`) from logs before storage.
4. **Standardized Exception Handling**:
    - Update `planka_ops.py` to handle MCP errors gracefully with standardized exit codes.
    - Ensure clear error messaging for automated observability during future failures.
5. **Regression Test Suite**: Create `test_planka_ops.py` to verify:
   - `cardId` (and other IDs) remains `str`.
   - `position` and `isCompleted` follow type mapping.
   - Sanitization pass for tokens in mock error logs.
6. **Verification**: Run the patched script with the sanitization logic to verify the fix and log protection.
   - **Acceptance**: Script functions without type errors; Unit tests pass; All log outputs sanitized; Planka updated.

### Milestone 4: Quality Assurance (QA)
1. QA (09) verifies the fix and the end-to-end sync of a test card.
2. QA performs negative testing (e.g., verifying that invalid inputs for IDs are correctly rejected or handled as strings).
3. QA documents test results in `agent-output/qa/001-test-results.md`.
   - **Acceptance**: QA sign-off in `agent-output/qa/`, including verification of security hardening.

### Milestone 5: Release and DevOps
1. DevOps (11) updates the `CHANGELOG.md` and prepares the release artifacts.
2. Update version artifact to `v0.1.0`.
3. Handoff to Roadmap agent (01) for final Epic closure in Planka and `product-roadmap.md`.
   - **Acceptance**: Version bumped; CHANGELOG updated; Roadmap Epic 1.1 marked as "Done".

## Decisions & Architectural/Security Review
- See [[WF-1]] for architectural invariants and the review verdict.
- See [[WF-2]] for security hardening requirements and log sanitization constraints.
- Plan ID `1` and Epic `1.1` MUST be used for tracking all operations.
- Regression test for `planka_ops.py` MUST be included in the implementation cycle.
- Capture AND SANITIZE raw stderr in the analysis artifact if script fails.

## Validation
- Final verification of Planka Card `1724973066225714708` status.
- Verification of Obsidian Graph links (if applicable).

## Risks
- **Dependency Risk**: Script bug prevents automated Planka updates.
- **Mitigation**: Use direct MCP tool calls as a fallback until the fix is deployed.
