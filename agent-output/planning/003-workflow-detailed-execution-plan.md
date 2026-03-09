---
ID: 3
Origin: 2
UUID: a4f9e1c2
Status: Code Review Approved
Target Release: v0.2.0
Epic Alignment: Epic 2.1: End-to-End Workflow Confidence Across Planka, Obsidian, and Memory
---

# Plan-3: Detailed Execution and Cross-Tool Validation

## Value Statement and Business Objective
**As an** automated coding agent,
**I want to** execute a high-fidelity series of issue-sized work packages,
**so that** the v0.2.0 release is backed by empirical evidence of the new Release -> Epic -> Issue hierarchy across all core tools.

## Objective
To transition from the initial rehearsal (Plan-2) to the production-grade execution of Epic 2.1. This plan focuses on deep-tier validation where metadata moves through Planka, Obsidian, and Memory with zero drift, specifically verifying that issue-level evidence is queryable and rollable.

## Assumptions
- Planka card 1725309812348028678 remains the operational hub for Epic 2.1.
- Memory entities for the new agent contracts are active and referenceable.

## Issue Breakdown
- **ISS-2.1-101**: Establish Issue-Relational Baseline in Memory ($P0$).
- **ISS-2.1-102**: Implement Cross-Tool Status Transition Check ($P1$).
- **ISS-2.1-103**: Execute Strategic Obsidian Sync with Relational Wikilink Audit ($P0$).
- **ISS-2.1-104**: Generate final Release Readiness Evidence for v0.2.0 ($P0$).
- **ISS-2.1-105**: Test Memory Concurrency and Idempotency Verification.
- **ISS-2.1-106**: Systematically Resolve Roots from Environment Variables (ADR-003).

## Plan

### Milestone 1: Relational Hardening (Analyst/Architect)
1. **ISS-2.1-101**: Map the relationship between the 13 new agent contracts and the Issue hierarchy in the Memory graph.
   - Use `mcp_memory_create_relations` to link `agent://*-contract` to `workflow://release-epic-issue-model`.
   - **SECURITY CONTROL**: Validate all URI-style entity names against injection patterns before persistence.
2. **ISS-2.1-102**: Perform a dry-run of a status transition. Move an issue task through "Todo" -> "Done" and verify that the Planka comment audit matches the Roadmap "Active Release Tracker".
3. **ISS-2.1-105**: Execute a batch relation update in `memory.jsonl` and verify **idempotency** (zero line duplication) by checking the file line count delta before and after the operation.
   - **SECURITY CONTROL**: Verify zero sensitive environment data is persisted into the persistent `memory.jsonl`.

### Milestone 2: Technical Execution (Implementer)
1. **ISS-2.1-103**: Run the `verify-obsidian-graph.mjs` script against the `agent-output` folder.
   - Capture the logs in a standardized implementation comment on Planka.
   - Ensure the `parent` link in WF-21 points to the v0.2.0 Roadmap node.
2. **ISS-2.1-106**: Refactor `verify-obsidian-graph.mjs` and related scripts to resolve absolute workspace roots from environment variables rather than hardcoded paths. Scripts must fail-fast with a specific error message if executed outside the defined workspace boundary.
   - **SECURITY CONTROL**: Implement path sanitization; all absolute path telemetry must use the `<WORKSPACE_ROOT>` placeholder in shared/persistent artifacts.

### Milestone 3: Quality & Handoff (QA/UAT)
1. **ISS-2.1-104**: Compile the "Epic Readiness Matrix" based on the results of the 100-series issues.
   - Verify that all completed issues have the mandatory "Issue Completion Evidence" block.
   - Include telemetry logs for the absolute paths used during verification.
   - **SECURITY CONTROL**: Audit all final evidence comments for raw path disclosure before plan closure.

## Testing Strategy
- **Graph Coverage**: All 10 workflow notes must pass verification.
- **Evidence Integrity**: Planka comments must contain the `ISS-` prefix and matching outcome statements.

## Validation / Success Criteria
- [ ] Memory graph reflects `ISS-2.1-101` through `ISS-2.1-104` entities.
- [ ] Planka card 1725309812348028678 has at least 4 new "Issues" tasks.
- [ ] Roadmap tracker table reflects the current execution progress of Plan-3.

## Version Management
- **Milestone 4**: Update `CHANGELOG.md` and release markers for v0.2.0 upon plan completion.
