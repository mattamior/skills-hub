import { readFile } from "node:fs/promises";
import path from "node:path";

const data = JSON.parse(await readFile("dist/skills.json", "utf8"));
const health = JSON.parse(await readFile("dist/health.json", "utf8"));
const html = await readFile("dist/index.html", "utf8");
const app = await readFile("dist/app.js", "utf8");
const detailScript = await readFile("dist/detail.js", "utf8");
const languageScript = await readFile("dist/lang.js", "utf8");

if (!Array.isArray(data.skills) || data.skills.length === 0) throw new Error("Gallery contains no skills");
for (const skill of data.skills) {
  const required = ["name", "displayName", "shortDescription", "description", "brandColor", "defaultPrompt", "body", "source", "agentSource"];
  for (const field of required) {
    if (!skill[field]) throw new Error(`Incomplete gallery entry ${skill.slug}: missing ${field}`);
  }
  if (!skill.defaultPrompt.includes(`$${skill.slug}`)) throw new Error(`Gallery prompt does not invoke ${skill.slug}`);

  const zh = skill.localized?.["zh-CN"];
  if (!zh?.shortDescription || !zh?.description || !zh?.examplePrompt) throw new Error(`Gallery entry ${skill.slug} is missing zh-CN localization`);
  if (!zh.examplePrompt.includes(`$${skill.slug}`)) throw new Error(`Chinese gallery example does not invoke ${skill.slug}`);

  const detail = await readFile(path.join("dist", "skills", skill.slug, "index.html"), "utf8");
  if (!detail.includes(skill.displayName)) throw new Error(`Detail page title missing for ${skill.slug}`);
  if (!detail.includes(`./scripts/link-skills.sh ${skill.slug}`)) throw new Error(`Install command missing for ${skill.slug}`);
  if (!detail.includes(skill.source) || !detail.includes(skill.agentSource)) throw new Error(`Source provenance missing for ${skill.slug}`);
  if (!detail.includes('data-lang="en"') || !detail.includes('data-lang="zh"')) throw new Error(`Language switch missing for ${skill.slug}`);
  if (!detail.includes(`https://skills-hub.hkooii.com/skills/${skill.slug}/`)) throw new Error(`Canonical detail URL missing for ${skill.slug}`);
  if (!detail.includes('id="skill-localization"') || !detail.includes('/lang.js')) throw new Error(`Localized detail payload missing for ${skill.slug}`);
}
if (health.status !== "ok" || health.skills !== data.skills.length) throw new Error("Health metadata does not match gallery data");
if (!html.includes("Agent Skills") || !html.includes("skills.json") || !html.includes('id="usage"')) throw new Error("Gallery shell is missing required content hooks");
if (!html.includes('<link rel="canonical" href="https://skills-hub.hkooii.com/">')) throw new Error("Gallery canonical URL is missing or stale");
if (!html.includes('data-lang="en"') || !html.includes('data-lang="zh"')) throw new Error("Gallery language switch is missing");
if (!app.includes("/skills/") || !app.includes('localized?.["zh-CN"]')) throw new Error("Catalog cards are not wired to localized skill detail pages");
if (!detailScript.includes("#skill-localization") || !detailScript.includes("skillsHubLanguage")) throw new Error("Detail pages are not wired to the language runtime");
if (!languageScript.includes("skills-hub-language") || !languageScript.includes("localStorage")) throw new Error("Language preference persistence is missing");

console.log(`Verified bilingual catalog output for ${data.skills.length} skill(s), including localized summaries, prompts, and detail pages.`);
