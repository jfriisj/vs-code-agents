---
name: architecture-patterns
description: Common software architecture patterns, ADR templates, and anti-pattern detection. Integrates with Obsidian for architectural memory graphs and Planka for design constraints tracking.
license: MIT
metadata:
  author: groupzer0
  version: "1.1"
---

# Architecture Patterns

Reference for architectural design and documentation. Use this skill when:
- Architect reviews system design
- Planner considers architectural constraints
- Analyst investigates integration approaches
- Critic evaluates architectural alignment

## The Triad of Truth (Architecture)

Every architectural decision must be reflected across three systems:
1. **Markdown (`agent-output/architecture/`)**: The detailed ADRs, master architecture doc, and findings.
2. **Obsidian Graph (`workflows/`)**: The `WF-` nodes linking architecture decisions to specific Epics and Plans.
3. **Planka Board**: The "Architecture & Design" Task List on the relevant Epic card to enforce implementation constraints.

---

## Architecture Decision Records (ADR)

### ADR Format

Every significant architectural decision should be documented. All ADRs and Findings documents MUST include this standard YAML frontmatter for Obsidian indexing:

```markdown
---
ID: [NNN]
Type: Architecture
Status: [Proposed | Accepted | Deprecated]
Epic: "[[WF-Epic-ID]]"
Planka-Card: "[cardId]"
---
# ADR-[NNN]: [Decision Title]

## Context
[What is the situation? What forces are at play?]

## Decision
[What is the change being proposed or decided?]

## Consequences
### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Tradeoff 1]
- [Tradeoff 2]

### Neutral
- [Side effect]

## Alternatives Considered
1. [Alternative 1]: [Why rejected]
2. [Alternative 2]: [Why rejected]

## Related
- ADR-XXX: [Related decision]
- [External reference]
```

### When to Write ADRs

| Scenario | ADR Required? |
| --- | --- |
| New external dependency | Yes |
| New architectural pattern | Yes |
| Technology switch | Yes |
| Module boundary change | Yes |
| Performance tradeoff | Yes |
| Bug fix | No |
| Refactoring (same behavior) | Usually no |

---

## Common Patterns

### Layered Architecture

```
┌─────────────────────────────────┐
│         Presentation            │  UI, API endpoints
├─────────────────────────────────┤
│          Application            │  Use cases, orchestration
├─────────────────────────────────┤
│           Domain                │  Business logic, entities
├─────────────────────────────────┤
│        Infrastructure           │  DB, external services
└─────────────────────────────────┘
```

**Rules:**

* Dependencies point downward only
* Lower layers never import from higher
* Domain has no external dependencies

**Use when:** Enterprise apps, clear separation needed

### Repository Pattern

**Purpose:** Abstract data access, enable testability

```typescript
// Interface in domain layer
interface UserRepository {
  findById(id: string): Promise<User | null>;
  save(user: User): Promise<void>;
}

// Implementation in infrastructure layer
class PostgresUserRepository implements UserRepository {
  async findById(id: string): Promise<User | null> {
    const row = await db.query('SELECT * FROM users WHERE id = $1', [id]);
    return row ? mapToUser(row) : null;
  }
}
```

**Use when:** - Need to swap data stores

* Testing without real database
* Multiple data sources

### Service Layer

**Purpose:** Encapsulate business operations

```typescript
class OrderService {
  constructor(
    private orderRepo: OrderRepository,
    private paymentGateway: PaymentGateway,
    private notifier: Notifier
  ) {}

  async placeOrder(cart: Cart, payment: PaymentInfo): Promise<Order> {
    const order = Order.fromCart(cart);
    await this.paymentGateway.charge(payment, order.total);
    await this.orderRepo.save(order);
    await this.notifier.sendConfirmation(order);
    return order;
  }
}
```

**Use when:**

* Multiple steps in operation
* Transaction coordination
* Cross-cutting concerns

### Event-Driven Architecture

```
┌─────────┐    Event    ┌─────────┐
│ Service │───────────► │  Queue  │
│    A    │             │         │
└─────────┘             └────┬────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
         ┌─────────┐   ┌─────────┐   ┌─────────┐
         │ Handler │   │ Handler │   │ Handler │
         │    1    │   │    2    │   │    3    │
         └─────────┘   └─────────┘   └─────────┘
```

**Use when:**

