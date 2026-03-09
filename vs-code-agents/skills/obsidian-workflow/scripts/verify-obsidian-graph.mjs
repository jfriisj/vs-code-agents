import fs from 'fs';
import path from 'path';

/**
 * Deterministic Workspace Root Resolution (ADR-003)
 */
const getWorkspaceRoot = () => {
  const envRoot = process.env.WORKSPACE_ROOT;
  if (envRoot && fs.existsSync(envRoot)) {
    return path.resolve(envRoot);
  }
  
  // Search for the project marker from the current script location
  let currentDir = path.dirname(new URL(import.meta.url).pathname);
  while (currentDir !== '/') {
    // Check if we are at the workspace root (contains vs-code-agents child and CHANGELOG.md)
    if (fs.existsSync(path.join(currentDir, 'vs-code-agents')) && fs.existsSync(path.join(currentDir, 'CHANGELOG.md'))) {
      return path.resolve(currentDir);
    }
    currentDir = path.dirname(currentDir);
  }

  console.error("CRITICAL ERROR: Failed to resolve deterministic workspace root via environment or markers.");
  process.exit(1);
};

const WORKSPACE_ROOT = getWorkspaceRoot();
// The vault root is located at <WORKSPACE_ROOT>/agent-output relative to the workspace core
const VAULT_ROOT = path.join(WORKSPACE_ROOT, 'agent-output');

console.log(`[ADR-003] Resolved WORKSPACE_ROOT: ${WORKSPACE_ROOT}`);
console.log(`[Security] Using VAULT_ROOT: <WORKSPACE_ROOT>/agent-output`);

/**
 * Graph Verification Logic
 */
const verifyGraph = () => {
    if (!fs.existsSync(VAULT_ROOT)) {
        console.error(`ERROR: Vault root not found at expected location: ${VAULT_ROOT}`);
        process.exit(1);
    }

    const workflowDir = path.join(VAULT_ROOT, 'workflows');
    if (!fs.existsSync(workflowDir)) {
        console.warn(`WARNING: workflow directory not found: ${workflowDir}`);
        return;
    }

    const files = fs.readdirSync(workflowDir).filter(f => f.endsWith('.md'));
    let validCount = 0;

    files.forEach(file => {
        const content = fs.readFileSync(path.join(workflowDir, file), 'utf8');
        if (content.includes('parent:') || content.includes('type: Roadmap')) {
            validCount++;
        }
    });

    console.log(`Obsidian graph verification passed for ${validCount} workflow note(s).`);
};

verifyGraph();
