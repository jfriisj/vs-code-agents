---
workflow_id: WF-21
project_name: "Agent System"
type: Epic
parent: "none"
status: In Progress
owner: 01-roadmap
last_updated: 2026-03-08
---

## Summary
- Epic 2.1 creates cross-tool confidence for workflow governance.
- This node tracks strategic outcomes for Planka, Obsidian, and Memory coherence.

## Relations
- **Depends On**: none
- **Blocks**: [[002-workflow-rehearsal-plan]], [[product-roadmap]], [[003-obsidian-workflow-hardening-brief]]
- **Implementing Plan**: [[planning/002-workflow-rehearsal-plan|Plan-2]]

## Decisions
- Prioritize one end-to-end rehearsal across all integrated tools before v0.2.0 release readiness.
- **ADR-002**: Integrated `verify-obsidian-graph.mjs` as a mandatory validation gate for all SDLC phases.

## Constraints
- Canonical source of truth remains `agent-output/` markdown artifacts.
- Tool drift must be documented with explicit expected-versus-observed outcomes.
- **AR-1**: Milestone 2 MUST resolve Roadmap dual-state drift (Header/Table decoupling).
- **SEC-001**: Clean/sanitize all roadmap-sourced data before manual input to Planka/Memory.

## Artifacts
- [[roadmap/product-roadmap|Product Roadmap]]
- [[ops/003-obsidian-workflow-hardening-brief|Obsidian Workflow Hardening Brief]]
- [[planning/002-workflow-rehearsal-plan|Plan-2: Workflow Rehearsal and Analysis]]
- [[architecture/004-workflow-rehearsal-architecture-findings|004-Architecture Findings: Plan-2 Approval]]
- [[security/005-workflow-rehearsal-security-review|005-Security Review: Plan-2 Verdict]]
- [[critiques/006-workflow-rehearsal-critique|006-Critique: Work Rehearsal Plan Audit]]

## Handoffs
### 2026-03-07 07:21 [01-roadmap]
- Status: Epic node created for cross-tool assurance scope.
- Decisions: Added strategic objective and release gating criteria for end-to-end validation.
- Changes: Roadmap release v0.2.0 and Epic 2.1 were added and synced.

### 2026-03-07 07:55 [02-planner]
- Status: Detailed implementation plan (Plan-2) created.
- Decisions: Subdivided rehearsal into Analyst, Planner, and QA milestones.
- Changes: Promoted Epic 2.1 to In Progress in Roadmap and Planka.
- Artifacts: [agent-output/planning/002-workflow-rehearsal-plan.md](agent-output/planning/002-workflow-rehearsal-plan.md)

### 2026-03-07 08:30 [04-architect]
- Status: Plan-2 APPROVED_WITH_CHANGES.
- Decisions: Defined [DD-003] Roadmap Dual-State Inconsistency. Mandated structural task lists and memory entity verification.
- Changes: Updated system-architecture.md with ADR-002. Created findings artifact.
- Artifacts: [agent-output/architecture/004-workflow-rehearsal-architecture-findings.md](agent-output/architecture/004-workflow-rehearsal-architecture-findings.md)

### 2026-03-07 08:50 [05-security]
- Status: Plan-2 APPROVED_WITH_CONTROLS.
- Decisions: Mandated sanitization of roadmap-sourced data. Defined [SEC-001] via [WF-21].
- Changes: Created security audit artifact. 
- Artifacts: [agent-output/security/005-workflow-rehearsal-security-review.md](agent-output/security/005-workflow-rehearsal-security-review.md)

### 2026-03-07 09:55 [06-critic]
- Status: Plan-2 APPROVED. RE-REVIEW COMPLETE.
- Decisions: Confirmed hardening and refinements. Verified [DD-003] and [SEC-001] are correctly addressed.
- Next Owner: 07-implementer
- Open Risks: None at the planning level.
- Artifacts: [agent-output/critiques/007-workflow-rehearsal-critique.md](agent-output/critiques/007-workflow-rehearsal-critique.md)

### 2026-03-07 10:45 [07-implementer]
- Status: Milestone 2.1 and 2.2 Complete.
- Decisions: Reconciled Roadmap dual-status drift. Populated Planka card with acceptance criteria and implementation tasks.
- Changes: Milestone 2.3 (Establish Obsidian WF-21) marked as current active work. Added this handoff to verify transition.
- Artifacts: [agent-output/implementation/008-workflow-rehearsal-implementation.md](agent-output/implementation/008-workflow-rehearsal-implementation.md)

