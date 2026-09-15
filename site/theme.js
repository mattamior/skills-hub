(() => {
  const STORAGE_KEY = "skills-hub-theme";
  const DARK = "dark";
  const LIGHT = "light";
  const root = document.documentElement;
  const media = window.matchMedia("(prefers-color-scheme: dark)");

  function storedTheme() {
    try {
      const value = localStorage.getItem(STORAGE_KEY);
      return value === DARK || value === LIGHT ? value : null;
    } catch {
      return null;
    }
  }

  function preferredTheme() {
    return media.matches ? DARK : LIGHT;
  }

  function currentTheme() {
    return root.dataset.theme === LIGHT ? LIGHT : DARK;
  }

  function isChinese() {
    return String(root.lang || "").toLowerCase().startsWith("zh");
  }

  function controlLabel(theme) {
    if (theme === DARK) return isChinese() ? "切换到亮色模式" : "Use light mode";
    return isChinese() ? "切换到暗色模式" : "Use dark mode";
  }

  function syncControls(theme) {
    const label = controlLabel(theme);
    for (const button of document.querySelectorAll("[data-theme-toggle]")) {
      button.setAttribute("aria-label", label);
      button.setAttribute("title", label);
      button.dataset.themeCurrent = theme;
      const icon = button.querySelector("[data-theme-icon]");
      if (icon) icon.textContent = theme === DARK ? "☀" : "☾";
    }
  }

  function syncThemeColor(theme) {
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", theme === DARK ? "#090a09" : "#f6f7f2");
  }

  function apply(theme, persist = true) {
    const normalized = theme === LIGHT ? LIGHT : DARK;
    root.dataset.theme = normalized;
    root.style.colorScheme = normalized;
    syncThemeColor(normalized);
    syncControls(normalized);
    if (persist) {
      try {
        localStorage.setItem(STORAGE_KEY, normalized);
      } catch {}
    }
    return normalized;
  }

  function toggle() {
    return apply(currentTheme() === DARK ? LIGHT : DARK);
  }

  function wireControls() {
    for (const button of document.querySelectorAll("[data-theme-toggle]")) {
      if (button.dataset.themeWired === "true") continue;
      button.dataset.themeWired = "true";
      button.addEventListener("click", toggle);
    }
    syncControls(currentTheme());
  }

  apply(storedTheme() || preferredTheme(), false);

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wireControls, { once: true });
  } else {
    wireControls();
  }

  media.addEventListener?.("change", (event) => {
    if (!storedTheme()) apply(event.matches ? DARK : LIGHT, false);
  });

  new MutationObserver(() => syncControls(currentTheme())).observe(root, {
    attributes: true,
    attributeFilter: ["lang"]
  });

  window.skillsHubTheme = {
    get: currentTheme,
    set: apply,
    toggle
  };
})();
