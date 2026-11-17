#!/usr/bin/env python3
"""Local conditional valuation; Python standard library only. No network access."""
import argparse
from calendar import isleap
from datetime import date
from html import escape
import hashlib
import json
import math
from pathlib import Path
import sys
from string import Template

VERSION = '0.1.0'
BASE = Path(__file__).resolve().parent.parent
FACT_FIELDS = ('price', 'net_profit', 'current_shares')
STATUSES = {'user_input': '用户输入·原数未核实', 'verified': '提供者标记已核验·本程序不核验原数', 'synthetic': '纯示意·非公司实绩'}


class InputError(ValueError):
    pass


def number(value, name, positive=False):
    try:
        finite = not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value)
    except OverflowError:
        finite = False
    if not finite:
        raise InputError(f'{name} 必须为有限数值')
    if positive and value <= 0:
        raise InputError(f'{name} 必须大于0；亏损或零利润不适用本模型')
    return float(value)


def text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise InputError(f'{name} 必须填写非空文字')
    return value.strip()


def as_date(value, name):
    try:
        s = text(value, name)
        d = date.fromisoformat(s)
        if d.isoformat() != s:
            raise ValueError()
        return d
    except (ValueError, TypeError):
        raise InputError(f'{name} 必须为有效YYYY-MM-DD日期') from None


def anniversary(start, year):
    day = 28 if start.month == 2 and start.day == 29 and not isleap(year) else start.day
    return start.replace(year=year, day=day)


def years_between(start, end):
    """Whole calendar anniversaries plus fraction of the next anniversary year."""
    if end <= start:
        raise InputError('目标日期必须晚于价格基准日和利润基期末')
    whole = end.year - start.year
    if anniversary(start, start.year + whole) > end:
        whole -= 1
    left = anniversary(start, start.year + whole)
    # Exact anniversaries do not need a potentially out-of-range year + 1.
    if left == end:
        return float(whole)
    right = anniversary(start, start.year + whole + 1)
    return whole + (end - left).days / (right - left).days


def validate(data):
    if not isinstance(data, dict):
        raise InputError('输入必须为JSON对象')
    required = {'schema_version', 'company', 'share_basis', 'currency', 'price', 'net_profit',
                'profit_unit', 'profit_period_start', 'profit_period_end', 'profit_basis',
                'price_date', 'current_shares', 'target_shares', 'target_fiscal_year',
                'target_date', 'required_return', 'target_pe', 'sensitivity_pe',
                'assumptions_confirmed', 'applicability', 'evidence'}
    if missing := required - data.keys():
        raise InputError('缺少字段：' + ', '.join(sorted(missing)))
    if unknown := data.keys() - required:
        raise InputError('未知字段：' + ', '.join(sorted(unknown)))
    if type(data['schema_version']) is not int or data['schema_version'] != 1:
        raise InputError('schema_version 必须为整数1')
    for key in ('company', 'share_basis', 'profit_basis', 'target_fiscal_year'):
        text(data[key], key)
    if data['currency'] not in ('USD', 'CNY', 'HKD', 'EUR', 'JPY', 'GBP', 'TWD', 'KRW', 'CAD', 'AUD'):
        raise InputError('currency 不支持；须显式统一币种，程序不换汇')
    if data['profit_unit'] not in ('unit', 'M', 'B'):
        raise InputError('profit_unit 只能为unit、M或B；M=100万，B=10亿')
    for key in ('price', 'net_profit', 'current_shares', 'target_shares', 'target_pe'):
        number(data[key], key, positive=True)
    r = number(data['required_return'], 'required_return')
    if r <= -1:
        raise InputError('required_return 必须大于-1；0.10表示10%')
    if data['assumptions_confirmed'] is not True:
        raise InputError('请先由用户确认回报率、PE、目标年份、同单位股数及模型假设')
    a = data['applicability']
    if not isinstance(a, dict) or set(a) != {'comparable_profit', 'major_capital_changes', 'special_industry'}:
        raise InputError('applicability 须包含可比利润、重大资本结构变化及特殊行业判断')
    if any(type(v) is not bool for v in a.values()):
        raise InputError('applicability 各项必须为布尔值')
    if not a['comparable_profit'] or a['major_capital_changes'] or a['special_industry']:
        raise InputError('本模型不适用：利润不可比、重大资本结构变化或特殊行业，请使用专门模型')
    pdate = as_date(data['price_date'], 'price_date')
    pstart = as_date(data['profit_period_start'], 'profit_period_start')
    pend = as_date(data['profit_period_end'], 'profit_period_end')
    target = as_date(data['target_date'], 'target_date')
    if not 350 <= (pend - pstart).days + 1 <= 380:
        raise InputError('净利润基期须为一个完整年度（本版支持350—380天含首尾）；不接受单季/半年年化')
    if pend > pdate:
        raise InputError('利润基期末不得晚于价格基准日')
    years_between(pdate, target)
    years_between(pend, target)
    # Delayed comparisons must both be representable.
    if target.year > 9997:
        raise InputError('目标日期过远，无法生成延迟两年的日期')
    pe = data['sensitivity_pe']
    if not isinstance(pe, list) or not 1 <= len(pe) <= 7:
        raise InputError('sensitivity_pe 需为1—7个由用户确认的PE数值')
    for v in pe:
        number(v, 'sensitivity_pe', positive=True)
    if len(set(pe)) != len(pe) or data['target_pe'] not in pe:
        raise InputError('敏感性PE不可重复，且必须包含目标PE')
    ev = data['evidence']
    if not isinstance(ev, dict) or set(ev) != set(FACT_FIELDS):
        raise InputError('evidence 必须逐项给price、net_profit、current_shares来源')
    for key in FACT_FIELDS:
        e = ev[key]
        if not isinstance(e, dict) or set(e) != {'source', 'status', 'source_date', 'currency'}:
            raise InputError(f'evidence.{key} 字段须为source/status/source_date/currency')
        text(e['source'], f'{key}.source')
        if not isinstance(e['status'], str) or e['status'] not in STATUSES:
            raise InputError(f'{key}.status 无效')
        source_date = as_date(e['source_date'], f'{key}.source_date')
        if source_date > pdate:
            raise InputError(f'{key} 来源在价格基准日之后，不能用未来资料解释历史价格')
        if key == 'net_profit' and source_date < pend:
            raise InputError('net_profit来源日期不得早于完整利润基期末')
        if key == 'price' and source_date != pdate:
            raise InputError('价格来源日期必须与价格基准日一致')
        expected = 'shares' if key == 'current_shares' else data['currency']
        if e['currency'] != expected:
            raise InputError(f'{key} 币种/量纲不一致；股数填shares，金额须与currency一致')
    return data


