"""Check annual and interim group revenue coverage in the delivered HTML."""

import argparse
from dataclasses import dataclass, field
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re


TABLE_IDS = ('annual-revenue', 'quarter-revenue')
GROUP_LABEL = re.compile(r'集团(?:持续经营)?(?:收入|营收)?')
AMOUNT = re.compile(r'^(?:[$¥€£]\s*)?[+−-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?=\s|$|[（(/])')


@dataclass
class RevenueTable:
    id: str
    rows: list[list[str]] = field(default_factory=list)


class RevenueTables(HTMLParser):
    def __init__(self, section_id):
        super().__init__()
        self.section_id = section_id
        self.scope = None
        self.scope_depth = 0
        self.pending = None
        self.table = None
        self.table_depth = 0
        self.row = None
        self.cell = None
        self.tables = []

    def handle_starttag(self, tag, attrs):
        element_id = dict(attrs).get('id')
        if self.scope is None:
            if element_id == self.section_id and tag in ('section', 'article', 'div', 'main'):
                self.scope, self.scope_depth = tag, 1
            return
        if tag == self.scope:
            self.scope_depth += 1
        if tag == 'table':
            if self.table_depth == 0:
                table_id = element_id if element_id in TABLE_IDS else self.pending
                self.table = RevenueTable(table_id) if table_id else None
                self.pending = None
            self.table_depth += 1
        elif self.table_depth == 0 and tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.pending = element_id if element_id in TABLE_IDS else None
        elif self.table is not None and self.table_depth == 1:
            if tag == 'tr':
                self.row = []
            elif tag in ('th', 'td') and self.row is not None:
                self.cell = []
            elif tag in ('br', 'small', 'p', 'div') and self.cell is not None:
                self.cell.append(' ')

    def handle_data(self, data):
        if self.cell is not None and self.table_depth == 1:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if self.scope is None:
            return
        if tag == self.scope:
            self.scope_depth -= 1
            if self.scope_depth == 0:
                self.scope, self.pending = None, None
        if tag == 'table' and self.table_depth:
            self.table_depth -= 1
            if self.table_depth == 0 and self.table is not None:
                self.tables.append(self.table)
                self.table, self.row, self.cell = None, None, None
        elif self.table is not None and self.table_depth == 1:
            if tag in ('th', 'td') and self.cell is not None:
                self.row.append(' '.join(''.join(self.cell).split()))
                self.cell = None
            elif tag == 'tr' and self.row is not None:
                if self.row:
                    self.table.rows.append(self.row)
                self.row = None


def period_key(header):
    return re.sub(r'\s+', '', header.upper()).removeprefix('FY')


def inspect_table(table, expected):
    if not table.rows:
        return [], ['表格没有数据行']
    headers = [period_key(cell) for cell in table.rows[0][1:]]
    errors = []
    if not all(re.fullmatch(r'\d{4}(?:Q[1-4]|H[1-2])?', header) for header in headers):
        errors.append('期间列须使用明确的财年、单季或半年标签')
    period_type = expected[0][4:5]
    if any(header[4:5] != period_type for header in headers):
        errors.append('年度、单季及半年须分表')
    if headers != sorted(set(headers)):
        errors.append('期间列须按时间升序且不得重复')
    group_rows = [row for row in table.rows[1:] if GROUP_LABEL.fullmatch(row[0])]
    if len(group_rows) != 1 or len(group_rows[0]) != len(headers) + 1:
        return [], errors + ['须有一行与期间列逐项对应的集团营收金额']
    group_values = group_rows[0][1:]
    actual = [period for period, cell in zip(headers, group_values) if AMOUNT.match(cell)]
    missing = [period for period in expected if period not in actual]
    if missing:
        errors.append(f'缺少集团营收金额或期间：{", ".join(missing)}')
    return actual, errors


def check_html(html, section_id, annual, interim):
    reader = RevenueTables(section_id)
    reader.feed(html)
    reader.close()
    errors, actual = [], {}
    if [table.id for table in reader.tables] == list(reversed(TABLE_IDS)):
        errors.append('年度营收表须位于单季/半年营收表之前')
    for table_id, expected in zip(TABLE_IDS, (annual, interim)):
        matches = [table for table in reader.tables if table.id == table_id]
        if len(matches) != 1:
            actual[table_id] = []
            errors.append(f'{table_id}：须有且仅有一张营收底表；预期期间 {", ".join(expected)}')
            continue
        actual[table_id], issues = inspect_table(matches[0], expected)
        errors.extend(f'{table_id}：{issue}' for issue in issues)
    return actual, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html', type=Path)
    parser.add_argument('--latest-annual', type=int, required=True, help='最新已披露的完整财年，例如 2025')
    parser.add_argument('--latest-period', required=True, help='最新已披露单季或半年，如 2026Q3 或 2026H1')
    parser.add_argument('--annual-count', type=int, default=3)
    parser.add_argument('--section-id', default='revenue')
    args = parser.parse_args()
    match = re.fullmatch(r'(\d{4})(?:Q([1-4])|H([1-2]))', period_key(args.latest_period))
    if not match or args.annual_count < 3:
        parser.error('最新期间使用 YYYYQ1–Q4 或 YYYYH1–H2，至少核对三个完整财年')
    year, quarter, half = match.groups()
    if args.latest_annual not in (int(year), int(year) - 1):
        parser.error('最新完整财年须与最新期间处于同一财年或前一财年')
    annual = [str(y) for y in range(args.latest_annual - args.annual_count + 1, args.latest_annual + 1)]
    if quarter:
        latest_quarter = int(year) * 4 + int(quarter) - 1
        interim = [f'{index // 4:04d}Q{index % 4 + 1}'
                   for index in range(latest_quarter - 3, latest_quarter + 1)]
    else:
        interim = [f'{year}H{i}' for i in range(1, int(half) + 1)]
    try:
        raw = args.html.read_bytes()
        actual, errors = check_html(raw.decode('utf-8'), args.section_id, annual, interim)
    except (OSError, UnicodeError) as exc:
        parser.exit(1, f'无法读取报告：{exc}\n')
    print(json.dumps({
        'report': str(args.html),
        'sha256': hashlib.sha256(raw).hexdigest(),
        'expected': dict(zip(TABLE_IDS, (annual, interim))),
        'actual': actual,
        'errors': errors,
    }, ensure_ascii=False, indent=2))
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
