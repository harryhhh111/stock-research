"""CORZ 数值复算。只读快照、打印结果，无第三方依赖。"""
import json
from pathlib import Path

d = json.loads((Path(__file__).resolve().parent / 'data/inputs_20260921.json').read_text())
q, h, b, c, a, v = (d[k] for k in ['q2', 'h1', 'balance', 'coreweave', 'amd', 'valuation'])
results = {
    'Q2 托管营收占比 %': q['colo']/q['revenue']*100,
    'H1 托管营收占比 %': h['colo']/h['revenue']*100,
    'Q2 托管毛利 M$': q['colo']-q['colo_cost'],
    'Q2 托管毛利率 %': (q['colo']-q['colo_cost'])/q['colo']*100,
    'Q2 自营挖矿毛利 M$': q['mining']-q['mining_cost'],
    'Q2 自营挖矿毛利率 %': (q['mining']-q['mining_cost'])/q['mining']*100,
    'Q2 剔除权证变动后的机械净亏损 M$': q['net_loss']+q['warrant_change'],
    'H1 OCF-PP&E-土地支出 M$': h['ocf']-h['ppe_cash']-h['land_cash'],
    '账面现金扣除后的面值净债务 M$': b['debt_face']-b['cash'],
    '全部现有票息年额 M$': b['senior_debt']*b['senior_coupon']+b['convert_2029']*b['convert_coupon'],
    'CoreWeave 每 IT MW 年均收入 M$': c['annual_revenue']/c['it_mw'],
    'CoreWeave 每 gross MW 年均收入 M$': c['annual_revenue']/c['gross_mw'],
    'CoreWeave 隐含每kW月 $': c['annual_revenue']*1e6/c['it_mw']/1000/12,
    'CoreWeave 项目利润低端 M$': c['annual_revenue']*c['margin_low'],
    'CoreWeave 项目利润高端 M$': c['annual_revenue']*c['margin_high'],
    'Q2 比2025年末增加计费 MW': c['billing_q2']-c['billing_2025'],
    '7月 比2025年末增加计费 MW': c['billing_july']-c['billing_2025'],
    '7月到CoreWeave全部完成剩余 MW': c['it_mw']-c['billing_july'],
    'AMD+neocloud精确已签 MW': a['direct_it']+a['neocloud_it'],
    '全部已签 MW': c['it_mw']+a['direct_it']+a['neocloud_it'],
    'AMD组合均年收入下界 M$': a['tcv_floor']/a['years'],
    'AMD组合每MW年均收入下界 M$': a['tcv_floor']/a['years']/(a['direct_it']+a['neocloud_it']),
    '旧股数乘新股价示意基本市值 M$': v['basic_shares']*v['price'],
    '基本股数示意EV M$': v['basic_shares']*v['price']+b['debt_face']-b['cash'],
    '公司proforma股数乘股价权益敏感性 M$': v['company_pro_forma_shares']*v['price'],
    'Polaris 每gross MW收购价 M$': d['polaris']['cash_price']/d['polaris']['gross_mw'],
}
assert abs(q['colo']+q['mining']+q['hosted_mining']-q['revenue']) < 1e-8
assert abs(q['lease_fixed']+q['lease_variable']-q['colo']) < 1e-8
for name, value in results.items():
    print(f'{name}: {value:,.4f}')
