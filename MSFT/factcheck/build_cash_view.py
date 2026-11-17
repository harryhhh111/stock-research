"""从既有核验输入生成离线HTML及同源Markdown机器底稿；非全公司研究更新。"""
import json,html
from pathlib import Path
p=Path(__file__).resolve().parent;root=p.parent
d=json.loads((p/'data/inputs.json').read_text());a=d['annual']
# 年报现金流量表补充摘录，单位B美元；原表为M美元，除以1000。
source={'url':d['source_annual'],'date':'2026-07-29','location':'FY2026现金流量表','start':'2025-07-01','end':'2026-06-30','type':'annual','unit':'B USD','status':'company_reported','values':{'期初现金':30.242,'经营现金净流入':182.935,'投资现金净流出':-139.500,'融资现金净流出':-52.546,'汇率影响':-.196,'期末现金':20.935}}
v=source['values'];assert abs(v['期初现金']+sum(list(v.values())[1:5])-v['期末现金'])<1e-8
outflows=[('现金固定资产投入',a['2026']['capex']),('现金分红',a['2026']['dividend']),('现金流表回购',a['2026']['buyback'])]
assert abs(a['2026']['cfo']-a['2026']['capex']-66.987)<1e-8
profit_values={'集团收入':331.839,'营业成本':106.374,'毛利':225.465,'研发':35.562,'销售':26.710,'管理':7.956,'经营利润':155.237}
assert abs(profit_values['集团收入']-profit_values['营业成本']-profit_values['毛利'])<1e-8
assert abs(profit_values['毛利']-sum(profit_values[k] for k in ['研发','销售','管理','经营利润']))<1e-8
sections=[]
def billing_diagram():
 cards=[('PC厂商','Windows OEM','预装操作系统许可'),('企业IT部门','Windows / SQL Server','本地部署授权'),('企业与个人','Office / M365','本地许可或订阅服务')]
 return '<div class="billing">'+''.join('<div class="billing-row"><b>'+a+'</b><span aria-label="支付">→</span><b>'+b+'</b><span aria-label="购买">→</span><span>'+c+'</span></div>' for a,b,c in cards)+'</div><p class="meta">等宽箭头仅表示交易关系，不表示金额；传统软件独立现金收款未披露。</p>'

def uses_chart():
 b=''
 for i,(name,value) in enumerate(outflows):
  y=30+i*65
  b+=txt(205,y+22,name,16,anchor='end')+f'<rect x="225" y="{y}" width="{value*5}" height="34" rx="3" fill="#b96535"/>'+txt(238+value*5,y+23,f'{value:.3f}',15,anchor='start')
 return svgbody(b,'FY2026已列三项现金用途，固定资产投入115.948、分红26.445、回购22.271',240)

