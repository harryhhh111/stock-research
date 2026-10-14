"""重算BTC/HYPE收益相关、回归与事件时间线。numpy；默认只读原始数据。"""
import datetime as dt
import hashlib
import json
from pathlib import Path
import numpy as np

BASE=Path(__file__).resolve().parent
TZ=dt.timezone(dt.timedelta(hours=8))
STEP=300000

def ms(value):
    return int(dt.datetime.fromisoformat(value).timestamp()*1000)

def stamp(t):
    return dt.datetime.fromtimestamp(int(t)/1000,TZ).isoformat()

def regression(x,y):
    if len(x)<10:
        return dict(n=len(x),correlation=None,beta=None,intercept=None,r_squared=None,note='少于10个收益样本，不报告不稳定系数')
    beta=float(np.cov(x,y,ddof=1)[0,1]/np.var(x,ddof=1))
    corr=float(np.corrcoef(x,y)[0,1])
    return dict(n=len(x),correlation=corr,beta=beta,intercept=float(np.mean(y)-beta*np.mean(x)),r_squared=corr*corr)

def lag_curve(x,y):
    result=[]
    for k in range(-72,73):
        xx=x[:-k] if k>0 else x[-k:] if k<0 else x
        yy=y[k:] if k>0 else y[:k] if k<0 else y
        result.append(dict(lag_minutes=k*5,correlation=float(np.corrcoef(xx,yy)[0,1]),n=len(xx)))
    return result

