---
ID: 1
Origin: 1
UUID: 22222222
Status: Active
handoff_id: "[[WF-1]]"
---

# VS Code Agents - System Architecture

**Last Updated**: 2026-03-13
**Architect**: 04-Architect (GitHub Copilot)
**Status**: DRAFT - Initializing Foundation

## Changelog
| Date | Change | Rationale | Plan/Epic |
|------|--------|-----------|-----------|
| 2026-03-15 | Approved Planka Sync Strategy | Added mapping durability & telemetry requirements. | Plan-003 |
| 2026-03-15 | Formalized Memory Invariants | Added ID Contract & 10-Line Rule. | Plan-002 |
| 2026-03-13 | Initial Architecture Draft | Establish baseline for multi-agent system. | Epic 1.1 |

## Purpose
A multi-agent workflow system for GitHub Copilot in VS Code that brings structure, quality gates, and long-term memory to AI-assisted development.

## High-Level Architecture
The system follows a role-based multi-agent pattern where specialized agents handle distinct parts of the development lifecycle, coordinated via shared memory (Obsidian) and agile tracking (Planka).

### Components
1. **Roadmap Agent**: Owns `product-roadmap.md` and high-level Epic synchronization.
2. **Architect Agent**: Owns `system-architecture.md`, ADRs, and structural invariants.
3. **Analyst Agent**: Performs research and provides technical context.
4. **Planner/Critic Agent**: Creates and validates executable implementation plans.
5. **Implementer/QA Agent**: Executes plans and verifies quality.

## Runtime Flows
- **Memory Initialization**: [Date: 2026-03-15] Reconciled from Plan-002: Standardized `WF-` ID contract (`WF-E<epic-id>`, `WF-P<plan-id>`, etc.) and 10-Line Rule.
- **Epic Initiation**: User -> Roadmap Agent -> Planka Epic Card -> Architecture Assessment.
- **Task Execution**: Architect Review -> Planner -> Critic Review -> Implementer -> QA -> Architect Audit.

## Data Boundaries
- **Workspace**: Source code and local configuration.
- **Agent Output**: Standardized directory structure for agent artifacts (`/agent-output/`).
- **Memory**: Obsidian vault for relational context and handoffs using `WF-<ID>` nodes in `agent-output/workflows/`.
- **Agile**: Planka for execution visibility and status tracking.

## Quality Attributes
- **Maintainability**: Strict separation of concerns between roles.
- **Traceability**: Unified numbering and document lifecycle (`document-lifecycle` skill).
- **Persistence**: Long-term memory decoupled from chat history.

## Problem Areas
- [ ] Circular dependencies between agent toolsets.
- [ ] Context window limits for large architectural summaries.

## Decisions (ADRs)
- **ADR-002: Dynamic Planka-Roadmap Sync (Idempotent Architecture)**
  - **Context**: Static IDs in Planka vary across board instances. Manual status sync is error-prone.
  - **Choice**: Use name-based list resolution and diff-based sync with mandatory telemetry logging.
  - **Consequences**: Robust visibility across environments; overhead of metadata retrieval.
- **ADR-001: Role-Based Agent Specialization**
  - **Context**: LLMs struggle with multi-stage complex tasks in a single prompt.
  - **Choice**: Separate roles into specialized agents with distinct toolsets.
  - **Consequences**: Higher quality output; requires robust handoff mechanism.

## Recommendations
- Enforce **Den Gyldne Rengøringsregel**: Leave the architecture cleaner than you found it.
- Prioritize telemetry/observability in all new module designs.
