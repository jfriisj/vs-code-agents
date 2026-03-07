import { readdir, readFile } from "node:fs/promises";
import path from "node:path";

function parseArgs(argv) {
  const parsed = {};

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (!arg.startsWith("--")) {
      continue;
    }

    const normalized = arg.slice(2);
    if (normalized.includes("=")) {
      const [key, value] = normalized.split(/=(.*)/s);
      parsed[key] = value;
      continue;
    }

    const next = argv[index + 1];
    if (next && !next.startsWith("--")) {
      parsed[normalized] = next;
      index += 1;
    } else {
      parsed[normalized] = "true";
    }
  }

  return parsed;
}

function escapeRegex(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function normalizeLinkTarget(rawTarget) {
  let target = rawTarget.split("|")[0]?.trim() ?? "";
  target = target.split("#")[0]?.trim() ?? "";
  target = target.replace(/^\.\//, "");

  if (target.includes("/")) {
    const parts = target.split("/");
    target = parts[parts.length - 1] ?? target;
  }

  return target.trim();
}

function extractWikiLinkTargets(content) {
  return [...content.matchAll(/\[\[([^\]]+)\]\]/g)]
    .map((match) => normalizeLinkTarget(match[1] ?? ""))
    .filter(Boolean);
}

function extractIndexWorkflowTargets(indexContent) {
  return [...indexContent.matchAll(/\[\[workflows\/([^\]|#]+)(?:\|[^\]]+)?\]\]/g)]
    .map((match) => normalizeLinkTarget(match[1] ?? ""))
    .filter(Boolean);
}

function parseFrontmatterObject(frontmatterRaw) {
  const parsed = {};
  const lines = frontmatterRaw.split(/\r?\n/);

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.length === 0 || trimmed.startsWith("#")) {
      continue;
    }

    const match = line.match(/^([A-Za-z0-9_-]+)\s*:\s*(.*)$/);
    if (!match) {
      return {
        error: `frontmatter line is not key:value -> ${line}`,
        value: null
      };
    }

    const key = match[1];
    let value = (match[2] ?? "").trim();

    if (
      (value.startsWith("\"") && value.endsWith("\"")) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }

    parsed[key] = value;
  }

  return { error: null, value: parsed };
}

function parseFrontmatterAndBody(content) {
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);

  if (!frontmatterMatch) {
    return {
      frontmatter: null,
      body: content,
      parseError: "missing frontmatter block"
    };
  }

  const [, frontmatterRaw, body] = frontmatterMatch;
  const { error, value } = parseFrontmatterObject(frontmatterRaw);

  if (error) {
    return {
      frontmatter: null,
      body,
      parseError: error
    };
  }

  return {
    frontmatter: value,
    body,
    parseError: null
  };
}

async function collectMarkdownBasenames(rootDir) {
  const basenames = new Set();

  async function walk(currentDir) {
    const entries = await readdir(currentDir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);
      if (entry.isDirectory()) {
        await walk(fullPath);
        continue;
      }

      if (!entry.isFile() || !entry.name.toLowerCase().endsWith(".md")) {
        continue;
      }

      basenames.add(entry.name.replace(/\.md$/i, ""));
    }
  }

  await walk(rootDir);
  return basenames;
}

function validateWorkflowNote({
  fileName,
  content,
  workflowIndex,
  markdownBasenames,
  requiredFrontmatterFields,
  requiredHeadings,
  placeholderPatterns
}) {
  const failures = [];
  const notePath = path.posix.join("agent-output", "workflows", fileName);
  const noteBaseName = fileName.replace(/\.md$/i, "");

  const { frontmatter, body, parseError } = parseFrontmatterAndBody(content);

  if (parseError) {
    failures.push(`${notePath}: ${parseError}`);
    return failures;
  }

  for (const field of requiredFrontmatterFields) {
    const value = frontmatter[field];

    if (typeof value !== "string" || value.trim().length === 0) {
      failures.push(`${notePath}: missing required frontmatter field \`${field}\``);
    }
  }

  const workflowId = frontmatter.workflow_id ?? "";
  if (typeof workflowId === "string") {
    if (!/^WF-[A-Za-z0-9][A-Za-z0-9.-]*$/.test(workflowId)) {
      failures.push(`${notePath}: \`workflow_id\` must start with WF- and use [A-Za-z0-9.-]`);
    }

    if (!(fileName === `${workflowId}.md` || fileName.startsWith(`${workflowId}-`))) {
      failures.push(`${notePath}: file name must start with workflow_id \`${workflowId}\``);
    }
  }

  const parentValue = frontmatter.parent ?? "";
  let parentTarget = "";
  if (parentValue !== "none") {
    const parentTargets = extractWikiLinkTargets(parentValue);
    parentTarget = parentTargets[0] ?? "";

    if (!/^\[\[[^\]]+\]\]$/.test(parentValue) || parentTargets.length !== 1) {
      failures.push(`${notePath}: \`parent\` must be \`none\` or a single wikilink`);
    } else if (!markdownBasenames.has(parentTarget)) {
      failures.push(`${notePath}: parent wikilink target does not resolve -> [[${parentTarget}]]`);
    }
  }

  if (typeof frontmatter.last_updated === "string" && !/^\d{4}-\d{2}-\d{2}$/.test(frontmatter.last_updated)) {
    failures.push(`${notePath}: \`last_updated\` must use YYYY-MM-DD format`);
  }

  for (const heading of requiredHeadings) {
    const headingPattern = new RegExp(`^##\\s+${escapeRegex(heading)}\\s*$`, "m");
    if (!headingPattern.test(body)) {
      failures.push(`${notePath}: missing required heading \`## ${heading}\``);
    }
  }

  for (const pattern of placeholderPatterns) {
    if (pattern.test(content)) {
      failures.push(`${notePath}: contains placeholder-like WF identifier (${pattern})`);
    }
  }

  const bodyLinks = extractWikiLinkTargets(body);
  const selfTargets = new Set([noteBaseName]);

  for (const target of bodyLinks) {
    if (selfTargets.has(target)) {
      continue;
    }

    if (!markdownBasenames.has(target)) {
      failures.push(`${notePath}: unresolved wikilink target [[${target}]]`);
    }
  }

  const indexPattern = new RegExp(
    `\\[\\[workflows/${escapeRegex(noteBaseName)}(?:\\|[^\\]]+)?\\]\\]`,
    "m"
  );
  if (!indexPattern.test(workflowIndex)) {
    failures.push(`${notePath}: missing index link in agent-output/ops/workflow-index.md`);
  }

  return failures;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const workspaceRoot = path.resolve(args["workspace-root"] ?? process.cwd());
  const workflowsDir = path.join(workspaceRoot, "agent-output", "workflows");
  const workflowIndexPath = path.join(workspaceRoot, "agent-output", "ops", "workflow-index.md");
  const agentOutputRoot = path.join(workspaceRoot, "agent-output");

  const requiredFrontmatterFields = [
    "workflow_id",
    "project_name",
    "type",
    "parent",
    "status",
    "owner",
    "last_updated"
  ];

  const requiredHeadings = [
    "Summary",
    "Relations",
    "Decisions",
    "Constraints",
    "Artifacts",
    "Handoffs",
    "Next"
  ];

  const placeholderPatterns = [
    /\[\[WF-\[[^\]]+\]\]\]/,
    /WF-[A-Za-z]+-ID/,
    /WF-\[ID\]/,
    /\[\[WF-\[[^\]]+\]\]\]/
  ];

  let workflowIndex = "";
  try {
    workflowIndex = await readFile(workflowIndexPath, "utf8");
  } catch {
    console.error(`Obsidian graph verification failed: missing ${workflowIndexPath}`);
    process.exitCode = 1;
    return;
  }

  const entries = await readdir(workflowsDir, { withFileTypes: true });
  const workflowFiles = entries
    .filter((entry) => entry.isFile() && /^WF-.*\.md$/i.test(entry.name))
    .map((entry) => entry.name)
    .sort();

  if (workflowFiles.length === 0) {
    console.log("No workflow notes found in agent-output/workflows; skipping graph verification.");
    return;
  }

  const markdownBasenames = await collectMarkdownBasenames(agentOutputRoot);
  const failures = [];
  const workflowBasenames = new Set(workflowFiles.map((fileName) => fileName.replace(/\.md$/i, "")));

  const indexTargets = extractIndexWorkflowTargets(workflowIndex);
  for (const target of indexTargets) {
    if (!workflowBasenames.has(target)) {
      failures.push(
        `agent-output/ops/workflow-index.md: index link points to missing workflow note [[workflows/${target}]]`
      );
    }
  }

  for (const fileName of workflowFiles) {
    const filePath = path.join(workflowsDir, fileName);
    const content = await readFile(filePath, "utf8");

    failures.push(
      ...validateWorkflowNote({
        fileName,
        content,
        workflowIndex,
        markdownBasenames,
        requiredFrontmatterFields,
        requiredHeadings,
        placeholderPatterns
      })
    );
  }

  if (failures.length > 0) {
    console.error("Obsidian graph verification failed:");
    for (const failure of failures) {
      console.error(`- ${failure}`);
    }
    process.exitCode = 1;
    return;
  }

  console.log(`Obsidian graph verification passed for ${workflowFiles.length} workflow note(s).`);
}

main().catch((error) => {
  console.error(
    "Obsidian graph verification failed:",
    error instanceof Error ? error.message : String(error)
  );
  process.exitCode = 1;
});
