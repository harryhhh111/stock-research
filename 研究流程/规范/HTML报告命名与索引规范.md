# HTML 报告命名与索引规范

维护日期：2026-11-17。本文是报告路径、命名、登记及兼容规则的唯一维护位置。研究内容要求仍见[研究方式](../../研究方式.md)，图表见[展示规范](HTML报告与财务可视化规范.md)，网站接入见[接入入口](HTML报告内部网站接入.md)。

## 1. 固定路径

| 类型/report_type | 标准路径 | 说明 |
|---|---|---|
| company_research | `<项目>/reports/main.html` | 每家公司最多一份非归档主报告 |
| topic | `<项目>/reports/<slug>.html` | 持续专题，slug为小写英文数字及单个连字符 |
| update | `<项目>/reports/YYYY-MM-DD-<slug>.html` | 日期型更新，日期须显式给定且有效 |
| demo | `<项目>/reports/<slug>.html` | 演示须标synthetic，不能混作真实研究 |
| 展示资源 | `<项目>/reports/assets/` | 新资源优先放此；历史证据仍留factcheck并显式登记权限 |

项目可沿用已有嵌套主体目录，不为命名统一移动其他公司。slug只作稳定标识，中文标题写在索引和HTML中；main保留给公司主报告。不使用“最终版/最新版”等文件名。HTML为唯一维护正文，历史版本由Git/发布快照保留，不生成Markdown正文副本。

## 2. 唯一索引及数据契约

[html-index.json](../索引/html-index.json)是全库HTML报告唯一登记源；网站读取，不再另建手工维护的第二份清单。[html-index.schema.json](../索引/html-index.schema.json)是机器结构契约（Draft 2020-12），字段含义如下：

| 字段 | 要求 |
|---|---|
| schema_version / reports / redirects | 当前版本1；reports为报告列表，redirects为显式兼容入口列表 |
| report_id | 稳定、全库唯一的英文slug，不随标题或路径变更；不静默删除，退出使用archive |
| entity_id / project_dir | 显式关联主体及所属公司/主题目录；demo可无主体，不靠ticker猜身份 |
| title / entry_path / report_type | 中文可读标题、仓库根目录相对POSIX路径、上表类型 |
| status | draft/ready/archived；表示交付维护状态，不是买卖观点或自动公开权限 |
| content_status | unreviewed/partial/verified/synthetic；人工核验结论，工具不自动提升 |
| document_updated_at / financial_as_of / market_as_of | ISO日期或null；未知如实留空，不用mtime补齐；详细期间口径仍在报告正文 |
| content_sha256 | 与登记正文版本绑定的SHA-256或null；ready必须有值，正文变更后哈希失配即失败 |
| assets | 逐项批准随报告访问的本地资源/附件路径，不是扫描整个factcheck目录生成的公开许可 |
| unpublished_links | HTML中尚不在发布范围的本地来源链接→具体原因；记录附件访问缺口；非空不阻止正文ready，也不表示研究尚未完成 |
| layout | standard，或仅既有六份报告允许的legacy；不得为新报告扩大legacy豁免 |
| redirects中的from/report_id | 老兼容页路径及目标稳定ID；兼容页须与工具生成内容一致，不作为第二份正文 |

### 交付状态、内容核验和访问权限分别判断

| 维度 | 定义与执行规则 |
|---|---|
| `status=draft` | 作者明确仍在编写、尚未交付；内部网站可供登录用户阅读，必须标“草稿” |
| `status=ready` | 作者已交付可阅读的版本；允许存在已披露的研究缺口和不可访问附件，不等于事实全部核验通过 |
| `status=archived` | 已退出当前维护，默认不进当前报告列表；历史入口另行提供 |
| `content_status` | `unreviewed`未完成内容验收；`partial`仅部分范围通过，正文说明范围和缺口；`verified`声明范围通过内容验收；`synthetic`为演示数据。不得由交付状态、哈希或结构检查自动推断 |
| 网站访问权限 | 由网站登录与授权决定；`draft`不是禁止阅读，`ready`不是公开授权 |

Agent完成写作后，须主动执行对应范围的内容验收，再按实际结果分别填写两类状态；不能用`ready`绕过研究验收。`ready`的机器条件为非占位正文、真实文档更新日和匹配的正文哈希；`unreviewed`或`partial`须在网站明确提示核验状态与已知缺口。哈希只绑定版本，不证明事实正确。附件未开放不自动降为`draft`，核心图表、样式或数据文件缺失则仍不通过展示依赖检查。

所有路径必须在仓库内、不能有`..`、反斜线、绝对路径或符号链接；索引写原文件名，不写URL编码。HTML相对链接可使用不越界的`../`和单次URL编码，由工具归一化检查。网址由后端构造，不能把本机绝对路径交给浏览器。

证券身份继续来自既有入口规范；旧research.yaml仍只接受Markdown，不修改schema、不恢复旧正文更新。HTML报告索引不冒充已经实现的章节提取器。源commit/working-tree、dirty和发布包版本由发布端在读取该索引时另行记录，不将索引自身的commit号硬写成自引用字段。

## 3. Agent 必须执行的流程

**先查索引 → 确定更新或新建 → 用工具取得/登记标准路径 → 写HTML及必要资源 → 复核并更新元数据 → 运行check与内容验收 → 交付。**

