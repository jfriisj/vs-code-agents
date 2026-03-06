# Changelog

All notable changes to this repository will be documented in this file.

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.0] - 2026-03-06

### Added
- **Optimized Agent Instruction Set**: Comprehensive updates to all 13 agent role definitions for improved task execution and integration.
- **Planka Integration Regression Suite**: Added `test_planka_ops.py` to verify ID handling and security redaction logic.
- **Workflow State Management**: New `agent-output/` directory structure for tracking plan, implementation, and verification artifacts.

### Fixed
- **Planka ID Type Casting**: Fixed critical bug in `planka_ops.py` where numeric string IDs (e.g. `1724...`) were incorrectly cast to integers, breaking MCP tool calls.
- **Log Sanitization**: Implemented `PLANKA_TOKEN` and secret redaction in script error logs (SEC-002) to prevent credential leakage.
- **Redundant Imports**: Resolved issue in `planka_ops.py` where imports were duplicated across exception handlers.

### Changed
- **Lifecycle Pipeline**: Validated the complete round-trip and handoff between Roadmap, Planner, Architect, Implementer, Code Reviewer, QA, UAT, and DevOps.

## 2026-01-18

### Added

- **Code Reviewer agent**: New quality gate between Implementer and QA. Reviews code for architecture alignment, SOLID/DRY/YAGNI/KISS, TDD compliance, documentation/comments, security, and code smells. Can reject on quality alone.
- **code-review-standards skill**: Extracted review checklist, severity definitions, and document templates for reuse.

### Changed

- **UAT agent simplified**: Now a quick, document-based value validation (read-only tools only). Relies on Implementation, Code Review, and QA docs rather than inspecting code directly.
- **Implementer handoff**: Now goes to Code Reviewer instead of QA directly.
- **Workflow updated**: `Implementer → Code Reviewer → QA → UAT → DevOps`

## 2026-01-15

### Added

- Uncertainty-aware issue analysis guidance across Analyst, Architect, and QA agents.
- Analyst hard pivot trigger to avoid forced root-cause narratives when evidence is missing.
- Normal vs debug telemetry criteria, plus a minimum viable incident telemetry baseline.
- Reusable uncertainty review template: `vs-code-agents/reference/uncertainty-review-template.md`.

### Changed

- QA guidance now prefers validating telemetry via structured fields/events over brittle log string matching.
