import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/browser",
  fullyParallel: false,
  retries: 0,
  workers: 1,
  reporter: "line",
  use: {
    baseURL: "http://127.0.0.1:4173",
    headless: true,
    trace: "retain-on-failure"
  },
  webServer: {
    command: "node scripts/serve-dist.mjs",
    url: "http://127.0.0.1:4173/health.json",
    reuseExistingServer: false,
    timeout: 10000
  }
});