- 已有report_id优先原位更新，不因新日期再建一份公司主报告；未取得真实数据截止日就保留null。
- 使用`create`生成已登记草稿；已有生成器可以先输出到标准路径，再用`register`登记。生成文件尚未登记期间check会失败，这是正常的未完成状态。
- 用`update`同步元数据并重算正文哈希；运行这个命令不代表已经事实核验，content_status须按实际结果选择。
- 不手工扩大排除目录、删索引项、增加legacy路径、填虚假verified或编造日期来消除错误。
- 更新内容后检查所有受影响图表、引用、生成脚本和核验记录；索引通过只证明路径/结构等对应检查通过，不能替代研究内容与视觉验收。

工具依赖安装到本目录被Git忽略的虚拟环境；不影响报告或Skill的运行依赖：

```bash
python3 -m venv 研究流程/工具/报告工具/.venv
研究流程/工具/报告工具/.venv/bin/python -m pip install -r 研究流程/工具/报告工具/requirements.txt
```

常用命令（从仓库根目录运行；其他位置用脚本绝对路径或`--root`）：

```bash
研究流程/工具/报告工具/.venv/bin/python 研究流程/工具/报告工具/reports.py list
研究流程/工具/报告工具/.venv/bin/python 研究流程/工具/报告工具/reports.py create --id msft-new-topic --project MSFT --title "新专题" --entity company:microsoft --type topic --slug new-topic
研究流程/工具/报告工具/.venv/bin/python 研究流程/工具/报告工具/reports.py register --id amd-update-example --project AMD --title "更新示例" --entity company:amd --type update --slug earnings-update --date 2026-11-17
研究流程/工具/报告工具/.venv/bin/python 研究流程/工具/报告工具/reports.py update --id msft-new-topic --metadata /path/to/reviewed-metadata.json
研究流程/工具/报告工具/.venv/bin/python 研究流程/工具/报告工具/reports.py archive --id msft-new-topic
研究流程/工具/报告工具/.venv/bin/python 研究流程/工具/报告工具/reports.py check
```

上方创建命令是用法示例，不要求在正式库创建示例公司/空报告。metadata是JSON对象，只填需改字段，例如`{"document_updated_at":"2026-11-17","content_status":"partial"}`，路径替换为本次实际输入文件。不得替用户或审稿人声明核验通过。资源和未发布链接可通过metadata显式补齐；ID、主体、项目、类型、路径不能借update偷偷修改。

## 4. 检查范围及 CI

check先按Schema检查，再验ID/正文路径唯一、主报告唯一、路径/类型匹配、日期格式、文件/资源存在、锚点、重复id、链接边界、外部展示依赖、未发布链接及正文哈希；通过Git盘点全库研究HTML，检测索引外的新报告（不只扫描reports目录）。factcheck、assets、skills、外部参考/独立checkout及工具/规划目录按固定规则排除，不能被登记为正文。

检查支持静态可解析的src/href/poster/srcset、CSS url及字面量fetch；动态拼接的脚本资源须人工列assets并浏览器检查，不能声称静态扫描覆盖任意JavaScript。`unpublished_links`仅用于本地来源超链接，不豁免图片、样式、图表数据等展示依赖。draft和ready均可保留这些来源链接；网站须显示不可用原因或在发布副本中禁用链接，不开放未获准文件，不能把网站404当正常来源。

`check --base-ref HEAD`默认对照HEAD防止静默删除稳定ID；CI按PR基线或push前版本对照。首次引入索引时旧基线无索引，仍执行全库漏登记扫描。校验失败非零退出，不改变研究文件。

已加入[HTML Reports工作流](../../.github/workflows/html-reports.yml)，在push和pull_request上运行工具测试与check，依赖版本固定、只读权限、不使用pull_request_target。**工作流文件不等于分支保护**：GitHub需另将`HTML report index`检查设为必需、要求PR合并并限制绕过，才能阻止不合格变更合并；本轮未改远端分支保护设置。检验工作流的权限/事件建议依据[GitHub官方安全说明](https://docs.github.com/en/actions/reference/security/secure-use)。

## 5. 既有报告的兼容与迁移

首次登记的六份HTML使用legacy路径，未批量移动正文/资源。当时公司报告保守地初始化为draft/unreviewed，并对未知日期留空；这些导入默认值不能证明作者仍在编写。后续更新以当前索引为准。须逐篇检查交付记录和实际核验范围后修正元数据，不为填充网站列表批量改成ready，也不把登记成功当事实验收。本次状态语义修订不改现有报告状态。

`move --id <id> --slug <新slug>`可将自包含专题/演示移动到标准路径（日期型更新另给--date；主报告固定main），保持正文原字节、ID和研究日期，登记老地址兼容页。浏览器允许脚本时自动携带锚点跳转；禁脚本时点击链接。兼容页由同一索引维护，不作为重复正文。

有跨文件相对依赖的报告，move会拒绝自动搬迁，避免改坏图表/证据。此类迁移须先协调生成器、相对链接、核验脚本和旧路径映射，再审阅落地；禁止简单mv后宣称完成。老报告暂留明确豁免，新报告不享有豁免。任何迁移不得借结构整理删除重要解释、改财务核验日或覆盖他人进行中的工作。

## 6. 首次落地验收记录

本轮范围为规则、索引、管理脚本和本地CI同等命令，不包含网站部署或公司事实更新。六份现有报告登记；已发现未审核附件链接保留为显式缺口。实际自动检查结果见[工具验证记录](../工具/报告工具/validation.json)，现有公司内容和并行QXO改动不因此标为完整研究验收通过。
