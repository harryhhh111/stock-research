from pathlib import Path
import importlib.util,json,io,contextlib,subprocess,sys
P=Path(__file__).resolve().parent;R=P.parents[2]/'repo'/'tools'
s=importlib.util.spec_from_file_location('audit',R/'report_audit.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
# Two separately retrieved sources. Official via research agent's saved annual report, SA opened in this valuation task on2026-11-15.
official={'FY2026收入':331839,'FY2026净利润':133749,'FY2026经营现金流':182935,'FY2026现金资本开支':115948,'FY2026现金与短期投资':76843,'FY2026自由现金流':66987}
third_party={'FY2026收入':331839,'FY2026净利润':133749,'FY2026经营现金流':182935,'FY2026现金资本开支':115948,'FY2026现金与短期投资':76843,'FY2026自由现金流':66987}
source1='https://www.microsoft.com/investor/reports/ar26/index.html';source2='https://stockanalysis.com/stocks/msft/financials/'
text='# 财务抽检输入（纯数据证据，非研究报告）\n\n单位：百万美元；FY2026截至2026-06-30。FCF=经营现金流-现金资本开支。\n\n| 指标 | FY2026 |\n|---|---|\n'+''.join(f'| {k} | {v} |\n' for k,v in official.items())
(P/'audit-input.md').write_text(text)
points=a.extract_data_points(text);sample=a.sample_points(points,.15,42)
for q in sample:
 label=next(k for k in official if q['label'].startswith(k));q.update(fetched_value=official[label],fetched_source=source1,fetched_value2=third_party[label],fetched_source2=source2)
(P/'audit-results.json').write_text(json.dumps(sample,ensure_ascii=False,indent=2))
subprocess.run([sys.executable,str(R/'report_audit.py'),'extract','--report',str(P/'audit-input.md'),'--seed','42'],stdout=(P/'audit-extract.txt').open('w'))
b=io.StringIO()
with contextlib.redirect_stdout(b): verdict=a.render_verdict(sample,'FY2026财务底表，非整篇HTML报告')
(P/'audit-verdict.txt').write_text(b.getvalue());(P/'audit-verdict.json').write_text(json.dumps(verdict,ensure_ascii=False,indent=2));print(b.getvalue())
