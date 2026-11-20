import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {spawn} from 'node:child_process';
import {fileURLToPath,pathToFileURL} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const reports=path.resolve(here,'../reports');
const profile=await fs.mkdtemp(path.join(os.tmpdir(),'sndk-visual-'));
const proc=spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',['--headless=new','--remote-debugging-port=0',`--user-data-dir=${profile}`,'--disable-background-networking','--no-first-run','about:blank'],{stdio:'ignore'});
let ws;let seq=0;const pending=new Map();const results=[];
try{
 let port;for(let i=0;i<100;i++){try{port=(await fs.readFile(path.join(profile,'DevToolsActivePort'),'utf8')).split('\n')[0];break;}catch{}await new Promise(r=>setTimeout(r,100));}
 if(!port)throw Error('Chrome unavailable');
 const pages=await(await fetch(`http://127.0.0.1:${port}/json/list`)).json();ws=new WebSocket(pages.find(x=>x.type==='page').webSocketDebuggerUrl);
 await new Promise(r=>ws.addEventListener('open',r,{once:true}));ws.addEventListener('message',e=>{const m=JSON.parse(e.data);if(m.id&&pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result);}});
 const cmd=(method,params={})=>new Promise((resolve,reject)=>{const id=++seq;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}));});
 const ev=async expression=>(await cmd('Runtime.evaluate',{expression,returnByValue:true})).result.value;
 await cmd('Page.enable');await cmd('Network.enable');await cmd('Network.emulateNetworkConditions',{offline:true,latency:0,downloadThroughput:0,uploadThroughput:0});
 const files=(await fs.readdir(reports)).filter(x=>x.endsWith('.html')).map(x=>path.join(reports,x));
 const ind=path.resolve(here,'../../../行业研究/NAND/reports');for(const f of await fs.readdir(ind)){if(f.endsWith('.html'))files.push(path.join(ind,f));}
 for(const file of files){
  const name=path.basename(file,'.html');const record={page:file.split('/').slice(-4).join('/')};
  const out=path.resolve(path.dirname(file),'../factcheck/visual');await fs.mkdir(out,{recursive:true});
  for(const [mode,width]of[['desktop',1440],['mobile',390]]){
   await cmd('Emulation.setDeviceMetricsOverride',{width,height:1000,deviceScaleFactor:1,mobile:false});
   await cmd('Page.navigate',{url:pathToFileURL(file).href});await new Promise(r=>setTimeout(r,180));
   record[mode]=await ev('({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,headings:document.querySelectorAll("h1").length,tables:document.querySelectorAll("table").length,charts:document.querySelectorAll("svg").length})');
   if(record[mode].scrollWidth>width)throw Error('Body overflow '+file+' '+mode);
   const shot=await cmd('Page.captureScreenshot',{format:'png'});await fs.writeFile(path.join(out,`${name}-${mode}.png`),Buffer.from(shot.data,'base64'));
  }
  await cmd('Emulation.setDeviceMetricsOverride',{width:681,height:970,deviceScaleFactor:1,mobile:false});await cmd('Emulation.setEmulatedMedia',{media:'print'});
  record.print=await ev('({tables:[...document.querySelectorAll("table")].map(t=>({id:t.id,width:t.scrollWidth,available:t.parentElement.clientWidth}))})');
  if(record.print.tables.some(t=>t.width>t.available+2))throw Error('Print table overflow '+file);
  const printShot=await cmd('Page.captureScreenshot',{format:'png'});await fs.writeFile(path.join(out,`${name}-print-preview.png`),Buffer.from(printShot.data,'base64'));
  const pdf=await cmd('Page.printToPDF',{printBackground:true,preferCSSPageSize:true});await fs.writeFile(path.join(out,`${name}-print.pdf`),Buffer.from(pdf.data,'base64'));
  await cmd('Emulation.setEmulatedMedia',{media:''});results.push(record);
 }
 // Income and cash charts independently inspected at readable desktop scale.
 const out=path.join(here,'visual');
 for(const [file,id,name]of[['revenue-profit.html','income-flow','income-flow'],['cash-capital.html','cash-use','cash-use']]){
  await cmd('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
  await cmd('Page.navigate',{url:pathToFileURL(path.join(reports,file)).href});await new Promise(r=>setTimeout(r,150));await ev(`document.getElementById('${id}').scrollIntoView()`);
  const shot=await cmd('Page.captureScreenshot',{format:'png'});await fs.writeFile(path.join(out,`${name}-detail.png`),Buffer.from(shot.data,'base64'));
 }
 await fs.writeFile(path.join(here,'visual-checks.json'),JSON.stringify({offline:true,pages:results},null,2));console.log(JSON.stringify(results));
}finally{ws?.close();proc.kill();}
