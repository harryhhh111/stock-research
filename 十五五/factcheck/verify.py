"""复算官方财政引用值；从脚本自身路径读取输入，保留原始输入。"""
import json
from pathlib import Path

base = Path(__file__).resolve().parent
inputs = json.loads((base / 'data/fiscal_inputs.json').read_text(encoding='utf-8'))
results = {}
for key in ('special_treasury', 'local_special'):
    values = inputs[key]
    results[key] = {
        'annual_quota_yoy_pct': round((values['2026'] / values['2025'] - 1) * 100, 2),
        'h1_issuance_progress_pct': round(values['2026_h1_issued'] / values['2026'] * 100, 2),
    }
output = {'checked_on': inputs['checked_on'], 'results': results,
          'boundary': '额度、发行、下达、实际支出不可混同；不代表企业订单或收入。'}
(base / '核验结果.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(output, ensure_ascii=False, indent=2))