### 2026-03-07 11:35 [08-code-reviewer]
- Status: Plan-2 Implementation APPROVED.
- Decisions: Confirmed remediation of Roadmap Drift [AR-1], Planka task population with [SEC-001] sanitization, and Memory registration with [AR-2] URI identifiers.
- Changes: Updated Plan-2 status to `Code Review Approved`.
- Artifacts: [agent-output/code-review/009-workflow-rehearsal-code-review.md](agent-output/code-review/009-workflow-rehearsal-code-review.md)

### 2026-03-07 08:30 [agent-optimizer]
- Status: Release-Epic-Issue migration phase initialized.
- Decisions: Adopted `Release -> Epic -> Issue` hierarchy for smaller execution slices while keeping roadmap strategic.
- Changes: Added migration brief `agent-output/ops/004-release-epic-issue-migration-brief.md` and updated Roadmap agent contract in both instruction roots.
- Next Owner: 02-planner
- Open Risks: Remaining agents still need sequential issue-contract rollout.
- Artifacts: [agent-output/ops/004-release-epic-issue-migration-brief.md](agent-output/ops/004-release-epic-issue-migration-brief.md)

### 2026-03-07 08:41 [agent-optimizer]
- Status: Planner issue-contract rollout complete.
- Decisions: Planner now enforces `Issue Breakdown` with `ISS-<epic>-<nnn>` IDs and blocks handoff without issue coverage.
- Changes: Updated `02-planner.agent.md` in both roots and added issue-level Planka exit validation requirements.
- Next Owner: 03-analyst
- Open Risks: Remaining agents still need sequential issue-contract rollout.
- Artifacts: [agent-output/ops/004-release-epic-issue-migration-brief.md](agent-output/ops/004-release-epic-issue-migration-brief.md)

### 2026-03-07 08:46 [agent-optimizer]
- Status: Analyst issue-contract rollout complete.
- Decisions: Analyst now requires issue-scoped analysis mapping and issue-ID evidence in Planka/analysis artifacts.
- Changes: Updated `03-analyst.agent.md` in both roots with issue coverage protocol and issue-evidence exit gates.
- Next Owner: 04-architect
- Open Risks: Remaining agents still need sequential issue-contract rollout.
- Artifacts: [agent-output/ops/004-release-epic-issue-migration-brief.md](agent-output/ops/004-release-epic-issue-migration-brief.md)

### 2026-03-07 08:51 [agent-optimizer]
- Status: Architect issue-contract rollout complete.
- Decisions: Architect now enforces issue-aware architecture mapping and requires issue-ID coverage in architecture tasks/comments.
- Changes: Updated `04-architect.agent.md` in both roots with issue traceability requirements and issue coverage exit gate.
- Next Owner: 05-security
- Open Risks: Remaining agents still need sequential issue-contract rollout.
- Artifacts: [agent-output/ops/004-release-epic-issue-migration-brief.md](agent-output/ops/004-release-epic-issue-migration-brief.md)

### 2026-03-07 08:54 [agent-optimizer]
- Status: Security issue-contract rollout complete.
- Decisions: Security now enforces issue-scoped controls, issue-ID task naming, and issue coverage in verdict evidence.
- Changes: Updated `05-security.agent.md` in both roots with issue coverage mapping and mandatory issue evidence checks at Planka exit.
- Next Owner: 06-critic
- Open Risks: Remaining agents still need sequential issue-contract rollout.
- Artifacts: [agent-output/ops/004-release-epic-issue-migration-brief.md](agent-output/ops/004-release-epic-issue-migration-brief.md)

### 2026-03-07 08:58 [agent-optimizer]
- Status: Critic issue-contract rollout complete.
- Decisions: Critic now enforces issue-granularity review quality and requires issue-linked critique evidence in Planka handoff.
- Changes: Updated `06-critic.agent.md` in both roots with issue decomposition critique checks and issue evidence requirements in exit gates.
- Next Owner: 07-implementer
- Open Risks: Remaining agents still need sequential issue-contract rollout.
- Artifacts: [agent-output/ops/004-release-epic-issue-migration-brief.md](agent-output/ops/004-release-epic-issue-migration-brief.md)

### 2026-03-07 09:00 [agent-optimizer]
- Status: Implementer issue-contract rollout complete.
- Decisions: Implementer now enforces issue-first execution order and issue-level completion evidence in handoff comments.
- Changes: Updated `07-implementer.agent.md` in both roots with issue execution sequencing and issue evidence checks in Planka exit gates.
- Next Owner: 08-code-reviewer
- Open Risks: Remaining agents still need sequential issue-contract rollout.
- Artifacts: [agent-output/ops/004-release-epic-issue-migration-brief.md](agent-output/ops/004-release-epic-issue-migration-brief.md)

