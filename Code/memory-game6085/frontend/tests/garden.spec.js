import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

test('桌面：真实翻牌、暂停、完整配对、验证昵称并保存排行榜', async ({ page }) => {
  const errors = []
  page.on('pageerror', error => errors.push(error.message))
  await page.goto('/')
  await expect(page.getByRole('heading', { name: '今天，也要好好玩。' })).toBeVisible()
  await expect(page.getByRole('heading', { name: '第一片叶子，等你种下' })).toBeVisible()
  await page.screenshot({ path: 'test-results/desktop-ready.png', fullPage: true })
  await page.getByRole('group', { name: '游戏难度' }).getByRole('button', { name: /轻松/ }).click()
  await page.getByRole('button', { name: '开始翻牌' }).click()
  await expect(page.locator('.game-card')).toHaveCount(12)
  await expect(page.locator('.game-card').first()).toBeFocused()
  const firstResponse = page.waitForResponse(response => response.url().endsWith('/flip') && response.request().method() === 'POST')
  await page.locator('.game-card').first().press('Enter')
  const firstFlip = await (await firstResponse).json()
  await expect(page.locator('.game-card.revealed')).toHaveCount(1)
  await page.getByRole('button', { name: '暂停游戏', exact: true }).click()
  await expect(page.getByRole('heading', { name: '休息一下，也很好。' })).toBeVisible()
  await expect(page.locator('.game-card.revealed')).toHaveCount(0)
  const pausedTime = await page.locator('.stat').first().locator('strong').innerText()
  await page.waitForTimeout(1100)
  await expect(page.locator('.stat').first().locator('strong')).toHaveText(pausedTime)
  await page.getByRole('button', { name: '继续漫游' }).click()

  await expect(page.locator('.game-card.revealed')).toHaveCount(1)
  const known = new Map([[firstFlip.cards[0].symbol, [0]]])
  for (let index = 0; index < 12; index += 2) {
    for (const position of [index, index + 1]) {
      if (position === 0) continue
      const response = page.waitForResponse(response => response.url().endsWith('/flip') && response.request().method() === 'POST')
      await page.locator('.game-card').nth(position).click()
      const result = await (await response).json()
      const symbol = result.cards[position].symbol
      known.set(symbol, [...(known.get(symbol) || []), position])
      if (result.lockedForMs > 0) {
        await expect(page.locator('.game-card.revealed:not(.matched)')).toHaveCount(0)
      }
    }
  }
  await page.screenshot({ path: 'test-results/desktop-playing.png', fullPage: true })
  for (const pair of known.values()) {
    const card = page.locator('.game-card').nth(pair[0])
    if ((await card.getAttribute('class')).includes('matched')) continue
    for (const index of pair) {
      const response = page.waitForResponse(response => response.url().endsWith('/flip') && response.request().method() === 'POST')
      await page.locator('.game-card').nth(index).click()
      await response
    }
  }
  await expect(page.getByRole('dialog', { name: '你的花园，开花了。' })).toBeVisible()
  expect((await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze()).violations).toEqual([])
  await page.getByRole('button', { name: '保存到花园榜单' }).click()
  await expect(page.getByRole('alert')).toContainText('1–16')
  await page.getByLabel('给这份好心情留个名字').fill('测试花匠6085')
  await page.getByRole('button', { name: '保存到花园榜单' }).click()
  await expect(page.getByText('成绩已保存，花园记住了你的名字。')).toBeVisible()
  await page.screenshot({ path: 'test-results/desktop-completed.png', fullPage: true })
  await page.getByRole('button', { name: '关闭成绩窗口' }).click()
  await expect(page.locator('.ranking-list')).toContainText('测试花匠6085')
  expect((await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze()).violations).toEqual([])
  await page.reload()
  await page.locator('.rank-tabs').getByRole('button', { name: '轻松' }).click()
  await expect(page.locator('.ranking-list')).toContainText('测试花匠6085')
  expect(errors).toEqual([])
})

test('窄屏、横屏与减少动态效果：无横向溢出，规则弹窗可键盘关闭', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' })
  await page.setViewportSize({ width: 375, height: 812 })
  await page.goto('/')
  await expect(page.getByRole('button', { name: '开始翻牌' })).toBeVisible()
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
  await page.screenshot({ path: 'test-results/mobile-ready.png', fullPage: true })
  await page.getByRole('button', { name: '玩法指南' }).click()
  await expect(page.getByRole('dialog', { name: '一起来种点好心情。' })).toBeVisible()
  await page.keyboard.press('Escape')
  await expect(page.getByRole('dialog')).not.toBeVisible()
  await expect(page.getByRole('button', { name: '玩法指南' })).toBeFocused()
  await page.getByRole('button', { name: '开始翻牌' }).click()
  await page.getByRole('button', { name: '重新开始', exact: true }).click()
  await expect(page.getByRole('dialog', { name: '要重新种一片花园吗？' })).toBeVisible()
  await page.getByRole('button', { name: '再想想' }).click()
  await expect(page.locator('.card-grid')).toBeVisible()
  await page.getByRole('group', { name: '游戏难度' }).getByRole('button', { name: /挑战/ }).click()
  await page.getByRole('button', { name: '开始新的一局' }).click()
  await expect(page.locator('.game-card')).toHaveCount(24)
  await page.setViewportSize({ width: 812, height: 375 })
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
  await page.screenshot({ path: 'test-results/mobile-landscape.png', fullPage: true })
  await page.setViewportSize({ width: 320, height: 740 })
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
})

test('排行榜连接失败有真实错误和重试入口', async ({ page }) => {
  await page.route('**/api/leaderboard*', route => route.fulfill({ status: 503, contentType: 'application/json', body: JSON.stringify({ message: '排行榜暂时不可用，请稍后重试。' }) }))
  await page.goto('/')
  await expect(page.getByRole('alert')).toContainText('排行榜暂时不可用')
  await expect(page.getByRole('button', { name: '重新加载' })).toBeVisible()
  await page.unroute('**/api/leaderboard*')
  await page.getByRole('button', { name: '重新加载' }).click()
  await expect(page.locator('.rank-error')).toHaveCount(0)
})
