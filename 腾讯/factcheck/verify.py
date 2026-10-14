"""Run with Python 3; source values in data/inputs.csv, monetary figures RMB million."""
from pathlib import Path
import csv, json
base = Path(__file__).resolve().parent
with (base / 'data/inputs.csv').open() as f:
    rows = list(csv.DictReader(f))
v = {r['key']: float(r['value']) for r in rows}
out = {}
def put(name, value, formula):
    out[name] = {'value': round(value, 4), 'formula': formula, 'status': '✅ 属实（据所列输入复算）'}
for key in ['vas', 'marketing', 'fintech', 'other']:
    put(f'q2_{key}_share_pct', v[f'q2_{key}']/v['q2_revenue']*100, f'q2_{key}/q2_revenue*100')
put('q2_revenue_growth_pct', (v['q2_revenue']/v['q2_2025_revenue']-1)*100, '(q2_revenue/q2_2025_revenue-1)*100')
put('q2_gross_margin_pct', v['q2_gross_profit']/v['q2_revenue']*100, 'q2_gross_profit/q2_revenue*100')
put('q2_capex_ratio_pct',v['q2_capex']/v['q2_revenue']*100,'q2_capex/q2_revenue*100')
put('q2_capex_growth_pct',(v['q2_capex']/v['q2_2025_capex']-1)*100,'(q2_capex/q2_2025_capex-1)*100')
put('h1_capex_growth_pct',(v['h1_capex']/v['h1_2025_capex']-1)*100,'(h1_capex/h1_2025_capex-1)*100')
put('q2_fcf_rounded',v['q2_ocf']-v['q2_capex_paid']-v['q2_content_paid']-v['q2_lease_paid'],'q2_ocf-q2_capex_paid-q2_content_paid-q2_lease_paid; input rounded')
put('q2_compute_prepaid_inferred',v['q2_fcf_ex_prepaid']-v['q2_fcf'],'q2_fcf_ex_prepaid-q2_fcf; inferred from rounded figures')
put('q2_new_ai_operating_drag',v['q2_op_ex_ai']-v['q2_op_adjusted'],'q2_op_ex_ai-q2_op_adjusted; rounded, not total AI spend')
put('h1_capex_vs_fy2025_pct',v['h1_capex']/v['fy2025_capex']*100,'h1_capex/fy2025_capex*100')
for kind in ['ifrs','adjusted']:
    eps=v[f'fy2025_eps_{kind}']-v[f'h1_2025_eps_{kind}']+v[f'h1_eps_{kind}']
    put(f'ttm_diluted_eps_{kind}_approx',eps,f'fy2025_eps_{kind}-h1_2025_eps_{kind}+h1_eps_{kind}; period share counts vary')
    put(f'rmb_counter_pe_{kind}_approx',v['rmb_counter_price']/eps,f'rmb_counter_price/ttm_diluted_eps_{kind}_approx')
put('hkd_dividend_yield_pct',v['hkd_dividend']/v['hkd_price']*100,'hkd_dividend/hkd_price*100; historical paid dividend')
put('interest_bearing_debt',v['borrowings_current']+v['borrowings_noncurrent']+v['notes_noncurrent'],'borrowings_current+borrowings_noncurrent+notes_noncurrent; excludes leases')
put('net_cash_decline_from_yearend',v['yearend_net_cash']-v['q2_net_cash'],'yearend_net_cash-q2_net_cash')
put('h1_revenue_growth_pct',(v['h1_revenue']/v['h1_2025_revenue']-1)*100,'(h1_revenue/h1_2025_revenue-1)*100')
put('capital_commitment_multiple',v['capital_commitments']/v['yearend_capital_commitments'],'capital_commitments/yearend_capital_commitments')
put('other_commitment_multiple',v['other_commitments']/v['yearend_other_commitments'],'other_commitments/yearend_other_commitments')
put('related_party_revenue_share_pct',v['related_party_revenue']/v['h1_revenue']*100,'related_party_revenue/h1_revenue*100; not single-customer concentration')
put('indicative_rmb_equity_value',v['rmb_counter_price']*v['june_shares']/1e6,'rmb_counter_price*june_shares/1e6; June shares, October price, indicative only')
for current, prior in [('fy2023', 'fy2022'), ('fy2024', 'fy2023'), ('fy2025', 'fy2024'), ('h1', 'h1_2025'), ('q2', 'q2_2025')]:
    total_delta = v[current+'_revenue'] - v[prior+'_revenue']
    for segment in ['revenue', 'vas', 'marketing', 'fintech', 'other', 'games', 'social']:
        ck, pk = current+'_'+segment, prior+'_'+segment
        if ck not in v or pk not in v:
            continue
        put(ck+'_yoy_pct', (v[ck]/v[pk]-1)*100, f'({ck}/{pk}-1)*100')
        if segment != 'revenue':
            put(ck+'_growth_contribution_pct', (v[ck]-v[pk])/total_delta*100,
                f'({ck}-{pk})/({current}_revenue-{prior}_revenue)*100; games and social are VAS subsets')
for period in ['fy2024', 'fy2025', 'h1_2025', 'h1', 'q2']:
    for metric in ['gross_profit', 'op_ifrs', 'op_nonifrs', 'net_ifrs', 'net_nonifrs']:
        key = period+'_'+metric
        put(key+'_margin_pct', v[key]/v[period+'_revenue']*100, f'{key}/{period}_revenue*100; net uses attributable profit')
put('q2_liabilities_assets_pct', v['q2_liabilities']/v['q2_assets']*100, 'q2_liabilities/q2_assets*100')
put('q2_interest_bearing_debt_assets_pct', (v['borrowings_current']+v['borrowings_noncurrent']+v['notes_noncurrent'])/v['q2_assets']*100, '(borrowings_current+borrowings_noncurrent+notes_noncurrent)/q2_assets*100; excludes leases')
for metric in ['ocf', 'fcf', 'fcf_ex_prepaid']:
    put('q2_'+metric+'_margin_pct', v['q2_'+metric]/v['q2_revenue']*100, f'q2_{metric}/q2_revenue*100; rounded cash inputs')
(base/'计算结果.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
