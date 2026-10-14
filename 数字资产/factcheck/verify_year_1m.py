"""核对1分钟年度快照的完整性，并聚合到5分钟与已归档5分钟快照逐根核对。"""
import datetime as dt
import hashlib
import json
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent
START, END = 1759515300000, 1791051300000          # 与5分钟年度快照同窗口（北京 2025-10-04 02:15 → 2026-10-04 02:15）
MIN_MS, FIVE_MS = 60000, 300000
EXPECTED = (END - START) // MIN_MS                  # 525,600根/币


def load(token, interval):
    p = BASE / 'data' / 'normalized' / 'binance-perp' / interval / token / f'{START}-{END}.json'
    raw = p.read_bytes()
    doc = json.loads(raw)
    return doc, hashlib.sha256(raw).hexdigest(), p


def main():
    result = dict(start_utc='2025-10-03T18:15:00+00:00', end_exclusive_utc='2026-10-03T18:15:00+00:00',
                  interval='1m', source='binance-perp', assets=[])
    for token in ['HYPE', 'BTC']:
        doc, sha, path = load(token, '1m')
        candles = doc['candles']
        t = np.array([c['open_time_ms'] for c in candles], dtype=np.int64)
        assert len(candles) == EXPECTED, f'{token} 根数 {len(candles)} != {EXPECTED}'
        assert np.all(np.diff(t) == MIN_MS), f'{token} 时间轴不连续'
        assert t[0] == START and t[-1] == END - MIN_MS
        # 聚合到5分钟：open首/high max/low min/close末/volume、quote_volume、trades求和
        idx = (t - START) // FIVE_MS
        assert len(idx) % 5 == 0
        g = idx.reshape(-1, 5)                       # 每根5分钟K线含5根1分钟K线
        assert np.all(g[:, 0] == g[:, -1]), '5分钟分组错位'
        def col(name):
            return np.array([c[name] for c in candles], dtype=float).reshape(-1, 5)
        agg = dict(open_time_ms=(START + g[:, 0] * FIVE_MS).tolist(),
                   open=col('open')[:, 0].tolist(), high=col('high').max(axis=1).tolist(),
                   low=col('low').min(axis=1).tolist(), close=col('close')[:, -1].tolist(),
                   volume=col('volume').sum(axis=1).tolist(), quote_volume=col('quote_volume').sum(axis=1).tolist(),
                   trades=col('trades').sum(axis=1).tolist())
        ref_doc, ref_sha, _ = load(token, '5m')
        ref = ref_doc['candles']
        assert len(ref) == len(agg['open'])
        max_dev = dict(volume=0.0, quote_volume=0.0)
        mismatch = 0
        for i, rc in enumerate(ref):
            assert agg['open_time_ms'][i] == rc['open_time_ms'], f'{token} 第{i}根时间戳错位'
            for f in ['open', 'high', 'low', 'close']:
                if agg[f][i] != rc[f]:
                    mismatch += 1
            assert agg['trades'][i] == rc['trades'], f'{token} 第{i}根成交笔数不符'
            for f in ['volume', 'quote_volume']:
                denom = abs(rc[f]) if rc[f] else 1.0
                dev = abs(agg[f][i] - rc[f]) / denom
                max_dev[f] = max(max_dev[f], dev)
                assert dev < 1e-9, f'{token} 第{i}根{f}偏差{dev}'
        assert mismatch == 0, f'{token} 有{mismatch}个OHLC与5分钟快照不符'
        result['assets'].append(dict(token=token, path=str(path.relative_to(BASE)), sha256=sha,
                                     count=len(candles), raw_pages=len(doc['raw_sources']),
                                     five_mismatch_ohlc=0, five_max_rel_dev=max_dev,
                                     five_ref_sha256=ref_sha, five_cointegrity='✅ 1分钟完整、与5分钟年度快照逐根一致'))
    out = BASE / '2026-10-05-一年1分钟K线核对.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
