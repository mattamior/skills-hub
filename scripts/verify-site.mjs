import { readFile } from "node:fs/promises";
import path from "node:path";

const data = JSON.parse(await readFile("dist/skills.json", "utf8"));
const health = JSON.parse(await readFile("dist/health.json", "utf8"));
const html = await readFile("dist/index.html", "utf8");
const app = await readFile("dist/app.js", "utf8");
const detailScript = await readFile("dist/detail.js", "utf8");
const languageScript = await readFile("dist/lang.js", "utf8");
const themeScript = await readFile("dist/theme.js", "utf8");
const themeStyle = await readFile("dist/theme.css", "utf8");
const sitemap = await readFile("dist/sitemap.xml", "utf8");
const robots = await readFile("dist/robots.txt", "utf8");
const headers = await readFile("dist/_headers", "utf8");
const notFound = await readFile("dist/404.html", "utf8");

const publicUrl = "https://skills-hub.lapplax.com";

function assertBilingualPairs(source, label) {
  const pairs = [
    ["data-en=", "data-zh="],
    ["data-aria-en=", "data-aria-zh="],
    ["data-placeholder-en=", "data-placeholder-zh="],
    ["data-content-en=", "data-content-zh="]
  ];
  for (const tag of source.match(/<[^>]+>/g) ?? []) {
    for (const [english, chinese] of pairs) {
      const hasEnglish = tag.includes(english);
      const hasChinese = tag.includes(chinese);
      if (hasEnglish !== hasChinese) {
        throw new Error(`${label} has an incomplete bilingual attribute pair in ${tag.slice(0, 160)}`);
      }
    }
  }
}

if (Object.hasOwn(data, "generatedAt")) throw new Error("skills.json must remain deterministic and omit generatedAt");
if (!Array.isArray(data.skills) || data.skills.length === 0) throw new Error("Gallery contains no skills");
assertBilingualPairs(html, "Gallery shell");
assertBilingualPairs(notFound, "404 page");

for (const skill of data.skills) {
  const required = ["name", "displayName", "shortDescription", "description", "brandColor", "defaultPrompt", "body", "source", "agentSource"];
  for (const field of required) {
    if (!skill[field]) throw new Error(`Incomplete gallery entry ${skill.slug}: missing ${field}`);
  }
  if (!skill.defaultPrompt.includes(`$${skill.slug}`)) throw new Error(`Gallery prompt does not invoke ${skill.slug}`);

  const zh = skill.localized?.["zh-CN"];
  for (const field of ["displayName", "shortDescription", "description", "examplePrompt", "bodyMarkdown"]) {
    if (!zh?.[field]) throw new Error(`Gallery entry ${skill.slug} is missing zh-CN ${field}`);
  }
  if (!zh.examplePrompt.includes(`$${skill.slug}`) || !zh.bodyMarkdown.includes(`$${skill.slug}`)) {
    throw new Error(`Chinese gallery invocation copy does not invoke ${skill.slug}`);
  }

  const detail = await readFile(path.join("dist", "skills", skill.slug, "index.html"), "utf8");
  const canonicalUrl = `${publicUrl}/skills/${skill.slug}/`;
  assertBilingualPairs(detail, `Detail page ${skill.slug}`);
  if (!detail.includes(skill.displayName) || !detail.includes(zh.displayName)) throw new Error(`Bilingual detail page title missing for ${skill.slug}`);
  if (!detail.includes(`./scripts/link-skills.sh ${skill.slug}`)) throw new Error(`Install command missing for ${skill.slug}`);
  if (!detail.includes(skill.source) || !detail.includes(skill.agentSource)) throw new Error(`Source provenance missing for ${skill.slug}`);
  if (!detail.includes('data-lang="en"') || !detail.includes('data-lang="zh"')) throw new Error(`Language switch missing for ${skill.slug}`);
  if (!detail.includes('data-contract-lang="en"') || !detail.includes('data-contract-lang="zh"')) throw new Error(`Bilingual operating contract missing for ${skill.slug}`);
  if (!detail.includes('data-theme-toggle') || !detail.includes('/theme.js') || !detail.includes('/theme.css')) throw new Error(`Theme runtime missing for ${skill.slug}`);
  if (!detail.includes(`<link rel="canonical" href="${canonicalUrl}">`)) throw new Error(`Canonical detail URL missing for ${skill.slug}`);
  if (!detail.includes(`<meta property="og:url" content="${canonicalUrl}">`)) throw new Error(`Open Graph URL missing for ${skill.slug}`);
  if (!detail.includes('/lang.js') || !detail.includes('/detail.js')) throw new Error(`Localized detail runtime missing for ${skill.slug}`);
  if (!detail.includes(`${skill.source.replace("SKILL.md", "references/")}`) && skill.body.includes("references/")) {
    throw new Error(`Rendered Markdown references are not linked to repository source for ${skill.slug}`);
  }
  if (!sitemap.includes(`<loc>${canonicalUrl}</loc>`)) throw new Error(`Sitemap is missing ${skill.slug}`);
}

