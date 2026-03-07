# Obsidian Workflow Feature Coverage Matrix

This matrix defines the low-token operational contract for Obsidian workflow usage.

| Workflow Feature | MCP Surface | Required Usage | Token Guardrail |
|---|---|---|---|
| Workflow discovery | `search_notes` | Query by `WF-[ID]` or exact note path only (`limit` ≤ 3) | Max 1 search |
| Context retrieval | `read_note` / `read_multiple_notes` | Read index + active workflow note only | Max 2 reads |
| Decision updates | `patch_note` | Patch `Decisions` section only via exact replace | 1 write |
| Artifact sync | `patch_note` | Patch `Artifacts` section with relative paths | 1 write |
| Ownership transition | `update_frontmatter` | Update `owner`, `status`, `last_updated` with merge | Included in write budget |
| Handoff logging | `write_note` | Append timestamped block under `Handoffs` (`mode: append`) | Included in write budget |
| Next-step routing | `patch_note` | Update `Next` with exact next owner + gate | Included in write budget |

## Deprecated Patterns (Do Not Use)

- Broad vault search without workflow ID.
- Rewriting whole notes for small heading changes.
- Copying large text from `agent-output/` into Obsidian.
- Multiple status updates in comments instead of one structured handoff block.

## Validation Rule

Before claiming sync complete, verify:
1. The workflow note has current `owner`, `status`, and `last_updated`.
2. The latest handoff block includes status, decisions/result, and next owner.
3. Artifact links point to `agent-output/` paths, not duplicated note content.
4. The turn stayed within budget (or includes escalation reason).
