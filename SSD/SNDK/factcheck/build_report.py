"""Rebuild the sole HTML research text from sourced numeric inputs and module prose.
Run from any directory; no Markdown report is generated. Register pages via reports.py.
"""
from pathlib import Path
import json, subprocess, sys, hashlib
from html import escape
from datetime import date

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parent
ROOT=HERE.parents[2]
OUT=PROJECT/'reports'
IND=ROOT/'行业研究'/'NAND'/'reports'
PY=ROOT/'研究流程/tools/reports/.venv/bin/python'
TOOL=ROOT/'研究流程/tools/reports/reports.py'
DATE='2026-11-19'
S={
 'annual':('FY2026 10-K / 财务主表及附注','https://investor.sandisk.com/node/8171/html'),
 'old':('FY2025 10-K / 三年可比基数','https://investor.sandisk.com/static-files/11d54418-0d36-4853-955a-72db293e1da6'),
 'q':('FY2027 Q1 10-Q / 2026-10-30','https://investor.sandisk.com/static-files/c31aa9f9-d8e1-43e5-8642-360f5d0dad15'),
 'release':('Q1 业绩及 Q2 指引 / 2026-10-29','https://www.sec.gov/Archives/edgar/data/2023554/000162828026068243/sndkq1-27ex991xpressrelease.htm'),
 'call':('电话会媒体转录 / 2026-10-29','https://www.fool.com/earnings/call-transcripts/2026/10/30/sandisk-sndk-q1-2027-earnings-call-transcript/'),
 'spot':('TrendForce 现货调查 / 2026-11-18','https://www.trendforce.com/news/2026/11/18/insights-memory-spot-price-update-nand-spot-contract-price-gap-exceeds-20-amid-weak-demand/'),
 'outlook':('TrendForce 报告公开摘要 / 2026-11-18','https://www.trendforce.com/research/download/RP261118TU'),
 'weak':('TrendForce 公开摘要 / 2026-11-05','https://www.trendforce.com/research/download/RP261105BM'),
 'split':('公司拆股 FAQ','https://investor.sandisk.com/static-files/adc41ac6-9db7-4e6a-a29f-f73c1a0123e4'),
 'price':('Investing 历史行情 / 11-18 收盘','https://www.investing.com/equities/sandisk-corp-historical-data'),
 'consensus':('S&P Global 数据转引 / 10-30 快照','https://stockanalysis.com/stocks/sndk/forecast/'),
 'beat':('财报发布时预期 / StreetInsider','https://www.streetinsider.com/Earnings/Sandisk%2B%28SNDK%29%2BTops%2BQ1%2BEPS%2Bby%2B%242.36%2C%2BBeats%2Bon%2BRevenue%3B%2BOffers%2BQ2%2BGuidance/27257903.html'),
 'nintendo':('官方 Nintendo 产品采用与支持 / 2025-09-16','https://support-eu.sandisk.com/app/answers/detailweb/a_id/53259/~/learn-about-nintendo-licensed-microsd-express-and-microsd-memory-card-support'),
 'oem':('官方 OEM 销售支持说明 / 更新 2026-05-29','https://support-en.sandisk.com/app/answers/detailweb/a_id/7820/~/difference-between-original-equipment-manufacturer-%28oem%29-and-retail-%28rtl%29'),
 'vote':('股东大会 8-K / 2026-11-18','https://investor.sandisk.com/static-files/8465a6cb-1196-4b9f-ac15-96cb70b9d833')}
def src(*keys):return '<p class="source">来源：'+' · '.join(f'<a href="{S[k][1]}">{S[k][0]}</a>' for k in keys)+'</p>'
def p(s):return '<p>'+s+'</p>'
def h(id,t):return f'<h2 id="{id}">{t}</h2>'
def table(id,heads,rows):return f'<div class="table-wrap"><table id="{id}"><thead><tr>'+''.join('<th>'+str(x)+'</th>' for x in heads)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(x)+'</td>' for x in r)+'</tr>' for r in rows)+'</tbody></table></div>'
def num(x):return f'{x:,.2f}'
def pct(x):return f'{x:+.2f}%'
CSS='''*{box-sizing:border-box}body{margin:0;background:#f2f4f3;color:#172c32;font:17px/1.8 -apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}main{max-width:1120px;margin:auto;padding:42px 32px 80px}h1{font-size:36px;line-height:1.3;letter-spacing:-1px}h2{margin-top:44px;border-top:1px solid #ccd5d4;padding-top:22px;font-size:25px}.meta,.source,small{font-size:13px;color:#52676c}.answer{background:#113e49;color:#fff;padding:25px;border-radius:12px}.cards{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin:25px 0}.card{display:block;border:1px solid #c9d6d3;border-radius:12px;padding:23px;background:#fff;text-decoration:none;color:inherit}.card b{display:block;font-size:23px}.card:hover,.card:focus{outline:3px solid #2b8076}a{color:#126b68}table{width:100%;border-collapse:collapse;background:white;font-size:14px}td,th{padding:12px 15px;border-bottom:1px solid #dce2df;text-align:right;vertical-align:top}td:first-child,th:first-child{text-align:left;min-width:135px}th{background:#e3ece8}.table-wrap{overflow-x:auto;margin:18px 0}.chart{overflow-x:auto;background:white;padding:20px;border-radius:12px;margin:20px 0}svg{display:block;min-width:680px;width:100%;height:auto}svg text{font:13px sans-serif;fill:#233b41}.notice{padding:15px;border-left:4px solid #b96c32;background:#fff1df}nav{font-size:14px}footer{margin-top:38px;font-size:13px} @media(max-width:600px){main{padding:24px 18px}h1{font-size:28px}.cards{grid-template-columns:1fr}td,th{padding:10px}body{font-size:16px}}@media print{body{background:white;font-size:11pt}main{padding:0;max-width:none}nav{display:none}.cards{display:block}.card{margin:8px 0;break-inside:avoid}.table-wrap{overflow:visible}table{font-size:9pt}tr,svg{break-inside:avoid}svg{min-width:0}.chart{padding:8px}a{color:inherit}h2{break-after:avoid} @page{size:A4;margin:15mm}'''
def page(title,body,home='main.html'):
 meta='更新 2026-11-19　|　全球NAND与SSD · 证据截至2026-11-19' if title.startswith('NAND') else '更新 2026-11-19　|　财报 FY2027 Q1 · 2026-10-02　|　行情 2026-11-18 收盘 · USD'
 return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+'</title><style>'+CSS+'</style></head><body><main><nav><a href="'+home+'">← 研究首页</a></nav><h1>'+title+'</h1><p class="meta">'+meta+'</p>'+body+'<footer>原始披露 / 管理层指引 / 媒体转述 / 自行复算 / 我的推演分别标注。金额 M美元＝100万美元。静态离线报告。</footer></main></body></html>'
