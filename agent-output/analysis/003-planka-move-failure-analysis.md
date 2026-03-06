---
ID: 3
Type: Analysis
Status: Active
Epic: "[[Epic 1.1: Core Handoff Synchronization]]"
Planka: "http://localhost:25478/card/1724973066225714708"
Tags: [agent/analyst, status/active]
---

# Analysis-3: Planka Card Move Failure Investigation

**Value Statement and Business Objective**:
As a developer, I want to understand why cards are not moving between lists in Planka, so that the automated lifecycle transitions can be completed successfully.

**Objective**:
Diagnose the root cause of "move_card" operation failures in `planka_ops.py`.

---

## Methodology
1.  **Code Inspection**: Examined `.github/skills/planka-workflow/scripts/planka_ops.py` for `card:move` operation mapping.
2.  **Runtime Trace**: Attempted to list boards to find destination list IDs.
3.  **Error Reproduction**: Triggered `MCP error -32602` by running the script with numeric IDs.

## Findings

### Verified (Root Cause)
The failure to move cards is the same underlying issue as Analysis-2: **Type Mismatch**.
1.  The `card:move` operation requires both `cardId` and `listId`.
2.  The script's `parse_value` function casts these numeric strings (e.g., `1724973066225714708`) into Python `int`.
3.  The Planka MCP server strictly requires IDs as `string`.
4.  **Result**: Every attempt to move a card via the current script fails before reaching the server because the arguments fail schema validation.

### System Weaknesses
- **Failure to Fail Loudly**: When the script encounters an MCP validation error, it may not be providing clear enough feedback to the calling agent about *why* the move didn't happen, leading to "ghost" failures where the card simply stays put.
- **Dependency on Broken Infrastructure**: The Implementer is trying to move cards using a tool that is fundamentally broken for numeric IDs.

---

## Analysis Recommendations

1.  **Block Move Operations**: Do not attempt to move cards using `planka_ops.py` until the fix for **Analysis-2** (Plan-1, Milestone 3) is implemented.
2.  **Immediate Workaround**: Use direct MCP tool calls (`mcp_planka_move_card`) to complete lifecycle transitions for Plan-1.
3.  **Sanitization Check**: Ensure that when `move_card` is called via MCP, the `listId` is retrieved accurately from the board state, as an invalid destination `listId` will also cause a silent failure or 404 in the MCP server.

## Next Steps
- Implementer MUST prioritize the patch to `parse_value` (Plan-1) as it is the "double blocker" for both comments and card movements.

