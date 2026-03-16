# Reproduction Steps

1. Run baseline stack:
   - `sh .github/scripts/check_skill_gate_coverage.sh`
   - `sh .github/scripts/check_obsidian_graph_contract.sh`
   - `sh .github/scripts/check_strict_governance.sh`
   - `sh .github/scripts/scaffold_required_files.sh`
   - `sh .github/scripts/check_workflow_contract.sh --changed-only`
   - `npx -y markdownlint-cli2 ".github/**/*.md" "agent-output/test-runs/**/*.md" --config .markdownlint.json`
2. Inject Skill failure:
   - remove token `analysis-methodology` from `.github/agents/12-retrospective.agent.md`.
3. Run `sh .github/scripts/check_skill_gate_coverage.sh` and confirm failure.
4. Restore `.github/agents/12-retrospective.agent.md`.
5. Inject Obsidian graph failure:
   - rename heading `# Obsidian Graph Memory` in `.github/agents/09-qa.agent.md`.
6. Run `sh .github/scripts/check_obsidian_graph_contract.sh` and confirm failure.
7. Restore `.github/agents/09-qa.agent.md` heading.
8. Re-run baseline stack and confirm all green.
