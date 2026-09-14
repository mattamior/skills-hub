import { readdir, readFile } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const localizationPath = path.join(root, "locales", "zh-CN.json");
const localization = JSON.parse(await readFile(localizationPath, "utf8"));
const readmeZh = await readFile(path.join(root, "README.zh.md"), "utf8");
const readmeEn = await readFile(path.join(root, "README.en.md"), "utf8");
const entries = await readdir(path.join(root, "skills"), { withFileTypes: true });
const skillSlugs = entries.filter((entry) => entry.isDirectory()).map((entry) => entry.name).sort();
const localizedSlugs = Object.keys(localization.skills ?? {}).sort();

if (localization.locale !== "zh-CN") throw new Error(`${localizationPath} locale must be zh-CN`);
if (JSON.stringify(skillSlugs) !== JSON.stringify(localizedSlugs)) {
  throw new Error(`Localization skill keys must exactly match skills/: expected ${skillSlugs.join(", ")}; found ${localizedSlugs.join(", ")}`);
}

for (const slug of skillSlugs) {
  const entry = localization.skills[slug];
  for (const field of ["shortDescription", "description", "examplePrompt"]) {
    if (typeof entry?.[field] !== "string" || !entry[field].trim()) {
      throw new Error(`${localizationPath} ${slug} is missing ${field}`);
    }
  }
  if (!entry.examplePrompt.includes(`$${slug}`)) {
    throw new Error(`${localizationPath} ${slug} examplePrompt must invoke $${slug}`);
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

console.log(`Verified structured zh-CN localization and bilingual README alignment for ${skillSlugs.length} skill(s).`);
