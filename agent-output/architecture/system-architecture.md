# System Architecture: VS Code Agent Ecosystem

**Last Updated**: 2026-03-06
**Status**: Initial Baseline (In-Progress)
**Architecture Owner**: 04-Architect

## Changelog
| Date       | Change                                      | Rationale                                     | Plan/Epic |
|------------|---------------------------------------------|-----------------------------------------------|-----------|
| 2026-03-06 | Initial Baseline established during Plan-1 review | Live test of optimized agent ecosystem. | Plan-1 / Epic 1.1 |

---

## 1. Purpose
The VS Code Agent Ecosystem is a modular, multi-agent system designed to automate the software development lifecycle (SDLC) from roadmap planning to deployment. It emphasizes clear handoffs, standardized communication artifacts, and integration with external tools like Planka (Agile) and Obsidian (Relational Knowledge).

## 2. High-Level Architecture
The system follows a **Pipelined Agent Workflow** where each agent acts as a specialized node with defined inputs, outputs, and tool permissions.

### 2.1 Component Overview
- **Roadmap (01)**: Strategic vision and Epic management.
- **Planner (02)**: Detailed implementation planning.
- **Analyst (03)**: R&D, root cause analysis, and technical investigations.
- **Architect (04)**: Design authority and system integrity.
- **Implementer (07)**: Code execution and modification.
- **QA (09)**: Verification and validation.
- **DevOps (11)**: Environment, release, and automation management.

## 3. Runtime Flows
### 3.1 Feature Lifecycle (v0.1.0)
1. **Roadmap** -> `product-roadmap.md` -> Synced to Planka.
2. **Planner** -> `Planning Artifact` -> Linked to Planka Card.
3. **Architect** -> `Architecture Findings` -> Approval/Rejection of Plan.
4. **Implementer/Analyst** -> `Implementation` -> Planka Task Updates.
5. **QA** -> `QA Results` -> Final Verification.

## 4. Data Boundaries
- **Workdir**: Active project source code.
- **`agent-output/`**: Standardized directory for all agent-generated artifacts.
- **Planka**: External source of truth for task status and agile visibility.
- **Obsidian**: Relational graph for cross-agent context (Workflow nodes).

## 5. Architectural Invariants
### 5.1 Den Gyldne Rengøringsregel
- Every architectural change MUST leave boundaries, coupling, and diagnosability cleaner than before.
- Minimum Expectation: Structural risk reduction or telemetry improvement.

### 5.2 Artifact Integrity
- Every plan MUST have a unique ID and UUID.
- Every architectural finding MUST reference a Plan ID and Epic.

## 6. Problem Areas & Design Debt
- **[DD-001] Script Type Validation**: `planka_ops.py` currently fails on numeric string IDs due to incorrect integer casting in `parse_value`.
- **[DD-002] Path Hardcoding**: Historical use of `vs-code-agents/` prefix in agent instructions (fixed in v0.1.0).

## 7. Decisions (ADRs)
### ADR-001: Standardized Agent Root Variables
- **Status**: Accepted
- **Context**: Agents were using hardcoded relative paths, making the system brittle to directory moves.
- **Decision**: All agents resolve `*_ROOT` and `*_PATH` variables at runtime based on workspace structure.
- **Consequences**: (+) Improved portability; (-) Slight increase in agent instruction complexity.

---

## 8. Recommendations
- **Immediate**: Fix [DD-001] via the Analyst-Implementer cycle as planned in Plan-1.
- **Strategic**: Implement centralized telemetry (Correlation IDs) across all agent tool calls.
