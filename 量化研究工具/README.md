# 量化研究工具

共享配对回测库从`研究流程/pair_lib/`迁入本目录，避免与研究SOP混放。模型、数据口径和数值逻辑保持不变。

- `pair_lib/data.py`：数据加载、对齐、分日与资金费/借券费事件。
- `pair_lib/engine.py`：常驻多空及美元口径计算。
- `pair_lib/metrics.py`：收益、风险、回撤及相对基准指标。
- `pair_lib/regress_hype_btc.py`：与既有HYPE/BTC归档比较；需要本地完整原始输入，不因迁移就宣称已重新跑完整回测。

调用方将本目录加入`sys.path`后`import pair_lib`。CRWV与HYPE现有调用脚本已同步路径；数据仍位于各自项目的factcheck目录，不在此复制行情或原始证据。

本目录只放跨项目可复用的计算工具，公司/策略结论仍回写对应研究项目。运行依赖NumPy；目录迁移验证用合成序列和导入检查，不需要重新下载数据。
