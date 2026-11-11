"""从已保存公司新闻稿表格提取并复算；不需要网络。单位 M USD。"""
import json,re
from pathlib import Path
from bs4 import BeautifulSoup
BASE=Path(__file__).resolve().parent
DATA=BASE/'data'/'q3-2026'
def tables(name):
    soup=BeautifulSoup((DATA/name).read_text(),'html.parser')
    return [[ [c.get_text(' ',strip=True) for c in tr.find_all(['td','th'])] for tr in t.find_all('tr')] for t in soup.find_all('table')]
def row(ts,label):
    for t in ts:
        for r in t:
            if r and r[0].strip()==label:
                vals=[]
                for x in r[1:]:
                    x=x.replace(',','').replace('$','').replace('%','').replace(' ','')
                    if x in ['','—']: 
                        if x=='—': vals.append(0)
                        continue
                    if re.fullmatch(r'\(?-?\d+(\.\d+)?\)?',x): vals.append(float(x.strip('()'))*(-1 if '(' in x else 1))
                if vals:return vals
    raise ValueError(label)
keys={'revenue':'Revenue','op':'Operating income','interest':'Interest expense, net','net':'Net loss','ebitda':'Adjusted EBITDA','adj_op':'Adjusted operating income','cfo':'Net cash provided by operating activities','capex':'Purchases of property and equipment, including capitalized internal-use software','sbc':'Stock-based compensation expense'}
out={}
for q in ['q1','q2','q3']:
    ts=tables(q+'-release.html'); d={}
    for k,l in keys.items():
        aliases=[l]
        if k=='op':aliases+=['Operating income (loss)','Operating loss']
        if k=='cfo':aliases+=['Net cash provided by']
        if k=='capex':aliases+=['Purchase of property and equipment, including capitalized internal-use software']
        for a in aliases:
            try:d[k]=row(ts,a);break
            except ValueError:pass
        assert k in d,(q,k)
    out[q]={k:v[0] for k,v in d.items()}
    z=out[q];z['cash_capex']=abs(z['capex']);z['fcf']=z['cfo']-z['cash_capex']
    z['revenue_yoy_pct']=(z['revenue']/d['revenue'][1]-1)*100
    z['op_margin']=z['op']/z['revenue']*100;z['net_margin']=z['net']/z['revenue']*100;z['ebitda_margin']=z['ebitda']/z['revenue']*100
    z['gross_margin']=(z['revenue']-row(ts,'Cost of revenue')[0])/z['revenue']*100
assert sum(out[q]['revenue'] for q in out)==8314
assert sum(out[q]['net'] for q in out)==-2075
assert sum(out[q]['cfo'] for q in out)==5638
assert sum(out[q]['cash_capex'] for q in out)==23558
q3=out['q3'];q3['revenue_qoq_pct']=(3661/2575-1)*100
assert 207-846+13-83==-709
assert -709+1889+846+160+83-13==2256
assert 1975-9836+7361==-500
out['ttm']={'revenue':8314+1572,'net':-2075-452,'cfo':5638+1559,'cash_capex':23558+4060,'fcf':5638+1559-23558-4060}
out['balance']={'cash':4122,'restricted_cash':1405+877,'debt_ex_leases':9183+1389+32417+3884,'finance_leases':296+353,'operating_leases':668+18029,'net_debt_ex_leases':9183+1389+32417+3884-4122,'equity':4025}
(BASE/'q3-2026-results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
