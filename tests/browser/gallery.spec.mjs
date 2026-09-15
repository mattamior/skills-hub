import { expect, test } from "@playwright/test";

test("catalog discovery, search shortcuts, and complete language preference work in a real browser", async ({ page }) => {
  await page.goto("/");
  const catalog = await page.evaluate(async () => (await fetch("/skills.json")).json());

  await expect(page.locator("#skill-count")).toHaveText(String(catalog.skills.length));
  await expect(page.locator(".skill-card")).toHaveCount(catalog.skills.length);
  await expect(page.locator("#catalog-status")).toHaveText(`Showing ${catalog.skills.length} of ${catalog.skills.length} skills`);
  await expect(page.locator(".policy-badge")).toHaveCount(catalog.skills.length);
  await expect(page.locator(".product-chip")).toHaveCount(catalog.skills.length);

  await page.keyboard.press("/");
  await expect(page.locator("#search")).toBeFocused();
  await page.locator("#search").fill("pet-avatar-generation");
  await expect(page.locator(".skill-card")).toHaveCount(1);
  await expect(page.locator(".skill-card")).toContainText("Pet Avatar Generation");
  await expect(page.locator("#catalog-status")).toHaveText(`Showing 1 of ${catalog.skills.length} skills`);
  await expect(page.locator("#search-clear")).toBeVisible();

  await page.locator("#search-clear").click();
  await expect(page.locator(".skill-card")).toHaveCount(catalog.skills.length);
  await expect(page.locator("#search")).toHaveValue("");

  await page.getByRole("button", { name: "中文" }).click();
  await expect(page.locator("html")).toHaveAttribute("lang", "zh-CN");
  await expect(page.locator("#search")).toHaveAttribute("placeholder", "搜索 Skills…");
  await expect(page.locator("#catalog-status")).toHaveText(`显示 ${catalog.skills.length} / ${catalog.skills.length} 个 Skills`);
  await expect(page.getByRole("heading", { level: 3, name: "宠物头像生成" })).toBeVisible();
  await expect(page.getByRole("heading", { level: 3, name: "品牌设计系统" })).toBeVisible();
  expect(await page.evaluate(() => localStorage.getItem("skills-hub-language"))).toBe("zh");

  await page.locator("#search").fill("保留宠物身份特征");
  await expect(page.locator(".skill-card")).toHaveCount(1);
  await expect(page.locator(".skill-card h3")).toHaveText("宠物头像生成");
  await page.locator("#search-clear").click();

  await page.reload();
  await expect(page.locator("html")).toHaveAttribute("lang", "zh-CN");
  await expect(page.locator("#search")).toHaveAttribute("placeholder", "搜索 Skills…");
  await expect(page.getByRole("heading", { level: 3, name: "宠物头像生成" })).toBeVisible();
  await expect(page.locator(".hero-panel")).toBeVisible();
});

test("light and dark theme preference persists across site surfaces", async ({ page }) => {
  await page.goto("/");
  await page.evaluate(() => localStorage.setItem("skills-hub-theme", "dark"));
  await page.reload();

  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await expect(page.locator('link[rel="canonical"]')).toHaveAttribute("href", "https://skills-hub.lapplax.com/");
  const homeThemeToggle = page.locator("[data-theme-toggle]").first();
  await expect(homeThemeToggle).toHaveAttribute("aria-label", "Use light mode");

  await homeThemeToggle.click();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  await expect(page.locator('meta[name="theme-color"]')).toHaveAttribute("content", "#f6f7f2");
  expect(await page.evaluate(() => localStorage.getItem("skills-hub-theme"))).toBe("light");

  await page.goto("/skills/pet-avatar-generation/");
  await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  await expect(page.locator('link[rel="canonical"]')).toHaveAttribute("href", "https://skills-hub.lapplax.com/skills/pet-avatar-generation/");
  await expect(page.locator("[data-theme-toggle]").first()).toHaveAttribute("aria-label", "Use dark mode");

  await page.getByRole("button", { name: "中文" }).click();
  await expect(page.locator("[data-theme-toggle]").first()).toHaveAttribute("aria-label", "切换到暗色模式");

  const response = await page.goto("/this-route-does-not-exist");
  expect(response?.status()).toBe(404);
  await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  await expect(page.locator("[data-theme-toggle]").first()).toHaveAttribute("aria-label", "切换到暗色模式");
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("页面不存在");
});

test("skill detail fully localizes and copy interaction preserves the localized invocation", async ({ page, context }) => {
  await context.grantPermissions(["clipboard-read", "clipboard-write"], { origin: "http://127.0.0.1:4173" });
  await page.goto("/skills/pet-avatar-generation/");

  await expect(page.locator(".detail-hero h1")).toHaveText("Pet Avatar Generation");
  await expect(page.locator("#skill-description")).toContainText("Create or refine stylized avatar images");
  await expect(page.locator('article.markdown[data-contract-lang="en"]')).toContainText("Preserve pet identity");
  await expect(page.locator('article.markdown[data-contract-lang="zh"]')).toBeHidden();

  await page.getByRole("button", { name: "中文" }).click();
  await expect(page.locator("html")).toHaveAttribute("lang", "zh-CN");
  await expect(page).toHaveTitle("宠物头像生成 — Agent Skills");
  await expect(page.locator(".detail-hero h1")).toHaveText("宠物头像生成");
  await expect(page.locator("#skill-description")).toContainText("不适用于人物头像");
  await expect(page.getByRole("heading", { level: 2, name: "安装与调用" })).toBeVisible();
  await expect(page.locator('article.markdown[data-contract-lang="en"]')).toBeHidden();
  const chineseContract = page.locator('article.markdown[data-contract-lang="zh"]');
  await expect(chineseContract).toBeVisible();
  await expect(chineseContract).toContainText("保留宠物身份特征");
  await expect(chineseContract).not.toContainText("Preserve pet identity");
  await expect(page.locator("#invoke-command code")).toContainText("把源图里的宠物做成三个明显不同的头像风格");

  const invokeCopy = page.locator('[data-copy-target="invoke-command"]');
  await invokeCopy.click();
  await expect(invokeCopy).toHaveText("已复制");
  const copied = await page.evaluate(() => navigator.clipboard.readText());
  expect(copied).toContain("$pet-avatar-generation");
  expect(copied).toContain("把源图里的宠物");
});

test("unknown routes use the fully localized branded 404 page", async ({ page }) => {
  const response = await page.goto("/this-route-does-not-exist");
  expect(response?.status()).toBe(404);
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("Page not found");
  await expect(page.locator('a.button-primary[href="/"]')).toHaveText("Back to catalog");
  await expect(page.locator("[data-theme-toggle]")).toBeVisible();

  await page.getByRole("button", { name: "中文" }).click();
  await expect(page).toHaveTitle("页面不存在 — Agent Skills");
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("页面不存在");
  await expect(page.locator('a.button-primary[href="/"]')).toHaveText("返回技能目录");
});
