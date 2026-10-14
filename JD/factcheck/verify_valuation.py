from pathlib import Path
import json

d=json.loads((Path(__file__).resolve().parent/'data/valuation_inputs_20261007.json').read_text())
value=d['price_usd']*d['ordinary_shares_million']/d['ads_shares']*d['rmb_per_usd']
ttm=d['2025FY']['net_income']-d['2025H1']['net_income']+d['2026H1']['net_income']
adj=d['2025FY']['non_gaap_net_income']-d['2025H1']['non_gaap_net_income']+d['2026H1']['non_gaap_net_income']
print('参考市值亿美元',value/d['rmb_per_usd']/100,'人民币亿元',value/100)
print('TTM PE',value/ttm,'调整PE',value/adj,'2025PE',value/d['2025FY']['net_income'],'PB',value/d['2026-06-30']['parent_equity'])
print('股息率',d['dividend_usd_per_ads']/d['price_usd']*100)
print('2025ROE',d['2025FY']['net_income']/((d['2024FY']['parent_equity']+d['2025FY']['parent_equity'])/2)*100)
print('TTMROE',ttm/((d['parent_equity_2025H1']+d['2026-06-30']['parent_equity'])/2)*100)
print('2026H1ROE',d['2026H1']['net_income']/((d['2025FY']['parent_equity']+d['2026-06-30']['parent_equity'])/2)*100)
for income in [150,250,350]: print('情景',income,value/100/income)
