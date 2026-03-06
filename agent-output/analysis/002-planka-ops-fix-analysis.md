---
ID: 2
Type: Analysis
Status: Active
Epic: "[[Epic 1.1: Core Handoff Synchronization]]"
Planka: "http://localhost:25478/card/1724973066225714708"
Tags: [agent/analyst, status/active]
---

# Analysis-2: Planka Ops Python Script Type-Casting Bug

**Value Statement and Business Objective**:
As a developer, I want the Planka helper script to correctly pass numeric IDs as strings to the MCP server, so that operations do not fail due to type mismatches.

**Objective**:
Diagnose and propose a fix for the unwanted integer-casting of ID-like strings in `planka_ops.py`.

---

## Methodology
1.  **Code Review**: Inspected `.github/skills/planka-workflow/scripts/planka_ops.py:parse_value`.
2.  **Reproduction**: Verified that strings like `"1724973066225714708"` and `"001"` are automatically cast to `int`.
3.  **Impact Mapping**: Identified all string-based ID fields in the script that are vulnerable to this casting.

## Findings

### Verified (Root Cause)
The `parse_value` function uses `raw.isdigit()` to determine if a value should be cast to an integer. 

```python
# .github/skills/planka-workflow/scripts/planka_ops.py:108
try:
    if raw.isdigit() or (raw.startswith("-") and raw[1:].isdigit()):
        return int(raw)
    return float(raw)
except ValueError:
    return raw
```

Because this function is used for all key-value arguments (`key=value`), it cannot differentiate between numeric properties (like `position`) and high-entropy numeric IDs (like `cardId`).

### Inference
- **Planka MCP Requirement**: The Planka server expects IDs (e.g., `cardId`, `listId`) to be **strings**.
- **JSON-RPC mismatch**: Passing an integer where the schema expects a string causes `MCP error -32602`.

### System Weaknesses (Architecture/Code)
- **Generic Parsing**: `parse_value` lacks context of the key it is parsing for.
- **Over-eager Type Inference**: `isdigit()` is too aggressive for a system that uses strictly numeric strings as primary keys.

---

## Analysis Recommendations

1.  **Context-Aware Parsing**: Update `parse_key_value_args` to pass the key name to `parse_value`.
2.  **Exclusion List**: Define a list of "ID fields" (e.g., matching `*Id`) that should ALWAYS remain strings.
3.  **Regression Test**: Create `.github/skills/planka-workflow/scripts/test_planka_ops.py` to verify:
    - `cardId="123"` -> `"123"` (string)
    - `position="123"` -> `123` (int)
    - `isCompleted="true"` -> `True` (bool)

## Next Steps
- Implementer to modify `parse_key_value_args` and `parse_value` signature.
- Implementer to create unit tests as specified.

## Open Questions
- Are there any numeric fields other than `position` that *require* integer casting? (Confirmed `total` in stopwatch, but that is handled via dict merging usually).

