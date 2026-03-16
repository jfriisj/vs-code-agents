# Context

- Run ID: 20260316-1800-hardening-obsidian-graph-smoke
- Date: 2026-03-16
- Scenario: Hardening checks for skill semantics + per-role declarations + Obsidian graph contract.
- Trigger: User requested optional hardening implementation and explicit confidence in Obsidian graph usage.

## Scope

1. Strengthen `check_skill_gate_coverage.sh` semantics.
2. Add per-role assertions for release/retrospective declarations.
3. Add `check_obsidian_graph_contract.sh`.
4. Integrate new checker in CI/governance docs.
5. Run baseline, two controlled negative tests, restore, and final rerun.

## Acceptance Criteria

- Baseline passes with new checks.
- Skill checker fails on declared-skill drift.
- Obsidian checker fails on graph-contract heading drift.
- Repository restored to all-green state.
