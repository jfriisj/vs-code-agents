# Reproduction Steps

1. Run baseline stack:
   - `sh .github/scripts/check_skill_gate_coverage.sh`
   - `sh .github/scripts/check_strict_governance.sh`
   - `sh .github/scripts/scaffold_required_files.sh`
   - `sh .github/scripts/check_workflow_contract.sh --changed-only`
   - `npx -y markdownlint-cli2 ".github/**/*.md" "agent-output/test-runs/**/*.md" --config .markdownlint.json`
2. Inject failure in `.github/agents/13-pi.agent.md`:
   - replace `analysis-methodology` token in the Investigation Methodology line.
3. Run `sh .github/scripts/check_skill_gate_coverage.sh` and verify failure.
4. Restore original PI line containing `analysis-methodology`.
5. Re-run full baseline stack and verify all checks pass.
