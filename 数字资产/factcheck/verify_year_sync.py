"""核对2026-10-04的HYPE/BTC一年5分钟快照，并比较旧三个月快照。"""
import hashlib
import json
from pathlib import Path
from sync_prices import parse_time,validate,iso

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[1]
START=parse_time('2025-10-04T02:15:00+08:00')
END=parse_time('2026-10-04T02:15:00+08:00')

def main():
    result={'start_utc':iso(START),'end_exclusive_utc':iso(END),'interval':'5m','source':'binance-perp','assets':[]}
    all_times=[]
    for token in ['HYPE','BTC']:
        path=BASE/'data'/'normalized'/'binance-perp'/'5m'/token/f'{START}-{END}.json'
        payload=path.read_bytes();doc=json.loads(payload)
        candles=doc['candles']
        check=validate(candles,START,END,300000)
        assert check['complete'],f'{token}年度数据不完整'
        assert check['count']==105120
        for source in doc['raw_sources']:
            raw=(BASE/source['file']).read_bytes()
            assert hashlib.sha256(raw).hexdigest()==source['sha256']
        old_path=ROOT/'HYPE'/'factcheck'/'data'/f'2026-10-02-0015-{token}USDT-5m.json'
        old=json.loads(old_path.read_text())['candles']
        indexed={c['open_time_ms']:c for c in candles}
        for c in old:
            new=indexed[c['open_time_ms']]
            assert all(c[key]==new[key] for key in ['open','high','low','close','volume','quote_volume','trades']),f'{token}旧数据不一致'
        all_times.append([c['open_time_ms'] for c in candles])
        result['assets'].append(dict(token=token,path=str(path.relative_to(BASE)),sha256=hashlib.sha256(payload).hexdigest(),
                                     count=len(candles),raw_pages=len(doc['raw_sources']),overlap_count=len(old),
                                     overlap_ohlcv_trades_match=True,missing_count=check['missing_count'],
                                     duplicate_count=check['duplicate_count'],invalid_count=check['invalid_count'],
                                     first_open_utc=candles[0]['open_time_utc'],last_open_utc=candles[-1]['open_time_utc'],
                                     first_open_price=candles[0]['open'],last_close_price=candles[-1]['close']))
    assert all_times[0]==all_times[1]
    result['both_tokens_exactly_aligned']=True
    result['status']='✅ 年度连续性、原始文件哈希、双币时间对齐及旧快照重叠一致性通过'
    out=BASE/'2026-10-04-一年5分钟K线核对.json'
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
