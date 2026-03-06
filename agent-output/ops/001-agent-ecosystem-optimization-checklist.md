---
ID: 001
Type: Ops
Status: Active
Title: Agent Ecosystem Optimization Checklist Execution
Date: 2026-03-06
source_agents:
  - vs-code-agents/agents/01-roadmap.agent.md
  - vs-code-agents/agents/02-planner.agent.md
  - vs-code-agents/agents/03-analyst.agent.md
  - vs-code-agents/agents/04-architect.agent.md
  - vs-code-agents/agents/05-security.agent.md
  - vs-code-agents/agents/06-critic.agent.md
  - vs-code-agents/agents/07-implementer.agent.md
  - vs-code-agents/agents/08-code-reviewer.agent.md
  - vs-code-agents/agents/09-qa.agent.md
  - vs-code-agents/agents/10-uat.agent.md
  - vs-code-agents/agents/11-devops.agent.md
  - vs-code-agents/agents/12-retrospective.agent.md
  - vs-code-agents/agents/13-pi.agent.md
source_skills:
  - vs-code-agents/skills/obsidian-workflow/SKILL.md
  - vs-code-agents/skills/planka-workflow/SKILL.md
source_workflows:
  - .github/workflows/markdown-lint.yml
  - vs-code-agents/workflows/markdown-lint.yml
source_hooks: []
canonical_artifact: agent-output/ops/001-agent-ecosystem-optimization-checklist.md
---

# Agent Ecosystem Optimization Checklist Execution

## Scope
- Focused implementation pass on Planner plus ecosystem safety/consistency fixes required to prevent parser/runtime failures.
- Repository root resolved as `/home/jonfriis/Dokumenter/vs-code-agents`.
- Canonical tracked roots in this repo:
  - `agents_root`: `vs-code-agents/agents/`
  - `skills_root`: `vs-code-agents/skills/` (with one legacy tracked file under `.github/skills/`)
  - `workflows_root`: both `.github/workflows/` and `vs-code-agents/workflows/` are tracked

## skills.sh Discovery Evidence (MANDATORY)
Search terms used:
- `find-skills`, `skill-creator`, `agent-tools`, `workflow`, `ci`, `hook`, `prompt`, `memory`, `obsidian`

Candidates evaluated:
1. `https://skills.sh/vercel-labs/skills/find-skills`
- Fit: high for mandatory external-skill discovery policy and repeatable search workflow.
- Gaps: does not itself implement optimization logic.
- Decision: `Adopt` (as process pattern for future skill-related work).

2. `https://skills.sh/anthropics/skills/skill-creator`
- Fit: high for prompt slimming, progressive disclosure, and eval-driven skill quality loops.
- Gaps: broad skill-authoring workflow; needs adaptation to this repo conventions.
- Decision: `Adapt` (use principles, not full workflow verbatim).

3. `https://skills.sh/tul-sh/skills/agent-tools`
- Fit: low for this repo (focuses on inference.sh app runtime).
- Gaps: not aligned with Planner/Workflow optimization scope.
- Security posture on listing: failed warnings shown.
- Decision: `Reject`.

## Phase-by-Phase Checklist Status

### Phase 1: Agent Definition & Prompt Tuning
- [x] Strip Narrative Fluff (Planner section tightening, direct command style retained)
- [x] Consolidate Constraints (Planner constraints tightened around `PLANNING_ROOT` + degraded mode)
- [~] Standardize Handoffs (format mostly consistent; payload token variants still differ by agent role)
- [x] Dynamic Pathing (Planner now resolves `PROJECT_NAME`, `ROADMAP_PATH`, `ARCHITECTURE_PATH`, `PLANNING_ROOT`)
- [x] Verify Graceful Degradation (Planner now explicitly degrades to markdown-only mode if integrations fail)

Implemented in:
- `vs-code-agents/agents/02-planner.agent.md`

### Phase 2: Tool Environment & Security
- [x] Enforce Terminal Baselines (Planner now explicitly uses `bash` baseline on Linux/CachyOS)
- [x] Audit Tool Scope (Planner tool scope reduced to minimum required set)
- [~] Validate MCP Connections (host settings inspected; explicit mappings for obsidian/planka/memory not present in `~/.config/Code/User/settings.json` excerpt)
- [x] Idempotent Operations (Planner Planka section now mandates read-first, diff-only updates)

Implemented in:
- `vs-code-agents/agents/02-planner.agent.md`

Evidence:
- `python3 .github/skills/planka-workflow/scripts/planka_ops.py --help` succeeds.
- `mcp_memory_search_nodes` callable.
- `mcp_mcp-obsidian_get_notes_info` callable.
- `mcp_planka_get_board` reachable (400 on fake ID confirms endpoint path is active).

### Phase 3: Skill Modularity & Reuse
- [x] skills.sh Discovery Pass
- [~] Single Responsibility Principle (assessed; broad scripts still exist, no script refactor done in this pass)
- [~] Standardize Skill I/O (partial: existing scripts mostly JSON-friendly; not fully normalized across all skill scripts)

### Phase 4: Workflow & Graph Relations
- [~] Map the Edge Graph (documented relation chain below; not yet enforced by automatic check across all docs)
- [x] Stop Content Duplication (Planner/Roadmap wording preserves canonical `agent-output/*` source rule)
- [~] Orphan Sweep (policy exists; full repository orphan sweep not run in this pass)
- [~] Verify Memory Checkpoints (explicit in prompts; no runtime assertion hooks yet)

Relation chain (target model):
- `Agent -> Skill -> Workflow -> Hook -> Artifact`
- Example:
  - `02-planner.agent.md -> planka-workflow SKILL -> markdown-lint workflow -> (future hook event) -> agent-output/planning/*.md`

### Phase 5: Hooks & CI/CD Pipelines
- [~] Trigger Precision (no dedicated webhook trigger scripts in this repo for Planka state changes)
- [~] Add Fallbacks (not fully implemented for external webhook failure logging)
- [x] Optimize Linting/Testing Cycles (markdown lint workflow changed to changed-files only)

Implemented in:
- `.github/workflows/markdown-lint.yml`
- `vs-code-agents/workflows/markdown-lint.yml`

Validation:
- Both YAML files parse successfully via `python3` + `yaml.safe_load`.

## Additional Ecosystem Safety Fix
Parser-stability replacement executed across agents:
- Replaced `#tool:mcp-obsidian/*` with parser-safe `mcp-obsidian_*` wording in all tracked agent files under `vs-code-agents/agents/`.

## Open Items / Blockers
1. MCP mapping verification is partial because user-level VS Code settings show only `CodeGraphContext` in the visible `mcpServers` section.
2. Handoff payload standardization still has role-specific variants (`WF-[Plan-ID]`, `WF-[Calling-ID]`, etc.); standard contract file should be introduced to normalize this.
3. Hook-level fallback logging for external failures is not implemented yet (requires dedicated hook scripts/events).

## Recommended Next Execution Slice
1. Normalize handoff contract string and payload placeholders across all agents.
2. Run tool-scope minimization pass for Architect/Security/Critic/QA/UAT/DevOps.
3. Add a dedicated workflow/hook validation script that checks:
- parser-safe tool tokens
- mandatory handoff line format
- dynamic pathing block presence
- forbidden wildcard scopes by agent role
