const source = document.querySelector("#gallery-source").textContent.trim();
const grid = document.querySelector("#skill-grid");
const count = document.querySelector("#skill-count");
const search = document.querySelector("#search");
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

function render(query = "") {
  const normalized = query.trim().toLowerCase();
  const filtered = skills.filter((skill) => [
    skill.slug,
    skill.displayName,
    skill.shortDescription,
    skill.description,
    skill.defaultPrompt,
    skill.body,
    skill.localized?.["zh-CN"]?.shortDescription,
    skill.localized?.["zh-CN"]?.description,
    skill.localized?.["zh-CN"]?.examplePrompt
  ].filter(Boolean).join(" ").toLowerCase().includes(normalized));

  grid.replaceChildren();
  filtered.forEach((skill, index) => {
    const locale = localized(skill);
    const card = document.createElement("a");
    card.className = "skill-card";
    card.href = `/skills/${encodeURIComponent(skill.slug)}/`;
    card.setAttribute("aria-label", cardAriaLabel(skill.displayName));
    card.innerHTML = `
      <span class="card-index">${String(index + 1).padStart(2, "0")}</span>
      <span class="card-arrow" aria-hidden="true">↗</span>
      <div class="card-copy">
        <span class="card-slug">$${escapeHtml(skill.slug)}</span>
        <h3>${escapeHtml(skill.displayName)}</h3>
        <p>${escapeHtml(locale.shortDescription || skill.shortDescription)}</p>
      </div>`;
    grid.append(card);
  });
  empty.hidden = filtered.length !== 0;
}

search.addEventListener("input", () => render(search.value));
language.subscribe((nextLanguage) => {
  currentLanguage = nextLanguage;
  render(search.value);
});
render();
