# 004-remediation-phase1-delta

```yaml
ID: 004
Origin: 003
UUID: 3f9e8a71
Status: Active
Date: 2026-03-16
Scope: Phase 1 remediation delta (Planka + Obsidian)
```

## Applied Remediations
1. Added missing canonical lifecycle lists on Planka board `Epics` (`1729877970501240657`):
   - `Planned`
   - `Deferred`
   - `Closed`
2. Applied list-level quarantine for non-canonical legacy columns (all empty) by renaming and moving them to far-right positions:
  - `LEGACY - Planned (Do Not Use)`
  - `LEGACY - Implementation In Progress`
  - `LEGACY - Implementation Done A`
  - `LEGACY - Implementation Done B`
  - `LEGACY - Implementation Done C`
  - `LEGACY - QA Pending`
  - `LEGACY - UAT Released`
3. Reordered canonical lifecycle lanes to deterministic operational order:
  - `Planned` (1)
  - `In Progress` (2)
  - `Delivered` (3)
  - `Deferred` (4)
  - `Closed` (5)
4. Updated Epic card governance metadata:
   - Epic 1.1 description now includes `**Obsidian Root Node**: [[WF-E1.1]]`
   - Epic 1.3 description now includes `**Obsidian Root Node**: [[WF-E1.3]]`
5. Corrected Epic 1.2 label set:
   - Added `Priority P1`
   - Removed redundant `Release v0.1.0` (kept `Release v0.1.1`)
6. Added explicit Delivered-deferment governance markers on both Delivered epics with open checklist work:
  - Epic 1.1 comment marker: `DELIVERED-DEFERRED-RATIONALE-2026-03-16`
  - Epic 1.2 comment marker: `DELIVERED-DEFERRED-RATIONALE-2026-03-16`
7. Repaired missing WF targets by creating deterministic compatibility nodes:
   - `WF-IMPL-001.md`
   - `WF-P001.md`
   - `WF-QA-2-persistent-memory-obsidian.md`
   - `WF-P-002.md`
   - `WF-CR-2.md`
   - `WF-001.md`
   - `WF-1.md`
   - `WF-2.md`
   - `WF-1.2.md`
   - `WF-1.3.md`
   - `WF-AR-003.md`

## Validation Results
- Board lane governance:
  - Canonical lanes present and active: `Planned`, `In Progress`, `Delivered`, `Deferred`, `Closed`.
  - Canonical lane order is deterministic: `Planned`, `In Progress`, `Delivered`, `Deferred`, `Closed`.
  - Non-canonical active lanes with cards: `0`.
  - Legacy lanes quarantined: `7` (all `cards=0`, positions `90-96`).
- Delivered deferment controls:
  - Epic 1.1 has explicit deferment-rationale control marker comment.
  - Epic 1.2 has explicit deferment-rationale control marker comment.
- Workflow internal link integrity:
  - Before: `8` files with missing targets.
  - After: `0` files with missing targets.
- Persisted Planka comment WF-reference check (36 comments across Epic 1.1 + 1.2):
  - Before: broken targets present.
  - After: `0` comments with missing WF targets.
- New workflow note lint check:
  - `11`/`11` files lint-clean (`0` markdown errors).
- Epic label governance:
  - Epic 1.1: release + priority present.
  - Epic 1.2: release + priority present.
  - Epic 1.3: release + priority present.
- Epic root-node traceability:
  - Epic 1.1, 1.2, 1.3 now all include explicit `Obsidian Root Node` in description.

## Remaining Gaps
1. Board still contains `7` legacy active lists (now clearly quarantined and empty).
2. Exact lifecycle-only board state is blocked by missing `delete_list` tool exposure in this runtime schema (only `update_list` is available).

## Next Enforcement Step
- Execute final list deletion once `delete_list` is exposed to this session:
  - `Planned`, `In Progress`, `Delivered`, `Deferred`, `Closed`
