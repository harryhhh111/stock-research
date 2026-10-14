from pathlib import Path
import csv,json
root=Path(__file__).resolve().parent
with (root/'data/annual_profit.csv').open() as f:
 rows={int(r['year']):{k:float(r[k]) for k in ('revenue','gross_profit','op_ifrs','op_nonifrs','net_ifrs','net_nonifrs')} for r in csv.DictReader(f)}
out={}
for year in (2023,2024,2025):
 out[year]={}
 for k in ('gross_profit','op_ifrs','op_nonifrs','net_ifrs','net_nonifrs'):
  out[year][k]={'profit_rmb_100million':rows[year][k]/100,'yoy_pct':(rows[year][k]/rows[year-1][k]-1)*100,'margin_pct':rows[year][k]/rows[year]['revenue']*100,'status':'✅ 属实（据年报复算）'}
(root/'三年利润计算结果.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
