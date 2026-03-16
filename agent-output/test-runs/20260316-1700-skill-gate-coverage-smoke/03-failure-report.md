Run-ID: 20260316-1700-skill-gate-coverage-smoke
Date: 2026-03-16
Agent: GitHub Copilot
Model: GPT-5.3-Codex
Scenario: skill-gate-negative-test
Severity: LOW
Status: Verified

## 1) Expected Behavior

- New skill-gate checker catches missing role/stage skill coverage.
- Restored state returns checker and full stack to green.

## 2) Actual Behavior

- Checker failed with two violations after injection:
  - missing `analysis-methodology` in PI role-specific check,
  - missing Process Hardening stage coverage for `analysis-methodology`.
- Checker passed after restoration.

## 3) Reproduction Steps

See `02-reproduction-steps.md`.

## 4) Prompt & Context

- Prompt used: "continue"
- Context: verify whether runs use skills correctly and close the gap with enforceable validation.

## 5) Evidence Links

- Terminal output: `evidence/terminal.txt`
- Problems output: `evidence/problems.txt`
- Prompt trace: `evidence/prompt.txt`
- Outcome trace: `evidence/response.txt`

## 6) Root Cause Hypotheses

- Prior governance checks verified file/heading integrity but did not enforce phase/role skill coverage.

## 7) Fix Plan

- Added `.github/scripts/check_skill_gate_coverage.sh`.
- Integrated checker into CI, required file catalog, scaffold inventory, strict governance docs, and bootstrap guide.

## 8) Verification

- [x] Reproduced failure
- [x] Restored and re-ran
- [x] Full stack green
- [x] No markdown lint regressions

## 9) Closure Note

- Skill-gate coverage is now explicitly enforced and audited.
