# HTML 报告命名与索引规范

维护日期 2026-11-20。路径、登记和迁移按本页执行。研究内容见[研究 SOP](../../研究方式.md)，展示见[图表规范](HTML报告与财务可视化规范.md)，网站见[接入说明](HTML报告内部网站接入.md)。

## 1. 固定路径

| 类型 | 标准路径 | 要求 |
|---|---|---|
| 公司首页 `company_research` | `<项目>/reports/main.html` | 每个公司主体最多一个非归档首页 |
| 专题或模块 `topic` | `<项目>/reports/<slug>.html` | 同公司模块沿用其 `entity_id`，每页有独立 `report_id` |
| 更新 `update` | `<项目>/reports/YYYY-MM-DD-<slug>.html` | 显式给出实际更新日期 |
| 演示 `demo` | `<项目>/reports/<slug>.html` | 内容状态用 `synthetic` |
| 展示资源 | `<项目>/reports/assets/` | 按需登记，历史证据留在 `factcheck/` |

slug 仅用小写英文字母、数字和单个连字符。中文标题写在页面和索引，历史版本由 Git 或发布快照保留。项目沿用既有主体目录。

### 每家公司唯一 HTML 主入口

以 `entity_id` 聚合，网站公司列表只打开唯一非归档首页。已登记的 legacy 首页沿用原路径。只有专题或更新的公司标「主入口待补建」，内部可保留待整理链接。补建时如实说明实际内容与缺口。首页和模块按[模板](公司研究主文档模板.md#唯一主入口)组织，重要判断变化时联动更新首页及相关模块。工具检查主入口唯一和标准卡片顺序，交付另验首页和应有模块的覆盖及实际导航。

### 独立行业入口及模块

在 `行业研究/<细分行业>/reports/` 建档。首页和模块均为 `topic`，共享 `topic:industry-<industry-slug>`，各有独立报告 ID。首页 ID 为 `industry-<industry-slug>-overview`，文件为 `<industry-slug>.html`。模块使用自己的 slug，从首页卡片进入并可返回。公司直接引用适用行业模块及锚点。交付时检查首页唯一、跨页可达，网站快照包括相关模块和获准资源。

## 2. 唯一索引及数据契约

[html-index.json](../index/html-index.json)是唯一清单，字段和取值以 [JSON Schema](../index/html-index.schema.json) 为准。源版本、工作树状态和权限由消费端记录。

| 字段 | 登记规则 |
|---|---|
| `report_id` / `entity_id` | 报告 ID 全库唯一，标题或路径变化时保留。明确写主体，演示可为空 |
| `project_dir` / `entry_path` | 仓库根目录相对 POSIX 路径 |
| `document_updated_at` / `financial_as_of` / `market_as_of` | 分别记真实日期，未知留空，不用文件 mtime。期间细节留在正文 |
| `assets` / `unpublished_links` | 前者列获准资源；后者记录尚未发布的本地来源超链接及原因。图片、样式和绘图数据等必需依赖须可访问 |
| `layout` / `redirects` | 仅首次登记的六份报告适用 legacy。旧兼容页按路径关联稳定 ID |
| `content_sha256` | 绑定实际正文。正文变化后由工具重算，`ready` 要求有效哈希 |

### 交付状态、内容核验和访问权限分别判断

- `draft` 为尚未交付，授权读者可内部阅读并看到草稿标记。 `ready` 为交付可读，要求真实更新日、非占位正文及匹配哈希，允许标明研究和来源缺口。 `archived` 退出当前列表，保留历史入口。
- `content_status` 按实际验收填写。 `unreviewed` 尚未验收，`partial` 仅部分通过，`verified` 为声明范围通过，`synthetic` 为演示。网站显示正文的核验范围及缺口。
- 访问权限由网站登录授权决定。未发布来源保留原因及可见提示，可阅读的正文仍可交付。结构通过后仍须按范围完成内容与视觉验收。

## 3. Agent 执行流程

1. 查索引并确定新建、更新或迁移。用 `create` 生成登记草稿，已有生成器用 `register` 登记生成的页面。
2. 写正文与必要资源。已有页面按稳定 ID 原位更新；复核受影响的图表、引用、生成脚本与核验记录。
3. 用 `update --id <ID> --metadata <JSON路径>` 填真实元数据并同步哈希。JSON 只写要变动的字段，不借更新改 ID、主体、项目、类型或路径。
4. 逐页复核状态和日期，运行 `check` 再交付。退出维护用 `archive`。校验失败时处理实际缺项，禁止扩大豁免、删稳定 ID、编日期或擅自标 `verified`。

从仓库根目录安装和调用：

```bash
tool_dir=研究流程/tools/reports
python3 -m venv "$tool_dir/.venv"
"$tool_dir/.venv/bin/python" -m pip install -r "$tool_dir/requirements.txt"
"$tool_dir/.venv/bin/python" "$tool_dir/reports.py" check
"$tool_dir/.venv/bin/python" "$tool_dir/reports.py" register --help
```

替换最后的子命令可查 `list`、`create`、`update`、`archive` 和 `move`。其他位置可用脚本绝对路径及 `--root`。

## 4. 检查范围及 CI

`check` 校验 Schema、路径与类型、稳定 ID、主入口、日期、哈希、重复 id、锚点及资源。静态检查覆盖可解析的 HTML 引用、CSS URL 和字面量 fetch。动态资源须人工登记及浏览器复核。通过 Git 盘点漏登记的研究 HTML，按工具规则排除原始证据、缓存、外部库、工具等目录。未发布链接声明仅适用于来源超链接。

[HTML Reports 工作流](../../.github/workflows/html-reports.yml)在 push 和 PR 运行测试和检查。 `--base-ref` 以历史索引核对稳定 ID，默认 HEAD；CI 采用 PR 基线或推送前版本。没有历史索引时仍检查全库漏登记。失败非零退出。需要阻断不合格合并时，在 GitHub 将检查设为必需。

## 5. 既有报告迁移

自包含报告可用 `move` 迁至标准路径。专题给 `--slug`，日期更新另给 `--date`。工具保留正文原字节、ID、日期与旧兼容页。兼容页启用脚本可携锚点跳转，关闭脚本时保留普通链接。含跨文件相对依赖的报告须先核对生成器、证据、脚本与旧地址映射，再按实际范围迁移。保留重要解释、财务核验日和并行工作。
