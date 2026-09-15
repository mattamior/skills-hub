import { readdir, readFile } from "node:fs/promises";
import path from "node:path";
import YAML from "yaml";

const root = process.cwd();
const localizationPath = path.join(root, "locales", "zh-CN.json");
const localization = JSON.parse(await readFile(localizationPath, "utf8"));
const readmeZh = await readFile(path.join(root, "README.zh.md"), "utf8");
const readmeEn = await readFile(path.join(root, "README.en.md"), "utf8");
const entries = await readdir(path.join(root, "skills"), { withFileTypes: true });
const skillSlugs = entries.filter((entry) => entry.isDirectory()).map((entry) => entry.name).sort();
const localizedSlugs = Object.keys(localization.skills ?? {}).sort();

function parseSkillSource(source, label) {
  const lines = source.split(/\r?\n/);
  if (lines[0]?.trim() !== "---") throw new Error(`${label} must start with YAML frontmatter`);
  const closingIndex = lines.findIndex((line, index) => index > 0 && line.trim() === "---");
  if (closingIndex === -1) throw new Error(`${label} frontmatter is not closed`);
  const frontmatter = YAML.parse(lines.slice(1, closingIndex).join("\n")) ?? {};
  return {
    frontmatter,
    body: lines.slice(closingIndex + 1).join("\n").trim()
  };
}

function relativeLinks(markdown) {
  return [...markdown.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)]
    .map((match) => match[1])
    .filter((href) => !/^(https?:|mailto:|#)/.test(href))
    .map((href) => href.replace(/^\.\//, ""))
    .sort();
}

function countMatches(source, pattern) {
  return [...source.matchAll(pattern)].length;
}

function contentBlockCount(source) {
  return source
    .split(/\n\s*\n/)
    .map((block) => block.trim())
    .filter(Boolean)
    .filter((block) => !block.startsWith("```"))
    .length;
}

if (localization.locale !== "zh-CN") throw new Error(`${localizationPath} locale must be zh-CN`);
if (JSON.stringify(skillSlugs) !== JSON.stringify(localizedSlugs)) {
  throw new Error(`Localization skill keys must exactly match skills/: expected ${skillSlugs.join(", ")}; found ${localizedSlugs.join(", ")}`);
}

for (const slug of skillSlugs) {
  const entry = localization.skills[slug];
  for (const field of ["displayName", "shortDescription", "description", "examplePrompt", "bodyMarkdown"]) {
    if (typeof entry?.[field] !== "string" || !entry[field].trim()) {
      throw new Error(`${localizationPath} ${slug} is missing ${field}`);
    }
  }
  if (!entry.examplePrompt.includes(`$${slug}`)) {
    throw new Error(`${localizationPath} ${slug} examplePrompt must invoke $${slug}`);
  }
  if (!entry.bodyMarkdown.startsWith(`# ${entry.displayName}\n`)) {
    throw new Error(`${localizationPath} ${slug} bodyMarkdown must start with its localized displayName`);
  }

  const sourcePath = path.join(root, "skills", slug, "SKILL.md");
  const source = await readFile(sourcePath, "utf8");
  const { body } = parseSkillSource(source, sourcePath);
  if (body.includes(`$${slug}`) && !entry.bodyMarkdown.includes(`$${slug}`)) {
    throw new Error(`${localizationPath} ${slug} bodyMarkdown must preserve the canonical explicit invocation`);
  }

  const englishH2 = countMatches(body, /^##\s+/gm);
  const chineseH2 = countMatches(entry.bodyMarkdown, /^##\s+/gm);
  if (englishH2 !== chineseH2) {
    throw new Error(`${localizationPath} ${slug} bodyMarkdown must preserve all ${englishH2} level-two sections; found ${chineseH2}`);
  }

  const englishFences = countMatches(body, /^```/gm);
  const chineseFences = countMatches(entry.bodyMarkdown, /^```/gm);
  if (englishFences !== chineseFences) {
    throw new Error(`${localizationPath} ${slug} bodyMarkdown must preserve fenced code structure`);
  }

  const englishLinks = relativeLinks(body);
  const chineseLinks = relativeLinks(entry.bodyMarkdown);
  if (JSON.stringify(englishLinks) !== JSON.stringify(chineseLinks)) {
    throw new Error(`${localizationPath} ${slug} bodyMarkdown must preserve repository-relative references`);
  }

  const englishBlocks = contentBlockCount(body);
  const chineseBlocks = contentBlockCount(entry.bodyMarkdown);
  if (englishBlocks !== chineseBlocks) {
    throw new Error(`${localizationPath} ${slug} bodyMarkdown must preserve all ${englishBlocks} non-code content blocks; found ${chineseBlocks}`);
  }

  if (!readmeZh.includes(entry.shortDescription)) {
    throw new Error(`README.zh.md must include the canonical zh-CN summary for ${slug}`);
  }
  if (!readmeZh.includes(entry.examplePrompt)) {
    throw new Error(`README.zh.md must include the canonical zh-CN invocation example for ${slug}`);
  }
  if (!readmeZh.includes(slug) || !readmeEn.includes(slug)) {
    throw new Error(`Both formal READMEs must mention ${slug}`);
  }
}

console.log(`Verified complete structured zh-CN localization and bilingual README alignment for ${skillSlugs.length} skill(s).`);
