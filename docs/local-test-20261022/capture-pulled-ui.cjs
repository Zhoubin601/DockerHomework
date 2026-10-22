const { createRequire } = require('node:module');
const path = require('node:path');
const fs = require('node:fs/promises');
const root=path.resolve(__dirname,'../..');
const { chromium, expect }=createRequire(path.join(root,'Code/memory-game6085/frontend/package.json'))('@playwright/test');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 try{
  const page=await browser.newPage({viewport:{width:1440,height:1100},reducedMotion:'reduce'});
  const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:18087');
  await expect(page.getByRole('heading',{name:'今天，也要好好玩。'})).toBeVisible();
  await page.getByRole('group',{name:'排行榜难度'}).getByRole('button',{name:'轻松',exact:true}).click();
  await expect(page.locator('.ranking-list')).toContainText('测试花匠6085');
  await page.screenshot({path:path.join(__dirname,'docker-roundtrip/after-recreate-ui.png'),fullPage:true});
  if(errors.length)throw new Error(errors.join('\n'));
  await fs.writeFile(path.join(__dirname,'docker-roundtrip/browser-after.json'),JSON.stringify({url:page.url(),savedScoreVisible:true,pageErrors:errors,result:'passed'},null,2));
  console.log('Pulled-image browser and persisted leaderboard: passed');
 } finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
