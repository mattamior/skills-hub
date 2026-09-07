const language = window.skillsHubLanguage;
const localizationSource = document.querySelector("#skill-localization");
const localized = localizationSource ? JSON.parse(localizationSource.textContent) : null;
const escapeHtml = (value) => String(value)
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;")
  .replaceAll("'", "&#039;");

if (!language || !localized) throw new Error("Bilingual detail runtime is not initialized");

function pair(element, en, zh) {
  if (!element) return;
  element.dataset.en = en;
  element.dataset.zh = zh;
}

const nav = document.querySelector(".topbar nav");
const navLinks = [...document.querySelectorAll(".topbar nav > a")];
const wordmark = document.querySelector(".wordmark");
const breadcrumb = document.querySelector(".breadcrumb");
const pills = [...document.querySelectorAll(".detail-meta .pill")];
const actionLinks = [...document.querySelectorAll(".detail-actions .button")];
const sectionHead = document.querySelector(".detail-section-head");
const actionCards = [...document.querySelectorAll(".action-card")];
const contractAside = document.querySelector(".contract-aside");
const footer = document.querySelector(".footer");
const description = document.querySelector("#skill-description") || document.querySelector(".detail-description");
const prompt = document.querySelector("#invoke-command code");
const metaDescription = document.querySelector('meta[name="description"]');
const copyButtons = [...document.querySelectorAll("[data-copy-target]")];

if (wordmark) {
  wordmark.dataset.ariaEn = "Agent Skills home";
  wordmark.dataset.ariaZh = "Agent Skills 首页";
}
if (nav) {
  nav.dataset.ariaEn = "Primary navigation";
  nav.dataset.ariaZh = "主导航";
}
pair(navLinks[0], "Catalog", "技能目录");
pair(navLinks[1], "How to use", "如何使用");
pair(breadcrumb, "← Back to catalog", "← 返回目录");

const implicitAllowed = pills[0]?.textContent.includes("Automatic");
pair(pills[0], implicitAllowed ? "Automatic selection allowed" : "Explicit invocation only", implicitAllowed ? "允许自动选择" : "仅显式调用");

pair(actionLinks[0], "Use this skill", "使用此 Skill");
pair(actionLinks[1], "Open SKILL.md ↗", "打开 SKILL.md ↗");
pair(actionLinks[2], "Open agent config ↗", "打开 Agent 配置 ↗");

pair(sectionHead?.querySelector(".eyebrow"), "Start here", "从这里开始");
pair(sectionHead?.querySelector("h2"), "Install and invoke", "安装与调用");
pair(sectionHead?.querySelector(":scope > p"), "The commands and prompt below are generated from this repository’s current skill metadata.", "下方命令和调用示例由当前仓库内容生成，并与仓库保持同步。");

pair(actionCards[0]?.querySelector("h3"), "Install for Codex", "安装到 Codex");
pair(actionCards[0]?.querySelector(":scope > p:not(.product-note)"), "Install the skill at user scope so it is discoverable from any Codex project.", "将 Skill 安装到用户级，使它能在任意 Codex 项目中被发现。");
pair(actionCards[1]?.querySelector("h3"), "Invoke explicitly", "显式调用");
pair(actionCards[1]?.querySelector(":scope > p:not(.product-note)"), "Use the skill name in Codex, or adapt this default prompt for the task at hand.", "在 Codex 中使用 Skill 名称调用；中文模式展示 README.zh.md 中维护的中文调用示例。");

pair(contractAside?.querySelector(".eyebrow"), "Operating contract", "工作契约");
pair(contractAside?.querySelector("p:last-child"), "This is the skill’s repository instruction body, rendered directly from the same source used by ChatGPT and Codex.", "以下是仓库中的原始 SKILL.md 指令正文（英文），直接来自 ChatGPT 与 Codex 使用的同一事实源。");
pair(footer?.querySelector("a"), "View repository ↗", "查看仓库 ↗");

const installNote = actionCards[0]?.querySelector(".product-note");
const installCommand = installNote?.querySelector("code")?.textContent || "";
const chatgptNote = actionCards[1]?.querySelector(".product-note");
const skillName = chatgptNote?.querySelector("strong")?.textContent || "";
const sourcePaths = [...(footer?.querySelectorAll("code") || [])].map((node) => node.textContent);

let currentLanguage = language.init();

function copyLabel(state = "copy") {
  const labels = currentLanguage === "zh"
    ? { copy: "复制", copied: "已复制", fallback: "选择并复制" }
    : { copy: "Copy", copied: "Copied", fallback: "Select & copy" };
  return labels[state];
}

function renderDynamic() {
  const data = currentLanguage === "zh" ? localized.zh : localized.en;
  if (description && data.description) description.textContent = data.description;
  if (prompt && data.prompt) prompt.textContent = data.prompt;
  if (metaDescription && data.description) metaDescription.setAttribute("content", data.description);

  if (pills[1]) {
    pills[1].innerHTML = currentLanguage === "zh"
      ? `配置： <code>agents/openai.yaml</code>`
      : `Config: <code>agents/openai.yaml</code>`;
  }
  if (installNote) {
    installNote.innerHTML = currentLanguage === "zh"
      ? `已经克隆仓库？只需运行 <code>${escapeHtml(installCommand)}</code>。`
      : `Already cloned the repository? Run only <code>${escapeHtml(installCommand)}</code>.`;
  }
  if (chatgptNote) {
    chatgptNote.innerHTML = currentLanguage === "zh"
      ? `在 ChatGPT 中，从 Skills 选择器选择 <strong>${escapeHtml(skillName)}</strong>（如可用）。启用自动调用时，匹配的请求也可能自动选择它。`
      : `In ChatGPT, select <strong>${escapeHtml(skillName)}</strong> from the Skills picker when available. Matching requests may also select it automatically when implicit invocation is enabled.`;
  }
  if (footer && sourcePaths.length >= 2) {
    const prefix = currentLanguage === "zh" ? "生成自" : "Generated from";
    const conjunction = currentLanguage === "zh" ? "与" : "and";
    const span = footer.querySelector("span");
    if (span) span.innerHTML = `${prefix} <code>${escapeHtml(sourcePaths[0])}</code> ${conjunction} <code>${escapeHtml(sourcePaths[1])}</code>.`;
  }

  for (const button of copyButtons) {
    if (!button.dataset.copyState || button.dataset.copyState === "copy") {
      button.dataset.copyState = "copy";
      button.textContent = copyLabel();
    }
  }
}

for (const button of copyButtons) {
  button.addEventListener("click", async () => {
    const target = document.getElementById(button.dataset.copyTarget);
    if (!target) return;
    const value = target.textContent.trim();
    try {
      await navigator.clipboard.writeText(value);
      button.dataset.copyState = "copied";
      button.textContent = copyLabel("copied");
    } catch {
      const range = document.createRange();
      range.selectNodeContents(target);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      button.dataset.copyState = "fallback";
      button.textContent = copyLabel("fallback");
    }
    window.setTimeout(() => {
      button.dataset.copyState = "copy";
      button.textContent = copyLabel();
    }, 1800);
  });
}

language.subscribe((nextLanguage) => {
  currentLanguage = nextLanguage;
  for (const button of copyButtons) button.dataset.copyState = "copy";
  renderDynamic();
});
renderDynamic();
