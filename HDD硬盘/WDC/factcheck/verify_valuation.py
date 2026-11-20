"""Recalculate the 2026-11-19 report's valuation tables from its disclosed inputs."""

import json
import re
from datetime import date
from hashlib import sha256
from pathlib import Path
from xml.etree import ElementTree


REPORTS = Path(__file__).resolve().parent.parent / 'reports'


def table_rows(path, table_id):
    html = path.read_text(encoding='utf-8')
    match = re.search(rf'<table id="{re.escape(table_id)}"[^>]*>.*?</table>', html, re.S)
    table = ElementTree.fromstring(match[0].replace('&nbsp;', '&#160;'))
    return [[''.join(cell.itertext()) for cell in row] for row in table.findall('./tbody/tr')]


def number(cell):
    return float(re.search(r'-?[\d,]+(?:\.\d+)?', cell)[0].replace(',', ''))


def check(cell, value, label):
    shown = re.search(r'-?[\d,]+(?:\.(\d+))?', cell)
    decimals = len(shown[1] or '')
    if abs(number(cell) - value) > 0.5 * 10 ** -decimals + 1e-9:
        raise ValueError(f'{label}: reported {cell}, calculated {value}')


def value(flows, discount, terminal_growth, years):
    weights = [(1 + discount) ** -year for year in years]
    terminal = flows[-1] * (1 + terminal_growth) / (discount - terminal_growth)
    return (
        flows[0] * years[0] * weights[0]
        + sum(amount * weight for amount, weight in zip(flows[1:], weights[1:]))
        + terminal * weights[-1]
    )


def reverse(market_cap, baseline, discount, terminal_growth, years):
    # Solve for the annual FCF multiplier by bisection.
    low, high = 0.5, 2.0
    for _ in range(64):
        growth = (low + high) / 2
        flows = [baseline * growth ** i for i in range(1, 5)]
        if value(flows, discount, terminal_growth, years) < market_cap:
            low = growth
        else:
            high = growth
    return flows


def main():
    valuation = REPORTS / 'valuation.html'
    cash = REPORTS / 'cash-capital.html'
    snapshot = {row[0]: row[1:] for row in table_rows(valuation, 'market-snapshot')}
    price = number(snapshot['WDC 收盘'][0])
    shares = number(snapshot['普通股流通数'][0])
    net_cash = number(snapshot['期末净现金'][0])
    ttm = next(row for row in table_rows(cash, 'ttm-cash') if row[0] == '自由现金流')
    baseline = number(ttm[1]) / 1000
    market_cap = price * shares / 1e9
    for label, expected in {
        '估算股权市值': market_cap,
        '近似 EV': market_cap - net_cash,
        '市值 / TTM FCF': market_cap / baseline,
        'TTM FCF 收益率': 100 * baseline / market_cap,
    }.items():
        check(snapshot[label][0], expected, label)

    price_date = date.fromisoformat(snapshot['WDC 收盘'][1][:10])
    year_ends = (date(2027, 7, 2), date(2028, 6, 30), date(2029, 6, 29), date(2030, 6, 28))
    years = [(end - price_date).days / 365.25 for end in year_ends]
    required = reverse(market_cap, baseline, 0.10, 0.025, years)
    path = table_rows(valuation, 'required-path')
    for i, amount in enumerate(required, 1):
        check(path[0][i], amount, 'required FCF')
        check(path[1][i], amount / 0.30, 'required revenue')
    for label, *cells in table_rows(valuation, 'reverse-sensitivity'):
        discount = number(label) / 100
        for cell, growth in zip(cells, (0.02, 0.025, 0.03)):
            flows = reverse(market_cap, baseline, discount, growth, years)
            check(cell, flows[-1], 'reverse sensitivity')

    scenarios = []
    for label, _, revenues, margins, shown_flows, shown_price, shown_return in table_rows(valuation, 'scenario-table'):
        flows = [number(a) * number(b) / 100 for a, b in zip(revenues.split('/'), margins.split('/'))]
        for shown, actual in zip(shown_flows.split('/'), flows):
            check(shown, actual, label)
        model_price = value(flows, 0.10, 0.025, years) * 1e9 / shares
        check(shown_price, model_price, label)
        check(shown_return, 100 * (model_price / price - 1), label)
        scenarios.append(flows)

    base = scenarios[1]
    for i, (label, shown_flows, shown_price, shown_return) in enumerate(table_rows(valuation, 'delay-table')):
        flows = ([base[0]] * i + base)[:4] if i < 3 else base
        for shown, actual in zip(shown_flows.split('/'), flows):
            check(shown, actual, label)
        model_price = value(flows, 0.10, 0.025 if i < 3 else 0.01, years) * 1e9 / shares
        check(shown_price, model_price, label)
        check(shown_return, 100 * (model_price / price - 1), label)

    print(json.dumps({
        'result': 'passed',
        'valuation_html_sha256': sha256(valuation.read_bytes()).hexdigest(),
        'price_date': str(price_date),
        'market_cap_usd_billion': round(market_cap, 2),
        'ttm_fcf_usd_billion': baseline,
        'required_fy2030_fcf_usd_billion': round(required[-1], 2),
    }, indent=2))


if __name__ == '__main__':
    main()
