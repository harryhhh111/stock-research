"""Compare CFO, cash CapEx, FCF and a cash bridge with HTML report tables."""

import argparse
from dataclasses import dataclass, field
from decimal import Decimal
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re


METRICS = ('cfo', 'cash_capex', 'fcf')
BRIDGE_ROLES = {'opening', 'cfo', 'investing', 'financing', 'fx', 'other', 'closing'}
REQUIRED_ROLES = BRIDGE_ROLES - {'fx', 'other'}
NUMBER = re.compile(r'[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?')


@dataclass
class Table:
    id: str | None
    heading: str
    rows: list[list[str]] = field(default_factory=list)


class Tables(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tables = []
        self.heading = ''
        self.heading_parts = None
        self.table = None
        self.depth = 0
        self.row = None
        self.cell = None
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            if self.depth == 0:
                self.table = Table(dict(attrs).get('id'), self.heading)
            self.depth += 1
        elif self.depth == 0 and tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.heading_parts = []
        elif self.depth == 1:
            if tag == 'tr':
                self.row = []
            elif tag in ('th', 'td') and self.row is not None:
                self.cell = []

    def handle_endtag(self, tag):
        if tag == 'table' and self.depth:
            self.depth -= 1
            if self.depth == 0:
                if self.table.rows:
                    self.tables.append(self.table)
                self.table = self.row = self.cell = None
        elif self.heading_parts is not None and tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.heading = self.clean(self.heading_parts)
            self.heading_parts = None
        elif self.depth == 1:
            if tag in ('th', 'td') and self.cell is not None:
                self.row.append(self.clean(self.cell))
                self.cell = None
            elif tag == 'tr' and self.row is not None:
                if self.row:
                    self.table.rows.append(self.row)
                self.row = None

    def handle_data(self, data):
        if self.depth == 1 and self.cell is not None:
            self.cell.append(data)
        elif self.heading_parts is not None:
            self.heading_parts.append(data)

    @staticmethod
    def clean(parts):
        return ' '.join(''.join(parts).split())

    def find(self, selector):
        if 'id' in selector:
            matches = [table for table in self.tables if table.id == selector['id']]
        else:
            prefix = selector.get('header_prefix', [])
            matches = [table for table in self.tables if table.heading == selector['heading']
                       and table.rows[0][:len(prefix)] == prefix]
        if len(matches) != 1:
            raise ValueError(f'应匹配一张表，实际匹配 {len(matches)} 张：{selector}')
        return matches[0].rows


def source_amount(value):
    if isinstance(value, bool) or not isinstance(value, (int, str, Decimal)):
        raise ValueError('来源金额须为数值')
    try:
        result = Decimal(value)
    except ArithmeticError as exc:
        raise ValueError(f'无效来源金额：{value}') from exc
    if not result.is_finite():
        raise ValueError(f'来源金额须为有限值：{value}')
    return result


def displayed_amount(rows, label, label_column, value_column):
    matches = [row for row in rows[1:] if len(row) > label_column and row[label_column] == label]
    if len(matches) != 1 or len(matches[0]) <= value_column:
        raise ValueError(f'找不到唯一金额单元格：{label}')
    cell = matches[0][value_column].replace('−', '-')
    if cell.startswith('(') and cell.endswith(')'):
        cell = '-' + cell[1:-1]
    if not NUMBER.fullmatch(cell):
        raise ValueError(f'{label} 的单元格须为金额，实际为 {cell!r}')
    amount = Decimal(cell.replace(',', ''))
    return amount, Decimal('0.5').scaleb(amount.as_tuple().exponent)


def period_key(text):
    return re.sub(r'\s+', '', text.upper()).removeprefix('FY')


def compare(errors, location, actual, expected, tolerance):
    difference = actual - expected
    if abs(difference) > tolerance:
        errors.append(f'{location}：报告 {actual}，预期 {expected}，差额 {difference}（舍入限 {tolerance}）')


def check_periods(tables, spec, periods, errors):
    rows = tables.find(spec['table'])
    headers = [period_key(cell) for cell in rows[0][1:]]
    data = spec['values']
    labels = spec['rows']
    results = {}
    for period in periods:
        before = len(errors)
        if headers.count(period) != 1:
            errors.append(f'{period}：CFO/现金 CapEx/FCF 缺列或期间重复')
            continue
        if period not in data:
            errors.append(f'{period}：缺独立来源金额')
            continue
        column = headers.index(period) + 1
        amounts, roundings = {}, {}
        expected = {}
        for metric in METRICS:
            location = f'{period} {labels[metric]}'
            try:
                amounts[metric], roundings[metric] = displayed_amount(rows, labels[metric], 0, column)
                expected[metric] = source_amount(data[period][metric])
                compare(errors, location, amounts[metric], expected[metric], roundings[metric])
            except (KeyError, ValueError) as exc:
                errors.append(f'{location}：{exc}')
        if len(amounts) == len(METRICS):
            if amounts['cash_capex'] < 0 or expected.get('cash_capex', 0) < 0:
                errors.append(f'{period}：现金 CapEx 须以支出为正列示')
            compare(errors, f'{period} FCF=CFO−现金 CapEx', amounts['fcf'],
                    amounts['cfo'] - amounts['cash_capex'], sum(roundings.values()))
        if len(errors) == before:
            results[period] = amounts
    return results


def check_bridge(tables, spec, period_results, errors):
    rows = tables.find(spec['table'])
    totals = {}
    cells = set()
    tolerance = Decimal(0)
    before = len(errors)
    for entry in spec['items']:
        label, role = entry['label'], entry['role']
        label_column = entry.get('label_column', 0)
        sign = entry.get('sign', 1)
        location = f'{spec["period"]} 现金桥 {label}'
        if role not in BRIDGE_ROLES or (label_column, label) in cells or (
                role in ('opening', 'closing') and role in totals):
            errors.append(f'{location}：角色无效或项目重复')
            continue
        if type(label_column) is not int or label_column < 0 or type(sign) is not int or sign not in (-1, 1):
            errors.append(f'{location}：列位置或符号无效')
            continue
        cells.add((label_column, label))
        try:
            amount, rounding = displayed_amount(rows, label, label_column, label_column + 1)
            signed = amount * sign
            compare(errors, location, signed, source_amount(entry['expected']), rounding)
            totals[role] = totals.get(role, Decimal(0)) + signed
            tolerance += rounding
        except (KeyError, ValueError) as exc:
            errors.append(f'{location}：{exc}')
    required = set(spec.get('required_roles', [])) | REQUIRED_ROLES
    missing = required - totals.keys()
    if missing:
        errors.append(f'{spec["period"]} 现金桥缺少：{", ".join(sorted(missing))}')
    if len(errors) == before:
        compare(errors, f'{spec["period"]} 期初加净变动等于期末', totals['closing'],
                sum(value for role, value in totals.items() if role != 'closing'), tolerance)
        same_period = period_results.get(period_key(spec['period']))
        if same_period is not None:
            compare(errors, f'{spec["period"]} 现金桥与底表 CFO', totals['cfo'], same_period['cfo'], tolerance)
    return totals


def audit(html, inputs):
    year = int(inputs['latest_annual'])
    years = int(inputs.get('annual_count', 3))
    latest = re.fullmatch(r'(\d{4})(?:Q([1-4])|H([1-2]))', period_key(inputs['latest_period']))
    if not latest or not 3 <= years <= 10 or year not in (int(latest[1]), int(latest[1]) - 1):
        raise ValueError('须提供不少于三年且与最新已披露季度/半年匹配的年度范围')
    interim_year, quarter, half = latest.groups()
    annual = [str(value) for value in range(year - years + 1, year + 1)]
    if quarter:
        latest_quarter = int(interim_year) * 4 + int(quarter) - 1
        interim = [f'{index // 4:04d}Q{index % 4 + 1}'
                   for index in range(latest_quarter - 3, latest_quarter + 1)]
    else:
        interim = [f'{interim_year}H{i}' for i in range(1, int(half) + 1)]
    tables = Tables(html)
    errors, results = [], {}
    for key, periods in (('annual', annual), ('interim', interim)):
        spec = inputs[key]
        if spec['capex_basis'] != 'cash_paid':
            errors.append(f'{key}：CapEx 必须来自实际现金付款，不得使用资产新增或未付款承诺')
        if not spec['source'].strip():
            errors.append(f'{key}：缺少披露来源定位')
        try:
            results.update(check_periods(tables, spec, periods, errors))
        except ValueError as exc:
            errors.append(f'{key}：{exc}')
    bridge = inputs['bridge']
    if not all(bridge[key].strip() for key in ('source', 'cash_scope', 'period')):
        errors.append('现金桥须标明来源、期间及现金范围')
    try:
        totals = check_bridge(tables, bridge, results, errors)
    except ValueError as exc:
        totals = {}
        errors.append(f'{bridge["period"]} 现金桥：{exc}')
    return {'expected_periods': annual + interim, 'verified_periods': list(results),
            'bridge_period': bridge['period'], 'bridge_totals': totals, 'errors': errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report', type=Path)
    parser.add_argument('--input', type=Path, required=True, help='按原始披露准备的核验输入 JSON')
    args = parser.parse_args()
    try:
        report = args.report.read_bytes()
        source = args.input.read_bytes()
        inputs = json.loads(source, parse_float=Decimal)
        if not all(inputs[key].strip() for key in ('entity', 'unit')):
            raise ValueError('须注明主体与统一单位')
        result = audit(report.decode(), inputs)
        result.update(entity=inputs['entity'], unit=inputs['unit'])
    except (OSError, UnicodeError, KeyError, TypeError, AttributeError, ValueError) as exc:
        parser.exit(1, f'现金流核验输入错误：{exc}\n')
    result.update(report_sha256=hashlib.sha256(report).hexdigest(), input_sha256=hashlib.sha256(source).hexdigest())
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return int(bool(result['errors']))


if __name__ == '__main__':
    raise SystemExit(main())