def scenario(data, target, pe):
    pdate = as_date(data['price_date'], 'price_date')
    pend = as_date(data['profit_period_end'], 'profit_period_end')
    n = years_between(pdate, target)
    growth_n = years_between(pend, target)
    factor = {'unit': 1., 'M': 1e6, 'B': 1e9}[data['profit_unit']]
    try:
        future_price = data['price'] * (1 + data['required_return']) ** n
        profit = future_price * data['target_shares'] / pe / factor
        if profit <= 0 or not math.isfinite(profit):
            raise ArithmeticError()
        ratio = profit / data['net_profit']
        growth = math.expm1(math.log(ratio) / growth_n)
        result = {'target_date': target.isoformat(), 'target_pe': pe,
                  'return_years': n, 'profit_growth_years': growth_n,
                  'required_price': future_price, 'required_profit': profit,
                  'profit_multiple': ratio, 'profit_cagr': growth,
                  'price_present_value': future_price / (1 + data['required_return']) ** n}
        if not all(math.isfinite(v) for v in result.values() if isinstance(v, (float, int))):
            raise ArithmeticError()
        return result
    except (OverflowError, ArithmeticError, ValueError):
        raise InputError('参数导致数值溢出或精度不可用，请缩小假设范围') from None


def calculate(data):
    validate(data)
    target = as_date(data['target_date'], 'target_date')
    dates = [anniversary(target, target.year + delay) for delay in range(3)]
    rows = [scenario(data, d, data['target_pe']) for d in dates]
    matrix = [{'pe': pe, 'scenarios': [scenario(data, d, pe) for d in dates]}
              for pe in sorted(data['sensitivity_pe'])]
    digest = hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True,
                                       allow_nan=False).encode()).hexdigest()
    warnings = ['仅为给定假设的条件反推，不是市场共识、目标价建议或完整DCF。',
                '期间现金分红未建模；回购/增发仅通过目标股数假设反映。',
                '延迟情景固定PE、回报率与目标股数，未预测费用、投入及竞争变化。',
                '本程序只验证输入结构与计算，不验证来源原数；核验标签由输入提供者声明。']
    if data['profit_period_end'] != data['price_date']:
        warnings.append('价格日与利润基期末不同：回报年数与利润增长年数分开计算。')
    if (as_date(data['price_date'], 'price_date') - as_date(data['profit_period_end'], 'profit_period_end')).days > 550:
        warnings.append('利润基期较旧（距价格日超过550天），可能无法代表当前经营；请确认仍适用。')
    return {'model_version': VERSION, 'input_sha256': digest, 'input': data,
            'synthetic': any(e['status'] == 'synthetic' for e in data['evidence'].values()),
            'base': rows[0], 'delays': rows, 'sensitivity': matrix, 'limitations': warnings,
            'calculation_check': '公式计算完成；不代表公司事实或研究质量验收通过'}


def fmt(x, digits=2):
    return f'{x:,.{digits}f}'


