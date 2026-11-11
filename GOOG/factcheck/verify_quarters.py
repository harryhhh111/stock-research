"""按官方公告原始单季值复算，并与H1/9M勾稽；金额M美元。"""
from pathlib import Path
import json
P=Path(__file__).resolve().parent
# revenue, cloud revenue/op, group op/common net, CFO, CapEx, SBC, EPS
rows={'2025Q4':[113828,17664,5313,35934,34455,52402,27851,7071,2.82],
'2025Q1':[90234,12260,2177,30606,34540,36150,17197,5516,2.81],
'2025Q2':[96428,13624,2826,31271,28196,27747,22446,5998,2.31],
'2025Q3':[102346,15157,3594,31228,34979,48414,23953,6368,2.87],
'2026Q1':[109896,20028,6598,39696,62578,45790,35674,6751,5.11],
'2026Q2':[119796,24768,8814,40770,112107,39069,44924,7957,9.11],
'2026Q3':[127577,30709,11121,40576,26170,42290,51355,8630,2.12]}
keys=['revenue','cloud','cloud_op','op','common_net','cfo','capex','sbc','eps']
data={q:dict(zip(keys,v)) for q,v in rows.items()}
for q,x in data.items():x['fcf']=x['cfo']-x['capex'];x['cloud_margin']=x['cloud_op']/x['cloud'];x['cloud_share']=x['cloud']/x['revenue']
for k,total in {'revenue':357269,'op':121042,'common_net':200855,'cfo':127149,'capex':131953,'sbc':23338}.items():assert sum(data[f'2026Q{i}'][k] for i in range(1,4))==total,k
for k,total in {'revenue':229692,'op':80466,'common_net':174685,'cfo':84859,'capex':80598,'sbc':14708}.items():assert sum(data[f'2026Q{i}'][k] for i in range(1,3))==total,k
sources={q:f'https://s206.q4cdn.com/479360582/files/doc_financials/{q[:4]}/q{q[-1]}/{q[:4]}q{q[-1]}-alphabet-earnings-release.pdf' for q in ['2026Q1','2026Q2','2026Q3','2025Q4']}
(P/'data/2026-11-04-quarter-inputs.json').write_text(json.dumps({'unit':'USD million; EPS USD','method':'All quarters directly disclosed; 2025 Q1-Q3 comparatives in respective 2026 releases; Q4 from 2025 release','sources':sources,'quarters':data},ensure_ascii=False,indent=2))
s='### 当年完整单季序列（2026-11-04补齐）\n\n单位：M美元（1 M＝100万美元）；EPS为美元。季度均截至3/6/9月末，Google财年等于自然年；Q1环比基期为2025Q4。金额为官方原始单季值，比例为复算。\n\n| 季度 | Cloud收入 | 同比 | 环比 | 集团收入占比 | Cloud经营利润 | 同比 | 环比 | 利润率 | 环比变化 |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n'
for i in range(1,4):
 x=data[f'2026Q{i}'];y=data[f'2025Q{i}'];b=data['2025Q4' if i==1 else f'2026Q{i-1}'];s+=f"| 2026Q{i} | {x['cloud']:,} | {x['cloud']/y['cloud']-1:.2%} | {x['cloud']/b['cloud']-1:.2%} | {x['cloud_share']:.2%} | {x['cloud_op']:,} | {x['cloud_op']/y['cloud_op']-1:.2%} | {x['cloud_op']/b['cloud_op']-1:.2%} | {x['cloud_margin']:.2%} | {(x['cloud_margin']-b['cloud_margin'])*100:+.2f}个百分点 |\n"
s+='\n### 集团投入：三年年度历史\n\n单位：M美元。以下均为集团口径，不能解释为Cloud独立现金流。\n\n| 年度 | CFO | 现金CapEx | FCF |\n|---|---:|---:|---:|\n| 2023 | 101,746 | 32,251 | 69,495 |\n| 2024 | 125,299 | 52,535 | 72,764 |\n| 2025 | 164,713 | 91,447 | 73,266 |\n\n### 集团投入：当年完整单季序列\n\n单位：M美元。FCF跨零不用百分比增长。\n\n| 季度 | CFO | 同比 | 环比 | 现金CapEx | 同比 | 环比 | FCF | 同比变化金额 | 环比变化金额 | SBC |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n'
for i in range(1,4):
 x=data[f'2026Q{i}'];y=data[f'2025Q{i}'];b=data['2025Q4' if i==1 else f'2026Q{i-1}'];s+=f"| 2026Q{i} | {x['cfo']:,} | {x['cfo']/y['cfo']-1:.2%} | {x['cfo']/b['cfo']-1:.2%} | {x['capex']:,} | {x['capex']/y['capex']-1:.2%} | {x['capex']/b['capex']-1:.2%} | {x['fcf']:,} | {x['fcf']-y['fcf']:+,} | {x['fcf']-b['fcf']:+,} | {x['sbc']:,} |\n"
s+='\n【复算判定】✅ Q1+Q2与H1公告的收入、经营利润、普通股净利润、CFO、CapEx、SBC一致；再加Q3与9M一致；每季FCF=CFO−现金CapEx。EPS取单季披露，不以累计差分。\n\n【趋势解释】Cloud收入同比从63.36%升至81.80%、102.61%，利润率由32.94%升至35.59%、36.21%；但集团FCF从Q1的10,116转为Q2的−5,855、Q3的−9,065，显示收入扩张与现金回报暂不同步。Q3 CFO另受TPU库存和欧盟罚款现金支付影响，不应全部归因于建设。Cloud利润未分摊全部共享前沿AI研发。\n\n来源：'
s+='、'.join(f'[{q}官方公告]({u})' for q,u in sources.items())+'；原件存factcheck/data对应PDF，同季基数来自公告对比栏。计算及原始值见[季度脚本](factcheck/verify_quarters.py)、[季度底表](factcheck/data/2026-11-04-quarter-inputs.json)。\n\n'
(P/'2026-11-04-季度表.md').write_text(s)
print('H1与9M六项勾稽通过')

# 主要业务占比与同比，以及分部加总勾稽。
segment_file=P/'data/2026-11-04-segment-quarter-inputs.json'
if segment_file.exists():
 segments=json.loads(segment_file.read_text())['segments_prior_current']
 for i in range(3):
  assert sum(segments[k][1][i] for k in ['Search','YouTube ads','Network','订阅/平台/设备'])==segments['Services合计'][1][i]
 ratios={k:[{'yoy':b[i]/a[i]-1,'group_share':b[i]/data[f'2026Q{i+1}']['revenue']} for i in range(3)] for k,(a,b) in segments.items()}
 (P/'2026-11-04-分部季度复算.json').write_text(json.dumps(ratios,ensure_ascii=False,indent=2))
 print('分部加总及季度比例复算通过')
