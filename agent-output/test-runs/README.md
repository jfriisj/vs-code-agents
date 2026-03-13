# Model Test Runs

Use this folder to store reproducible model-validation runs.

Primary protocol: `.github/reference/model-test-run-protocol.md`

## Folder naming

Use one folder per run:

`YYYYMMDD-HHMM-[scenario-slug]`

Example: `20260313-1530-handoff-validation`

## Recommended contents

- `00-context.md` — environment, model, agent, branch, commit
- `01-expected-vs-actual.md` — acceptance criteria + observed behavior
- `02-reproduction-steps.md` — exact prompt/sequence to reproduce
- `03-failure-report.md` — filled from `.github/reference/model-failure-report-template.md`
- `04-agent-findings-log.md` — one-line findings summary per agent
- `evidence/` — raw outputs (`terminal.txt`, `problems.txt`, screenshots, etc.)

## Fast workflow

1. Create run folder.
2. Copy `.github/reference/model-failure-report-template.md` into `03-failure-report.md`.
3. Fill fields immediately when failure occurs.
4. Link the run folder from a WF node and relevant Planka card comment.
