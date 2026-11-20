# 研究流程导航

整理日期 2026-11-20。研究先从 [研究方式](../研究方式.md) 进入，按任务加载模块、模板和执行检查。公司研究前先查适用的行业背景。

## 按任务进入

| 你要做什么 | 先看哪里 |
|---|---|
| 开始公司研究/更新 | [研究方式](../研究方式.md) → 先做行业一轮 → 按追问推进相关模块 → [卡片首页及模块模板](standards/公司研究主文档模板.md) → [验收清单](standards/研究更新与交付检查清单.md) |
| 独立行业调研或复用 | [行业研究](../行业研究/README.md) → [行业与竞争模块](standards/modules/行业与竞争.md) |
| 生成HTML与财务图表 | [展示规范](standards/HTML报告与财务可视化规范.md) |
| 新建、修改、登记、归档报告 | [命名与索引规范](standards/HTML报告命名与索引规范.md) → [报告清单](index/html-index.json) |
| 后端加载展示HTML | [内部网站接入](standards/HTML报告内部网站接入.md)，直接读取唯一索引，不维护第二份清单 |
| 研究主体、证券和旧Markdown入口 | [研究库项目规范](standards/研究库项目规范.md) → [入口工具说明](tools/entry/README.md) |
| 决定哪些材料提交Git | [Git管理说明](standards/2026-10-08-Git管理说明.md) |
| 回看过去的缺口分析/验证 | [归档](archive/)，只作历史背景 |
| 配对回测与量化公共代码 | [量化研究工具](../量化研究工具/README.md)，不在本目录维护 |

## 目录职责

```text
研究流程/
├── README.md
├── standards/     # 规则、模板、验收与网站接入
│   └── modules/   # 各研究模块的执行细则
├── index/         # html-index.json 及 JSON Schema
├── skills/        # 研究模块使用的仓库 Skill
├── tools/
│   ├── entry/     # research.yaml 校验与 Markdown 章节提取
│   └── reports/   # HTML 报告管理与校验
└── archive/       # 历史分析、覆盖盘点与验证记录
```

本地`.venv`、`__pycache__`等环境/缓存仍被Git忽略；它们不是研究文档，也不应作为发布资源。现有Python环境随工具目录迁移，文档命令统一使用`python -m pip`，不依赖旧位置的pip启动脚本。

## 常用检查

```bash
研究流程/tools/reports/.venv/bin/python 研究流程/tools/reports/reports.py check
研究流程/tools/reports/.venv/bin/python -m unittest discover -s 研究流程/tools/reports/tests -v
python3 研究流程/tools/entry/validate.py
python3 -m unittest discover -s 研究流程/tools/entry -v
```

首次安装依赖按[命名规范](standards/HTML报告命名与索引规范.md)与[入口工具说明](tools/entry/README.md)操作。命令通过分别证明其对应的结构/逻辑检查通过，不替代财务事实与视觉验收。

## 索引路径迁移

当前唯一索引位于 `研究流程/index/html-index.json`。报告工具校验历史 Git 版本时也能读取旧位置的索引，以核对稳定 ID。网站读取当前版本时使用新路径。
