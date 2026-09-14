import { expect, test } from "@playwright/test";

test("catalog search and language preference work in a real browser", async ({ page }) => {
  await page.goto("/");
  const catalog = await page.evaluate(async () => (await fetch("/skills.json")).json());

  await expect(page.locator("#skill-count")).toHaveText(String(catalog.skills.length));
  await expect(page.locator(".skill-card")).toHaveCount(catalog.skills.length);

  await page.locator("#search").fill("pet-avatar-generation");
  await expect(page.locator(".skill-card")).toHaveCount(1);
  await expect(page.locator(".skill-card")).toContainText("Pet Avatar Generation");

  await page.getByRole("button", { name: "中文" }).click();
  await expect(page.locator("html")).toHaveAttribute("lang", "zh-CN");
  await expect(page.locator("#search")).toHaveAttribute("placeholder", "搜索 Skills…");
  expect(await page.evaluate(() => localStorage.getItem("skills-hub-language"))).toBe("zh");

  await page.reload();
  await expect(page.locator("html")).toHaveAttribute("lang", "zh-CN");
  await expect(page.locator("#search")).toHaveAttribute("placeholder", "搜索 Skills…");
});

test("skill detail localizes and copy interaction preserves the invocation", async ({ page, context }) => {
  await context.grantPermissions(["clipboard-read", "clipboard-write"], { origin: "http://127.0.0.1:4173" });
  await page.goto("/skills/pet-avatar-generation/");

  await expect(page.getByRole("heading", { level: 1 })).toHaveText("Pet Avatar Generation");
  await expect(page.locator("#skill-description")).toContainText("Create or refine stylized avatar images");
  await expect(page.locator("article.markdown")).toContainText("Preserve pet identity");

  await page.getByRole("button", { name: "中文" }).click();
  await expect(page.locator("#skill-description")).toContainText("将真实宠物照片转成保持辨识度的风格化头像");

  const invokeCopy = page.locator('[data-copy-target="invoke-command"]');
  await invokeCopy.click();
  await expect(invokeCopy).toHaveText("已复制");
  expect(await page.evaluate(() => navigator.clipboard.readText())).toContain("$pet-avatar-generation");
});

test("unknown routes use the branded 404 page", async ({ page }) => {
  const response = await page.goto("/this-route-does-not-exist");
  expect(response?.status()).toBe(404);
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("Page not found");
  await expect(page.locator('a.button-primary[href="/"]')).toHaveText("Back to catalog");
});
