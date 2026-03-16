---
ID: 3
Origin: 1
UUID: 3c4d5e6f
Status: Active
Target Release: v0.1.1
handoff_id: "[[WF-P3]]"
---

# Plan 003: Planka Agile Execution Visibility Sync

**Value Statement and Business Objective**:
As a product owner, I want to see the status of AI-driven epics and tasks in a Kanban board, so that I can track progress transparently and bridge the gap between AI automation and traditional project management.

## 1. Objective
Establish an automated synchronization between the Markdown Roadmap (`product-roadmap.md`) and the Planka Kanban board. This ensuring that any status change in the roadmap is immediately reflected in the visual Planka board.

## 2. Assumptions
- Use native Planka MCP tools exclusively for all state changes.
- The `product-roadmap.md` is the Source of Truth for Status.
- Target release for this infrastructure patch is `v0.1.1`.

## 3. Plan

### Milestone 1: Synchronization Logic & Mapping
1. **Define Status-to-List Mapping**:
   - `Delivered` -> `Delivered` (ID: `1731195059669304399`)
   - `In Progress` -> `In Progress` (ID: `1731195093844493393`)
   - `EPIC APPROVED` -> `Planning / Ready for Dev` (ID: `1729877983956567893`)
2. **Strategy for Diff-based Sync**:
   - Implement logic to read `product-roadmap.md` and compare it against the current Planka cards.
   - For each Epic in roadmap:
     - If card missing: Create card and set initial list based on status.
     - If status changed: Move card to the corresponding list ID.
     - Update card description with current Acceptance Criteria from roadmap.

### Milestone 2: Planka Card Reconciliation & Task Automation
1. **Canonical Task List Sync**:
   - For each Epic card, ensure task lists match roadmap Acceptance Criteria (AC1, AC2, etc.).
   - Implement automatic renaming of legacy lists or removal of non-canonical lists.
2. **Obsidian-Planka Linking**:
   - Every sync operation must add a comment to the Planka card with the strategic node link `[[WF-E<epic-id>]]`.
   - Card descriptions must include a direct link to the Markdown roadmap artifact.

### Milestone 3: Validation & Version Management
1. **End-to-End Verification**:
   - Change an Epic status in `product-roadmap.md` from `EPIC APPROVED` to `In Progress`.
   - Verify Planka card moves to the correct list and a comment is appended.
2. **Version Update**:
   - Bump internal project version to `v0.1.1`.
   - Update `CHANGELOG.md` with "Planka visibility sync infrastructure".

## 4. Testing Strategy
- **Integration**: Verify `mcp_planka_move_card` correctly places cards in target lists based on status strings.
- **Verification**: Ensure no duplicate cards are created during sync.

## 5. Risks
- **ID Fragility**: Hardcoding List IDs (Mitigation: Use board metadata retrieval first to find list by name).
- **Concurrency**: Multiple syncs running simultaneously (Mitigation: Plan 003 ensures sequential execution).

## 6. Handoff Ready
Parent Node context for the next agent is [[WF-E1.3-planka-visibility]] (Planka Card: 1729878222469859173).