* Loose coupling between components
* Asynchronous processing
* Multiple consumers of same event
* Audit trail needed

### Dependency Injection

**Purpose:** Invert control, enable testing

```typescript
// Without DI (hard to test)
class OrderService {
  private db = new PostgresDatabase();
}

// With DI (testable)
class OrderService {
  constructor(private db: Database) {}
}

// Production
new OrderService(new PostgresDatabase());

// Test
new OrderService(new MockDatabase());
```

---

## Anti-Patterns to Detect

| Anti-Pattern | Detection | Fix |
| --- | --- | --- |
| **God Object** | Class with 20+ methods, 500+ lines | Extract classes |
| **Circular Dependencies** | A→B→C→A | Introduce interface |
| **Big Ball of Mud** | No clear structure | Define boundaries |
| **Spaghetti Code** | Tangled control flow | Refactor, add layers |
| **Golden Hammer** | Same pattern everywhere | Choose appropriate |
| **Anemic Domain** | Data classes + procedure classes | Move logic to domain |
| **Leaky Abstraction** | Implementation details exposed | Hide behind interface |
| **Premature Optimization** | Complex code for speed | Measure first |

### Detection Commands

```bash
# Find large files (potential God objects)
find . -name "*.ts" -exec wc -l {} \; | sort -rn | head -10

# Find circular dependencies (TypeScript)
npx madge --circular src/

# Find files with many imports
grep -c "^import" src/**/*.ts | sort -t: -k2 -rn | head -10
```

---

## System Architecture Documentation

### Required Sections

For `system-architecture.md` (Must also contain Dataview YAML header):

1. **Purpose**: What does this system do?
2. **High-Level Architecture**: Diagram, major components
3. **Components**: Each component's responsibility
4. **Data Flow**: How data moves through system
5. **Dependencies**: External services, libraries
6. **Quality Attributes**: Performance, security, scalability goals
7. **Decisions**: ADRs or decision log
8. **Known Issues**: Technical debt, problem areas

### Diagram Standards

Use Mermaid for version-controlled diagrams. See `references/diagram-templates.md` for full templates.

---

## Reconciliation Changelog Template

When the Architect reconciles architecture docs after implementations, use this format in the `system-architecture.md` changelog:

```markdown
| Date | Change | Rationale | Source |
|------|--------|-----------|--------|
| 2024-12-20 | Added memory retrieval caching layer | Reconciled from Plan-015 implementation | Plan-015-memory-caching |
| 2024-12-18 | Updated API boundary diagram | Implementation added new endpoint | Post-implementation audit |

```

---

## Design Debt Registry Template

Track architectural improvements in the **Problem Areas** section of `system-architecture.md`:

```markdown
## Problem Areas / Design Debt Registry

### Active Design Debt

| ID | Area | Current State | Optimal State | Priority | Discovered | Last Reviewed |
|----|------|---------------|---------------|----------|------------|---------------|
| DD-001 | Memory Subsystem | Direct Cognee calls scattered | Unified memory service facade | Medium | 2024-12-15 | 2024-12-20 |

```

---

## Agent Responsibilities & The Triad Handoff

### 04-Architect (Execution & Handoff)

Before handing off, the Architect MUST align the triad:

1. **The Artifact (`agent-output/`)**: Document ADRs and update `system-architecture.md`.
2. **The Execution (Planka Board)**:
* Ensure an "Architecture & Design" Task List exists on the Epic card.
* Add Tasks for specific constraints the Implementer must follow.
* Leave a comment with the final verdict (`APPROVED`, `APPROVED_WITH_CHANGES`, `REJECTED`) and link to the findings document.


3. **The Memory (Obsidian Graph)**:
* Create/Update `workflows/WF-[ID]-[slug].md`.
* Set `type: Architecture` and `parent: "[[WF-[Calling-ID]]]"`.
* Summarize the architectural invariant/constraint in max 3 bullets.
* Patch the calling agent's node to link back to the Architect node.



### Analyst Agent

* Reference architecture when investigating integration points.
* Consult Architect for systemic pattern questions.
* Link findings nodes to architecture nodes in Obsidian if proposing new dependencies.

### Planner Agent

* Read the active `WF-Architecture` notes and `system-architecture.md` before planning.
* Ensure plans respect documented patterns.

### Critic Agent

* Reference `system-architecture.md` during plan review.
* Verify architectural alignment.
* Flag plans that violate documented decisions.
