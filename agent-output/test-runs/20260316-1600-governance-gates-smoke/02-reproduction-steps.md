# Reproduction Steps

1. Run baseline:
   - `sh .github/scripts/check_strict_governance.sh`
   - `sh .github/scripts/scaffold_required_files.sh`
   - `sh .github/scripts/check_workflow_contract.sh --changed-only`
   - `npx -y markdownlint-cli2 "**/*.md" --config .markdownlint.json`
2. Inject strict failure:
   - change heading `## Workflow Memory Rules (Mandatory)` to `## Workflow Memory Rules (Temporary Test)` in `.github/agents/13-pi.agent.md`.
3. Run strict check and verify failure.
4. Restore heading to original.
5. Inject workflow failure:
   - add summary line containing `[[WF-[ID]]]` to `agent-output/workflows/WF-IMPL-001.md`.
6. Run workflow contract check (`--changed-only`) and verify failure.
7. Restore workflow note to original content.
8. Re-run full baseline command set and verify all green.
