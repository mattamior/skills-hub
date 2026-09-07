(() => {
  const STORAGE_KEY = "skills-hub-language";
  const listeners = new Set();

  const normalize = (value) => String(value || "").toLowerCase().startsWith("zh") ? "zh" : "en";

  function storedLanguage() {
    try {
      const value = localStorage.getItem(STORAGE_KEY);
      return value === "en" || value === "zh" ? value : null;
    } catch {
      return null;
    }
  }

  function get() {
    return storedLanguage() || normalize(navigator.language);
  }

  function apply(language) {
    const suffix = language === "zh" ? "Zh" : "En";
    document.documentElement.lang = language === "zh" ? "zh-CN" : "en";

    for (const element of document.querySelectorAll("[data-en][data-zh]")) {
      element.textContent = language === "zh" ? element.dataset.zh : element.dataset.en;
    }
    for (const element of document.querySelectorAll("[data-placeholder-en][data-placeholder-zh]")) {
      element.setAttribute("placeholder", element.dataset[`placeholder${suffix}`]);
    }
    for (const element of document.querySelectorAll("[data-aria-en][data-aria-zh]")) {
      element.setAttribute("aria-label", element.dataset[`aria${suffix}`]);
    }
    for (const element of document.querySelectorAll("[data-content-en][data-content-zh]")) {
      element.setAttribute("content", element.dataset[`content${suffix}`]);
    }
    for (const button of document.querySelectorAll("[data-lang]")) {
      const active = button.dataset.lang === language;
      button.classList.toggle("button-primary", active);
      button.setAttribute("aria-pressed", String(active));
    }
  }

  function set(language, persist = true) {
    const normalized = normalize(language);
    if (persist) {
      try {
        localStorage.setItem(STORAGE_KEY, normalized);
      } catch {}
    }
    apply(normalized);
    for (const listener of listeners) listener(normalized);
    return normalized;
  }

  function subscribe(listener) {
    listeners.add(listener);
    return () => listeners.delete(listener);
  }

  function init() {
    for (const button of document.querySelectorAll("[data-lang]")) {
      button.addEventListener("click", () => set(button.dataset.lang));
    }
    return set(get(), false);
  }

  window.skillsHubLanguage = { get, set, subscribe, init };
})();
