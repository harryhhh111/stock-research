"""Binance USDT本位永续 aggTrades（成交明细）日归档同步与核对。

来源：data.binance.vision 每日zip（https://data.binance.vision/data/futures/um/daily/aggTrades/），
公开S3，无API权重限制；仍按礼貌节奏串行下载（0.4秒/文件），429/5xx指数退避并尊重Retry-After。
已存在且zip完整性校验通过的日文件直接跳过（缓存使重跑免费）。

口径：aggTrades为官方合并成交（同价同向相近时间合并为一行），比K线trades字段的原始笔数少
约2.5–2.8倍；quantity为币本位成交量，与K线volume同口径。日文件按UTC自然日[00:00,次日00:00)。

产物：
- data/raw/binance-perp/aggtrades/<TOKEN>/<SYM>-aggTrades-<日期>.zip（原始留档，含.request.json记载来源URL与SHA-256）；
- data/normalized/binance-perp/aggtrades/<TOKEN>/<start>-<end>.npz（t_ms int64 / price f64 / qty f64 / maker u8，
  紧凑压缩，可直接numpy载入做秒级分析）及其同名.json清单（校验、逐日来源、与1分钟K线的成交量/笔数比对）。
- 本目录 runs/ 运行摘要；核对结论写入 数字资产/factcheck/<日期>-aggTrades同步.json。

注意：vision也有按月归档（monthly/），范围跨整月时月文件更少请求，但日文件便于断点续传与逐日核对。
"""
import argparse
import datetime as dt
import hashlib
import io
import json
import sys
import time
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import requests

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
VISION = 'https://data.binance.vision/data/futures/um/daily/aggTrades'
MIN_GAP = 0.4          # 两次下载间隔（秒）

WINDOW_END_MS = 1791051300000   # 已归档1分钟K线窗口的结束（北京时间2026-10-04 02:15）


def day_range(start, end):
    d = start
    while d < end:
        yield d
        d += dt.timedelta(days=1)


def fetch(url, target: Path, meta: Path):
    """下载一个日zip；返回(bytes, sha256)。已存在且完整则直接读盘。"""
    if target.exists():
        payload = target.read_bytes()
        try:
            with zipfile.ZipFile(io.BytesIO(payload)) as zf:
                if zf.testzip() is None:
                    return payload, hashlib.sha256(payload).hexdigest()
        except zipfile.BadZipFile:
            pass
        target.unlink()
    attempt = 0
    while True:
        try:
            time.sleep(MIN_GAP)
            resp = requests.get(url, timeout=60)
            if resp.status_code in (429, 500, 502, 503, 504):
                wait = float(resp.headers.get('Retry-After') or 5 * (attempt + 1))
                print(f'⚠️ {resp.status_code}，等待{wait:.0f}秒后重试 {url}', flush=True)
                time.sleep(wait)
                attempt += 1
                if attempt > 5:
                    raise RuntimeError(f'下载重试5次仍失败：{url}')
                continue
            if resp.status_code == 404:
                return None, None
            resp.raise_for_status()
            payload = resp.content
            with zipfile.ZipFile(io.BytesIO(payload)) as zf:
                bad = zf.testzip()
                if bad:
                    raise RuntimeError(f'zip内损坏文件：{bad}')
            tmp = target.with_suffix('.zip.part')
            tmp.write_bytes(payload)
            tmp.rename(target)
            meta.write_text(json.dumps(dict(
                url=url, fetched_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                sha256=hashlib.sha256(payload).hexdigest()), ensure_ascii=False, indent=2) + '\n')
            return payload, hashlib.sha256(payload).hexdigest()
        except (requests.RequestException, zipfile.BadZipFile, RuntimeError) as exc:
            if isinstance(exc, RuntimeError) and '重试' not in str(exc):
                raise
            attempt += 1
            if attempt > 5:
                raise
            time.sleep(3 * attempt)


def parse_day(payload):
    """解析单日zip为numpy数组；校验agg_trade_id递增、时间非降。"""
    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        name = zf.namelist()[0]
        df = pd.read_csv(zf.open(name))
    t = df['transact_time'].to_numpy(dtype=np.int64)
    price = df['price'].to_numpy(dtype=np.float64)
    qty = df['quantity'].to_numpy(dtype=np.float64)
    maker = df['is_buyer_maker'].astype(np.uint8).to_numpy()
    ids = df['agg_trade_id'].to_numpy(dtype=np.int64)
    n = len(t)
    if n:
        if not (np.all(np.diff(ids) > 0) and np.all(np.diff(t) >= 0)):
            raise ValueError('agg_trade_id非递增或时间乱序')
    return t, price, qty, maker, int(ids[0]) if n else None, int(ids[-1]) if n else None, n


def kline_day_sums(token, day_start_ms, day_end_ms):
    """从归档1分钟K线取[day_start,day_end)的volume与trades合计，供逐日比对。"""
    import glob
    files = sorted(glob.glob(str(ROOT / '数字资产' / 'factcheck' / 'data' / 'normalized'
                                 / 'binance-perp' / '1m' / token / '*.json')))
    if not files:
        return None
    doc = json.loads(Path(files[-1]).read_bytes())
    vol = tr = 0.0
    for c in doc['candles']:
        if day_start_ms <= c['open_time_ms'] < day_end_ms:
            vol += c['volume']
            tr += c['trades']
    return vol, tr


