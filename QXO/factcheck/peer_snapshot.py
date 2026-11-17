from pathlib import Path
import json
P=Path(__file__).resolve().parent
rows=[
 {'ticker':'BLDR','price':60.15,'shares':107.603,'debt':4658.904,'finance_lease_added':0,'cash':55.012,'quarter_ebitda':311.1,'debt_basis':'principal, already includes finance leases and other finance obligations'},
 {'ticker':'IBP','price':231.97,'shares':26.578484,'debt':1053.4,'finance_lease_added':10.8,'cash':415.9,'quarter_ebitda':128.3,'debt_basis':'carrying value of current and long-term debt; plus finance leases, debt issuance fees not added back'}]
for x in rows:
 x['marketcap']=x['price']*x['shares'];x['EV']=x['marketcap']+x['debt']+x['finance_lease_added']-x['cash'];x['EV_to_Q3_annualized_adjEBITDA']=x['EV']/(4*x['quarter_ebitda'])
result={'price_date':'2026-11-16 US regular close','capital_balance_date':'2026-09-30','units':'MUSD, million shares, USD per share','source_prices':{'BLDR':'https://finance.yahoo.com/quote/BLDR/','IBP':'https://finance.yahoo.com/quote/IBP/'},'source_financials':{'BLDR':'https://www.sec.gov/Archives/edgar/data/1316835/000119312526437728/bldr-20260930.htm','IBP':'https://www.sec.gov/Archives/edgar/data/1580905/000162828026070582/ibp-q32026earningsrelease.htm'},'limitations':'Quarterly annualization is not TTM or forecast. IBP November acquisitions and refinancing are not reflected in September debt. Peer capital instruments/SBC not comprehensively option-valued. Cannot be used as a precise cheapness ranking.','rows':rows}
(P/'peer_snapshot.json').write_text(json.dumps(result,indent=2));print([(x['ticker'],x['marketcap'],x['EV'],x['EV_to_Q3_annualized_adjEBITDA']) for x in rows])
