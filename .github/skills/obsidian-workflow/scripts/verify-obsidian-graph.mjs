import { readdir, readFile } from "node:fs/promises";
import path from "node:path";

import YAML from "yaml";

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

const args = parseArgs(process.argv.slice(2));
const workspaceRoot = path.resolve(args["workspace-root"] ?? process.cwd());

const workflowsDir = path.join(workspaceRoot, "agent-output", "workflows");
const workflowIndexPath = path.join(workspaceRoot, "agent-output", "ops", "workflow-index.md");

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

function escapeRegex(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function normalizePosixPath(...parts) {
  return path.posix.join(...parts);
}

function extractWikiLinkTargets(content) {
  return [...content.matchAll(/\[\[([^\]]+)\]\]/g)]
    .map((match) => match[1])
    .map((value) => value.split("|")[0]?.trim() ?? "")
    .map((value) => value.split("#")[0]?.trim() ?? "")
    .filter(Boolean);
}

function parseFrontmatterAndBody(content) {
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);

  if (!frontmatterMatch) {
    return {
      frontmatter: null,
      body: content,
      parseError: "missing YAML frontmatter"
    };
  }

  const [, frontmatterRaw, body] = frontmatterMatch;

  try {
    const parsed = YAML.parse(frontmatterRaw);

    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
      return {
        frontmatter: null,
        body,
        parseError: "frontmatter must be a YAML object"
      };
    }

    return {
      frontmatter: parsed,
      body,
      parseError: null
    };
  } catch (error) {
    return {
      frontmatter: null,
      body,
      parseError: `invalid YAML frontmatter (${error instanceof Error ? error.message : String(error)})`
    };
  }
}

function validateWorkflowNote({ fileName, content, workflowIndex }) {
  const failures = [];
  const notePath = normalizePosixPath("agent-output", "workflows", fileName);
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

  if (typeof frontmatter.workflow_id === "string") {
    if (!/^WF-\d+/.test(frontmatter.workflow_id)) {
      failures.push(`${notePath}: \`workflow_id\` must start with WF-<number>`);
    }

    if (!(fileName === `${frontmatter.workflow_id}.md` || fileName.startsWith(`${frontmatter.workflow_id}-`))) {
      failures.push(`${notePath}: file name must start with workflow_id \`${frontmatter.workflow_id}\``);
    }
  }

  const parentValue = frontmatter.parent;
  let parentTarget = "";

  if (typeof parentValue === "string") {
    if (parentValue === "none") {
      parentTarget = "none";
    } else {
      const parentTargets = extractWikiLinkTargets(parentValue);
      parentTarget = parentTargets[0] ?? "";

      if (!/^\[\[[^\]]+\]\]$/.test(parentValue) || parentTarget.length === 0) {
        failures.push(`${notePath}: \`parent\` must be \`none\` or a single wikilink like [[WF-123]]`);
      } else if (!/WF-\d+/.test(parentTarget)) {
        failures.push(`${notePath}: \`parent\` wikilink must target a WF node`);
      }
    }
  }

  if (typeof frontmatter.last_updated === "string" && !/^\d{4}-\d{2}-\d{2}$/.test(frontmatter.last_updated)) {
    failures.push(`${notePath}: \`last_updated\` should use YYYY-MM-DD format`);
  }

  for (const heading of requiredHeadings) {
    const headingPattern = new RegExp(`^##\\s+${escapeRegex(heading)}\\s*$`, "m");

    if (!headingPattern.test(body)) {
      failures.push(`${notePath}: missing required heading \`## ${heading}\``);
    }
  }

  const bodyLinks = extractWikiLinkTargets(body);
  const normalizedSelfTargets = new Set([
    noteBaseName,
    normalizePosixPath("workflows", noteBaseName)
  ]);

  const nonSelfLinks = bodyLinks.filter((target) => !normalizedSelfTargets.has(target));
  const relationEdges = parentTarget !== "none" && parentTarget ? [parentTarget, ...nonSelfLinks] : nonSelfLinks;

  if (relationEdges.length === 0) {
    failures.push(`${notePath}: missing graph edges; add wikilinks in Relations/Artifacts or set a parent wikilink`);
  }

  const noteLinkPattern = new RegExp(
    `\\[\\[workflows\\/${escapeRegex(noteBaseName)}(?:\\|[^\\]]+)?\\]\\]`,
    "m"
  );

  if (!noteLinkPattern.test(workflowIndex)) {
    failures.push(`${notePath}: missing index link in agent-output/ops/workflow-index.md`);
  }

  return failures;
}

async function main() {
  const workflowIndex = await readFile(workflowIndexPath, "utf8");
  const entries = await readdir(workflowsDir, { withFileTypes: true });

  const workflowFiles = entries
    .filter((entry) => entry.isFile() && /^WF-\d+.*\.md$/i.test(entry.name))
    .map((entry) => entry.name)
    .sort();

  if (workflowFiles.length === 0) {
    console.log("No workflow notes found in agent-output/workflows; skipping graph verification.");
    return;
  }

  const failures = [];

  for (const fileName of workflowFiles) {
    const filePath = path.join(workflowsDir, fileName);
    const content = await readFile(filePath, "utf8");

    failures.push(...validateWorkflowNote({ fileName, content, workflowIndex }));
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
