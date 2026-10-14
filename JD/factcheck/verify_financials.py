"""Recalculate JD financial ratios, cash flow and snapshot valuations.
Inputs in RMB millions. FX/share dates deliberately differ from price date;
market value is a reference estimate, not an exchange-reported live market cap.
"""
import json
from pathlib import Path
base = Path(__file__).resolve().parent
x = json.loads((base / 'data' / 'financial_inputs_20261005.json').read_text())
r = {}
for period in ('2024FY', '2025FY', '2025H1', '2026H1'):
    d = x[period]
    calculated = d['cfo'] + d['consumer_adjustment'] - d['capex']
    if calculated != d['fcf']:
        raise ValueError(f'{period}: free cash flow does not reconcile')
    r[f'{period}_fcf'] = calculated
for period in ('2025FY', '2026H1'):
    d = x[period]
    if sum(d[k] for k in ('retail_revenue','logistics_revenue','new_revenue','eliminations')) != d['revenue']:
        raise ValueError(f'{period}: segment revenues do not reconcile')
    if sum(d[k] for k in ('electronics','general','marketplace','services_other')) != d['revenue']:
        raise ValueError(f'{period}: revenue categories do not reconcile')
    r[f'{period}_services_share_pct'] = 100*(d['marketplace']+d['services_other'])/d['revenue']
for k in ('revenue','net_income','non_gaap_net_income','cfo','consumer_adjustment','capex','fcf'):
    r[f'ttm_{k}'] = x['2025FY'][k] - x['2025H1'][k] + x['2026H1'][k]
if r['ttm_cfo'] + r['ttm_consumer_adjustment'] - r['ttm_capex'] != r['ttm_fcf']:
    raise ValueError('TTM cash flow does not reconcile')
b = x['2026-06-30']
r['gross_cash'] = b['cash']+b['restricted']+b['short_investments']
r['cash_ex_restricted'] = b['cash']+b['short_investments']
r['financial_debt'] = sum(b[k] for k in ('short_debt','long_debt','current_notes','noncurrent_notes'))
r['lease_liabilities'] = b['current_leases']+b['noncurrent_leases']
r['net_cash_ex_restricted'] = r['cash_ex_restricted']-r['financial_debt']
r['net_cash_after_leases'] = r['net_cash_ex_restricted']-r['lease_liabilities']
r['current_ratio'] = b['current_assets']/b['current_liabilities']
r['liabilities_to_assets_pct'] = 100*b['liabilities']/b['assets']
r['inventory_increase'] = b['inventory']-x['2025-12-31']['inventory']
r['payables_increase'] = b['payables']-x['2025-12-31']['payables']
r['roe_2025_pct'] = 100*x['2025FY']['net_income']/((x['2024FY']['parent_equity']+x['2025FY']['parent_equity'])/2)
r['reference_marketcap_usd_million'] = x['price_usd']*x['ordinary_shares_million']/x['ads_shares']
r['reference_marketcap_rmb_million'] = r['reference_marketcap_usd_million']*x['rmb_per_usd']
r['reference_ttm_pe'] = r['reference_marketcap_rmb_million']/r['ttm_net_income']
r['reference_ttm_non_gaap_pe'] = r['reference_marketcap_rmb_million']/r['ttm_non_gaap_net_income']
r['reference_pb'] = r['reference_marketcap_rmb_million']/b['parent_equity']
r['reference_group_fcf_yield_pct'] = 100*r['ttm_fcf']/r['reference_marketcap_rmb_million']
r['dividend_yield_pct'] = 100*x['dividend_usd_per_ads']/x['price_usd']
r['share_reduction_h1_pct'] = 100*(2742-2688)/2742
r['logistics_external_share_pct'] = 100*x['logistics_external_revenue_2025']/x['logistics_total_revenue_2025']
r['logistics_internal_growth_contribution_pct'] = 100*(80314.094-55061.616)/(217146.986-182837.584)
r['h1_income_change_pct'] = 100*(x['2026H1']['net_income']/x['2025H1']['net_income']-1)
r['h1_revenue_change_pct'] = 100*(x['2026H1']['revenue']/x['2025H1']['revenue']-1)
r['gross_margin_2024_pct'] = 100*(1-x['2024FY']['cost']/x['2024FY']['revenue'])
r['gross_margin_2025_pct'] = 100*(1-x['2025FY']['cost']/x['2025FY']['revenue'])
for earnings in (15000,25000,35000):
    r[f'scenario_pe_{earnings}'] = r['reference_marketcap_rmb_million']/earnings
print(json.dumps(r,ensure_ascii=False,indent=2))
