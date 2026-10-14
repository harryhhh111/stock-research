"""资金费率同步（Binance USDT本位永续 fundingRate）；原始响应按请求哈希缓存。

限流：fundingRate 单次请求权重低（limit≤1000），仍按不低于0.30秒/请求的节奏分页
（与 sync_prices.py 同一余量标准），收到429/418按Retry-After退避。缓存命中的页
不发起请求。

口径：每次资金费事件一条记录 {fundingTime, fundingRate, markPrice}。
注意 Binance 部分币种资金费间隔会调整（如 HYPE 经历过 4h 与 8h 并存），
校验只报告事实：事件数、间隔分布、最大缺口，不推断缺失原因。
已知案例：HYPE 2026-06-24 12:00(北京) 事件缺记录，复核原接口仍不返回，
见 HYPE/factcheck/2026-10-05-funding跨距核对.json。
"""
import argparse
import datetime as dt
import hashlib
import json
import math
import re
import sys
import time
from pathlib import Path

import requests

BASE = Path(__file__).resolve().parent
URL = 'https://fapi.binance.com/fapi/v1/fundingRate'
MIN_INTERVAL = 0.30
_last_call = 0.0


def pace():
    global _last_call
    gap = time.monotonic() - _last_call
    if gap < MIN_INTERVAL:
        time.sleep(MIN_INTERVAL - gap)
    _last_call = time.monotonic()


def iso(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).isoformat()


def parse_time(value):
    parsed = dt.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError('日期必须附时区，例如2026-10-02T00:15:00+08:00')
    return int(parsed.timestamp() * 1000)


