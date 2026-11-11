"""复算Q3附注手工摘录输入；来源及日期保存在输入JSON，路径相对脚本。"""
import json
from pathlib import Path
b=Path(__file__).resolve().parent
d=json.loads((b/'data/q3-10q-inputs-2026-11-04.json').read_text())
debt=d['debt_face']-d['discount_cost']
assert abs(debt-d['debt_current']-d['debt_noncurrent'])<1e-8
assert abs(sum(d['commitments'])-d['commitments_total'])<1e-8
net=debt-d['cash']-d['securities']
r={'units':'USD billion','as_of':'2026-09-30','debt':debt,'net_debt_ex_leases':net,'net_debt_finance_leases':net+d['finance_lease'],'net_debt_all_leases':net+d['finance_lease']+d['operating_lease'],'interest_coverage_9m':79.389/3.805,'ttm_fcf_gross':168.300-215.192,'ttm_fcf_company':168.300-215.192+4.535,'ttm_fcf_less_sbc_sensitivity':168.300-215.192+4.535-19.873,'checks':'debt reconciliation and commitment sums passed'}
(b/'q3-balance-results-2026-11-04.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