def table(headers,rows):return '<div class="scroll"><table><thead><tr>'+''.join('<th>'+x+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def svgbody(body,label,height=340):return f'<svg role="img" aria-label="{label}" viewBox="0 0 960 {height}" xmlns="http://www.w3.org/2000/svg"><title>{label}</title>{body}</svg>'
def txt(x,y,t,size=15,color='#334155',anchor='middle'):return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{html.escape(str(t))}</text>'
def sankey(nodes,edges,columns,scale=1.5,height=770):
 # 所有节点与路径共享金额比例；源/终端可不守恒，中间节点必须守恒。
 incoming={k:0. for k in nodes};outgoing={k:0. for k in nodes}
 for u,v,val in edges:
  assert val>=0
  outgoing[u]+=val;incoming[v]+=val
 for k in nodes:
  if incoming[k] and outgoing[k]:assert abs(incoming[k]-outgoing[k])<1e-6,(k,incoming[k],outgoing[k])
 coords={};width=1250
 for c,keys in enumerate(columns):
  total=sum(nodes[k][1]*scale for k in keys)+(len(keys)-1)*42
  yy=80+(height-150-total)/2
  for k in keys:
   coords[k]=(210+c*(780/(len(columns)-1)),yy);yy+=nodes[k][1]*scale+42
 b='';ino={k:0. for k in nodes};outo=ino.copy()
 for u,v,val in edges:
  x1,y1=coords[u];x2,y2=coords[v];x1+=10;y1+=outo[u];y2+=ino[v];h=val*scale
  outo[u]+=h;ino[v]+=h;mid=(x1+x2)/2
  path=f'M{x1},{y1} C{mid},{y1} {mid},{y2} {x2},{y2} L{x2},{y2+h} C{mid},{y2+h} {mid},{y1+h} {x1},{y1+h} Z'
  color=nodes[u][2]
  label=f'{nodes[u][0]} → {nodes[v][0]}：{val:.3f} B美元；占起点 {val/nodes[u][1]*100:.2f}%'
  b+=f'<path class="flow" tabindex="0" aria-label="{label}" d="{path}" fill="{color}" fill-opacity=".28"><title>{label}</title></path>'
 for k,(name,val,color) in nodes.items():
  x,y=coords[k];h=val*scale;b+=f'<rect x="{x}" y="{y}" width="10" height="{h}" fill="{color}"/>'
  # 外侧标签避开路径；中间标签置于节点上方。
  if k in columns[0]:tx=x-14;anchor='end';ty=y+h/2
  elif k in columns[-1]:tx=x+22;anchor='start';ty=y+h/2
  else:tx=x+5;anchor='middle';ty=y-33
  b+=txt(tx,ty,name,14,anchor=anchor)+txt(tx,ty+20,f'{val:,.3f}',15,color,anchor)
 return f'<svg class="sankey" role="img" aria-label="金额比例桑基图，详见下方同源底表" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg"><title>金额单位B美元，带宽按金额同比例绘制</title>{b}</svg>'
def waterfall():
 n={'start':('期初现金',30.242,'#64748b'),'cfo':('经营现金净流入',182.935,'#138778'),'pool':('现金来源合计',213.177,'#405878'),'invest':('投资净流出',139.5,'#b76b45'),'fin':('融资净流出',52.546,'#ab7757'),'fx':('汇率减少 · 非付款',.196,'#8896a6'),'end':('期末现金 · 留存',20.935,'#405878')}
 e=[('start','pool',30.242),('cfo','pool',182.935)]+[('pool',k,n[k][1]) for k in ['invest','fin','fx','end']]
 return sankey(n,e,[['start','cfo'],['pool'],['invest','fin','fx','end']],2.0,760)
def profit_chart():
 colors=['#4c78a8','#138778','#b49950','#8876a4','#629eac','#8090a0']
 products=d['products'];keys=list(products);names=['服务器产品与云服务','M365商业产品与云服务','Xbox','LinkedIn','Windows与设备','其余产品与服务']
 values=[products[k][2] for k in keys[:5]]+[sum(products[k][2] for k in keys[5:])]
 n={str(i):(name,val,colors[i]) for i,(name,val) in enumerate(zip(names,values))}
 n.update({'rev':('集团收入',profit_values['集团收入'],'#405878'),'cost':('营业成本',profit_values['营业成本'],'#bd8669'),'gross':('毛利',profit_values['毛利'],'#138778'),'rd':('研发费用',profit_values['研发'],'#b76b45'),'sales':('销售费用',profit_values['销售'],'#b76b45'),'admin':('管理费用',profit_values['管理'],'#b76b45'),'op':('经营利润',profit_values['经营利润'],'#138778')})
 e=[(str(i),'rev',val) for i,val in enumerate(values)]+[('rev','cost',106.374),('rev','gross',225.465)]+[('gross',k,n[k][1]) for k in ['rd','sales','admin','op']]
 return sankey(n,e,[[str(i) for i in range(6)],['rev'],['cost','gross'],['rd','sales','admin','op']],1.4,900)
def grouped():
 b='';colors=['#137c66','#b96535','#2454a4'];names=['CFO','现金CapEx','FCF'];base=265
 for tick in [0,50,100,150,200]:
  yy=base-tick;b+=f'<line x1="55" x2="930" y1="{yy}" y2="{yy}" stroke="#e2e8f0"/>'+txt(40,yy+5,tick,12)
 for i,(year,row) in enumerate(a.items()):
  vals=[row['cfo'],row['capex'],row['cfo']-row['capex']]
  for j,val in enumerate(vals):
   x=115+i*285+j*65;b+=f'<rect x="{x}" y="{base-val}" width="48" height="{val}" fill="{colors[j]}" rx="3"/>'+txt(x+24,base-val-10,f'{val:.3f}',12)
  b+=txt(205+i*285,290,'FY'+year)
 for j,n in enumerate(names):b+=f'<rect x="{240+j*190}" y="315" width="12" height="12" fill="{colors[j]}"/>'+txt(260+j*190,326,n,13,anchor='start')
 return svgbody(b,'集团三年经营现金流、现金资本开支与自由现金流；三者不能相加',350)
rows=[['Windows OEM','PC厂商支付预装许可费','设备与消费者','传统许可'],['Windows商业本地许可','企业采购桌面系统使用权','代理与基础设施／生产力及服务器许可','传统许可'],['Windows Server / SQL Server','企业采购本地服务器或数据库使用权','代理与基础设施／生产力及服务器许可','传统许可；按期付费也不自动是SaaS'],['M365 / Office','企业或个人采购订阅、升级或本地许可','云服务与本地许可按合同区分','应用服务与本地许可分开'],['Azure托管数据库','客户为托管平台及资源使用付费','Azure','云平台服务，不属于本地数据库许可']]
blocks=[('boundary','01 / 先把业务边界画清楚', '<p>第一层关注Windows、Office与服务器数据库等成熟业务。它们的客户、收费和财报归属不同；传统授权、按期订阅、SaaS和Azure服务不能混成一类。</p>'+billing_diagram()+table(['产品','钱从谁来、为何支付','披露归属','研究分类'],rows)+'<div class="callout">披露边界：微软未单列这组“传统软件业务”的完整现金收入、经营付款和FCF。不能画出“SQL Server现金流入→AI建设”的精确资金流。集团资金统一调配，现金具有可替代性。</div>'),('profit','02 / 收入从哪里来，如何留下利润', '<p class="meta">微软集团 · FY2026 · B美元 · 会计收入及费用，非现金收付款。[S1]</p>'+profit_chart()+table(['收入来源','金额'],[[k,f"{val[2]:.3f}"] for k,val in d['products'].items()])+table(['利润形成','金额'],[[k,f'{val:.3f}'] for k,val in profit_values.items()])+'<p>其余产品与服务为搜索广告、M365消费者、Dynamics、企业与伙伴服务及其他之和。费用含非现金折旧及股权薪酬；本图停在经营利润，不把CapEx或分红混作费用。共享节点后的路径不代表产品级成本分摊。</p>'),('bridge','03 / 集团现金：从哪里来，到哪里去', '<p class="meta">Microsoft集团 · FY2026年度 · B美元 · 现金及现金等价物，不含短期证券。来源[S1]现金流量表；✅ 起终点勾稽。</p>'+waterfall()+table(['现金桥项目','金额'],[[k,f'{val:+.3f}'] for k,val in v.items()])+'<p>现金减少9.307。CFO是扣除经营付款后的净额，不能再从此处重复扣研发、工资、采购等费用。投资及融资用净额展示，包含流入与流出；不是“全部现金付款构成图”。</p>'),('uses','04 / 净流出如何展开', '<p class="meta">Microsoft集团 · FY2026年度 · B美元 · 只列三项互斥现金用途，不代表全部支出。[S1]</p>'+table(['归属','明细','金额'],[['投资净流出','现金固定资产投入','115.948'],['投资净流出','其他投资净流出（复算残差）','23.552'],['融资净流出','现金分红','26.445'],['融资净流出','现金流表回购','22.271'],['融资净流出','偿债','3.000'],['融资净流出','剩余融资净流出（复算残差）','0.830']])+'<p>投资净流出139.500＝115.948＋23.552；融资净流出52.546＝26.445＋22.271＋3.000＋0.830。剩余融资净流出＝其他融资净额2.839－发股流入2.009，含义并非全部融资付款。固定资产115.948既支持云和AI，也服务其他业务，不能全部标为AI投入。分红26.445与现金流表回购22.271合计48.716；回购含员工税务代扣相关交易，不能与公开计划口径混用。</p>'),('trend','05 / 赚得更多，留下的现金是否也更多', '<p class="meta">Microsoft集团 · FY2024—FY2026完整财年 · B美元 · 现金CapEx按正数表示支出规模。FCF＝CFO－现金CapEx，是计算结果，非第三种可相加用途。[S1]</p>'+grouped()+table(['年度指标','FY2024','FY2025','FY2026'],[[name]+[f'{(row["cfo"]-row["capex"] if key=="fcf" else row[key]):.3f}' for row in a.values()] for key,name in [('cfo','经营现金流CFO'),('capex','现金固定资产投入'),('fcf','自由现金流FCF')]])+'<p><strong>【我的推演】</strong>经营现金流上升，而FCF连续下降，说明现金投入增速更快。它提出了资本回报问题，却不能证明传统软件业务本身衰退，也不能证明全部投入都是AI。</p>'),('next','06 / 第一层接下来真正要验证什么','<ul><li>收入来源：传统Windows、Office及服务器数据库许可各自规模与增速；新旧分类重述后再比较。</li><li>经营质量：续费、升级、定价权、费用与利润证据；不把订阅增长自动解释为提价。</li><li>现金转化：合同确认与收款时点、递延收入和应收变化；利润和现金分开。</li><li>向AI过渡：传统许可被云订阅替代的影响，以及每用户收入是否覆盖新增推理成本。</li></ul><p>本页是HTML展示测试，非第一层完整研究验收；尚未填入可独立归属于传统软件的现金总额。最新季度及分部详情继续见<a href="云服务、数据中心与AI业务.md">AI专题底稿</a>和<a href="MSFT.md">集团研究</a>。本页年度图不冒充最新季度或当前行情。</p>')]
md='HTML阅读入口：[微软桑基图](传统软件与现金流.html)\n\n# 微软微软收入、利润与现金桑基图\n\n展示生成日期：2026-11-12；沿用2026-11-04核验数据；非最新财务刷新。\n\n'
for id,title,body in blocks:
 sections.append(f'<section id="{id}"><h2>{title}</h2>{body}</section>')
 md+='## '+title+'\n\n'+body+'\n\n'
sourcehtml=f'<p id="s1">[S1] <a href="{d["source_annual"]}">微软FY2026年报</a>，现金流量表；报告期末2026-06-30，10-K提交2026-07-29。三年数据沿用<a href="factcheck/data/inputs.json">既有核验输入</a>。现金桥补充输入与元数据内嵌在<a href="factcheck/build_cash_view.py">生成脚本</a>；运行 python MSFT/factcheck/build_cash_view.py 可同时重建HTML及机器底稿。</p><p>[S2] <a href="https://www.sec.gov/Archives/edgar/data/789019/000119312526436133/msft-20260930.htm">FY2027 Q1 10-Q附注16</a>，2026-10-29；用于授权与服务分类边界，未将Q1业务收入当作现金收款。</p>'
check='<p>本轮检查：现金桥起终点断言、FCF勾稽、图表与表格同源；图形静态SVG、不依赖网络、脚本或悬停。桑基图重构日期2026-11-12；内置浏览器对本地file页面返回访问策略拦截，未完成桌面、窄屏、打印视觉验收。仅FY2026现金桥资料已核对，故不提供缺少现金底表年份的切换，三年历史保持独立展示。悬停及键盘聚焦路径可高亮，但实际交互效果尚未视觉验收。没有据此宣称完整公司或第一层基本面研究验收通过。</p>'
css='''.billing{border:1px solid #dce3e9;padding:12px;background:#f7fafb}.billing-row{display:grid;grid-template-columns:1fr 30px 1.6fr 30px 1.5fr;gap:8px;padding:14px 4px;font-size:14px;border-bottom:1px solid #e2e8f0} .flow{transition:fill-opacity .16s;outline:none}.flow:hover,.flow:focus{fill-opacity:.75;stroke:#334155;stroke-width:1}.sankey text{paint-order:stroke;stroke:white;stroke-width:4px;stroke-linejoin:round}svg.sankey{min-width:1000px}nav a{font-size:13px;text-decoration:none} body{margin:0;background:#f3f5f7;color:#172c3e;font:16px/1.8 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{max-width:1100px;margin:0 auto;padding:48px 28px}header{padding:32px 0;border-bottom:3px solid #137c66}h1{font-size:38px;line-height:1.3;letter-spacing:-1px}h2{font-size:24px}small,.meta{color:#526578;font-size:14px}.eyebrow{letter-spacing:3px;color:#137c66;font-weight:700}nav{display:flex;gap:18px;flex-wrap:wrap;padding:20px 0}a{color:#2454a4}section{margin:24px 0;background:white;border:1px solid #dce3e9;border-radius:12px;padding:28px}svg{width:100%;height:auto;min-width:650px;display:block}section:has(svg){overflow:auto}.scroll{overflow:auto}table{border-collapse:collapse;width:100%;font-size:14px;margin:18px 0}th,td{padding:12px;border-bottom:1px solid #dce3e9;text-align:right;min-width:90px}th:first-child,td:first-child{text-align:left;position:sticky;left:0;background:white;min-width:140px}thead{background:#edf3f5}.callout{border-left:4px solid #b96535;background:#faf4eb;padding:16px;margin-top:20px}strong{color:#137c66}@media(max-width:600px){main{padding:20px 12px}section{padding:18px}h1{font-size:28px}h2{font-size:21px}}@media print{body{background:white;font-size:11px}main{padding:0;max-width:none}section{border:0;padding:8px 0;overflow:visible!important;break-inside:avoid}svg{min-width:0!important;width:100%}nav{display:none}table{font-size:10px}td,th{min-width:0!important;padding:6px;position:static!important}.scroll{overflow:visible}a{color:inherit}h1{font-size:25px}}'''
intro='''<header><div class="eyebrow">MICROSOFT / CASH ECONOMICS</div><h1>微软的钱，<br>从哪里来，流向哪里？</h1><p>先分清收入、利润与现金，再观察成熟业务能否支撑新投入。</p><small>展示测试 · 2026-11-12生成 · 沿用2026-11-04核验材料<br>现金图：FY2026及FY2024—FY2026年度历史；非传统软件独立现金流，非最新行情。</small></header>'''
report='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>微软｜传统软件与集团现金流</title><style>'+css+'</style></head><body><main>'+intro+'<nav>'+''.join(f'<a href="#{id}">{title}</a>' for id,title,_ in blocks)+'</nav>'+''.join(sections)+'<section id="sources"><h2>核验与来源</h2>'+sourcehtml+check+'</section></main></body></html>'
(root/'传统软件与现金流.html').write_text(report)
(root/'传统软件与现金流底稿.md').write_text(md+'## 核验与来源\n\n'+sourcehtml+check)
(p/'cash_view_metadata.json').write_text(json.dumps(source,ensure_ascii=False,indent=2))
print('现金桥、FCF断言通过；HTML与底稿生成完成')
