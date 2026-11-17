"""Explicit reviewer decisions against every current SOP checkbox; no inference from test counts."""
from pathlib import Path
import json,re,hashlib
P=Path(__file__).resolve().parent;root=P.parent;ws=root.parent
sop=(ws/'研究流程/规范/研究更新与交付检查清单.md').read_text()
groups={};g=None
for line in sop.splitlines():
 if line.startswith('## 4.'):g='内容'
 elif line.startswith('### HTML'):g='HTML'
 elif line.startswith('### 全模块'):g='选图'
 elif line.startswith('## 5.'):break
 if g and line.startswith('- [ ]'):groups.setdefault(g,[]).append(line[6:])
# Status, actual evidence anchor(s), reviewer rationale. These are substantive review judgments.
reviews={
'内容':[
('通过（结构，保留draft/partial）','html-index-status,verification','qxo-main沿用已登记legacy入口；索引同步2026-11-17文档、2026-09-30财务与2026-11-16行情截止，正文哈希由管理工具更新并通过check。来源附件尚未批准发布，保留draft与unpublished_links，不称verified或已发布。'),
('通过','judgment,business,revenue,financials,customers,competition,industry,valuation,governance,moat','九章/十一项已定位；核心矛盾前置，订单和资本分配归属明确。'),
('通过（可比边界已说明）','revenue,coverage-review','2023—2025三完整财年，2026Q1—Q3集团及已披露产品均展示；前身软件及并表变化不能当连续建材增长。'),
('通过','financials,coverage-review','年度、单季、9M与TTM分表；Q1环比使用2025Q4，亏损比较金额，季节性就近说明。'),
('通过','revenue,financials,verification','M美元、股数、EPS及百分比/百分点分开。'),
('未通过','source-version-note,financials','发现并量化跨版本净利息和税项差异，部分超过通常舍入上限；主表已核，变动成因未确认，不将1.51容差等同原因核验通过。'),
('通过','income-flow,profit-bridge,financials','Q3毛利→费用→经营利润→净利润已可复算；2024/25经营亏损有费用桥和非经营解释。'),
('不适用（已核查）','financials','展示期间毛利率未超100%，没有以冲回或小分母解释不存在的负成本；2024高净利率由利息收入解释。'),
('未通过','financials,source-version-note,gaps','2024现金利息、收购摊销、营运资金成因已有依据；2025Q3异常税项事件细分与版本差异仍无完整证据。'),
('通过','judgment,profit-bridge,cash-full-flow,verification','用户追问的收入流向已补；税项改善与税前恶化、融资摊薄和现金压力说明保留，并在复验记录揭示限制。'),
('通过','financials,valuation,tracking','最新财务截止沿用9月30日，TTM及已交割C融资一致；回购授权不当执行。'),
('通过','financials,valuation','利润/现金、净利息/其他收益、税前/税后、摊销及股份支付均区分；桥已勾稽。'),
('通过（披露范围内）','cash-full-flow,financials','三年及9M现金资本分配、股票并购对价、租赁与承诺区分；未披露采购承诺不填零。'),
('通过','valuation','行情11月16日常规收盘、股数11月6日、资产负债9月30日均明确；本轮不是行情刷新。'),
('通过（条件分析）','valuation','公开40亿目标与研究反推分开；业务提效、2030兑现窗口、关键经营条件和反证明确。'),
('通过（条件分析）','valuation','固定收入/爬坡、税率、资本开支等，求解2030 EBITDA；对照现有基数、公司目标与终值敏感性。'),
('未通过','valuation,gaps','现金流及终值已折现，但优先股分配/转换路径和期权时间价值只作近似，跨时点净债务冻结；不得将条件模型等同完整资本定价。'),
('通过（条件分析）','valuation','既有、40亿兑现、延迟两年且费用增加、8倍压缩四路径已计算，终值现值占比及偏离结果常驻显示。'),
('通过','judgment,valuation,risks,gaps','未称市场唯一预期/AI残差/成功概率；重要估值限制已同步摘要、风险及缺口。'),
('未通过（整体门槛）','gaps,sop-review','完整资本定价、同业期后调整和异常/版本归因仍存在未通过项；已披露这些限制，但不能据此标整篇完成。'),
('通过（证据范围内）','customers','两个实名材料下单案例及阶段已核，网页无发布日期则注明核查日；无逐笔发票/金额未伪造，合作方不当客户。'),
('通过（本地证据）','verification','来源、计算输入及相对路径有效；HTML入口不兼容如实说明。原始资料留存，旧research.yaml章节提取与新HTML整页索引区分，来源/事实核验与结构检查分开。')],
'HTML':[
('通过','contents,verification','章节、目录、来源和核验锚点有效，原有id保留。'),
('通过','judgment,verification','文档/财务/行情日期分列，表旁期间单位明确；未将展示日期冒充更新财务。'),
('通过','business,customers','付费方、交付和收入确认可读；真实案例与机制解释区分，主营收入相邻。'),
('通过','revenue','实绩、10月管理层口径、2030目标和未提供短期量化指引分列；未编指引区间。'),
('通过','income-flow,cash-deficit-bridge,cash-full-flow','收入主图后接独立现金缺口桥，已显示完整现金桑基图链接；负406不是期末现金。'),
('通过','customers,financials,governance','实名案例/RPO/回收期限同章；自身租赁在资本分配；治理用薪酬、关联交易与关键人行为证据。'),
('通过','income-flow,cash-full-flow,verification','新桑基图与底表共用flow_data；金额从原10-Q带id标签抽取；各期间图表口径分别明确。'),
('通过','revenue,financials,valuation','年度/季度/累计/TTM分开；净亏损与CFO缺口保留正负，未使用双轴/3D。'),
('通过','income-flow','原构成条图已替换；产品互斥可加总，自有品牌不重复计入；无未知余额伪造。'),
('通过（本轮纠正）','income-flow,cash-full-flow','收入利润前段和现金来源净用途已补桑基图；没有虚构产品费用分摊。'),
('通过（本轮纠正）','cash-deficit-bridge,profit-bridge','局部瀑布图分别说明负缺口余额与负净利润终点、替代范围和另一处桑基图锚点；不只在聊天说明。'),
('通过（本轮纠正）','income-flow,cash-full-flow,cash-deficit-bridge','负净利没有豁免收入前段，负CFO按现金净用途处理；遗漏已补图，没有把写理由当绘图完成。'),
('通过','income-flow,cash-full-flow','带宽统一比例、节点守恒；2百万利润及3/4百万小流量不增粗，文本补充可读性，逐项机械核验。'),
('通过','cash-full-flow,cash-deficit-bridge,profit-bridge','现金来源/用途各12129；净CFO未重复扣工资/采购，融资父子项不重复，桥终点可勾稽。'),
('通过（适用范围内）','revenue,financials','增长桥保留原有范围−66；没有将净利润到CFO负调节画饼；两个局部瀑布图标签及符号视觉复核。'),
('待视觉复核','verification','改图后重新离线渲染桌面/窄屏/打印；在观察最终版本前不标通过。'),
('通过（静态页面）','contents,verification','核心内容不依赖JS，无筛选/图例交互；链接可键盘访问，宽表容器滚动，来源/本地资源有效。'),
('通过','verification','唯一HTML正文，原始事实与计算脚本不作第二正文；HTML未接入research.yaml明确记录，算术检查独立于内容结论。')],
'选图':[
('通过','income-flow,cash-full-flow,cash-deficit-bridge,profit-bridge','两张桑基图解释分配，两个瀑布图解释局部负值变化；非重复图，邻近精确底表、来源和边界保留。'),
('不适用（图形）','business,customers','未另画无金额的付费/股权图；文字交易链路及实名案例保留，无客户金额或留存造数。'),
('通过','revenue,financials','增长桥仅剔除并表贡献，未造量价拆分；净利→CFO→FCF已公式勾稽，未来SBC经济成本未忽略。'),
('不适用（图形）','business,industry','没有建设产能时间线，分销/安装模式不套制造良率；收购日期明确实际发生，不作预测产能。'),
('不适用（图形）','financials,customers','未画股数桥或RPO滚动桥；实际股数与SBC费用分开，RPO18个月为预计，不伪造取消/季度分摊。'),
('未通过（精确估值比较）','competition,valuation,gaps','份额/价格未披露不造图，条件估值非共识；同业Q3年化代理保留，完整稀释与期后并购调整仍未完成。'),
('通过','moat,risks','壁垒证据矩阵及风险传导有事实和边界，无主观雷达或概率评分，相关不当因果。'),
('通过','verification,sop-review','财务算术、来源变动、选图与视觉分别记录，未通过项不能被77项或新增技术检查覆盖。')]
}
assert all(len(groups[k])==len(reviews[k]) for k in groups),[(k,len(groups[k]),len(reviews[k])) for k in groups]
visual=P/'visual_checks.json'
qa=json.loads(visual.read_text()) if visual.exists() else {}
# Only an observed re-audit visual check can resolve the pending item.
visual_pass=qa.get('audit_revision')=='sop-reaudit-2026-11-17' and qa.get('status')=='passed'
items=[]
for g,requirements in groups.items():
 for n,(req,r) in enumerate(zip(requirements,reviews[g]),1):
  state,anchors,note=r
  if state=='待视觉复核' and visual_pass:state='通过';note='新版收入/现金桑基图、局部瀑布图及完整页面已离线复核桌面、窄屏与打印；证据visual_checks.json。'
  items.append({'id':f'{g}-{n:02}','requirement':req,'result':state,'evidence':anchors.split(','),'review':note})
result={'date':'2026-11-17','revision':'sop-reaudit-2026-11-17','basis':'研究方式.md及研究流程/规范/研究更新与交付检查清单.md（2026-11-17）','sop_sha256':hashlib.sha256(sop.encode()).hexdigest(),'scope':'QXO原报告的完整内容/选图复验；沿用财报2026-09-30、行情2026-11-16，不刷新行情','overall':'未通过完整研究验收','items':items,'summary':{'total':len(items),'passed':sum(x['result'].startswith('通过') for x in items),'failed':sum(x['result'].startswith('未通过') for x in items),'not_applicable':sum(x['result'].startswith('不适用') for x in items),'pending':sum(x['result'].startswith('待') for x in items)}}
(P/'sop_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result['summary'],ensure_ascii=False))
