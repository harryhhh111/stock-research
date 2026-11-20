"""Upgrade the stable company entries to the full SOP coverage, not a separate report."""
from pathlib import Path
import json,math,re
from bs4 import BeautifulSoup
from full_research_data import build,ROOT,C,N
DATA=build()
SRC={
 'c-annual':('CoreWeave FY2025 10-K，2026-03-02，三年报表','https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm'),
 'c-ipo':('CoreWeave IPO招股书，2025-03，F-4至F-6','https://d18rn0p25nwr6d.cloudfront.net/CIK-0001769628/d9ab0488-f3b1-4252-9520-c523a279fb84.pdf'),
 'n-annual':('Nebius FY2025 20-F，2026-04-30，三年持续经营报表及附注15','https://www.sec.gov/Archives/edgar/data/1513845/000110465926052948/nbis-20251231x20f.htm'),
 'n-2024':('Nebius FY2024 20-F，2025-04-30，2022基期与分拆前权益','https://www.sec.gov/Archives/edgar/data/1513845/000155837025005991/nbis-20241231x20f.htm'),
 'n-q3-notes':('Nebius Q3 2026法定财务报表，2026-11-12，6-K附件99.2','https://www.sec.gov/Archives/edgar/data/1513845/000110465926126238/nbis-ex99d2.htm'),
 'n-q3-mda':('Nebius Q3 2026经营讨论，2026-11-12，6-K附件99.1','https://www.sec.gov/Archives/edgar/data/1513845/000110465926126238/nbis-ex99d1.htm'),
 'n-msft':('Nebius–Microsoft五年合同，2025-09-08，原始6-K','https://assets.nebius.com/assets/86625727-9e66-46c1-af79-c27d57434e3c/25-25580-1_Nebius%20Group%20N.V._6-K.pdf?cache-buster=2025-09-08T21%3A23%3A09.625Z'),
 'n-meta':('Nebius–Meta新协议，2026-03-16','https://nebius.com/newsroom/nebius-signs-new-ai-infrastructure-agreement-with-meta'),
 'c-openai':('CoreWeave–OpenAI扩展合同，2025-09-25','https://investors.coreweave.com/news/news-details/2025/CoreWeave-Expands-Agreement-with-OpenAI-by-up-to-6-5B/default.aspx'),
 'c-corz-end':('Core Scientific并购终止，2025-10-30，目标公司公告','https://investors.corescientific.com/news-events/press-releases/detail/124/core-scientific-announces-termination-of-merger-agreement-with-coreweave'),
 'c-corz-q3':('Core Scientific Q3 10-Q，2026-11-05，实际计费容量','https://investors.corescientific.com/sec-filings/all-sec-filings/content/0001839341-26-000030/core-20260930.htm'),
 'c-apld':('Applied Digital，2026-06-09，租约转让MOU及评级条件','https://ir.applieddigital.com/news-events/press-releases/detail/153/applied-digital-secures-revolving-credit-facility-of-up-to'),
 'n-citi':('Nebius–Citi 3.5B融资额度，2026-10-22','https://nebius.com/newsroom/nebius-secures-3-5-billion-financing-facility-with-citi'),
}

