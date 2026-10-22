const fs = require('fs');
const path = require('path');
let playwright;
try { playwright = require(process.env.PLAYWRIGHT_MODULE_PATH || 'playwright'); }
catch (error) {
 if (process.platform !== 'win32') throw error;
 playwright = require('C:/Users/a3185/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
}
const { chromium } = playwright;
const work = __dirname;
const escape = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
(async()=>{
 const options={headless:true};
 if(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH) options.executablePath=process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH;
 else if(process.platform==='win32') options.channel='msedge';
 const browser = await chromium.launch(options);
 const page = await browser.newPage({viewport:{width:1240,height:900},deviceScaleFactor:1});
 const stages = process.argv.slice(2);
 for(const stage of stages){
  const source = fs.readFileSync(path.join(work,stage+'.txt'),'utf8');
  const lines = source.trimEnd().split(/\r?\n/);
  const limit=31;
  const pages=[];
  for(let i=0;i<lines.length;i+=limit){
   const filename=stage+'-log-'+String(pages.length+1).padStart(2,'0');
   const html=`<!doctype html><meta charset="utf-8"><style>*{box-sizing:border-box}body{margin:0;padding:28px;background:#fff;color:#111;font-family:Arial,"Microsoft YaHei",sans-serif}h1{font-size:25px;margin:0 0 10px}p{font-size:17px;margin:5px 0 12px;color:#444}pre{font-family:Consolas,monospace;font-size:21px;line-height:1.35;white-space:pre-wrap;overflow-wrap:anywhere;background:#f3f5f7;border:1px solid #b4bac2;padding:17px;margin:0}</style><h1>Docker 6085 补充实验 · 实际命令日志</h1><p>${escape(stage+'.txt')} · 原日志第 ${i+1}—${Math.min(i+limit,lines.length)} 行 · UTC 时间按日志保留</p><pre>${escape(lines.slice(i,i+limit).join('\n'))}</pre>`;
   fs.writeFileSync(path.join(work,filename+'.html'),html);
   await page.setContent(html);await page.screenshot({path:path.join(work,filename+'.png'),fullPage:true});
   pages.push(filename+'.png');
  }
  fs.writeFileSync(path.join(work,stage+'-captures.json'),JSON.stringify(pages,null,2));
  console.log(stage+': '+pages.length+' real log screenshots');
 }
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
