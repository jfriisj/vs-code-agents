# VS Code Agents - Deep Dive Documentation

> This comprehensive guide covers advanced usage patterns, agent collaboration, Obsidian graph integration, Planka Agile tracking, and the design philosophy behind this multi-agent workflow.
>
> **New users**: Start with [USING-AGENTS.md](USING-AGENTS.md) for quick setup.

---

## Table of Contents

1. [Design Philosophy](#design-philosophy)
2. [Agent Collaboration Patterns](#agent-collaboration-patterns)
3. [The Document-Driven Workflow](#the-document-driven-workflow)
4. [Obsidian Graph Integration](#obsidian-graph-integration)
5. [Planka Agile Integration](#planka-agile-integration)
6. [Agent Deep Dives](#agent-deep-dives)
7. [Customization Guide](#customization-guide)
8. [Troubleshooting & FAQ](#troubleshooting--faq)
9. [Agent Orchestration Playbook](#agent-orchestration-playbook)

---

## Design Philosophy

### Why Multiple Specialized Agents?

A single general-purpose AI tries to do everything—plan, code, test, review—often poorly. By splitting responsibilities:

1. **Each agent has clear constraints**: Planner can't write code, Implementer can't redesign
2. **Quality gates are built in**: Critic reviews before implementation, Security audits before production
3. **Handoffs create checkpoints**: Work is documented at each stage
4. **Specialization improves quality**: A security-focused agent catches vulnerabilities a general agent misses

### The Separation of Concerns

| Concern | Agent(s) | Key Constraint |
|---------|----------|----------------|
| **Vision** | 01-Roadmap | Outcomes, not implementation |
| **Planning** | 02-Planner | WHAT/WHY, never HOW (no code) |
| **Research** | 03-Analyst | Analysis only, no fixes |
| **Design** | 04-Architect | Patterns, not implementation details |
| **Quality** | 06-Critic | Reviews, doesn't modify artifacts |
| **Security** | 05-Security | Findings, doesn't implement remediations |
| **Implementation** | 07-Implementer | Follows plans, doesn't redesign |
| **Code Quality** | 08-Code Reviewer | Quality gate before QA, can reject |
| **Testing** | 09-QA | Test strategy, not business value |
| **Value** | 10-UAT | Business value, not technical quality |
| **Release** | 11-DevOps | Requires explicit user approval |

### Document-First Development

Every agent produces **Markdown documents** in `agent-output/`:

```text
agent-output/
├── planning/           # Plans with WHAT/WHY
├── analysis/           # Research findings
├── architecture/       # ADRs and design decisions
├── critiques/          # Plan reviews
├── security/           # Security assessments
├── qa/                 # Test strategies
├── uat/                # Value validation
├── retrospectives/     # Lessons learned
└── releases/           # Release documentation


```

**Why documents?**

* **Auditability**: See what was decided and why
* **Handoff context**: Next agent reads the artifacts
* **Memory anchors**: Obsidian stores graph relations to these documents
* **Version control**: Track evolution of decisions

---

## Agent Collaboration Patterns

### Pattern 1: The Planning Pipeline

```text
┌──────────┐    ┌─────────┐    ┌───────────┐    ┌──────────┐
│ Roadmap  │───▶│ Planner │───▶│ Analyst/  │───▶│  Critic  │
│ (vision) │    │ (plan)  │    │ Architect │    │ (review) │
└──────────┘    └─────────┘    │ /Security │    └──────────┘
                               └───────────┘           │
                                                       ▼
                                               ┌──────────────┐
                                               │ Implementer  │
                                               │ (approved)   │
                                               └──────────────┘


```

**When to use**: Starting a new feature from scratch.

**Example flow**:

1. Select **Roadmap** → Define epic: "User authentication system"
2. Select **Planner** → Create plan from epic → `agent-output/planning/001-auth-plan.md`
3. Select **Analyst** → Research OAuth providers → `agent-output/analysis/001-auth-analysis.md`
4. Select **Architect** → Review design fit → updates plan or creates ADR
5. Select **Security** → Threat model → `agent-output/security/001-auth-security.md`
6. Select **Critic** → Final review → `agent-output/critiques/001-auth-plan-critique.md`
7. Select **Implementer** → Code when approved

### Pattern 2: The Implementation Loop

```text
┌─────────────┐    ┌─────────────┐    ┌──────┐    ┌──────┐    ┌────────┐
│ Implementer │───▶│ Code        │───▶│  QA  │───▶│ UAT  │───▶│ DevOps │
│   (code)    │    │ Reviewer    │    │(test)│    │(value)│    │(release)│
└─────────────┘    └─────────────┘    └──────┘    └──────┘    └────────┘
       ▲               │               │           │
       └───────────────┴───────────────┴───────────┘
              (fix issues)


```

**When to use**: Plan is approved, coding phase.

**Example flow**:

1. Select **Implementer** → Implement plan → code changes + tests
2. Select **Code Reviewer** → Verify code quality → `agent-output/code-review/001-auth-code-review.md`
3. If quality issues: back to Implementer
4. Select **QA** → Verify coverage → `agent-output/qa/001-auth-qa.md`
5. If gaps: back to Implementer
6. Select **UAT** → Validate value → `agent-output/uat/001-auth-uat.md`
7. If gaps: back to Implementer
8. Select **DevOps** → Release → requires user approval

### Pattern 3: The Investigation Branch

```text
┌─────────────┐    ┌─────────┐    ┌─────────────┐
│ Any Agent   │───▶│ Analyst │───▶│ Back to     │
│ hits unknown│    │(research)    │ calling agent
└─────────────┘    └─────────┘    └─────────────┘


```

**When to use**: Hit technical uncertainty during any phase.

**Example flow**:

1. With **Planner** selected, planning auth but unsure about JWT vs session tokens
2. Select **Analyst** → investigates → `agent-output/analysis/002-jwt-vs-sessions.md`
3. Findings go back to Planner to inform the plan

**Incident/bug variant (when evidence is incomplete)**:

* If logs/telemetry are insufficient to prove a single root cause, Analyst switches to an uncertainty-aware format: label Verified vs Hypothesis, then pivot to system weaknesses + required telemetry. A reusable template exists at `vs-code-agents/reference/uncertainty-review-template.md`.

### Pattern 4: The Security Gate

```text
┌─────────────┐    ┌──────────┐    ┌─────────────┐
│ Any Phase   │───▶│ Security │───▶│ Continue or │
│ (sensitive) │    │ (audit)  │    │ Block       │
└─────────────┘    └──────────┘    └─────────────┘


```

**When to use**: Feature touches auth, sensitive data, external interfaces.

**Security can be invoked**:

* During planning (threat model)
* During implementation (code audit)
* Before production (final gate)

### Pattern 5: The Retrospective Cycle

```text
┌──────────┐    ┌───────────────┐    ┌────────────────────┐
│ Delivery │───▶│ Retrospective │───▶│ Process Improvement│
│ complete │    │ (lessons)     │    │ (evolve agents)    │
└──────────┘    └───────────────┘    └────────────────────┘


```

**When to use**: After feature delivery, to improve the workflow.

**Example flow**:

1. Feature shipped
2. Select **Retrospective** → captures what went well/poorly
3. Select **Process Improvement** → updates agent instructions if patterns emerge

---

## The Document-Driven Workflow

### Document Naming Convention

```text
NNN-feature-name-type.md


```

* **NNN**: Sequential number (001, 002, ...)
* **feature-name**: Descriptive name (auth-system, api-refactor)
* **type**: Document type (plan, analysis, critique, security, etc.)

**Examples**:

* `001-user-auth-plan.md`
* `001-user-auth-analysis.md`
* `001-user-auth-plan-critique.md`
* `001-user-auth-code-audit.md`

### Document Structure Standards

Every document should have:

1. **Changelog** (at top): Track revisions
2. **Value Statement** (plans): "As a [user] I want [X] so that [Y]"
3. **Clear Sections**: Standardized headings
4. **Status/Verdict**: Current state (APPROVED, BLOCKED, etc.)
5. **References**: Links to related documents

### Document Status Tracking

All agents track and update document status fields. This provides at-a-glance visibility into document state:

| Status | Meaning |
| --- | --- |
| `Draft` | Initial creation, not yet reviewed |
| `In Progress` | Actively being worked on |
| `Pending Review` | Ready for next agent's review |
| `Approved` | Passed review gate |
| `Blocked` | Cannot proceed until issues resolved |
| `Released` | Committed and pushed |

Agents update status when:

* **Implementer**: Marks plan "In Progress" when starting implementation
* **Critic/QA/UAT**: Updates to "Approved" or "Blocked" after review
* **DevOps**: Updates to "Released" after successful release

### Document Lifecycle and Closure

Completed documents move to `closed/` subfolders to keep active work visible:

```text
agent-output/
├── planning/
│   ├── 085-active-feature.md      ← currently active
│   └── closed/
│       ├── 080-completed.md       ← archived after commit
│       └── 081-completed.md
├── qa/
│   └── closed/
└── ...


```

**Key concepts:**

| Concept | Description |
| --- | --- |
| **Unified numbering** | All documents in a work chain share the same ID (analysis 080 → plan 080 → qa 080) |
| **`.next-id` file** | Global counter at `agent-output/.next-id`, incremented by originating agents |
| **Terminal statuses** | `Committed`, `Released`, `Abandoned`, `Deferred`, `Superseded` trigger closure |
| **Closure trigger** | DevOps moves docs to `closed/` after successful commit |
| **Orphan detection** | Agents self-check on start; Roadmap runs periodic sweep |

See `document-lifecycle` skill for full details.

### Open Question Gate

Plans may contain `OPEN QUESTION` items that require resolution before implementation.

**Question lifecycle:**

1. Planner marks unresolved questions as `OPEN QUESTION: [description]`
2. When resolved, Planner updates to `OPEN QUESTION [RESOLVED]: [description]` or `[CLOSED]`
3. Before handoff, Planner warns user if unresolved questions remain

**Implementer behavior:**

* Scans plans for unresolved `OPEN QUESTION` items
* If any exist, **halts and strongly recommends resolution** before proceeding
* Requires explicit user acknowledgment to proceed despite warning
* Documents user's decision in implementation doc

> [!CAUTION]
> Proceeding with unresolved open questions risks building on flawed assumptions. Always resolve or explicitly acknowledge before implementation.

### Handoff Protocol

When handing off between agents, we rely on **Obsidian Workflow Notes** (`WF-[ID]`).

```markdown
## Handoff Ready
Parent Node context for the next agent is [[WF-NNN-feature-type]]


```

---

## Obsidian Graph Integration

### Replacing the External Memory Server

Instead of relying on an external, opaque Memory MCP server that dumps massive JSON blobs into the context window, this workflow uses **Obsidian** as its native long-term memory graph.

**Why Obsidian is superior for Agent Memory**:

* **Token Efficiency**: Agents load tiny "summary nodes" instead of full document histories.
* **Relational Graph**: YAML frontmatter defines exact relationships (Epic -> Plan -> Implementation).
* **Auditability**: You can visually open your Obsidian vault and see exactly how decisions map to one another.
* **Tools**: Relies purely on the `mcp-obsidian/*` toolset.

### The "Summary Node" Pattern

To prevent context window bloat, agents do not dump massive contents into Obsidian. They create lightweight `WF-[ID]` (Workflow) nodes. These nodes act as **pointers and semantic edges**.

**The 10-Line Rule for `WF-` Notes**:

1. **Frontmatter**: Graph relations (Type, Status, Parent/Child links).
2. **TL;DR**: Maximum 3 bullet points summarizing the decision, constraint, or verdict.
3. **Artifact Link**: A direct path to the full markdown file in `agent-output/`.

*Example of a Workflow Node (`workflows/WF-002-Auth-Plan.md`):*

```markdown
---
ID: 002
Type: Plan
Status: Active
parent: "[[WF-001-Auth-Epic]]"
Blocks: "[[WF-004-Security-Audit]]"
---
### Summary
* Decided to use JWT tokens over session cookies.
* Defined 4 implementation milestones.
* See artifact for exact file paths.

**Artifact**: `agent-output/planning/002-auth-plan.md`


```

### Retrieval and Storage Patterns

**Retrieval (Lazy Loading)**:
When an agent starts a task or receives a handoff, it should NOT search the entire vault. It should:

1. Read the provided `[[WF-[ID]]]` note using `#mcp-obsidian/read_note`.
2. Understand the context from the bullet points and frontmatter.
3. Follow the `parent:` link if broader strategic context is needed.
4. Only read the full `agent-output/` artifact if deep implementation details are strictly necessary.

**Storage**:
Agents update the graph when:

* Completing a task or phase.
* Making a significant decision.
* Handing off to another agent.

They use `#mcp-obsidian/patch_note` to update the Status, append a quick summary bullet, or link to a new downstream node.

### Memory Enables Agent Collaboration

Without the Obsidian graph, each agent session starts fresh. With it:

1. **Analyst** creates an analysis node (`WF-003`) linked to the plan.
2. **Planner** reads `WF-003` to instantly understand the POC results.
3. **Security** links their audit node to the plan, blocking it if necessary.
4. **Implementer** retrieves constraints from the Planner's node before coding.

Memory is the connective tissue that makes multi-agent workflows coherent.

---

## Planka Agile Integration

While Obsidian acts as the relational memory graph and `agent-output/` serves as the authoritative source of truth for documents, **Planka** is the execution engine. It provides the Agile Kanban view for tracking task progression, labels, and day-to-day execution status.

### The Triad of Truth

1. **Markdown (`agent-output/`)**: *What* we are building and *Why* (Full details).
2. **Obsidian Graph (`workflows/`)**: *How* decisions relate to each other (Memory).
3. **Planka Board**: *Who* is doing what, and *Where* it is in the pipeline. Execution is driven by **Native MCP Tools** directly interacting with Planka.

### Agent Roles in Planka

Agents use the `planka-workflow` skill to keep the board synchronized:

* **01-Roadmap**: The owner of the Planka board. Uses the Python CLI script `sync_roadmap_epics.py` to bulk-reconcile `product-roadmap.md` with Planka, ensuring every Epic has a corresponding card, correct release/priority labels, and lifecycle columns (`Planned`, `In Progress`, `Delivered`).
* **02-Planner**: Reads the Epic card and uses **native MCP tools** (`create_task_list`, `create_task`) to translate plan milestones into actionable Tasks on the card. Appends handoff comments linking back to Obsidian.
* **03-Analyst**: Creates an "Analysis & Spikes" Task List via MCP tools and leaves a comment with findings when research is done.
* **04-Architect**: Creates an "Architecture & Design" Task List via MCP tools for design constraints and leaves an Approved/Rejected verdict comment.
* **05-Security**: Tracks required controls and vulnerabilities via MCP tasks.
* **06-Critic**: Manages visual labels (e.g., `Plan Approved` vs `Revision Required`) via `add_label_to_card` and appends their critique link to the card's comments.

**Handoff Synergy (The Triad Bridge)**:
When an agent finishes its work, it updates the Obsidian graph, updates the Planka board (checking off tasks and adding verdict comments via native MCP), and ensures its final comment points the next agent to the correct `[[WF-ID]]` node.

---

## Agent Deep Dives

### Roadmap Agent

**Purpose**: Own product vision and ensure features align with business objectives.

**Key Responsibilities**:

* Define and maintain product roadmap
* Translate business needs into epics
* Validate that plans deliver stated value
* Guard the "Master Product Objective"
* Bulk-synchronize the master roadmap with the Planka board using `sync_roadmap_epics.py`

**When NOT to use**:

* Implementation details
* Technical decisions
* Code review

---

### Planner Agent

**Purpose**: Transform epics into implementation-ready plans.

**Key Responsibilities**:

* Create structured plans with WHAT and WHY
* Define milestones and deliverables
* Identify unknowns requiring investigation
* Coordinate with Analyst, Architect, Security
* Map plan steps to Planka tasks using native MCP tools

**Critical Constraint**: **Never writes code or implementation details**.

Plans answer:

* WHAT are we building?
* WHY are we building it (value statement)?
* WHAT are the acceptance criteria?
* WHAT dependencies exist?

Plans do NOT contain:

* HOW to implement (code snippets, algorithms)
* Test case implementations
* Technical architecture (that's Architect's job)

---

### Analyst Agent

**Purpose**: Deep technical investigation when unknowns arise.

**Key Responsibilities**:

* Research APIs, libraries, patterns
* Conduct experiments and benchmarks
* Analyze root causes
* Document findings with evidence

**Uncertainty-aware investigation (incident/bug work)**:

* If a root cause cannot be proven with available evidence, Analyst must NOT force a narrative.
* Analyst uses an objective hard pivot trigger (timebox/evidence gate) to stop digging and pivot to system weaknesses + required telemetry.
* Telemetry is classified as **normal** vs **debug** (always-on actionable signals vs opt-in verbose signals).

**Key Constraint**: **Investigates but doesn't fix**. Produces analysis docs, not code changes.

---

### Architect Agent

**Purpose**: Maintain system design coherence.

**Key Responsibilities**:

* Create and maintain Architecture Decision Records (ADRs)
* Define patterns and boundaries
* Review plans for architectural fit
* Guide cross-cutting concerns

**Observability is architecture (incident/bug work)**:

* When RCA is uncertain, Architect treats insufficient telemetry as an architectural risk.
* Architect requires explicit normal-vs-debug guidance and recommends a minimum viable incident telemetry baseline.

**Key Constraint**: **Defines WHERE things live, not exact implementation**.

---

### Critic Agent

**Purpose**: Quality gate for plans before implementation.

**Key Responsibilities**:

* Review plans for clarity, completeness, scope
* Check architectural alignment
* Track critique resolution
* Manage visual labels (Approved/Rejected) on Planka cards via native MCP tools

**Key Constraint**: **Reviews but doesn't modify**. Creates critique docs, doesn't edit plans.

**Verdicts**:

* Issues → Recommend revision
* Clean → Approve for implementation

---

### Security Agent

**Purpose**: Comprehensive security assessment and guidance.

**Five-Phase Framework**:

1. **Architectural Security**: Trust boundaries, STRIDE threat modeling, attack surface
2. **Code Security**: OWASP Top 10, language-specific vulnerabilities
3. **Dependency Security**: CVE scanning, supply chain risks
4. **Infrastructure Security**: Headers, TLS, container security
5. **Compliance**: OWASP ASVS, NIST, industry standards

**Key Constraint**: **Identifies and documents, doesn't fix**. Provides remediation guidance.

---

### Implementer Agent

**Purpose**: Write code that implements approved plans.

**Key Responsibilities**:

* Implement plan requirements
* Write and run tests
* Create implementation documentation
* Request clarification when plan is ambiguous
* Update task progress natively in Planka

**Key Constraint**: **Follows the plan**. Doesn't redesign or expand scope.

---

### Code Reviewer Agent

**Purpose**: Quality gate between implementation and QA.

**Key Responsibilities**:

* Review code for architecture alignment (uses Architect's docs as source of truth)
* Check SOLID, DRY, YAGNI, KISS principles
* Verify TDD compliance
* Assess documentation and comments (explaining "why" not "what")

**Key Constraint**: **Reviews but doesn't fix**. Can reject on code quality alone.

**Authority**: CAN REJECT implementation before QA invests testing time.

---

### QA Agent

**Purpose**: Ensure technical quality through testing.

**Key Responsibilities**:

* Design test strategy
* Verify test coverage
* Execute tests
* Identify gaps

**Diagnosability as a QA concern (incident/bug work)**:

* If a root cause cannot be proven, QA expects changes to improve diagnosability (telemetry markers, correlation IDs, structured context).

**Key Constraint**: **Technical quality, not business value** (that's UAT).

---

### UAT Agent

**Purpose**: Validate that implementation delivers business value.

**Key Responsibilities**:

* Read plan's value statement
* Review Implementation, Code Review, and QA docs (document-based, not code inspection)
* Verify implementation satisfies value statement
* Assess from user perspective
* Make release recommendation

**Key Constraint**: **Value, not technical quality** (that's QA). Quick sanity check when docs are present.

---

### DevOps Agent

**Purpose**: Manage releases safely.

**Key Responsibilities**:

* Verify packaging and versioning
* Execute release process
* Move Planka card to `Delivered` via native MCP tools
* Require explicit user approval

**Critical Constraint**: **Must ask user before releasing**. Never auto-releases.

---

### Retrospective & Process Improvement Agents

**Purpose**: Capture lessons after delivery and evolve the workflow.

**Critical Constraint**: **Requires user approval** before modifying `.agent.md` files.

---

## Skills System

Agents leverage **Claude Skills**—modular, reusable instruction sets that load on-demand via progressive disclosure. This keeps agent files lean while providing deep expertise when needed.

### Available Skills

| Skill | Purpose | Key Content |
| --- | --- | --- |
| `obsidian-workflow` | Graph Storage Contract | When/how to retrieve and store, anti-patterns, graph edges |
| `planka-workflow` | Agile tracking & Native MCP | Workflow board conventions, task lists, and the Triad of Truth bridge |
| `analysis-methodology` | Investigation techniques | Confidence levels, gap tracking, POC guidance |
| `architecture-patterns` | ADR templates, patterns, anti-patterns | Layered architecture, repository pattern, STRIDE |
| `code-review-checklist` | Pre/post-implementation review criteria | Value statement assessment, security checklist |
| `code-review-standards` | Code review checklist, severity definitions, templates | Review focus areas, finding format, document template |
| `cross-repo-contract` | Multi-repo API type safety | Contract discovery, sync workflow, breaking change coordination |
| `document-lifecycle` | Unified numbering, closure, orphan detection | ID inheritance, terminal statuses, closed/ folders |
| `engineering-standards` | SOLID, DRY, YAGNI, KISS | Detection patterns, refactoring guidance |
| `release-procedures` | Two-stage release workflow, semver | Version consistency, platform constraints |
| `security-patterns` | OWASP Top 10, language vulnerabilities | Python, JavaScript, Java, Go specific patterns |
| `testing-patterns` | TDD workflow, test pyramid | Anti-patterns, coverage strategies, mocking |

### Skill Placement

Skills are placed in different directories depending on your VS Code version:

| Version | Location | Notes |
| --- | --- | --- |
| **VS Code Stable (1.107.1)** | `.claude/skills/` | Legacy location, still supported |
| **VS Code Insiders** | `.github/skills/` | New recommended location |

> [!NOTE]
> These locations are changing with upcoming VS Code releases. The `.github/skills/` location is becoming the standard. Check the [VS Code Agent Skills documentation](https://code.visualstudio.com/docs/copilot/customization/agent-skills) for the latest guidance.

### Creating Skills

Each skill is a directory with a `SKILL.md` file:

```text
vs-code-agents/skills/
└── my-skill/
    ├── SKILL.md           # Required: skill definition
    ├── references/        # Optional: detailed docs
    │   └── guide.md
    └── scripts/           # Optional: automation
        └── check.sh


```

**SKILL.md format:**

```yaml
---
name: my-skill
description: Brief description of when to use this skill
license: MIT
metadata:
  author: yourname
  version: "1.0"
---

# Skill Title

Detailed instructions, tables, code examples...


```

---

## Customization Guide

### Adding New Agents

1. Create `your-agent.agent.md` in `vs-code-agents/agents/`
2. Follow the frontmatter format:

```yaml
---
description: One-line description
name: YourAgent
tools: ['edit/createFile', 'search', ...]
model: Claude 4.5 Sonnet (or preferred)
handoffs:
  - label: Handoff Name
    agent: TargetAgent
    prompt: Suggested prompt
    send: false
---


```

3. Define Purpose, Responsibilities, Constraints
4. Include the Obsidian Contract and Planka Contract sections
5. Copy to `.github/agents/` in your workspace

### Modifying Existing Agents

**Safe to modify**:

* `description`: Update for clarity
* `model`: Change to preferred model
* `handoffs`: Add/remove handoff targets
* Response style preferences

**Modify with caution**:

* `tools`: Removing tools limits capability
* Constraints: Removing constraints changes behavior significantly

**Generally don't modify**:

* Core separation of concerns (e.g., making Planner write code)

### Creating Workspace-Specific Variants

You can have project-specific agent variants:

1. Copy agent from `vs-code-agents/agents/` to `.github/agents/`
2. Modify for project needs
3. Project-specific agents override global agents with same name

---

## Troubleshooting & FAQ

### Agent Issues

**Q: Agent not appearing in Copilot**

* Check file location: `.github/agents/` for workspace, [VS Code profile folder](https://code.visualstudio.com/docs/configure/profiles) for user-level
* Verify file extension is `.agent.md`
* Reload VS Code

**Q: Agent ignores constraints**

* Re-invoke with explicit constraint reminder
* Check if constraint is clear in the `.agent.md` file
* Models sometimes drift; be explicit

**Q: Agent tries to do another agent's job**

* Use explicit handoff: "Hand off to [Agent] for [task]"
* Reference the agent's constraints

### Obsidian Graph Issues

**Q: Obsidian integration not working**

* Is the `mcp-obsidian` server enabled for this workspace?
* Do agents have access to the `mcp-obsidian/*` tools?
* Check relevant MCP/server logs or VS Code output for MCP connection errors.

**Q: Retrievals return irrelevant results**

* Stop searching the full vault. Ensure the agent uses `read_note` on the specific `WF-[ID]` handoff node.

### Planka Issues

**Q: Cards aren't updating or syncing natively**

* Ensure the `mcp-planka` server is running (e.g., via Docker on port 25478) and connected in your VS Code MCP tool settings.
* Verify agents have permission to call tools like `add_comment` or `create_task_list`.
* For the **Roadmap agent only**: Check if the Planka URL and API tokens are correctly set in your `.env` for the `sync_roadmap_epics.py` bulk script.

### Workflow Issues

**Q: Plans have too much implementation detail**

* Remind Planner of constraint: "WHAT and WHY, not HOW"
* Check if Planner `.agent.md` has this constraint

**Q: Security review is superficial**

* Use the enhanced Security agent (v2)
* Request specific phases: "Conduct Phase 2 (Code Security Review)"
* Provide specific files/endpoints to review

**Q: Too many handoffs, losing context**

* Ensure the Obsidian summary nodes (`WF-[ID]`) are used correctly to maintain context.
* Reference artifact paths explicitly.

### General FAQ

**Q: Do I need all 13 agents?**
No. Start with Planner + Implementer. Add others as needed.

**Q: Can I use this without Obsidian?**
Yes, but agents won't remember context across handoffs effectively. Each conversation will require you to manually reference the artifact files.

**Q: Why separate QA and UAT?**

* QA = Technical quality (tests pass, coverage adequate)
* UAT = Business value (feature solves the stated problem)

**Q: Why can't Planner write code?**
Keeping planning separate from implementation:

* Forces clear requirements before coding
* Prevents premature implementation decisions
* Makes plans reviewable by non-coders

**Q: How do I handle urgent fixes that don't need full planning?**
For hotfixes:

1. Go directly to Implementer with clear scope
2. Have Security review if security-relevant
3. QA for test verification
4. Skip full planning pipeline

---

## Contributing

Improvements to agents are welcome! Key areas:

* **Agent refinements**: Better constraints, clearer responsibilities
* **New agents**: For specialized workflows
* **Documentation**: Examples, tutorials, troubleshooting
* **Obsidian/Planka patterns**: Better integration strategies

See individual agent files for their specific improvement opportunities.

---

## Agent Orchestration Playbook

> This section documents when and how to use local, background, and subagent execution patterns for custom agents in VS Code 1.107+.

### Execution Modes Overview

| Mode | When to Use | Key Characteristics |
| --- | --- | --- |
| **Local Interactive** | Planning, strategy, review, handoffs | User in the loop, real-time collaboration |
| **Background Agent** | Long-running implementation, parallel tasks | Git worktree isolation, hands-off execution |
| **Subagent** | Focused subtask delegation | Context-isolated, returns findings to caller |

### Phase 1: Local Interactive (Strategy & Planning)

**Agents**: Roadmap, Architect, Planner, Analyst, Critic, Security (threat modeling)

**Pattern**: User selects agent from dropdown in VS Code chat. Conversation is interactive with frequent checkpoints.

```text
User selects Roadmap agent → "Define epic for X"
     selects Planner agent → "Create plan for epic"
     selects Architect agent → "Review architectural fit"
     selects Critic agent → "Review plan 002"


```

> [!NOTE]
> Custom agents are selected from the agents dropdown—not invoked with `@` syntax. The `@` symbol is for built-in participants like `@workspace`.

**When to use**:

* Defining strategic direction (Roadmap)
* Creating or revising plans (Planner)
* Architectural decisions requiring judgment (Architect)
* Pre-implementation reviews (Critic, Security)
* Research with unclear scope (Analyst)

**Tool approvals**: Generally safe to auto-approve read-only tools. Terminal commands should be reviewed case-by-case.

### Phase 2: Background Implementation (Execution)

**Agents**: Implementer, QA, Security (code audit)

**Pattern**: After plan approval, run execution-focused agents as background agents in Git worktrees for isolated, parallel, or long-running work.

```text
Planner (plan approved) ──▶ Background: Implementer in worktree
                            Background: QA test strategy
                            Background: Security code audit


```

**When to use**:

* Multi-file implementation (Implementer)
* Comprehensive test execution (QA)
* Full 5-phase security audits (Security)
* Any task expected to take >15 minutes

**Benefits**:

* Git worktree isolation prevents interference with main workspace
* Can run multiple background agents in parallel (e.g., QA + Security)
* Results can be reviewed and selectively merged

**Tool approvals**: Background agents should NOT have "allow all" terminal access. Review and approve commands explicitly, especially for:

* Package installs
* Test execution with side effects
* Any file writes outside `agent-output/`

### Phase 3: Review & Merge (Validation)

**Agents**: QA, UAT, Security, DevOps

**Pattern**: Return to local interactive mode to review background agent results, validate value delivery, and prepare release.

```text
Background results ──▶ Local: @QA verify tests
                       Local: @UAT validate value
                       Local: @Security final gate
                       Local: @DevOps release (user approval required)


```

**When to use**:

* Reviewing background implementation results
* Final value validation (UAT)
* Pre-release security gate (Security)
* Release execution (DevOps always local, always requires explicit user approval)

### Subagent Usage Patterns

**Definition**: A subagent is invoked by another agent (the "caller") to perform a focused, context-isolated task. The subagent returns findings to the caller rather than taking independent action.

**Subagent-Eligible Agents** (may be auto-invoked):

| Agent | Subagent Use Case |
| --- | --- |
| Analyst | Clarify technical questions mid-implementation |
| Security | Targeted security review of specific code |
| QA | Test implications for a specific change |
| Retrospective | Synthesize lessons after a subtask completes |

**Explicit-Only Agents** (should NOT be auto-invoked):

| Agent | Reason |
| --- | --- |
| Roadmap | Strategic decisions require user involvement |
| Architect | System-level decisions need explicit review |
| Process Improvement | Cross-cutting process changes need approval |
| DevOps | Release actions require explicit user confirmation |

**Subagent Invocation Example**:

```text
Implementer working on feature
├── Hits technical unknown
├── Invokes Analyst as subagent: "How does API X handle pagination?"
├── Analyst returns findings
└── Implementer continues with answer


```

### Security and Tool Approval Guidance

#### Tool Approval Categories

**Always Manual Approval** (never auto-approve):

* `execute/runInTerminal` with destructive commands (rm, git push --force, npm publish)
* `execute/runTask` for deploy/publish tasks
* Any command modifying infrastructure or external services
* Package install commands in production contexts

**Session Auto-Approval Eligible** (based on risk tolerance):

* Read-only file operations
* Linters and formatters
* Test execution (unit tests with no external dependencies)
* `git status`, `git diff`, `git log`

**Treat as Untrusted** (validate before following):

* `fetch` results from external URLs
* MCP tool outputs
* User-pasted content from external sources

#### Per-Agent Tool Safety Rules

**Implementer**:

* Auto-approve: file reads, search, linters
* Manual approve: terminal commands, package installs
* Never auto-approve: git push, npm publish, deploy scripts

**QA**:

* Auto-approve: test execution (isolated), file reads
* Manual approve: test execution with external dependencies
* Never auto-approve: commands modifying test data in shared environments

**DevOps**:

* Manual approve: ALL terminal commands
* MUST get explicit user confirmation before any release action
* Never auto-approve: git tag, npm publish, vsce publish

**Security**:

* Auto-approve: file reads, grep, dependency scans
* Manual approve: network requests, vulnerability scanner execution
* Never auto-approve: any command that could exfiltrate data

### Orchestration Quick Reference

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    AGENT ORCHESTRATION FLOW                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  PHASE 1: LOCAL INTERACTIVE (Strategy)                              │
│  ┌─────────┐   ┌─────────┐   ┌──────────┐   ┌────────┐             │
│  │ Roadmap │──▶│ Planner │──▶│ Architect│──▶│ Critic │             │
│  └─────────┘   └─────────┘   └──────────┘   └────────┘             │
│       │             │              │             │                   │
│       └─────────────┴──────────────┴─────────────┘                   │
│                    [Analyst/Security as needed]                      │
│                                                                     │
│  PHASE 2: BACKGROUND (Execution) ─── Git Worktree Isolation         │
│  ┌─────────────┐   ┌────────────┐   ┌──────────────┐               │
│  │ Implementer │   │     QA     │   │   Security   │               │
│  │ (parallel)  │   │ (parallel) │   │  (parallel)  │               │
│  └─────────────┘   └────────────┘   └──────────────┘               │
│                                                                     │
│  PHASE 3: LOCAL INTERACTIVE (Validation)                            │
│  ┌──────┐   ┌──────┐   ┌──────────┐   ┌────────┐                   │
│  │  QA  │──▶│ UAT  │──▶│ Security │──▶│ DevOps │                   │
│  │verify│   │value │   │  gate    │   │release │                   │
│  └──────┘   └──────┘   └──────────┘   └────────┘                   │
│                                         ▲                           │
│                                         │                           │
│                              [USER APPROVAL REQUIRED]               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘


```

---

## License

MIT License - see [LICENSE](https://www.google.com/search?q=LICENSE)
