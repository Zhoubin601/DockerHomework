import { chromium } from '@playwright/test'
import { mkdir, writeFile } from 'node:fs/promises'
import path from 'node:path'

const mode = process.argv[2] || 'before'
const evidence = path.resolve(process.env.GARDEN_EVIDENCE_DIR || '../../../docs/v3-evidence')
const base = process.env.GARDEN_DEMO_URL || 'http://127.0.0.1:18086'
await mkdir(evidence, { recursive: true })
const browser = await chromium.launch({ headless: true, executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH || '/usr/bin/chromium', args: ['--no-sandbox'] })
const context = await browser.newContext({ viewport: { width: 1440, height: 1100 }, reducedMotion: 'reduce' })
const page = await context.newPage()
const errors = []
page.on('pageerror', error => errors.push(error.message))
try {
  await page.goto(base)
  await page.waitForFunction(() => !document.querySelector('.leaderboard .spin'))
  if (mode === 'before') {
    await page.screenshot({ path: path.join(evidence, 'desktop-v3.png'), fullPage: true })
    const mobile = await context.newPage()
    await mobile.setViewportSize({ width: 375, height: 812 })
    await mobile.goto(base)
    await mobile.waitForFunction(() => !document.querySelector('.leaderboard .spin'))
    const overflow = await mobile.evaluate(() => document.documentElement.scrollWidth > innerWidth)
    if (overflow) throw new Error('Mobile viewport overflows horizontally')
    await mobile.screenshot({ path: path.join(evidence, 'mobile-v3.png'), fullPage: true })
    await mobile.close()
    await page.getByRole('group', { name: '游戏难度' }).getByRole('button', { name: /轻松/ }).click()
    await page.getByRole('button', { name: '开始翻牌' }).click()
    await page.waitForFunction(() => document.querySelector('.card-grid')?.getAttribute('aria-busy') === 'false' && !document.querySelector('.board-overlay'))
    const known = new Map()
    for (let index = 0; index < 12; index += 2) {
      for (const position of [index, index + 1]) {
        const response = page.waitForResponse(r => r.url().endsWith('/flip') && r.request().method() === 'POST')
        await page.locator('.game-card').nth(position).click()
        const state = await (await response).json()
        known.set(state.cards[position].symbol, [...(known.get(state.cards[position].symbol) || []), position])
        if (state.lockedForMs > 0) await page.waitForFunction(() => !document.querySelector('.game-card.revealed:not(.matched)'))
      }
    }
    for (const pair of known.values()) {
      if ((await page.locator('.game-card').nth(pair[0]).getAttribute('class')).includes('matched')) continue
      for (const position of pair) {
        const response = page.waitForResponse(r => r.url().endsWith('/flip') && r.request().method() === 'POST')
        await page.locator('.game-card').nth(position).click()
        await response
      }
    }
    await page.getByRole('dialog', { name: '你的花园，开花了。' }).waitFor()
    await page.getByLabel('给这份好心情留个名字').fill('6085v3实验')
    const submitted = page.waitForResponse(r => r.url().endsWith('/score') && r.request().method() === 'POST')
    await page.getByRole('button', { name: '保存到花园榜单' }).click()
    const score = await (await submitted).json()
    await page.getByText('成绩已保存，花园记住了你的名字。').waitFor()
    await page.screenshot({ path: path.join(evidence, '05-game-saved.png') })
    await writeFile(path.join(evidence, 'saved-score.json'), JSON.stringify(score, null, 2))
    console.log('Actual v3 container game completed:', JSON.stringify(score))
  } else {
    await page.getByRole('group', { name: '排行榜难度' }).getByRole('button', { name: '轻松', exact: true }).click()
    await page.getByText('6085v3实验', { exact: true }).waitFor()
    await page.screenshot({ path: path.join(evidence, '10-after-recreate-ui.png'), fullPage: true })
  }
  if (errors.length) throw new Error(errors.join('\n'))
  await writeFile(path.join(evidence, `browser-${mode}.json`), JSON.stringify({ base, mode, capturedAt: new Date().toISOString(), pageErrors: errors, result: 'passed' }, null, 2))
} finally { await browser.close() }
