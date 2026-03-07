# 003 - Obsidian Workflow Hardening Brief

Date: 2026-03-07
Status: Validated
Owner: agent-optimizer

## Scope
- Stabilize Obsidian workflow validation without external runtime dependencies.
- Normalize all tracked `agent-output/workflows/WF-*.md` notes to one schema.
- Remove placeholder WF identifiers from tracked agent instructions.
- Add CI gate for workflow graph verification.

## Baseline Findings
- Verifier was not runnable in a clean environment due to missing `yaml` package.
- `agent-output/ops/workflow-index.md` did not exist.
- Workflow schema drift: mixed frontmatter keys and missing required sections.
- Unresolved link aliases in workflow notes (`WF-Plan-1`, `WF-Deployment-v0.1.0`, etc.).
- Agent instructions contained placeholder examples that could leak into live notes.

## skills.sh Discovery Evidence

| Candidate Skill | URL | Fit | Decision | Rationale |
|---|---|---|---|---|
| find-skills | https://skills.sh/vercel-labs/skills/find-skills | Medium | Adapt | Useful for discovery workflow, but does not provide an Obsidian schema migrator/verifier. |
| web-design-guidelines | https://skills.sh/vercel-labs/agent-skills/web-design-guidelines | Low | Reject | Frontend review guidance; not related to markdown graph validation or migration. |
| frontend-design | https://skills.sh/anthropics/skills/frontend-design | Low | Reject | Frontend aesthetic generation guidance; unrelated to Obsidian graph integrity. |

Notes:
- `skills.sh` query pages are JS-heavy and redirect to `/?q=...`, but direct skill pages were reachable and reviewed.
- No suitable external skill was found for this repository-specific workflow contract migration and verifier gate.

## Implemented Changes
- Added zero-dependency verifier:
  - `vs-code-agents/skills/obsidian-workflow/scripts/verify-obsidian-graph.mjs`
- Added one-time migration/index generator:
  - `vs-code-agents/skills/obsidian-workflow/scripts/migrate-workflow-notes.mjs`
- Normalized Obsidian skill contract and templates:
  - `vs-code-agents/skills/obsidian-workflow/SKILL.md`
  - `vs-code-agents/skills/obsidian-workflow/references/workflow-note-template.md`
  - `vs-code-agents/skills/obsidian-workflow/references/workflow-index-template.md`
- Migrated workflow notes and generated managed index:
  - `agent-output/workflows/WF-1.md` ... `agent-output/workflows/WF-7.md`
  - `agent-output/workflows/WF-1-retrospective.md`
  - `agent-output/workflows/WF-1-process-improvement.md`
  - `agent-output/ops/workflow-index.md`
  - `agent-output/ops/002-obsidian-workflow-migration-report.md`
- Hardened tracked agent instructions against placeholder leakage:
  - `vs-code-agents/agents/01-roadmap.agent.md` ... `vs-code-agents/agents/13-pi.agent.md`
- Added CI verification workflow:
  - `.github/workflows/obsidian-graph-verify.yml`
  - `vs-code-agents/workflows/obsidian-graph-verify.yml`

## Validation Results
- Migration run: `Migrated 9 workflow note(s)`.
- Verifier run: `Obsidian graph verification passed for 9 workflow note(s)`.
- Placeholder token scan in tracked agents: no `WF-*-ID` or `[[WF-[...]]]` matches.

## Measurable Improvement
- Graph verification execution reliability: from non-runnable to deterministic local run (no external package install required).
- Workflow schema compliance: from `0/9` fully compliant notes to `9/9` passing verifier.
- Unresolved workflow wikilink targets: from multiple missing aliases to zero verifier failures.

## Relation Map
- Agent -> Skill:
  - `vs-code-agents/agents/*` -> `vs-code-agents/skills/obsidian-workflow/SKILL.md`
- Skill -> Workflow:
  - `vs-code-agents/skills/obsidian-workflow/scripts/verify-obsidian-graph.mjs` -> `.github/workflows/obsidian-graph-verify.yml`
- Workflow -> Artifact:
  - `.github/workflows/obsidian-graph-verify.yml` -> `agent-output/workflows/*.md`, `agent-output/ops/workflow-index.md`
- Hook/Trigger -> Validation:
  - GitHub `pull_request`/`push` -> verifier script pass/fail gate

## Rollback Plan
- Revert new workflow gate files and script changes if false positives block delivery.
- Restore previous `WF-*` note revisions from git history if migration content mapping is unacceptable.
- Keep `agent-output/ops/002-obsidian-workflow-migration-report.md` for traceability.

## Prompt and Token Window Audit
- Consolidated duplicate protocol blocks in the Obsidian skill to reduce instruction ambiguity.
- Replaced role-placeholder WF tokens with concrete-ID guidance, reducing downstream repair cycles and repeated context reads.
