import { cp, mkdir, readdir, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import MarkdownIt from "markdown-it";
import YAML from "yaml";

const root = process.cwd();
const skillsDir = path.join(root, "skills");
const siteDir = path.join(root, "site");
const distDir = path.join(root, "dist");
const localizationFile = path.join(root, "locales", "zh-CN.json");
const repositoryUrl = "https://github.com/mattamior/skills-hub";
const publicUrl = "https://skills-hub.lapplax.com";

function parseFrontmatter(source) {
  const lines = source.split(/\r?\n/);
  if (lines[0]?.trim() !== "---") throw new Error("SKILL.md must start with YAML frontmatter");

  const closingIndex = lines.findIndex((line, index) => index > 0 && line.trim() === "---");
  if (closingIndex === -1) throw new Error("SKILL.md frontmatter is not closed");

  let frontmatter;
  try {
    frontmatter = YAML.parse(lines.slice(1, closingIndex).join("\n")) ?? {};
  } catch (error) {
    throw new Error(`Unable to parse SKILL.md frontmatter: ${error.message}`, { cause: error });
  }
  if (!frontmatter || typeof frontmatter !== "object" || Array.isArray(frontmatter)) {
    throw new Error("SKILL.md frontmatter must be a YAML mapping");
  }

  return {
    frontmatter,
    body: lines.slice(closingIndex + 1).join("\n").trim()
  };
}

function parseYamlMapping(source, label) {
  let value;
  try {
    value = YAML.parse(source);
  } catch (error) {
    throw new Error(`Unable to parse ${label}: ${error.message}`, { cause: error });
  }
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new Error(`${label} must be a YAML mapping`);
  }
  return value;
}

const escapeHtml = (value) => String(value)
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;")
  .replaceAll("'", "&#039;");

const escapeXml = (value) => escapeHtml(value);

