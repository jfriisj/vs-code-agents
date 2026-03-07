import { mkdir, readdir, readFile, writeFile } from "node:fs/promises";
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

function normalizeKey(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, "");
}

function parseFrontmatterObject(frontmatterRaw) {
  const parsed = {};
  const lines = frontmatterRaw.split(/\r?\n/);

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.length === 0 || trimmed.startsWith("#")) {
      continue;
    }

    const match = line.match(/^([^:]+):\s*(.*)$/);
    if (!match) {
      continue;
    }

    const key = normalizeKey(match[1]);
    let value = (match[2] ?? "").trim();

    if (
      (value.startsWith("\"") && value.endsWith("\"")) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }

    parsed[key] = value;
  }

  return parsed;
}

function parseFrontmatterAndBody(content) {
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);

  if (!frontmatterMatch) {
    return {
      frontmatter: {},
      body: content,
      parseError: "missing frontmatter"
    };
  }

  const [, frontmatterRaw, body] = frontmatterMatch;

  return {
    frontmatter: parseFrontmatterObject(frontmatterRaw),
    body,
    parseError: null
  };
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

function normalizeWikiAliases(content, aliasMap, replacementCounter) {
  return content.replace(/\[\[([^\]]+)\]\]/g, (fullMatch, rawTarget) => {
    const target = rawTarget.split("|")[0]?.trim() ?? "";
    const suffix = rawTarget.includes("|") ? `|${rawTarget.split("|").slice(1).join("|")}` : "";
    const normalized = normalizeLinkTarget(target);
    const mapped = aliasMap.get(normalized);

    if (!mapped) {
      return fullMatch;
    }

    replacementCounter.set(normalized, (replacementCounter.get(normalized) ?? 0) + 1);
    return `[[${mapped}${suffix}]]`;
  });
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

async function resolveProjectName(workspaceRoot) {
  const roadmapPath = path.join(workspaceRoot, "agent-output", "roadmap", "product-roadmap.md");

  try {
    const content = await readFile(roadmapPath, "utf8");
    const heading = content.match(/^#\s+(.+)$/m)?.[1]?.trim();
    if (heading && heading.length > 0) {
      return heading.replace(/\s+-\s+Product Roadmap$/i, "").trim();
    }
  } catch {
    // Fall back to workspace folder name.
  }

  return path.basename(workspaceRoot);
}

function inferWorkflowType(frontmatter, title) {
  const frontmatterType = frontmatter.type ?? frontmatter.Type ?? frontmatter.workflow_type;
  if (typeof frontmatterType === "string" && frontmatterType.trim().length > 0) {
    return frontmatterType.trim();
  }

  const normalizedTitle = title.toLowerCase();
  const map = [
    ["architecture", "Architecture"],
    ["security", "Security"],
    ["critique", "Critique"],
    ["code-review", "CodeReview"],
    ["codereview", "CodeReview"],
    ["qa", "QA"],
    ["uat", "UAT"],
    ["deployment", "Deployment"],
    ["retrospective", "Retrospective"],
    ["process improvement", "ProcessImprovement"],
    ["process-improvement", "ProcessImprovement"],
    ["pi", "ProcessImprovement"],
    ["plan", "Plan"],
    ["analysis", "Analysis"],
    ["epic", "Epic"]
  ];

  for (const [needle, mapped] of map) {
    if (normalizedTitle.includes(needle)) {
      return mapped;
    }
  }

  return "Analysis";
}

function ownerForType(workflowType) {
  const key = workflowType.toLowerCase();
  const owners = {
    epic: "01-roadmap",
    plan: "02-planner",
    analysis: "03-analyst",
    architecture: "04-architect",
    security: "05-security",
    critique: "06-critic",
    implementation: "07-implementer",
    codereview: "08-code-reviewer",
    qa: "09-qa",
    uat: "10-uat",
    deployment: "11-devops",
    retrospective: "12-retrospective",
    processimprovement: "13-pi",
    pi: "13-pi"
  };

  return owners[key] ?? "02-planner";
}

function normalizeWorkflowId(fileBaseName, frontmatter) {
  const fromFrontmatter =
    frontmatter.workflow_id ??
    frontmatter.id ??
    frontmatter.wf_id ??
    frontmatter.workflow;

  if (typeof fromFrontmatter === "string" && fromFrontmatter.trim().length > 0) {
    const trimmed = fromFrontmatter.trim();
    if (/^WF-/i.test(trimmed)) {
      return trimmed.replace(/\s+/g, "-");
    }
  }

  if (/^WF-/i.test(fileBaseName)) {
    return fileBaseName;
  }

  return `WF-${fileBaseName}`;
}

function normalizeParent(rawParent, markdownBasenames) {
  if (typeof rawParent !== "string" || rawParent.trim().length === 0) {
    return "none";
  }

  const trimmed = rawParent.trim();
  if (trimmed === "none") {
    return "none";
  }

  if (!/^\[\[[^\]]+\]\]$/.test(trimmed)) {
    return "none";
  }

  const target = normalizeLinkTarget(trimmed.slice(2, -2));
  if (target.length === 0) {
    return "none";
  }

  if (!markdownBasenames.has(target)) {
    return "none";
  }

  return `[[${target}]]`;
}

