"""通用成交K线同步；来源必须显式选定，原始响应按请求哈希缓存。

限流：Binance合约/现货K线 limit=1000 每请求权重10，默认每IP 2400 weight/分钟，
工具按不低于0.30秒/请求的节奏分页（≈2000 weight/分钟，留20%余量），收到429/418
按Retry-After退避（限流等待不消耗三次尝试），响应头X-MBX-USED-WEIGHT-1M超过2000时
等待下一分钟窗口。缓存命中的页不发起请求。
"""
import argparse
import calendar
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
INTERVALS = {k: v*60000 for k,v in {
    '1m':1,'3m':3,'5m':5,'15m':15,'30m':30,'1h':60,'2h':120,
    '4h':240,'8h':480,'12h':720,'1d':1440}.items()}
SOURCES = {
    'binance-perp':('https://fapi.binance.com/fapi/v1/klines','Binance','USD-M perpetual futures','USDT'),
    'binance-spot':('https://api.binance.com/api/v3/klines','Binance','spot','USDT'),
    'hyperliquid-perp':('https://api.hyperliquid.xyz/info','Hyperliquid','native perpetual futures','USD'),
}
# 每来源两次请求的最小间隔（秒）：Binance K线 limit=1000 权重10，0.30秒→约2000 weight/分钟，
# 低于默认上限2400；Hyperliquid单次快照请求，留1秒礼貌间隔。
MIN_INTERVAL={'binance-perp':0.30,'binance-spot':0.30,'hyperliquid-perp':1.0}
_last_call=0.0

def pace(source):
    """按来源限流节奏 sleep，保证两次真实请求间隔不低于MIN_INTERVAL。"""
    global _last_call
    floor=MIN_INTERVAL[source]
    gap=time.monotonic()-_last_call
    if gap<floor:
        time.sleep(floor-gap)
    _last_call=time.monotonic()

def iso(ms):
    return dt.datetime.fromtimestamp(ms/1000,dt.timezone.utc).isoformat()

def parse_time(value):
    parsed=dt.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError('日期必须附时区，例如2026-10-02T00:15:00+08:00')
    return int(parsed.timestamp()*1000)

def subtract_months(ms, months):
    local=dt.datetime.fromtimestamp(ms/1000,dt.timezone(dt.timedelta(hours=8)))
    index=local.year*12+local.month-1-months
    year,month=divmod(index,12)
    month+=1
    return int(local.replace(year=year,month=month,day=min(local.day,calendar.monthrange(year,month)[1])).timestamp()*1000)

def normalize(rows, source, start, end):
    output=[]
    for row in rows:
        if source=='hyperliquid-perp':
            t=int(row['t'])
            item=dict(open_time_ms=t,close_time_ms=int(row['T']),
                      open=float(row['o']),high=float(row['h']),low=float(row['l']),
                      close=float(row['c']),volume=float(row['v']),
                      quote_volume=None,trades=int(row['n']))
        else:
            t=int(row[0])
            item=dict(open_time_ms=t,close_time_ms=int(row[6]),
                      open=float(row[1]),high=float(row[2]),low=float(row[3]),
                      close=float(row[4]),volume=float(row[5]),
                      quote_volume=float(row[7]),trades=int(row[8]))
        if start<=t<end:
            item['open_time_utc']=iso(t)
            output.append(item)
    return sorted(output,key=lambda c:c['open_time_ms'])

def validate(candles,start,end,step):
    times=[c['open_time_ms'] for c in candles]
    missing=sorted(set(range(start,end,step))-set(times))
    duplicates=len(times)-len(set(times))
    invalid=[]
    for c in candles:
        values=[c[k] for k in ['open','high','low','close','volume']]
        if not (all(math.isfinite(v) for v in values)
                and c['low']>0 and c['low']<=min(c['open'],c['close'])
                <=max(c['open'],c['close'])<=c['high']
                and c['volume']>=0 and c['open_time_ms']%step==0
                and c['close_time_ms']==c['open_time_ms']+step-1
                and c['trades']>=0
                and (c['quote_volume'] is None or (math.isfinite(c['quote_volume']) and c['quote_volume']>=0))):
            invalid.append(c['open_time_ms'])
    return dict(count=len(times),expected_count=(end-start)//step,
                missing_count=len(missing),missing_open_times_ms=missing,
                duplicate_count=duplicates,invalid_count=len(invalid),
                invalid_open_times_ms=invalid,
                complete=not(missing or duplicates or invalid))

