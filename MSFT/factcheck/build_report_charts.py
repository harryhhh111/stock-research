"""刷新MSFT.html内的图形区块；正文仅维护HTML，不重建/同步Markdown。"""
from pathlib import Path
import json,html,ast,re
p=Path(__file__).resolve().parent;root=p.parent
d=json.loads((p/'data/inputs.json').read_text());a=d['annual'];r=json.loads((p/'results.json').read_text());val=json.loads((p/'valuation_2026-11-13_results.json').read_text());vi=json.loads((p/'data/valuation_2026-11-13.json').read_text())
# 只复用已认可图形的纯函数定义，绝不执行旧脚本的文件写入/Markdown同步。
old=ast.parse((p/'build_cash_view.py').read_text());wanted={'txt','svgbody','sankey','profit_chart','waterfall','grouped','billing_diagram'}
exec(compile(ast.Module(body=[n for n in old.body if isinstance(n,ast.FunctionDef) and n.name in wanted],type_ignores=[]),'existing_chart_functions','exec'))
profit_values={'集团收入':331.839,'营业成本':106.374,'毛利':225.465,'研发':35.562,'销售':26.710,'管理':7.956,'经营利润':155.237}
colors=['#138778','#bc7954','#496c9e','#a68c47']
def frame(body,label,height=350,width=1000):return f'<svg role="img" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg"><title>{label}</title>{body}</svg>'
def fig(title,meta,svg,note):return '<figure><figcaption><h4>'+title+'</h4><p class="chart-meta">'+meta+'</p></figcaption><div class="chart-scroll">'+svg+'</div><p class="chart-note">'+note+'</p></figure>'
def table(headers,rows):return '<div class="table-scroll"><table><thead><tr>'+''.join('<th>'+str(k)+'</th>' for k in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(k)+'</td>' for k in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def bars(labels,series,maximum=None):
 maxv=maximum or max(max(v) for _,v in series)*1.22;bottom=265;scale=205/maxv;b=''
 for j in range(5):
  tick=maxv*j/4;y=bottom-tick*scale;b+=f'<line x1="65" x2="975" y1="{y}" y2="{y}" stroke="#e1e8ed"/>'+txt(52,y+5,f'{tick:.0f}',12,anchor='end')
 group=880/len(labels);bw=min(54,(group-45)/len(series))
 for i,l in enumerate(labels):
  for j,(name,vs) in enumerate(series):
   x=90+i*group+j*(bw+6);v=vs[i];b+=f'<rect x="{x}" y="{bottom-v*scale}" width="{bw}" height="{v*scale}" fill="{colors[j]}" rx="3"/>'+txt(x+bw/2,bottom-v*scale-9,f'{v:.2f}',12)
  b+=txt(90+i*group+len(series)*(bw+6)/2,292,l,13)
 for j,(name,_) in enumerate(series):b+=f'<rect x="{110+j*230}" y="320" width="12" height="12" fill="{colors[j]}"/>'+txt(130+j*230,332,name,13,anchor='start')
 return frame(b,'；'.join(n+':'+','.join(map(str,v)) for n,v in series))
def bridge(labels,values,totals):
 # 相邻柱间距仅12；项目名紧贴浮动柱，避免与柱形分隔在图底两端。
 cur=0;points=[]
 for i,v in enumerate(values):
  nxt=v if i in totals else cur+v;points.append((cur,nxt));cur=nxt
 assert abs(sum(values[:-1])-values[-1])<1e-8
 bottom=260;scale=200/max(max(x) for x in points);step=114;bw=102;b=''
 b+=txt(30,22,'蓝色＝起终总额    绿色＝加回    棕色＝扣除',13,anchor='start')
 for i,((start,end),label,v) in enumerate(zip(points,labels,values)):
  if i in totals:start=0
  x=35+i*step;y=bottom-max(start,end)*scale;h=abs(end-start)*scale;c=colors[2] if i in totals else colors[0] if v>=0 else colors[1]
  b+=f'<rect x="{x}" y="{y}" width="{bw}" height="{h}" fill="{c}" rx="2"/>'+txt(x+bw/2,y-9,f'{v:.3f}' if i in totals else f'{v:+.3f}',14,c)
  label_y=y+h+19
  b+=txt(x+bw/2,label_y,label,13)
  if i==len(values)-1:b+=txt(x+bw/2,label_y+19,'经营现金流',12)
  if i<len(values)-1:b+=f'<line x1="{x+bw}" x2="{x+step}" y1="{bottom-end*scale}" y2="{bottom-end*scale}" stroke="#64748b" stroke-width="1.5"/>'
 b+=f'<line x1="25" x2="835" y1="{bottom}" y2="{bottom}" stroke="#b8c4cc"/>'
 return frame(b,' → '.join(f'{l} {v:.3f}' for l,v in zip(labels,values)),315,860)
def margins():
 b='';bottom=260;sc=2.9
 for tick in [0,20,40,60,80]:
  y=bottom-tick*sc;b+=f'<line x1="80" x2="930" y1="{y}" y2="{y}" stroke="#e1e8ed"/>'+txt(60,y+5,f'{tick}%',12)
 for j,(key,name) in enumerate([('gross_margin','毛利率'),('op_margin','经营利润率'),('net_margin','净利率')]):
  vals=[r['annual'][y][key] for y in a];pts=[(180+i*320,bottom-v*sc) for i,v in enumerate(vals)];b+=f'<polyline points="'+ ' '.join(f'{x},{y}' for x,y in pts)+f'" stroke="{colors[j]}" stroke-width="3" fill="none"/>'
  for (x,y),v in zip(pts,vals):b+=f'<circle cx="{x}" cy="{y}" r="4" fill="{colors[j]}"/>'+txt(x,y-12,f'{v:.2f}%',13,colors[j])
  b+=txt(180+j*290,330,name,14,colors[j])
 for i,y in enumerate(a):b+=txt(180+i*320,290,'FY'+y,14)
 return frame(b,'三年利润率；全部零起点单轴百分比')
def sensitivity():
 rows=[]
 for pe in [20,25,30]:
  cells=[]
  for target in [.08,.10,.12]:
   g=((vi['price']*(1+target)**5/pe/vi['openai_adjusted_eps'])**.2-1)*100
   cells.append(f'<span class="heat" style="--intensity:{max(.10,min(.7,g/35)):.3f}">{g:.2f}%</span>')
  rows.append([f'{pe}倍']+cells)
 return table(['终值PE / 要求年化回报','8%','10%','12%'],rows)
def growth_strip():
 # 单根带正负方向的堆叠条；所有金额同比例，负贡献不转绝对值饼图。
 scale=13;zero=180;y=110;b=''
 b+=f'<line x1="{zero}" y1="70" x2="{zero}" y2="185" stroke="#64748b"/>'
 x=zero
 for name,value,color in [('生产力',19.186,colors[0]),('智能云',31.526,colors[2])]:
  width=value*scale;b+=f'<rect x="{x}" y="{y}" width="{width}" height="50" fill="{color}"/>'+txt(x+width/2,y+30,f'{name} +{value:.3f}',14,'white');x+=width
 b+=f'<rect x="{zero-.597*scale}" y="{y}" width="{.597*scale}" height="50" fill="{colors[1]}"/>'+txt(zero-18,y-16,'个人计算 −0.597',14,colors[1],anchor='end')
 b+=txt(520,48,'净新增收入 +50.115 B美元',23,colors[0])+txt(zero,205,'0',13)+txt(520,240,'FY2025 → FY2026；只比较增量，不混入期初与期末存量',14)
 assert abs(19.186+31.526-.597-50.115)<1e-8
 return frame(b,'新增收入净增50.115；生产力19.186加智能云31.526减个人计算0.597',270)
def rpo_strip():
 b=f'<rect x="100" y="85" width="240" height="50" fill="{colors[0]}"/><rect x="340" y="85" width="560" height="50" fill="{colors[2]}"/>'
 b+=txt(220,115,'约30% / 203.1',17,'white')+txt(620,115,'约70% / 473.9',17,'white')+txt(220,165,'未来12个月',15)+txt(620,165,'以后确认',15)+txt(500,40,'商业RPO合计 677 B美元',22)
 return frame(b,'预计确认结构：未来12个月约30%，其后约70%，总额677',205)
def capital_flow():
 row=a['2026'];cfo=row['cfo'];capex=row['capex'];div=row['dividend'];buy=row['buyback'];fcf=cfo-capex;remainder=fcf-div-buy
 assert abs(fcf-66.987)<1e-8 and abs(remainder-18.271)<1e-8
 n={'cfo':('经营现金净流入',cfo,'#138778'),'capex':('现金固定资产投入',capex,'#bc7954'),'fcf':('自由现金流 FCF',fcf,'#496c9e'),'div':('现金分红',div,'#a68c47'),'buy':('现金回购',buy,'#8876a4'),'remaining':('扣除三项后差额',remainder,'#64748b')}
 edges=[('cfo','capex',capex),('cfo','fcf',fcf),('fcf','div',div),('fcf','buy',buy),('fcf','remaining',remainder)]
 return sankey(n,edges,[['cfo'],['capex','fcf'],['div','buy','remaining']],2.1,650)
charts={}
charts['business']=fig('三条收费链路，三种研究边界','机制示意 · 不按金额编码',billing_diagram(),'传统授权不等于SaaS。Azure托管数据库是另一种服务交付；未披露的传统软件独立收款不补造。')
charts['profit']=fig('卖了什么，又留下多少经营利润？','FY2026 · Microsoft集团 · B美元 · [S1]收入表及产品附注',profit_chart(),'产品服务加总331.839；成本106.374＋毛利225.465；毛利扣研发35.562、销售26.710、管理7.956后经营利润155.237。公共节点不代表产品级成本分摊。')
charts['capital']=fig('收入之后，看现金投向哪里','FY2026 · 微软集团 · B美元 · [S1]现金流量表与复算',capital_flow(),'182.935－现金固定资产投入115.948＝FCF 66.987；再扣现金分红26.445和现金回购22.271，差额18.271【复算✅】。这是经营现金流覆盖三项用途的算术示意，不代表资金逐笔追踪。差额还未计其他投资、偿债、发行融资和汇率影响，不能称期末现金或现金净增加；完整现金变动见第3节。现金CapEx含非AI用途、不含非现金新增融资租赁；回购采用现金流量表口径，含员工税务代扣相关交易。')
charts['growth']=fig('这一年新增收入，主要是谁带来的？','FY2025→FY2026 · 旧分部同口径 · B美元 · [S1]',growth_strip(),'一根有方向的堆叠条：右侧为正贡献，左侧为负贡献，共同金额比例；19.186＋31.526－0.597＝净增50.115【复算✅】。含负数，不用饼图；不把FY2027新分部与旧分部直接拼接。')
charts['quarter']=fig('最新季度：Azure与M365云的收入量级','FY2027 Q1 vs FY2026 Q1重述 · B美元 · [S2]',bars(['Azure','M365云','生产力及服务器许可'],[('上年同期',[22.384,23.694,8.678]),('本期',[33.165,27.778,8.407])]),'本期Azure33.165、M365云27.778。两项均包含非AI业务；新口径同期重述，不能直接与旧年度分类串接。完整产品表见下方。')
charts['margins']=fig('毛利率承压，经营利润率仍提高','FY2024—FY2026 · 集团 · % · [S1]及复算',margins(),'金额与比率分图。FY2026净利率受投资损益影响；高净利率不等于AI独立利润率。')
charts['cfo']=fig('净利润如何调节为经营现金流？','FY2026 · 集团 · B美元 · [S1]现金流量表',bridge(['净利润','折旧等','股权薪酬','投资收益扣除','递延所得税','营运资本等','CFO'],[133.749,38.534,12.405,-11.047,14.189,-4.895,182.935],{0,6}),'133.749＋38.534＋12.405－11.047＋14.189－4.895＝182.935。紧凑瀑布图保留正负调整方向，项目名贴近对应柱形；含负数且为加减调节关系，不适用饼图。SBC为非现金加回，仍有经济成本；营运资本等为原表相关变动汇总。')
charts['cash']=fig('经营产生的现金，最后流向哪里？','FY2026 · 集团 · B美元 · 现金及现金等价物，不含短期证券 [S1]',waterfall(),'30.242＋182.935－139.500－52.546－0.196＝20.935。这里使用投资/融资净流出；期初余额不是当年收入、期末余额不是费用、汇率减少不是付款，CFO已扣经营付款。')+table(['现金桥项目','金额（B美元）'],[['期初现金','30.242'],['CFO','182.935'],['投资净流出','-139.500'],['融资净流出','-52.546'],['汇率','-0.196'],['期末现金','20.935']])
charts['cashtrend']=fig('现金投入增长，FCF连续下降','FY2024—FY2026 · 集团 · B美元 · [S1]及复算',grouped(),'FCF＝CFO－现金固定资产支出。CapEx正值表示付款规模；FCF并非第三项可与前两者相加的用途。集团数据不冒充传统软件或AI独立现金流。')
charts['cashtrend']+=table(['集团现金指标（B美元）','FY2024','FY2025','FY2026'],[['CFO减现金CapEx',*[f'{a[y]["cfo"]-a[y]["capex"]:.3f}' for y in a]],['再扣融资租赁本金',*[f'{a[y]["cfo"]-a[y]["capex"]-lease:.3f}' for y,lease in zip(a,[1.286,2.283,3.101])]]])+ '<p class="chart-note">融资租赁本金分别1.286、2.283、3.101 B美元，[S1]租赁附注。补充现金观察为72.785、69.328、63.886，仍未扣并购/股权投资，不能称AI独立回报。</p>'
charts['sensitivity']=fig('支持这个价格，需要多少EPS增长？','【我的推演】11月11日521.13美元 · 5年 · 起点EPS18.04美元',sensitivity(),'表中为所需EPS年复合增速；公式＝[价格×(1＋要求回报率)^5÷终值PE÷起点EPS]^(1/5)－1，不计股息。起点仅剔除OpenAI影响，尚非完全正常化利润；不是一致预期。')
charts['rpo']=fig('已经签下的收入，预计什么时候兑现？','2026-09-30期末 · 商业RPO · B美元 · 公司预计确认比例 [S3]',rpo_strip(),'单根100%堆叠柱展示预计确认结构；677×30%＝203.1，其余473.9【复算✅】。不属于当期现金收款，不全部是Azure/AI收入，不保证按期交付。')
# 金额/序列断言与可重复刷新，仅修改标记中的图形，不覆盖人工维护的HTML正文。
for i,year in enumerate(a):
 assert abs(sum(v[i] for v in d['products'].values())-a[year]['revenue'])<1e-6
assert abs(133.749+38.534+12.405-11.047+14.189-4.895-182.935)<1e-6
report=root/'MSFT.html'
if report.exists():
 s=report.read_text()
 for key,value in charts.items():
  pattern=f'<!-- FIGURE:{key}:START -->.*?<!-- FIGURE:{key}:END -->'
  s,n=re.subn(pattern,f'<!-- FIGURE:{key}:START -->{value}<!-- FIGURE:{key}:END -->',s,flags=re.S)
  assert n==1,(key,n)
 report.write_text(s)
 print(f'{len(charts)}个图形区块已刷新；正文未改写；收入/现金/利润桥勾稽通过')