### 2026-03-07 09:02 [agent-optimizer]
- Status: Code Reviewer issue-contract rollout complete.
- Decisions: Code Reviewer now requires issue-scoped findings and issue-level verdict evidence for QA handoff.
- Changes: Updated `08-code-reviewer.agent.md` in both roots with issue mapping in findings/tasks/comments and issue evidence checks in exit gates.
- Next Owner: 09-qa
- Open Risks: Remaining agents still need sequential issue-contract rollout.
- Artifacts: [agent-output/ops/004-release-epic-issue-migration-brief.md](agent-output/ops/004-release-epic-issue-migration-brief.md)

### 2026-03-07 09:07 [agent-optimizer]
- Status: QA issue-contract rollout complete.
- Decisions: QA now requires issue-scoped test coverage mapping and issue-level verdict evidence before `QA Complete`.
- Changes: Updated `09-qa.agent.md` in both roots with issue-linked coverage/regression checks and issue evidence validations in Planka exit gates.
- Next Owner: 10-uat
- Open Risks: Remaining agents still need sequential issue-contract rollout.
- Artifacts: [agent-output/ops/004-release-epic-issue-migration-brief.md](agent-output/ops/004-release-epic-issue-migration-brief.md)

### 2026-03-07 09:09 [agent-optimizer]
- Status: UAT issue-contract rollout complete.
- Decisions: UAT now requires issue-scoped acceptance evidence and issue roll-up in epic/release decisions.
- Changes: Updated `10-uat.agent.md` in both roots with issue-level acceptance mapping and issue evidence checks in Planka completion gates.
- Next Owner: 11-devops
- Open Risks: Remaining agents still need sequential issue-contract rollout.
- Artifacts: [agent-output/ops/004-release-epic-issue-migration-brief.md](agent-output/ops/004-release-epic-issue-migration-brief.md)

### 2026-03-07 09:12 [agent-optimizer]
- Status: DevOps issue-contract rollout complete.
- Decisions: DevOps now enforces issue-informed release readiness and requires issue roll-up evidence in deployment readiness and release comments.
- Changes: Updated `11-devops.agent.md` in both roots with issue roll-up verification and issue evidence checks in release/deployment gates.
- Next Owner: 12-retrospective
- Open Risks: Remaining agents still need sequential issue-contract rollout.
- Artifacts: [agent-output/ops/004-release-epic-issue-migration-brief.md](agent-output/ops/004-release-epic-issue-migration-brief.md)

### 2026-03-07 09:15 [agent-optimizer]
- Status: Retrospective issue-contract rollout complete.
- Decisions: Retrospective now captures lessons by issue clusters and feeds issue roll-up insights back into workflow improvement.
- Changes: Updated `12-retrospective.agent.md` in both roots with issue-cluster learning analysis and issue evidence checks in completion gates.
- Next Owner: 13-pi
- Open Risks: Remaining agents still need sequential issue-contract rollout.
- Artifacts: [agent-output/ops/004-release-epic-issue-migration-brief.md](agent-output/ops/004-release-epic-issue-migration-brief.md)

### 2026-03-07 09:17 [agent-optimizer]
- Status: Process Improvement issue-contract rollout complete.
- Decisions: Process Improvement now requires issue-metric analysis and preserves issue-level evidence gates in future workflow changes.
- Changes: Updated `13-pi.agent.md` in both roots with issue-pattern optimization requirements and issue evidence checks in completion gates.
- Next Owner: 01-roadmap
- Open Risks: None for the release-epic-issue contract rollout.
- Artifacts: [agent-output/ops/004-release-epic-issue-migration-brief.md](agent-output/ops/004-release-epic-issue-migration-brief.md)

### 2026-03-08 00:00 [agent-optimizer]
- Status: Release-Epic-Issue migration documentation closed.
- Decisions: Marked migration brief as completed after final consistency and tri-tool verification.
- Changes: Updated `agent-output/ops/004-release-epic-issue-migration-brief.md` with rollout-complete status and validation evidence.
- Next Owner: 01-roadmap
- Open Risks: None identified for the contract rollout.
- Artifacts: [agent-output/ops/004-release-epic-issue-migration-brief.md](agent-output/ops/004-release-epic-issue-migration-brief.md)

## Next
- Release-Epic-Issue contract rollout is complete across agents 01-13 in both roots.
- Continue normal workflow execution with issue-level evidence as the default gate.
- Keep tri-tool verification mandatory at every phase transition.