def request_page(session,url,params,is_hl,source,rawdir):
    descriptor=dict(method='POST' if is_hl else 'GET',url=url,parameters=params)
    key=hashlib.sha256(json.dumps(descriptor,sort_keys=True).encode()).hexdigest()
    target=rawdir/f'{key}.json'
    meta=rawdir/f'{key}.request.json'
    if target.exists():
        payload=target.read_bytes()
    else:
        rate_waits=0
        attempt=0
        while True:
            try:
                pace(source)
                if is_hl:
                    response=session.post(url,json=params,timeout=30)
                else:
                    response=session.get(url,params=params,timeout=30)
                if response.status_code in (418,429):
                    rate_waits+=1
                    if rate_waits>10:
                        raise RuntimeError(f'限流{response.status_code}：退避10次仍被限制，请稍后再跑（缓存使重跑免费）')
                    wait=float(response.headers.get('Retry-After') or 10)+1
                    print(f'⚠️ 限流{response.status_code}，按Retry-After等待{wait:.0f}秒后重试',flush=True)
                    time.sleep(wait)
                    continue
                response.raise_for_status()
                data=response.json()
                if not isinstance(data,list):
                    raise ValueError(f'接口返回错误：{data}')
                payload=response.content
                descriptor['fetched_at_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
                target.write_bytes(payload)
                meta.write_text(json.dumps(descriptor,ensure_ascii=False,indent=2)+'\n')
                used=response.headers.get('X-MBX-USED-WEIGHT-1M')
                if used is not None and float(used)>2000:
                    print('⚠️ 本分钟权重用量超过2000，等待下一分钟窗口',flush=True)
                    time.sleep(62)
                break
            except (requests.RequestException,ValueError):
                if attempt==2:
                    raise
                attempt+=1
                time.sleep(attempt+1)
    data=json.loads(payload)
    if not isinstance(data,list):
        raise ValueError('原始缓存不是K线数组')
    return data,dict(file=str(target.relative_to(BASE)),
                     request_file=str(meta.relative_to(BASE)),
                     sha256=hashlib.sha256(payload).hexdigest())

def sync_token(token,source,interval,start,end,step,allow_partial):
    url,exchange,market,quote=SOURCES[source]
    is_hl=source=='hyperliquid-perp'
    symbol=token if is_hl else token+'USDT'
    rawdir=BASE/'data'/'raw'/source/interval/token
    rawdir.mkdir(parents=True,exist_ok=True)
    cursor=start
    rows=[]
    sources=[]
    with requests.Session() as session:
        while cursor<end:
            params=(dict(type='candleSnapshot',req=dict(coin=token,interval=interval,startTime=cursor,endTime=end-1))
                    if is_hl else dict(symbol=symbol,interval=interval,startTime=cursor,endTime=end-1,
                                       limit=1000))
            data,origin=request_page(session,url,params,is_hl,source,rawdir)
            sources.append(origin)
            rows.extend(data)
            if not data or is_hl:
                break
            next_cursor=max(int(row[0]) for row in data)+step
            if next_cursor<=cursor:
                raise ValueError('分页游标未前进')
            cursor=next_cursor
            print(f'{source} {token}: {len(rows)}根',flush=True)
    candles=normalize(rows,source,start,end)
    check=validate(candles,start,end,step)
    slug=f'{start}-{end}'
    outdir=BASE/'data'/'normalized'/source/interval/token
    outdir.mkdir(parents=True,exist_ok=True)
    output=outdir/f'{slug}.json'
    doc=dict(schema_version=1,token=token,symbol=symbol,exchange=exchange,source=url,
             source_id=source,market=market,price_type='trade OHLC',quote_asset=quote,
             volume_unit=token,interval=interval,start_utc=iso(start),end_exclusive_utc=iso(end),
             validation=check,raw_sources=sources,candles=candles)
    if is_hl:
        doc['note']='仅原生永续；价格单位USD，保证金机制另行区分。quote_volume接口未提供，留null。'
    output.write_text(json.dumps(doc,ensure_ascii=False,separators=(',',':'))+'\n')
    report=dict(token=token,source=source,output=str(output.relative_to(BASE)),**check)
    if candles:
        report.update(first_open_utc=candles[0]['open_time_utc'],
                      last_open_utc=candles[-1]['open_time_utc'],
                      first_open_price=candles[0]['open'],last_close_price=candles[-1]['close'])
        if check['complete']:
            report['period_return']=candles[-1]['close']/candles[0]['open']-1
    report['status']='✅ 完整' if check['complete'] else '⚠️ 不完整；无插值，无自动换源'
    report['accepted']=check['complete'] or (allow_partial and not(check['duplicate_count'] or check['invalid_count']))
    return report

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--tokens',nargs='+',required=True,help='币种代码，如HYPE BTC ETH，不带USDT')
    ap.add_argument('--source',choices=SOURCES,required=True)
    ap.add_argument('--interval',choices=INTERVALS,default='5m')
    window=ap.add_mutually_exclusive_group(required=True)
    window.add_argument('--start',help='附时区ISO日期')
    window.add_argument('--months',type=int,help='向前自然月数量，以北京时间计算')
    ap.add_argument('--end',help='附时区ISO日期；默认最近已完成K线边界')
    ap.add_argument('--allow-partial',action='store_true',help='显式接受有缺口数据')
    args=ap.parse_args(argv)
    try:
        step=INTERVALS[args.interval]
        now=int(time.time()*1000)
        end=parse_time(args.end) if args.end else now//step*step
        if args.months is not None and args.months<=0:
            raise ValueError('months必须为正数')
        start=parse_time(args.start) if args.start else subtract_months(end,args.months)
        if start%step or end%step or end<=start or end>now//step*step:
            raise ValueError('时间必须对齐UTC K线边界且仅覆盖已完成K线')
        tokens=list(dict.fromkeys(t.upper() for t in args.tokens))
        if any(not re.fullmatch(r'[A-Z0-9]+',t) for t in tokens):
            raise ValueError('本版仅支持普通币种代码；HIP-3与Hyperliquid现货需要额外映射')
        if args.source=='hyperliquid-perp' and start < (now//step-4999)*step and not args.allow_partial:
            raise ValueError('Hyperliquid仅保留最近5000根（含当前未完成一根）；所选开始时间过早。缩短区间或显式--allow-partial，不会自动换源。')
        reports=[]
        for token in tokens:
            try:
                reports.append(sync_token(token,args.source,args.interval,start,end,step,args.allow_partial))
            except (requests.RequestException,ValueError,KeyError,TypeError,RuntimeError) as exc:
                reports.append(dict(token=token,source=args.source,status='❌ 同步失败',accepted=False,error=str(exc)))
        summary=dict(created_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                     source=args.source,interval=args.interval,start_utc=iso(start),
                     end_exclusive_utc=iso(end),assets=reports)
        directory=BASE/'runs'
        directory.mkdir(parents=True,exist_ok=True)
        suffix='-'.join(tokens)
        path=directory/f'{args.source}-{args.interval}-{start}-{end}-{suffix}.json'
        path.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps([{k:v for k,v in r.items() if k not in ['missing_open_times_ms','invalid_open_times_ms']} for r in reports],ensure_ascii=False,indent=2))
        return 0 if all(r['accepted'] for r in reports) else 2
    except ValueError as exc:
        print(f'参数错误：{exc}',file=sys.stderr)
        return 2

if __name__=='__main__':
    sys.exit(main())