function cleanLegacyBody(body) {
  const lines = body.split(/\r?\n/);

  const withoutMainHeading = lines.filter((line, index) => {
    if (index === 0 && /^#\s+/.test(line.trim())) {
      return false;
    }
    return true;
  });

  const withoutHandoffLines = withoutMainHeading.filter(
    (line) => !line.includes("Handoff Ready. Parent Node context")
  );

  const normalizedHeadings = withoutHandoffLines.map((line) => line.replace(/^##\s+/g, "### "));

  return normalizedHeadings.join("\n").trim();
}

function extractSummary(title, workflowType, migrationDate) {
  return [
    title.length > 0 ? title : `Workflow note for ${workflowType}`,
    `Normalized to the unified workflow schema on ${migrationDate}.`
  ];
}

function extractConstraints(legacyBody) {
  const matches = legacyBody
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line.length > 0)
    .filter((line) => /(must|should|constraint|risk|gate|critical|sec-|pi-)/i.test(line))
    .slice(0, 4);

  if (matches.length === 0) {
    return ["No explicit constraints captured in the legacy note."];
  }

  return matches;
}

function extractArtifacts(legacyBody, fileName, markdownBasenames) {
  const paths = new Set();

  for (const match of legacyBody.matchAll(/agent-output\/[A-Za-z0-9_./-]+\.md/g)) {
    paths.add(match[0]);
  }

  const wikilinks = extractWikiLinkTargets(legacyBody);
  for (const target of wikilinks) {
    if (markdownBasenames.has(target)) {
      paths.add(`[[${target}]]`);
    }
  }

  if (paths.size === 0) {
    paths.add(`agent-output/workflows/${fileName}`);
  }

  return [...paths].slice(0, 8);
}

function writeIndexContent(entries, date) {
  const lines = [
    "# Active Workflows (Graph Index)",
    "",
    "> [!INFO] Managed Index",
    "> Regenerated by `node vs-code-agents/skills/obsidian-workflow/scripts/migrate-workflow-notes.mjs --workspace-root .`",
    "",
    "## Workflow Links"
  ];

  for (const entry of entries) {
    lines.push(
      `- [[workflows/${entry.baseName}|${entry.workflowId}]] | type: ${entry.type} | status: ${entry.status} | owner: ${entry.owner} | parent: ${entry.parent}`
    );
  }

  lines.push("", "## Metadata", `- last_updated: ${date}`, `- total_workflows: ${entries.length}`, "");

  return lines.join("\n");
}

async function loadWorkflowMetadata(workflowsDir) {
  const entries = await readdir(workflowsDir, { withFileTypes: true });
  const workflowFiles = entries
    .filter((entry) => entry.isFile() && /^WF-.*\.md$/i.test(entry.name))
    .map((entry) => entry.name)
    .sort();

  const metadata = [];

  for (const fileName of workflowFiles) {
    const filePath = path.join(workflowsDir, fileName);
    const content = await readFile(filePath, "utf8");
    const { frontmatter } = parseFrontmatterAndBody(content);
    const baseName = fileName.replace(/\.md$/i, "");

    metadata.push({
      fileName,
      baseName,
      workflowId: frontmatter.workflow_id ?? baseName,
      type: frontmatter.type ?? "Unknown",
      status: frontmatter.status ?? "Unknown",
      owner: frontmatter.owner ?? "Unknown",
      parent: frontmatter.parent ?? "none"
    });
  }

  return metadata;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const workspaceRoot = path.resolve(args["workspace-root"] ?? process.cwd());
  const writeIndexOnly = args["write-index-only"] === "true";

  const workflowsDir = path.join(workspaceRoot, "agent-output", "workflows");
  const opsDir = path.join(workspaceRoot, "agent-output", "ops");
  const indexPath = path.join(opsDir, "workflow-index.md");
  const reportPath = path.join(opsDir, "002-obsidian-workflow-migration-report.md");
  const agentOutputRoot = path.join(workspaceRoot, "agent-output");

  const now = new Date();
  const migrationDate = now.toISOString().slice(0, 10);

  await mkdir(opsDir, { recursive: true });

  if (writeIndexOnly) {
    const metadata = await loadWorkflowMetadata(workflowsDir);
    const indexContent = writeIndexContent(metadata, migrationDate);
    await writeFile(indexPath, indexContent, "utf8");
    console.log(`Updated workflow index with ${metadata.length} note(s).`);
    return;
  }

  const markdownBasenames = await collectMarkdownBasenames(agentOutputRoot);
  const projectName = await resolveProjectName(workspaceRoot);
  const replacementCounter = new Map();

  const aliasMap = new Map([
    ["WF-Plan-1", "Plan-1"],
    ["WF-Plan-1-Implementation-1", "001-core-handoff-implementation"],
    ["WF-Deployment-v0.1.0", "v0.1.0"],
    ["WF-Retrospective-1", "WF-1-retrospective"],
    ["WF-PI-1", "WF-1-process-improvement"],
    ["v0.1.0 Release Notes", "v0.1.0"]
  ]);

  const entries = await readdir(workflowsDir, { withFileTypes: true });
  const workflowFiles = entries
    .filter((entry) => entry.isFile() && /^WF-.*\.md$/i.test(entry.name))
    .map((entry) => entry.name)
    .sort();

  if (workflowFiles.length === 0) {
    console.log("No workflow notes found. Nothing to migrate.");
    return;
  }

  const migrated = [];

  for (const fileName of workflowFiles) {
    const filePath = path.join(workflowsDir, fileName);
    const originalContent = await readFile(filePath, "utf8");
    const { frontmatter, body } = parseFrontmatterAndBody(originalContent);

    const normalizedBody = normalizeWikiAliases(body, aliasMap, replacementCounter);
    const title = normalizedBody.match(/^#\s+(.+)$/m)?.[1]?.trim() ?? fileName.replace(/\.md$/i, "");
    const fileBaseName = fileName.replace(/\.md$/i, "");

    const workflowId = normalizeWorkflowId(fileBaseName, frontmatter);
    const workflowType = inferWorkflowType(frontmatter, title);
    const status = (frontmatter.status ?? frontmatter.Status ?? "Completed").trim();
    const owner = ownerForType(workflowType);

    const rawParent = frontmatter.parent ?? frontmatter.Parent ?? "none";
    const normalizedParentBody = normalizeWikiAliases(String(rawParent), aliasMap, replacementCounter);
    const parent = normalizeParent(normalizedParentBody, markdownBasenames);

    const links = extractWikiLinkTargets(normalizedBody);
    const blockTargets = [...new Set(links)]
      .filter((target) => target !== fileBaseName)
      .filter((target) => `[[${target}]]` !== parent)
      .slice(0, 6);

    const summary = extractSummary(title, workflowType, migrationDate);
    const legacyBody = cleanLegacyBody(normalizedBody);
    const constraints = extractConstraints(legacyBody);
    const artifacts = extractArtifacts(legacyBody, fileName, markdownBasenames);

    const handoffLine = normalizedBody
      .split(/\r?\n/)
      .map((line) => line.trim())
      .find((line) => line.includes("Handoff Ready. Parent Node context"));

    const legacyNotesBlock = legacyBody.length > 0 ? legacyBody : "- No legacy decision text captured.";

    const content = [
      "---",
      `workflow_id: ${workflowId}`,
      `project_name: \"${projectName}\"`,
      `type: ${workflowType}`,
      `parent: \"${parent}\"`,
      `status: ${status}`,
      `owner: ${owner}`,
      `last_updated: ${migrationDate}`,
      "---",
      "",
      "## Summary",
      `- ${summary[0]}`,
      `- ${summary[1]}`,
      "",
      "## Relations",
      `- **Depends On**: ${parent}`,
      `- **Blocks**: ${blockTargets.length > 0 ? blockTargets.map((target) => `[[${target}]]`).join(", ") : "none"}`,
      "",
      "## Decisions",
      "- Preserved legacy decision context below.",
      "",
      "### Legacy Notes",
      legacyNotesBlock,
      "",
      "## Constraints",
      ...constraints.map((line) => `- ${line.replace(/^-\s*/, "")}`),
      "",
      "## Artifacts",
      ...artifacts.map((artifact) => `- ${artifact}`),
      "",
      "## Handoffs",
      `### ${migrationDate} 00:00 [workflow-migration]`,
      "- Status: Legacy workflow note normalized to the unified schema.",
      "- Decisions: Placeholder identifiers and stale aliases were remapped where possible.",
      "- Changes: Frontmatter, headings, and graph links were standardized.",
      "- Next Owner: n/a",
      "- Open Risks: Review parent and block links if upstream workflow IDs change.",
      `- Artifacts: agent-output/workflows/${fileName}`,
      ...(handoffLine ? ["", `### ${migrationDate} 00:01 [legacy-handoff]`, `- Status: ${handoffLine}`] : []),
      "",
      "## Next",
      "- Keep this note immutable unless reconciliation with source artifacts is required.",
      ""
    ].join("\n");

    await writeFile(filePath, content, "utf8");

    migrated.push({
      fileName,
      baseName: fileBaseName,
      workflowId,
      type: workflowType,
      status,
      owner,
      parent
    });
  }

  const indexContent = writeIndexContent(migrated, migrationDate);
  await writeFile(indexPath, indexContent, "utf8");

  const replacementLines = [...replacementCounter.entries()]
    .sort((a, b) => a[0].localeCompare(b[0]))
    .map(([from, count]) => `- ${from} -> ${aliasMap.get(from)} (${count} replacement${count === 1 ? "" : "s"})`);

  const reportLines = [
    "# 002 - Obsidian Workflow Migration Report",
    "",
    `Date: ${migrationDate}`,
    "",
    "## Summary",
    `- Migrated workflow notes: ${migrated.length}`,
    "- Normalized schema: workflow_id, project_name, type, parent, status, owner, last_updated",
    "- Added required sections: Summary, Relations, Decisions, Constraints, Artifacts, Handoffs, Next",
    `- Regenerated index: ${path.posix.join("agent-output", "ops", "workflow-index.md")}`,
    "",
    "## Alias Replacements",
    ...(replacementLines.length > 0 ? replacementLines : ["- No alias replacements were needed."]),
    "",
    "## Notes",
    "- This migration preserves legacy narrative under `## Decisions` > `### Legacy Notes`.",
    "- Run verifier after migration:",
    "  - `node vs-code-agents/skills/obsidian-workflow/scripts/verify-obsidian-graph.mjs --workspace-root .`",
    ""
  ];

  await writeFile(reportPath, reportLines.join("\n"), "utf8");

  console.log(`Migrated ${migrated.length} workflow note(s).`);
  console.log(`Wrote workflow index: ${indexPath}`);
  console.log(`Wrote migration report: ${reportPath}`);
}

main().catch((error) => {
  console.error("Workflow migration failed:", error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
});
