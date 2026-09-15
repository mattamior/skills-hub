import { createHash } from "node:crypto";
import { readdir, readFile } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const distDir = path.join(root, "dist");
const manifestPath = path.join(distDir, "asset-version.json");
const manifest = JSON.parse(await readFile(manifestPath, "utf8"));

async function collectHtmlFiles(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const entryPath = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...await collectHtmlFiles(entryPath));
    else if (entry.isFile() && entry.name.endsWith(".html")) files.push(entryPath);
  }
  return files;
}

if (!/^[0-9a-f]{12}$/.test(manifest.version || "")) {
  throw new Error("asset-version.json must contain a 12-character lowercase SHA-256 prefix");
}
if (!Array.isArray(manifest.assets) || manifest.assets.length === 0) {
  throw new Error("asset-version.json must list the runtime assets used to derive the version");
}
const expectedAssets = [...manifest.assets].sort();
if (JSON.stringify(manifest.assets) !== JSON.stringify(expectedAssets)) {
  throw new Error("asset-version.json assets must stay sorted for deterministic output");
}

const actualAssets = (await readdir(distDir, { withFileTypes: true }))
  .filter((entry) => entry.isFile() && /\.(?:js|css)$/.test(entry.name))
  .map((entry) => entry.name)
  .sort();
if (JSON.stringify(actualAssets) !== JSON.stringify(expectedAssets)) {
  throw new Error(`asset-version.json asset list does not match dist/: ${actualAssets.join(", ")}`);
}

const hash = createHash("sha256");
for (const asset of actualAssets) {
  hash.update(asset);
  hash.update("\0");
  hash.update(await readFile(path.join(distDir, asset)));
  hash.update("\0");
}
const expectedVersion = hash.digest("hex").slice(0, 12);
if (manifest.version !== expectedVersion) {
  throw new Error(`Asset version ${manifest.version} does not match emitted runtime content ${expectedVersion}`);
}

const assetSet = new Set(actualAssets);
const htmlFiles = (await collectHtmlFiles(distDir)).sort();
for (const htmlFile of htmlFiles) {
  const source = await readFile(htmlFile, "utf8");
  const refs = [...source.matchAll(/\b(?:src|href)="\/([^"/?]+\.(?:js|css))(?:\?v=([^"&]+))?"/g)];
  if (refs.length === 0) throw new Error(`${path.relative(root, htmlFile)} has no runtime asset references`);
  for (const [, asset, version] of refs) {
    if (!assetSet.has(asset)) continue;
    if (!version) throw new Error(`${path.relative(root, htmlFile)} references /${asset} without a cache-busting version`);
    if (version !== manifest.version) {
      throw new Error(`${path.relative(root, htmlFile)} references /${asset} with stale version ${version}`);
    }
  }
}

const headers = await readFile(path.join(distDir, "_headers"), "utf8");
if (!headers.includes("Cache-Control: no-cache")) {
  throw new Error("Cloudflare Pages headers must require browser revalidation in addition to versioned asset URLs");
}

console.log(`Verified content-versioned runtime assets (${manifest.version}) across ${htmlFiles.length} HTML page(s).`);
