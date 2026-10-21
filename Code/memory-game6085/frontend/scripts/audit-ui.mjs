import { chromium } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'
import { mkdir, writeFile } from 'node:fs/promises'

const root = process.env.GARDEN_TEST_URL || 'http://127.0.0.1:18080'
const browser = await chromium.launch({
  headless: true,
  ...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ? { executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH } : {}),
})
const context = await browser.newContext({ reducedMotion: 'reduce' })
const page = await context.newPage()
const audit = []
await mkdir('test-results/review', { recursive: true })
async function inspect(name, width, height) {
  const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']).analyze()
  const overflow = await page.evaluate(() => ({ actual: document.documentElement.scrollWidth, viewport: innerWidth }))
  await page.screenshot({ path: `test-results/review/${name}.png`, fullPage: true })
  audit.push({ name, width, height, overflow, violations: result.violations.map(item => ({ id: item.id, impact: item.impact, description: item.description, nodes: item.nodes.map(node => ({ target: node.target, summary: node.failureSummary })) })) })
  console.log(`${name}: ${result.violations.length} axe violations; width ${overflow.actual}/${overflow.viewport}`)
}
try {
  for (const [name, width, height] of [['desktop', 1440, 1100], ['tablet', 768, 1024], ['mobile', 375, 812], ['landscape', 812, 375], ['small', 320, 740]]) {
    await page.setViewportSize({ width, height })
    await page.goto(root)
    await page.waitForFunction(() => !document.querySelector('.leaderboard .spin'))
    await inspect(name, width, height)
  }
  await page.setViewportSize({ width: 375, height: 812 })
  await page.getByRole('button', { name: '玩法指南' }).click()
  await inspect('rules-dialog', 375, 812)
  await page.keyboard.press('Escape')
  await page.setViewportSize({ width: 1440, height: 1100 })
  await page.getByRole('button', { name: '开始翻牌' }).click()
  await page.waitForFunction(() => document.querySelector('.card-grid')?.getAttribute('aria-busy') === 'false' && !document.querySelector('.board-overlay'))
  const flipped = page.waitForResponse(response => response.url().endsWith('/flip') && response.request().method() === 'POST')
  await page.locator('.game-card').first().press('Enter')
  await flipped
  await page.locator('.game-card.revealed').first().waitFor()
  await inspect('playing', 1440, 1100)
  await page.getByRole('button', { name: '暂停游戏', exact: true }).click()
  await inspect('paused', 1440, 1100)
  await writeFile('test-results/review/ui-audit.json', JSON.stringify(audit, null, 2))
  if (audit.some(item => item.violations.length || item.overflow.actual > item.overflow.viewport)) process.exitCode = 1
} finally { await browser.close() }
