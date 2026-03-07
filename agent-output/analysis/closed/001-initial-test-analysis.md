---
ID: 001
Type: Analysis
Status: Resolved
Epic: "[[Epic 1.1: Core Handoff Synchronization]]"
Planka: "http://localhost:25478/card/1724973066225714708"
Origin: analyst-agent
UUID: 6ac75d37-1b4e-40e0-923b-77b39f72ecfe
---

# Analysis-001: Script Argument Parsing Limitation

**Value Statement**:
Investigate the reported argument parsing issue in the Planka synchronization script to ensure robust communication between agents and the Agile board.

**Business Objective**:
Uncover why card IDs are being misparsed as numbers instead of strings during script execution.

**Findings**:
1. The script `.github/skills/planka-workflow/scripts/planka_ops.py` uses a custom `parse_value` function.
2. `parse_value` uses `isdigit()` to decide if a string should be converted to an `int`.
3. Planka IDs are long numeric strings which exceed standard integer limits or trigger numeric validation in the MCP server even if Python handles them as large integers.
4. MCP Server (`mcp-server-planka`) explicitly requires `cardId` to be a `string`.

**Root Cause**:
The custom parser in the Python helper script is "too smart" and converts the Planka ID string into an integer before passing it to the MCP client, causing an MCP schema validation error.

**Recommendation**:
- Update `planka_ops.py` to preserve ID-like strings as strings.
- Or, use direct MCP tool calls when using automated agents as they handle the schema correctly.

**Next Investigative Steps**:
- Verify if other ID fields (projectId, boardId) suffer the same conversion issue.
