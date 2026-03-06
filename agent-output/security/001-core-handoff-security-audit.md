---
ID: 1
Origin: 1
UUID: 7a82b9c1
Target Release: v0.1.0
Status: APPROVED_WITH_HARDENING
Epic: "Epic 1.1: Core Handoff Synchronization"
Planka: "http://localhost:25478/card/1724973066225714708"
Tags: [agent/security, verdict/approved-with-hardening, cvss/3.3]
---

# 1-Core-Handoff-Security-Audit

**Verdict**: `APPROVED_WITH_HARDENING`
**Status**: `OPEN` (Findings pending remediation)
**Baseline**: Linux/CachyOS (Bash)

---

## 1. Executive Summary
Security review of **Plan-1: Core Handoff Lifecycle Verification**. The plan involves modifying a Python helper script (`planka_ops.py`) that interacts with an external MCP server (Planka). The primary risks are **Injection (A03:2021)** via unvalidated string parsing and **Insecure Design (A04:2021)** related to trust boundaries between the script and the MCP client.

## 2. Risk Assessment (STRIDE)

| Threat | Risk | Mitigation |
|--------|------|------------|
| **Tampering** | Insecure type-casting could be used to bypass logic if `position` or `isCompleted` are manipulated. | **Hardening**: Context-aware parsing with strict type-mapping for known keys. |
| **Information Disclosure** | Verbose `stderr` capture (requested by Architect) could leak sensitive MCP environment variables or tokens. | **Hardening**: Sanitize captured logs; exclude `Authorization` or `Token` headers from raw error dumps. |
| **Injection** | The `parse_value` function's JSON parsing (`json.loads`) could be vulnerable if malicious JSON payloads are passed via CLI. | **Hardening**: Limit recursion depth; perform basic structural validation before `json.loads`. |

## 3. Findings & Hardening Recommendations

### [SEC-001] Insecure String Parsing (Medium)
**Location**: `.github/skills/planka-workflow/scripts/planka_ops.py:parse_value`
**Vulnerability**: The current `parse_value` uses a generic `isdigit()` check. While the Architect's fix (ID exclusion list) solves the functional bug, it does not address the lack of input validation.
**Hardening**:
- Implement a **Positive Allowlist** for numeric fields (e.g., `position`, `total`, `isDueDateCompleted`).
- Any field NOT in the allowlist and NOT in the ID exclusion list should default to `string` to prevent accidental type-sniffing.

### [SEC-002] Error Log Sanitization (Low)
**Location**: `agent-output/analysis/002-planka-ops-fix-analysis.md` (Implementation requirement)
**Requirement**: The Architect requested capturing raw `stderr`.
**Hardening**:
- The **Implementer** MUST ensure that the capture logic filters out sensitive strings (e.g., `PLANKA_TOKEN`, `ACCESS_KEY`) using a simple regex replacement before writing to the analysis artifact.

### [SEC-003] Defensive CLI Execution (Low)
**Location**: `mcp_client.py` and tool invocation in `planka_ops.py`
**Hardening**: Ensure all data passed to the `MCPClient` is serialized cleanly. Avoid `shell=True` if the client uses subshells for any reason (checked: `mcp_client.py` currently uses direct imports, which is secure).

---

## 4. Compliance Mapping (OWASP ASVS)
- **V5.1.3**: Verify that all input is validated against a positive allowlist (Hardening SEC-001).
- **V7.4.3**: Verify that logs do not contain sensitive data (Hardening SEC-002).

## 5. Implementation Constraints for Implementer (07)
1. **Sanitize stderr**: Use `sed` or Python to remove tokens from logs before outputting to `agent-output/`.
2. **Strict Field Types**: Create a `TYPE_MAP` dictionary for properties that are NOT IDs (e.g., `{'position': int, 'isCompleted': bool}`).

---

**Verdict**: `APPROVED_WITH_HARDENING`
Next Agent: [[WF-1]] context applies.
Reference: [001-core-handoff-architecture-findings.md](../../architecture/001-core-handoff-architecture-findings.md)
