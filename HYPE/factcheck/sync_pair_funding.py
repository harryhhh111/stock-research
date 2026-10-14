"""获取与年度K线同区间的Binance真实历史资金费率，原始响应留档。"""
import datetime as dt
import hashlib
import json
import time
from pathlib import Path
import requests

BASE=Path(__file__).resolve().parent
START=1759515300000
END=1791051300000
URL='https://fapi.binance.com/fapi/v1/fundingRate'

def main():
    for token in ['BTC','HYPE']:
        rawdir=BASE/'data'/'pair-funding-raw'/token
        rawdir.mkdir(parents=True,exist_ok=True)
        rows=[];origins=[];cursor=START
        with requests.Session() as session:
            while cursor<END:
                params=dict(symbol=token+'USDT',startTime=cursor,endTime=END-1,limit=1000)
                key=hashlib.sha256(json.dumps(params,sort_keys=True).encode()).hexdigest()
                file=rawdir/f'{key}.json'
                if file.exists():
                    payload=file.read_bytes()
                else:
                    for attempt in range(3):
                        try:
                            response=session.get(URL,params=params,timeout=30)
                            response.raise_for_status()
                            data=response.json()
                            if not isinstance(data,list):raise ValueError(str(data))
                            payload=response.content
                            file.write_bytes(payload)
                            (rawdir/f'{key}.request.json').write_text(json.dumps(dict(url=URL,params=params,fetched_at_utc=dt.datetime.now(dt.timezone.utc).isoformat()),indent=2)+'\n')
                            break
                        except (requests.RequestException,ValueError):
                            if attempt==2:raise
                            time.sleep(attempt+1)
                data=json.loads(payload)
                origins.append(dict(file=str(file.relative_to(BASE)),sha256=hashlib.sha256(payload).hexdigest(),params=params))
                if not data:break
                rows+=data
                next_cursor=max(int(r['fundingTime']) for r in data)+1
                if next_cursor<=cursor:raise ValueError('cursor did not advance')
                cursor=next_cursor
                print(token,len(rows),'funding events',flush=True)
                time.sleep(.2)
        rows=sorted((r for r in rows if START<=int(r['fundingTime'])<END),key=lambda r:int(r['fundingTime']))
        stamps=[int(r['fundingTime']) for r in rows]
        assert len(stamps)==len(set(stamps)) and rows
        assert all(r['symbol']==token+'USDT' and float(r['markPrice'])>0 for r in rows)
        gaps=[b-a for a,b in zip(stamps,stamps[1:])]
        coverage=dict(count=len(rows),first_time_ms=stamps[0],last_time_ms=stamps[-1],max_gap_hours=max(gaps)/3600000,
                      start_to_first_hours=(stamps[0]-START)/3600000,last_to_end_hours=(END-stamps[-1])/3600000,
                      interval_hours_observed=sorted(set(round(g/3600000,4) for g in gaps)))
        out=BASE/'data'/f'2026-10-05-{token}-funding-year.json'
        out.write_text(json.dumps(dict(token=token,source=URL,market='Binance USD-M perpetual',start_ms=START,end_exclusive_ms=END,coverage=coverage,raw_sources=origins,events=rows),ensure_ascii=False,indent=2)+'\n')
        print(json.dumps(coverage))

if __name__=='__main__':main()
