from pathlib import Path
import json
x=json.loads((Path(__file__).resolve().parent/'data/affiliates_inputs_20261007.json').read_text())['JD_Property']
print('2024产发营收同比',f"{(x['2024FY']['revenue']/x['2023FY']['revenue']-1)*100:.2f}%")
for period in ['2023FY','2024FY','2025_9M']:
    r=x[period]
    print(period, '收入/净利润/调整利润（亿元）',r['revenue']*10,r['net_profit']*10,r['adjusted_profit']*10)
print('说明：算术核验通过，不等于已独立审计媒体转述值；九个月不年化。')