A={'2023':[6086,500,3637,1949], '2024':[6663,325,4069,2269], '2025':[7355,960,4127,2268], '2026':[20248,5153,12160,2935]}
Q={'2026Q1':[2308,269,1387,652],'2026Q4':[8965,2977,5432,556],'2027Q1':[11031,4802,5832,397]}
F={'2024':dict(rev=6663,gp=1072,op=-468,net=-672,cfo=-309,capex=166,sbc=149,cash=328,equity=11082), '2025':dict(rev=7355,gp=2212,op=-1377,net=-1641,cfo=84,capex=204,sbc=182,cash=1481,equity=9216), '2026':dict(rev=20248,gp=14472,op=12389,net=11433,cfo=11671,capex=177,sbc=232,cash=4762,equity=15736), '2027Q1':dict(rev=11031,gp=9378,op=8780,net=8101,cfo=6363,capex=54,sbc=91,cash=5136,equity=18134)}
PRICE=776.22;SHARES=142289365;MC=PRICE*SHARES/1e6
def bars(title,labels,series):
 colors=['#167d8d','#c8883b','#6f8b59'];mx=max(sum(v) for v in series);s=f'<div class="chart"><strong>{title} · M美元</strong><svg viewBox="0 0 900 260" role="img" aria-label="{title}">'
 for j,(label,vals) in enumerate(zip(labels,series)):
  x=130+j*230;y=210
  for k,v in enumerate(vals):
   ht=v/mx*155;s+=f'<rect x="{x}" y="{y-ht}" width="105" height="{ht}" fill="{colors[k]}"/>';y-=ht
  s+=f'<text x="{x}" y="235">{label}</text><text x="{x}" y="{y-10}">{sum(vals):,.0f}</text>'
 s+='<line x1="60" y1="210" x2="850" y2="210" stroke="#889"/><text x="60" y="208">0</text></svg>Datacenter 青 / Edge 金 / Consumer 绿；零基线，实绩。精确值及占比见下表。</div>';return s
def sankey(title,sources,targets,total):
 # Proportional aggregate allocations: no product-level cost assignment.
 scale=240/total; sy=50;ty=50;parts=[];nodes=[];msy=50;mty=50
 for label,v in sources:
  height=v*scale;cy=sy+height/2;my=msy+height/2;parts.append(f'<path d="M180,{cy} C300,{cy} 300,{my} 410,{my}" stroke="#a5c4c5" stroke-width="{height}" fill="none" opacity=".6"/>');nodes.append(f'<rect x="165" y="{sy}" width="15" height="{height}" fill="#167d8d"/><text x="5" y="{cy+4}">{label} {num(v)}</text>');sy+=height+24;msy+=height
 for label,v in targets:
  height=v*scale;cy=ty+height/2;my=mty+height/2;parts.append(f'<path d="M440,{my} C555,{my} 555,{cy} 670,{cy}" stroke="#b2c9b1" stroke-width="{height}" fill="none" opacity=".6"/>');nodes.append(f'<rect x="670" y="{ty}" width="15" height="{height}" fill="#537b58"/><text x="695" y="{cy+4}">{label} {num(v)}</text>');ty+=height+24;mty+=height
 return '<div class="chart"><strong>'+title+' · M美元</strong><svg viewBox="0 0 980 490" role="img" aria-label="'+title+'">'+''.join(parts)+''.join(nodes)+f'<rect x="410" y="50" width="30" height="240" fill="#173f49"/><text x="355" y="330">汇总 {num(total)}</text></svg><small>边宽统一按金额比例；公共汇总不代表可追溯逐笔资金或产品成本归属。</small></div>'
def audit(text):return h('verification','核验与限制')+p(text)+p('状态：已完成本页所列实绩的加总/比例复算；公司未披露与研究缺口分别保留。程序检查只验证对应算式与期间，不替代来源核验。')
def waterfall():
 values=[('净利润',8101),('非现金等',-391),('营运资本',-1347),('CFO',6363)]
 s='<div class="chart"><strong>FY2027 Q1 净利润→CFO · M美元</strong><svg viewBox="0 0 900 310" role="img" aria-label="净利润到经营现金流瀑布图">'
 running=0;scale=210/8500
 for i,(label,v) in enumerate(values):
  total=i in [0,3];start=0 if total else running;end=v if total else running+v
  y=250-max(start,end)*scale;height=abs(end-start)*scale;x=90+i*210
  s+=f'<rect x="{x}" y="{y}" width="105" height="{height}" fill="'+('#167d8d' if total else '#b76d40')+f'"/><text x="{x}" y="{y-12}">{v:+,}</text><text x="{x}" y="280">{label}</text>'
  running=end
  if i<3:s+=f'<line x1="{x+105}" y1="{250-end*scale}" x2="{x+210}" y2="{250-end*scale}" stroke="#889" stroke-dasharray="4 3"/>'
 return s+'<line x1="65" y1="250" x2="850" y2="250" stroke="#889"/><text x="45" y="254">0</text></svg><small>零基线；负调节以向下浮动柱表示；总额柱从零起。</small></div>'
def register(id,project,title,typ,slug=None):
 index=json.loads((ROOT/'研究流程/index/html-index.json').read_text())
 if any(x['report_id']==id for x in index['reports']):return
 args=[str(PY),str(TOOL),'create','--id',id,'--project',project,'--title',title,'--entity','company:sandisk' if project=='SSD/SNDK' else 'topic:industry-nand','--type',typ]
 if slug:args+=['--slug',slug]
 subprocess.run(args,check=True,capture_output=True)
modules = [
    ('industry-position', '行业、周期与竞争', '处于周期哪一段？AI与厂商扩产如何影响盈利？'),
    ('business-model', '业务、客户与订单', '谁付钱，NBM 到底保护什么？'),
    ('revenue-profit', '营收与盈利质量', '量增、涨价和产品组合各解释什么？'),
    ('cash-capital', '现金、融资与资本配置', '利润怎样变成现金，又流向哪里？'),
    ('governance', '主体沿革、治理与文化', '谁承担资本配置与周期风险？'),
    ('valuation', '估值与市场预期', '高盈利要维持多久，现价才有安全边际？'),
]
register('sndk-main','SSD/SNDK','闪迪：高利润与下行周期的再定价','company_research')
for slug,title,_ in modules:register('sndk-'+slug,'SSD/SNDK','闪迪｜'+title,'topic',slug)
register('industry-nand-overview','行业研究/NAND','NAND 行业研究','topic','nand')
register('industry-nand-cycle','行业研究/NAND','NAND｜价格、供需与竞争框架','topic','cycle')
OUT.mkdir(exist_ok=True);IND.mkdir(parents=True,exist_ok=True)

