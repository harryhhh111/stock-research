import json
from pathlib import Path
base=Path(__file__).resolve().parent
rows=json.loads((base/'data/cash_flow.json').read_text())['rows']
output=[]
for r in rows:
 x=dict(period=r['period'],ocf_margin=r['ocf']/r['revenue']*100,fcf_margin=r['fcf']/r['revenue']*100,cash_change_before_fx=r['ocf']+r['icf']+r['fin'])
 for key in ['ocf','fcf']:
  prior=r['prior_'+key]
  x[key+'_yoy']=None if prior is None else (r[key]/prior-1)*100
 output.append(x)
(base/'现金流计算结果.json').write_text(json.dumps(output,ensure_ascii=False,indent=2))
print(json.dumps(output,ensure_ascii=False,indent=2))
