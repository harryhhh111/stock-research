from pathlib import Path
import json
P=Path(__file__).resolve().parent
v=json.loads((P/'valuation-results.json').read_text());price=v['price'];eps=v['adjusted_eps_ttm'];shares=v['shares_million'];div=3.92
hist=[]
for year,px,cap,pe,ps,fcf_multiple in [(2024,439.21,3321869,37.69,13.55,44.85),(2025,492.54,3697022,36.31,13.12,51.63),(2026,372.32,2770955,20.72,8.35,41.37)]:hist.append(dict(fy=year,price=px,market_cap_million=cap,pe_gaap=pe,ps=ps,p_fcf=fcf_multiple,fcf_yield_pct=100/fcf_multiple,price_basis=f'{year}-06-30或最近前交易日；供应商年度快照，非全年均值',source='https://stockanalysis.com/stocks/msft/financials/ratios/'))
future_eps=(price-sum(div/1.1**y for y in range(1,4)))*1.1**3/25
ni=future_eps*shares;margin=134375/346445;target_revenue=ni/margin
qmargin=36422/92279;qtarget=ni/qmargin
bridge=[]
for m365g in [.10,.15]:
 for otherg in [0,.05]:
  m365=27778*4*(1+m365g)**3;other=(92279-33165-27778)*4*(1+otherg)**3;azure=qtarget-m365-other
  bridge.append(dict(m365_growth=m365g,other_growth=otherg,required_azure_revenue_million=azure,required_azure_growth=(azure/(33165*4))**(1/3)-1))
out=dict(as_of='2026-11-13',history=hist,peers=[dict(symbol='MSFT',price=523.88,ttm_pe_gaap=27.35,forward_pe=25.24,source='https://stockanalysis.com/stocks/msft/statistics/'),dict(symbol='AMZN',price=266.66,ttm_pe_gaap=21.55,forward_pe=26.97,source='https://stockanalysis.com/stocks/amzn/statistics/'),dict(symbol='GOOGL',price=295.77,ttm_pe_gaap=15.44,forward_pe=21.45,source='https://stockanalysis.com/stocks/googl/statistics/')],peer_caveat='第三方集团口径快照，AMZN混合零售/广告/AWS，GOOGL混合搜索/视频/云，微软混合企业软件/云/消费业务。TTM净利均可能含投资估值等非经营项；本轮未完成同业调整利润复核，不能据PE判微软比同业贵或直接套云业务估值。Forward PE为供应商一致预期，非公司指引。',reverse_bridge=dict(horizon='2029-11-13；FY2030为最近完整财年代理，非精确FY2030预测',target_eps=future_eps,fixed_shares_million=shares,target_adjusted_net_income_million=ni,ttm_normalized_margin=margin,target_revenue_if_ttm_margin_million=target_revenue,q1_annualized_adjusted_margin=qmargin,target_revenue_if_q1_margin_million=qtarget,q1_annualized_base_million=dict(azure=33165*4,m365=27778*4,other=(92279-33165-27778)*4),azure_conditional_bridge=bridge,limitations='Q1年度化仅为条件桥，非管理层年度指引；季节性未消除。调整利润仅剔OpenAI，仍含Anthropic等其他一次性项目，非完全正常化利润率。Azure和Microsoft365包括传统业务与AI，不能将其收入全称AI。假设业务组合变化但集团利润率不变，纯敏感性，非唯一市场预期；固定股数，无净回购增厚。',source='https://www.microsoft.com/en-us/Investor/earnings/FY-2027-Q1/press-release-webcast'))
(P/'data'/'valuation-comparables.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2))