# Coverage is fixed before authoring: FY2024–26 and FY2027 Q1; same-period FY26 Q1/Q4 comparators.
coverage={'latest_annual':2026,'latest_period':'2027Q1','annual':['2024','2025','2026'],'interim':['2027Q1'],'comparators':['2026Q1','2026Q4'],'source_locations':{'annual':'FY26 10-K pp.46–48,58–61; FY25 10-K pp.48,60','interim':'FY27 Q1 10-Q pp.5–8,13–14,35–36'}}
(HERE/'coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2))
(HERE/'data').mkdir(exist_ok=True)
(HERE/'data'/'financial-inputs-2026-11-19.json').write_text(json.dumps({'unit':'M美元','facts':F,'revenue':A,'quarters':Q,'sources':S,'source_precision':'财务金额为公司百万美元整数；市场价格为美元小数；人工回原表核验','market':{'price':PRICE,'date':'2026-11-18','shares':SHARES,'shares_as_of':'2026-10-26'}},ensure_ascii=False,indent=2))

# Revenue module.
b='<section id="revenue">'+p('答案：数据中心正在成为第二个收入支柱；Edge 仍最大，但最新同比量缩价升。总收入爆发不能直接当作总 NAND 需求爆发。')
b+=h('guidance','最新实绩与指引先看')+table('guidance-table',['指标','FY2027 Q1 实际','FY2027 Q2 管理层指引'],[['集团营收',11031,'12,200–12,600'],['Non-GAAP 毛利率','85.1%','84.5%–85.5%'],['Non-GAAP EPS（美元，拆前）','49.51','55–57']])+src('release')
b+=p('指引发布 2026-10-29，不是已实现收入；中值营收环比 +12.41%、EPS +13.11%，毛利率中值低 0.1 个百分点。公司未给分市场数值指引。Q2 上年收入基数 3,025M（旧季度公告），中值同比约 +310%，但高增长主要反映比较基数与涨价，非同幅度出货增长。')
b+=h('income-flow','最新收入如何形成经营利润')+sankey('FY2027 Q1 收入→集团→成本与经营利润',[('Datacenter',4802),('Edge',5832),('Consumer',397)],[('营业成本',1653),('研发',384),('销售管理',214),('经营利润',8780)],11031)+src('q')
b+=p('从经营利润 8,780 加非经营净收益 539、扣所得税 1,218，得到 GAAP 净利润 8,101。非经营净收益含南亚科技投资收益 513，不能当 SSD 毛利；没有披露各终端利润，桑基不向产品分摊成本。收入确认后现金可能尚未到账，下一张图请看独立的 <a href="cash-capital.html#cash-use">现金用途与完整现金桥</a>。')
b+=h('annual','三完整财年营收结构')+p('单位：M美元；每格为金额 / 同比 / 同期集团占比。FY2024 的同比基数另取 FY2023；Cloud/Client 历史名称对应现 Datacenter/Edge。')+bars('年度营收结构',['FY2024','FY2025','FY2026'],[A[y][1:] for y in ['2024','2025','2026']])
rows=[]
for i,label in enumerate(['集团营收','Datacenter','Edge','Consumer']):
 cells=[]
 for y in ['2024','2025','2026']:
  v=A[y][i];prev=A[str(int(y)-1)][i];cells.append(f'{v:,.0f}<br>同比 {pct((v/prev-1)*100)}<br>占比 {v/A[y][0]*100:.2f}%')
 rows.append([label]+cells)
b+=table('annual-revenue',['指标','FY2024','FY2025','FY2026'],rows)+src('annual','old')
b+=h('quarter','本财年全部已披露单季与同季基数')+p('单位：M美元。FY2027 目前仅 Q1 已披露；不把 Q2 指引算入季度实绩。')
b+=table('quarter-revenue',['指标','FY2027 Q1'],[[label,f'{Q["2027Q1"][i]:,}<br>同比 {pct((Q["2027Q1"][i]/Q["2026Q1"][i]-1)*100)}<br>占比 {Q["2027Q1"][i]/11031*100:.2f}%'] for i,label in enumerate(['集团营收','Datacenter','Edge','Consumer'])])
b+=table('quarter-base',['指标','FY2026 Q1 同比基期','FY2026 Q4 环比基期','FY2027 Q1 环比'],[[label,Q['2026Q1'][i],Q['2026Q4'][i],pct((Q['2027Q1'][i]/Q['2026Q4'][i]-1)*100)] for i,label in enumerate(['集团','Datacenter','Edge','Consumer'])])+src('release')
b+=h('price-volume','同比量价：必须分开看三种终端')+table('volume',['市场','bit 同比（公司概数）','收入/GB 同比（含组合）','收入增量 M美元 / 对集团增收贡献'],[['Datacenter','接近 +330%','接近 +320%','4,533 / 51.97%'],['Edge','-20%','超过 +450%','4,445 / 50.96%'],['Consumer','下降超过70%','上升超过110%','-255 / -2.92%'],['集团','接近 +10%','未披露合并精确值','8,723 / 100%']])+src('q')
b+=p('Edge 量缩价升；消费量缩已压过提价。环比增量 2,066M 中数据中心贡献 1,825M / 88.33%；电话会称环比增长约六成来自量、四成来自价格，这是贡献比例，不是 bit/ASP 增速。量价概数不能精确相乘闭合，且产品组合无法单独量化。绝对 EB、TLC/QLC 产品收入与裸晶粒绝对 $/GB 均未披露。')+src('call')
b+=h('profit','盈利：三年历史与最新季度')
finrows=[]
for key,label in [('rev','营收'),('gp','毛利'),('op','营业利润'),('net','净利润'),('sbc','SBC 股权激励费用')]:finrows.append([label]+[num(F[y][key]) for y in ['2024','2025','2026']])
for key,label in [('gp','毛利率'),('op','营业利润率'),('net','净利率')]:finrows.append([label]+[f'{F[y][key]/F[y]["rev"]*100:.2f}%' for y in ['2024','2025','2026']])
b+=table('annual-profit',['指标（M美元/注明比率）','FY2024','FY2025','FY2026'],finrows)+src('annual')
b+=p('FY2025 营业亏损 1,377 含商誉减值 1,830；简单加回为经营盈利 453，但不代表完整调整后利润。非现金减值意味着历史收购价值受损，不能当作无经济成本。FY2026 毛利率71.47%到最新季度85.01%，反映价格/组合上行，不能直接当长期中枢。')
b+=p('年度利润变动用金额而非负基数增长率：FY2025经营亏损较FY2024扩大909M、净亏扩大969M；FY2026经营利润改善13,766M、净利润改善13,074M，均为扭亏。')
b+=table('q-profit',['指标（M美元；EPS美元）','FY2026 Q1','FY2026 Q4','FY2027 Q1'],[['营业利润',176,7037,8780],['GAAP净利润',112,6903,8101],['Non-GAAP EPS',1.22,39.25,49.51],['GAAP毛利率','29.8%','84.6%','85.0%']])+src('release')
b+=table('q-profit-growth',['Q1指标','同比复算','环比复算'],[['营业利润',pct((8780/176-1)*100),pct((8780/7037-1)*100)],['GAAP净利润',pct((8101/112-1)*100),pct((8101/6903-1)*100)],['Non-GAAP EPS',pct((49.51/1.22-1)*100),pct((49.51/39.25-1)*100)],['营业利润率',f'{8780/11031*100:.2f}%，提升{(8780/11031-176/2308)*100:.2f}个百分点',f'提升{(8780/11031-7037/8965)*100:.2f}个百分点'],['净利率',f'{8101/11031*100:.2f}%，提升{(8101/11031-112/2308)*100:.2f}个百分点',f'变动{(8101/11031-6903/8965)*100:.2f}个百分点']])
b+=p('TTM（截至2026-10-02）：FY2026＋FY2027 Q1−FY2026 Q1；收入28,971、营业利润20,993、净利润19,422M，营业/净利率72.46%/67.04%。增长仍强不意味着持续性已确认，南亚投资收益须与经营分开。')
b+=audit('营收 Skill 覆盖矩阵：FY2024–26、FY2027 Q1；同/环比基期就地展示。分市场和集团逐期加总，贡献分母分别为同比8,723/环比2,066。年度、单季、TTM分开；本页脚本结果见首页核验链接。')+'</section>'
(OUT/'revenue-profit.html').write_text(page('闪迪｜营收与盈利质量',b))

# Cash module.
b=p('答案：高利润已转成大量经营现金，但客户预付款、制造联盟投入和激励税款使“净利润＝可分配现金”不成立。')+h('annual-cash','三年与本财年现金底表')+p('单位：M美元。现金 CapEx 按购置 PP&E 实付毛额，资产出售回款另列，不与付款抵销。')
cashrows=lambda ys:[[label]+[num(F[y][key] if key!='fcf' else F[y]['cfo']-F[y]['capex']) for y in ys] for key,label in [('cfo','经营现金流 CFO'),('capex','现金资本开支'),('fcf','自由现金流 FCF')]]
b+=table('annual-cash-flow',['指标','FY2024','FY2025','FY2026'],cashrows(['2024','2025','2026']))+table('interim-cash-flow',['指标','FY2027 Q1'],cashrows(['2027Q1']))+src('annual','q')
b+=p('FY2024 PP&E 出售回款137M单独进入投资现金流；若用净额29M作投入，会得到FCF -338M。本表用毛付款166M，因此FCF -475M，口径差137M，不是算错。FY2025/26及最新季没有同类PP&E出售差额。')
b+=h('cash-use','最新经营现金的用途')+sankey('FY2027 Q1 CFO→投入/回购/余量（净额分配）',[('CFO',6363)],[('现金CapEx',54),('回购',5000),('余量',1309)],6363)+p('6,363−54＝FCF 6,309；再扣回购5,000，剩余1,309M。未付现金分红。余量不是现金净增加，仍须支付激励归属税、JV投入和其他投资；完整桥见下。')
b+=h('cash-bridge','完整期初至期末现金桥')
bridge=[('opening','期初现金',4762),('cfo','经营现金流',6363),('investing','投资现金流',-238),('financing','融资现金流',-5755),('fx','汇率影响',4),('closing','期末现金',5136)]
b+=table('cash-bridge-table',['项目','现金影响/余额 M美元'],[[l,num(v)] for _,l,v in bridge])+p('4,762＋6,363−238−5,755＋4＝5,136（✅勾稽）。投资净额：PP&E -54、JV贷款净额-148、短期投资-70、业务出售+34；融资：回购-5,000、激励归属代扣税-755。未将CFO已经扣除的研发/员工经营付款再扣一次。')+src('q')
b+=h('cash-quality','利润到经营现金与调整后FCF')+waterfall()+table('cash-adjust',['项目','Q1 M美元'],[['净利润',8101],['非现金及其他调节合计（复算）',-391],['营运资本变动合计（复算）',-1347],['经营现金流',6363],['现金CapEx',-54],['FCF',6309],['Flash Ventures净活动',-148],['NBM现金影响（公司调整口径）',-465],['调整后FCF',5696]])
b+=p('净利润到CFO含负调节项，不适合以正向分配桑基表达，采用带符号瀑布图与桥表；可表达的CFO分配已在上图展示。非现金调节含投资收益扣除-513、折旧+43、SBC+91等；应收增加-1,877、库存-318是主要现金占用。NBM -465为公司调节口径，不能强等同两项资产负债余额变化之和。调整后FCF环比+13.13%，率51.64%，低于Q4的56.2%。')+src('release','q')
b+=p('TTM CFO＝11,671＋6,363−488＝17,546M；现金CapEx＝177＋54−50＝181M；FCF＝17,365M。它仍含NBM客户付款影响，不能直接当长期股东收益。')
b+=h('balance','资产负债与投入义务')+table('balance-table',['期末指标 M美元','FY2024','FY2025','FY2026','FY2027 Q1'],[['现金',328,1481,4762,5136],['权益',11082,9216,15736,18134],['计息金融债务','无外部债务；WDC应付票据814',1849,0,0],['库存',1955,2079,2698,3016]])+src('old','annual','q')
b+=p('最新经营租赁负债201M（流动23、长期178），不能说零债务就零义务。租赁现值已与未来租金分开；EV基础口径仅扣现金、另列租赁及JV义务。JV一半固定成本与技术迁移出资，使合并报表CapEx低估体系资本强度。')+table('commitments',['Q1期末承诺 M美元','总额','FY2027余9月','FY2028–29','FY2030–31','更后'],[['JV',7141,2481,2975,1504,181],['采购与其他',5628,1191,3721,716,0]])+p('年末JV6,559/采购4,902均已上升；最新总额12,769，余9个月3,672M。承诺不是本期已付现金，不与CapEx指引重复相加，也不把全部总额当近期债务到期。')+src('q')
b+=h('allocation','资本分配与资金效率')+table('capital',['项目 M美元','FY2024','FY2025','FY2026','FY2027 Q1'],[['回购现金',0,0,4524,5000],['现金股权投资（南亚）',0,0,970,0],['SBC费用',149,182,232,91]])
b+=p('本季约3.2M股回购花5B，舍入均价约1,563美元，高于行情基准价；这暴露高景气时回购的择时风险。期末净股数约146M→144M，10月26日实际142.289365M；不能将SBC费用直接当新增股数。剩余授权10.5B并非已执行。南亚投资账面2,289M含重估，锁定限制使其不能全部当随时可用现金。gross CapEx 378M是较宽制造体系投入，不可与54M PP&E重复相加。')+src('q','call')
b+=p('FY2024 ROE=-672/平均(11,439,11,082)=-5.97%；FY2025=-1,641/平均(11,082,9,216)=-16.17%；FY2026=11,433/平均(9,216,15,736)=91.64%；Q1单季=8,101/平均(15,736,18,134)=47.84%，不年化。期初权益来自FY2025年报权益表。ROIC受JV非并表、租赁与客户预付资金影响，尚未构建调整投入资本，不能用简单PP&E分母伪造高回报。')
b+=audit('现金Skill对最终页面运行，年度2024–26及2027Q1，毛现金CapEx和现金桥已核；最新采购/JV承诺、三年ROE已补。调整ROIC因非并表制造体系尚未完成。')
(OUT/'cash-capital.html').write_text(page('闪迪｜现金、融资与资本配置',b))
ci={'entity':'Sandisk','unit':'M美元','latest_annual':2026,'latest_period':'2027Q1','annual_count':3,'annual':{'table':{'id':'annual-cash-flow'},'rows':{'cfo':'经营现金流 CFO','cash_capex':'现金资本开支','fcf':'自由现金流 FCF'},'source':S['annual'][1]+' cash flow PP&E purchases gross','capex_basis':'cash_paid','values':{y:{'cfo':F[y]['cfo'],'cash_capex':F[y]['capex'],'fcf':F[y]['cfo']-F[y]['capex']} for y in ['2024','2025','2026']}},'interim':{'table':{'id':'interim-cash-flow'},'rows':{'cfo':'经营现金流 CFO','cash_capex':'现金资本开支','fcf':'自由现金流 FCF'},'source':S['q'][1]+' p8','capex_basis':'cash_paid','values':{'2027Q1':{'cfo':6363,'cash_capex':54,'fcf':6309}}},'bridge':{'table':{'id':'cash-bridge-table'},'period':'2027Q1','cash_scope':'现金及现金等价物','source':S['q'][1]+' p8','required_roles':['opening','cfo','investing','financing','fx','closing'],'items':[{'role':r,'label':l,'expected':v} for r,l,v in bridge]}}
(HERE/'cash-input.json').write_text(json.dumps(ci,ensure_ascii=False,indent=2))

# Business & customer module: preserve earlier research questions, without duplicate narrative.
b=p('答案：闪迪把NAND晶圆加工成客户可用的存储产品，通过OEM、云客户和零售渠道收钱。它已从WDC独立，后者经营HDD；与铠侠共研/共投制造，但销售和客户不是同一家公司。')+h('transaction','一笔生意怎样完成')+p('采购晶圆与制造服务 → 封装/控制器/固件及认证 → 向客户交付合格SSD或嵌入式产品 → 控制权转移确认收入 → 赊销回款。NBM客户可在交货前预付/提供保证金：收到的钱先是负债，交货后才是收入。价格依容量、性能、认证和合同而异，不能以京东某一SKU反推公司实现ASP。')+src('annual','q')
b+=table('products',['收入池 / 最新季度','谁为何付钱','收费及产品','利润贡献边界'],[['Datacenter 4,802M /43.53%','云/企业客户为容量、延迟、可靠性和认证采购','服务器NVMe SSD，TLC性能型/QLC容量型','没有单列利润；企业SSD溢价是产品经济性判断'],['Edge 5,832M /52.87%','PC/手机/汽车OEM把NAND装入设备','客户端SSD、UFS/eMMC、汽车工业存储','内部PC/移动/汽车收入、bit与利润排名未披露'],['Consumer 397M /3.60%','终端消费者和渠道为升级/影像/游戏购买','零售SSD、移动SSD、SD/microSD、USB','零售价/促销不等于全公司ASP']])+src('release')
b+=h('customers','客户：实名采用和付款方分开')+table('customer-cases',['证据','采用/交易阶段','可确认与不可推断'],[['Nintendo Switch 2｜官方支持页，2025-09-16','联名microSD Express已上市并有支持流程','终端用户→零售/渠道→Sandisk；Nintendo是授权/平台伙伴，不证明它直接采购或是NBM客户'],['OEM售后说明｜2026-05-29','官方说明向Dell、Apple等电脑厂商/渠道批量销售的模式','可核验OEM交易类别；不能由举例推出当季收入或大客户排名'],['Q1 10-Q，2026-10-30','两名匿名客户分别占季度营收12%','集中度已高于FY2026全年无单客>10%的历史状态；不能猜其为OpenAI/Google']])+src('nintendo','oem','q')
b+=p('已查官方OEM支持、Nintendo采用与PS5产品资料。公开材料不足以列出当前eSSD/NBM客户实名及采购额；这是公司披露边界。实际消费销售链已确认，当前数据中心实名采用案例仍是研究缺口，不以HBF联盟成员替代客户。')
b+=h('nbm','NBM 长协：889亿美元不是保证收入')+table('contracts',['最新披露项目','FY2027 Q1期末','解释'],[['未履约义务交易价','88,900M','其中未开票87,400M；约20%预计12个月确认'],['合约负债','1,529M','流动777＋非流动752；不是已确认收入'],['可退还保证金','1,597M','不等于永久自由资金'],['合同bit覆盖（管理层/媒体转录）','FY2027约50%；FY2028约2/3','覆盖不是全产能售罄；待谈pipeline不算已签订单']])+src('q','call')
b+=p('约20%×88,900＝17,780M为预计12个月收入转化，非年度收入指引。期初59,800到88,900的净增加29,100M不等于新签订单：确认收入、范围和新协议需一并桥接。不能把历史93.9B媒体金额当最新RPO。条款涉及量承诺、最低财务保证与结构化定价；未公开所有客户退出、重谈及价格下限，故不能认定消除周期。')
b+=h('technology','保留原研究的技术边界')+table('tech',['问题','研究结论与边界'],[['NAND是不是一样','TLC每单元3bit，QLC为4bit；密度/耐久/速度不同，晶圆工艺、分档、控制器与认证使产品不能即刻替代'],['DWPD','保修期内每天可全盘写入次数；容量×DWPD决定写入额，不能只追最高DWPD'],['CMX / KV cache','HBM服务活跃计算，DRAM和SSD可作更低层缓存；SSD需求取决于保留窗口、命中、读写模式，非每柜固定配比'],['利润最高为何不全做eSSD','客户认证、控制器/固件、需求规模、供货承诺、良率与不同NAND特性约束；高毛利不等于无限需求'],['HBF / NBM','HBF为潜在高带宽闪存技术；NBM为商业协议，完全不同。未确认HBF收入，不加到现有营收']])
b+=audit('原MD §2、§4的业务/产品/量价边界迁至本页与营收模块；不再维护MD。客户/伙伴/匿名大客分开。当前云客户实名案例仍未完成，其余客户集中度及RPO已由最新10-Q核对。')
(OUT/'business-model.html').write_text(page('闪迪｜业务、客户与订单',b))

# Industry reusable background.
indbody=p('范围：全球NAND晶圆、客户端/企业SSD；不把DRAM/HBM或HDD并入同一个供需分母。更新2026-11-19，资料截止2026-11-18。')+h('cycle','行业回报：密度、认证与价格共同决定')+p('NAND原厂承担研发和制造资本，SSD厂商增加控制器、固件与认证价值。bit供给＝晶圆投入×每片可售bit×良率；层数/QLC迁移可在晶圆不扩张时增加bit。eSSD认证会延迟供给转换，消费级现货却先反映去库存。短缺推价带来的毛利不能直接当永久定价权。')
indbody+=h('price','最新证据：已出现实际价格转弱')+p('【TrendForce直接调查】11月18日称渠道库存消化、卖方降价，现货与合约价差超过20%；文中512Gb TLC平均14.238美元，但其周度标注为November 9，与刊载日期不一致，保留该时点限制，不当作11月18日单日成交价。')+src('spot')
indbody+=p('【机构预测/公开摘要，非已发生事实】11月18日更新认为中国CSP采购下修、消费规格降级与供给爬坡会使2027转过剩，合约降价较此前提前一季。仅取得公开摘要，未读付费2页模型，不声称知道精确供需缺口。11月5日公开摘要已指出模组库存压力与中国服务器采购偏谨慎，因此此前聊天“没有NAND转弱证据”至少从该日起应修正。')+src('outlook','weak')
indbody+=h('competition','可比与替代')+table('competitors',['主体','比较范围','边界'],[['Samsung / SK hynix-Solidigm / Micron','NAND成本、eSSD产品、认证、扩产','集团有DRAM/HBM，不能拿集团PE直接对标纯NAND'],['Kioxia','共研制造、独立销售，最接近纯Flash比较','与Sandisk制造供给可合并，营收利润不能重复计'],['YMTC','消费/模组晶粒与先进层数/扩产','新品公布不等于已售有效bit；高端客户认证需验证'],['WDC / Seagate','HDD容量存储替代','不是NAND供给，$/GB差与工作负载限制替换']])
indbody+=p('【多视角】TrendForce提供价格/供需调查；S&P Global的卖方盈利汇总仍预期FY2027盈利高增，两者在“当季利润强、未来压力加大”上可同时成立。供应商电话会表述为当事人利益相关观点，不能取代独立供需模型。报告不采用未复核的绝对EB模型或确定性产能售罄叙事。')+src('consensus','call')
indbody+=audit('最小行业研究：价值链、边界、价格证据、可比对象已核；付费供需完整模型未取得、各厂2027有效bit产能未独立重建，不能给精确过剩率。行业首页和模块同一主体登记。')
(IND/'cycle.html').write_text(page('NAND｜价格、供需与竞争框架',indbody,'nand.html'))
(IND/'nand.html').write_text(page('NAND 行业研究',p('行业入口｜全球NAND与SSD，资料截至2026-11-18。')+'<div class="cards"><a class="card" href="cycle.html"><b>价格、供需与竞争</b>现货转弱如何影响合约与不同终端？<p>渠道降价已发生，2027过剩仍是机构预测。</p></a></div>','nand.html'))
b=p('答案：闪迪的主要风险已从“DRAM新闻间接拖累”升级为“NAND现货实际转弱，能否向合约传导”。')+h('industry','行业基准')+p('<a href="../../../行业研究/NAND/reports/cycle.html">阅读独立NAND行业模块</a>，资料截至2026-11-18；边界为全球NAND/SSD，不含DRAM/HBM。')+p('对闪迪：Q1数据中心占43.53%，比全年25.45%更能抵御消费疲弱；但Edge占52.87%，量已同比缩20%，若其收入/GB回落，数据中心必须持续放量才能对冲。现货不是企业合约，更不是所有eSSD的同一价格，但会给下一轮谈判提供锚。')+h('moat','护城河按业务验收')+table('moat-table',['壁垒','证据与方向','侵蚀者及边界'],[['制造规模与工艺','Kioxia共研、共同制造降低单家公司资本负担','竞争者层数/QLC迁移降低成本；联盟不等于垄断'],['eSSD认证/固件','数据中心FY24 325M→FY26 5,153M→Q1 4,802M，采用规模上升','涨价与低基数也贡献营收；缺长期独立利润率证明'],['零售品牌/渠道','Nintendo、PS5兼容/授权产品证明市场采用','Consumer bit下降>70%，品牌无法隔离需求弹性'],['NBM承诺','合同负债与RPO提供跨期能见度','条款未全公开，未经历下行验证'],['HBF','潜在新品，不计收入估值','样品/标准不等于成熟生态或量产收益']])+src('annual','q')+audit('行业证据与公司终端结构对应；未以主观评分声称护城河。过去3年数据中心采用证据增强，但3–5年正常化ROIC/留存证据不足，护城河持续超额收益尚未验证。')
from cycle_research import build_cycle
new_cycle=build_cycle(page,p,h,table,IND,OUT)
b=new_cycle+b[b.index(h('moat','护城河按业务验收')):]
(OUT/'industry-position.html').write_text(page('闪迪｜行业、周期与竞争',b))

b=p('答案：分拆提高了纯NAND风险暴露，资本分配成为治理重点。高景气回购、JV固定义务、客户长协保护需要同时评价。')+h('boundary','主体沿革与并表')+p('2025-02-21从WDC分拆完成；分拆前财务为carve-out，分配WDC共享费用，与完整独立经营并非完全相同。FY2026含53周。Flash Ventures与Kioxia相关实体为非并表安排，投资、成本及义务仍会影响现金；南亚为金融投资，不能把其营收加进Sandisk。')+src('annual','old')
b+=h('governance','董事会、激励与经营文化证据')+p('11月17日股东大会选举八位董事，并通过薪酬咨询投票。薪酬投票赞成88,780,373、反对3,818,289，不含弃权/经纪未投票的赞成比例95.88%（复算）。投票通过不证明薪酬合理；Q1 SBC91M及755M激励归属代扣税是实际激励兑现/现金影响，二者不能相加当成当期薪酬费用。')+src('vote','q')
b+=p('【我的推演】文化不能只摘“资本纪律”自述。本季回购5B、上一年偿债1.9B是可核行为：偿债降低融资风险；约1,563的回购舍入均价在价格776附近时显得昂贵，需检验是否在周期峰值过度返现。JV即使少买wafer仍承担固定成本，客户合同可见度和制造承诺必须配对。')+h('gaps','治理未决')+p('董事独立性、最新主要股东投票控制、薪酬绩效权重和潜在关联利益需回2026 proxy逐项核验，当前只核实8-K投票及年报分拆/JV，不因“无单客>10%”推断股权分散。未查到处罚不等于证明无处罚；本轮未完成全司法辖区治理/诉讼检索。')+audit('主体边界与大会表决已核；治理文化行为证据有边界。完整治理验收未通过：proxy薪酬/控制权逐项尚未取得。首页明确内容为partial，不宣称全文完整核验。')
b=b.split(h('gaps','治理未决'))[0]+h('incentives','Proxy：控制监督与激励')+table('incentive-table',['项目','2026-10-06 Proxy披露及研究判断'],[['监督结构','CEO兼董事长；Cassidy为首席独董，除CEO外董事均独立。形式独立不等于决策无偏。'],['年度STI','利润指标50%、FCF25%、战略指标25%；资金上限200%。利润部分随非GAAP营业利润达到最高档，需警惕周期风口使门槛失去区分。'],['长期PSU','收入及非GAAP EPS各50%；CEO/CFO LTI目标分配PSU75%、RSU25%。EPS与回购相关，应评价每股价值而非只评价EPS提高。'],['受益股权','Proxy按9月4日股数列Vanguard7.6%；引用更早13G且处置权与投票权不同，不当作实时控制或资金流。']])+p('<a href="https://investor.sandisk.com/static-files/e7a5b974-b495-4f32-9ce0-74dea993d754">原始Proxy：董事会结构、STI、LTI及受益持股章节。</a>')+audit('已核原始proxy监督结构、激励权重、股权申报时点与大会投票；经营文化限于可核资本配置行为。未做全司法辖区诉讼检索，不据此宣称无处罚；SBC授予估值与已付激励税款不混同。')
(OUT/'governance.html').write_text(page('闪迪｜主体沿革、治理与文化',b))

# Confirmed conditional valuation Skill.
vi={'schema_version':1,'company':'Sandisk Corporation','share_basis':'SNDK普通股，2026-11-18拆股前；目标股数同单位不变','currency':'USD','price':PRICE,'price_date':'2026-11-18','net_profit':11433,'profit_unit':'M','profit_period_start':'2025-06-28','profit_period_end':'2026-07-03','profit_basis':'FY2026 GAAP归属普通股年度利润；含投资收益，持续性另作压力情景，不作为正常化利润','current_shares':SHARES,'target_shares':SHARES,'target_fiscal_year':'FY2029','target_date':'2029-06-29','required_return':.10,'target_pe':10,'sensitivity_pe':[8,10,12],'assumptions_confirmed':True,'applicability':{'comparable_profit':True,'major_capital_changes':False,'special_industry':False},'evidence':{'price':{'source':S['price'][1],'status':'verified','source_date':'2026-11-18','currency':'USD'},'net_profit':{'source':S['annual'][1],'status':'verified','source_date':'2026-08-17','currency':'USD'},'current_shares':{'source':S['q'][1]+' cover 2026-10-26','status':'verified','source_date':'2026-10-30','currency':'shares'}}}
(HERE/'valuation-input.json').write_text(json.dumps(vi,ensure_ascii=False,indent=2))
skill=Path('/Users/vinci/.codex/skills/implied-valuation/scripts/valuation.py')
result=HERE/'valuation-2026-11-19.html'
if not result.exists():subprocess.run([sys.executable,str(skill),'--input',str(HERE/'valuation-input.json'),'--output',str(result)],check=True,capture_output=True)
skill_result=json.loads(result.with_suffix('.json').read_text())
years=skill_result['base']['return_years']
b=p('答案：按短期高盈利现价倍数低；但现货转弱使“低PE是否周期陷阱”比“是否超预期”更重要。底部尚未确认。')+h('quote','行情与一致预期')+table('quote',['输入','值及口径'],[['价格',f'{PRICE}美元；2026-11-18收盘，拆前'],['实际股数','142,289,365；10月26日，非季度稀释154M'],['估计市值',f'{MC:,.2f}M美元；价格×跨时点实际股数'],['基础EV（不扣股权投资）',f'{MC-5136:,.2f}M；市值−期末现金，未加经营租赁201M'],['TTM净利/市值利润比',f'19,422M / {MC/19422:.2f}倍；含投资收益'],['Q2 EPS中值机械年化',f'56×4＝224；价格/224＝{PRICE/224:.2f}倍，不是全年预测']])+src('price','q','release')
b+=p('2026-10-30卖方快照FY2027 EPS227.80、FY2028 EPS287.26，现价分别3.41/2.70倍；这是旧预测快照，不冒充11月19日最新共识。财报时Q1 EPS49.51对预期47.15高5.0%；Q2指引中值收入12.4B对12.29B仅高0.9%。公开预期已很高，不能从股价下跌反推“财报低于预期”。')+src('consensus','beat')
b+=h('implied','已确认条件反推：FY2029赚多少才支撑现价')+p('用户2026-11-19确认：必要回报10%，目标FY2029，终值PE10倍/敏感性8、12倍，目标股数不变，延迟一年/两年。Skill已执行；拆股仅将每股数除8、股数乘8，不算经济稀释。价格到目标约2.61年，利润增长基期FY2026末到FY2029末约3年，两个时钟不同。')
vrows=[]
for delay in [0,1,2]:
 for pe in [8,10,12]:
  exact=next(x for x in skill_result['sensitivity'] if x['pe']==pe)['scenarios'][delay]
  req=exact['required_profit'];growth=exact['profit_cagr']
  vrows.append([f'FY{2029+delay}',f'{pe}x',num(req),pct(growth*100)])
b+=table('implied-table',['兑现财年','终值PE','所需全年利润 M美元','相对FY2026年复合变化'],vrows)+p('本表直接采用Skill同一结果，回报与利润增长分别按各自基期日数/365计时。公式：所需净利润＝现价×目标股数×(1+r)^t÷PE。模型不含期间分红，回购仅由固定目标股数假设体现；不额外加净现金，避免股权PE口径重复。它不是市场唯一预期。')
b+=h('required-revenue','把所需利润翻译为收入与产品条件')
required=skill_result['base']['required_profit']
b+=table('required-revenue-values',['FY2029净利率假设','所需营收 M美元','较FY2026','较最新TTM'],[[f'{m:.0%}',num(required/m),pct((required/m/20248-1)*100),pct((required/m/28971-1)*100)] for m in [.20,.30,.50,.60]])
b+=p('以上净利率是研究假设，非公司指引。10倍终值PE对应全年净利14,165.50M；若正常化净利率30%，需要收入47,218.33M，比FY2026高133.20%；若维持50%，只需28,331.00M，接近最新TTM28,971M。核心因此是高价利润能保留多少。假设FY2029 Edge/Consumer合计20,000M、集团净利率30%，数据中心必须贡献约27,218M，约为Q1收入机械年化19,208M的1.42倍；这是集团条件桥，不假造各业务独立利润率。企业SSD认证、有效bit供给、NBM价格条款必须共同支持该路径。目标日期2029-06-29为模型计时假设，并非公司已公布的FY2029结账日。')
b+=h('scenarios','经营结果、兑现延迟与倍数收缩')
sc=[]
for name,year,rev,margin,pe in [('既有高盈利延续',2029,50000,.55,10),('数据中心放量且高价较稳',2029,60000,.60,12),('消费/Edge降价、部分长协保护',2029,40000,.30,10),('量增不足抵降价且PE收缩',2029,35000,.20,8),('放量延迟、投入仍发生',2030,40000,.30,10)]:
 profit=rev*margin;t=years+year-2029;pv=profit*1e6/SHARES*pe/(1.1**t)
 sc.append([name,str(year),num(rev),f'{margin*100:.0f}%',num(profit),f'{pe}x',num(pv),pct((pv/PRICE-1)*100)])
b+=table('scenarios-table',['研究假设（非预测）','FY','营收 M美元','净利率','净利润 M美元','PE','折现每股价值美元','较现价'],sc)
b+=p('全部为研究者条件情景：终值现值占100%，不含期间分红，因此高依赖终值。HBF不单列价值，eSSD放量已有收入不能都称新业务。FY2029所需利润可用Edge/Datacenter收入和利润率多组合满足，无法唯一识别市场看法。延迟情景保留投入与费用、价格竞争，利润率30%而非简单把高价季度平移；只要期间FCF不能覆盖资本支出，固定股数还会低估融资稀释风险。')
b+=h('tape','近期行情与底部验证')+table('prices',['日期','拆前收盘美元','证据含义'],[['11-05',806.43,'恐慌低点'],['11-11',977.69,'反弹21.24%'],['11-17',797.24,'盘中749.39，跌破前低'],['11-18',776.22,'较反弹高点-20.61%；连续五日下跌']])+src('price')
b+=p('事实：反弹失败，749–754附近仅为近期交易低点；收复800–840并相对美光/半导体增强，才提高企稳证据。价格低不自动构成底部。宏观及被动资金可能放大波动，但缺逐笔资金/买方调查不能归因到某机构正在卖。11月20日拟拆股后交易，776.22对应97.03；上述区间都除8。')+src('split')
b+=audit('implied-valuation输入由用户确认；以FY2026完整正利润为条件基数，投资收益和周期峰值局限已明确。估值模型算术与情景成立不等于目标价有效。当前共识时间序列、独立同业正常化估值、买方隐含预期尚未完成，不能断言现价已充分计入衰退或底部。')
b+=h('cycle-profit','周期怎样进入利润：量、价、成本一起算')+p('【本文压力模型，非预测】以Q1收入11,031M、成本1,653M、经营费用598M为基数；假设未来可售bit比基期高22%、每bit成本降15%、经营费用增10%，各产品组合/合同覆盖不变。22%取自铠侠长期GB目标，仅作情景参数，不是闪迪单季指引；收入/GB变化不等于现货变化。')
cycle_rows=[]
for asp in [-.10,-.20,-.40,-.60]:
 r=11031*1.22*(1+asp);c=1653*1.22*.85;op=r-c-598*1.10
 cycle_rows.append([f'{asp:.0%}',num(r),num(op),f'{op/r*100:.2f}%',pct((op/8780-1)*100)])
b+=table('cycle-profit-values',['收入/GB变化假设','季度收入 M美元','季度经营利润 M美元','经营利润率','较基期经营利润'],cycle_rows)
b+=src('q')
b+=p('公式：收入＝基期收入×bit倍数×收入/GB倍数；成本＝基期成本×bit倍数×单位成本倍数；再扣经营费用。模型把收入近似为bit×价，忽略其他服务/组合变化。即使降价20%，在量增与降成本兑现时，经营利润只下降约4.4%；不能把现货跌20%直接推成利润崩塌。若bit不增且单位成本不降、费用仍增10%，降价20%则使经营利润下降约25.8%。')
b+=p('这解释为何尚不能只靠“强周期”直接做空：极高毛利提供缓冲，NBM可能保护部分收入。反之，不能把当前利润年化后按低PE买入：FY2029单位利润和现金投入仍须验证。前面50–60%净利率情景属于高价延续，非默认正常化；20–30%情景是更深周期回落，不是从单次现货跌幅线性推导。<a href="../../../行业研究/NAND/reports/cycle.html#balance-model">行业供需假设及反证</a>。')
b=b.replace('<h2 id="quote">','<h2 id="quote-overview">')
audit_start=b.index('<h2 id="verification">');model_start=b.index('<h2 id="cycle-profit">')
b=b[:audit_start]+b[model_start:]+b[audit_start:model_start]
(OUT/'valuation.html').write_text(page('闪迪｜估值与市场预期',b))

cards=''.join(f'<a class="card" href="{slug}.html"><b>{title}</b>{question}<p>'+{'valuation':'反弹失败；当前估值需用周期回落压力检验。','revenue-profit':'数据中心占43.53%，Edge同比量缩20%。','cash-capital':'CFO6,363M，调整后FCF5,696M；回购5,000M。','business-model':'最新RPO88,900M；两名匿名客户各占12%。','industry-position':'NAND现货已走弱，不能沿用单纯情绪下跌判断。','governance':'资本分配行为可核，proxy控制权/激励细项仍有缺口。'}[slug]+'</p></a>' for slug,title,question in modules)
b='<div class="answer"><b>高利润已兑现，市场正在下调持续时间。</b><p>【我的推演】闪迪值得用正常化现金流重新估值；NAND现货转弱和反弹失败，使“短期便宜”和“底部已确认”不能画等号。研究主问题：企业级SSD/长协能否在FY2027–2029抵消Edge及消费端的价格回落？</p></div>'+cards
b=b.replace('高利润已兑现，市场正在下调持续时间。','高景气后段：AI抬高需求，供给响应仍可能带来下行。').replace('【我的推演】闪迪值得用正常化现金流重新估值；NAND现货转弱和反弹失败，使“短期便宜”和“底部已确认”不能画等号。','【研究判断】现货已转弱、合约涨幅预测下修；五大制造体系存在不同程度扩供，2027总bit供给预计增长25–30%。AI增长未必足以抵消中国采购与消费走弱。').replace('NAND现货已走弱，不能沿用单纯情绪下跌判断。','高景气后段；AI未消除周期，2027有效bit供给预计加速。')
b+=h('status','研究状态与关键反证')+p('可阅读交付；内容核验 partial。三年营收/利润/现金及最新季度底表已回原始披露，最新行业证据改变旧结论；尚未达到整篇完整研究验收。旧Markdown停更保留，不同步正文；旧research.yaml仍仅定位历史MD，HTML通过唯一索引读取。')
b+=table('tracking',['变量','已核观察值','改变判断的条件'],[['价格/行业','11月18日现货合约价差>20%','合约价格实际下调/止跌，区分中国与北美、TLC/QLC'],['业务需求','数据中心43.53%、Edge52.87%','eSSD放量能否抵消费降价；总bit与价格分开'],['长协','RPO88.9B，20%预计12个月确认','实际转收入/退款/重谈，非pipeline金额'],['现金','Q1调整后FCF率51.64%','投入增加后仍兑现，预付款与经营现金分开'],['股价','11月18日776.22；低点749.39','更高低点、相对强度和成交承接，不作自动买卖信号']])
b+=h('coverage','十一项覆盖与验收入口')+table('coverage-table',['要求','实际页面','状态'],[['业务/客户/订单','<a href="business-model.html">业务模块</a>','机制与RPO核验；当前云客户实名有缺口'],['营收/盈利','<a href="revenue-profit.html#verification">财务核验</a>','FY2024–26及FY2027Q1已覆盖'],['现金/投入/资本分配','<a href="cash-capital.html#verification">现金核验</a>','现金桥及核心底表核验；承诺滚动/ROIC不足'],['行业/竞争/护城河','<a href="industry-position.html">行业与竞争</a>','最小行业研究；2027绝对bit供需模型未独立重建'],['估值/资金效率','<a href="valuation.html#verification">估值核验</a>','条件反推与延迟，非共识归因'],['治理文化','<a href="governance.html#verification">治理核验</a>','控制权/激励细项未完成']])
b+=h('verification','本轮交付核验记录')+p('日期2026-11-19；范围：新HTML主入口与六模块，包含历史研究重构、最新财报及行业修正。行情截至11月18日，财报截至10月2日。源表、脚本和检查结果保存在本项目factcheck；首页仅给证据定位，不复制第二份研究正文。')
b+=p('本轮纠错：原版行业研究不足以回答强周期公司的核心问题。本次重写独立行业页、公司行业判断；新增周期证据矩阵、AI多空机制、五大制造体系项目表、2027供需指数模型及量价成本利润压力表。行业证据更新至11月19日，财务/行情截止未改变。机构预测与公司计划分列，不宣称已精确测量2027供需缺口。复算证据：factcheck/cycle-evidence-2026-11-19.json；视觉及结构沿用本轮检查输出。')
b+=p('迁移保留：旧MD的NAND用途、Edge细分披露边界、bit绝对值缺失、TLC/QLC/DWPD/CMX、NBM与HBF区别移到业务/营收；现金/JV义务移至现金；旧估值不冒充现价；KV缓存定量专题保留历史证据，本报告不重算GPU机柜容量。新增修正：两个客户各12%、RPO88.9B、NAND现货走弱，不能只保留旧财报乐观结论。')
b+=p('已完成源表和计算核对：分市场加总、同比/占比、TTM、费用桥、现金桥；营收与现金Skill对最终页面运行，结果由factcheck/验收脚本记录。收入利润与CFO分配均已用同源桑基；负数利润-CFO调节以带符号表兜底。结构与视觉结果运行后记录，未核验的项目不升级verified。')
b+=p('未通过项：①研究尚未完成：proxy控制权/薪酬权重、最新全部采购/JV承诺滚动、FY2024期初权益、可比ROIC和当前eSSD实名案例；②公司未披露：终端产品利润、Edge子业务份额、绝对EB及全部NBM条款；③不可比：分拆前carve-out与53周财年；④不适用：HBF未形成可确认收入，不单列估值。上述缺口影响跨周期护城河与长期价值确定性，不能称完整研究全部通过。')
b=b.replace('proxy控制权/薪酬权重、最新全部采购/JV承诺滚动、FY2024期初权益、可比ROIC和当前eSSD实名案例','可比调整ROIC、当前eSSD实名案例、最新卖方修订序列和2027绝对bit供需模型')
b=b.replace('现金桥及核心底表核验；承诺滚动/ROIC不足','现金桥、最新承诺、ROE已核；调整ROIC不足').replace('控制权/激励细项未完成','监督结构及激励权重已核；更早股权申报不当实时控制')
b=b.replace('proxy控制权/激励细项仍有缺口','Proxy监督与激励权重已核，需跟踪回购每股价值')
b=b.replace('三年营收/利润/现金及最新季度底表已回原始披露','三年营收/利润/现金、最新季度、治理激励及最新投入义务已回原始披露')
b=b.replace('最小行业研究；2027绝对bit供需模型未独立重建','周期/AI/厂商扩供及指数模型已补；绝对EB与良率未披露')
b=b.replace('11月18日现货合约价差>20%','11月19日：现货已回调>20%，4Q合约涨幅预测下修至8–13%')
b+=p('新增供给跟踪：2027 NAND bit供给+25–30%、行业CapEx299亿美元均为机构预测，后续以实际设备/产出、价格与库存验证；各厂项目、来源及假设见<a href="../../../行业研究/NAND/reports/cycle.html#expansion">厂商扩供表</a>和<a href="../../../行业研究/NAND/reports/cycle.html#balance-model">供需敏感性</a>。')
b=b.replace('负数利润-CFO调节以带符号表兜底。结构与视觉结果运行后记录，未核验的项目不升级verified。','负数利润-CFO调节以瀑布图及带符号表展示。最终期间检查见factcheck/revenue-coverage.json，现金复算见cash-verification.json，结构/入口见report-index-verification.json与entry-verification.json；各检查不替代内容核验。')
vcheck=HERE/'visual-checks.json'
if vcheck.exists():b+=h('visual-audit','实际视觉检查')+p('本地Chrome断网打开所有九页，桌面1440px、窄屏390px和A4打印分别检查，详情及逐页指标在factcheck/visual-checks.json。页面无网络展示依赖；横向财务表保留滚动，打印保留完整表列。')
(OUT/'main.html').write_text(page('闪迪 SNDK｜高利润与下行周期的再定价',b))

# Minimal research input audit, no duplicated report text.
checks=[]
for y,vals in A.items():assert sum(vals[1:])==vals[0];checks.append('annual '+y+' sum ok')
for y,vals in Q.items():assert sum(vals[1:])==vals[0];checks.append('quarter '+y+' sum ok')
assert 4762+6363-238-5755+4==5136
assert 8101-391-1347==6363
assert 6309-148-465==5696
(HERE/'calculation-audit.json').write_text(json.dumps({'date':DATE,'checks':checks+['cash bridge ok','profit CFO bridge ok','adjusted FCF bridge ok'],'market_cap_m':MC,'html_sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in OUT.glob('*.html')}},ensure_ascii=False,indent=2))
print('Generated main + 6 company modules + 2 industry pages; partial scope disclosed.')
