# Context

- Run ID: 20260316-1600-governance-gates-smoke
- Date: 2026-03-16
- Scenario: Governance gate verification + controlled failure injection + restore
- Trigger: User requested to continue and prove the current governance setup works end-to-end.

## Scope

1. Baseline gate validation.
2. Negative test: strict governance gate failure.
3. Negative test: workflow contract gate failure.
4. Immediate restoration and final all-green validation.
5. Persist auditable evidence bundle.

## Acceptance Criteria

- Baseline checks pass.
- Each injected fault is detected by the intended checker.
- Repository state is restored.
- Final checks pass with zero lint errors.
