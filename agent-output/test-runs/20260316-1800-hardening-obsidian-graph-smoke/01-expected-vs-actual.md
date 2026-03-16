# Expected vs Actual

## Baseline with New Hardening
- Expected: full stack passes with strengthened skill checker and Obsidian graph checker.
- Actual: pass.

## Negative Test A (Skill Semantics)
- Injection: removed `analysis-methodology` token from `12-retrospective.agent.md` declaration line.
- Expected: skill checker fails on retrospective role declaration.
- Actual: failed with expected missing-token error.

## Negative Test B (Obsidian Graph Contract)
- Injection: changed `# Obsidian Graph Memory` heading in `09-qa.agent.md`.
- Expected: Obsidian graph checker fails.
- Actual: failed with expected missing heading error.

## Final Restored State
- Expected: full stack passes after restoring both edits.
- Actual: pass (`skill`, `obsidian graph`, `strict`, `scaffold`, `workflow`, lint).
