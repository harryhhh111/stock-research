"""Deterministic truth cases, unit/date errors, HTML injection and CLI behavior."""
from copy import deepcopy
from datetime import date
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'implied-valuation'
SCRIPT = SKILL / 'scripts' / 'valuation.py'
spec = importlib.util.spec_from_file_location('valuation', SCRIPT)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


class ValuationTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((SKILL / 'assets' / 'example-input.json').read_text())

    def test_hand_calculated_five_year_case(self):
        r = v.calculate(self.data)
        # 100 * 1.1^5 = 161.051, profit 161.051 * 1000m / PE20 = 8052.55m.
        self.assertAlmostEqual(r['base']['required_price'], 161.051)
        self.assertAlmostEqual(r['base']['required_profit'], 8052.55)
        self.assertAlmostEqual(r['base']['profit_cagr'], 8.05255 ** .2 - 1)
        self.assertEqual(r['base']['return_years'], 5)
        self.assertAlmostEqual(r['base']['price_present_value'], 100)
        self.assertAlmostEqual(r['delays'][2]['required_profit'], 9743.5855)

    def test_dilution_and_buyback(self):
        original = v.calculate(self.data)['base']
        for ratio in (1.2, .8):
            with self.subTest(ratio=ratio):
                d = deepcopy(self.data)
                d['target_shares'] *= ratio
                r = v.calculate(d)['base']
                self.assertAlmostEqual(r['required_profit'], original['required_profit'] * ratio)
                self.assertAlmostEqual(r['required_price'], original['required_price'])

    def test_units_are_equivalent(self):
        for unit, profit in [('unit', 1e9), ('M', 1000), ('B', 1)]:
            d = deepcopy(self.data)
            d.update(profit_unit=unit, net_profit=profit)
            self.assertAlmostEqual(v.calculate(d)['base']['profit_multiple'], 8.05255)

    def test_profit_and_return_horizons_differ(self):
        d = deepcopy(self.data)
        d.update(profit_period_start='2024-01-01', profit_period_end='2024-12-31')
        d['evidence']['net_profit']['source_date'] = '2025-02-01'
        r = v.calculate(d)['base']
        self.assertEqual(r['return_years'], 5)
        self.assertEqual(r['profit_growth_years'], 6)
        self.assertAlmostEqual(r['profit_cagr'], 8.05255 ** (1/6) - 1)

    def test_leap_day_anniversaries(self):
        self.assertEqual(v.years_between(date(2024,2,29), date(2025,2,28)), 1)
        self.assertEqual(v.years_between(date(2024,2,29), date(2028,2,29)), 4)
        self.assertAlmostEqual(v.years_between(date(2025,1,1),date(2025,7,1)),181/365)

    def test_sensitivity_monotonicity(self):
        r = v.calculate(self.data)
        for col in range(3):
            profits = [x['scenarios'][col]['required_profit'] for x in r['sensitivity']]
            self.assertEqual(profits, sorted(profits, reverse=True))
        self.assertTrue(all(r['delays'][i+1]['required_profit'] > r['delays'][i]['required_profit'] for i in range(2)))

    def test_zero_return_and_negative_return(self):
        d = deepcopy(self.data)
        d['required_return'] = 0
        self.assertAlmostEqual(v.calculate(d)['base']['required_price'],100)
        d['required_return'] = -.1
        self.assertAlmostEqual(v.calculate(d)['base']['required_price'],59.049)

    def test_invalid_numeric_inputs(self):
        for field, values in {'net_profit':[0,-1,True,'100',float('nan'), 10**400], 'target_pe':[0,-1],
                              'required_return':[-1,float('inf')], 'current_shares':[0],
                              'target_shares':[-1], 'price':[0]}.items():
            for value in values:
                with self.subTest(field=field,value=value):
                    d = deepcopy(self.data)
                    d[field] = value
                    with self.assertRaises(v.InputError): v.calculate(d)

    def test_invalid_dates_or_incomplete_annual(self):
        for changes in [{'target_date':'2025-12-31'}, {'target_date':'2025-02-30'},
                        {'profit_period_start':'2025-07-01'}, {'profit_period_end':'2026-01-31'},
                        {'target_date':'9998-12-31'}]:
            d = deepcopy(self.data)
            d.update(changes)
            with self.subTest(changes=changes), self.assertRaises(v.InputError): v.calculate(d)

    def test_future_evidence_and_currency(self):
        for key, change in [('net_profit',{'source_date':'2026-01-01'}),
                            ('price',{'currency':'CNY'}), ('current_shares',{'currency':'USD'}),
                            ('net_profit',{'source_date':'2025-10-01'})]:
            d = deepcopy(self.data)
            d['evidence'][key].update(change)
            with self.subTest(key=key,change=change), self.assertRaises(v.InputError): v.calculate(d)

    def test_confirmations_and_applicability(self):
        for key,value in [('comparable_profit',False),('major_capital_changes',True),('special_industry',True)]:
            d=deepcopy(self.data);d['applicability'][key]=value
            with self.assertRaises(v.InputError):v.calculate(d)
        self.data['assumptions_confirmed']=False
        with self.assertRaises(v.InputError):v.calculate(self.data)

    def test_unknown_missing_and_sensitivity(self):
        for mode in ['extra','missing','pe','duplicate','type']:
            d=deepcopy(self.data)
            if mode=='extra': d['price_currency']='USD'
            elif mode=='missing': del d['share_basis']
            elif mode=='pe':d['sensitivity_pe']=[15,25]
            elif mode=='duplicate':d['sensitivity_pe']=[20,20]
            else:d['schema_version']=True
            with self.subTest(mode=mode), self.assertRaises(v.InputError):v.calculate(d)

    def test_overflow_is_reported(self):
        self.data['required_return']=1e200
        with self.assertRaises(v.InputError):v.calculate(self.data)

    def test_input_unchanged_and_safe_html(self):
        d=deepcopy(self.data)
        d['company']='<script>alert(1)</script>'
        d['evidence']['price']['source']='javascript:alert(1) & <img src=x onerror=alert(1)>'
        before=deepcopy(d)
        result=v.calculate(d)
        html=v.render(result)
        self.assertEqual(before,d)
        self.assertNotIn('<script',html)
        self.assertNotIn('<img',html)
        self.assertIn('&lt;script&gt;',html)
        self.assertIn('8,052.55',html)
        self.assertNotIn('<script src=',html)
        self.assertTrue(result['synthetic'])

    def test_cli_outputs_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/'report.html'
            command=[sys.executable,str(SCRIPT),'--input',str(SKILL/'assets/example-input.json'),'--output',str(target)]
            run=subprocess.run(command,cwd=td,capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            result=json.loads(target.with_suffix('.json').read_text())
            self.assertAlmostEqual(result['base']['required_profit'],8052.55)
            original=target.read_bytes()
            self.assertEqual(subprocess.run(command,capture_output=True).returncode,2)
            self.assertEqual(target.read_bytes(),original)

    def test_cli_invalid_json_leaves_no_output(self):
        with tempfile.TemporaryDirectory() as td:
            for i, payload in enumerate(['{"price":NaN}', '{"price":1,"price":2}', '{']):
                source=Path(td)/f'input{i}.json';source.write_text(payload)
                target=Path(td)/f'report{i}.html'
                result=subprocess.run([sys.executable,str(SCRIPT),'--input',str(source),'--output',str(target)],capture_output=True)
                self.assertEqual(result.returncode,2)
                self.assertFalse(target.exists())
                self.assertFalse(target.with_suffix('.json').exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