def render(result):
    d = result['input']
    b = result['base']
    e = lambda x: escape(str(x), quote=True)
    money_unit = f"{d['profit_unit']} {d['currency']}" if d['profit_unit'] != 'unit' else d['currency']
    year_labels = [e(x['target_date']) for x in result['delays']]
    paths = ''.join(f'<tr><th scope="row">{["原定", "延迟一年", "延迟两年"][i]}</th>'
                    f'<td>{e(x["target_date"])}</td><td>{fmt(x["return_years"], 3)} / {fmt(x["profit_growth_years"], 3)}</td>'
                    f'<td>{fmt(x["required_price"])}</td><td>{fmt(x["required_profit"])}</td>'
                    f'<td>{x["profit_cagr"]:.2%}</td></tr>' for i, x in enumerate(result['delays']))
    sensitivity = ''.join(f'<tr><th scope="row">{fmt(row["pe"], 1)}×</th>' + ''.join(
        f'<td><strong>{fmt(x["required_profit"])}</strong><small>利润 CAGR {x["profit_cagr"]:.2%}</small></td>'
        for x in row['scenarios']) + '</tr>' for row in result['sensitivity'])
    input_rows = [
        ('价格基准', f"{d['price_date']} · {fmt(d['price'])} {d['currency']} / 证券单位"),
        ('证券单位', d['share_basis']),
        ('利润期间', f"{d['profit_period_start']} 至 {d['profit_period_end']}"),
        ('利润基数与口径', f"{fmt(d['net_profit'])} {money_unit} · {d['profit_basis']}"),
        ('当前 / 目标股数', f"{fmt(d['current_shares'], 0)} / {fmt(d['target_shares'], 0)} 证券单位 · 目标数为假设"),
        ('目标财年 / 期末', f"{d['target_fiscal_year']} / {d['target_date']}"),
        ('确认的假设', f"必要年化回报率 {d['required_return']:.2%} · 目标PE {fmt(d['target_pe'],1)}× · 敏感性PE {', '.join(str(v) for v in d['sensitivity_pe'])}"),
    ]
    inputs = ''.join(f'<tr><th scope="row">{e(k)}</th><td>{e(v)}</td></tr>' for k, v in input_rows)
    facts = ''.join(f'<tr><th scope="row">{e({"price":"价格","net_profit":"利润","current_shares":"当前股数"}[k])}</th>'
                    f'<td>{e(v["source"])}</td><td>{e(v["source_date"])}</td>'
                    f'<td>{e(STATUSES[v["status"]])}</td></tr>' for k, v in d['evidence'].items())
    limits = ''.join(f'<li>{e(v)}</li>' for v in result['limitations'])
    badge = '纯示意数据 · 非公司实绩' if result['synthetic'] else '条件反推 · 来源状态见表'
    return Template((BASE / 'assets' / 'report.html').read_text()).substitute(
        company=e(d['company']), badge=e(badge), date=e(d['price_date']),
        target=e(d['target_fiscal_year']), target_date=e(d['target_date']),
        profit=fmt(b['required_profit']), unit=e(money_unit), growth=f'{b["profit_cagr"]:.2%}',
        multiple=f'{b["profit_multiple"]:.2f}', years=fmt(b['return_years'], 3),
        growth_years=fmt(b['profit_growth_years'], 3), pe=fmt(d['target_pe'], 1),
        rate=f'{d["required_return"]:.2%}', price=fmt(d['price']), currency=e(d['currency']),
        paths=paths, sensitivity=sensitivity, year0=year_labels[0], year1=year_labels[1], year2=year_labels[2],
        inputs=inputs, evidence=facts, limits=limits, version=VERSION, sha=e(result['input_sha256']))


def reject_constant(value):
    raise InputError(f'JSON不允许NaN/Infinity：{value}')


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise InputError(f'JSON字段重复：{key}')
        obj[key] = value
    return obj


def main(argv=None):
    p = argparse.ArgumentParser(description='从已确认输入反推未来利润，输出离线HTML及同源JSON；无联网取数。')
    p.add_argument('--input', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path, help='新建.html报告；不会覆盖已有文件')
    args = p.parse_args(argv)
    output = args.output
    json_path = output.with_suffix('.json')
    try:
        if output.suffix.lower() != '.html':
            raise InputError('output必须是.html文件')
        if output.exists() or json_path.exists():
            raise InputError('输出已存在；请使用新文件名保留历史版本')
        raw = json.loads(args.input.read_text(encoding='utf-8'), parse_constant=reject_constant,
                         object_pairs_hook=unique_object)
        result = calculate(raw)
        html = render(result)
        payload = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
        output.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation protects both existing reports and the input file.
        with json_path.open('x', encoding='utf-8') as f:
            f.write(payload)
        try:
            with output.open('x', encoding='utf-8') as f:
                f.write(html)
        except OSError:
            json_path.unlink()  # Only this invocation's newly-created sidecar.
            raise
        print(json.dumps({'html': str(output.resolve()), 'json': str(json_path.resolve()),
                          'model_version': VERSION, 'synthetic': result['synthetic']}, ensure_ascii=False))
        return 0
    except (InputError, OSError, json.JSONDecodeError, TypeError, KeyError) as exc:
        print(f'无法生成报告：{exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
