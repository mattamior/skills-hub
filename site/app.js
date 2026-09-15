const source = document.querySelector("#gallery-source").textContent.trim();
const grid = document.querySelector("#skill-grid");
const count = document.querySelector("#skill-count");
const search = document.querySelector("#search");
const searchClear = document.querySelector("#search-clear");
const status = document.querySelector("#catalog-status");
const empty = document.querySelector("#empty-state");
const language = window.skillsHubLanguage;

let currentLanguage = language.init();

const escapeHtml = (value) => String(value)
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;")
  .replaceAll("'", "&#039;");

const response = await fetch(source);
if (!response.ok) throw new Error(`Unable to load gallery data: ${response.status}`);
const { skills } = await response.json();
count.textContent = skills.length;

function localized(skill) {
  if (currentLanguage === "zh") {
    return skill.localized?.["zh-CN"] || {};
  }
  return {};
}

function cardAriaLabel(name) {
  return currentLanguage === "zh" ? `打开 ${name}` : `Open ${name}`;
}

function policyLabel(skill) {
  if (skill.allowImplicitInvocation) {
    return currentLanguage === "zh" ? "可自动选择" : "Automatic";
  }
  return currentLanguage === "zh" ? "显式调用" : "Explicit";
}

function ctaLabel() {
  return currentLanguage === "zh" ? "查看 Skill" : "View skill";
}

function statusLabel(visible) {
  return currentLanguage === "zh"
    ? `显示 ${visible} / ${skills.length} 个 Skills`
    : `Showing ${visible} of ${skills.length} skills`;
}

function render(query = "") {
  const normalized = query.trim().toLowerCase();
  const filtered = skills.filter((skill) => [
    skill.slug,
    skill.displayName,
    skill.shortDescription,
    skill.description,
    skill.defaultPrompt,
    skill.body,
    skill.localized?.["zh-CN"]?.displayName,
    skill.localized?.["zh-CN"]?.shortDescription,
    skill.localized?.["zh-CN"]?.description,
    skill.localized?.["zh-CN"]?.examplePrompt,
    skill.localized?.["zh-CN"]?.bodyMarkdown
  ].filter(Boolean).join(" ").toLowerCase().includes(normalized));

  grid.replaceChildren();
  filtered.forEach((skill) => {
    const locale = localized(skill);
    const displayName = locale.displayName || skill.displayName;
    const ordinal = skills.indexOf(skill) + 1;
    const card = document.createElement("a");
    card.className = "skill-card";
    card.href = `/skills/${encodeURIComponent(skill.slug)}/`;
    card.setAttribute("aria-label", cardAriaLabel(displayName));
    card.style.setProperty("--skill-accent", skill.brandColor);
    card.innerHTML = `
      <div class="card-top">
        <span class="card-index">${String(ordinal).padStart(2, "0")}</span>
        <span class="policy-badge"><i aria-hidden="true"></i>${escapeHtml(policyLabel(skill))}</span>
      </div>
      <div class="card-copy">
        <span class="card-slug">$${escapeHtml(skill.slug)}</span>
        <h3>${escapeHtml(displayName)}</h3>
        <p>${escapeHtml(locale.shortDescription || skill.shortDescription)}</p>
      </div>
      <div class="card-footer">
        <span class="product-chip">ChatGPT · Codex</span>
        <span class="card-cta">${escapeHtml(ctaLabel())} <span aria-hidden="true">↗</span></span>
      </div>`;
    grid.append(card);
  });

  status.textContent = statusLabel(filtered.length);
  searchClear.hidden = search.value.length === 0;
  empty.hidden = filtered.length !== 0;
}

function clearSearch({ focus = true } = {}) {
  search.value = "";
  render();
  if (focus) search.focus();
}

search.addEventListener("input", () => render(search.value));
search.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") return;
  if (search.value) {
    event.preventDefault();
    clearSearch();
  } else {
    search.blur();
  }
});
searchClear.addEventListener("click", () => clearSearch());

document.addEventListener("keydown", (event) => {
  if (event.key !== "/" || event.metaKey || event.ctrlKey || event.altKey) return;
  const active = document.activeElement;
  const isTyping = active && (
    active.tagName === "INPUT" ||
    active.tagName === "TEXTAREA" ||
    active.isContentEditable
  );
  if (isTyping) return;
  event.preventDefault();
  search.focus();
});

language.subscribe((nextLanguage) => {
  currentLanguage = nextLanguage;
  render(search.value);
});
render();
