"""Sourced cycle research, maintained as part of the existing HTML report builder."""
import json
from pathlib import Path

SOURCES = {
 'tf': ('TrendForce原始调查/预测，2026-11-19', 'https://www.trendforce.com/presscenter/news/20261119-13314.html'),
 'july': ('TrendForce历史预测，2026-07-21', 'https://www.trendforce.com/presscenter/news/20260721-13148.html'),
 'sep': ('TrendForce历史预测，2026-09-30', 'https://www.trendforce.com/presscenter/news/20260930-13258.html'),
 'hana': ('Hana证券原始研报，2026-11-12，PDF第8页', 'https://file.hanaw.com/download/research/FileServer/WEB/industry/industry/2026/11/11/Semi_Indepth_261112_F.pdf'),
 'kioxia': ('铠侠Investor Day原始问答，2026-06-02，第1/3页', 'https://www.kioxia-holdings.com/content/dam/kioxia-hd/en-jp/ir/library/event/asset/Investor-Day-2026-Eng-QA.pdf'),
 'kioxia_deck': ('铠侠原始Investor Day演示，2026-06-02，第17页', 'https://www.kioxia-holdings.com/content/dam/kioxia-hd/en-jp/ir/library/event/asset/Kioxia-Investor-Day-2026-en.pdf'),
 'kioxia_actual': ('铠侠Integrated Report 2026，10月公开', 'https://www.kioxia-holdings.com/content/dam/kioxia-hd/en-jp/ir/library/integrated-report/2026/asset/Integrated-Report-2026-all-en.pdf'),
 'sk': ('SK hynix原始Q3公告，2026-10-28', 'https://news.skhynix.com/en/q3-2026-business-results/'),
 'm17': ('SK hynix原始投资公告，2026-08-07', 'https://news.skhynix.com/en/fab-facility-investment-2026/'),
 'mu': ('Micron原始建厂公告，2026-01-26', 'https://investors.micron.com/news/press-release/2026/Micron-Breaks-Ground-on-Advanced-Wafer-Fabrication-Facility-in-Singapore-01-26-2026/default.aspx'),
 'samsung': ('Samsung原始Q3公告，2026-10-29', 'https://news.samsung.com/global/samsung-electronics-announces-third-quarter-2026-results'),
}

CYCLE_POSITION_CSS = """
.cycle-position{margin:18px 0 26px;padding:clamp(14px,3vw,30px);background:#fff;border:1px solid #c9d6d3;border-radius:12px}
.cycle-position figcaption{font-size:13px;color:#52676c}
.cycle-stages{display:grid;grid-template-columns:repeat(3,1fr) minmax(72px,1.65fr) 1fr;list-style:none;margin:0 0 22px;padding:0;text-align:center}
.cycle-stages li{display:grid;grid-template-rows:24px 18px auto;align-items:center;font-size:14px;color:#52676c;line-height:1.35}
.cycle-stages .cycle-current{font-size:12px;font-weight:700;color:#125b51}
.cycle-stages .cycle-marker{position:relative;display:grid;place-items:center;height:18px}
.cycle-marker::before{content:"";position:absolute;inset:8px 0 auto;border-top:2px solid #becdc9}
.cycle-stages li:first-child .cycle-marker::before{left:50%}
.cycle-stages li:last-child .cycle-marker::before{right:50%;border-top-style:dashed}
.cycle-stages [aria-current] .cycle-marker::before{border-image:linear-gradient(to right,#becdc9 50%,#2b8076 50%) 1}
.cycle-marker::after{content:"";position:relative;width:9px;height:9px;border:2px solid #839c96;border-radius:50%;background:#fff}
.cycle-stages [aria-current] .cycle-marker::after{width:14px;height:14px;border-color:#125b51;background:#125b51;box-shadow:0 0 0 3px #d9efe8}
.cycle-stages .cycle-stage-label{margin-top:7px}
.cycle-stages [aria-current] .cycle-stage-label{color:#125b51;font-weight:750}
.cycle-signals{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;list-style:none;margin:0 0 15px;padding:0}
.cycle-signals li{padding:10px 12px;border:1px solid #dce5e1;border-radius:8px;background:#f5f8f7;font-size:14px;line-height:1.5}
.cycle-signals small{display:block;margin-bottom:2px}
@media(max-width:560px){#position{margin-top:26px;padding-top:14px;font-size:21px}.cycle-signals{grid-template-columns:1fr}.cycle-signals small{display:inline;margin-right:8px}}
@media print{.cycle-position{break-inside:avoid;print-color-adjust:exact}}
"""