def request_page(session, symbol, start, end, rawdir):
    params = dict(symbol=symbol, startTime=start, endTime=end - 1, limit=1000)
    descriptor = dict(method='GET', url=URL, parameters=params)
    key = hashlib.sha256(json.dumps(descriptor, sort_keys=True).encode()).hexdigest()
    target = rawdir / f'{key}.json'
    meta = rawdir / f'{key}.request.json'
    if target.exists():
        payload = target.read_bytes()
    else:
        rate_waits = 0
        attempt = 0
        while True:
            try:
                pace()
                response = session.get(URL, params=params, timeout=30)
                if response.status_code in (418, 429):
                    rate_waits += 1
                    if rate_waits > 10:
                        raise RuntimeError(f'限流{response.status_code}：退避10次仍被限制，请稍后再跑（缓存使重跑免费）')
                    wait = float(response.headers.get('Retry-After') or 10) + 1
                    print(f'⚠️ 限流{response.status_code}，按Retry-After等待{wait:.0f}秒后重试', flush=True)
                    time.sleep(wait)
                    continue
                response.raise_for_status()
                data = response.json()
                if not isinstance(data, list):
                    raise ValueError(f'接口返回错误：{data}')
                payload = response.content
                descriptor['fetched_at_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
                target.write_bytes(payload)
                meta.write_text(json.dumps(descriptor, ensure_ascii=False, indent=2) + '\n')
                used = response.headers.get('X-MBX-USED-WEIGHT-1M')
                if used is not None and float(used) > 2000:
                    print('⚠️ 本分钟权重用量超过2000，等待下一分钟窗口', flush=True)
                    time.sleep(62)
                break
            except (requests.RequestException, ValueError):
                if attempt == 2:
                    raise
                attempt += 1
                time.sleep(attempt + 1)
    data = json.loads(payload)
    if not isinstance(data, list):
        raise ValueError('原始缓存不是资金费数组')
    return data, dict(file=str(target.relative_to(BASE)),
                      request_file=str(meta.relative_to(BASE)),
                      sha256=hashlib.sha256(payload).hexdigest())


def normalize(rows, start, end):
    events = []
    for row in rows:
        t = int(row['fundingTime'])
        if start <= t < end:
            item = dict(funding_time_ms=t, funding_time_utc=iso(t),
                        funding_rate=float(row['fundingRate']))
            if row.get('markPrice') is not None:
                item['mark_price'] = float(row['markPrice'])
            events.append(item)
    events.sort(key=lambda e: e['funding_time_ms'])
    return events


def validate(events):
    times = [e['funding_time_ms'] for e in events]
    duplicates = len(times) - len(set(times))
    invalid = [e['funding_time_ms'] for e in events
               if not (math.isfinite(e['funding_rate']) and abs(e['funding_rate']) < 0.05
                       and ('mark_price' not in e or (math.isfinite(e['mark_price']) and e['mark_price'] > 0)))]
    gaps = sorted(set(b - a for a, b in zip(times, times[1:])))
    gap_hist = {}
    for g in gaps:
        gap_hist[f'{g / 3600000:.4g}'] = gap_hist.get(f'{g / 3600000:.4g}', 0) + 1
    interval_hist = dict(sorted(((float(h), c) for h, c in gap_hist.items()), key=lambda x: x[1], reverse=True))
    max_gap_hours = (times[-1] - times[0]) / 3600000 / max(1, len(times) - 1) if len(times) > 1 else None
    true_max_gap = max((b - a for a, b in zip(times, times[1:])), default=0) / 3600000
    return dict(count=len(times), duplicate_count=duplicates, invalid_count=len(invalid),
                invalid_times_ms=invalid, gap_hours_histogram={h: c for h, c in interval_hist.items()},
                max_gap_hours=true_max_gap,
                complete=not (duplicates or invalid or true_max_gap > 8.0001))


def sync_token(token, start, end):
    symbol = token + 'USDT'
    rawdir = BASE / 'data' / 'raw' / 'binance-perp' / 'funding' / token
    rawdir.mkdir(parents=True, exist_ok=True)
    cursor = start
    rows = []
    sources = []
    with requests.Session() as session:
        while cursor < end:
            data, origin = request_page(session, symbol, cursor, end, rawdir)
            sources.append(origin)
            rows.extend(data)
            if not data or len(data) < 1000:
                break
            next_cursor = max(int(row['fundingTime']) for row in data) + 1
            if next_cursor <= cursor:
                raise ValueError('分页游标未前进')
            cursor = next_cursor
            print(f'{token}: {len(rows)}条', flush=True)
    events = normalize(rows, start, end)
    check = validate(events)
    slug = f'{start}-{end}'
    outdir = BASE / 'data' / 'normalized' / 'binance-perp' / 'funding' / token
    outdir.mkdir(parents=True, exist_ok=True)
    output = outdir / f'{slug}.json'
    doc = dict(schema_version=1, token=token, symbol=symbol, exchange='Binance',
               source=URL, market='USD-M perpetual futures',
               start_utc=iso(start), end_exclusive_utc=iso(end),
               validation=check, raw_sources=sources, events=events,
               note='资金费间隔以交易所安排为准，可能随时间调整（见 gap_hours_histogram）；'
                    '正费率=多头付空头。')
    output.write_text(json.dumps(doc, ensure_ascii=False, separators=(',', ':')) + '\n')
    report = dict(token=token, output=str(output.relative_to(BASE)), **check)
    if events:
        report.update(first_time_utc=events[0]['funding_time_utc'],
                      last_time_utc=events[-1]['funding_time_utc'],
                      mean_rate=float(np_mean([e['funding_rate'] for e in events])))
    report['status'] = '✅ 完整' if check['complete'] else '⚠️ 存在重复/非法/超8小时缺口'
    report['accepted'] = check['complete']
    return report


def np_mean(xs):
    return sum(xs) / len(xs)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--tokens', nargs='+', required=True, help='币种代码，如BTC HYPE ETH SOL，不带USDT')
    window = ap.add_mutually_exclusive_group(required=True)
    window.add_argument('--start', help='附时区ISO日期')
    window.add_argument('--start-ms', type=int, help='毫秒时间戳')
    ap.add_argument('--end', help='附时区ISO日期；默认与全年1分钟K线窗口对齐')
    args = ap.parse_args(argv)
    try:
        if args.start_ms is not None:
            start = args.start_ms
        else:
            start = parse_time(args.start)
        end = parse_time(args.end) if args.end else 1791051300000
        if end <= start:
            raise ValueError('end必须大于start')
        tokens = list(dict.fromkeys(t.upper() for t in args.tokens))
        if any(not re.fullmatch(r'[A-Z0-9]+', t) for t in tokens):
            raise ValueError('本版仅支持普通币种代码')
        reports = []
        for token in tokens:
            try:
                reports.append(sync_token(token, start, end))
            except (requests.RequestException, ValueError, KeyError, TypeError, RuntimeError) as exc:
                reports.append(dict(token=token, status='❌ 同步失败', accepted=False, error=str(exc)))
        summary = dict(created_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                       source=URL, start_utc=iso(start), end_exclusive_utc=iso(end), assets=reports)
        directory = BASE / 'runs'
        directory.mkdir(parents=True, exist_ok=True)
        suffix = '-'.join(tokens)
        path = directory / f'funding-{start}-{end}-{suffix}.json'
        path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps([{k: v for k, v in r.items() if k != 'invalid_times_ms'} for r in reports],
                         ensure_ascii=False, indent=2))
        return 0 if all(r['accepted'] for r in reports) else 2
    except ValueError as exc:
        print(f'参数错误：{exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
