# 004 - Release-Epic-Issue Migration Brief

Date: 2026-03-07
Owner: agent-optimizer
Status: Completed (Rollout finished across agents 01-13)

## Objective
Introduce a three-level delivery model across the agent workflow:
- Release: contains multiple epics.
- Epic: represents one complete user-facing feature.
- Issue: small, verifiable work slice inside an epic.

This reduces batch size and enables tighter iteration than epic-only execution.

## Recommended Model
1. Keep Release and Epic ownership with Roadmap.
2. Add Issue as the execution unit under each epic.
3. Treat issues as explicit task items inside the epic card in Planka (task list `Issues`).
4. Require plan/implementation/QA/UAT handoffs to reference issue IDs, not only epic IDs.

## Why This Approach
- Works with current toolchain immediately (Planka task APIs already used by all agents).
- Preserves true containment: issues live under their parent epic card.
- Avoids introducing a second board contract before first iteration is proven.

## Data Contract Changes
- Roadmap: release and epic remain canonical; epic section gains issue decomposition expectation.
- Planner: must produce issue breakdown for each epic before implementation starts.
- Planka: each active epic must include task list `Issues` with issue-formatted tasks.
- Obsidian: workflow notes add issue coverage links in `Artifacts` and `Decisions`.
- Memory: store workflow-model and agent-contract entities with relations enforcing issue-aware gates.

## Issue Definition Standard
Use compact issue IDs and acceptance language:
- Format: `ISS-<epic>-<nnn>: <outcome statement>`
- Example: `ISS-2.1-001: Reconcile roadmap/planka status drift`
- Rule: each issue must be independently verifiable and small enough for one short iteration.

## Agent Rollout Sequence (One Agent at a Time)
1. 01-Roadmap: define issue-level contract and epic readiness requirements.
2. 02-Planner: mandatory issue decomposition and sequencing.
3. 03-Analyst: analysis scoped per issue.
4. 04-Architect: architecture constraints mapped to issue sets.
5. 05-Security: threat controls and checks per issue.
6. 06-Critic: plan critique includes issue granularity quality gate.
7. 07-Implementer: execute/close issues with proof per issue.
8. 08-Code Reviewer: findings and verdict by issue.
9. 09-QA: test evidence and regression mapping by issue.
10. 10-UAT: acceptance decisions by issue and epic roll-up.
11. 11-DevOps: release gate requires issue completion roll-up.
12. 12-Retrospective: learning capture by issue cluster.
13. 13-PI: process improvements from issue-level metrics.

## skills.sh Discovery Evidence
Search basis: workflow, planning, project management, issue tracking.

| Candidate | URL | Fit | Decision | Rationale |
|---|---|---|---|---|
| find-skills | https://skills.sh/vercel-labs/skills/find-skills | Discovery/meta only | Adopt (supporting) | Useful for finding reusable skills, but not a delivery hierarchy contract. |
| skills docs/leaderboard samples | https://skills.sh/docs | Generic platform docs | Reject (direct use) | No direct release-epic-issue operational contract found. |

Conclusion: no external skill directly matches this repository's tri-tool workflow contract; proceed with local agent instruction updates.

## Risks and Controls
- Risk: issue definitions become too large.
  - Control: enforce issue size and independent verification language.
- Risk: partial rollout creates inconsistent behavior.
  - Control: one-agent-at-a-time with explicit rollout matrix and planka checklist.
- Risk: duplicate instruction roots drift.
  - Control: patch both `.github/agents/` and `vs-code-agents/agents/` for each agent step.

## Final Deliverables
- Updated agent contracts in both roots for all agents `01` through `13`:
  - `.github/agents/*.agent.md`
  - `vs-code-agents/agents/*.agent.md`
- Updated workflow handoff ledger with rollout completion and owner reset:
  - `agent-output/workflows/WF-21-cross-tool-workflow-confidence.md`
- Added memory entities and relations for issue-contract governance:
  - `.vscode/memory.jsonl`

## Validation Evidence
- Tri-tool preflight validated at close:
  - Planka card `1725309812348028678` present and synchronized.
  - Obsidian node `WF-21-cross-tool-workflow-confidence` resolves with owner `01-roadmap`.
  - Memory graph includes `workflow://release-epic-issue-model` and agent contract relations.
- Final marker audit across both roots (`26` files total) confirmed:
  - Every agent file contains `Release -> Epic -> Issue` hierarchy marker.
  - Every agent file contains issue ID contract references (`ISS-<epic>-<nnn>` / `ISS-*`).

## Outcome
The migration objective is complete. The workflow now enforces issue-level execution and evidence roll-up by default while preserving release-level governance.
