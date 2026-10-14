"""BTC/HYPE配对研究：收益beta、协整、冻结模型的滚动样本外回测。"""
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels
from statsmodels.tsa.stattools import adfuller,coint
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[1]
TZ=dt.timezone(dt.timedelta(hours=8))
STEP=300000
INITIAL=100000.0

def bj(t):return dt.datetime.fromtimestamp(int(t)/1000,TZ).isoformat()

def fit(x,y):
    beta=float(np.cov(x,y,ddof=1)[0,1]/np.var(x,ddof=1))
    alpha=float(np.mean(y)-beta*np.mean(x))
    residual=y-alpha-beta*x
    return alpha,beta,residual

def coint_test(y,x,maxlag=24):
    stat,p,crit=coint(y,x,trend='c',maxlag=maxlag,autolag='aic')
    return dict(statistic=float(stat),pvalue=float(p),critical_5pct=float(crit[1]),maxlag=maxlag,autolag='aic',trend='c')

def adf(z):
    stat,p,lag,n,*_=adfuller(z,maxlag=24,autolag='AIC',regression='c',result_object=False)
    return dict(statistic=float(stat),pvalue=float(p),chosen_lag=int(lag),n=int(n))

def load():
    docs=[];origins=[];funding=[]
    for token in ['BTC','HYPE']:
        p=ROOT/'数字资产'/'factcheck'/'data'/'normalized'/'binance-perp'/'5m'/token/'1759515300000-1791051300000.json'
        raw=p.read_bytes();doc=json.loads(raw);docs.append(doc['candles'])
        origins.append(dict(token=token,file=str(p.relative_to(ROOT)),sha256=hashlib.sha256(raw).hexdigest()))
        p=BASE/'data'/f'2026-10-05-{token}-funding-year.json'
        raw=p.read_bytes();doc=json.loads(raw)
        assert doc['coverage']['max_gap_hours']<8.001
        assert doc['coverage']['start_to_first_hours']<8.001 and doc['coverage']['last_to_end_hours']<8.001
        funding.append(doc)
        origins.append(dict(token=token,type='funding',file=str(p.relative_to(ROOT)),sha256=hashlib.sha256(raw).hexdigest()))
    t=np.array([c['open_time_ms'] for c in docs[0]],dtype=np.int64)
    assert np.array_equal(t,[c['open_time_ms'] for c in docs[1]]) and np.all(np.diff(t)==STEP)
    opens=np.array([[c['open'] for c in rows] for rows in docs]).T
    closes=np.array([[c['close'] for c in rows] for rows in docs]).T
    groups={}
    for k,stamp in enumerate(t):groups.setdefault(int(stamp//3600000),[]).append(k)
    hour_indices=np.array([idx[-1] for _,idx in sorted(groups.items()) if len(idx)==12],dtype=int)
    hour_t=t[hour_indices]+STEP
    return t,opens,closes,hour_t,closes[hour_indices],funding,origins

def models(hour_t,prices,lookback=1440):
    logs=np.log(prices)
    output=[]
    for start in range(lookback,len(logs),168):
        end=min(start+168,len(logs))
        xx,yy=logs[start-lookback:start].T
        alpha,beta,res=fit(xx,yy)
        test=coint_test(yy,xx,12)
        delta=np.diff(res)
        _,phi,_=fit(res[:-1],delta)
        rho=1+phi
        half=-np.log(2)/np.log(rho) if 0<rho<1 else None
        ra,rb,_=fit(np.diff(xx),np.diff(yy))
        output.append(dict(id=len(output),train_start_bj=bj(hour_t[start-lookback]),train_end_bj=bj(hour_t[start-1]),
                           test_start_bj=bj(hour_t[start]),test_end_bj=bj(hour_t[end-1]),
                           start=start,end=end,alpha=alpha,beta=beta,return_beta=rb,
                           mean=float(np.mean(res)),sigma=float(np.std(res,ddof=1)),
                           coint=test,ar1_half_life_hours=float(half) if half is not None else None,
                           eligible=bool(test['pvalue']<.05 and beta>0)))
    return output

def backtest(t,opens,closes,hour_t,hour_prices,funding,folds,cost_bps=6,gated=True,sizing_mode='price_beta'):
    """5分钟逐根计价；整点收盘信号，整点+5分钟开盘模拟执行。"""
    signal_map={}
    for model in folds:
        for j in range(model['start'],model['end']):
            z=(np.log(hour_prices[j,1])-model['alpha']-model['beta']*np.log(hour_prices[j,0])-model['mean'])/model['sigma']
            signal_map[int(hour_t[j])]=(model,float(z),j==model['end']-1)
    fund_map={}
    for leg,doc in enumerate(funding):
        for event in doc['events']:
            stamp=int(event['fundingTime'])
            k=int(np.searchsorted(t,stamp,side='right')-1)
            if 0<=k<len(t) and t[k]<=stamp<t[k]+STEP:
                fund_map.setdefault(k,[]).append((leg,float(event['fundingRate']),float(event['markPrice'])))
    qty=np.zeros(2);equity=INITIAL;pending=None;active=None;trades=[];curve=[]
    total_price=total_funding=total_cost=0.0
    exposed=0;test_bars=0
    first_signal=int(hour_t[folds[0]['start']])
    for k in range(len(t)):
        # 持仓跨K线开收盘的小跳动也计入现金PnL。
        if k>0:
            pnl=float(np.dot(qty,opens[k]-closes[k-1]))
            equity+=pnl;total_price+=pnl
            if active:active['price_pnl']+=pnl
        if pending and int(t[k])>=pending['execute_ms']:
            if pending['action']=='close' and active:
                fee=float(np.sum(np.abs(qty)*opens[k]))*cost_bps/10000
                equity-=fee;total_cost+=fee;active['cost']+=fee
                active.update(exit_bj=bj(t[k]),exit_ms=int(t[k]),exit_prices=opens[k].tolist(),reason=pending['reason'],exit_z=pending['z'],
                              holding_hours=(int(t[k])-active['entry_ms'])/3600000,
                              net_pnl=active['price_pnl']+active['funding_pnl']-active['cost'])
                trades.append(active);active=None;qty=np.zeros(2)
            elif pending['action']=='open' and active is None:
                model=pending['model'];beta=model['beta'] if sizing_mode=='price_beta' else model['return_beta'];direction=pending['direction']
                gross=equity
                notionals=np.array([-direction*beta/(1+beta),direction/(1+beta)])*gross
                qty=notionals/opens[k]
                fee=float(np.sum(np.abs(notionals)))*cost_bps/10000
                equity-=fee;total_cost+=fee
                active=dict(fold=model['id'],entry_bj=bj(t[k]),entry_ms=int(t[k]),signal_ms=pending['signal_ms'],
                            train_end_bj=model['train_end_bj'],entry_prices=opens[k].tolist(),qty=qty.tolist(),
                            direction='long HYPE / short BTC' if direction==1 else 'short HYPE / long BTC',
                            beta=beta,signal_price_beta=model['beta'],sizing_mode=sizing_mode,entry_z=pending['z'],entry_gross_notional=gross,
                            price_pnl=0.0,funding_pnl=0.0,cost=fee)
            pending=None
        for leg,rate,mark in fund_map.get(k,[]):
            cash=-float(qty[leg])*mark*rate
            equity+=cash;total_funding+=cash
            if active:active['funding_pnl']+=cash
        pnl=float(np.dot(qty,closes[k]-opens[k]))
        equity+=pnl;total_price+=pnl
        if active:active['price_pnl']+=pnl
        close_time=int(t[k]+STEP)
        if close_time>=first_signal:
            test_bars+=1
            exposed+=bool(active)
            curve.append([close_time,equity])
        if close_time in signal_map and pending is None:
            model,z,last=signal_map[close_time]
            execution=close_time+STEP
            if active:
                direction=1 if active['qty'][1]>0 else -1
                reverted=(direction==1 and z>=-.5) or (direction==-1 and z<=.5)
                reason=('fold_end' if last else 'mean_revert' if reverted else 'z_stop' if abs(z)>=4 else
                        '72h_timeout' if close_time+STEP-active['entry_ms']>=72*3600000 else None)
                if reason:
                    pending=dict(action='close',execute_ms=execution,reason=reason,z=z)
            elif not last and model['beta']>0 and (model['eligible'] or not gated) and 2<=abs(z)<4:
                pending=dict(action='open',execute_ms=execution,model=model,direction=-1 if z>0 else 1,z=z,signal_ms=close_time)
        if equity<=0:raise ValueError('Equity exhausted; need liquidation model')
    if active:
        # 只对最终边界无法延迟成交的残留持仓按末根收盘清算，明确记final_boundary。
        fee=float(np.sum(np.abs(qty)*closes[-1]))*cost_bps/10000
        equity-=fee;total_cost+=fee;active['cost']+=fee
        active.update(exit_bj=bj(t[-1]+STEP),exit_ms=int(t[-1]+STEP),exit_prices=closes[-1].tolist(),reason='final_boundary',exit_z=None,
                      holding_hours=(int(t[-1]+STEP)-active['entry_ms'])/3600000,
                      net_pnl=active['price_pnl']+active['funding_pnl']-active['cost'])
        trades.append(active);curve[-1][1]=equity
    assert abs(equity-INITIAL-total_price-total_funding+total_cost)<1e-6
    assert abs(sum(x['net_pnl'] for x in trades)-(equity-INITIAL))<1e-6
    for tr in trades:
        assert tr['entry_ms']>=tr['signal_ms']+STEP
        assert dt.datetime.fromisoformat(tr['train_end_bj']).timestamp()*1000<tr['signal_ms']
    eq=np.array([r[1] for r in curve]);peak=np.maximum.accumulate(np.r_[INITIAL,eq])
    dd=float(np.min(np.r_[INITIAL,eq]/peak-1))
    ledgers_by_month={}
    for trade in trades:
        key=trade['exit_bj'][:7];item=ledgers_by_month.setdefault(key,dict(trades=0,net_pnl=0.0))
        item['trades']+=1;item['net_pnl']+=trade['net_pnl']
    summary=dict(gated=gated,sizing_mode=sizing_mode,cost_bps_per_leg_per_fill=cost_bps,trades=len(trades),
                 return_pct=(equity/INITIAL-1)*100,price_pnl=total_price,funding_pnl=total_funding,
                 execution_cost=total_cost,net_pnl=equity-INITIAL,max_drawdown_pct=dd*100,
                 win_rate=float(np.mean([tr['net_pnl']>0 for tr in trades])) if trades else None,
                 exposure_fraction=exposed/test_bars,average_hold_hours=float(np.mean([tr['holding_hours'] for tr in trades])) if trades else None,
                 exit_reasons={reason:sum(tr['reason']==reason for tr in trades) for reason in ['mean_revert','z_stop','72h_timeout','fold_end','final_boundary']},
                 exit_month_pnl=ledgers_by_month)
    return summary,trades,curve

def main():
    t,opens,closes,ht,hp,funding,origins=load()
    logs=np.log(hp);ret5=np.diff(np.log(closes),axis=0);reth=np.diff(logs,axis=0)
    a,levelbeta,spread=fit(logs[:,0],logs[:,1])
    ra,rb,returnresid=fit(reth[:,0],reth[:,1])
    full=dict(hourly_n=len(hp),price_level_correlation=float(np.corrcoef(logs.T)[0,1]),
              return_correlation_5m=float(np.corrcoef(ret5.T)[0,1]),return_correlation_1h=float(np.corrcoef(reth.T)[0,1]),
              return_beta_1h=rb,level_alpha=a,level_beta=levelbeta,
              variance_reduction_same_hype_notional=1-float(np.var(returnresid,ddof=1)/np.var(reth[:,1],ddof=1)),
              coint_hype_on_btc=coint_test(logs[:,1],logs[:,0]),coint_btc_on_hype=coint_test(logs[:,0],logs[:,1]),
              adf={token:dict(log_level=adf(logs[:,leg]),log_returns=adf(reth[:,leg])) for leg,token in enumerate(['BTC','HYPE'])})
    rolling=[]
    for i in range(720,len(reth),24):
        rr=reth[i-720:i]
        _,beta,res=fit(rr[:,0],rr[:,1])
        rolling.append(dict(end_bj=bj(ht[i]),correlation=float(np.corrcoef(rr.T)[0,1]),return_beta=beta))
    monthly=[]
    months=sorted(set(bj(stamp)[:7] for stamp in ht))
    for month in months:
        mask=np.array([bj(stamp)[:7]==month for stamp in ht])
        if np.sum(mask)<168:continue
        xx,yy=logs[mask].T
        _,lb,_=fit(xx,yy);_,rbet,_=fit(np.diff(xx),np.diff(yy))
        monthly.append(dict(month=month,hours=int(np.sum(mask)),return_correlation=float(np.corrcoef(np.diff(xx),np.diff(yy))[0,1]),
                            return_beta=rbet,price_beta=lb,coint=coint_test(yy,xx)))
    print('Full:',json.dumps(full),flush=True)
    folds=models(ht,hp)
    print('Folds:',len(folds),'eligible:',sum(m['eligible'] for m in folds),flush=True)
    experiments=[];curves={};ledgers={}
    for gated in [True,False]:
        for bps in [0,6,12]:
            summary,ledger,curve=backtest(t,opens,closes,ht,hp,funding,folds,bps,gated)
            key=('gated' if gated else 'ungated')+f'_{bps}bps'
            experiments.append(dict(name=key,**summary));curves[key]=curve;ledgers[key]=ledger
            print(key,json.dumps(summary),flush=True)
    # 机制对照：信号不变，仅用事前收益beta分配名义金额；不据此挑选最优参数。
    summary,ledger,curve=backtest(t,opens,closes,ht,hp,funding,folds,6,True,'return_beta')
    key='gated_return_beta_6bps'
    experiments.append(dict(name=key,**summary));curves[key]=curve;ledgers[key]=ledger
    print(key,json.dumps(summary),flush=True)
    result=dict(date='2026-10-05',data_cutoff_bj=bj(t[-1]+STEP),sources=origins,
                versions=dict(numpy=np.__version__,pandas=pd.__version__,statsmodels=statsmodels.__version__,matplotlib=matplotlib.__version__),
                full=full,rolling_30d=rolling,monthly=monthly,folds=folds,
                rules=dict(train_hours=1440,retrain_hours=168,entry_z=2,exit_z=.5,stop_z=4,max_hold_hours=72,
                           gross_notional_to_equity=1,execution_delay_minutes=5,signal_frequency='1h',funding='historical actual Binance'),
                backtests=experiments)
    (BASE/'2026-10-05-pair研究结果.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    for key,ledger in ledgers.items():
        (BASE/f'2026-10-05-pair交易明细-{key}.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    (BASE/'2026-10-05-pair净值曲线.json').write_text(json.dumps(curves,ensure_ascii=False,separators=(',',':'))+'\n')
    fig,axes=plt.subplots(3,1,figsize=(12,11),constrained_layout=True)
    dates=[dt.datetime.fromtimestamp(v/1000,TZ) for v in ht]
    axes[0].plot(dates,hp[:,0]/hp[0,0],label='BTC',color='#3262aa',lw=1.2)
    axes[0].plot(dates,hp[:,1]/hp[0,1],label='HYPE',color='#b36820',lw=1.2)
    axes[0].set_ylabel('Start = 1');axes[0].set_title('BTC / HYPE: correlated returns do not ensure a stable price spread')
    axes[0].legend()
    rd=[dt.datetime.fromisoformat(row['end_bj']) for row in rolling]
    axes[1].plot(rd,[row['return_beta'] for row in rolling],label='30-day hourly return beta',color='#3262aa')
    axes[1].set_ylabel('BTC hedge notional / HYPE notional');axes[1].legend()
    for key,label,color in [('gated_6bps','Cointegration gate, 6 bps / fill','#3262aa'),('ungated_6bps','No gate, 6 bps / fill','#b36820')]:
        curve=np.array(curves[key]);idx=np.arange(0,len(curve),12)
        axes[2].plot([dt.datetime.fromtimestamp(v/1000,TZ) for v in curve[idx,0]],curve[idx,1]/INITIAL,label=label,color=color)
    axes[2].set_ylabel('Equity / initial equity');axes[2].set_title('Walk-forward simulation: actual funding, no liquidation model');axes[2].legend()
    for ax in axes:ax.grid(alpha=.2);ax.tick_params(axis='x',rotation=0)
    fig.savefig(ROOT/'HYPE'/'2026-10-05-pair研究.png',dpi=160)
    plt.close(fig)

if __name__=='__main__':main()
