const language = window.skillsHubLanguage;
const contracts = [...document.querySelectorAll("[data-contract-lang]")];
const copyButtons = [...document.querySelectorAll("[data-copy-target]")];

if (!language) throw new Error("Bilingual detail runtime is not initialized");

let currentLanguage = "en";

function copyLabel(state = "copy") {
  const labels = currentLanguage === "zh"
    ? { copy: "复制", copied: "已复制", fallback: "选择并复制" }
    : { copy: "Copy", copied: "Copied", fallback: "Select & copy" };
  return labels[state];
}

function renderContracts() {
  for (const contract of contracts) {
    contract.hidden = contract.dataset.contractLang !== currentLanguage;
  }
}

function resetCopyButtons() {
  for (const button of copyButtons) {
    button.dataset.copyState = "copy";
    button.textContent = copyLabel();
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
  renderContracts();
  resetCopyButtons();
});

currentLanguage = language.init();
renderContracts();
resetCopyButtons();
