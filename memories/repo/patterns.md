# Repostitory Implementation Patterns (v0.1.0+)

The following patterns have been established via the v0.1.0 release lifecycle to ensure consistent agent operations.

## 1. Context-Aware Data Parsing (PI-001-CODE)
- **Problem**: Naive `isdigit()` type-sniffing incorrectly casts numeric string IDs (e.g., Planka IDs) to integers, breaking downstream tool compatibility.
- **Pattern**: Parsers MUST receive the `key` name and check against an ID exclusion list (`*Id`) before type-sniffing.
- **Example**:
```python
def parse_value(key, value):
    if key.endswith("Id"):
        return str(value)  # IDs are always strings
    if value.isdigit():
        return int(value)
    ...
```

## 2. Automated Log Sanitization (SEC-002)
- **Problem**: Tool output (stdout/stderr) from agent helper scripts may contain sensitive environment variables (e.g., `PLANKA_TOKEN`).
- **Pattern**: Every automated agent helper script MUST implement a redaction pass for sensitive strings before output.
- **Example**:
```python
def redact_secrets(text):
    secrets = [os.getenv("PLANKA_TOKEN")]
    for secret in secrets:
        if secret:
            text = text.replace(secret, "[REDACTED]")
    return text
```

## 3. Mandatory DevOps Force-Staging (PI-001-GIT)
- **Problem**: `agent-output/` and `.github/` are often ignored by `.gitignore`, causing staging failures during releases.
- **Pattern**: The **11-DevOps** agent (and any agent committing to these paths) MUST use `git add -f` to ensure artifact trackability.

## 4. Absolute Addressing for Skills (PI-001-PATH)
- **Problem**: Shifts in working directory (`cwd`) across agent handoffs lead to script location failures.
- **Pattern**: Use absolute pathing for all helper script tool calls initiated by agents.

## 5. Dual Agent Instruction Roots (PI-001-AGENT-ROOTS)
- **Problem**: Agent instruction files exist in both `.github/agents/` and `vs-code-agents/agents/`; patching only one root causes policy drift.
- **Pattern**: When enforcing global agent policy (gates, handoff contracts, lifecycle rules), update and validate both roots unless one is explicitly deprecated.
