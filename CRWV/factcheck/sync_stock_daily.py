"""同步美股日 K 线（Polygon.io 免费档）→ CRWV/factcheck/data/。

用法：
  1. 到 https://polygon.io 注册免费账号拿 API key（免费档：5 次/分钟、15 分钟延迟、日线历史 2 年）
  2. 在工作区根目录 .env 写入：POLYGON_API_KEY=你的key（.env 已在 .gitignore）
  3. python3 sync_stock_daily.py

产出（原始数据保留不修改，可重复运行覆盖同名文件）：
  data/{运行日}-{TICKER}-1d.csv
  字段：t_ms,open,high,low,close,volume,vwap,n_trades（Polygon 原字段标准化，t_ms 为 UTC 毫秒）

范围（用户拍板 2026-10-21）：最近一年日线。免费档是否含 1h  aggregates 待 key 实测，
如可用可把 INTERVAL 改回 1/hour、文件名后缀改回 -1h（engine 与 bar 粒度无关）。
"""
import csv
import json
import os
import subprocess
import sys
import time
import datetime as dt
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / 'data'
ROOT = BASE.parents[1]                     # 工作区根目录（CRWV/factcheck → 根）
TICKERS = ('NBIS', 'CRWV', 'QQQ')          # QQQ 作相对基准
FROM_DATE = '2025-10-21'                   # 一年窗口起点
INTERVAL = 'day'                           # 免费档日线确定可用；1h 待实测
LIMIT = 50000                              # 单次请求上限（一年日线 ≈ 250 根，远够用）


def load_key():
    k = os.environ.get('POLYGON_API_KEY')
    if k and k.strip():
        return k.strip()
    env = ROOT / '.env'
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith('POLYGON_API_KEY='):
                v = line.split('=', 1)[1].strip()
                if v:
                    return v
    sys.exit('缺少 POLYGON_API_KEY：注册 https://polygon.io 免费 key 后写入根目录 .env'
             '（一行 POLYGON_API_KEY=你的key），或在环境变量中提供。')


def fetch_bars(ticker, key):
    to_date = dt.date.today().isoformat()
    url = (f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/{INTERVAL}'
           f'/{FROM_DATE}/{to_date}?adjusted=true&sort=asc&limit={LIMIT}&apiKey={key}')
    last_err = None
    for attempt in range(3):
        try:
            # 本机网络对交易所类 API 走 TLS 拦截代理，urllib 校验失败；curl 走系统配置可用
            r = subprocess.run(['curl', '-s', '--max-time', '30', url],
                               capture_output=True, text=True)
            doc = json.loads(r.stdout)
            status = doc.get('status')
            if status in ('OK', 'DELAYED'):     # 免费档返回 DELAYED（15分钟延迟），同为成功
                return doc.get('results') or []
            if status == 'NOT_FOUND':
                return []
            raise RuntimeError(f'{ticker}: status={status} message={doc.get("error") or doc.get("message")}')
        except Exception as e:
            last_err = e
            if attempt == 2:
                raise
            print(f'  {ticker} 第{attempt + 1}次失败（{e}），2s 后重试')
            time.sleep(2)
    return []


def main():
    key = load_key()
    DATA.mkdir(exist_ok=True)
    stamp = dt.date.today().isoformat()
    suffix = '1d' if INTERVAL == 'day' else '1h'
    for t in TICKERS:
        rows = fetch_bars(t, key)
        if not rows:
            print(f'{t}: 无数据（检查代码与免费档权限）')
            continue
        out = DATA / f'{stamp}-{t.lower()}-{suffix}.csv'
        with out.open('w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['t_ms', 'open', 'high', 'low', 'close', 'volume', 'vwap', 'n_trades'])
            for b in rows:
                w.writerow([b['t'], b['o'], b['h'], b['l'], b['c'], b['v'], b.get('vw', ''), b.get('n', '')])
        first = dt.datetime.fromtimestamp(rows[0]['t'] / 1000, dt.timezone.utc)
        last = dt.datetime.fromtimestamp(rows[-1]['t'] / 1000, dt.timezone.utc)
        print(f'{t}: {len(rows)} bars, {first:%Y-%m-%d} ~ {last:%Y-%m-%d} UTC → {out.name}')
        time.sleep(13)                     # 免费档 5 次/分钟，留重试余量


if __name__ == '__main__':
    main()
