---ID: 1
Origin: 1
UUID: 11111111
Status: Active
handoff_id: "[[WF-1]]"
---

# VS Code Agents - Product Roadmap

**Last Updated**: 2026-03-13
**Roadmap Owner**: Roadmap Agent
**Strategic Vision**: Establish a robust, memory-backed multi-agent workflow system in VS Code that ensures structural integrity, quality gates, and long-term context retention for AI-assisted development.

## Change Log
| Date & Time | Change | Rationale |
|-------------|--------|-----------|
| 2026-03-13 13:00 | Initial Roadmap Creation | Baseline product vision and initial epics for system stabilization. |

---

## Release v0.1.0 - Foundation & Core Workflow
**Target Date**: 2026-04-01
**Strategic Goal**: Establish the core infrastructure and basic agent coordination for memory-backed workflows.

### Epic 1.1: Multi-Agent Coordination Layer
**Priority**: P0
**Status**: Delivered [CardID: 1729878110406444893] [BoardID: 1729877970501240657] [WF-E1.1]

**User Story**:
As a developer, I want a structured system where different AI agents (Planner, Architect, Roadmap, Reviewer) collaborate on tasks, so that I get higher quality code with less manual oversight.

**Business Value**:
- Reduces cognitive load on the developer.
- Ensures distinct roles for planning, design, and execution.
- Prevents "context drift" in complex tasks.

**Dependencies**:
- None

**Acceptance Criteria**:
- [x] Agents can hand off tasks using a standardized protocol.
- [x] Clear separation of concerns between Planner and Architect roles.

### Epic 1.2: Persistent Memory with Obsidian
**Priority**: P0
**Status**: In Progress [CardID: 1729878166190688097] [BoardID: 1729877970501240657] [WF-E1.2]

**User Story**:
As a developer, I want my project's context and decisions to persist across chat sessions via Obsidian, so that the AI doesn't forget previous architectural choices.

**Business Value**:
- Enables long-lived project maintenance.
- Provides a searchable knowledge base of AI-led decisions.

**Dependencies**:
- None

**Acceptance Criteria**:
- [ ] Automated generation of `WF-*` nodes in Obsidian for tactical tracking.
- [ ] Roadmap and Architecture artifacts linked in memory graph.

### Epic 1.3: Planka Agile execution visibility
**Priority**: P1
**Status**: In Progress [CardID: 1729878222469859173] [BoardID: 1729877970501240657] [WF-E1.3]

**User Story**:
As a product owner, I want to see the status of AI-driven epics and tasks in a Kanban board, so that I can track progress transparently.

**Business Value**:
- Provides high-level visibility into AI agent activities.
- Bridges the gap between AI automation and traditional project management.

**Dependencies**:
- None

**Acceptance Criteria**:
- [ ] Epics from roadmap are synchronized to Planka "Epics" board.
- [ ] Status updates in Planka reflect roadmap state.

---

## Active Release Tracker
| Release | Theme | Status | Target Date |
|---------|-------|--------|-------------|
| v0.1.0  | Foundation | In Progress | 2026-04-01 |

### Epic Readiness Matrix (v0.1.0)
| Epic ID | Title | Status | Linked Plans | Blockers |
|---------|-------|--------|--------------|----------|
| 1.1     | Multi-Agent Coordination Layer | Delivered | Plan 001 | - |
| 1.2     | Persistent Memory with Obsidian | EPIC APPROVED | - | - |
| 1.3     | Planka Agile execution visibility | EPIC APPROVED | - | - |

---

# Artifact Metadata Standard (Document Lifecycle)

---
ID: 001
Origin: 000
UUID: a1b2c3d4
Status: Draft
---