def cycle_position_figure():
 return """<figure class="cycle-position" id="cycle-position-chart" aria-labelledby="cycle-position-caption">
<ol class="cycle-stages" aria-label="NAND 行业周期阶段">
 <li><span></span><span class="cycle-marker" aria-hidden="true"></span><span class="cycle-stage-label">筑底</span></li>
 <li><span></span><span class="cycle-marker" aria-hidden="true"></span><span class="cycle-stage-label">复苏</span></li>
 <li><span></span><span class="cycle-marker" aria-hidden="true"></span><span class="cycle-stage-label">上行</span></li>
 <li aria-current="step"><span class="cycle-current">当前判断</span><span class="cycle-marker" aria-hidden="true"></span><span class="cycle-stage-label">高景气后段</span></li>
 <li><span></span><span class="cycle-marker" aria-hidden="true"></span><span class="cycle-stage-label">下行</span></li>
</ol>
<ul class="cycle-signals" aria-label="判断依据">
 <li><small>现货 · 调查</small><strong>渠道价格已转弱</strong></li>
 <li><small>合约价 · 预测修订</small><strong>仍预计上涨，涨幅下修</strong></li>
 <li><small>供给 · 2027 年预测</small><strong>预计有效供给加速</strong></li>
</ul>
<figcaption id="cycle-position-caption">截至 2026-11-19 · 周期阶段示意，转入下行尚待确认。<a href="#cycle-evidence">查看数据和口径</a></figcaption>
</figure>"""