def sync_token(token, start, end):
    sym = token + 'USDT'
    rawdir = BASE / 'data' / 'raw' / 'binance-perp' / 'aggtrades' / token
    rawdir.mkdir(parents=True, exist_ok=True)
    parts = {'t_ms': [], 'price': [], 'qty': [], 'maker': []}
    days = []
    missing = []
    for day in day_range(start, end):
        ds = day.isoformat()
        url = f'{VISION}/{sym}/{sym}-aggTrades-{ds}.zip'
        target = rawdir / f'{sym}-aggTrades-{ds}.zip'
        meta = rawdir / f'{sym}-aggTrades-{ds}.request.json'
        payload, sha = fetch(url, target, meta)
        if payload is None:
            missing.append(ds)
            days.append(dict(date=ds, missing=True))
            print(f'{token} {ds}: ⚠️ 404缺档', flush=True)
            continue
        t, price, qty, maker, id0, id1, n = parse_day(payload)
        d0 = int(dt.datetime.combine(day, dt.time.min, tzinfo=dt.timezone.utc).timestamp() * 1000)
        d1 = min(d0 + 86400000, WINDOW_END_MS)
        ks = kline_day_sums(token, d0, d1)
        vol_full = float(qty.sum())
        vol_win = float(qty[t < WINDOW_END_MS].sum())   # 与K线窗口对齐的部分，用于比对
        rec = dict(date=ds, zip_file=str(target.relative_to(BASE)), sha256=sha,
                   n_aggtrades=int(n), qty_sum=vol_full,
                   qty_sum_in_kline_window=vol_win,
                   first_ms=int(t[0]) if n else None, last_ms=int(t[-1]) if n else None,
                   agg_id_first=id0, agg_id_last=id1)
        if ks is not None and ks[1] > 0:
            kvol, ktr = ks
            rec['kline_volume'] = kvol
            rec['kline_trades'] = int(ktr)
            rec['volume_rel_diff'] = (vol_win - kvol) / kvol if kvol else None
            rec['raw_per_agg'] = ktr / n if n else None
        days.append(rec)
        parts['t_ms'].append(t)
        parts['price'].append(price)
        parts['qty'].append(qty)
        parts['maker'].append(maker)
        print(f'{token} {ds}: {n}条 量{vol_full:.1f} 对K线差异'
              f'{rec.get("volume_rel_diff", 0) * 100:.4f}%', flush=True)
    if parts['t_ms']:
        t = np.concatenate(parts['t_ms'])
        assert np.all(np.diff(t) >= 0), '跨日时间乱序'
        outdir = BASE / 'data' / 'normalized' / 'binance-perp' / 'aggtrades' / token
        outdir.mkdir(parents=True, exist_ok=True)
        slug = f'{start.isoformat()}-{end.isoformat()}'
        npz = outdir / f'{slug}.npz'
        np.savez_compressed(npz, t_ms=t, price=np.concatenate(parts['price']),
                            qty=np.concatenate(parts['qty']), maker=np.concatenate(parts['maker']))
        manifest = dict(schema_version=1, token=token, symbol=sym, exchange='Binance',
                        source=f'{VISION}/{sym}/', source_id='binance-perp',
                        market='USD-M perpetual futures', price_type='aggTrades（官方合并成交）',
                        quote_asset='USDT', volume_unit=token,
                        start_utc=start.isoformat() + 'T00:00:00+00:00',
                        end_exclusive_utc=end.isoformat() + 'T00:00:00+00:00',
                        n_records=int(len(t)),
                        note='maker=1表示买方为maker（主动卖）；t_ms为成交时间（毫秒）。'
                             '与K线trades字段的关系：trades计原始笔数，aggTrades约为其1/2.5–1/2.8。'
                             '末日文件（end前一天）覆盖UTC完整自然日，比已归档1分钟K线窗口多含当日18:15–24:00部分。',
                        days=days)
        (outdir / f'{slug}.json').write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
        bad = [d for d in days if not d.get('missing') and d.get('volume_rel_diff') is not None
               and abs(d['volume_rel_diff']) > 0.001]
        status = '✅ 完整' if not missing and not bad else \
            ('⚠️ 有缺档' if missing else '⚠️ 成交量比对异常')
        return dict(token=token, n_records=int(len(t)),
                    first_ms=int(t[0]), last_ms=int(t[-1]),
                    days=len(days), missing_dates=missing,
                    volume_mismatch_dates=[d['date'] for d in bad],
                    npz=str(npz.relative_to(BASE)),
                    status=status, accepted=not missing and not bad)
    return dict(token=token, status='❌ 无数据', accepted=False, missing_dates=missing)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--tokens', nargs='+', required=True, help='币种代码，如BTC HYPE，不带USDT')
    ap.add_argument('--start', required=True, help='UTC开始日期（含），YYYY-MM-DD')
    ap.add_argument('--end', required=True, help='UTC结束日期（不含），YYYY-MM-DD；须不晚于今天')
    args = ap.parse_args(argv)
    start = dt.date.fromisoformat(args.start)
    end = dt.date.fromisoformat(args.end)
    today = dt.datetime.now(dt.timezone.utc).date()
    if end <= start or end > today:
        print('参数错误：结束日期须晚于开始日期且不晚于今天（当日文件未生成完毕）', file=sys.stderr)
        return 2
    reports = []
    for token in list(dict.fromkeys(t.upper() for t in args.tokens)):
        try:
            reports.append(sync_token(token, start, end))
        except Exception as exc:  # noqa: BLE001
            reports.append(dict(token=token, status=f'❌ 同步失败：{exc}', accepted=False))
    summary = dict(created_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                   source=VISION, interval='aggTrades（日归档）',
                   start_utc=start.isoformat(), end_exclusive_utc=end.isoformat(),
                   assets=reports)
    path = BASE / f'{today.isoformat()}-aggTrades同步-{start.isoformat()}-{end.isoformat()}.json'
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(reports, ensure_ascii=False, indent=2))
    return 0 if all(r.get('accepted') for r in reports) else 2


if __name__ == '__main__':
    sys.exit(main())
