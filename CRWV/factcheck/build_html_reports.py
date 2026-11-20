"""Generate the two maintained HTML entries from saved evidence. No network required.
Run with Python 3 standard library (CoreWeave source extraction runs separately). Money: USD millions unless explicitly stated.
"""
from pathlib import Path
import json, math, re, html
ROOT=Path(__file__).resolve().parents[2]
C=ROOT/'CRWV'; N=ROOT/'Nebius公司研究'
cf=json.loads((C/'factcheck/q3-2026-results.json').read_text())
read=re.sub(r'\s+',' ',(N/'factcheck/data/q3-2026/release-readable.txt').read_text())
letter=re.sub(r'\s+',' ',(N/'factcheck/data/q3-2026/letter-readable.txt').read_text())
# Assertions tie the transcribed Q3 facts to the saved original PDF extraction.
for phrase in ['Revenues 146.1 980.8 302.1 1,962.1','Debt, current 24.5 187.5','Debt, non-current 4,103.2 14,003.3','Cash and cash equivalents 3,678.1 7,425.6','Accounts receivable 720.3 4,039.9','(273.0)', '4,231.1','(7,300.4) 664%','3,434.0','(3,761.8)']:
 assert phrase in read,phrase
for phrase in ['$325 million','low end of our $3.0-3.4 billion','$27 billion','$40-45 billion','remaining tranches now scheduled for 2Q27']:
 assert phrase in letter,phrase
nb={
 'q1':dict(revenue=399.0,op=-128.0,net=621.2,ebitda=129.5,cfo=2258.0,cash_capex=2472.9,sbc=35.3,cloud=389.7,cloud_ebitda=174.0,prior=50.9,cloud_prior=41.4),
 'q2':dict(revenue=582.3,op=-175.9,net=-190.4,ebitda=236.2,cfo=4504.1-2258.0,cash_capex=8130.3-2472.9,sbc=137.8-35.3,cloud=574.9,cloud_ebitda=285.7,prior=105.1,cloud_prior=93.7),
 'q3':dict(revenue=980.8,op=50.4,net=-37.5,ebitda=465.8,cfo=-273.0,cash_capex=7300.4,sbc=58.7,cloud=973.8,cloud_ebitda=518.2,prior=146.1,cloud_prior=131.1),
 'balance':dict(cash=7425.6,restricted_cash=1215.5,debt_ex_leases=187.5+14003.3,net_debt_ex_leases=187.5+14003.3-7425.6,equity=12299.2),
 'ttm':dict(revenue=1962.1+227.7,net=393.3+(9.8-278.6),cfo=4231.1+834.3,cash_capex=15430.7+2056.0)
}
for q in ['q1','q2','q3']:
 d=nb[q];d.update(fcf=d['cfo']-d['cash_capex'],revenue_yoy_pct=(d['revenue']/d['prior']-1)*100,op_margin=d['op']/d['revenue']*100,net_margin=d['net']/d['revenue']*100,ebitda_margin=d['ebitda']/d['revenue']*100)
nb['ttm']['fcf']=nb['ttm']['cfo']-nb['ttm']['cash_capex']
for key,total in [('revenue',1962.1),('net',393.3),('ebitda',831.5),('op',-253.5),('cfo',4231.1),('cash_capex',15430.7)]:
 assert math.isclose(sum(nb[q][key] for q in ['q1','q2','q3']),total,abs_tol=.001),(key,total)
assert math.isclose(50.4+30.2-112.5-2.8-49.5+21.5+25.2,-37.5,abs_tol=.001)
assert math.isclose(9098.1-273-7635.2+7457.6-6.4,8641.1,abs_tol=.001)
assert 6904+1975-9836+7361==6404
# Same regular-session closing-price basis, not intraday peak-to-trough.
prices={'dates':['2026-11-10','2026-11-11','2026-11-12','2026-11-13'],'CRWV':[48.73,60.77,56.60,53.13],'NBIS':[134,154.69,128.64,115.88]}
for sym in ['CRWV','NBIS']:
 raw=(C/f'factcheck/data/2026-11-18/{sym.lower()}-prices.txt').read_text()
 for i,val in enumerate(prices[sym]):
  date='Nov '+str(int(prices['dates'][i][-2:]))+', 2026'
  m=re.search(re.escape(date)+r' ([\d,.]+) ([\d,.]+) ([\d,.]+) ([\d,.]+)',raw)
  assert m and float(m.group(4).replace(',',''))==val,(sym,date,val)
returns={s:{'nov11_to13':(prices[s][-1]/prices[s][1]-1)*100,'nov10_to13':(prices[s][-1]/prices[s][0]-1)*100,'nov11':(prices[s][1]/prices[s][0]-1)*100} for s in ['CRWV','NBIS']}
(N/'factcheck/q3-2026-results.json').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
(C/'factcheck/data/2026-11-18/closing-prices.json').write_text(json.dumps(prices,indent=2)+'\n')
audit={'checked_at':'2026-11-18','scope':'Full main-report migration: FY2023–2025 and 2026 Q1–Q3, current TTM and conditional valuation','quarter_reconciliations':'pass','income_and_cash_bridges':'pass','price_basis':'regular-session close, unadjusted','returns_pct':returns,'nbis_nonrecurring_revenue_pct':325/980.8*100,'nbis_revenue_ex325':980.8-325,'nbis_remaining_capex_funding_range_billion':[40*.15,45*.25],'annual_history':'FY2023/FY2024/FY2025 rendered in the final HTML; independently checked by audit_full_reports.py','valuation':'Conditional reverse DCF with Nov16 price, economic shares, discount/growth and delay sensitivity; not a forecast'}
(C/'factcheck/html-update-verification.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
fmt=lambda v:f'{v:,.1f}'
def table(headers,rows,caption=''):
 return f'<div class="table-wrap"><table><caption>{caption}</caption><thead><tr>'+''.join(f'<th>{h}</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<{ "th" if i==0 else "td"}>{v}</{ "th" if i==0 else "td"}>' for i,v in enumerate(row))+'</tr>' for row in rows)+'</tbody></table></div>'
