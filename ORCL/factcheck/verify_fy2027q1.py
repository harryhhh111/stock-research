"""复算FY2027 Q1更新；输入保留公司披露值，结果单位M美元。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / 'data/fy2027q1_inputs.json').read_text())
a, old, q = (data[k] for k in ('fy26', 'fy26q1', 'fy27q1'))
b = data['balance_q1']
growth = lambda x, y: (x / y - 1) * 100
rows = {}
for key in ('revenue', 'cloud', 'iaas', 'saas', 'software', 'license', 'support', 'hardware', 'services'):
    rows[key] = {'current': q[key], 'prior': old[key], 'yoy_pct': growth(q[key], old[key]),
                 'group_share_pct': q[key] / q['revenue'] * 100}
assert q['cloud'] == q['iaas'] + q['saas']
assert q['software'] == q['license'] + q['support']
assert q['revenue'] == sum(q[k] for k in ('cloud', 'software', 'hardware', 'services'))
assert old['revenue'] == sum(old[k] for k in ('cloud', 'software', 'hardware', 'services'))
ttm = {k: a[k] - old[k] + q[k] for k in ('revenue', 'operating_income', 'net_income', 'common_income', 'cfo', 'capex', 'sbc')}
ttm['fcf'] = ttm['cfo'] - ttm['capex']
net_capex = q['capex'] - q['prepayments'] - q['other_capex_finance']
assert net_capex == 17966
assert q['cfo'] - q['capex'] == -5396
assert q['cfo'] - q['capex'] + 13111 - 81 + 11 == 7645
debt = b['current_debt'] + b['noncurrent_debt']
net_debt = debt - b['cash'] - b['marketable']
lease_net_debt = net_debt + b['operating_lease'] + b['finance_lease']
cap = data['price']['value'] * b['shares_m']
roe = data['roe_fy26']
result = {
 'period': '2025-09-01..2026-08-31', 'revenue_rows': rows,
 'q1_yoy_pct': {k:growth(q[k],old[k]) for k in ('operating_income','net_income','common_income','eps','cfo','capex','interest')},
 'q1_margins_pct': {'operating':q['operating_income']/q['revenue']*100,'net':q['net_income']/q['revenue']*100},
 'op_margin_change_pp':q['operating_income']/q['revenue']*100-old['operating_income']/old['revenue']*100,
 'operating_profit_bridge_m': {'revenue_increase':4419,'cloud_software_cost_increase':-2793,'hardware_cost_increase':-103,'services_cost_decrease':47,'sales_marketing_savings':252,'rd_savings':90,'amortization_savings':218,'restructuring_savings':321},
 'ttm':ttm,'net_cash_capex':net_capex,'cfo_excluding_specific_prepayment':q['cfo']-q['prepayments'],
 'net_debt':net_debt,'lease_inclusive_net_debt':lease_net_debt,
 'roe_fy26_pct':roe['net_income']/((roe['begin_parent_equity']+roe['end_parent_equity'])/2)*100,
 'q1_roe_not_annualized_pct':q['net_income']/((42508+66772)/2)*100,
 'shares_qoq_pct':growth(b['shares_m'],data['balance_fy26']['shares_m']),
 'valuation':{'market_cap_m':cap,'ev_excluding_leases_and_preferred_m':cap+net_debt,'market_cap_to_ttm_common_income':cap/ttm['common_income'],'ttm_diluted_eps_sum':a['eps']-old['eps']+q['eps'],'pe_diluted_eps_sum':data['price']['value']/(a['eps']-old['eps']+q['eps']),'guidance_pe':data['price']['value']/8.10,'fcf_yield_pct':ttm['fcf']/cap*100},
 'nov2_coupon_m':2000*.07+1750*.0745+2250*.0785+2500*.08+1500*.0865,
 'rpo_next_12months_m':664000*.13,
 'q1_qoq_pct': {k:growth(q[k],v) for k,v in {'operating_income':6133,'net_income':4304,'eps':1.45,'cfo':14620,'capex':16493}.items()},
 'prepayment_share_of_cfo_increase_pct':q['prepayments']/(q['cfo']-old['cfo'])*100,
 'net_margin_change_pp':q['net_income']/q['revenue']*100-old['net_income']/old['revenue']*100,
 'ttm_operating_margin_pct':ttm['operating_income']/ttm['revenue']*100,
 'ttm_net_margin_pct':ttm['net_income']/ttm['revenue']*100,
 'ttm_capex_to_cfo_pct':ttm['capex']/ttm['cfo']*100,
 'guidance_revenue_growth_pct':growth(90000,a['revenue']),
 'future_30b_fcf_to_snapshot_market_cap_pct':30000/cap*100,
}
assert sum(result['operating_profit_bridge_m'].values()) == q['operating_income']-old['operating_income']
assert abs(result['nov2_coupon_m'] - data['nov2']['annual_coupon_m']) < 0.001
output = ROOT / 'fy2027q1_results.json'
output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
