// Uses the local Chrome executable and built-in Node CDP/WebSocket; no browser package or CDN.
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {spawn} from 'node:child_process';
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.dirname(here);const out=path.join(root,'assets');await fs.mkdir(out,{recursive:true});
const profile=await fs.mkdtemp(path.join(os.tmpdir(),'qxo-render-'));
const executable='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const proc=spawn(executable,['--headless=new','--remote-debugging-port=0',`--user-data-dir=${profile}`,'--no-first-run','--disable-background-networking','--disable-extensions','about:blank'],{stdio:'ignore'});
let ws;
try{
 let port;
 for(let i=0;i<100;i++){
  try{port=(await fs.readFile(path.join(profile,'DevToolsActivePort'),'utf8')).split('\n')[0];break;}catch{}await new Promise(r=>setTimeout(r,100));
 }
 if(!port)throw Error('Chrome did not start');
 const list=await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
 ws=new WebSocket(list.find(x=>x.type==='page').webSocketDebuggerUrl);
 await new Promise((resolve,reject)=>{ws.addEventListener('open',resolve,{once:true});ws.addEventListener('error',reject,{once:true});});
 let next=0;const pending=new Map();ws.addEventListener('message',ev=>{const m=JSON.parse(ev.data);if(m.id&&pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result);}});
 const cmd=(method,params={})=>new Promise((resolve,reject)=>{const id=++next;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}));});
 await cmd('Page.enable');await cmd('Network.enable');await cmd('Network.emulateNetworkConditions',{offline:true,latency:0,downloadThroughput:0,uploadThroughput:0});
 await cmd('Emulation.setDeviceMetricsOverride',{width:1440,height:1100,deviceScaleFactor:1,mobile:false});
 await cmd('Page.navigate',{url:pathToFileURL(path.join(root,'QXO.html')).href});await new Promise(r=>setTimeout(r,1000));
 const evaluate=async expression=>(await cmd('Runtime.evaluate',{expression,returnByValue:true})).result.value;
 await cmd('Runtime.evaluate',{expression:'document.documentElement.style.scrollBehavior="auto";scrollTo(0,0)'});
 const metrics={desktop:await evaluate('({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight,charts:document.querySelectorAll("svg").length})')};
 async function shot(name){let r=await cmd('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});await fs.writeFile(path.join(out,name),Buffer.from(r.data,'base64'));}
 await shot('2026-11-17-desktop.png');
 for(const [id,name] of [['income-flow','income-flow'],['cash-full-flow','cash-flow']]){
  await cmd('Runtime.evaluate',{expression:`document.getElementById('${id}').scrollIntoView()`});await shot(`2026-11-17-${name}.png`);
 }
 metrics.sankeyLabels=await evaluate(`Array.from(document.querySelectorAll('svg[data-flow]')).map(svg=>({flow:svg.dataset.flow,overflow:Array.from(svg.querySelectorAll('text')).map(t=>({text:t.textContent,b:t.getBBox()})).filter(x=>x.b.x<0||x.b.y<0||x.b.x+x.b.width>svg.viewBox.baseVal.width||x.b.y+x.b.height>svg.viewBox.baseVal.height).map(x=>x.text)}))`);
 await cmd('Runtime.evaluate',{expression:'document.getElementById("valuation").scrollIntoView()'});await shot('2026-11-17-valuation.png');
 await cmd('Emulation.setDeviceMetricsOverride',{width:390,height:1000,deviceScaleFactor:1,mobile:false});await cmd('Runtime.evaluate',{expression:'scrollTo(0,0)'});await shot('2026-11-17-mobile.png');
 metrics.mobile=await evaluate('({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight})');
 await cmd('Runtime.evaluate',{expression:'document.querySelector(".chart").scrollIntoView()'});await shot('2026-11-17-mobile-chart.png');
 await cmd('Runtime.evaluate',{expression:'document.getElementById("cash-full-flow").scrollIntoView()'});await shot('2026-11-17-mobile-cash-flow.png');
 await cmd('Emulation.setDeviceMetricsOverride',{width:1440,height:1100,deviceScaleFactor:1,mobile:false});
 await cmd('Emulation.setEmulatedMedia',{media:'print'});
 const pdf=await cmd('Page.printToPDF',{printBackground:true,preferCSSPageSize:true,displayHeaderFooter:false});await fs.writeFile(path.join(out,'2026-11-17-print.pdf'),Buffer.from(pdf.data,'base64'));
 metrics.print={pdf:'assets/2026-11-17-print.pdf',bytes:Buffer.from(pdf.data,'base64').length};
 await fs.writeFile(path.join(here,'visual_checks.json'),JSON.stringify(metrics,null,2));console.log(JSON.stringify(metrics));
}finally{ws?.close();proc.kill();}