def p(t,cl=''):return f'<p class="{cl}">{t}</p>'
def section(id,title,body):return f'<section id="{id}"><h2>{title}</h2>{body}</section>'
def fig(title,svg,note):return f'<figure><figcaption>{title}</figcaption>{svg}<p class="note">{note}</p></figure>'
colors=['#177e89','#d47b32','#5369a6','#819a56','#ad5472','#607d8b']
def bars(title,series,labels,unit,source):
 vals=[v for _,vs in series for v in vs];lo=min([0]+vals);hi=max([0]+vals);spread=hi-lo or 1;lo-=spread*.13 if lo<0 else 0;hi+=spread*.18
 y=lambda v:65+(hi-v)/(hi-lo)*235
 svg='<svg viewBox="0 0 960 365" role="img" aria-label="'+title+'"><rect width="960" height="365" fill="white"/>'
 for i in range(5):
  v=lo+(hi-lo)*i/4;yy=y(v);svg+=f'<path d="M85 {yy}H925" stroke="#dfe6e8"/><text x="75" y="{yy+4}" text-anchor="end">{v:,.0f}</text>'
 svg+=f'<path d="M85 {y(0)}H925" stroke="#78878d"/>'
 for j,(name,vs) in enumerate(series):
  svg+=f'<rect x="{90+j*245}" y="15" width="12" height="12" fill="{colors[j]}"/><text x="{108+j*245}" y="26">{name}</text>'
  for i,v in enumerate(vs):
   x=135+i*265+j*65; yy=y(max(0,v));h=abs(y(v)-y(0));svg+=f'<rect x="{x}" y="{yy}" width="40" height="{h}" fill="{colors[j]}"/><text x="{x+20}" y="{y(v)-8 if v>=0 else y(v)+20}" text-anchor="middle">{fmt(v)}</text>'
 for i,l in enumerate(labels):svg+=f'<text x="{155+i*265+(len(series)-1)*32.5}" y="350" text-anchor="middle">{l}</text>'
 return fig(title,svg+'</svg>',f'{unit}；{source}。完整精确值见相邻表，负值保留。')
def sankey(title,left,right,note):
 total=sum(v for _,v in left);assert math.isclose(total,sum(v for _,v in right),abs_tol=.01)
 H=400;gap=24;scale=(H-gap*(max(len(left),len(right))-1))/total
 def positions(items):
  ht=sum(v*scale for _,v in items)+gap*(len(items)-1);y=60+(H-ht)/2;out=[]
  for name,v in items:out.append((name,v,y,v*scale));y+=v*scale+gap
  return out
 a,b=positions(left),positions(right);svg=f'<svg viewBox="0 0 1100 510" role="img" aria-label="{title}"><rect width="1100" height="510" fill="white"/><text x="550" y="25" text-anchor="middle">汇总 {fmt(total)} M USD</text>'
 cy=60;cursor=cy
 for i,(name,v,y,h) in enumerate(a):
  svg+=f'<path d="M280 {y} C410 {y} 400 {cursor} 530 {cursor} L530 {cursor+h} C400 {cursor+h} 410 {y+h} 280 {y+h}Z" fill="{colors[i%6]}" opacity=".35"/><rect x="270" y="{y}" width="10" height="{h}" fill="{colors[i%6]}"/><text x="10" y="{y+h/2-3}">{name}</text><text x="10" y="{y+h/2+18}">{fmt(v)}</text>';cursor+=h
 svg+=f'<rect x="530" y="{cy}" width="12" height="{total*scale}" fill="#254551"/>'
 cursor=cy
 for i,(name,v,y,h) in enumerate(b):
  svg+=f'<path d="M542 {cursor} C670 {cursor} 660 {y} 790 {y} L790 {y+h} C660 {y+h} 670 {cursor+h} 542 {cursor+h}Z" fill="{colors[i%6]}" opacity=".35"/><rect x="790" y="{y}" width="10" height="{h}" fill="{colors[i%6]}"/><text x="820" y="{y+h/2-3}">{name}</text><text x="820" y="{y+h/2+18}">{fmt(v)}</text>';cursor+=h
 return fig(title,svg+'</svg>',note+'；单位 M USD。带宽与金额成比例；净额现金流保留净额边界。')
def hbars(title,rows,note):
 maxv=max(v for _,v in rows);svg='<svg viewBox="0 0 960 340" role="img" aria-label="'+title+'"><rect width="960" height="340" fill="white"/>'
 for i,(label,v) in enumerate(rows):
  y=25+i*49;svg+=f'<text x="15" y="{y+20}">{label}</text><rect x="180" y="{y}" width="{v/maxv*600}" height="28" fill="#177e89"/><text x="{190+v/maxv*600}" y="{y+20}">{fmt(v)}</text>'
 return fig(title,svg+'</svg>',note+'；横轴金额从0开始，M USD。')
def price_chart():
 svg='<svg viewBox="0 0 960 345" role="img" aria-label="两股收盘价归一化"><rect width="960" height="345" fill="white"/>'
 for v in [80,90,100,110,120,130]:
  y=290-(v-80)*4.5;svg+=f'<path d="M75 {y}H900" stroke="#dfe6e8"/><text x="65" y="{y+5}" text-anchor="end">{v}</text>'
 for j,s in enumerate(['CRWV','NBIS']):
  points=[(100+i*240,290-(v/prices[s][0]*100-80)*4.5) for i,v in enumerate(prices[s])]
  svg+=f'<polyline points="'+ ' '.join(f'{x},{y}' for x,y in points)+f'" fill="none" stroke="{colors[j]}" stroke-width="3"/>'
  for x,y in points:svg+=f'<circle cx="{x}" cy="{y}" r="5" fill="{colors[j]}"/>'
  svg+=f'<text x="{105+j*250}" y="25" fill="{colors[j]}">{s} · 11/10 = 100</text>'
 for i,d in enumerate(['11/10','11/11','11/12','11/13']):svg+=f'<text x="{100+i*240}" y="325" text-anchor="middle">{d}</text>'
 return fig('财报周：同一起点看相对表现',svg+'</svg>','美股正常交易时段收盘；2026-11-10＝100。纵轴80–130，非零起点。仅展示本次事件窗口，不是截至11/18的最新行情。来源：Quiver历史行情，11/18取得。')
