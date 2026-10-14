"""Recalculate Toshiba ratios. Input: manually transcribed official tables, JPY bn.
Paths are relative to this script. Does not modify source data.
"""
import csv
from pathlib import Path
from decimal import Decimal as D
DATA = Path(__file__).resolve().parent / 'data' / 'toshiba' / 'financials.csv'
with DATA.open(encoding='utf-8', newline='') as f:
    rows = {r['period']: r for r in csv.DictReader(f)}
for name, r in rows.items():
    sales, op = D(r['net_sales']), D(r['operating_income'])
    cash_sum = D(r['operating_cash_flow']) + D(r['investing_cash_flow'])
    assert abs(cash_sum-D(r['reported_fcf'])) <= D('0.1')
    print(f"{name}: operating margin={op/sales*100:.2f}%; OCF+ICF={cash_sum} JPY bn")
for current, prior in [('FY2025','FY2024'),('FY2026Q1','FY2025Q1')]:
    for field in ['net_sales','operating_income']:
        value = (D(rows[current][field])/D(rows[prior][field])-1)*100
        print(f'{current} {field} YoY={value:.2f}%')
    r=rows[current]
    ratio=D(r['kioxia_income'])/(D(r['operating_income'])+D('2412.9' if current=='FY2025' else '6348.9'))*100
    print(f'{current} Kioxia-related income / pretax income={ratio:.2f}% (not net-income contribution)')
print(f'M12 SMR max capacity vs MA11: {(D(34)/D(28)-1)*100:.2f}%')
print(f'1 decimal EB at 24TB/drive: {D(1000000)/D(24):.0f} drives; at 34TB/drive: {D(1000000)/D(34):.0f} drives')
print(f'Hypothetical EB supply: drive units 2x, 24TB->34TB: {D(2)*D(34)/D(24):.2f}x; NOT actual Toshiba guidance')
