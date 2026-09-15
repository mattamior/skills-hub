import { expect, test } from "@playwright/test";

test("skill detail language runtime is cache-busted and switches both directions", async ({ page }) => {
  const pageErrors = [];
  page.on("pageerror", (error) => pageErrors.push(error.message));

  await page.goto("/skills/pet-avatar-generation/");

  const detailSrc = await page.locator('script[src^="/detail.js"]').getAttribute("src");
  const languageSrc = await page.locator('script[src^="/lang.js"]').getAttribute("src");
  const themeSrc = await page.locator('script[src^="/theme.js"]').getAttribute("src");
  const themeCss = await page.locator('link[href^="/theme.css"]').getAttribute("href");
  const stylesCss = await page.locator('link[href^="/styles.css"]').getAttribute("href");

  for (const assetUrl of [detailSrc, languageSrc, themeSrc, themeCss, stylesCss]) {
    expect(assetUrl).toMatch(/^\/(?:detail|lang|theme|styles)\.(?:js|css)\?v=[0-9a-f]{12}$/);
  }
  const versions = [detailSrc, languageSrc, themeSrc, themeCss, stylesCss]
    .map((assetUrl) => new URL(assetUrl, "http://127.0.0.1:4173").searchParams.get("v"));
  expect(new Set(versions).size).toBe(1);

  await expect(page.locator(".detail-hero h1")).toHaveText("Pet Avatar Generation");
  await expect(page.locator('article.markdown[data-contract-lang="en"]')).toBeVisible();
  await expect(page.locator('article.markdown[data-contract-lang="zh"]')).toBeHidden();

  await page.getByRole("button", { name: "中文" }).click();
  await expect(page.locator("html")).toHaveAttribute("lang", "zh-CN");
  await expect(page.locator(".detail-hero h1")).toHaveText("宠物头像生成");
  await expect(page.locator('article.markdown[data-contract-lang="en"]')).toBeHidden();
  await expect(page.locator('article.markdown[data-contract-lang="zh"]')).toBeVisible();

  await page.getByRole("button", { name: "EN" }).click();
  await expect(page.locator("html")).toHaveAttribute("lang", "en");
  await expect(page.locator(".detail-hero h1")).toHaveText("Pet Avatar Generation");
  await expect(page.locator('article.markdown[data-contract-lang="en"]')).toBeVisible();
  await expect(page.locator('article.markdown[data-contract-lang="zh"]')).toBeHidden();

  await page.getByRole("button", { name: "中文" }).click();
  await expect(page.locator(".detail-hero h1")).toHaveText("宠物头像生成");
  expect(pageErrors).toEqual([]);
});
