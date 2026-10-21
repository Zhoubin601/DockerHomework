import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  timeout: 90000,
  expect: { timeout: 7000 },
  workers: 1,
  reporter: [['list']],
  use: {
    baseURL: process.env.GARDEN_TEST_URL || 'http://127.0.0.1:18080',
    headless: true,
    viewport: { width: 1440, height: 1100 },
    launchOptions: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ? { executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH } : {},
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },
})
