"""AWS投入强度复算；历史输入来自2025年报Note10，季度输入Q3 10-Q Note8。单位B美元。"""
from pathlib import Path
import json
b=Path(__file__).resolve().parent
inputs={'2023':{'revenue':90.757,'op':24.631,'additions':24.843,'depreciation':12.531,'ppe':72.701},'2024':{'revenue':107.556,'op':39.834,'additions':53.267,'depreciation':13.320,'ppe':110.683},'2025':{'revenue':128.725,'op':45.606,'additions':96.496,'depreciation':21.450,'ppe':190.055},'2025_9m':{'revenue':93.146,'op':33.141,'additions':64.808,'depreciation':14.882},'2026_9m':{'revenue':125.803,'op':48.555,'additions':147.236,'depreciation':24.583,'ppe':313.009},'2025Q3':{'revenue':33.006,'op':11.434,'additions':28.301,'depreciation':5.648},'2026Q3':{'revenue':45.984,'op':17.773,'additions':57.116,'depreciation':9.230}}
r={}
for k,d in inputs.items():r[k]={**d,'addition_revenue_pct':d['additions']/d['revenue']*100,'addition_depreciation_multiple':d['additions']/d['depreciation'],'depreciation_revenue_pct':d['depreciation']/d['revenue']*100,'op_margin_pct':d['op']/d['revenue']*100}
for a,c in [('2025_9m','2026_9m'),('2025Q3','2026Q3')]:
 r[c]['yoy_pct']={k:(inputs[c][k]/inputs[a][k]-1)*100 for k in ['revenue','op','additions','depreciation']}
r['depreciation_sensitivity']={str(z):{'extra_cost':9.230*z,'op':17.773-9.230*z,'margin_pct':(17.773-9.230*z)/45.984*100} for z in [.1,.2]}
(b/'aws-spending-results-2026-11-04.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(r['2026_9m']));print(json.dumps(r['depreciation_sensitivity']))