comparison=table(['观察维度','CoreWeave（11/10披露）','Nebius（11/12披露）'],[
 ['Q3集团收入 / 环比','3,661.0 M / +42.2%','980.8 M / +68.4%；含325.0 M非经常收入'],
 ['2026收入公司指引','上调至13.0–13.3 B','原3.0–3.4 B区间的低端'],
 ['交付信号','active power >1.7 GW','部分第三方容量延至2027 H1；NJ余下批次2027 Q2'],
 ['2026资本开支公司指引','37–39 B（原35–39 B）','约27 B（原20–25 B）'],
 ['Q3 CFO / 自算FCF','1,975.0 / −7,466.0 M','−273.0 / −7,573.4 M'],
 ['9/30账面债务，不含租赁','46,873.0 M','14,190.8 M'],
 ['订单指标，定义不同','backlog 132.5 B；RPO 132.3 B','RPO 38.7 B'],
 ['解释边界','利润率与交付兑现改善','需求仍在，但时间表后移、融资规模上升']],'B＝十亿美元；M＝百万美元。指引为公司预测；CFO为经营现金流，FCF为本报告统一的CFO减现金CapEx，非公司全部非GAAP口径。')
price_rows=[]
for i,d in enumerate(prices['dates']):
 row=[d]
 for s in ['CRWV','NBIS']:
  change='基期' if i==0 else f'{(prices[s][i]/prices[s][i-1]-1)*100:+.2f}%'
  row.append(f'${prices[s][i]:.2f}<small>较前收盘：{change}</small>')
 price_rows.append(row)
price_content=p('<strong>【复算】✅ 属实：</strong>CoreWeave并非没有跌。11/11至11/13，CRWV为−12.57%，NBIS为−25.09%；若从CRWV财报公布前11/10收盘起算，到11/13分别为+9.03%和−13.52%。基期决定了“抗跌”的含义。')+price_chart()+table(['美东交易日','CRWV收盘','NBIS收盘'],price_rows,'美元/股；11/10为起点，之后涨跌均按相邻收盘价自行复算。')+p('<strong>【我的推演】</strong>CRWV这次先给出更快的收入兑现及上调指引；NBIS随后给出交付后移、全年收入靠近区间低端及更高投入。两家公司都在扩张，但财报对“多久产生收入、多久还要融资”的边际回答不同。这比把分化归结为AI需求强弱更贴近原始披露。')+p('此解释是候选机制，不能从两只股票的表现直接证明资金迁移。当前窗口未加入QQQ/行业组合和分钟级消息时戳，尚未剥离市场共同因子，不称为事件因果识别。','note')+comparison
CSS='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f2f5f4;color:#20313a;font:16px/1.75 -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif}main{max-width:1120px;margin:auto;padding:42px 38px;background:#fff}header{border-top:5px solid #177e89;padding-top:28px}h1{font-size:36px;line-height:1.25;letter-spacing:-1px;margin:8px 0 12px}h2{font-size:25px;line-height:1.4;margin:0 0 18px}h3{font-size:19px;margin:24px 0 10px}section{border-top:1px solid #dce5e4;padding-top:28px;margin-top:38px;scroll-margin-top:20px}p{margin:12px 0}a{color:#117784;text-underline-offset:3px;overflow-wrap:anywhere}.eyebrow{color:#49716f;font-size:13px;letter-spacing:2px}.lead{font-size:20px;color:#33565e}.tags{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0}.tags span{border:1px solid #cedbd8;border-radius:30px;padding:4px 12px;font-size:13px}.scope{border-left:4px solid #d47b32;background:#fff7ed;padding:12px 18px}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:24px 0}.card{background:#f1f6f5;padding:18px;border-radius:6px}.card strong{display:block;font-size:27px;color:#176f78}.card small{display:block;color:#52676f}.note,small{font-size:13px;color:#596e76}small{display:block}nav{background:#f1f6f5;padding:18px 22px;margin:25px 0}nav ol{columns:2;padding-left:0;margin:0;list-style:none}table{border-collapse:collapse;width:100%;min-width:620px;font-size:14px;font-variant-numeric:tabular-nums}caption{caption-side:top;text-align:left;font-size:13px;color:#52676f;padding:6px 0 10px}th,td{padding:11px 13px;border-bottom:1px solid #dee6e5;text-align:right;vertical-align:top}thead th:first-child{position:sticky;left:0;z-index:2}thead th{background:#eaf1ef;color:#294e55}tbody th{position:sticky;left:0;z-index:1;text-align:left;min-width:155px;background:#f7f9f8;font-weight:500}td{min-width:140px}td small{font-size:12px}.table-wrap{overflow-x:auto;margin:16px 0 22px}figure{margin:22px 0;background:#fff;border:1px solid #dce6e3;border-radius:6px;padding:14px;break-inside:avoid}figcaption{font-size:16px;font-weight:600;margin-bottom:12px}svg{display:block;width:100%;height:auto;min-width:960px;font:14px -apple-system,"PingFang SC",sans-serif}figure{overflow-x:auto}figure .note{min-width:0;margin:5px 0}ul,ol{padding-left:23px}footer{color:#60757c;font-size:13px;border-top:1px solid #ddd;margin-top:35px;padding-top:20px}.pill{color:#a35a1f}strong{font-weight:650}@media(max-width:650px){main{padding:24px 18px}h1{font-size:29px}.lead{font-size:18px}.cards{grid-template-columns:1fr}.card{padding:12px 16px}.card strong{font-size:24px}nav ol{columns:1}section{margin-top:28px}figure{padding:10px}table{font-size:13px}}@media print{@page{size:A4 landscape;margin:13mm}body{background:white;font-size:10pt}main{max-width:none;padding:0}h1{font-size:25pt}h2{font-size:17pt}h3{font-size:13pt}section{margin-top:18px;padding-top:15px}nav{display:none}table{min-width:0;font-size:9pt}th,td{min-width:0;padding:6px}.table-wrap,figure{overflow:visible}svg{min-width:0;max-height:120mm}tbody th,thead th:first-child{position:static}figure{padding:7px}thead{display:table-header-group}tr{break-inside:avoid}a{color:#245b65}.cards{grid-template-columns:repeat(3,1fr)}p{orphans:3;widows:3}}'''
chapters=[('business','1. 公司与业务'),('revenue','2. 营收与资金分配'),('finance','3. 盈利、负债、现金流与资本回报'),('customers','4. 客户、订单与需求'),('competition','5. 竞争对手'),('cycle','6. 行业景气'),('valuation','7. 估值与资金效率'),('governance','8. 治理与文化'),('moat','9. 护城河')]
cs='https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Third-Quarter-2026-Results/default.aspx'
ns='https://nebius.com/newsroom/nebius-reports-third-quarter-2026-financial-results'

