const fs=require('fs');
const path=require('path');
let playwright;
try{playwright=require(process.env.PLAYWRIGHT_MODULE_PATH||'playwright')}catch(e){playwright=require('C:/Users/a3185/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright')}
const work=__dirname,base='http://127.0.0.1:18089';
const mode=process.argv[2]||'before';
(async()=>{
 const opts={headless:true};
 if(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH)opts.executablePath=process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH;
 else if(process.platform==='win32')opts.channel='msedge';
 const browser=await playwright.chromium.launch(opts);
 const context=await browser.newContext({viewport:{width:1440,height:1100},reducedMotion:'reduce'});
 const page=await context.newPage(),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 try{
  await page.goto(base);
  await page.waitForFunction(()=>!document.querySelector('.leaderboard .spin'));
  if(mode==='before'){
   await page.screenshot({path:path.join(work,'08-browser-home.png'),fullPage:true});
   await page.getByRole('group',{name:'游戏难度'}).getByRole('button',{name:/轻松/}).click();
   await page.getByRole('button',{name:'开始翻牌'}).click();
   await page.waitForFunction(()=>document.querySelector('.card-grid')?.getAttribute('aria-busy')==='false'&&!document.querySelector('.board-overlay'));
   const known=new Map();
   for(let index=0;index<12;index+=2){
    for(const position of [index,index+1]){
     const response=page.waitForResponse(r=>r.url().endsWith('/flip')&&r.request().method()==='POST');
     await page.locator('.game-card').nth(position).click();
     const state=await(await response).json();
     known.set(state.cards[position].symbol,[...(known.get(state.cards[position].symbol)||[]),position]);
     if(state.lockedForMs>0)await page.waitForFunction(()=>!document.querySelector('.game-card.revealed:not(.matched)'));
    }
   }
   for(const pair of known.values()){
    if((await page.locator('.game-card').nth(pair[0]).getAttribute('class')).includes('matched'))continue;
    for(const position of pair){
     const response=page.waitForResponse(r=>r.url().endsWith('/flip')&&r.request().method()==='POST');
     await page.locator('.game-card').nth(position).click();await response;
    }
   }
   await page.getByRole('dialog',{name:'你的花园，开花了。'}).waitFor();
   await page.getByLabel('给这份好心情留个名字').fill('6085补充实验');
   const submitted=page.waitForResponse(r=>r.url().endsWith('/score')&&r.request().method()==='POST');
   await page.getByRole('button',{name:'保存到花园榜单'}).click();
   const score=await(await submitted).json();
   await page.getByText('成绩已保存，花园记住了你的名字。').waitFor();
   await page.screenshot({path:path.join(work,'08-browser-saved.png')});
   fs.writeFileSync(path.join(work,'saved-score.json'),JSON.stringify(score,null,2));
   await page.getByRole('button',{name:'关闭成绩窗口'}).click();
   await page.screenshot({path:path.join(work,'08-browser-leaderboard.png'),fullPage:true});
   console.log(JSON.stringify(score));
  }else{
   await page.getByRole('group',{name:'排行榜难度'}).getByRole('button',{name:'轻松',exact:true}).click();
   await page.getByText('6085补充实验',{exact:true}).waitFor();
   await page.screenshot({path:path.join(work,'11-browser-recreated.png'),fullPage:true});
  }
  if(errors.length)throw Error(errors.join('\n'));
  fs.writeFileSync(path.join(work,'browser-'+mode+'.json'),JSON.stringify({base,mode,completedUtc:new Date().toISOString(),pageErrors:errors,result:'passed'},null,2));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
