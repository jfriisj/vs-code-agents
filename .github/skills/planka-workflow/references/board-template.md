# Planka Board Template (Agile Epic Management)

**Project**: `<Project Name from roadmap heading>`
**Board**: `Epics`

## Status Lists (Columns)
Kortene bevæger sig gennem disse kolonner baseret på deres overordnede livscyklus.

1. `Planned` (Backlog og godkendte Epics)
2. `In Progress` (Epics under aktiv udvikling, test eller review)
3. `Delivered` (Kode i produktion)
4. `Deferred` (Udskudt eller droppet)
5. `Closed` (Terminal tilstand for gamle kort)

## Primary Workflow Card (Epic)
Hvert kort repræsenterer en komplet Epic.

**Title**: `Epic [X.Y]: [Title]`
**Due Date**: Sync from release `**Target Date**` when available (`YYYY-MM-DDT23:59:59.000Z`).

**Description template**:
Beskrivelsen fungerer som "Single Source of Truth" i Planka. Den indeholder Epic-definitionen i toppen, og agenterne tilføjer løbende links til deres markdown-filer i bunden.

**User Story**:
As a [user type], I want [capability/outcome], So that [business value/benefit].

**Business Value**:
- [Why this matters]

**Dependencies**:
- [List]

**Acceptance Criteria** (outcome-focused):
- [ ] [Observable outcome 1]
- [ ] [Observable outcome 2]

**Constraints**:
- [List]

**Labels (Portfolio Overview):**
- `Release vX.Y.Z`
- `Priority P0|P1|P2|P3`

**Default Task-List Scaffolding (bootstrap mode `--ensure-task-lists`):**
- `Acceptance Criteria`
- `Analysis & Spikes`
- `Architecture & Design`
- `Security & Compliance`
- `Implementation`
- `Code Review`
- `QA & Testing`
- `UAT & Acceptance`
- `Release & Deployment`
- `Retrospective & Learnings`

---
**Artifacts (Appended by agents):**
- [Analysis]: agent-output/analysis/...
- [Plan]: agent-output/planning/...
- [Architecture]: agent-output/architecture/...
- [Implementation]: agent-output/implementation/...
- [QA]: agent-output/qa/...