if (health.status !== "ok" || health.skills !== data.skills.length) throw new Error("Health metadata does not match gallery data");
if (!html.includes("Agent Skills") || !html.includes("skills.json") || !html.includes('id="usage"')) throw new Error("Gallery shell is missing required content hooks");
if (!html.includes(`<link rel="canonical" href="${publicUrl}/">`)) throw new Error("Gallery canonical URL is missing or stale");
if (!html.includes(`<meta property="og:url" content="${publicUrl}/">`)) throw new Error("Gallery Open Graph URL is missing or stale");
if (!html.includes('property="og:title"') || !html.includes('name="twitter:card"')) throw new Error("Gallery social metadata is missing");
if (!html.includes('data-lang="en"') || !html.includes('data-lang="zh"')) throw new Error("Gallery language switch is missing");
if (!html.includes('data-theme-toggle') || !html.includes('/theme.js') || !html.includes('/theme.css')) throw new Error("Gallery theme switch is missing");
if (!app.includes("/skills/") || !app.includes('localized?.["zh-CN"]?.displayName') || !app.includes('localized?.["zh-CN"]?.bodyMarkdown')) {
  throw new Error("Catalog cards/search are not wired to complete zh-CN skill localization");
}
if (!detailScript.includes("[data-contract-lang]") || !detailScript.includes("skillsHubLanguage")) throw new Error("Detail pages are not wired to complete language switching");
if (!languageScript.includes("skills-hub-language") || !languageScript.includes("localStorage")) throw new Error("Language preference persistence is missing");
if (!themeScript.includes("skills-hub-theme") || !themeScript.includes("prefers-color-scheme") || !themeScript.includes("localStorage")) throw new Error("Theme preference runtime is incomplete");
if (!themeStyle.includes(':root[data-theme="light"]') || !themeStyle.includes('.theme-toggle')) throw new Error("Light theme styling is incomplete");
if (!sitemap.includes(`${publicUrl}/`)) throw new Error("Sitemap is missing the canonical root URL");
if (!robots.includes(`Sitemap: ${publicUrl}/sitemap.xml`)) throw new Error("robots.txt is missing the canonical sitemap URL");
for (const header of [
  "X-Frame-Options: DENY",
  "X-Content-Type-Options: nosniff",
  "Referrer-Policy: strict-origin-when-cross-origin",
  "Permissions-Policy:",
  "Cross-Origin-Opener-Policy: same-origin"
]) {
  if (!headers.includes(header)) throw new Error(`Cloudflare Pages security headers are missing ${header}`);
}
if (!headers.includes("https://skills-hub-ea7.pages.dev/*") || !headers.includes("https://:version.skills-hub-ea7.pages.dev/*") || !headers.includes("X-Robots-Tag: noindex")) {
  throw new Error("Provider Pages URLs are not excluded from indexing");
}
if (!headers.includes("https://skills-hub.hkooii.com/*")) throw new Error("Legacy custom domain is not excluded from indexing");
if (!notFound.includes('data-zh="页面不存在 — Agent Skills"') || !notFound.includes('data-lang="zh"') || !notFound.includes('data-theme-toggle')) {
  throw new Error("Bilingual themed 404 page is incomplete");
}

console.log(`Verified deterministic fully bilingual themed catalog output for ${data.skills.length} skill(s), including SEO, security metadata, and detail pages.`);