function resolveMarkdownHref(href, slug) {
  if (/^(https?:|mailto:|#)/.test(href)) return href;
  const relative = href.replace(/^\.\//, "");
  return `${repositoryUrl}/blob/main/skills/${slug}/${relative}`;
}

const markdown = new MarkdownIt({ html: false, linkify: false, typographer: false });
const defaultLinkOpen = markdown.renderer.rules.link_open;
markdown.renderer.rules.link_open = (tokens, index, options, env, self) => {
  const hrefIndex = tokens[index].attrIndex("href");
  if (hrefIndex >= 0 && env?.slug) {
    tokens[index].attrs[hrefIndex][1] = resolveMarkdownHref(tokens[index].attrs[hrefIndex][1], env.slug);
  }
  if (defaultLinkOpen) return defaultLinkOpen(tokens, index, options, env, self);
  return self.renderToken(tokens, index, options);
};

function renderMarkdown(source, slug) {
  return markdown.render(source, { slug });
}

function renderSkillPage(skill) {
  const zh = skill.localized["zh-CN"];
  const installCommand = `git clone ${repositoryUrl}.git\ncd skills-hub\n./scripts/link-skills.sh ${skill.slug}`;
  const implicitEn = skill.allowImplicitInvocation
    ? "Automatic selection allowed"
    : "Explicit invocation only";
  const implicitZh = skill.allowImplicitInvocation
    ? "允许自动选择"
    : "仅显式调用";
  const sourceUrl = `${repositoryUrl}/blob/main/${skill.source}`;
  const agentUrl = `${repositoryUrl}/blob/main/${skill.agentSource}`;
  const canonicalUrl = `${publicUrl}/skills/${encodeURIComponent(skill.slug)}/`;
  const pageTitleEn = `${skill.displayName} — Agent Skills`;
  const pageTitleZh = `${zh.displayName} — Agent Skills`;

  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="${escapeHtml(skill.shortDescription)}" data-content-en="${escapeHtml(skill.shortDescription)}" data-content-zh="${escapeHtml(zh.shortDescription)}">
  <meta name="theme-color" content="${escapeHtml(skill.brandColor)}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="${escapeHtml(pageTitleEn)}" data-content-en="${escapeHtml(pageTitleEn)}" data-content-zh="${escapeHtml(pageTitleZh)}">
  <meta property="og:description" content="${escapeHtml(skill.shortDescription)}" data-content-en="${escapeHtml(skill.shortDescription)}" data-content-zh="${escapeHtml(zh.shortDescription)}">
  <meta property="og:url" content="${escapeHtml(canonicalUrl)}">
  <meta name="twitter:card" content="summary">
  <title data-en="${escapeHtml(pageTitleEn)}" data-zh="${escapeHtml(pageTitleZh)}">${escapeHtml(pageTitleEn)}</title>
  <link rel="canonical" href="${escapeHtml(canonicalUrl)}">
  <script src="/theme.js"></script>
  <link rel="stylesheet" href="/styles.css">
  <link rel="stylesheet" href="/theme.css">
</head>
<body class="skill-page" style="--skill-accent: ${escapeHtml(skill.brandColor)}">
  <header class="shell topbar">
    <a class="wordmark" href="/" aria-label="Agent Skills home" data-aria-en="Agent Skills home" data-aria-zh="Agent Skills 首页">Agent Skills<span>.</span></a>
    <nav aria-label="Primary navigation" data-aria-en="Primary navigation" data-aria-zh="主导航">
      <a href="/#catalog" data-en="Catalog" data-zh="技能目录">Catalog</a>
      <a href="/#usage" data-en="How to use" data-zh="如何使用">How to use</a>
      <a class="nav-github" href="${repositoryUrl}">GitHub <span aria-hidden="true">↗</span></a>
      <button class="theme-toggle" type="button" data-theme-toggle aria-label="Use light mode" title="Use light mode">
        <span data-theme-icon aria-hidden="true">☀</span>
      </button>
      <div class="language-switch" role="group" aria-label="Language" data-aria-en="Language" data-aria-zh="语言">
        <button class="button" type="button" data-lang="en">EN</button>
        <button class="button" type="button" data-lang="zh">中文</button>
      </div>
    </nav>
  </header>

  <main class="shell detail-main">
    <section class="detail-hero">
      <a class="breadcrumb" href="/" data-en="← Back to catalog" data-zh="← 返回技能目录">← Back to catalog</a>
      <p class="eyebrow">$${escapeHtml(skill.slug)}</p>
      <h1 data-en="${escapeHtml(skill.displayName)}" data-zh="${escapeHtml(zh.displayName)}">${escapeHtml(skill.displayName)}</h1>
      <p id="skill-description" class="detail-description" data-en="${escapeHtml(skill.description)}" data-zh="${escapeHtml(zh.description)}">${escapeHtml(skill.description)}</p>
      <div class="detail-meta">
        <span class="pill" data-en="${escapeHtml(implicitEn)}" data-zh="${escapeHtml(implicitZh)}">${escapeHtml(implicitEn)}</span>
        <span class="pill"><span data-en="Config:" data-zh="配置：">Config:</span> <code>agents/openai.yaml</code></span>
      </div>
      <div class="detail-actions">
        <a class="button button-primary" href="#start" data-en="Use this skill" data-zh="使用此 Skill">Use this skill</a>
        <a class="button" href="${sourceUrl}" data-en="Open SKILL.md ↗" data-zh="打开 SKILL.md ↗">Open SKILL.md ↗</a>
        <a class="button" href="${agentUrl}" data-en="Open agent config ↗" data-zh="打开 Agent 配置 ↗">Open agent config ↗</a>
      </div>
    </section>

    <section id="start" class="detail-usage" aria-labelledby="start-heading">
      <div class="detail-section-head">
        <div>
          <p class="eyebrow" data-en="Start here" data-zh="从这里开始">Start here</p>
          <h2 id="start-heading" data-en="Install and invoke" data-zh="安装与调用">Install and invoke</h2>
        </div>
        <p data-en="The commands and prompt below are generated from this repository’s current skill metadata." data-zh="下方命令和调用示例由当前仓库中的 Skill 元数据生成，并与仓库保持同步。">The commands and prompt below are generated from this repository’s current skill metadata.</p>
      </div>
      <div class="action-grid">
        <article class="action-card">
          <h3 data-en="Install for Codex" data-zh="安装到 Codex">Install for Codex</h3>
          <p data-en="Install the skill at user scope so it is discoverable from any Codex project." data-zh="将 Skill 安装到用户级，使它能在任意 Codex 项目中被发现。">Install the skill at user scope so it is discoverable from any Codex project.</p>
          <div class="command">
            <pre id="install-command"><code>${escapeHtml(installCommand)}</code></pre>
            <button class="copy-button" type="button" data-copy-target="install-command" data-en="Copy" data-zh="复制">Copy</button>
          </div>
          <p class="product-note"><span data-en="Already cloned the repository? Run only" data-zh="已经克隆仓库？只需运行">Already cloned the repository? Run only</span> <code>./scripts/link-skills.sh ${escapeHtml(skill.slug)}</code><span data-en="." data-zh="。">.</span></p>
        </article>
        <article class="action-card">
          <h3 data-en="Invoke explicitly" data-zh="显式调用">Invoke explicitly</h3>
          <p data-en="Use the skill name in Codex, or adapt this default prompt for the task at hand." data-zh="在 Codex 中使用 Skill 名称调用，或根据当前任务调整下面的默认提示。">Use the skill name in Codex, or adapt this default prompt for the task at hand.</p>
          <div class="command">
            <pre id="invoke-command"><code data-en="${escapeHtml(skill.defaultPrompt)}" data-zh="${escapeHtml(zh.examplePrompt)}">${escapeHtml(skill.defaultPrompt)}</code></pre>
            <button class="copy-button" type="button" data-copy-target="invoke-command" data-en="Copy" data-zh="复制">Copy</button>
          </div>
          <p class="product-note"><span data-en="In ChatGPT, select" data-zh="在 ChatGPT 中，从 Skills 选择器选择">In ChatGPT, select</span> <strong data-en="${escapeHtml(skill.displayName)}" data-zh="${escapeHtml(zh.displayName)}">${escapeHtml(skill.displayName)}</strong> <span data-en="from the Skills picker when available. Matching requests may also select it automatically when implicit invocation is enabled." data-zh="（如可用）。启用自动调用时，匹配的请求也可能自动选择它。">from the Skills picker when available. Matching requests may also select it automatically when implicit invocation is enabled.</span></p>
        </article>
      </div>
    </section>

    <section class="contract" aria-labelledby="contract-heading">
      <div class="contract-grid">
        <aside class="contract-aside">
          <p class="eyebrow" data-en="Operating contract" data-zh="工作契约">Operating contract</p>
          <h2 id="contract-heading">SKILL.md</h2>
          <p data-en="This is the skill’s repository instruction body, rendered directly from the canonical English source used by ChatGPT and Codex." data-zh="以下为官网维护的 SKILL.md 中文镜像译文；英文源文件仍是 ChatGPT 与 Codex 使用的规范事实源。">This is the skill’s repository instruction body, rendered directly from the canonical English source used by ChatGPT and Codex.</p>
        </aside>
        <article class="markdown" data-contract-lang="en">${renderMarkdown(skill.body, skill.slug)}</article>
        <article class="markdown" data-contract-lang="zh" hidden>${renderMarkdown(zh.bodyMarkdown, skill.slug)}</article>
      </div>
    </section>
  </main>

  <footer class="shell footer">
    <span><span data-en="Generated from" data-zh="生成自">Generated from</span> <code>${escapeHtml(skill.source)}</code> <span data-en="and" data-zh="与">and</span> <code>${escapeHtml(skill.agentSource)}</code><span data-en="." data-zh="。">.</span></span>
    <a href="${repositoryUrl}" data-en="View repository ↗" data-zh="查看仓库 ↗">View repository ↗</a>
  </footer>
  <script src="/lang.js"></script>
  <script src="/detail.js" defer></script>
</body>
</html>
`;
}

function renderSitemap(skills) {
  const urls = [
    `${publicUrl}/`,
    ...skills.map((skill) => `${publicUrl}/skills/${encodeURIComponent(skill.slug)}/`)
  ];
  return `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.map((url) => `  <url><loc>${escapeXml(url)}</loc></url>`).join("\n")}\n</urlset>\n`;
}

const localization = JSON.parse(await readFile(localizationFile, "utf8"));
if (localization.locale !== "zh-CN" || !localization.skills || typeof localization.skills !== "object" || Array.isArray(localization.skills)) {
  throw new Error(`${localizationFile} must define locale zh-CN and a skills mapping`);
}

const entries = await readdir(skillsDir, { withFileTypes: true });
const skillEntries = entries.filter((item) => item.isDirectory()).sort((a, b) => a.name.localeCompare(b.name));
const skills = [];

for (const entry of skillEntries) {
  const skillFile = path.join(skillsDir, entry.name, "SKILL.md");
  const agentFile = path.join(skillsDir, entry.name, "agents", "openai.yaml");
  const source = await readFile(skillFile, "utf8");
  const agentSource = await readFile(agentFile, "utf8");
  const { frontmatter, body } = parseFrontmatter(source);
  const agent = parseYamlMapping(agentSource, agentFile);

  if (frontmatter.name !== entry.name) throw new Error(`${skillFile} name must match directory ${entry.name}`);
  if (typeof frontmatter.description !== "string" || !frontmatter.description.trim()) {
    throw new Error(`${skillFile} is missing description`);
  }
  if (!body) throw new Error(`${skillFile} instructions are empty`);

  const interfaceConfig = agent.interface;
  const policyConfig = agent.policy ?? {};
  if (!interfaceConfig || typeof interfaceConfig !== "object" || Array.isArray(interfaceConfig)) {
    throw new Error(`${agentFile} is missing interface metadata`);
  }

  const displayName = interfaceConfig.display_name;
  const shortDescription = interfaceConfig.short_description;
  const brandColor = interfaceConfig.brand_color;
  const defaultPrompt = interfaceConfig.default_prompt;
  const allowImplicitInvocation = policyConfig.allow_implicit_invocation === true;
  if (![displayName, shortDescription, brandColor, defaultPrompt].every((value) => typeof value === "string" && value.trim())) {
    throw new Error(`${agentFile} is missing required interface metadata`);
  }
  if (!/^#[0-9a-fA-F]{6}$/.test(brandColor)) throw new Error(`${agentFile} has an invalid brand_color`);
  if (!defaultPrompt.includes(`$${entry.name}`)) throw new Error(`${agentFile} default_prompt must explicitly invoke $${entry.name}`);

  const zh = localization.skills[entry.name];
  if (!zh || typeof zh !== "object" || Array.isArray(zh)) {
    throw new Error(`${localizationFile} is missing localization for ${entry.name}`);
  }
  for (const field of ["displayName", "shortDescription", "description", "examplePrompt", "bodyMarkdown"]) {
    if (typeof zh[field] !== "string" || !zh[field].trim()) {
      throw new Error(`${localizationFile} localization for ${entry.name} is missing ${field}`);
    }
  }
  if (!zh.examplePrompt.includes(`$${entry.name}`) || !zh.bodyMarkdown.includes(`$${entry.name}`)) {
    throw new Error(`${localizationFile} invocation copy for ${entry.name} must invoke $${entry.name}`);
  }

  skills.push({
    slug: entry.name,
    name: frontmatter.name,
    displayName,
    shortDescription,
    description: frontmatter.description,
    brandColor,
    defaultPrompt,
    allowImplicitInvocation,
    body,
    source: `skills/${entry.name}/SKILL.md`,
    agentSource: `skills/${entry.name}/agents/openai.yaml`,
    localized: { "zh-CN": zh }
  });
}

const expectedSlugs = skillEntries.map((entry) => entry.name).sort();
const localizedSlugs = Object.keys(localization.skills).sort();
if (JSON.stringify(expectedSlugs) !== JSON.stringify(localizedSlugs)) {
  throw new Error(`${localizationFile} skill keys must exactly match skills/: expected ${expectedSlugs.join(", ")}; found ${localizedSlugs.join(", ")}`);
}

await rm(distDir, { recursive: true, force: true });
await mkdir(distDir, { recursive: true });
await cp(siteDir, distDir, { recursive: true });
await writeFile(path.join(distDir, "skills.json"), `${JSON.stringify({ skills }, null, 2)}\n`);
await writeFile(path.join(distDir, "health.json"), `${JSON.stringify({
  status: "ok",
  skills: skills.length,
  revision: process.env.DEPLOY_REVISION || process.env.GITHUB_SHA || "development"
}, null, 2)}\n`);
await writeFile(path.join(distDir, "sitemap.xml"), renderSitemap(skills));

for (const skill of skills) {
  const detailDir = path.join(distDir, "skills", skill.slug);
  await mkdir(detailDir, { recursive: true });
  await writeFile(path.join(detailDir, "index.html"), renderSkillPage(skill));
}

console.log(`Built deterministic bilingual Agent Skills catalog with ${skills.length} skill(s).`);
