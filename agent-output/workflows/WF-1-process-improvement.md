---
workflow_id: WF-1-process-improvement
project_name: "Agent System"
type: PI
parent: "[[WF-1-retrospective]]"
status: Improvement Implemented
owner: 13-pi
last_updated: 2026-03-07
---

## Summary
- PI WF-1: Lifecycle Hardening (Epic 1.1)
- Normalized to the unified workflow schema on 2026-03-07.

## Relations
- **Depends On**: [[WF-1-retrospective]]
- **Blocks**: none

## Decisions
- Preserved legacy decision context below.

### Legacy Notes
### Summary
- PI WF-1: Lifecycle Hardening (Epic 1.1)
- Normalized to the unified workflow schema on 2026-03-07.

### Relations
- **Depends On**: [[WF-1-retrospective]]
- **Blocks**: none

### Decisions
- Preserved legacy decision context below.

### Legacy Notes
# PI WF-1: Lifecycle Hardening (Epic 1.1)

### Strategic Process Improvements
Based on Retrospective 1, the following process improvements have been codified:

1. **PI-001-GIT**: **Mandatory Git Force-Staging**. DevOps and agents MUST use `git add -f` for ignored `agent-output/` and `.github/` folders to ensure release record trackability.
2. **PI-001-CODE**: **Context-Aware Parsing Pattern**. Adopt the "Identify and Protect" pattern for numeric string IDs (e.g. `*Id`) to prevent incorrect integer casting as established in `planka_ops.py`.
3. **PI-001-PATH**: **Absolute Path Enforcement**. All skill-based helper scripts MUST be executed using absolute paths to survive `cwd` shifts across agent handoffs.
4. **SEC-002**: **Mandatory Log Sanitization**. Helper scripts MUST redact sensitive environment variables (`PLANKA_TOKEN`, etc.) before outputting `stdout/stderr`.
5. **PLANKA-EXIT-GATE**: All agent files (`01` through `13`) now contain a mandatory Planka post-condition verification gate to prevent comment-only completion drift.
6. **PLANKA-OPS HARDENING**: Added MCP retry/backoff and new idempotent CLI operations (`tasklist:ensure`, `task:ensure`, `comment:ensure-phase`, `phase:close`) with fail-safe behavior when backend payload shape blocks reliable checklist dedupe.

### Artifact Archive
- **PI Master Record**: [agent-output/pi/001-lifecycle-hardening.md](agent-output/pi/001-lifecycle-hardening.md)
- **Shared Repository Patterns**: [memories/repo/patterns.md](memories/repo/patterns.md)
- **Planka Sync Gap Analysis**: [agent-output/analysis/004-planka-card-sync-gap-analysis.md](agent-output/analysis/004-planka-card-sync-gap-analysis.md)

### Constraints
- 1. **PI-001-GIT**: **Mandatory Git Force-Staging**. DevOps and agents MUST use `git add -f` for ignored `agent-output/` and `.github/` folders to ensure release record trackability.
- 2. **PI-001-CODE**: **Context-Aware Parsing Pattern**. Adopt the "Identify and Protect" pattern for numeric string IDs (e.g. `*Id`) to prevent incorrect integer casting as established in `planka_ops.py`.
- 3. **PI-001-PATH**: **Absolute Path Enforcement**. All skill-based helper scripts MUST be executed using absolute paths to survive `cwd` shifts across agent handoffs.
- 4. **SEC-002**: **Mandatory Log Sanitization**. Helper scripts MUST redact sensitive environment variables (`PLANKA_TOKEN`, etc.) before outputting `stdout/stderr`.

### Artifacts
- agent-output/pi/001-lifecycle-hardening.md
- agent-output/analysis/004-planka-card-sync-gap-analysis.md

### Handoffs
### 2026-03-07 00:00 [workflow-migration]
- Status: Legacy workflow note normalized to the unified schema.
- Decisions: Placeholder identifiers and stale aliases were remapped where possible.
- Changes: Frontmatter, headings, and graph links were standardized.
- Next Owner: n/a
- Open Risks: Review parent and block links if upstream workflow IDs change.
- Artifacts: agent-output/workflows/WF-1-process-improvement.md

### 2026-03-07 00:01 [legacy-handoff]

### Next
- Keep this note immutable unless reconciliation with source artifacts is required.

## Constraints
- 1. **PI-001-GIT**: **Mandatory Git Force-Staging**. DevOps and agents MUST use `git add -f` for ignored `agent-output/` and `.github/` folders to ensure release record trackability.
- 2. **PI-001-CODE**: **Context-Aware Parsing Pattern**. Adopt the "Identify and Protect" pattern for numeric string IDs (e.g. `*Id`) to prevent incorrect integer casting as established in `planka_ops.py`.
- 3. **PI-001-PATH**: **Absolute Path Enforcement**. All skill-based helper scripts MUST be executed using absolute paths to survive `cwd` shifts across agent handoffs.
- 4. **SEC-002**: **Mandatory Log Sanitization**. Helper scripts MUST redact sensitive environment variables (`PLANKA_TOKEN`, etc.) before outputting `stdout/stderr`.

## Artifacts
- agent-output/pi/001-lifecycle-hardening.md
- agent-output/analysis/004-planka-card-sync-gap-analysis.md
- agent-output/workflows/WF-1-process-improvement.md
- [[WF-1-retrospective]]

## Handoffs
### 2026-03-07 00:00 [workflow-migration]
- Status: Legacy workflow note normalized to the unified schema.
- Decisions: Placeholder identifiers and stale aliases were remapped where possible.
- Changes: Frontmatter, headings, and graph links were standardized.
- Next Owner: n/a
- Open Risks: Review parent and block links if upstream workflow IDs change.
- Artifacts: agent-output/workflows/WF-1-process-improvement.md

### 2026-03-07 00:01 [legacy-handoff]
- Status: - Status: Handoff Ready. Parent Node context for the next agent is [[WF-1-process-improvement]].

## Next
- Keep this note immutable unless reconciliation with source artifacts is required.
