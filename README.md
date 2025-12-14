# VS Code Agents

> A multi-agent workflow system for GitHub Copilot in VS Code that brings structure, quality gates, and long-term memory to AI-assisted development.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## The Problem

AI coding assistants are powerful but chaotic:
- They forget context between sessions
- They try to do everything at once (plan, code, test, review)
- They skip quality gates and security reviews
- They lose track of decisions made earlier

## The Solution

This repository provides **specialized AI agents** that each own a specific part of your development workflow:

| Agent | Role |
|-------|------|
| **Roadmap** | Product vision and epics |
| **Planner** | Implementation-ready plans (WHAT, not HOW) |
| **Analyst** | Deep technical research |
| **Architect** | System design and patterns |
| **Critic** | Plan quality review |
| **Security** | Comprehensive security assessment |
| **Implementer** | Code and tests |
| **QA** | Test strategy and verification |
| **UAT** | Business value validation |
| **DevOps** | Packaging and releases |
| **Retrospective** | Lessons learned |
| **ProcessImprovement** | Workflow evolution |
| **Memory** | Cross-session context |

Each agent has **clear constraints** (Planner can't write code, Implementer can't redesign) and produces **structured documents** that create an audit trail.

## Quick Start

### 1. Get the Agents

```bash
git clone https://github.com/yourusername/agents.git
```

### 2. Add to Your Project

Copy agents to your workspace:
```
your-project/
└── .github/
    └── agents/
        ├── planner.agent.md
        ├── implementer.agent.md
        └── ... (others you need)
```

### 3. Use in Copilot Chat

```
@Planner Create a plan for adding user authentication
@Implementer Implement the approved plan at agent-output/planning/001-auth-plan.md
```

### 4. (Recommended) Enable Memory

