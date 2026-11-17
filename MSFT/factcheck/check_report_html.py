"""核验静态HTML、图表与既有输入勾稽；不代替事实与视觉验收。"""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import unquote
import re,json,hashlib
p=Path(__file__).resolve().parent;root=p.parent
s=BeautifulSoup((root/'MSFT.html').read_text(),'html.parser');ids=[x['id'] for x in s.select('[id]')]
assert len(ids)==len(set(ids))
for a in s.select('a[href]'):
 h=a['href']
 if h.startswith('#'):assert h[1:] in ids,h
 elif not re.match(r'^(https?:|mailto:)',h):assert (root/unquote(h.split('#')[0])).exists(),h
for i in [1,2,3,4,5,6,7,9,11]:assert s.select_one('#module-'+str(i)+' h2')
assert s.select_one('#module-2 #capital-overview')
assert s.select_one('#module-2 #current-outlook')
assert s.select_one('#module-4 #module-10 h3')
assert s.select_one('#module-8 h3')  # 资本分配已合并第三节，旧稳定锚点保留。
assert len(s.select('figure'))==11 and len(s.select('svg.sankey'))==3
assert not s.select('script[src],link[rel=stylesheet],img[src^=http]')
for key in ['Windows与SQL Server','GitHub','LinkedIn','Anthropic','OpenAI','不可比','租赁','不是市场一致预期','HTML尚未接入']:
 assert key in s.get_text(),key
# 图表序列来自同一核验文件，检查主表可见值和计算结果。
d=json.loads((p/'data/inputs.json').read_text());v=json.loads((p/'valuation_2026-11-13_results.json').read_text());t=s.get_text()
for y,a in d['annual'].items():
 assert abs(sum(x[int(y)-2024] for x in d['products'].values())-a['revenue'])<1e-6
 for k in ['revenue','op','net','cfo','capex']:assert f'{a[k]:.3f}' in t,(y,k)
for a in [30.242,182.935,139.500,52.546,.196,20.935]:assert f'{a:.3f}' in t
assert abs(30.242+182.935-139.500-52.546-.196-20.935)<1e-6
for key in ['pe_eps','pe_openai_adjusted','fcf_yield_pct']:assert f'{v[key]:.2f}' in t
for node in s.select('svg rect'):
 if node.has_attr('height'):assert float(node['height'])>=0
result={'date':'2026-11-14','scope':'HTML migration structure, numerical consistency and content preservation','reading_modules':9,'original_research_questions_covered':11,'figures':11,'inline_sankeys':3,'tables':len(s.select('table')),'local_links':'passed','same_input_checks':'passed','legacy_markdown_kept':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in ['MSFT.md','云服务、数据中心与AI业务.md','传统软件与现金流底稿.md']},'visual_scope':'browser evidence recorded separately in HTML; print preview not implied'}
(p/'html_report_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
