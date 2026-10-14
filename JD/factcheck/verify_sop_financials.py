"""Recompute JD three-year financial tables using dated manual primary-source inputs.
Run from any directory. Prints results; preserves original evidence unchanged.
Cash CapEx includes asset acquisitions but excludes business combinations.
"""
import json
from pathlib import Path
base = Path(__file__).resolve().parent
x = json.loads((base / 'data/sop_inputs_20261009.json').read_text())
revenues = json.loads((base / 'data/revenue_inputs_20261005.json').read_text())
valuation = json.loads((base / 'data/valuation_inputs_20261007.json').read_text())
prior_equity = x['opening_equity_2022']
prior_shares = x['opening_shares_2022']
r = {}
for year, d in x['annual'].items():
    organic = d['ppe'] + d['land'] + d['construction']
    cash_capex = organic + d['asset_acq']
    capex_bridge = cash_capex - d['property_sales'] - d['disposals']
    assert abs(capex_bridge - d['net_capex']) <= 1, (year, 'net CapEx bridge')
    assert d['cfo'] + d['consumer'] - d['net_capex'] == d['company_fcf'], (year, 'FCF')
    assert prior_shares + d['issued'] + d['exercised'] + d['vested'] - d['repurchased'] == d['shares'], (year, 'share bridge')
    assert d['liabilities'] + d['total_equity'] + d['mezzanine'] == d['assets'], (year, 'balance sheet')
    rv = revenues['rows'][year]
    assert sum(rv[:4]) == d['revenue'] == sum(rv[5:9]), (year, 'revenue reconciliation')
    r[year] = dict(gross_profit=d['revenue']-d['cost'], cash_capex=cash_capex,
        default_fcf=d['cfo']-cash_capex, company_fcf=d['company_fcf'],
        roe_pct=100*d['net'] / ((prior_equity+d['equity'])/2),
        net_cash=d['cash']+d['short_investments']-d['debt'],
        interest_cover=d['op']/d['interest'],
        net_share_change_pct=100*(d['shares']/prior_shares-1),
        capex_bridge_rounding_difference=capex_bridge-d['net_capex'],
        revenue_shares_pct=[100*v/d['revenue'] for v in rv])
    prior_equity, prior_shares = d['equity'], d['shares']
assert sum(x['debt_maturities_2025_long_term_borrowings_only']) == 44872
assert sum(x['lease_cash_payments_2025']) == 38177
marketcap = valuation['price_usd']*valuation['ordinary_shares_million']/valuation['ads_shares']*valuation['rmb_per_usd']
r['reference'] = dict(marketcap_rmb_million=marketcap,
    default_fcf_yield_2025_pct=100*r['2025']['default_fcf']/marketcap,
    company_fcf_yield_2025_pct=100*r['2025']['company_fcf']/marketcap,
    company_fcf_yield_ttm_pct=100*31415/marketcap,
    conditional_ev_ex_nci=marketcap+69892-221662,
    conditional_ev_book_nci=marketcap+69892-221662+63257,
    convertible_initial_potential_shares=2e9/1000*21.883*2,
    convertible_initial_dilution_pct=100*(2e9/1000*21.883*2)/prior_shares)
print(json.dumps(r, ensure_ascii=False, indent=2))
