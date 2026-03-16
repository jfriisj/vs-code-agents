# Expected vs Actual

## Baseline with New Skill Gate
- Expected: `check_skill_gate_coverage.sh` passes and full governance stack remains green.
- Actual: pass.

## Negative Test (Skill Gate)
- Injection: removed `analysis-methodology` token from `.github/agents/13-pi.agent.md` wording.
- Expected: `check_skill_gate_coverage.sh` fails on PI role and Process Hardening stage coverage.
- Actual: failed with 2 errors exactly as expected.

## Final Restored State
- Expected: full stack returns green after restoring PI token.
- Actual: pass (`skill-gate`, `strict`, `scaffold`, `workflow`, markdown lint).