def upgrade(document,sym,table,p,section,bars):
 d=DATA['quarterly'][sym];annual=DATA['annual'][sym];is_c=sym=='CRWV';name='CoreWeave' if is_c else 'Nebius';project=C if is_c else N
 soup=BeautifulSoup(document,'html.parser');fmt=lambda v:f'{(0 if abs(v)<1e-10 else v):,.2f}'
 def link(k,label=None):return f'<a href="#full-{k}">{label or SRC[k][0]}</a>'
 def frag(s):return BeautifulSoup(s,'html.parser')
 def append(id,s):soup.find(id=id).append(frag(s))
 def replace(id,s):
  target=soup.find(id=id);h=target.h2;target.clear();target.append(h);target.append(frag(s))
 def money_table(headers,rows,caption):return table(headers,rows,'单位：M美元；比率为%。'+caption)
 # The scope is the migration requested by the user, not the narrower previous attempt.
 soup.title.string=name+'：三年基本面、Q3兑现与资本回报'
 for x in soup.select('.tags span'):
  if '行情窗口' in x.text:x.string='估值行情：2026-11-16收盘'
  if '局部覆盖' in x.text:x.string='三年历史＋年内完整季度'
 soup.select_one('header .scope').replace_with(frag(p('本轮覆盖2023–2025三个完整财年、2026 Q1–Q3及最新TTM；财务与订单截至2026-09-30，估值采用11/16收盘价，事件复盘保留11/10–13窗口。历史Markdown停更保留；本文承接有效研究、纠正旧口径，不是单季专题。','scope')))
 thesis=('三年收入迅速放大，但现金扩张更多依赖预付与债务；Q3交付、利润率和收入指引改善，未改变高杠杆的约束。' if is_c else '三年持续经营收入已从9.8 M增至529.8 M，Q3增长又含初始合作收入；需求与定价强并不消除交付延后、现金投入和稀释风险。')
 soup.select_one('header .lead').string=thesis
 # Annual revenue layer. Every cell has amount, YoY and group denominator.
 def revenue_cells(amounts,group,prior=None,annual_mode=False):
  out=[]
  for i,v in enumerate(amounts):
   base=prior[i] if prior is not None else (amounts[i-1] if i else None)
   if base is None:yoy='不可比：2022含Toloka' if not is_c else f'约+{annual["2023"]["revenue_yoy_pct"]:,.2f}%'
   elif base==0:yoy='基数为0，增量 '+fmt(v-base)
   elif base<0:yoy='抵销变动 '+fmt(v-base)
   else:yoy=f'{(v/base-1)*100:+,.2f}%'
   share=v/group[i]*100
   out.append(f'{fmt(v)}<small>同比：{yoy}<br>占集团：{share:,.2f}%</small>')
  return out
 yr=['2023','2024','2025'];ar=[annual[y]['revenue'] for y in yr]
 annual_rows=[['集团持续经营收入' if not is_c else '集团收入']+revenue_cells(ar,ar)]
 sg=DATA['segments']
 if not is_c:
  for label,k in [('Nebius AI cloud','cloud'),('TripleTen','tripleten'),('Avride','avride'),('内部交易抵销','eliminations')]:
   vs=[annual[y][k] for y in yr];cells=revenue_cells(vs,ar)
   # FY2022 segment bases exist, but no current group-comparable restatement is supplied.
   base={'cloud':.5,'tripleten':2.2,'avride':.3,'eliminations':0}[k]
   yoy=f'{(vs[0]/base-1)*100:+,.2f}%' if base>0 else '抵销口径未重列'
   cells[0]=f'{fmt(vs[0])}<small>同比：{yoy}<br>占集团：{vs[0]/ar[0]*100:,.2f}%</small>'
   annual_rows.append([label]+cells)
 annual_rev='<h3 id="annual-revenue">三个完整财年：收入规模和业务结构</h3>'+money_table(['集团 / 业务','FY2023','FY2024','FY2025'],annual_rows,'同一自然年财年；集团同比取可比基数；分部包含内部交易，抵销以负值列示。')
 annual_rev+=bars('年度收入：从早期部署到规模化',[('集团收入',ar)],['FY2023','FY2024','FY2025'],'M美元',name+' FY2025法定年报')
 if is_c:
  annual_rev+=p('【复算】✅ 三年收入从229 M增至5,131 M，2023–2025两年复合增速约373.35%；2025同比约167.94%。报表只有一个经营分部，不再沿用旧笔记“GPU收入90%+、软件不足10%”的估计作为事实拆分。2023同比基期来自IPO披露2022收入15.830 M；最新10-K按整数M列示2023/2024金额，算得约1,346.62%与公司按更细数据披露约1,346%的差异属舍入，不构成独立精确增速。'+link('c-annual')+'；'+link('c-ipo')+'。')
  annual_rev+=p('增长证据主要是更多GPU集群上线与客户增加承诺容量；2025全年收入增长不是纯涨价。公司单一分部、软件与基础设施混合履约，未给足以独立复算硬件数量×实际利用率×价格的完整桥，所以未分解的组合/利用率效应不猜数。')
 else:
  annual_rev+=p('【口径修正】2023、2024、2025采用FY2025 20-F剔除俄罗斯业务和Toloka后的持续经营口径；不能把旧2024年收入117.5 M与新529.8 M直接相比，正确基数是91.5 M。2023集团9.8 M也不是旧Yandex集团约93亿美元收入。2022年旧表13.5 M包含Toloka，最新三年年报未列同口径2022重列，故不计算集团2023同比。可识别分部的2022基数来自FY2024附注，例外就近显示。'+link('n-annual')+'；'+link('n-2024')+'。')
  annual_rev+=p('【复算】✅ 2025收入增量438.3 M＝AI cloud +412.0、TripleTen +25.3、Avride +1.0、抵销变化0；AI cloud解释约94.00%的净增量。2024 AI cloud从9.6增至68.3 M，公司归因于新客户、客户项目扩大及GPU/机房扩容；2025新增五处地点支持客户与容量增长。价格与利用率贡献没有完整可加总拆分，不能把所有增长写成涨价。')
  annual_rev+=p('2023年AI cloud 9.6 M占集团97.96%，TripleTen 8.2 M占83.67%，两者之和超过100%，原因是内部抵销−8.0 M，并非数据重复或可以把占比重新归一成100%。2024、2025抵销均−5.9 M；分部利润也按披露口径，不按集团收入比例摊派。','note')
 # Complete year-to-date quarter revenue by all disclosed segments, not only the large one.
 qr=[d[q]['revenue'] for q in ['q1','q2','q3']];prior=([982,1212,1365] if is_c else [50.9,105.1,146.1])
 qrows=[['集团']+revenue_cells(qr,qr,prior)]
 if not is_c:
  for label,k in [('Nebius AI cloud','cloud'),('TripleTen','tripleten'),('Avride','avride'),('内部抵销','eliminations')]:qrows.append([label]+revenue_cells(sg['quarterly'][k],qr,sg['quarterly_prior'][k]))
 qrev='<h3 id="quarter-revenue">2026年内完整单季：同比分母与抵销一致</h3>'+money_table(['集团 / 业务','2026 Q1','2026 Q2','2026 Q3'],qrows,'单季，非累计；来源：Q1/Q2原始6-K或业绩稿、Q3法定财务表。')
 qrev+=bars('季度收入：同比与交付爬坡一起看',[('集团收入',qr)],['2026 Q1','2026 Q2','2026 Q3'],'M美元',name+' Q1–Q3财务披露')
 qrev+=p('集团环比：Q1 '+f'{(qr[0]/(1572 if is_c else 227.7)-1)*100:+.2f}%'+'（以2025 Q4收入'+fmt(1572 if is_c else 227.7)+' M为基期）；Q2 '+f'{(qr[1]/qr[0]-1)*100:+.2f}%'+'；Q3 '+f'{(qr[2]/qr[1]-1)*100:+.2f}%'+('。上线节奏和大合同爬坡造成季度台阶，不能据此识别固定季节性。' if is_c else '。Q3另有约325 M非经常性初始合作收入，不能把68.44%的总环比直接外推。'))
 if not is_c:
  qrev+=p('Q3股东信采用“约325 M非经常性轻资产初始部署收入”；法定附注15精确列示战略合作收入Q3为325.1 M、9M为409.1 M。这两个标签范围并非自动相同：H1战略合作收入合计84.0 M，不能推定全部是相同初始部署费。按325.1机械扣除的Q3余额为655.7 M；按股东信约325为655.8 M，舍入差0.1 M。没有同口径成本和逐季合作收入拆分，不把余额标为纯经常性收入，也不直接从EBITDA减收入。'+link('n-q3-notes')+'附注15。','scope')
 # Reorder the revenue chapter: actual/guidance, income and cash chains, annual then quarter history.
 rev=soup.find(id='revenue');guidance=str(rev.select_one('.table-wrap'));oldfigs=rev.find_all('figure');income_fig=str(oldfigs[1]);cash_fig=str(oldfigs[2]);alltables=rev.select('.table-wrap');income_table=str(alltables[2])
 chain_note=p('收入图为集团GAAP收入分配；现金图独立展示CFO、现金购建设备支出及FCF。分红/回购和其他投资、偿债的逐项边界见<a href="#capital-allocation">资本分配</a>及<a href="#cash-flow">完整现金桥</a>。不把负FCF称为“留存现金”，也不把资产增加或未付承诺塞入现金图。')
 replace('revenue',p('最新实绩与公司指引先看，随后分别展开三个完整年度和2026年完整单季。B＝10亿美元，M＝100万美元；现金CapEx与公司总投入指引不是可无条件相减的同一口径。')+guidance+income_fig+income_table+cash_fig+chain_note+annual_rev+qrev)
 # Annual income, cash, returns and capital allocation.
 rows=[]
 for label,k in [('收入','revenue'),('收入成本（NBIS不含单列折旧）','cost'),('经营利润','op'),('经营利润率','op_margin'),('持续经营净利润 / 合并净利润','net'),('同口径净利率','net_margin'),('利息费用（CRWV净额）','interest_expense'),('股权激励费用','sbc'),('折旧与摊销','da'),('经营现金流（持续经营）','cfo'),('现金CapEx','cash_capex'),('自算FCF','fcf')]:
  rows.append([label]+[f'{annual[y][k]:,.2f}%' if 'margin' in k else fmt(annual[y][k]) for y in yr])
 rows.insert(2,['收入减列示收入成本']+[fmt(annual[y]['revenue']-annual[y]['cost']) for y in yr])
 rows.insert(3,['列示成本后毛利率，未扣全部折旧']+[f'{annual[y]["gross_margin_ex_separate_da"]:.2f}%' for y in yr])
 if is_c:
  rows.insert(6,['归属普通股净利润（基本）']+[fmt(annual[y]['common_net']) for y in yr])
  rows.append(['基本EPS · 美元/股']+[fmt(annual[y]['eps']) for y in yr])
 else:rows.append(['持续经营基本EPS · 美元/股']+[fmt(x) for x in [-.81,-1.25,.04]])
 if not is_c:rows.insert(6,['归母总净利润（含终止经营）']+[fmt(annual[y]['parent_net']) for y in yr])
 annfin='<h3 id="annual-finance">三年盈利与现金流：收入扩大是否留下现金？</h3>'+money_table(['指标','FY2023','FY2024','FY2025'],rows,'EPS例外单位为美元/股。CRWV合并净利润；NBIS以持续经营净利润配持续经营收入，另列含终止经营归母利润。来源：'+link('c-annual' if is_c else 'n-annual')+'。')
 annfin+=bars('年度现金流与投入：现金缺口如何扩大',[('CFO',[annual[y]['cfo'] for y in yr]),('现金CapEx',[annual[y]['cash_capex'] for y in yr]),('FCF',[annual[y]['fcf'] for y in yr])],['FY2023','FY2024','FY2025'],'M美元',name+'三年现金流表，FCF＝CFO−现金CapEx')
 if is_c:
  annfin+=p('2023–2025 CFO分别为1,833、2,749、3,058 M，却远低于现金CapEx；2025现金FCF−7,251 M，2026 9M又扩大至−17,920 M。CFO不能直接当“产品自己赚来的钱”：2025递延收入变动贡献4,174 M，同时应收占用2,749 M。2023/2024净亏损另含公允价值调整损失约534/756 M；2025该项变为收益27 M，但净利息已升至1,229 M。'+link('c-annual')+'。')
 else:
  annfin+=p('2023集团收入基数很小，收入成本19.6 M已超过9.8 M收入；此时仍在建设AI云与支持其他早期业务，不能把早期负毛利率或巨额费用率解释成成熟业务稳态。2025持续经营净利9.8 M主要受598.9 M投资重估收益支撑，经营亏损仍−611.7 M；另有72.7 M终止经营净利，使归母总净利82.5 M。2025持续经营CFO401.9 M包含递延收入变动1,565.8 M，扣现金CapEx后FCF−3,664.1 M，净利润转正尚不代表云业务现金盈利。'+link('n-annual')+'。')
  annfin+=p('【历史数更新】FY2025业绩稿曾列持续经营净利29.0 M，而4/30法定20-F列9.8 M；本报告采用后者，不静默混用。由年报减Q3 2025的9M比较数，2025 Q4净利＝9.8−278.6＝−268.8 M，经营利润＝−611.7−（−361.7）＝−250.0 M；因此最新TTM持续经营净利为124.5 M，替换此前基于旧Q4的143.7 M。两份披露差异未被擅自归因于某一项会计原因。','scope')
 # Insert annual finance at chapter start and refresh the TTM figures with the latest annual basis.
 finance=soup.find(id='finance');finance.h2.insert_after(frag(annfin))
 finance.h2.insert_after(frag(p('利润分类说明：收入减财报单列收入成本为本报告复算值，未扣全部GPU折旧；CRWV相关折旧主要在技术与基础设施费用，NBIS折旧摊销单列。这里列示成本后毛利率不等于所有设备成本计入后的可持续产品毛利。收入至全部经营费用/利润已由上章桑基与本章利润桥覆盖。','note')))
 quarter_table=next(t for t in finance.find_all('table') if '单季 · M USD' in t.get_text())
 qc=[716,879,1183] if is_c else [103.8,133.6,219.7]
 quarter_table.tbody.append(frag('<tr><th>利息费用（CRWV净额）</th>'+''.join(f'<td>{-d[q]["interest"]:.2f}</td>' for q in ['q1','q2','q3'])+'</tr>'))
 quarter_table.tbody.append(frag('<tr><th>列示成本后毛利率，未扣全部折旧</th>'+''.join(f'<td>{(d[q]["revenue"]-qc[i])/d[q]["revenue"]*100:.2f}%</td>' for i,q in enumerate(['q1','q2','q3']))+'</tr>'))
 if not is_c:
  # Replace the existing TTM table identified by its header, not text-wide substitution.
  for wrap in finance.select('.table-wrap'):
   if 'TTM（2025 Q4' in wrap.get_text():
    wrap.replace_with(frag(money_table(['指标','2026 9M','TTM：2025 Q4＋2026 9M'],[[label,fmt(sum(d[q][k] for q in ['q1','q2','q3'])),fmt(d['ttm'][k])] for label,k in [('收入','revenue'),('经营利润','op'),('持续经营净利润','net'),('CFO','cfo'),('现金CapEx','cash_capex'),('自算FCF','fcf')]],'TTM截至2026-09-30；2025 Q4按已审计全年减可比9M重算，非旧业绩稿初步净利润。')))
 if is_c:
  for caption in finance.find_all('caption'):
   if 'TTM截至2026-09-30；Nebius' in caption.text:caption.string='单位：M美元。TTM截至2026-09-30，CRWV合并口径；净亏损不适用PE，普通股股东归属差异见年度表。'
 # Quarterly SBC and per-segment profitability are directly readable.
 add='<h3 id="segment-profit">业务利润与全年季度覆盖</h3>'
 if not is_c:
  rows=[]
  for label,k in [('AI cloud','cloud'),('Avride','avride'),('TripleTen','tripleten')]:
   rows.append([label+' · 调整后EBITDA']+[fmt(v) for v in sg['quarterly_ebitda'][k]])
   rows.append([label+' · 分部EBITDA率']+[f'{sg["quarterly_ebitda"][k][i]/sg["quarterly"][k][i]*100:,.2f}%' for i in range(3)])
  add+=money_table(['分部指标','2026 Q1','2026 Q2','2026 Q3'],rows,'分母为本分部收入；Avride收入很小，负利润率受小分母放大，金额为主；三分部EBITDA和＝集团。Q1/Q2法定披露＋Q3附注15。')
  add+=money_table(['年度分部调整后EBITDA','FY2023','FY2024','FY2025'],[[label]+[fmt(annual[y][k]) for y in yr] for label,k in [('AI cloud','cloud_ebitda'),('Avride','avride_ebitda'),('TripleTen','tripleten_ebitda'),('集团','ebitda')]],'非GAAP分部指标，不替代集团经营利润；分部现金流未披露，不按收入比例摊集团投入。')
 add+=money_table(['集团费用与现金质量','2026 Q1','2026 Q2','2026 Q3'],[['股权激励']+[fmt(d[q]['sbc']) for q in ['q1','q2','q3']],['现金CapEx / 收入']+[f'{d[q]["cash_capex"]/d[q]["revenue"]*100:,.2f}%' for q in ['q1','q2','q3']]],'股权激励是非现金经济成本，不以费用金额代替发股数量；现金CapEx强度描述建设周期，非稳态单位成本。')
 add+=table(['单季基本EPS · 美元/股','2026 Q1','2026 Q2','2026 Q3'],[['直接披露值']+[fmt(x) for x in ([-1.40,-1.14,-1.27] if is_c else [2.40,-.68,-.13])]],'直接取单季报表，非累计相减；加权平均股数与期末经济股本不同。')
 # Latest quarter YoY and sequential changes, signed deltas for losses.
 prev={'revenue':1365,'op':52,'net':-110,'cfo':1689,'cash_capex':3279,'fcf':1689-3279} if is_c else {'revenue':146.1,'op':-130.2,'net':-119.6,'cfo':-80.6,'cash_capex':955.5,'fcf':-80.6-955.5}
 add+='<h3 id="latest-comparison">最新季度同比与环比：亏损比较金额</h3>'+money_table(['集团指标','2025 Q3','2026 Q3','同比金额变化','较2026 Q2金额变化'],[[label,fmt(prev[k]),fmt(d['q3'][k]),f'{d["q3"][k]-prev[k]:+,.2f}',f'{d["q3"][k]-d["q2"][k]:+,.2f}'] for label,k in [('收入','revenue'),('经营利润','op'),('净利润','net'),('CFO','cfo'),('现金CapEx','cash_capex'),('自算FCF','fcf')]],'Q3公司原始财务表；跨零和负基数不计算失真的利润“增幅”。')
 if not is_c:
  add+=p('Q2产品开发费用191.0 M的同比增量148.2 M中，公司说明74.9 M为Eigen AI相关股权激励、41.0 M为并购后薪酬费用；这解释Q2集团SBC跳至102.5 M的重要原因。两者是费用确认，不等于整笔并购对价或当季全部已付现金。Q3相应费用回落不能全部解释为GPU业务的稳态经营杠杆。来源：Q2 2026 6-K经营讨论及附注3。')
  add+=p('2026年1月起，服务器与网络设备预计折旧年限由4年改为5年，前瞻适用，不重写旧年度。期初资产估算2026年折旧减少约167.6 M，实际全年受新增设备影响；因此经营利润改善同时包含增长与会计估计变化，不能把全部改善当作单位成本下降。Q3财务附注确认该估计已实施。'+link('n-annual')+'；'+link('n-q3-notes')+'附注2。')
  add+=p('【利息拆解】Q3利润表利息112.5 M＝债务费用53.8 M＋客户预付款显著融资成分及供应商延期付款利息58.7 M；债务费用本身已扣资本化利息91.9 M。9M相应295.3＝160.3＋135.0 M。预付款提供融资便利，却可能有经济融资成本；低票息不等于全部资本成本低。不能把53.8与112.5当冲突，也不能把资本化利息当作本期利润表费用再加一次。'+link('n-q3-notes')+'附注4/12。','scope')
 finance.append(frag(add))
 # Balance-sheet historical snapshots (not mixed with flows).
 bs=DATA['annual_balance'][sym];br=[]
 for label,key in [('现金及等价物','cash'),('债务，不含租赁','debt'),('净债务','net_debt'),('股东权益','equity')]:
  cells=[label]
  for y in yr:
   v=bs.get(y,{}).get(key)
   if v is None:cells.append('不可比：分拆前范围，见说明')
   else:cells.append(fmt(v))
  br.append(cells)
 bal='<h3 id="balance-history">历史期末快照与资本回报</h3>'+money_table(['期末指标','2023-12-31','2024-12-31','2025-12-31'],br,'最新2026-09-30余额仍见本章快照。来源：'+link('c-annual' if is_c else 'n-annual')+'；2023补充'+link('c-ipo' if is_c else 'n-2024')+'。')
 if not is_c:bal+=p('2023年末法律主体仍持有俄罗斯终止经营资产；持续经营现金与受限现金合计114.1 M，不与后两年纯现金口径直接作增长比较。2023归母权益3,293.7 M来自分拆前母体，2022期末4,488.8 M仅作ROE期初输入。2024退出俄罗斯和库存股交易使股数、权益骤变，历史资产规模不能直接解释当前云业务资金回报。')
 rr=DATA['roe_pct'][sym];bal+=table(['年度','ROE：归属股东利润 / 平均归属权益','解释'],[[y,'不具经济解释性：平均权益为负' if rr[y] is None else f'{rr[y]:,.2f}%',('IPO前普通股权益为负，不把数学上正比率称为盈利' if is_c and y!='2025' else 'IPO增资使期初期末均值敏感，分母=(−414+3,335)/2 M' if is_c else '含终止经营/投资收益的归母总利润口径；不代表AI云ROE')] for y in yr],'CRWV FY2025用普通股股东基本口径亏损1,196 M；NBIS用归母总净利241.3/−641.4/82.5 M和期初/末归母权益。')
 bal+=p('ROIC不用于两家公司直接排名：可赎回优先股、租赁、客户预付、非经营投资和大额在建资产使简单“债务＋普通股权益−现金”分母不稳定。替代观察为现金CapEx/收入、FCF与净融资、交付进度和合同回款；不把未计算或负投入资本造成的高ROIC称为优势。')
 finance.append(frag(bal))
 if is_c:
  finance.append(frag('<h3 id="funding">追索范围：项目融资不等于全部风险隔离</h3>'+money_table(['9/30债务账面分类','M美元'],[['有追索权债务',fmt(9183+32417)],['无追索权债务',fmt(1389+3884)],['合计',fmt(46873)]],'Q3资产负债表；不含租赁。')+p('有追索权包含母体直接义务或无条件担保；无追索权以项目资产/现金为偿债来源，但通常仍有欺诈、抵押资产挪用等有限追索例外。不能把全部46.9 B债务都称为母公司免责的GPU资产贷款；项目受限现金也不能无条件转作其他项目资金。Q3 10-Q附注10。')))
 # Financing maturity / commitments. NBIS available statutory detail is now reviewed.
 if not is_c:
  debtrows=[['2029-06',105.0,91.2,'2.00%'],['2030-02',3795.0,3417.4,'0.50%'],['2030-09',1818.4,1600.9,'1.00%'],['2031-03',3105.0,2613.5,'1.25%'],['2031-06',109.4,89.8,'3.00%'],['2032-09',1818.4,1583.7,'2.75%'],['2033-03',2100.0,1756.1,'2.625%'],['2034-02',2875.0,2277.1,'4.50%']]
  debt='<h3 id="funding">可转债与资产贷款：票息、账面、到期额不同</h3>'+money_table(['可转债到期日','附注本金/增值额','账面金额','票息（例外单位）'],[[a,fmt(b),fmt(c),r] for a,b,c,r in debtrows],'2026-09-30；附注本金含约定增值，不等于最初募资额；按法定附注12转录。')
  debt+=p('另有资产支持贷款附注本金751.8 M、账面733.1 M，按月摊还、最终到期日为2030-10；不能把全额751.8 M画成2030单年偿债墙。附注债务合计账面14,162.8 M，而主表187.5＋14,003.3＝14,190.8 M，两者差28.0 M未在本轮取得明确调节，估值保守采用较大的主表数；对每股价值的机械影响约0.09美元，不影响总体融资判断。'+link('n-q3-notes')+'附注12。')
  debt+=p('8月原始发行额5.75 B由3.45 B低票息2030债和2.30 B的2034债构成；后者按合约增值至更高到期本金，因此4.50%票息与7.16%有效利率不同。债转股时现金、股票或混合结算有公司选择，但选择现金仍需要融资，选择股票仍会稀释，不能把转股当免费偿债。')
  lease=[['2026余下',42.5],['2027',255.5],['2028',270.4],['2029',278.6],['2030',278.8],['以后',1404.7]]
  debt+='<h3>已起租与尚未起租承诺</h3>'+money_table(['经营租赁现金付款期间','未折现金额'],[[a,fmt(b)] for a,b in lease]+[['合计',fmt(2530.5)],['减隐含利息',fmt(-649)],['账面负债',fmt(1881.5)]],'附注8；不含未起租合约。')
  debt+=p('尚未起租合约未来未折现租金13,862.3 M，已预付619.7 M，剩余13,242.6 M，其中未来12个月572.7 M。余下金额与已预付不得重复计入“未来支出”。合同预计2026–2029起租，不等于这些产能都已可用；与集团现金CapEx、债务本金分开，避免简单相加冒充全部债务。')
  finance.append(frag(debt))
 if not is_c:
  finance.append(frag(p('资产贷款的借款主体、抵押现金/应收及股权有明确隔离与契约，最低偿债覆盖率1.15倍；母体仍有有限不当行为保证及部分履约保证。2026-09-30借款主体遵守契约，不能据此推断未来始终满足。可转债为高级无担保母体融资，不能与项目贷款混称同样的利率/追索风险。'+link('n-q3-notes')+'附注12。')))
 # Three-year distribution, shares and acquisitions.
 capital='<h3 id="capital-allocation">资本分配：设备投入、并购与股数</h3>'
 caprows=[]
 for label,key in [('现金CapEx','cash_capex'),('股权激励费用','sbc')]:caprows.append([label]+[fmt(annual[y][key]) for y in yr])
 caprows.append(['普通股现金股息']+['未见普通股股息支付']*3)
 if is_c:caprows.append(['优先股现金股息']+[fmt(-annual[y]['preferred_dividends_signed']) for y in yr])
 capital+=money_table(['分配项目','FY2023','FY2024','FY2025'],caprows,'普通股股息与已在IPO转换的可赎回优先股股息分开；本轮检查年报/现金流表，不把“无普通股股息”写成所有股类从未付息。')
 if is_c:
  capital+=p('FY2023/FY2024普通股期末约203.520/232.887 M（不含可赎回优先股），FY2025期末约502 M；2026-10-30普通股556.125724 M，较2025末约增10.78%。IPO优先股转换、并购对价、员工奖励及融资共同改变股本，不用SBC费用推算新增股数。历史库存股为回购及其他股权交易的存量，不能把库存股余额差直接当现金回购。')
  capital+=p('W&B于2025-05-05完成收购，对价约1.0 B（含现金、股票及股权奖励等），用于模型开发和应用工具；它已并表，不再把其估值另加到集团股权价值。2025现金流“业务合并净付款”合计108 M，不等于整笔收购经济对价。Core Scientific全股并购于2025-10-30终止，不能继续在自有数据中心或未来股本中计入该交易。'+link('c-annual')+'；'+link('c-corz-end')+'。')
  capital+=p('9月可转债初拟3.0 B及增购权已被完成4.2 B发行取代；该笔债券票息2.875%、初始转股价约97.85美元，已包含在9/30债务。Q3 capped call现金付款566 M并非偿债。35M股ATM截至9/30未售出；它仍是融资选择，不等于已经售股或可以保证以某一股价融资。')
 else:
  capital+=p('普通股流通总数：2023末361.482281 M、2024末235.753600 M、2025末253.016971 M、2026-09-30为292.902405 M。2024退出俄罗斯业务的对价含162.5 M公司A股，股数下降不能简单归为公开市场现金回购；2025/2026再售库存股会重新增加流通。2026另有NVIDIA预付认股权21.065936 M，行权价仅0.0001美元，本报告经济股本合计313.968341 M。'+link('n-annual')+'；'+link('n-q3-notes')+'附注14。')
  capital+=p('Q3 ATM售出4.6338 M股，均价229.14美元、净额1,048.5 M；9M售出17.363293 M股、净额3,859.6 M，25M授权剩余7.636707 M。不能把已融资额再加作未来额度。股价下降后同等募资额对应更多股数，才是稀释与交付之间的反馈机制，不是所有股价下跌都会立刻触发售股。')
  capital+=p('2026收购Tavily、ClarifAI、Eigen AI用于搜索/AI应用、部署与模型优化；9M现金净收购付款251.6 M，部分对价为股份，商誉605.7 M不等于现金付款。ClickHouse/Toloka为投资，不并入其营业收入；2025/2026投资重估净收益也不属于GPU租赁利润。10月Citi 3.5 B短期融资额度用于建设与GPU采购，为期后事项，并非9/30已到账现金。'+link('n-q3-notes')+'附注3/9/14；'+link('n-citi')+'。')
 finance.append(frag(capital))
 # Replace stale generic limitations now resolved by actual primary filings.
 for node in finance.find_all('p'):
  if 'CRWV债务本金时间表已补；NBIS本轮尚未完成' in node.get_text():node.string='资本分配与到期结构已结合附注复核；承诺与实付、借款与租赁、普通股与优先股保持分开。上文现金桥保留净额融资/投资，不把同一子项目再次计入合计。'
 # Real customers and concentration; anonymous labels are not guessed.
 cases=([
 ['OpenAI','模型训练/推理算力','2025扩展公告累计合同上限22.4 B；按期交付后确认收入','客户，兼有股权关系；不把合同额再加到backlog'],
 ['Wayve','AI驾驶模型训练','2026-11-09多年度协议，金额未披露','实际客户；与其GPU供应商区分'],
 ['Cohere / Jane Street','企业AI / 量化计算相关云能力','Q3业绩稿列关系扩展，具体金额未披露','客户；用途只按公告可支持范围'],
 ['NVIDIA','GPU供应与金融/容量合作','同时有供应商、股东及容量安排关系','多重角色；不是独立终端需求的纯证明']
 ] if is_c else [
 ['Microsoft','Vineland专属GPU容量','2025五年合同17.4 B，额外选择可增加；Q3更新交付时间','已签客户，不能把园区全部MW当微软独占'],
 ['Meta','新一代GPU容量与可用容量安排','2026协议上限27 B，其中12 B专属＋最多15 B其他可用容量','两部分结构不同，不全部作为同一无条件年收入'],
 ['Cognition','Devin研发的大规模Vera Rubin集群','Q3股东信列合作，具体收入未披露','真实客户；不从logo推断金额'],
 ['Prosus / Hark','Token Factory推理 / AI代理','Q3股东信列已选服务和用途','客户；Token Factory不是单列报告分部'],
 ['monday.com / IBM Research','Tavily实时搜索 / Granite后训练','Q3股东信列案例，IBM Q3扩范围','收购子公司业务客户，不与集团重复加总'],
 ['TD SYNNEX / Palantir / CDW','共同销售和渠道拓展','Q3股东信列生态伙伴','渠道伙伴，不能当作GPU付费大客户']])
 append('customers','<h3 id="customer-cases">谁付钱、为何买：公开实名案例</h3>'+table(['对象','所购 / 所用能力','合作阶段与证据','身份边界'],cases,'来源：Q3业绩稿/股东信，'+(link('c-openai')+'及Wayve原公告' if is_c else link('n-msft')+'、'+link('n-meta'))+'。未披露客户金额不填零，也不猜匿名客户姓名。'))
 if is_c:
  concentration=p('Q3收入匿名客户A/B占24%/30%，合计54%；9M占33%/26%，合计59%。2025同比标签A占67%，但不同期字母可能不是同一客户，不能直接以A由67%降至24%宣称“微软占比下降43个百分点”。期末四名客户应收占18%/33%/12%/14%，合计77%，集中度还体现在回款。10-Q附注2。')
 else:
  concentration=p('Q3收入匿名客户C/D/E占15%/22%/33%，合计70%；9M分别20%/21%/21%，合计62%。期末D/E占应收75%/10%，合计85%；不能仅以客户数量扩大判断收现风险分散，也不能给C/D/E擅自对应微软/Meta/某个合作方。'+link('n-q3-notes')+'附注4。')
 append('customers','<h3>集中度、预付与订单兑现</h3>'+concentration+p('客户承诺、backlog/RPO、预付款、应收款及当期收入是不同层级。新签合同增加与收入消耗、可变对价、可取消范围变化同时影响期末订单；在缺乏完整滚动桥时，不用“期末订单变化＋收入”冒充精确新签额。'))
 if not is_c:
  append('customers','<h3 id="contract-economics">定价、预付款和回收期：只适用于披露合同群组</h3>'+table(['公司指标','Q2新签约群组','Q3新签约群组','定义 / 限制'],[['新约年化收入 / MW','约20–25 M美元','>25 M美元','1–5年合同加权；非集团全部MW'],['预计回收期','22个月','19个月','可比1–3年合同；公司收入基础模型，含运营与资本成本，未计预付款益处'],['预付覆盖相关CapEx','50%–60%','>100%','一年以上新签群组；不意味着全部在建项目都已获全额预付'],['合同额带预付比例','公司Q2口径依原文','>90%','Q3签约合同价值；不是本季度已收现金 / 集团收入']],'来源：Q3股东信；新约条款与管理层预计回收，不是本报告独立验证的现金IRR。')+p('Q3开始至11/12披露日客户新增承诺>12 B覆盖Q3及部分Q4，不能全部归入9/30 RPO。Q3新签预付覆盖率、全年资金覆盖预期和现金流表递延变动各有分母/期间；三者不可简单相乘算融资缺口。'))
  finance.append(frag(p('【条件复算】2027 CapEx40–45 B × 未被预付/资产融资覆盖的15%–25%＝6.00–11.25 B区间；75%–85%为公司预计覆盖率，非全部已到位。剩余还可由期初现金、其他融资或调整投入承担，所以该区间不是“必须增发的金额”，更不是已经发生的现金流。')))
 # Site/electricity explanations retained and corrected, no invented MW aggregation.
 sites=([
 ['Core Scientific多个园区','第三方房东 / 托管','9/30为485 MW可计费客户容量，对应590 MW已租给CRWV，105 MW在建/调试','这是房东客户电力口径；不能直接相加当CRWV总设施电力'],
 ['Polaris Forge 1（Applied Digital）','托管 / 租约及项目融资','6/5 MOU允许三号楼租约在子公司取得投资级评级条件下转让','MOU和评级条件不等于已投产；不把Polaris Forge 2其他租户容量算入'],
 ['Kenilworth等自建与合建','CRWV承担更多建设责任','旧研究的250 MW/时间表保留为项目线索，不作为本次已投产数','缺逐站验收与相同MW边界，不用历史预测加总证明指引已兑现']
 ] if is_c else [
 ['Vineland / New Jersey','第三方DataOne交付，服务Microsoft','年末预计交付超过一半；剩余批次2027 Q2','临时发电退役与Bloom主电源扩容交接，属实际交付约束'],
 ['Missouri / Lappeenranta / 第二Mäntsälä / Alabama','公司预计2027投放的自有站点','自有站点将占后续新增容量多数，管理层预测','拥有场地提高控制，不豁免许可、电力与设备风险'],
 ['AI cloud轻资产伙伴','伙伴出资、Nebius架构/软件','初始合作收入已确认，后续产能收入预计逐步形成','软件部署收入不能折算成已交付自有GW']])
 append('business','<h3 id="power-and-delivery">电力、机房和设备：谁承担哪一段？</h3>'+table(['项目 / 链路','模式','已披露状态与时点','口径限制'],sites,'来源：'+(link('c-corz-q3')+'；'+link('c-apld') if is_c else 'Q3股东信')+'。历史预测不冒充最新实绩。')+p('电网侧由公用事业公司提供接入和输配电；站点侧的变电、变压器、开关柜、冷却和机房由房东或自建主体负责；GPU服务器、集群网络和存储由云公司部署。责任边界与预付款安排决定谁承担延期和涨价。可用电、IT负载、设施总功率、已签约容量、客户验收容量不能互换；无可靠披露时，不用固定1.3–1.4倍换算凑总量。')+p('旧研究曾尝试估计“几乎全部电网供电”与逐站设备预定。此次保留研究问题与责任链，撤下缺少全组合分母的99%电网比例及天然气自发电为0等结论：少数项目资料无法认证集团电力构成。2027变压器/开关柜逐笔采购与验收并非公开完整披露，已签电力不是设备已到场。','note'))
 # Competition now compares mechanisms and constraints instead of unsupported share/price rankings.
 append('competition','<h3>neocloud相对hyperscaler的优势在哪里成立？</h3>'+table(['维度','专门AI云可能的优势','hyperscaler优势 / 反证'],[['集群性能与工程支持','专门围绕GPU网络、调度、存储调优，减少训练中断与部署时间','AWS/Azure/GCP也可做专属大集群，性能优势须按同硬件工作负载测试'],['交付与容量采购','可从多房东、GPU代际和短长约中组合，客户自建来不及时提供容量','第三方房东/供电延期会吞掉交付优势；自有站点也需资本'],['产品/客户关系','直接触达AI开发者，训练、后训练、推理与工具链联动','超大云有企业采购、数据、身份/安全和综合分发优势'],['资本与单位成本','预付款＋资产融资可匹配合同，降低部分前期资金压力','超大云融资来源、现金流与自研芯片选择更强；低票息不等于总资金成本低'],['定价权','缺电、短期算力不足时可获得溢价','客户也能自建、用ASIC或在到期后换平台；当前短缺不证明永久壁垒']],'【我的推演】竞争优势按具体工作负载、交付时点和总成本验证，不从市值或收入倍数推导。')+p('两家公司商业边界也不同：CRWV目前规模和上线容量更大；NBIS强调自研全栈、未来自有站点与轻资产伙伴组合。房东如Core Scientific/APLD出售机房/电力与托管服务，承担的GPU采购和软件经营范围不同，不直接比较集团EBITDA率来决定谁更好。'))
 # Governance: current facts plus historical date, no unsupported insider summaries.
 governance=(p('Michael Intrator为联合创始人、董事长兼CEO。A股每股1票、B股每股10票；按10/30股数，B股合计约占16.23%的经济股数、65.96%的A/B投票权，B股群体不自动等同于单个创始人。控制权与普通股经济权益不对称，须结合具体关联交易与激励判断。'+link('c-annual')+'；Q3 10-Q封面/股权附注。')+p('2025已支付29 M可赎回优先股股息、IPO及并购改变股本；NVIDIA、OpenAI等角色交叉说明融资和商业关系相互影响，不等于已经证明虚假交易。法定报表披露与关联方采购/融资安排应逐项看公允性，不能用“公司有NVIDIA股东”替代治理检验。') if is_c else p('Arkady Volozh为创始人兼CEO；A股1票、B股10票。FY2025 20-F披露截至2026-03-31，CEO家族信托约52%投票权、约11%经济权益，这是明确历史时点，不能当作11月实时比例。双层股权使创始人有持续决策控制，外部普通股股东对大额再投资和稀释的约束较弱。'+link('n-annual')+'风险因素及主要股东。')+p('2024俄罗斯业务剥离改变了法律主体资产、股票流通和历史现金；Toloka在2025失去控制后出表。不能把旧Yandex业务收入、员工或利润当作当前AI云规模。Q3对第三方交付延后进行了公开修订，这是行为事实；不凭一封股东信就评价“文化优秀”。')+p('Q3 6-K披露美国数据中心分区、许可及环境合规诉讼，可能损失尚不能估计，属于法定风险，不直接等于判定违法或停工。期末期权6.735333 M、未归属RSU5.493478 M；股权奖励会影响未来股数，但不能把二者全部按数量直接加到当前稀释股本而忽略行权价/归属条件。'+link('n-q3-notes')+'附注11/13。'))
 if is_c:governance+=p('Q3 10-Q管理层认定披露控制在合理保证层面无效，财务报告内控重大缺陷持续；同时披露这些缺陷没有导致财报重大错报。控制缺陷和已发现造假是不同结论。扩张越快，采购、资本化、关联方和现金流程控制越重要，需跟踪补救而不是只看调整后利润。')
 governance+=p('文化的研究依据是资本分配、纠错速度、对少数股东的实际结果；公司的“高性能/客户优先”自述只作为自述。尚无可靠量化数据时，不编员工评分、内部人买卖胜率或把管理层口号当护城河。')
 replace('governance',governance)
 # Remove the old stray governance paragraph outside the section after migration.
 for node in list(soup.main.find_all('p',recursive=False)):
  if 'Q3 10-Q中管理层认定披露控制' in node.text:node.decompose()
 append('moat','<h3>三年证据与侵蚀方向</h3>'+p(('2023–2025收入229→1,915→5,131 M与RPO扩大，证明公司从早期GPU部署进入规模合同交付；2026 Q3收入和利润率改善进一步支持工程/供应执行能力。但三年FCF持续为负，且普通股权益受融资/转股影响，尚未证明股东层面持续超额现金回报。' if is_c else '2023–2025 AI cloud收入9.6→68.3→480.3 M，分部调整后EBITDA−134.1→−128.5→+59.0 M；到2026 Q3增至518.2 M，支持产品/容量与运营杠杆开始形成。但2026新增合作收入、会计折旧年限与更大CapEx共同改变利润结构，不能把盈利改善全部归为软件护城河。'))+p('侵蚀者是客户自建与ASIC、GPU代际替换、缺电溢价消退、到期后重定价及融资收紧。若交付持续落后、单位现金回收恶化或客户以更低成本迁移，需下调壁垒判断；没有将收入增长简单当作切换成本的证据。'))
 # Valuation: no unsupported full-year positive earnings basis for PE skill.
 v=DATA['valuation'][sym];m=DATA['market'][sym];b=d['balance'];price=v['price'];shares=v['shares_million'];nd=v['net_debt_billion']
 valuation=p('【我的推演·条件估值】两家公司利润与现金投入尚不稳定，未来PE反推Skill已检查，因缺少可比的完整年度经营正利润而不适用。NBIS的账面正利润含投资重估，不用于正常化PE。本节改用反向企业现金流模型，回答11/16价格需要怎样的2030现金回收；所有过渡期现金流、折现率和终值假设都是研究者条件，不是市场唯一预期、公司指引或用户已确认假设。')
 valuation+=table(['市场 / 股本与财务输入','数值','时点与边界'],[['股价',f'${price:.2f}','2026-11-16正常时段收盘；非11/18实时价'],['普通股数',f'{m["common_shares_million"]:.6f} M',m['share_date']],['经济股数基准',f'{shares:.6f} M','CRWV全部A/B；NBIS另含21.065936 M低行权价预付认股权'],['经济市值',f'{v["market_cap_billion"]:.3f} B','本报告股价×经济股数，未计将来ATM/RSU/可转债转股'],['债务 / 现金',f'{b["debt_ex_leases"]/1000:.3f} / {b["cash"]/1000:.3f} B','2026-09-30；现金不含受限，不含经营租赁负债'],['净债务 / 企业价值',f'{nd:.3f} / {v["enterprise_value_billion"]:.3f} B','EV＝经济市值＋净债务；未扣非经营投资']],f'行情：Quiver历史数据；股本：{"Q3 10-Q封面" if is_c else "Q3 6-K附注14"}；债务与现金：财务主表。跨时点限制已保留，未伪造11/16最新资产负债。')
 valuation+=table(['当前倍数（历史快照）','自行复算','解释'],[['EV / 最新TTM收入',f'{v["enterprise_value_billion"]/(d["ttm"]["revenue"]/1000):.2f}x','TTM截至2026-09-30；不能与ARR倍数混用'],['EV / 2026公司收入指引',f'{v["enterprise_value_billion"]/(13.15 if is_c else 3.0):.2f}x','CRWV用13.0–13.3中点13.15 B；NBIS用原区间低端3.0 B，仅定位示意'],['现金FCF / 经济市值',f'{d["ttm"]["fcf"]/1000/v["market_cap_billion"]*100:.2f}%','CFO−现金CapEx为投入后现金流，负值不称分红收益率'],['PE','不用于经营估值','CRWV亏损；NBIS盈利受非经营重估扭曲']],'✅ 公式与数值见factcheck/full-research-results.json。比较目的在于要求兑现什么，而不是用倍数标签决定贵便宜。')
 valuation+=table(['兑现层次','公开披露及时间','本报告如何处理'],[['当前交付业务','2026 Q3已上线集群与服务，收入/利润见前文','只给同口径实绩，不把订单当现金；正常化需扣更新投入'],['商业化中的新能力',('CRWV Forge/W&B/托管推理的服务整合' if is_c else 'NBIS自有站点、Token Factory/Tavily及轻资产合作'),'产品存在与收入贡献分开；未给独立利润/收入不单独分配市值'],['2027经营节点',('年末2026产能目标及长期订单转收入，2027–2029现金预测为条件' if is_c else '2027收入12–13 B、Q4税前盈亏平衡是公司指引；不等于FCF转正'),'管理层叙事有日期，非独立验证的分析师共识'],['2029–2030现金兑现','2030 UFCF为本报告反求变量，不是公司指引','以下固定假设下求支撑价格的结果；允许不同组合解释价格']],'来源：Q3业绩稿/股东信；经营节点与研究者条件分开，未把价格残差命名为某个新产品的市场价值。')
 valuation+='<h3 id="valuation-model">从2030回到基准价格：固定输入、只反求现金流</h3>'+p('模型单位B美元。企业价值 EV₀＝Σ过渡期未杠杆自由现金流/(1+r)^t ＋ FCF₂₀₃₀/(r−g)/(1+r)^T；股权价值＝EV₀−期初净债务。企业现金流折现率r＝12%（非公司票息或已确认股东要求回报率），g＝3%，T按2026-11-16至2029-12-31实际日数/365.25＝'+f'{v["T_years"]:.3f}'+'年。2030是终值第一年；2029末不是2030现金已到账。过渡期现金流已计继续投资所需资金，因此不再把同一融资缺口作为额外债务从模型重复扣除。')
 valuation+=table(['【研究者假设】现金流到期日','2026-12-31','2027-12-31','2028-12-31','2029-12-31'],[['过渡期UFCF · B美元']+[f'{x:.2f}' for x in v['assumed_ufcf_billion']]],'UFCF为融资前、扣全部现金投入及营运资本后的现金流。这里直接设定现金回收路径以反求终点，尚非逐站预测；不由EBITDA机械替代。客户预付净变动、追加GPU与维护更新必须最终体现在该路径。')
 valuation+=p(('公司实际锚点：2026收入13.0–13.3 B、CapEx37–39 B、年末active power>1.85 GW；2027–2029完整指引未在所查Q3业绩稿提供，本表为假设现金缺口，不能称“管理层预测”。' if is_c else '公司实际锚点：2027收入12–13 B、CapEx40–45 B、Q4税前盈亏平衡及每年新增>1 GW；这些并不等于FCF转正。2027预付17–20 B和75%–85%资金覆盖预期限制融资压力，却不保证全部投资回收。本表2027 UFCF−15 B是研究者条件，不是把CapEx−预付直接当FCF。'))
 req=v['required_2030_ufcf_billion'];valuation+=p(f'【复算】✅ 在以上条件下，过渡期现金流现值为{v["pv_interim_billion"]:.2f} B；支撑基准EV {v["enterprise_value_billion"]:.2f} B，需要2030年UFCF约<strong>{req:.2f} B</strong>。这个要求是多个固定假设下的解，不是从股价唯一识别出的市场共识。')
 neededrows=[]
 for margin,rev in zip([.15,.20,.25],v['required_revenue_at_fcf_margin_15_20_25pct_billion']):
  base=13.15 if is_c else 12.5;years=4 if is_c else 3;gr=(rev/base)**(1/years)-1
  neededrows.append([f'{margin*100:.0f}%',f'{rev:.2f} B',f'{gr*100:.2f}%',('以2026指引中点13.15 B至2030，4年' if is_c else '以2027指引中点12.5 B至2030，3年')])
 valuation+=table(['假定2030 UFCF率','需2030收入','从公司指引锚点需年复合增速','时间基准'],neededrows,'UFCF率已包含维护/更新与扩张现金开支后的现金回收，非EBITDA率。15%/20%/25%均为研究者条件，不能用业务贡献利润率替代。')
 valuation+=table(['2030收入转为合同服务功率：条件示意','15 M美元/MW-year','25 M美元/MW-year','40 M美元/MW-year'],[['按20% UFCF率所需2030收入 '+f'{req/.20:.2f} B']+[f'{req/.20/density:.2f} GW' for density in [15,25,40]]],'公式：所需收入B / 每MW年收入M＝GW。三个定价密度为归一化假设，不把CRWV短约或NBIS长约直接外推整个组合；这里的合同服务MW与设施总active power未必同口径，不与公司GW直接减法。')
 valuation+=p('可行性边界：以新签MW年收入乘以未来已收费MW仅能约束收入，仍要核对GPU密度、利用率、短长约、服务范围与更新投入。公司没有给出足以认证2030稳定现金利润率的完整合同群组数据，因此本模型不以高增长自动证明终点可实现；终值金额大且高度依赖资本回收。')
 valuation+=table(['2030兑现路径','2030 UFCF · B','企业价值现值 · B','每股条件价值','相对基准价','终值现值 / EV'],[[x['scenario'],f'{x["fcf2030_billion"]:.2f}',f'{x["pv_operating_billion"]:.2f}',f'${x["per_share"]:.2f}',f'{x["upside_pct"]:+.2f}%',f'{x["terminal_pv_share_of_EV_pct"]:.1f}%'] for x in v['scenarios']],'兑现偏低/更强＝支撑终点现金流的70%/130%；过渡期路径不变。负现金流使终值现值占比可能超过100%，不是算错，也表明远期假设主导。')
 valuation+='<h3>折现、终值收缩、兑现延迟与稀释</h3>'+table(['折现率 r / 终值增长 g','2%','3%','4%'],[[f'{x["discount_rate"]*100:.0f}%']+[f'${y:.2f}' for y in x['values_for_g_2_3_4pct']] for x in v['sensitivity']],'固定上文支撑基准价的2030现金流与过渡期现金流；重新计算各折现/终值条件的每股价值，非预测区间。')
 valuation+=p('固定12%折现时，g从3%降至2%，终值相当于从2030现金流的11.11倍降至10.00倍，约收缩10%；上表相应列直接检验终值倍数收缩及杠杆后的每股影响。')
 valuation+=p(f'一年延迟压力：终点推至2031，同时在2030额外加入UFCF {v["delay_extra_ufcf_billion"]:.1f} B的现金消耗，条件价值变为${v["delay_one_year_price"]:.2f}，相对基准{(v["delay_one_year_price"]/price-1)*100:+.2f}%。这不仅是现金流平移：原设备折旧/更新、机房租金与人员费用仍可能继续；条件中用额外现金消耗表达，实际影响需按合同及站点重估。')
 valuation+=p(f'纯股权激励分配压力：若总股权价值不变且无新增现金，未来经济股数增10%/20%，每股为${price/1.1:.2f}/${price/1.2:.2f}。该敏感性适用于无偿稀释的机械边界，不能直接套ATM募资，因为ATM同时增加现金；现存可转债若转股，应同时冲减债务并加股，不能两头扣。本模型保留债务，不再把同一债券的全部潜在转股股数计入经济股本。')
 valuation+=p('结论：价格要求的核心并非只有更多收入，还包括投入逐渐转成股东可享有的现金。改变判断的新增事实是交付/收入兑现快于假设、稳定的合同现金回收及较低的维护/融资负担；反证是更高现金消耗、期限延后或持续稀释。模型没有独立验证2030经营预测，也没有给出买卖目标价；非经营投资的上行未另估，NBIS保留1,603.9 M投资账面值可作资产线索，未经交易与税/控制权调整不直接按私人估值加回。','scope')
 replace('valuation',valuation)
 # Summary/risk/tracking are aligned to corrected financial and valuation evidence.
 head_j=soup.header.find_all('p')[-1]
 head_j.clear();head_j.append(frag('<strong>【我的推演】</strong>'+('CRWV的优势是已经兑现的大规模交付和平台工程能力，约束是债务、利息和更新投入。三年收入增长不能替代资本回报；Q3利息仍远超经营利润。' if is_c else 'NBIS的优势是全栈产品和更灵活的资金/产能组合，约束是交付时点、巨大CapEx及收入质量。Q3合作收入与投资重估均需从持续服务经营中分开看。')+f' 在本报告明确的现金缺口、12%折现和3%终值增长条件下，11/16价格需要2030年UFCF约{req:.2f} B；不是只要完成下一年收入指引就足够。'))
 risk_rows=[['交付兑现',('9/30 active >1.7 GW，年末目标>1.85 GW；第三方房东仍在施工' if is_c else 'NJ剩余批次2027 Q2；原年末ARR目标移至2027年2月'),'验收/上线或公司指引变化，重算收入与现金流时间'],['收入和利润质量',('2026 Q3经营利润207 M、净利息846 M' if is_c else 'Q3战略合作325.1 M；利息含58.7 M预付/供应商融资成分'),'持续服务收入、费用分类、折旧寿命或资本化发生变化'],['融资与股权',('35M ATM尚未使用（9/30）；2027本金付款10,974 M' if is_c else 'ATM剩余7.637 M；预付认股权已纳入经济股数'),'实际提款、发股、转股、资本成本或契约改变'],['现金回收',f'TTM自算FCF {d["ttm"]["fcf"]:,.1f} M；2030条件UFCF要求{req:.2f} B','核对现金CapEx、维护更新、净预付与应收，而非只看EBITDA'],['估值依赖','r=12%、g=3%及上文过渡期现金路径，非市场共识','现金路径恶化、终值收缩或延迟时重算，不把模型中点当目标价']]
 replace('tracking',table(['风险 / 跟踪项','最新观察与边界','触发复核条件'],risk_rows,'2026-11-18核对；财务9/30、市场11/16。')+'<h3>证据限制与待验证问题</h3>'+p('三年年度、年内单季、最新TTM与主要业务数据已在本报告就地展开。公司未单列的产品级现金流、完整合同群组单位经济与逐笔设备采购不能造数；2023 NBIS集团同比缺当前口径2022重列，保留不可比而非使用旧含Toloka基数。'+('' if is_c else 'NBIS附注债务与主表28.0 M差异尚缺明确调节，已采用较保守主表口径并量化影响。'))+p('2030及逐站现金预测、未来融资/稀释条款属于待验证假设，不是未完成历史财务表的借口。若要将条件模型升级为经营预测，需补合同到期与GPU更换群组、上线验收、资本化付款和预付净变动。治理与诉讼状态仅截至本轮所查法定资料，不承诺已覆盖所有非公开事实。'))
 # Add a broad-market benchmark to the same event window.
 raw=(C/'factcheck/data/full-rebuild/qqq-prices.txt').read_text();benchmark=[]
 for day in [10,11,12,13]:
  match=re.search(re.escape(f'Nov {day}, 2026')+r' ([\d,.]+) ([\d,.]+) ([\d,.]+) ([\d,.]+)',raw)
  assert match,day
  benchmark.append(float(match.group(4).replace(',','')))
 review=soup.find(id='price-review')
 for node in list(review.find_all('p')):
  if '未加入QQQ' in node.text:
   node.replace_with(frag(p('已加入QQQ广义科技市场基准：11/10至11/13为'+f'{(benchmark[-1]/benchmark[0]-1)*100:+.2f}%'+'，11/11至11/13为'+f'{(benchmark[-1]/benchmark[1]-1)*100:+.2f}%'+'；两股后两日回撤均明显大于基准，支持存在公司/行业因素，但收益差不是beta调整超额收益，更不能证明是哪一类资金卖出。QQQ并非纯neocloud指数，分钟级时戳、仓位与因果识别仍未由收盘数据完成。<a href="#full-qqq">基准来源</a>。')))
 pf=review.find('figure');svg=pf.find('svg');pts=[]
 for i,val in enumerate(benchmark):pts.append((100+i*240,290-(val/benchmark[0]*100-80)*4.5))
 svg.append(frag('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+'" fill="none" stroke="#5369a6" stroke-width="3" stroke-dasharray="6 4"/><text x="650" y="25" fill="#5369a6">QQQ · 11/10 = 100</text>'))
 pf.figcaption.string='财报周：两股与QQQ同一起点'
 pf.find('p',class_='note').string='美股正常交易时段收盘；2026-11-10＝100；QQQ为虚线，纵轴80–130（非零起点）。事件窗口不等于11/16估值日。来源：Quiver，11/18取得。'
 price_table=review.select_one('.table-wrap table');price_table.thead.tr.append(frag('<th>QQQ收盘</th>'))
 for tr,val in zip(price_table.tbody.find_all('tr'),benchmark):tr.append(frag(f'<td>${val:.2f}</td>'))
 SRC['qqq']=('QQQ历史收盘价 · 11/18取得','https://www.quiverquant.com/stock/QQQ/historical-prices/')
 review.append(frag(p('同一阶段CRWV的10-Q还披露可取消合同触发的递延收入重分类、债务付款和长期承诺，已回写本报告订单/融资章节。因此后两天CRWV回撤也不能只归为NBIS风险外溢；具体新闻贡献需要分钟级价格与公开时戳，本报告不作未经识别的因果分摊。')))
 # One comparison table is enough; the event review links back to it.
 price_review=soup.find(id='price-review')
 for wrap in list(price_review.select('.table-wrap')):
  if '观察维度' in wrap.text:wrap.replace_with(frag(p('财报与资金需求的并列对照见<a href="#competition">竞争对手章</a>。事件窗口仅比较两股，不宣称已识别板块超额收益或资金流向。')))
 # Full audit reflects actual report coverage, not files elsewhere in the repo.
 ver=soup.find(id='verification');ver.clear();ver.append(frag('<h2>核验记录、覆盖矩阵与来源</h2>'))
 checks=[['任务与范围','主报告迁移＋最新Q3更新。2023/2024/2025三完整年，2026 Q1/Q2/Q3，最新9M/TTM，九章覆盖十一项问题。'],['营收技能执行','revenue-analysis：先写factcheck/revenue-coverage.json；取数、复算后对最终HTML年度与单季精确表逐公司验收；不以脚本或旧Markdown出现年份冒充覆盖。'],['年度来源',link('c-annual' if is_c else 'n-annual')+'；基期/权益补充'+link('c-ipo' if is_c else 'n-2024')+'。原始HTML/PDF与行提取JSON保留。'],['季度/TTM勾稽','Q1–Q3合计＝9M；Q2现金流由H1−Q1；TTM＝FY2025−可比9M2025＋9M2026。NBIS改用年报净利9.8 M重算Q4和TTM124.5 M；EPS不差分。'],['营收结构与异常','分部加总＋内部抵销＝集团；NBIS全部三个分部年度/季度金额、同比、占比展开；2023比例和超过100%有抵销解释，集团FY2023同比保留不可比。CRWV单一分部，不编软件收入。'],['资本与融资','GAAP利润桥、完整现金桥、现金CapEx/资产新增/承诺去重；新增到期、租赁、ATM实绩、并购对价和经济股数说明；普通股与优先股股息分开。'],['估值Skill','implied-valuation已检查；经营正利润基数不适用，采用条件反向DCF。折现/终值/时间、未来现金流和股本边界显式列示；计算输出在full-research-results.json。'],['重要解释迁移','电力与站点口径、设备责任/采购证据、MW价格、预付款与融资、收益重估、可取消合同、两股分化均有稳定章节；撤下未经认证的比例/匿名客户映射，未把旧预测当实绩。'],['图表选择','收入/利润与现金来源用途均用同源桑基图；年度/季度趋势分图，金额/利润率分开，负值不绝对化；图表旁保留精确表。'],['视觉与索引','由浏览器离线、禁JavaScript检查桌面/390px窄屏/A4打印；实际记录见factcheck/html-visual-checks.json。唯一HTML索引用报告工具同步并check，结构通过不替代本表内容核验。'],['边界与限制','NBIS 2022集团基期不可比；细分现金流和逐站采购没有完整公开数字；DCF终点为条件推演，NBIS债务主表/附注28 M调节缺口已量化。均在数据旁解释，不填零。'],['入口与交付','HTML为唯一维护正文；本轮没有恢复Markdown同步。历史Markdown及research.yaml原定位停更保留，HTML尚未接入旧章节读取器；网站使用唯一HTML索引。数据文件与代码不构成第二份研究正文。']]
 ver.append(frag(table(['验收项','实际结果 / 证据'],checks,'核对日期2026-11-18；财报截至2026-09-30；估值11/16收盘，事件窗口11/10–13。')))
 ver.append(frag('<h3 id="coverage-matrix">最终HTML实际覆盖矩阵</h3>'+table(['指标组 / 主体','2023–2025年度','2026 Q1–Q3','比较与勾稽','结果'],[['集团营收 / 同比 / 占比','本页年度收入表','本页单季收入表','Q1环比基期2025Q4，2025同期同比','通过；NBIS 2023同比例外单列'],['主要业务 / 抵销','CRWV单一分部；NBIS三分部＋抵销','同范围完整单季','每期加总与占比复算','通过'],['盈利 / 利润率 / SBC','年度盈利与现金表','单季表＋同比/环比变化','NBIS持续经营与归母总额分开','通过'],['CFO / 现金CapEx / FCF','年度表＋年度现金图','全部单季＋最新9M/TTM','FY−9M＋新9M，现金桥勾稽','通过'],['资产负债 / 资本分配','年度快照、CapEx与股数；2023NBIS分拆边界','9/30余额；Q3融资/承诺','债务本金、账面与租赁分开','通过；已披露小额调节缺口'],['价格隐含预期','不适用PE基数，条件DCF','市场日与期末错位注明','2030终点、延迟、终值和稀释边界','条件计算通过，非经营预测认证']],'覆盖以最终HTML精确表为准；公司未披露、不可比和研究者假设分别标注。')))
 ver.append(frag('<h3>口径与更新后的来源</h3>'+p('主体CRWV/NBIS为Nasdaq上市公司，美元报表，自然年财年。M＝百万美元，B＝十亿美元；GWh是电量，GW/MW是功率，本报告未混用。FCF为CFO减现金CapEx；收入、ARR、RPO/backlog、预付/递延及现金余额分别解释。金额补零仅统一显示，不增加原披露精度；据年报舍入金额复算的比率有舍入误差；利润率用相同主体和期间收入作分母。真实客户与渠道伙伴分开；事实、公司预测与【我的推演】显式区分。')))
 # Keep all original direct-source anchors so existing report links remain valid.
 original=BeautifulSoup(document,'html.parser').find(id='verification')
 for ul in original.find_all('ul'):
  if ul.find(id='source-c'):ver.append(ul)
 source_ul='<ul>'+''.join(f'<li id="full-{k}"><a href="{u}">{label}</a></li>' for k,(label,u) in SRC.items())+'</ul>'
 ver.append(frag(source_ul))
 ver.append(frag(p('信息跟踪渠道：优先查看公司IR业绩稿、财务报表与股东信，再核对SEC法定披露（CRWV的8-K/10-Q/10-K、NBIS的6-K/20-F）。Business Wire属于新闻分发渠道，无法打开时可从IR或SEC交叉获取；URL中的日期不代替公开时间戳，未查分发和EDGAR接收时间前，不声称已证明最早渠道。本报告未配置自动通知。')))
 ver.append(frag(p('证据与复算：各项目factcheck/full-research-results.json；CRWV/factcheck/full_research_data.py、full_report_content.py与build_html_reports.py；保存的年报表行：factcheck/data/annual-table-extracts.json；NBIS季度PDF与原始6-K、CRWV FY2025官方镜像及IPO原文。原始文件保留，不将下载失败写成未披露；网页核阅的附注选录另保存在factcheck。','note')))
 # Preserve source navigation and useful anchors; add direct links to the new evidence.
 nav=soup.nav.ol
 nav.append(frag('<li><a href="#annual-revenue">三年营收与口径</a></li><li><a href="#capital-allocation">资本分配与股数</a></li><li><a href="#valuation-model">价格隐含的2030现金流</a></li><li><a href="#coverage-matrix">最终覆盖矩阵</a></li>'))
 soup.footer.clear();soup.footer.append(frag(name+' · 2026-11-18重做 · 三年历史与Q3更新 · <a href="'+('../../Nebius公司研究/reports/main.html' if is_c else '../../CRWV/reports/main.html')+'">对照公司主报告</a>'))
 # Print compactly without shrinking scientific labels below legibility.

 for f in soup.find_all('figure'):
  if f.figcaption and any(x in f.figcaption.text for x in ['收入如何形成经营利润','现金来源与去向']):f.svg['style']='font-size:16px'
 soup.style.append('\n@media print{body{font-size:10pt;line-height:1.45}h2,h3{break-after:avoid}figure{max-width:245mm;margin:10px auto;break-inside:avoid}svg{max-height:100mm}section{margin-top:14px;padding-top:12px}.table-wrap{margin:8px 0 14px}th,td{padding:5px}p{margin:8px 0}}')
 return str(soup).replace('M USD','M美元').replace('B USD','B美元')
