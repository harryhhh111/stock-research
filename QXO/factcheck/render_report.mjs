import fs from 'node:fs/promises';
import {spawn} from 'node:child_process';
import {pathToFileURL} from 'node:url';
import path from 'node:path';
import os from 'node:os';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const output=process.argv[2] ? path.resolve(process.argv[2]) : await fs.mkdtemp(path.join(os.tmpdir(),'qxo-visual-'));
await fs.mkdir(output,{recursive:true});

const profile=await fs.mkdtemp(path.join(os.tmpdir(),'qxo-profile-'));
const proc=spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',['--headless=new','--remote-debugging-port=0','--disable-background-networking','--disable-extensions','--no-first-run',`--user-data-dir=${profile}`,'about:blank'],{stdio:'ignore'});
let ws;
try {
  let port;
  for (let i=0; i<100; i++) {
    try {port=(await fs.readFile(path.join(profile,'DevToolsActivePort'),'utf8')).split('\n')[0];break;}
    catch {await new Promise(r=>setTimeout(r,100));}
  }
  if (!port) throw Error('Chrome did not start');
  const tabs=await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
  ws=new WebSocket(tabs.find(t=>t.type==='page').webSocketDebuggerUrl);
  await new Promise((ok,fail)=>{ws.addEventListener('open',ok,{once:true});ws.addEventListener('error',fail,{once:true});});
  let id=0; const pending=new Map();
  ws.addEventListener('message',({data})=>{const m=JSON.parse(data);const cb=pending.get(m.id);if(cb){pending.delete(m.id);m.error?cb.fail(m.error):cb.ok(m.result);}});
  const cmd=(method,params={})=>new Promise((ok,fail)=>{pending.set(++id,{ok,fail});ws.send(JSON.stringify({id,method,params}));});
  const evalJS=async(expression)=>(await cmd('Runtime.evaluate',{expression,returnByValue:true})).result.value;
  await cmd('Page.enable');
  await cmd('Network.enable');
  await cmd('Network.setBlockedURLs',{urls:['http://*','https://*']});
  const files={home:'QXO.html'};
  for (const slug of ['industry-position','business-model','revenue-profit','cash-capital','governance','valuation'])
    files[slug]='reports/'+slug+'.html';
  const all={};
  for (const [name,file] of Object.entries(files)) {
    const results={};
    await cmd('Page.navigate',{url:pathToFileURL(path.join(root,file)).href});
    await new Promise(r=>setTimeout(r,200));
    for(const [mode,width,height] of [['desktop',1440,1000],['mobile',390,950],['printPreview',794,1123]]) {
      await cmd('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:false});
      await cmd('Emulation.setEmulatedMedia',{media: mode==='printPreview'?'print':'screen'});
      await evalJS('document.documentElement.style.scrollBehavior="auto"; scrollTo(0,0)');

      const m=await evalJS('({width:document.documentElement.clientWidth,scrollWidth:document.documentElement.scrollWidth,heading:document.querySelector("h1").textContent,cards:[...document.querySelectorAll("nav a.card")].map(x=>x.getAttribute("href"))})');
      if (!m || m.scrollWidth>m.width+1) {
        const overflowing = await evalJS(`[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>document.documentElement.clientWidth+1 && !e.closest('.table-wrap,.chart')).slice(0,10).map(e=>({tag:e.tagName,cls:e.className,text:e.textContent.slice(0,90),right:e.getBoundingClientRect().right}))`);
        throw Error(name+' '+mode+' overflow '+JSON.stringify({metrics:m,overflowing}));
      }
      if(name==='home'&&mode==='desktop') {
        const focus=[];
        for(let i=0;i<6;i++) {
          await cmd('Input.dispatchKeyEvent',{type:'keyDown',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});
          await cmd('Input.dispatchKeyEvent',{type:'keyUp',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});
          focus.push(await evalJS('document.activeElement.getAttribute("href")'));
        }
        if (focus.join(',')!==m.cards.join(',')) throw Error('Keyboard card order '+focus.join(','));
        m.keyboard=focus;
      }
      const positions = {
        'revenue-profit':['income-flow','guidance-overview'],
        'cash-capital':['cash-full-flow','quarter-cash-flow'],
        'governance':['transaction-bridge'],
        'valuation':['valuation']
      };
      const capture = async (suffix) => {
        const shot=await cmd('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});
        await fs.writeFile(path.join(output,name+'-'+mode+suffix+'.png'),Buffer.from(shot.data,'base64'));
      };
      await capture('');
      for (const anchor of positions[name] || []) {
        await evalJS(`document.getElementById(${JSON.stringify(anchor)}).scrollIntoView()`);
        await capture('-'+anchor);
      }
      m.flows = await evalJS(`Array.from(document.querySelectorAll('svg[data-flow]')).map(svg=>({
        flow:svg.dataset.flow,
        labelOverflow:Array.from(svg.querySelectorAll('text')).filter(t=>{
          const b=t.getBBox();
          return b.x<0||b.y<0||b.x+b.width>svg.viewBox.baseVal.width||b.y+b.height>svg.viewBox.baseVal.height;
        }).map(t=>t.textContent)
      }))`);
      if (m.flows.some(flow=>flow.labelOverflow.length)) throw Error(name+' flow label overflow');
      results[mode]=m;
    }
    const print = await cmd('Page.printToPDF',{preferCSSPageSize:true,printBackground:true});
    await fs.writeFile(path.join(output,name+'-print.pdf'),Buffer.from(print.data,'base64'));
    all[name]=results;
  }
  await fs.writeFile(path.join(output,'browser-check.json'),JSON.stringify(all,null,2)+'\n');
  console.log('Checked '+Object.keys(all).join(', ')+'. Screenshots and metrics at '+output);
} finally {
  ws?.close();
  proc.kill();
}
