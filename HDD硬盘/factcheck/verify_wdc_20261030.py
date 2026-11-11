import json
from pathlib import Path
p=Path(__file__).resolve().parent/'data'/'wdc_2026-10-30'
rows=[json.loads(x) for f in ['latest_facts.jsonl','comparatives.jsonl'] for x in (p/f).read_text().splitlines()]
def get(field,date,start=None):
 r=[x for x in rows if x['standard_field']==field and x['report_date']==date and not x['dimensions'] and (start is None or x['period_start']==start)]
 v={x['value_numeric'] for x in r};assert len(v)==1,(field,date,v)
 return v.pop()/1e6
rev=get('revenues','2026-10-02','2026-07-04')
for f in ['revenues','gross_profit','operating_income','net_income','net_cash_from_operations','capital_expenditures']:
 a=get(f,'2026-10-02','2026-07-04');b=get(f,'2025-10-03','2025-06-28')
 print(f,a,b,'YoY%',round((a/b-1)*100,2))
fcf=get('net_cash_from_operations','2026-10-02','2026-07-04')-get('capital_expenditures','2026-10-02','2026-07-04')
print('FCF',fcf,'margin%',fcf/rev*100)
print('TTM revenue',12919+rev-2818)
print('TTM FCF',3511+fcf-(get('net_cash_from_operations','2025-10-03','2025-06-28')-get('capital_expenditures','2025-10-03','2025-06-28')))
print('quarter ROE%',1779/((8864+9348)/2)*100)
print('revenue QoQ%',(4381/3747-1)*100,'guidance midpoint QoQ%',(5100/4381-1)*100)
