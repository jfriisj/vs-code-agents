# Context

- Run ID: 20260316-1700-skill-gate-coverage-smoke
- Date: 2026-03-16
- Scenario: Validate skill-gate coverage enforcement and proof of failure detection.
- Trigger: Follow-up from governance smoke run to verify whether test runs use required skills correctly.

## Scope

1. Add automated skill-gate checker.
2. Integrate checker into governance/CI/docs.
3. Run baseline stack with new checker.
4. Inject one controlled skill-gate failure.
5. Restore state and re-run full stack.

## Acceptance Criteria

- Skill-gate checker reports pass on compliant state.
- Skill-gate checker fails on targeted missing-skill injection.
- Repository returns to compliant state after restore.
- Final gate stack passes with markdown lint green.