def make(sym,d,project,peer):
 is_c=sym=='CRWV';name='CoreWeave' if is_c else 'Nebius';source='#source-c' if is_c else '#source-n';src=f'<a href="{source}">原始财报与口径</a>'
 lead='交付兑现改善了，巨额资本需求仍然存在。' if is_c else '需求仍强，交付后移提高了现金回收的不确定性。'
 top=f'<div class="eyebrow">AI CLOUD RESEARCH / {sym}</div><h1>{name}（{sym}）</h1><p class="lead">{lead}</p><div class="tags"><span>更新：2026-11-18</span><span>财报：2026 Q3 · 09-30</span><span>行情窗口：11-10 至 11-13</span><span>局部覆盖 · partial</span></div>'
 top+=p('本次完成Q3财报、2026年内单季序列、融资/交付变化及两股分化分析。此页为公司唯一HTML主入口，尚未完整迁移历史研究；三完整财年、全套估值与治理核验不在本轮完成范围。历史Markdown停更保留；HTML尚未接入research.yaml章节读取器。','scope')
 q=d['q3'];top+='<div class="cards">'+''.join(f'<div class="card">{label}<strong>{val}</strong><small>{note}</small></div>' for label,val,note in [('Q3收入 · M USD',fmt(q['revenue']),f'同比 +{q["revenue_yoy_pct"]:.1f}% · 见营收表'),('Q3经营利润率',f'{q["op_margin"]:.2f}%','GAAP；未扣融资成本 · 见盈利桥'),('Q3自算FCF · M USD',fmt(q['fcf']),'CFO − 现金CapEx · 见现金流表')])+'</div>'
 top+=p('<strong>【我的推演】</strong>'+('本轮财报提高了近期兑现的可信度，不能据此把CoreWeave视作低风险资产。利润改善主要发生在融资前，利息与现金投入仍显著超过经营利润。若交付转慢或融资收紧，订单增长会放大资金压力。' if is_c else '本轮问题是收入兑现时间及资本效率，而非已经证实的订单取消。需同时考察交付延后、非经常收入和新增融资，不能单看68%的收入环比或调整后EBITDA转强就推断现金回收已稳定。'))
 nav='<nav aria-label="报告目录"><ol>'+''.join(f'<li><a href="#{i}">{t}</a></li>' for i,t in chapters)+'<li><a href="#price-review">财报周股价分化</a></li><li><a href="#tracking">风险、跟踪与缺口</a></li><li><a href="#verification">核验与来源</a></li></ol></nav>'
 body=section('business',chapters[0][1],p('客户购买GPU集群、网络、存储和配套软件来训练或运行AI模型。公司先投入服务器、电力和机房，再按已签合同中的可用容量或使用量收款；签单、开机、确认收入和实际回款是四个不同阶段。')+p(('CoreWeave面向AI实验室、企业和超大规模云厂商提供专门为AI设计的云服务，软件与工程支持帮助客户减少集群调试和闲置时间。Q3集团收入3,661.0 M；本轮业绩稿没有提供可独立核验的软件收入/利润拆分，不能把W&B或Forge价值另行重复相加。' if is_c else 'Nebius AI cloud是核心业务；集团同时并表Avride、TripleTen，ClickHouse与Toloka为投资边界。Q3 AI cloud收入973.8 M，占集团99.29%，调整后EBITDA518.2 M；集团为465.8 M，两者不能混用。325.0 M轻资产初始部署收入也是集团收入的一部分，不能再叠加。')+f' {src}。')+p('机制示意：客户购买一批可用GPU → 公司交付集群 → 按约提供服务 → 确认收入/收款。此处箭头不代表量化现金分配。'))
 guidance=([
 ['Q3收入','3,661.0 M；同比+168.2%','2026全年13.0–13.3 B，上调'],['Q3调整后经营利润','379.0 M；利润率10.35%','2026全年1.275–1.375 B'],['2026资本开支','Q3现金CapEx 9,441.0 M，非全年同一口径','公司全年CapEx 37–39 B'],['上线容量','9/30 active power >1.7 GW','年末 >1.85 GW'],['年末ARR','非当期收入','20–21 B；公司预测']
 ] if is_c else [
 ['Q3收入','980.8 M；同比+571.3%','2026为3.0–3.4 B原区间低端'],['Q3调整后EBITDA','465.8 M；利润率47.49%','2026利润率约40%'],['2026资本开支','Q3现金CapEx 7,300.4 M','全年约27 B，原20–25 B'],['ARR目标时点','9/30 6.4 B，单月年化','原12月7–9 B → 2027年2月 >7 B'],['2027初步指引','尚未实现','收入12–13 B；CapEx 40–45 B；Q4税前盈亏平衡']])
 rev=p('以下实绩为2026 Q3，预测列为管理层指引；B＝十亿美元，M＝百万美元。指引不是已实现收入或已落实融资。')+table(['指标','已披露实绩','公司指引与预测期间'],guidance,f'来源：{name}财报及股东信，'+('2026-11-10' if is_c else '2026-11-12')+'。')
 rows=[]
 for title,key in [('集团收入','revenue')]+([] if is_c else [('AI cloud收入','cloud')]):
  cells=[title]
  for quarter in ['q1','q2','q3']:
   z=d[quarter];v=z[key];yoy=z['revenue_yoy_pct'] if key=='revenue' else (v/z['cloud_prior']-1)*100
   cells.append(f'{fmt(v)}<small>同比：+{yoy:.1f}%<br>占集团：{v/z["revenue"]*100:.2f}%</small>')
  rows.append(cells)
 rev+=table(['单季收入 · M USD','2026 Q1','2026 Q2','2026 Q3'],rows,'集团并表口径；同比基期为上年同季，非累计；占比以同季集团收入为分母。Nebius AI cloud为分部披露值，含内部交易，其他分部及抵销未在此加总，不能当全部对外销售占比。')
 rev+=bars('收入逐季增长：规模与质量要分开看',[('集团收入',[d[x]['revenue'] for x in ['q1','q2','q3']])],['2026 Q1','2026 Q2','2026 Q3'],'M USD',name+' Q1/Q2/Q3公司披露')
 rev+=p(('Q1较2025 Q4收入1,572.0 M增长32.19%，Q2环比23.92%，Q3环比42.17%。快速扩容与合同收入确认共同驱动增长；公司没有提供足以完整拆分量、价和组合效应的桥，不把增幅全部归给涨价。' if is_c else 'Q1较2025 Q4收入227.7 M增长75.23%，Q2环比45.94%，Q3环比68.44%。Q3有325.0 M非经常性轻资产初始部署收入，占收入33.14%；扣除后的算术余额为655.8 M。余额不是公司披露的经常性收入，也不能在缺少Q2同口径调整时称为有机增速。缺少相关成本，不能从EBITDA直接减325.0 M得到“正常化利润”。')+f' {src}。')
 income=[('收入成本',1183),('其他经营费用',2271),('经营利润',207)] if is_c else [('收入成本，不含折旧',219.7),('产品开发',118.6),('销售与管理',237.4),('折旧与摊销',354.7),('经营利润',50.4)]
 rev+=sankey('Q3收入如何形成经营利润', [('集团收入',q['revenue'])],income,'2026 Q3；集团GAAP。'+('其他经营费用＝总经营费用3,454−收入成本1,183；' if is_c else '折旧摊销单列，不能与CRWV收入成本口径直接比较；')+'融资和税项见下一章净利润桥')
 rev+=table(['Q3收入分配 · M USD','金额'],[[k,fmt(v)] for k,v in income],f'加总＝{fmt(q["revenue"])}；来源：{src}。')
 rev+=bars('增长消耗现金：CFO、现金投入与FCF',[('CFO',[d[x]['cfo'] for x in ['q1','q2','q3']]),('现金CapEx（支出为正）',[d[x]['cash_capex'] for x in ['q1','q2','q3']]),('FCF',[d[x]['fcf'] for x in ['q1','q2','q3']])],['2026 Q1','2026 Q2','2026 Q3'],'M USD',name+'现金流量表；FCF自行复算')
 rev+=p('FCF＝CFO−现金购建固定/无形资产（CRWV含资本化软件）。FCF不是第三种可加总用途；未扣收购、股权投资或偿债。公司CapEx指引可能含应计和交付口径，不能机械用“全年指引−前三季现金付款”推算Q4付款。分红回购不在此公式内；完整现金去向见<a href="#cash-flow">现金桥</a>。三完整财年本轮未重新核验，未将历史Markdown数字当作已核验HTML年度表。','note')
 body+=section('revenue',chapters[1][1],rev)
 fin=table(['单季 · M USD（比率除外）','2026 Q1','2026 Q2','2026 Q3'],[[label]+[f'{d[x][k]:.2f}%' if 'margin' in k else fmt(d[x][k]) for x in ['q1','q2','q3']] for label,k in [('经营利润','op'),('经营利润率','op_margin'),('净利润 / 亏损','net'),('净利率','net_margin'),('调整后EBITDA','ebitda'),('调整后EBITDA率','ebitda_margin'),('CFO','cfo'),('现金CapEx','cash_capex'),('自算FCF','fcf')]],f'来源：{src}及Q1/Q2原始披露；Nebius净利润采用持续经营口径。Q2现金流由H1−Q1拆季，EPS不作差分。')
 if not is_c:
  fin+=table(['AI cloud分部 · 单季','2026 Q1','2026 Q2','2026 Q3'],[['调整后EBITDA · M USD']+[fmt(d[x]['cloud_ebitda']) for x in ['q1','q2','q3']],['调整后EBITDA率']+[f"{d[x]['cloud_ebitda']/d[x]['cloud']*100:.2f}%" for x in ['q1','q2','q3']]],'来源：Q1/Q2分部披露及Q3股东信；分母为分部收入，不能把分部利润率套用集团。')
 fin+=bars('经营利润率与净利率' ,[('经营利润率',[d[x]['op_margin'] for x in ['q1','q2','q3']]),('净利率',[d[x]['net_margin'] for x in ['q1','q2','q3']])],['2026 Q1','2026 Q2','2026 Q3'],'百分比（%）',name+'GAAP利润表；自行复算')
 bridge=([['经营利润','207.0'],['净利息费用','−846.0'],['其他收入','+13.0'],['所得税','−83.0'],['净亏损','−709.0']] if is_c else [['经营利润','50.4'],['利息收入 / 费用','+30.2 / −112.5'],['权益法投资损失','−2.8'],['诱导转股费用','−49.5'],['其他收入','+21.5'],['税收收益','+25.2'],['持续经营净亏损','−37.5']])
 fin+='<h3>经营利润为什么没有变成净利润？</h3>'+table(['2026 Q3 · GAAP利润桥','M USD'],bridge,f'来源：{src}；✅ 加总勾稽。')
 fin+=p('调整后EBITDA不是现金利润。'+('Q3 EBITDA调节：−709净亏损 +1,889折旧摊销 +846净利息 +160股权激励 +83所得税 −13其他＝2,256 M。利息支出约为经营利润的4.09倍；Q4利息费用公司预期1.05–1.15 B，融资约束仍然突出。' if is_c else 'Q1净利621.2 M包含780.6 M投资重估收益，9M持续经营净利393.3 M不意味着云业务累计GAAP盈利。Q3净亏损包含49.5 M诱导转股费用及25.2 M税收收益；归因要保留非经营性与税项，不能将全部变化归给GPU利润。'))
 fin+='<h3>累计与TTM：独立期间</h3>'+table(['指标 · M USD','2026 9M（Q1–Q3）','TTM（2025 Q4＋2026 9M）'],[[label,fmt(sum(d[x][k] for x in ['q1','q2','q3'])),fmt(d['ttm'][k])] for label,k in [('收入','revenue'),('净利润 / 亏损','net'),('CFO','cfo'),('现金CapEx','cash_capex'),('自算FCF','fcf')]],'TTM截至2026-09-30；Nebius持续经营口径，含非现金投资收益，不能据正TTM净利套正常化PE。')
 b=d['balance'];fin+='<h3>最新资产负债：2026-09-30快照</h3>'+table(['项目 · M USD','金额'],[[label,fmt(b[k])] for label,k in [('现金及等价物','cash'),('受限现金','restricted_cash'),('账面债务，不含租赁','debt_ex_leases'),('净债务＝债务−非受限现金','net_debt_ex_leases'),('股东权益','equity')]],f'来源：{src}。净债务未扣受限现金，不含经营/融资租赁；不是全部债务到期兑付额。')
 fin+=p(('债务46,873 M已包含期内融资，不能再把9月完成约4.2 B可转债加一次。融资租赁649 M、经营租赁18,697 M另列，不与上述债务混算。10-Q明确9M没有ATM售股或签订collared forward，9/30剩余额度仍为35M股；授权不等于已发行；“授权数/旧股数”是新增股数相对旧股本比例，不等于新股发行后旧股东持股比例下降的同一分母。' if is_c else '账面债务14,190.8 M，净债务6,765.2 M；可转债账面值与到期赎回/增值本金不同。9/30递延收入9,409.2 M不是额外现金余额。8月5.75 B可转债已发行；Q3约1.0 B ATM净融资也已经发生，不能再作为未使用融资能力。10月Citi 3.5 B为期后信贷额度，不等于9/30现金增加3.5 B。')+f' {src}。')
 left=[('期初现金及受限现金',6904),('经营现金流净流入',1975),('融资现金流净流入',7361)] if is_c else [('期初现金及受限现金',9098.1),('融资现金流净流入',7457.6)]
 right=[('投资现金流净流出',9836),('期末现金及受限现金',6404)] if is_c else [('CFO净流出（CFO=−273）',273),('投资现金流净流出',7635.2),('汇率减少',6.4),('期末现金及受限现金',8641.1)]
 if is_c:
  maturity=[('2026余下季度',2433),('2027',10974),('2028',5479),('2029',4727),('2030',4247),('以后年度',19645)]
  assert sum(v for _,v in maturity)==47505
  fin+='<h3>债务本金时间表与尚未起租承诺</h3>'+hbars('9/30债务未来本金付款',maturity,'来源：Q3 10-Q附注10；各年度本金，非利息/租金，非账面值')+table(['截止12月31日的付款期间','本金 · M USD'],[[k,fmt(v)] for k,v in maturity]+[['合计',fmt(47505)]],'债务本金47,505 M与账面债务46,873 M的差632 M，不能混作同一口径；账面折价/发行成本等需另看调节。')
  fin+=p('另有未起租合同的估计未折现租金47.4 B，预计2026–2029开始、期限7–17年；它不是本季支出，也不是全部已确认租赁负债，不与债务本金简单相加作为“总债务”。这会约束未来现金回收。<a href="#source-c-10q">10-Q附注8/10</a>。')
 fin+='<h3 id="cash-flow">资本分配与完整现金桥</h3>'+sankey('Q3现金来源与去向：净额口径',left,right,'2026 Q3现金流量表；来源：'+name+'原始财报。期末现金含受限现金，不等于可自由支配余额')
 fin+=table(['现金桥 · M USD','金额（现金变化方向）'],[['期初现金及受限现金',fmt(left[0][1])],['CFO',fmt(q['cfo'])],['投资现金流',fmt(-9836 if is_c else -7635.2)],['融资现金流',fmt(7361 if is_c else 7457.6)],['汇率影响',fmt(0 if is_c else -6.4)],['期末现金及受限现金',fmt(6404 if is_c else 8641.1)]],'✅ 期初＋四类变动＝期末；图中净流出作为用途显示，未将负CFO伪装成经营现金来源。')
 fin+=p(('投资净流出9,836 M中，现金CapEx 9,441 M、合营投资410 M、战略投资35 M，剩余净流入50 M；融资净流入7,361 M中含发债10,301 M、偿债2,344 M、capped call 566 M及其他净流出30 M。capped call为限额抵消潜在转股稀释的期权交易，实际付款不等于偿债。' if is_c else '投资净流出7,635.2 M中，现金CapEx 7,300.4 M、票据应收款预付348.6 M，其他净流入13.8 M。融资净流入7,457.6 M含可转债5,750.0 M、库存股出售1,061.8 M、长期借款773.3 M；发行费用、偿债与其他合计净流出127.5 M。CFO已含递延收入增加3,434.0 M，同时应收账款变动占用3,761.8 M，不能把客户预付款当作“CFO之外的额外现金”再加一次。')+f' {src}。')
 fin+=p('资金主要流向GPU与机房扩张。已核阅Q3现金流表，未见现金分红或市场回购付款行；不把未列示扩大为“公司从未分红回购”。CRWV债务本金时间表已补；NBIS本轮尚未完成全部到期/担保附注核验。两家公司ROE与承诺全景仍待核，不以账面现金覆盖短债推断没有流动性风险。','note')
 body+=section('finance',chapters[2][1],fin)
 cust=(p('9/30 backlog为132.5 B，Q2末104.2 B，增加28.3 B。该指标包括RPO及管理层预计将在已承诺合同下确认的其他金额，仍需满足交付和服务可用性条件；不是全额可自由提款的订单。10-Q披露RPO为132.3 B，其中36%预计在未来24个月、38%在第25–48个月确认。')+p('财报列明与OpenAI、Cohere、Jane Street等的关系扩展，并新增Wayve等客户。11/9 Wayve多年度协议用于AI驾驶训练，是实际客户用途；合同金额未披露，不能自行填入新增订单金额。') if is_c else p('9/30 RPO为38.7 B，Q2末37.5 B，增加1.2 B（+3.20%）。Microsoft与Meta合同可支持资产融资，但交付条件与确认收入时间仍然关键；不能把“Q3开始至披露日的新承诺”全部塞入Q3末RPO。')+p('新泽西Microsoft容量预计年末交付超过一半，余下批次延至2027 Q2。股东信说明DataOne在永久电力切换前退役部分临时发电；Bloom燃料电池已有上线并继续扩容。公司称受影响合同仍在，不应把延期直接写成取消。'))
 body+=section('customers',chapters[3][1],cust+(p('10-Q另披露：本季部分合同变为可取消，将期初递延收入中的1.9 B转入客户负债。重分类不等于当季现金退款或全部订单被取消，但说明并非所有客户承诺都无条件锁定。须跟踪对应交付/可取消条款，不能只用backlog总额判断保障程度。<a href="#source-c-10q">附注2</a>。','scope') if is_c else '')+f'<p>来源：{src}。订单金额不等于本期收入、利润或已收到现金。</p>')
 body+=section('competition',chapters[4][1],p('neocloud相对AWS/Azure/Google Cloud的候选优势是集中于GPU集群、网络调优、机房交付与AI软件工作流，且可为客户提供大规模专属容量。hyperscaler则有更低成本的资本、多产品分发、企业关系和自研芯片选择。大客户既是买家也可能自建替代，合作不自动形成长期定价权。')+p(f'本轮与<a href="{peer}">{"Nebius" if is_c else "CoreWeave"}主报告</a>交叉阅读。下方比较按同一财报期对齐，但backlog与RPO、折旧分类、CapEx与融资条款并非同口径。')+comparison)
 body+=section('cycle',chapters[5][1],p('需求与有效供给要分开：签下电力、取得GPU不等于已并网、客户验收或满负荷收费。本轮两家公司的订单与扩张计划都没有证明行业需求崩塌，Nebius的交付约束却表明“有需求”仍可能无法按期确认收入。')+p(('CRWV active power >1.7 GW、contracted power >4.6 GW，均为9/30口径；不能再用8月中旬4.2 GW当最新数。9月短约约40 M USD/MW-year为特定3–6个月合同年化指标，既非全年实绩，也非整个电力组合的统一售价。' if is_c else 'Nebius股东信称新签1–5年合同ACV超过25 M USD/MW，较CRWV特定3–6个月短约约40 M USD/MW-year有不同期限、硬件、利用率与资产分工。不能直接判定单位产能售价或利润谁高；Q3轻资产模式还会改变同一收入对应的自有投入。')+f' {src}；<a href="#source-c-sept">9/17短约披露</a>。'))
 val=p('本轮仅评价兑现路径和资金效率，不给现价目标价、当前市值/EV或买卖结论。11/13股价仅用于事件窗口，不冒充11/18现价。两家公司尚未形成可比、稳定的完整年度经营正利润，未来PE反推Skill不适用；Nebius正TTM净利包含投资重估。')
 if not is_c:
  val+=p('【条件复算】2027 CapEx40–45 B ×（1−覆盖率75%–85%）＝6.00–11.25 B未被该项覆盖的区间。这不是新增股权融资需求：现金、其他债务、预付进度及资产融资提款均会改变结果。75%–85%是管理层融资预期，不是全部合同资金已经到账。Q4 2027税前盈亏平衡假设算力五年折旧且已计融资成本，不是FCF转正。')
 else:val+=p('Q3净利息846 M与经营利润207 M的落差，说明EBITDA扩张与股东可得现金仍隔着折旧、利息、营运资本和新增投入。预计未来三个月约9 B客户预付/押金属于未来资金来源，不能放进9/30现金或当成当季已收款。')
 val+=p('后续估值须固定2027–2029交付路径、GPU更新投入、利用率、每MW合同收入、折现率、债务及转股/ATM稀释，再检验一年延期和倍数收缩。本轮未建立全套期末股数、潜在稀释与跨年度融资模型，故现价隐含预期验收未通过，不能由短期股价反应推断“估值便宜”。','scope')
 body+=section('valuation',chapters[6][1],val)
 body+=section('governance',chapters[7][1],p(('CEO Michael Intrator领导的扩张要同时考核交付与资本约束。' if is_c else '创始人Arkady Volozh在股东信中承认交付时点后移并调整ARR口径。')+'本轮可核验行为是对融资、交付及指引的公开披露；不足以证明文化优劣。董事会资本回报门槛、关联方交易、双层股权控制及管理层激励仍待完整核验。'))
 if is_c:
  body+=p('Q3 10-Q中管理层认定披露控制在合理保证层面无效，原因是持续存在的财务报告内控重大缺陷；公司同时说明未造成财务报表重大错报。两项须一并阅读，既不能省略控制缺陷，也不能据此断言已发现财务造假。<a href="#source-c-10q">Item 4</a>。')
 body+=section('moat',chapters[8][1],table(['候选优势','本轮证据','证伪条件'],[['集群交付与软件','收入扩大、客户扩展；是规模证据，未单独证明转换成本','交付持续延期、客户迁移或单位利润下降'],['合同融资能力','预付与资产抵押融资支持扩张','预付条款恶化、融资利差上升或抵押折扣提高'],['电力与场地','已签容量与在建项目提供扩张选择','签约容量无法转成可收费容量']],'【我的推演】不对护城河作无数据评分；技术、供应链与资本优势须持续复核。'))
 body+=section('price-review','财报周复盘：为什么两股反应不同？',price_content)
 tracking=table(['风险 / 追踪项','最新观察','下一次复核条件'],[
 ['交付→收入',('active power >1.7 GW；年末目标>1.85 GW' if is_c else 'NJ余下批次2027 Q2；2月ARR目标>7 B'),'上线、验收或指引变化即重做收入兑现路径'],
 ['利润→现金',f'Q3 EBITDA {fmt(q["ebitda"])} M；FCF {fmt(q["fcf"])} M','核对预收、应收、CapEx现金支付和利用率'],
 ['融资/稀释',('债务46,873 M；35M股ATM授权' if is_c else '债务14,190.8 M；Q3已进行ATM融资'),'实际提款/发股、转股条件或利差变化即更新模型'],
 ['收入质量',('利润改善仍未覆盖净利息' if is_c else '325 M非经常性轻资产初始部署收入'),'区分新业务前期收入与持续服务收入'],
 ['比较解释','财报窗口存在公司差异，但市场因子未剥离','取得基准指数和分钟级时戳后再作因果判断']])
 tracking+='<h3>缺口分类</h3><ul><li>研究尚未完成：三完整财年迁移、NBIS到期结构与两家公司完整担保附注、股本与估值情景、治理；不表示公司未披露。</li><li>不可比：两家订单定义、折旧费用分类、短约与长约MW价格、CapEx口径；不能直接排名。</li><li>公司材料未单列：本轮所查业绩稿没有完整产品级现金流及费用归属，不能造业务资金分配。</li><li>工具限制：HTML尚未接入旧Markdown研究入口；本地HTML及唯一HTML索引是本轮阅读入口。</li></ul>'
 body+=section('tracking','主要风险、跟踪指标与待验证问题',tracking)
 source_rows=[['source-c','CoreWeave Q3业绩稿 · 2026-11-10',cs],['source-n','Nebius Q3官网发布 · 2026-11-12',ns],['source-n-release','Nebius Q3财务报表PDF · 2026-11-12',json.loads((N/'factcheck/data/q3-2026/sources.json').read_text())['release']],['source-n-letter','Nebius Q3股东信PDF · 2026-11-12',json.loads((N/'factcheck/data/q3-2026/sources.json').read_text())['letter']],['source-c-10q','CoreWeave Q3 10-Q · 2026-11月','https://www.sec.gov/Archives/edgar/data/1769628/000176962826000465/crwv-20260930.htm'],['source-c-sept','CoreWeave短约定价披露 · 2026-09-17','https://investors.coreweave.com/news/news-details/2026/CoreWeave-Continues-to-Contract-New-Compute-Capacity-at-Higher-Prices/default.aspx'],['source-c-q1','CoreWeave Q1业绩稿 · 2026-05-07','https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-First-Quarter-2026-Results/default.aspx'],['source-c-q2','CoreWeave Q2业绩稿 · 2026-08-11','https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx'],['source-c-fy','CoreWeave FY2025业绩稿 · 2026-02-26','https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Fourth-Quarter-and-Fiscal-Year-2025-Results/default.aspx'],['source-prices-c','CRWV收盘价 · 11/18取证','https://www.quiverquant.com/stock/CRWV/historical-prices/'],['source-prices-n','NBIS收盘价 · 11/18取证','https://www.quiverquant.com/stock/NBIS/historical-prices/'],['source-wayve','Wayve训练协议 · 2026-11-09','https://www.coreweave.com/news/coreweave-to-power-wayves-ai-driver-training-in-multi-year-agreement']]
 verification=p('验收日2026-11-18；任务类型为局部财报更新与事件比较，财务截至9/30，事件行情截至11/13正常时段收盘。公司预测均以11/10或11/12公开材料为准，不声称已覆盖11/18全部新消息。')
 visual_path=project/'factcheck/html-visual-checks.json'
 visual_note='未完成：尚未取得本轮浏览器验收记录。'
 if visual_path.exists():
  v=json.loads(visual_path.read_text())
  if v.get('checked_at')=='2026-11-18' and not v.get('anchors') and v['desktop']['scrollWidth']==v['desktop']['width'] and v['mobile']['scrollWidth']==v['mobile']['width'] and not v['print']['tableOverflow'] and not v['print']['figureOverflow']:
   visual_note='已检查：1440px桌面与390px窄屏均无页面横溢；目录/来源锚点无失效，核心图表离线且禁JavaScript可读；A4横向打印无表/图横溢。截图已人工复核；核验结果见factcheck/html-visual-checks.json，本地截图见factcheck/visual/。宽表及图在窄屏局部横向滚动，保留全部数值。'
 verification+=table(['验收项' ,'范围 / 结果 / 证据'],[
 ['原始资料','CRWV已保存Q1/Q2/Q3及FY2025业绩稿，另通过SEC网页核阅10-Q订单、ATM、到期、承诺和内控章节；选录事实保存在factcheck/data/q3-2026/10q-key-facts.json；NBIS已保存官网Q3财务PDF与股东信、既有Q1/Q2法定附件及FY2025业绩稿。NBIS SEC直连403后使用官网同版PDF，不写成未披露。'],
 ['季度覆盖矩阵','营收、经营/净利及利润率、EBITDA、CFO/现金CapEx/FCF：Q1/Q2/Q3齐备；收入同比基期为2025同季，Q1环比用2025 Q4；9M和TTM分表。✅ 已复算。'],
 ['会计与计算','单季合计与9M、TTM滚动、GAAP利润桥、完整现金桥及收盘涨跌均勾稽。复算脚本：CRWV/factcheck/build_html_reports.py；CRWV另有verify_q3_2026.py；各项目factcheck/q3-2026-results.json保存数值。'],
 ['图表同源','季度收入/利润率/现金图、收入利润桑基及现金桑基均由同一数值生成；现金桥含受限现金、净融资/投资、负CFO和汇率边界。'],
 ['解释保留','融资与稀释、单位MW价格比较限制、交付时点、非经常收入及“CRWV也下跌”的修正均在正文就近保留。'],
 ['离线与视觉',visual_note],
 ['结构与入口','每家公司一个reports/main.html，交叉链接；reports.py登记并check。历史research.yaml与Markdown保持原样，旧入口不代表本轮HTML。'],
 ['未通过项及影响','完整研究及当前估值未验收通过：三年历史、NBIS到期结构、潜在稀释/情景和完整治理待补。不影响本轮已核数据、融资/交付事实与事件窗口收益计算，限制投资定价结论。'],
 ['交付结论','局部更新交付；content_status=partial，非完整公司研究验收通过。']])
 verification+='<h3>数据与术语口径</h3>'+p('主体为美国Nasdaq上市普通股CRWV、NBIS，币种美元；两家公司财年12月结，Q3为7–9月。M＝百万，B＝十亿，GW＝1,000 MW。CFO为经营现金流；FCF是本报告CFO减现金CapEx；EBITDA为公司调整后息税折旧摊销前利润；ARR为单月收入年化，并非全年已实现收入；RPO为剩余履约义务；backlog按公司自己的合同估计定义；ATM为按市况分批售股机制；capped call为一定股价范围内抵消可转债稀释的期权安排。以上术语为本轮阅读所需简释。')
 verification+='<h3>原始来源与行情</h3><ul>'+''.join(f'<li id="{i}"><a href="{html.escape(u,quote=True)}">{title}</a></li>' for i,title,u in source_rows)+'</ul>'
 verification+=p('Nebius Q1/Q2及FY2025本轮使用既有研究目录保存的SEC/业绩稿原文：research/data/q1_2026_ex991.txt、q1_2026_ex992.txt、q2_2026_ex991.txt、q2_2026_ex992.txt、q4_2025_ex991.txt；Q2报表同时保有HTML原件。Q1/Q2营收与现金流由报表核对；Q3原始PDF保存于本项目factcheck/data/q3-2026。CRWV行情原始网页文本保存在CRWV/factcheck/data/2026-11-18。上述为证据存放位置，不代表网站已开放附件。','note')
 body+=section('verification','核验记录、口径与来源',verification)
 out='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+name+'：Q3财报与交付融资研究</title><style>'+CSS+'</style></head><body><main><header>'+top+'</header>'+nav+body+'<footer>唯一维护正文 · '+name+' · 2026-11-18局部更新 · <a href="'+peer+'">对照公司主报告</a></footer></main></body></html>'
 from full_report_content import upgrade
 out=upgrade(out,sym,table,p,section,bars)
 (project/'reports/main.html').write_text(out)
make('CRWV',cf,C,'../../Nebius公司研究/reports/main.html')
make('NBIS',nb,N,'../../CRWV/reports/main.html')
print(json.dumps(audit,ensure_ascii=False,indent=2))
