"""Reproduce JD's disclosed segment operating-profit bridge; inputs in RMB millions."""
import csv
from pathlib import Path

base = Path(__file__).resolve().parent
with (base / 'data' / 'segment_profit.csv').open(encoding='utf-8', newline='') as f:
    rows = {r['period']: r for r in csv.DictReader(f)}
keys = ('retail', 'logistics', 'new_businesses', 'unallocated', 'group')
for period, row in rows.items():
    for key in keys:
        row[key] = int(row[key])
    residual = sum(row[k] for k in keys[:-1]) - row['group']
    if residual:
        raise ValueError(f'{period}: bridge residual {residual}')
    print(f'{period}: bridge verified, group={row["group"]/100:.2f}亿元')
for before, after in [('2024FY', '2025FY'), ('2025Q2', '2026Q2'), ('2025H1', '2026H1')]:
    deltas = {k: rows[after][k] - rows[before][k] for k in keys}
    print(f'{before} -> {after}: ' + ', '.join(f'{k}={v/100:+.2f}亿元' for k, v in deltas.items()))
    print(f'New-business contribution / group change: {deltas["new_businesses"] / deltas["group"]:.2%}')
print(f'2025 retail profit growth: {rows["2025FY"]["retail"]/rows["2024FY"]["retail"]-1:.2%}')
print(f'2025 group operating profit change: {rows["2025FY"]["group"]/rows["2024FY"]["group"]-1:.2%}')
