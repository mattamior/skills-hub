import { createHash } from "node:crypto";
import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const distDir = path.join(root, "dist");

async function collectHtmlFiles(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const entryPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      files.push(...await collectHtmlFiles(entryPath));
    } else if (entry.isFile() && entry.name.endsWith(".html")) {
      files.push(entryPath);
    }
  }
  return files;
}

const runtimeAssets = (await readdir(distDir, { withFileTypes: true }))
  .filter((entry) => entry.isFile() && /\.(?:js|css)$/.test(entry.name))
  .map((entry) => entry.name)
  .sort();

if (runtimeAssets.length === 0) {
  throw new Error("No root JavaScript or CSS assets were emitted to dist/");
}

const hash = createHash("sha256");
for (const asset of runtimeAssets) {
  hash.update(asset);
  hash.update("\0");
  hash.update(await readFile(path.join(distDir, asset)));
  hash.update("\0");
}
const version = hash.digest("hex").slice(0, 12);
const runtimeAssetSet = new Set(runtimeAssets);

const htmlFiles = (await collectHtmlFiles(distDir)).sort();
for (const htmlFile of htmlFiles) {
  const source = await readFile(htmlFile, "utf8");
  let replacements = 0;
  const versioned = source.replace(/\b(src|href)="\/([^"/?]+\.(?:js|css))"/g, (match, attribute, asset) => {
    if (!runtimeAssetSet.has(asset)) return match;
    replacements += 1;
    return `${attribute}="/${asset}?v=${version}"`;
  });
  if (replacements === 0) {
    throw new Error(`${path.relative(root, htmlFile)} contains no versionable runtime asset references`);
  }
  await writeFile(htmlFile, versioned);
}

await writeFile(path.join(distDir, "asset-version.json"), `${JSON.stringify({ version, assets: runtimeAssets }, null, 2)}\n`);
console.log(`Versioned ${runtimeAssets.length} gallery runtime asset(s) across ${htmlFiles.length} HTML page(s) with ${version}.`);
