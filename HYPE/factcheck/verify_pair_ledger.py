"""独立按进出价、数量、资金费事件和收费假设复核每笔交易损益。"""
import datetime as dt
import json
from pathlib import Path

BASE=Path(__file__).resolve().parent

def main():
    result=json.loads((BASE/'2026-10-05-pair研究结果.json').read_text())
    fund=[json.loads((BASE/'data'/f'2026-10-05-{token}-funding-year.json').read_text())['events'] for token in ['BTC','HYPE']]
    summaries=[]
    for case in result['backtests']:
        rows=json.loads((BASE/f"2026-10-05-pair交易明细-{case['name']}.json").read_text())
        totals=dict(price_pnl=0.0,funding_pnl=0.0,cost=0.0,net_pnl=0.0)
        for row in rows:
            q=row['qty'];entry=row['entry_prices'];exit=row['exit_prices']
            price=sum(q[i]*(exit[i]-entry[i]) for i in range(2))
            funding=sum(-q[i]*float(e['markPrice'])*float(e['fundingRate'])
                        for i in range(2) for e in fund[i]
                        if row['entry_ms']<=int(e['fundingTime'])<row['exit_ms'])
            cost=sum(abs(q[i])*(entry[i]+exit[i]) for i in range(2))*case['cost_bps_per_leg_per_fill']/10000
            net=price+funding-cost
            assert abs(price-row['price_pnl'])<1e-6
            assert abs(funding-row['funding_pnl'])<1e-6
            assert abs(cost-row['cost'])<1e-6
            assert abs(net-row['net_pnl'])<1e-6
            assert row['entry_ms']>=row['signal_ms']+300000
            assert dt.datetime.fromisoformat(row['train_end_bj']).timestamp()*1000<row['signal_ms']
            assert abs(sum(abs(q[i])*entry[i] for i in range(2))-row['entry_gross_notional'])<1e-6
            if row['reason']=='72h_timeout':assert row['holding_hours']==72
            for key,value in [('price_pnl',price),('funding_pnl',funding),('cost',cost),('net_pnl',net)]:totals[key]+=value
        assert abs(totals['net_pnl']-case['net_pnl'])<1e-6
        summaries.append(dict(name=case['name'],trades=len(rows),recomputed_totals=totals,status='✅ 逐笔现金损益、资金费时点、成本、名义金额及信号延迟核对通过'))
    for fold in result['folds']:
        assert dt.datetime.fromisoformat(fold['train_end_bj'])<dt.datetime.fromisoformat(fold['test_start_bj'])
    (BASE/'2026-10-05-pair核对结果.json').write_text(json.dumps(summaries,ensure_ascii=False,indent=2)+'\n')
    print('✅',len(summaries),'组研究情景逐笔复核通过')

if __name__=='__main__':main()
