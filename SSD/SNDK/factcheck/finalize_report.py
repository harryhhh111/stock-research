"""Run scoped checks, retain outputs, then bind reviewed reports to the index.

Content status is deliberately partial: automated checks do not certify sources.
"""
from pathlib import Path
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PY = ROOT / '研究流程/tools/reports/.venv/bin/python'
TOOL = ROOT / '研究流程/tools/reports/reports.py'

def run(name, args):
    result = subprocess.run([str(x) for x in args], cwd=ROOT, text=True, capture_output=True)
    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        output = {'stdout': result.stdout, 'stderr': result.stderr}
    (HERE / f'{name}.json').write_text(json.dumps(output, ensure_ascii=False, indent=2))
    if result.returncode or output.get('errors'):
        raise RuntimeError(f'{name}: {output}')
    return output

run('revenue-coverage', [sys.executable, ROOT / '研究流程/skills/revenue-analysis/scripts/check_coverage.py',
                       'SSD/SNDK/reports/revenue-profit.html', '--latest-annual', '2026', '--latest-period', '2027Q1'])
run('cash-verification', [sys.executable, Path.home() / '.codex/skills/cash-flow-analysis/scripts/check_cash_flow.py',
                          'SSD/SNDK/reports/cash-capital.html', '--input', HERE / 'cash-input.json'])
run('entry-verification', [sys.executable, ROOT / '研究流程/tools/entry/validate.py', '--root', 'SSD/SNDK'])

visual = json.loads((HERE / 'visual-checks.json').read_text())
assert visual['offline'] and len(visual['pages']) == 9
assert all(p[m]['scrollWidth'] <= p[m]['width'] for p in visual['pages'] for m in ['desktop', 'mobile'])
assert all(t['width'] <= t['available']+2 for p in visual['pages'] for t in p['print']['tables'])

index = json.loads((ROOT / '研究流程/index/html-index.json').read_text())
updates=[]
for entry in index['reports']:
    identifier = entry['report_id']
    if not (identifier.startswith('sndk-') or identifier in ['industry-nand-overview', 'industry-nand-cycle']):
        continue
    metadata = {'status': 'ready', 'content_status': 'partial', 'document_updated_at': '2026-11-19',
                'financial_as_of': '2026-10-02' if identifier.startswith('sndk-') else None,
                'market_as_of': '2026-11-18' if identifier.startswith('sndk-') else '2026-11-19'}
    if identifier=='sndk-industry-position':metadata['title']='闪迪｜行业、周期与竞争'
    if identifier=='industry-nand-cycle':metadata['title']='NAND｜周期位置、AI需求与扩产'
    updates.append({'id':identifier,'metadata':metadata})

# The CLI validates all ready hashes after each update, so several changed pages
# cannot be updated sequentially. Use its own update/save APIs in one transaction:
# stage each metadata_update, then run the unchanged validating save once.
patch_file=HERE/'index-update.json'
patch_file.write_text(json.dumps(updates,ensure_ascii=False,indent=2))
code='''import importlib.util,json,sys
from pathlib import Path
spec=importlib.util.spec_from_file_location("report_manager",sys.argv[1]);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
root=Path(sys.argv[2]);staged=m.load(root/"研究流程/index/html-index.json");real_save=m.save
def stage(root,new):
 global staged
 staged=new
m.save=stage
for u in json.loads(Path(sys.argv[3]).read_text()):m.metadata_update(root,staged,u["id"],u["metadata"])
real_save(root,staged)
'''
subprocess.run([str(PY),'-c',code,str(TOOL),str(ROOT),str(patch_file)],cwd=ROOT,check=True)

run('report-index-verification', [PY, TOOL, 'check'])
print('Coverage, cash bridge, historical entry, nine-page layouts and report index checks passed; content remains partial as disclosed.')