def build_cycle(page,p,h,table,industry,company):
 def src(*keys):return p('来源：'+' · '.join(f'<a href="{SOURCES[k][1]}">{SOURCES[k][0]}</a>' for k in keys))
 b=h('position','一、现在位于周期哪一段？')+cycle_position_figure()
 b+=p('【研究判断，2026-11-19】全球NAND处于高景气后段：现货/渠道已转弱，合约仍涨但斜率放缓，供应商利润处高位，2027供给加速。尚不能把全行业称为已经衰退，更不能从强财报判断刚进入上行初期。AI抬高需求基数、改变产品结构并可能延长景气，但没有消除供给响应和库存周期。')
 b+=p('边界：全球NAND及客户端/企业SSD；DRAM/HBM为资本竞争参照，不计入NAND产量。行业观察截至2026-11-19；厂商财报、项目指引、机构估计和本文压力模型分开。')
 b+=table('cycle-evidence',['指标','观察及出处性质','周期含义/限制'],[
 ['现货','11月19日TrendForce称近期回调超过20%【调查】','渠道先行转弱；不是所有eSSD已经同幅降价'],
 ['合约','4Q26整体涨幅预测由9月30日15–20%下修至11月19日8–13%【预测修订】','还在上涨，但边际定价权减弱；不是已实现季度涨幅'],
 ['利润','闪迪最新季度GAAP毛利率85.0%，下季调整后指引中点85.0%【实绩/指引】','高利润平台；利润峰值可能滞后现货拐点'],
 ['库存','渠道去库存；中国CSP存在高库存及采购下修【机构调查】','库存分布不均；没有全行业库存天数序列，不能断言各厂均积压'],
 ['供给','2027 bit供给预计+25–30%【预测】','未来有效产出增长，不能只数新厂数量'],
 ['价格前景','1Q27整体合约价预计环比0至-5%；2Q27起所有类别进入下行【预测】','构成顶部附近判断的前瞻证据，尚非已经实现']])
 b+=src('tf','sep')+p('【推演】典型传导链：涨价/高利润→厂商扩产及客户提前采购→消费降规格/渠道去库存→现货转弱→合约重谈→利润下滑。当前证据集中在中间几步，不能精确宣布某天见顶。个股股价与这条链可能领先或背离，不用股价下跌反证产业已衰退。')
 b+=p('【历史预测的变化】7月调查预计2026供给缺口4–5%、2H27转松；11月调查把合约降价起点提前至1Q27。这是同一机构的预测下修，不是两份独立证据，也不是已经量到的2027过剩率。')+src('july')
 b+=h('ai','二、AI改变了需求结构，为什么仍然会有周期？')
 b+=p('AI增加服务器本地盘、训练数据/检查点、向量及检索库、日志和可复用上下文缓存的存储需求。KV cache只是其中一项；其活跃层通常依赖HBM/DRAM，SSD卸载规模随模型、保留时间、命中率和架构变化，不能由token量直接乘出刚性采购。软件压缩和复用也会减少每单位工作负载所需容量。')
 b+=p('【框架】需求bit＝设备/服务器数量×单机NAND容量；供给bit≈晶圆投入×每片可售容量×良率。AI可能持续推高第一式，但高价也会压低手机/PC出货和容量，另一边QLC/高层数迁移不断提高供给。NAND不是HBM：不受完全相同的堆叠封装、GPU验证和DRAM晶圆约束，不能把HBM短缺直接搬过来。')
 b+=p('企业SSD的固件、耐久、控制器和认证形成局部瓶颈，使消费NAND和特定eSSD可以一弱一强；共享基础NAND制造又使这种隔离并不永久。生产商扩充合格产品、客户完成认证后，短缺也会缓解。AI更可能改变周期的高度、长度及各产品相位，而非取消周期。')
 b+=table('opposing-views',['证据链','观点及日期','怎样验证'],[
 ['SK hynix当事人观点','10月28日预计memory供不应求延续至2030；包括DRAM/HBM，不是单独NAND预测','看NAND实际出货/价格，不把集团表述当纯NAND缺口'],
 ['Samsung当事人观点','10月29日预计2027 AI需求强于供给，并增加QLC SSD供应','企业SSD订单落地、供应增量及单独NAND价格'],
 ['TrendForce独立调查','11月19日美国CSP仍上修需求，但中国采购削减及消费走弱使总量承压','中国库存下降后是否补单；美国增量能否反超'],
 ['Hana卖方估计','11月12日预计2027晶圆产能增加8%；观点整体偏多','晶圆增幅不等于bit增幅，且部分底层数据来自TrendForce，非完全独立']])+src('sk','samsung','hana')
 b+=h('expansion','三、几大厂商有没有扩产？有，但路径和时间不同')
 b+=table('vendor-expansion',['厂商/制造体系','已公布动作及性质','2027与之后的意义'],[
 ['Kioxia / Sandisk联盟','铠侠6月计划FY26 CapEx 4,500亿日元，FY25为2,800亿；FY27维持相近水平，投BiCS8/10、四日市Fab7和北上Fab2【公司计划】','支出复算+60.71%；支持CY25–28 GB年复合增长22%的目标，非每年保证产量。两家公司共享制造体系，不能把同一厂算两次'],
 ['Samsung','Q3公告增加QLC SSD供应；2026 DS总CapEx指引76.8万亿韩元【公司计划】；Hana估西安小幅扩张【机构估计】','DS含DRAM/代工，不能全算NAND；未取得官方NAND单列金额及2027每月片数'],
 ['SK hynix / Solidigm','Q3公告4Q26国内321层占比超过一半【计划】；Hana估Solidigm 2027增逾20k片/月【估计】','工艺升级和QLC增供先发生；不可把M15X的HBM扩产当NAND'],
 ['SK hynix M17','8月公告M17建厂投资19.1万亿韩元，首间洁净室2028年12月启用【批准投资/计划】','不是2027量产；洁净室启用也不等于满负荷可售产出。与7月更大长期投资愿景不是可叠加两笔'],
 ['Micron','新加坡新增NAND fab计划十年投入240亿美元，晶圆产出始于2H28【公司计划】','新厂不应计入2027新增供给；2027仍可来自旧厂升级。新加坡2027 HBM封装项目另算'],
 ['YMTC','Hana估2027月产能200k→270k片【机构估计，+35%】','不是公司承诺或已验收产量；设备、良率、层数和客户资格决定可售bit']])
 b+=src('kioxia','samsung','sk','m17','mu','hana')
 b+=p('铠侠原始演示另列FY26–28平均年度CapEx约4,700亿日元，相对FY25实际2,837亿约+65.67%；这是三年平均计划，不等于问答中单年4,500亿。其2026综合报告称北上Fab2于2025年9月开工生产、2026年7月新产线开始BiCS10生产，故联盟并非只在宣布遥远项目；但仍未给一致口径2027可售EB。')+src('kioxia_deck','kioxia_actual')
 b+=p('结论：并非所有厂商都在2027开大新厂，但行业已在扩充有效bit供给。优先利用现有厂房、装设备和提升密度，往往比新建厂更早影响价格。宣布投资→施工→洁净室→设备→良率爬坡→客户认证→可售出货，是不同阶段；美元CapEx不能直接换成EB。')
 b+=h('supply','四、2027到底增多少？把晶圆、bit、金额分开')
 wafer=1431/1.08;capex=29.9/1.267
 b+=table('supply-definitions',['口径','2027公开估计','本文复算/限制'],[
 ['晶圆产能（Hana）','1,431k片/月，同比约+8%',f'倒推2026约{wafer:,.1f}k，净增加约{1431-wafer:,.1f}k片/月；四舍五入输入，非已实产'],
 ['可供bit（TrendForce）','同比+25–30%','2026供应归一100→125–130；没有公开绝对EB，不能伪造EB'],
 ['NAND行业CapEx（TrendForce）','299亿美元，同比+26.7%',f'倒推2026约{capex:.2f}B美元，增约{29.9-capex:.2f}B；非全部转为当年产能'],
 ['密度/良率等综合项（跨口径示意）','(1+bit增幅)/(1+晶圆增幅)−1','约+15.74%至+20.37%；不能称纯工艺效率，两个机构的时点/利用率定义未完全一致']])+src('tf','hana')
 b+=p('各厂片数只是机构估计，不能相加后声称精确闭合；尤其晶圆产能是某时点能力而bit供给为全年流量。行业数据的精度足以检验“没有扩产/AI消除周期”，不足以给精确价格底部。')
 b+=h('balance-model','五、需求需要多强，才能吃掉这批供给？')
 b+=p('【本文假设模型，非机构预测】令2026供给=100、需求=104.5，4.5%仅取7月缺口4–5%的中值并假设分母为供给，非11月现状测量。假设2027供给+25–30%，则需求需增长19.62–24.40%才能平衡；若2026本来已平衡，门槛就是25–30%。初始缺口分母和大小会改变门槛，不能假装已知道。')
 rows=[]
 for dg in [.10,.20,.25,.30]:
  d=104.5*(1+dg)
  rows.append([f'{dg:.0%}',f'{d:.2f}',f'{(125/d-1)*100:+.2f}%',f'{(130/d-1)*100:+.2f}%'])
 b+=table('balance-values',['2027总需求增长假设','需求指数','供给125：供需差/需求','供给130：供需差/需求'],rows)
 b+=p('正数表示供给超过需求，负数表示不足；全为压力情景。再设服务器占2026 bit需求40%、其余60%不变或下降5%，要让总需求增长20–25%，服务器bit必须增长约50–62.5%，或57.5–70%。40%是便于复算的近似假设，7月机构称实际已超过40%，不是闪迪数据中心收入占比。服务器增长30%、其余下降5%时，总需求仅增9%。AI需求很强和全行业过剩可以同时成立。')
 b+=h('falsification','六、什么会推翻“高景气后段”的判断？')
 b+=table('cycle-triggers',['支持高景气延续','支持周期回落','观察窗口'],[
 ['中国CSP库存消化后补单，美国采购持续上调','中国削单继续超过北美增量','2027采购及后续两季订单'],
 ['供给爬坡明显低于25–30%预测，厂商减产','QLC/层数升级按期兑现，消费需求继续降规格','2027有效bit而非厂房面积'],
 ['合约未出现预计降价，eSSD保持溢价','1Q27合约下降、2Q扩散到企业级','CY2027；不混闪迪财年'],
 ['客户履约、NBM单位售价/现金保护有效','重谈、退款、应收库存占用扩大','公司未来10-Q与电话会']])
 b+=h('verification','本轮行业核验与边界')+p('2026-11-19专项重做：明确周期位置、AI双向机制、五大制造体系扩供路径、2027量化供需敏感性；公司首页、行业模块与估值联动。原始公司披露与机构原始研报按产品/时间区分，Hana与TrendForce共享部分底层数据。算式已复算；预测不标成事实。仍缺各厂一致口径实际wafer/良率/EB序列与长期协议完整定价条款，不能精确测量当前供需缺口。')
 b+=p('2026-11-20 展示更新：周期阶段图按 11 月 19 日证据区分现货调查、合约价预测修订和供给预测。已检查桌面、手机和打印版离线显示，以及图下底表跳转；窄屏底表可横滑。')
 cycle_html=page('NAND｜周期位置、AI需求与扩产',b,'nand.html')
 cycle_html=cycle_html.replace('<style>','<style>'+CYCLE_POSITION_CSS,1)
 cycle_html=cycle_html.replace('更新 2026-11-19　|　全球NAND与SSD','展示更新 2026-11-20　|　全球NAND与SSD',1)
 (industry/'cycle.html').write_text(cycle_html)
 overview=p('更新2026-11-19｜全球NAND与SSD。判断：高景气后段，消费/渠道转弱与AI企业需求并存；2027供给响应是核心。')+'<div class="cards"><a class="card" href="cycle.html"><b>周期、AI与扩产</b>现在在哪一段？AI能否改变周期？五大制造体系怎样扩供？<p>含2027晶圆/bit区分和需求平衡情景。</p></a></div>'
 (industry/'nand.html').write_text(page('NAND 行业研究',overview,'nand.html'))
 company_body=p('【研究判断，2026-11-19】闪迪处于高景气利润平台，而非周期底部。行业现货已回落、合约涨幅下修；AI企业SSD增长可延长景气，却不足以证明全公司跨周期盈利稳定。是否便宜取决于未来价格/成本和NBM保护，不能用高峰季度PE回答。')
 company_body+=p('<a href="../../../行业研究/NAND/reports/cycle.html">完整行业研究：周期位置、AI双向机制、厂商扩产及2027供需模型</a>。全球NAND边界，不把HBM/DRAM需求代入本公司供需。')
 company_body+=h('cycle-answers','三项核心问题，对闪迪分别意味着什么')+table('sndk-cycle-answers',['问题','结论','公司证据/反证'],[
 ['周期位置','高景气后段，局部先转弱；未确认所有合约已下降','最新毛利率85%是后视利润；Edge bit同比-20%、Consumer下降>70%，不支持需求普涨'],
 ['AI能否改变周期','抬高数据中心需求/产品门槛，未证明消除价格周期','Datacenter收入43.53%，但Edge/Consumer仍合计56.47%；收入占比不是bit占比'],
 ['厂商是否扩产','联盟、韩国、美国、中国均有供给响应；2027以旧厂升级和局部扩张为主','Kioxia 22%GB增长目标与299亿美元行业CapEx估计，意味着不能假设永久无供给'],
 ['NBM能否隔离','可能减缓销量/现金波动，未证明锁住85%毛利率','RPO88.9B与部分bit覆盖提供能见度；价格重设、退出/退款/违约条款未完整公开']])
 company_body+=src('tf','kioxia')
 company_body+=h('company-cycle','从行业到闪迪利润，不能只讲宏观')+p('若行业价格回落，Edge/OEM与零售先承压；数据中心认证与长协可能延后传导。因为高价产品组合和合同节奏不同，公司ASP/GB不必与现货同比例变化。反过来，行业仍缺货也不等于每个季度公司价格都能继续涨。')
 company_body+=p('投资判断应分三层：①季度利润/现金已经很强；②未来一两季能见度部分由NBM与eSSD订单支持；③FY2029可维持何种利润率仍未证明。当前报价较历史高位低，并不能证明跨周期便宜。新增供给、价格回落与工艺降成本三者必须同时进入估值。')
 company_body+=p('时间对齐：机构预测的CY1Q27约对应闪迪FY2027 Q3，CY2Q27约对应FY2027 Q4；当前Q2指引主要对应2026年末。所以下季指引强与明年合约价下行预测可以同时成立。若后续CY1Q27价格仍稳定、客户没有削量而供给爬坡推迟，本报告偏周期后段的判断需要上修，不能固守空头结论。')
 company_body+=p('<a href="valuation.html#cycle-profit">估值联动：bit增长与价格下降同时发生时，利润会怎样？</a>；<a href="business-model.html#nbm">NBM条款与订单边界</a>；<a href="cash-capital.html#balance">联盟投入及资金承诺</a>。')
 evidence={'as_of':'2026-11-19','sources':SOURCES,'nature':'issuer plans / institutional forecasts / author scenarios separated','model':{'supply_2026':100,'demand_2026_assumed':104.5,'supply_growth_2027':[.25,.30],'demand_growth_scenarios':[.10,.20,.25,.30]},'checks':{'kioxia_capex_growth_pct':(450/280-1)*100,'wafer_2026_inferred_k':wafer,'capex_2026_inferred_b':capex,'demand_growth_to_balance':[(s/104.5-1) for s in [125,130]]}}
 here=Path(__file__).resolve().parent
 evidence['profit_stress']=[{'asp_change':a,'revenue_m':11031*1.22*(1+a),'operating_profit_m':11031*1.22*(1+a)-1653*1.22*.85-598*1.1} for a in [-.1,-.2,-.4,-.6]]
 assert abs((450/280-1)*100-60.714285714)<1e-6
 assert abs((125/104.5-1)*100-19.61722488)<1e-6
 assert abs((130/104.5-1)*100-24.40191388)<1e-6
 evidence['check_result']='算式复算通过；机构预测和公司计划未当实绩'
 (here/'cycle-evidence-2026-11-19.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2))
 return company_body