Install [Flowbaby](https://marketplace.visualstudio.com/items?itemName=flowbaby.flowbaby) for cross-session memory:

1. VS Code Extensions → Search "Flowbaby" → Install
2. Command Palette → "Flowbaby: Initialize Workspace"
3. Command Palette → "Flowbaby: Set API Key"

---

## Documentation

| Document | Purpose |
|----------|---------|
| [USING-AGENTS.md](USING-AGENTS.md) | Quick start guide (5 min read) |
| [AGENTS-DEEP-DIVE.md](AGENTS-DEEP-DIVE.md) | Comprehensive documentation |
| [memory-contract-example.md](vs-code-agents/memory-contract-example.md) | Memory usage patterns |

---

## Typical Workflow

```
Roadmap → Planner → Analyst/Architect/Security/Critic → Implementer → QA → UAT → DevOps
```

1. **Roadmap** defines what to build and why
2. **Planner** creates a structured plan
3. **Analyst** researches unknowns
4. **Architect** ensures design fit
5. **Security** audits for vulnerabilities
6. **Critic** reviews plan quality
7. **Implementer** writes code
8. **QA** verifies tests
9. **UAT** confirms business value
10. **DevOps** releases (with user approval)

---

## Key Features

### 🎯 Separation of Concerns
Each agent has one job. Planner plans. Implementer implements. No scope creep.

### 📝 Document-Driven
Agents produce Markdown documents in `agent-output/`. Every decision is recorded.

### 🔒 Quality Gates
Critic reviews plans. Security audits code. QA verifies tests. Nothing ships without checks.

### 🧠 Long-Term Memory
With [Flowbaby](https://github.com/groupzer0/flowbaby), agents remember decisions across sessions.

### 🔄 Handoffs
Agents hand off to each other with context. No lost information between phases.

---

## Flowbaby Memory Integration

[Flowbaby](https://github.com/groupzer0/flowbaby) is a VS Code extension that provides **workspace-scoped long-term memory** for GitHub Copilot.

### Why Flowbaby?

Most AI memory solutions don't work well:

| Approach | Problem |
|----------|---------|
| Chat history | Lost between sessions |
| Vector DB alone | No structure, poor relationships |
| Manual notes | Inconsistent, requires effort |
| RAG on files | Noisy, retrieves irrelevant content |

**Flowbaby's approach**:
- **Hybrid Graph-Vector Search**: Combines knowledge graphs with vector similarity
- **Structured Summaries**: Stores decisions and reasoning, not raw logs
- **Workspace Isolation**: Each project has separate memory
- **Privacy-First**: All data stays local

### Key Features

- **Automatic memory search**: Flowbaby detects when context is needed
- **Automatic memory storage**: Stores key decisions and milestones
- **@flowbaby participant**: Query memory directly in chat
- **Agent tools**: `#flowbabyStoreSummary` and `#flowbabyRetrieveMemory`

### Links

- **GitHub**: https://github.com/groupzer0/flowbaby
- **VS Code Marketplace**: https://marketplace.visualstudio.com/items?itemName=flowbaby.flowbaby
- **Documentation**: See the GitHub README for full setup guide

---

## Repository Structure

```
agents/
├── README.md                    # This file
├── USING-AGENTS.md              # Quick start guide
├── AGENTS-DEEP-DIVE.md          # Comprehensive documentation
├── LICENSE                      # MIT License
└── vs-code-agents/              # Agent definitions
    ├── analyst.agent.md
    ├── architect.agent.md
    ├── critic.agent.md
    ├── devops.agent.md
    ├── implementer.agent.md
    ├── memory.agent.md
    ├── pi.agent.md              # ProcessImprovement
    ├── planner.agent.md
    ├── qa.agent.md
    ├── retrospective.agent.md
    ├── roadmap.agent.md
    ├── security.agent.md
    ├── uat.agent.md
    └── memory-contract-example.md
```

---

## Security Agent Highlight

The **Security Agent** has been enhanced to provide truly comprehensive security reviews:

### Five-Phase Framework
1. **Architectural Security**: Trust boundaries, STRIDE threat modeling, attack surface mapping
2. **Code Security**: OWASP Top 10, language-specific vulnerability patterns
3. **Dependency Security**: CVE scanning, supply chain risk assessment
4. **Infrastructure Security**: Headers, TLS, container security
5. **Compliance**: OWASP ASVS, NIST, industry standards

### Why This Matters

Most developers don't know how to conduct thorough security reviews. They miss:
- Architectural weaknesses (implicit trust, flat networks)
- Language-specific vulnerabilities (prototype pollution, pickle deserialization)
- Supply chain risks (abandoned packages, dependency confusion)
- Compliance gaps (missing security headers, weak TLS)

The Security Agent systematically checks all of these, producing actionable findings with severity ratings and remediation guidance.

See [security.agent.md](vs-code-agents/security.agent.md) for the full specification.

---

## Customization

### Modify Existing Agents

Edit `.agent.md` files to adjust:
- `description`: What shows in Copilot
- `tools`: Which VS Code tools the agent can use
- `handoffs`: Other agents it can hand off to
- Responsibilities and constraints

### Create New Agents

1. Create `your-agent.agent.md` following the existing format
2. Define purpose, responsibilities, constraints
3. Include the Memory Contract section
4. Add to `.github/agents/` in your workspace

---

## Contributing

Contributions welcome! Areas of interest:

- **Agent refinements**: Better constraints, clearer responsibilities
- **New agents**: For specialized workflows (e.g., Documentation, Performance)
- **Memory patterns**: Better retrieval/storage strategies
- **Documentation**: Examples, tutorials, troubleshooting

---

## Requirements

- VS Code with GitHub Copilot
- For memory: [Flowbaby extension](https://marketplace.visualstudio.com/items?itemName=flowbaby.flowbaby) + Python 3.10+

---

## License

MIT License - see [LICENSE](LICENSE)

---

## Related Resources

- [GitHub Copilot Agents Documentation](https://code.visualstudio.com/docs/copilot/copilot-agents)
- [Flowbaby Extension](https://github.com/groupzer0/flowbaby)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
