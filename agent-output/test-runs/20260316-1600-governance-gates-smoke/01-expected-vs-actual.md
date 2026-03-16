# Expected vs Actual

## Baseline Gates
- Expected: strict/scaffold/workflow/lint all pass.
- Actual: pass.

## Negative Test A (Strict Governance)
- Injection: renamed required heading in `.github/agents/13-pi.agent.md`.
- Expected: `.github/scripts/check_strict_governance.sh` fails.
- Actual: failed with `Missing workflow memory rules heading in .github/agents/13-pi.agent.md`.

## Negative Test B (Workflow Contract)
- Injection: added `[[WF-[ID]]]` placeholder to `agent-output/workflows/WF-IMPL-001.md`.
- Expected: `.github/scripts/check_workflow_contract.sh --changed-only` fails.
- Actual: failed with forbidden placeholder + missing note violations.

## Final Restored State
- Expected: all gates pass after rollback.
- Actual: pass (`strict`, `scaffold`, `workflow`, full markdown lint).