def aggregate_returns(candles,start,end,period):
    groups={}
    for c in candles:
        t=c['open_time_ms']
        if start<=t<end:
            groups.setdefault(t//period,[]).append(c)
    closes=[]
    expected=period//STEP
    for key,rows in sorted(groups.items()):
        if len(rows)==expected and rows[0]['open_time_ms']==key*period and rows[-1]['open_time_ms']==(key+1)*period-STEP:
            closes.append(rows[-1]['close'])
    return np.diff(np.log(closes))

def main():
    data={}; origins=[]
    for token in ['BTC','HYPE']:
        p=BASE/'data'/f'2026-10-02-0015-{token}USDT-5m.json'
        raw=p.read_bytes();doc=json.loads(raw)
        data[token]=doc['candles']
        origins.append(dict(token=token,file=str(p.relative_to(BASE)),sha256=hashlib.sha256(raw).hexdigest(),source=doc['source'],market=doc['market']))
    times=np.array([c['open_time_ms'] for c in data['BTC']],dtype=np.int64)
    assert np.array_equal(times,[c['open_time_ms'] for c in data['HYPE']])
    assert np.all(np.diff(times)==STEP)
    close=np.array([[c['close'] for c in data[token]] for token in ['BTC','HYPE']])
    returns=np.diff(np.log(close),axis=1)
    event_start=ms('2026-08-19T00:00:00+08:00');event_end=ms('2026-08-22T00:00:00+08:00')
    extended_start=ms('2026-08-17T00:00:00+08:00');extended_end=ms('2026-08-29T00:00:00+08:00')
    windows=dict(full=(int(times[0]),int(times[-1]+STEP)),event=(event_start,event_end),extended=(extended_start,extended_end),pre_event=(int(times[0]),event_start),post_event=(event_end,int(times[-1]+STEP)))
    statistics={}
    for name,(start,end) in windows.items():
        mask=(times[1:]>=start)&(times[1:]<end)
        rr=returns[:,mask]
        item=dict(start_bj=stamp(start),end_exclusive_bj=stamp(end),metrics={'5m':regression(*rr)})
        for label,period in [('1h',3600000),('1d',86400000)]:
            x,y=[aggregate_returns(data[token],start,end,period) for token in ['BTC','HYPE']]
            item['metrics'][label]=regression(x,y)
        curve=lag_curve(*rr)
        item['lag_curve_5m']=curve
        item['best_lag']=max(curve,key=lambda x:x['correlation'])
        item['best_positive_lag']=max((v for v in curve if v['lag_minutes']>0),key=lambda x:x['correlation'])
        statistics[name]=item
    # 日线统计按北京时间日界线；UTC日线相关另见上面的1d。
    daily=[]
    for day in range(12):
        start=extended_start+day*86400000;end=start+86400000
        row=dict(day=stamp(start)[:10])
        for token in ['BTC','HYPE']:
            cc=[c for c in data[token] if start<=c['open_time_ms']<end]
            row[token]=dict(open=cc[0]['open'],close=cc[-1]['close'],return_pct=(cc[-1]['close']/cc[0]['open']-1)*100)
        mask=(times[1:]>=start)&(times[1:]<end)
        curve=lag_curve(*returns[:,mask])
        row['same_time_correlation']=regression(*returns[:,mask])['correlation']
        row['best_lag']=max(curve,key=lambda x:x['correlation'])
        daily.append(row)
    event={}
    for token in ['BTC','HYPE']:
        cc=[c for c in data[token] if event_start<=c['open_time_ms']<event_end]
        initial=cc[0]['open']
        hits=[]
        for percent in [2,3,5,10,15,20]:
            hit=next((c for c in cc if c['close']/initial-1>=percent/100),None)
            if hit:
                hits.append(dict(threshold_pct=percent,first_close_bj=stamp(hit['open_time_ms']+STEP),close=hit['close']))
        maxbar=max(cc,key=lambda c:c['close']/c['open']-1)
        maxhigh=max(cc,key=lambda c:c['high'])
        event[token]=dict(start_price=initial,end_close=cc[-1]['close'],return_pct=(cc[-1]['close']/initial-1)*100,
                          thresholds=hits,max_5m_bar=dict(close_time_bj=stamp(maxbar['open_time_ms']+STEP),open=maxbar['open'],close=maxbar['close'],return_pct=(maxbar['close']/maxbar['open']-1)*100),
                          peak_high=dict(value=maxhigh['high'],bar_start_bj=stamp(maxhigh['open_time_ms'])),
                          peak_close_bj=stamp(max(cc,key=lambda c:c['close'])['open_time_ms']+STEP))
    # 共同参考节点的价格：用该时刻刚完成的5分钟收盘价。
    checkpoints=[]
    for value in ['2026-08-19T00:00:00+08:00','2026-08-19T23:00:00+08:00','2026-08-19T23:30:00+08:00','2026-08-20T00:35:00+08:00','2026-08-20T03:15:00+08:00','2026-08-20T03:20:00+08:00','2026-08-20T06:00:00+08:00','2026-08-21T00:00:00+08:00','2026-08-22T00:00:00+08:00']:
        end=ms(value);row={'time_bj':value}
        for token in ['BTC','HYPE']:
            c=next(c for c in data[token] if c['open_time_ms']==end-STEP)
            price=event[token]['start_price'] if end==event_start else c['close']
            row[token]=dict(close=price,from_event_start_pct=(price/event[token]['start_price']-1)*100)
        checkpoints.append(row)
    pre=statistics['pre_event']['metrics']['5m']
    btc_log=np.log(event['BTC']['end_close']/event['BTC']['start_price'])
    hype_log=np.log(event['HYPE']['end_close']/event['HYPE']['start_price'])
    comparison=dict(beta_from_pre_event=pre['beta'],zero_alpha_beta_scaled_btc_return_pct=float(np.expm1(pre['beta']*btc_log)*100),
                    observed_hype_return_pct=event['HYPE']['return_pct'],excess_log_return_pct=float((hype_log-pre['beta']*btc_log)*100),
                    note='仅用事前样本beta构造零截距比较，非因果归因，非可实现交易收益。')
    result=dict(data_cutoff_bj=stamp(times[-1]+STEP),source_files=origins,return_definition='log(close_t/close_t-1)',
                positive_lag_definition='corr(BTC_t,HYPE_t+k)，正k指BTC在先',statistics=statistics,
                event=event,daily=daily,checkpoints=checkpoints,pre_beta_comparison=comparison)
    p=BASE/'2026-10-02-BTC-HYPE相关与事件分析.json'
    p.write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['statistics','source_files']},ensure_ascii=False,indent=2))
    for name,item in statistics.items():
        print(name,json.dumps(item['metrics'],ensure_ascii=False), 'best',item['best_lag'],'bestpositive',item['best_positive_lag'])

if __name__=='__main__':
    main()
