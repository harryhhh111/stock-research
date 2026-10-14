"""兼容原HYPE/BTC命令；新产物保存到数字资产/factcheck。"""
import importlib.util
import sys
from pathlib import Path

if __name__ == '__main__':
    tool = Path(__file__).resolve().parents[2] / '数字资产/factcheck/sync_prices.py'
    spec = importlib.util.spec_from_file_location('token_price_sync', tool)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    args = sys.argv[1:]
    defaults = []
    if '--tokens' not in args:
        defaults += ['--tokens', 'HYPE', 'BTC']
    if '--source' not in args:
        defaults += ['--source', 'binance-perp']
    sys.exit(module.main(defaults + args))
