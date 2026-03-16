Run-ID: 20260316-1800-hardening-obsidian-graph-smoke
Date: 2026-03-16
Agent: GitHub Copilot
Model: GPT-5.3-Codex
Scenario: hardening-skill-and-obsidian-contract-negative-tests
Severity: LOW
Status: Verified

## 1) Expected Behavior

- New semantic skill checks fail when required role declaration is removed.
- Obsidian graph contract checks fail when required graph heading is removed.
- Full stack returns to green after restoration.

## 2) Actual Behavior

- Skill checker failed as expected on retrospective declaration drift.
- Obsidian graph checker failed as expected on graph heading drift.
- Final restored run returned all checks green.

## 3) Reproduction Steps

See `02-reproduction-steps.md`.

## 4) Prompt & Context

- Prompt used: "do it, also i want to be sure the agents use obsidian graph correctly"
- Context: optional hardening was requested and executed.

## 5) Evidence Links

- Terminal output: `evidence/terminal.txt`
- Problems output: `evidence/problems.txt`
- Prompt trace: `evidence/prompt.txt`
- Outcome trace: `evidence/response.txt`

## 6) Root Cause Hypotheses

- Prior checker relied on broad token presence and lacked dedicated Obsidian graph contract validation.

## 7) Fix Plan

- Strengthened skill checker to verify mandatory declaration semantics.
- Added per-role assertions for retrospective/process declarations.
- Added dedicated Obsidian graph contract checker.
- Integrated both into CI and governance catalogs.

## 8) Verification

- [x] Baseline passes
- [x] Skill negative test fails as expected
- [x] Obsidian negative test fails as expected
- [x] Restored final rerun passes
- [x] Markdown lint remains clean

## 9) Closure Note

- Hardening complete: skill and Obsidian graph usage are now actively enforced.
