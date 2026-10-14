"""复算融资情景；输入为注明来源的人工摘录，运行不修改文件。"""
import json
from pathlib import Path
p = Path(__file__).resolve().parent / 'data' / '2026-09-17-financing-inputs.json'
d = json.loads(p.read_text())
n = d['class_a'] + d['class_b']
s = d['atm_shares']
atm_b = s * d['reference_price'] / 1e9
print(f'总普通股: {n:,}; 全额ATM后: {n+s:,}')
print(f'新增股数/旧股本: {s/n:.6%}; 原股东持股比例降幅: {s/(n+s):.6%}')
print(f'ATM毛额情景: ${atm_b:.5f}B')
for b in (d['base_convert_b'], d['base_convert_b'] + d['option_b']):
    print(f'可转债 ${b:.1f}B: 总债务情景 ${d["debt_b"]+b:.1f}B; 合计融资毛额 ${atm_b+b:.5f}B; 年票息 ${b*d["coupon_low"]*1000:.3f}M–${b*d["coupon_high"]*1000:.3f}M')
print('短约每MW 3/6个月收入情景: $10M / $20M（$40M年化，假定全期履约）')
