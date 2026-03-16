Run-ID: 20260316-1600-governance-gates-smoke
Date: 2026-03-16
Agent: GitHub Copilot
Model: GPT-5.3-Codex
Scenario: controlled-governance-negative-tests
Severity: LOW
Status: Verified

## 1) Expected Behavior

- Negative injections should be caught by the corresponding gate.
- After rollback, all checks should return to green.

## 2) Actual Behavior

- Both injected failures were detected exactly by intended checks.
- All checks passed after restoration.

## 3) Reproduction Steps

See `02-reproduction-steps.md`.

## 4) Prompt & Context

- Prompt used: "continue"
- Active context: governance cleanup and verification continuation.

## 5) Evidence Links

- Run folder: `agent-output/test-runs/20260316-1600-governance-gates-smoke/`
- Terminal output: `agent-output/test-runs/20260316-1600-governance-gates-smoke/evidence/terminal.txt`
- Problems output: `agent-output/test-runs/20260316-1600-governance-gates-smoke/evidence/problems.txt`

## 6) Root Cause Hypotheses (if RCA incomplete)

- Not applicable. No persistent defect remained after test sequence.

## 7) Fix Plan

- Not applicable. This was a verification run with temporary fault injection.

## 8) Verification

- [x] Reproduced before fix
- [x] Patch applied
- [x] Re-run scenario passes
- [x] No regressions detected

## 9) Closure Note

- Final result: governance and workflow gates validated via positive + negative tests.
- Follow-up actions: none required.
