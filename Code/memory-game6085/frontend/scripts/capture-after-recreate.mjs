import { chromium } from '@playwright/test'
import { readFile } from 'node:fs/promises'
import path from 'node:path'

const evidence = path.resolve('../../..', 'docs/docker-evidence')
const before = JSON.parse(await readFile(path.join(evidence, 'before-leaderboard.json'), 'utf8'))
const after = await (await fetch('http://127.0.0.1:18085/api/leaderboard?difficulty=easy')).json()
if (JSON.stringify(before) !== JSON.stringify(after)) throw new Error('Scores changed after container recreation')
const browser = await chromium.launch({ headless: true, ...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ? { executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH } : {}) })
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1100 }, reducedMotion: 'reduce' })
  await page.goto('http://127.0.0.1:18085')
  await page.locator('.rank-tabs').getByRole('button', { name: '轻松' }).click()
  await page.locator('.ranking-list').getByText('6085实验').waitFor()
  await page.screenshot({ path: path.join(evidence, '10-after-recreate-ui.png'), fullPage: true })
  console.log('Recreated container browser screenshot captured; exact saved leaderboard preserved.')
} finally { await browser.close() }
