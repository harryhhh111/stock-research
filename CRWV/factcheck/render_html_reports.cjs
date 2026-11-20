// NODE_PATH must point to a Node environment containing Playwright.
const {chromium}=require('playwright');
const crypto=require('node:crypto');
const fs=require('node:fs/promises'),path=require('node:path'),{pathToFileURL}=require('node:url');
const root=path.resolve(__dirname,'../..');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME_BIN||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try{
 for(const project of ['CRWV','Nebius公司研究']){
  const out=path.join(root,project,'factcheck','visual');await fs.mkdir(out,{recursive:true});
  const ctx=await browser.newContext({viewport:{width:1440,height:1000},offline:true,javaScriptEnabled:false});const page=await ctx.newPage();
  await page.goto(pathToFileURL(path.join(root,project,'reports/main.html')).href);await page.evaluate(()=>{document.documentElement.style.scrollBehavior='auto'});
  const result={checked_at:'2026-11-18',scope:'full main-report rebuild',report_sha256:crypto.createHash('sha256').update(await fs.readFile(path.join(root,project,'reports/main.html'))).digest('hex'),offline:true,javascript:false};
  result.desktop=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,svgCount:document.querySelectorAll('svg').length,brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length}));
  result.anchors=await page.evaluate(()=>[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(decodeURIComponent(a.hash.slice(1)))).map(a=>a.hash));
  await page.screenshot({path:path.join(out,'desktop.png')});
  await page.locator('#revenue figure').nth(0).screenshot({path:path.join(out,'income-sankey.png')});
  await page.locator('#cash-flow + figure').screenshot({path:path.join(out,'cash-sankey.png')});
  await page.locator('#annual-revenue + .table-wrap').screenshot({path:path.join(out,'annual-revenue-table.png')});
  await page.locator('#quarter-revenue + .table-wrap').screenshot({path:path.join(out,'quarter-revenue-table.png')});
  await page.locator('#annual-finance + .table-wrap').screenshot({path:path.join(out,'annual-finance-table.png')});
  await page.locator('#valuation .table-wrap').nth(2).screenshot({path:path.join(out,'valuation-stages.png')});
  result.svgLabelBounds=await page.evaluate(()=>[...document.querySelectorAll('svg')].map((svg,i)=>({figure:i,viewBox:svg.getAttribute('viewBox'),overflow:[...svg.querySelectorAll('text')].map(t=>({text:t.textContent,b:t.getBBox()})).filter(x=>x.b.x<0||x.b.y<0||x.b.x+x.b.width>svg.viewBox.baseVal.width+1||x.b.y+x.b.height>svg.viewBox.baseVal.height+1).map(x=>x.text)})));
  await page.locator('#price-review figure').screenshot({path:path.join(out,'price-comparison.png')});
  await page.setViewportSize({width:390,height:900});
  result.mobile=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth}));
  await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:path.join(out,'mobile.png')});
  await page.locator('#annual-revenue').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'mobile-table.png')});
  await page.emulateMedia({media:'print'});await page.setViewportSize({width:1122,height:794});
  result.print=await page.evaluate(()=>({tableOverflow:[...document.querySelectorAll('.table-wrap')].filter(x=>x.scrollWidth>x.clientWidth+1).length,figureOverflow:[...document.querySelectorAll('figure')].filter(x=>x.scrollWidth>x.clientWidth+1).length}));
  await page.pdf({path:path.join(out,'print.pdf'),printBackground:true,preferCSSPageSize:true});
  await fs.writeFile(path.join(root,project,'factcheck/html-visual-checks.json'),JSON.stringify(result,null,2)+'\n');console.log(project,JSON.stringify(result));await ctx.close();
 }
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
