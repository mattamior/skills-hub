import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const distDir = path.join(root, "dist");
const repositoryUrl = "https://github.com/mattamior/skills-hub";
const publicUrl = "https://skills-hub.hkooii.com";

function parseChineseCatalog(markdown) {
  const purposes = new Map();
  const examples = new Map();

  for (const match of markdown.matchAll(/^\|\s*\[\`([^`]+)\`\]\([^)]+\)\s*\|\s*(.+?)\s*\|\s*$/gm)) {
    purposes.set(match[1], match[2].trim());
  }

  for (const line of markdown.split(/\r?\n/)) {
    const example = line.trim();
    const slug = example.match(/^\$([a-z0-9-]+)\s+.+$/)?.[1];
    if (slug && !examples.has(slug)) examples.set(slug, example);
  }

  return { purposes, examples };
}

const jsonForHtml = (value) => JSON.stringify(value).replaceAll("<", "\\u003c");

const readmeZh = await readFile(path.join(root, "README.zh.md"), "utf8");
const chineseCatalog = parseChineseCatalog(readmeZh);
const dataPath = path.join(distDir, "skills.json");
const data = JSON.parse(await readFile(dataPath, "utf8"));

for (const skill of data.skills) {
  const purpose = chineseCatalog.purposes.get(skill.slug);
  const examplePrompt = chineseCatalog.examples.get(skill.slug);
  if (!purpose) throw new Error(`README.zh.md is missing a Skills table purpose for ${skill.slug}`);
  if (!examplePrompt) throw new Error(`README.zh.md is missing a Chinese invocation example for ${skill.slug}`);

  skill.localized = {
    ...(skill.localized || {}),
    "zh-CN": {
      shortDescription: purpose,
      description: purpose,
      examplePrompt
    }
  };

  const detailPath = path.join(distDir, "skills", skill.slug, "index.html");
  let detail = await readFile(detailPath, "utf8");

  if (!detail.includes('data-lang="en"')) {
    const githubLink = `      <a href="${repositoryUrl}">GitHub ↗</a>`;
    const switcher = `${githubLink}
      <div role="group" aria-label="Language" data-aria-en="Language" data-aria-zh="语言">
        <button class="button" type="button" data-lang="en">EN</button>
        <button class="button" type="button" data-lang="zh">中文</button>
      </div>`;
    if (!detail.includes(githubLink)) throw new Error(`Unable to inject language switch for ${skill.slug}`);
    detail = detail.replace(githubLink, switcher);
  }

  if (!detail.includes('rel="canonical"')) {
    detail = detail.replace(
      '  <link rel="stylesheet" href="/styles.css">',
      `  <link rel="canonical" href="${publicUrl}/skills/${encodeURIComponent(skill.slug)}/">\n  <link rel="stylesheet" href="/styles.css">`
    );
  }

  const localization = {
    en: {
      description: skill.description,
      prompt: skill.defaultPrompt
    },
    zh: {
      description: purpose,
      prompt: examplePrompt
    }
  };

  if (!detail.includes('id="skill-localization"')) {
    const detailScript = '  <script src="/detail.js" defer></script>';
    const localizedScripts = `  <script src="/lang.js"></script>\n  <script type="application/json" id="skill-localization">${jsonForHtml(localization)}</script>\n${detailScript}`;
    if (!detail.includes(detailScript)) throw new Error(`Unable to inject localization payload for ${skill.slug}`);
    detail = detail.replace(detailScript, localizedScripts);
  }

  await writeFile(detailPath, detail);
}

await writeFile(dataPath, `${JSON.stringify(data, null, 2)}\n`);
console.log(`Localized Agent Skills catalog for English and Simplified Chinese (${data.skills.length} skill(s)).`);
