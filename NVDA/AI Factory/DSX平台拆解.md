# NVIDIA DSX 平台拆解：从参考设计到电网—GPU 控制回路

> 整理日期：2026-09-16；信息截止日：2026-09-16。技术事实主要来自 NVIDIA 官方 DSX 产品页和文档。性能数字均为 NVIDIA 的产品声明或示例，不作为独立验证后的项目结果。

## 结论先行

DSX 不是一套单独出售、包办数据中心全部功能的“超级操作系统”。它是 NVIDIA 把既有 GPU、网络、Kubernetes 软件与新增加的设施工程、电力和运维接口组合成的**AI Factory 参考架构与控制框架**。

它实际要解决的不是“怎样多装几张 GPU”这样单点问题，而是：在既定的土地、电力、机房和冷却约束下，怎样从设计阶段到运行阶段都提高每 MW 的 token 产出，并缩短从开工到可收费推理服务的时间。

对 NVIDIA 最有战略价值的组件是 DSX Exchange + MaxLPS + Flex：前者将楼宇、电力、冷却和计算数据接入同一消息层；后两者据此调节 GPU/机柜/工作负载功耗并响应电网信号。若被广泛采用，DSX 会令客户的物理设施和运行流程围绕 NVIDIA 的接口、硬件与软件共同设计；但它不拥有电网、机房或客户的云平台，也不能保证获得额外并网容量。

## 1. DSX 的边界：它是什么，不是什么

| 是 | 不是 |
|---|---|
| 面向 AI Factory 的参考设计、软件组件、API、工作流和伙伴接口集合 | 一个单一安装包或传统意义上完全替代客户 IT 系统的操作系统 |
| 把芯片、网络、存储、机房、电力、冷却和运维作为一个系统共同优化 | NVIDIA 自己建设并拥有全部数据中心、输电和发电资产 |
| 以最低 token 成本、token/MW、投产速度和稳定性为 KPI | 对客户收入、GPU 利用率、并网许可或电价的保证 |
| 供云厂商、主权云、LPS 供应商、OEM、系统集成商、工程公司和设施软件商共同使用的接口框架 | 只服务 NVIDIA 自建云或 OpenAI 一类单一客户 |

传统数据中心通常把 IT（服务器/网络）与 OT（电力、制冷、楼宇管理）分开购买、分开运行。DSX 的核心主张是两者必须共同设计和共同调度，因为 AI 集群的功耗密度、液冷和推理负载会使其中任意一层成为全项目的约束。

## 2. 一个 AI Factory 在 DSX 下怎样从“图纸”走到“出 token”

```text
① 规划、选址和工程设计
   DSX Reference Design + 设施参考设计
             ↓
② 建设前仿真
   DSX Sim / Omniverse DSX Blueprint：数字孪生、容量和故障情景验证
             ↓
③ 上架与集群 bring-up
   GPU / Network Operator、NICo、Cluster Readiness、Rack Management
             ↓
④ 生产运行
   KAI / Run:ai / Dynamo 等：调度、推理服务、多租户和故障恢复
             ↕
⑤ 设施与能源实时控制
   DSX Exchange（IT/OT 事件总线）→ MaxLPS（功率优化）→ Flex（电网响应）
             ↓
目标：固定 MW、机房和资本支出下的更多 token、较短投产期和更高可用性
```

这条链条也说明 NVIDIA 的介入边界：①—③主要影响工程标准与上架速度；④影响集群的软件运行；⑤才开始触及电力和设施调度。土地、电力合同、施工、变电站、冷却设备和客户业务负载仍由不同业主与供应商承担。

## 3. 六个组件的具体功能

### 3.1 DSX Reference Design：从 chip 到 grid 的工程“蓝图”

它是按 GPU 平台代际更新的验证架构，覆盖：

- 计算、网络、存储和硬件集群拓扑；
- 园区设施，包括变电、配电、冷却、控制系统，以及土建、结构和建筑设计；
- 接口与性能假设，使 OEM、机房、冷却、电气设备和软件厂商不用从零做一对一适配。

实际含义：NVIDIA 不只给客户 NVL72 等计算规格，也试图把“怎样建支持它的机房”一并规定下来。参考设计不是强制标准，客户可以改动；但按其验证架构施工，出故障时责任界面更清晰、投产风险更低，因此会提升采用 NVIDIA 全栈方案的概率。

### 3.2 DSX Sim：在建厂前先建一座数字工厂

DSX Sim 是仿真工具集合，包含三类东西：

1. **DSX Air**：对 GPU、SuperNIC、DPU、交换机及已验证伙伴软件的逻辑基础设施仿真；
2. **Omniverse DSX Blueprint**：针对 GW 级 AI Factory 的端到端数字孪生框架；
3. **SimReady 资产和流程样例**：将 CAD、设备元数据和硬件配置转成可验证模型。

它能用于在购买、施工和上架前验证机柜密度、网络拓扑、功耗、散热和流程的交叉权衡；建成后比较预期和实际运行。它不能证明电力一定拿得到，也不能取代专业工程师对施工、消防、并网和安全的签字。

### 3.3 DSX OS：不是一个“OS”，而是一组云原生运行组件

DSX OS 的公开定位是开源、模块化的 AI Factory 运营软件。其实际组成可分两层：

| 层级 | 组件示例 | 在做什么 |
|---|---|---|
| 工作负载与推理 | KAI Scheduler、Run:ai、NVCF、Grove、Dynamo | 拓扑感知调度、GPU 资源分配、多集群推理扩缩容、分布式推理服务 |
| 集群与设施运维 | GPU Operator、Network Operator、Topograph、NICo、NVSentinel、Cluster Readiness、Rack Management Service | 裸机配置、GPU/网络驱动管理、物理拓扑发现、故障检测和修复、机柜级电源/固件/交换机管理 |

这意味着 DSX OS 更像 NVIDIA 将一批 Kubernetes、GPU、网络、集群健康和推理组件封装成经过验证的运行栈。它有助于多租户 AI 云提高 GPU 利用率，但不会替代客户的 Kubernetes、账单、身份、模型治理或所有应用层软件。

### 3.4 DSX MaxLPS：在固定 MW 内榨出更多有效算力

MaxLPS 的全称对应 “Maximum Land, Power, Shell” 的约束优化。它不创造新的 MW，而是减少已获 MW 在保守预留、闲置功耗、冷却余量和静态分配中的浪费。

可把它理解为三个层次：

| 模式/能力 | 决策层级 | 逻辑 |
|---|---|---|
| MaxP | 单 GPU 静态功率 | 以最高性能功率设置作为机柜和行级供电/冷却设计基准 |
| MaxQ | 单 GPU 静态功率 | 追求较佳应用性能/瓦，而非最高绝对功率 |
| MaxLPS | 全厂动态功率 | 将设施、冷却、GPU、机柜和工作负载一起考虑，回收未用功率并动态分配 |

NVIDIA 的示例称，在固定 1MW、PUE 1.1 的 Vera Rubin NVL72 推理场景中，MaxLPS 可配置 400 张 GPU、token 吞吐为 MaxP 的 1.35 倍；公司也宣传在相同园区功率包络下“最多多部署 40% GPU”。这只是**尚在测试中的说明性推理场景**，实现前提包括从设计时就支持 45°C 液冷、具有合适的负载结构和可调度的功率余量，不能外推为所有训练集群或所有项目的 40% 增量。

### 3.5 DSX Exchange：最关键的 IT/OT 数据层

DSX Exchange 是一个 IT/OT 通信与集成层，技术上采用 NATS 事件总线，提供 MQTT 3.1.1 兼容、JetStream 持久化和跨集群 federation。选 MQTT 3.1.1 是为兼容既有楼宇管理系统（BMS）和工业 OT 设备，而不是要求它们完全换成 NVIDIA 专有控制器。

它让以下实际信号路径成为可能：

```text
BMS 电力遥测 ──> Dynamic Power Software ──> GPU/机柜功率重新分配
BMS 冷却液泄漏 ──> NICo ──> 隔离节点、迁移工作负载
电网需求响应信号 ──> DSX Flex ──> 调度器削减/移动负载
GPU 温度遥测 ──> 热管理代理 ──> 提前调整冷却设定点
```

这才是 DSX 可能变成“工厂控制平面”的原因：它试图规定来自 BMS、电网、冷却和 GPU 的信号怎样被解释、传递和反馈。但它需要工程集成商把 BMS 接入事件总线，且实际执行权仍受客户的安全策略、调度器、设备兼容性和电网协议限制。

### 3.6 DSX Flex：让 AI Factory 成为可调节负载

Flex 是面向电网的编排层：接收限电、需求响应和电价信号，协调电网电力、现场可再生能源和储能，并要求调度层改变工作负载。它的商业意义是降低电网和地方政府对“AI 数据中心是不可控大负荷”的顾虑：在尖峰时段，部分可延后的推理/训练工作可以降载或转移。

但是，Flex 不会消除客户的 SLA 约束，也不能使没有输电、发电或储能的园区凭空得到电力。其价值要由真实项目中“降载响应速度、对 token 生产的影响、为项目换得的并网容量/电价条件”来验证。

## 4. DSX 的商业化处在什么阶段

### 已可确认

- Omniverse DSX Blueprint 已一般可用；
- NVIDIA 已发布公开文档、GitHub 组件和 DSX Marketplace 的验证路径；
- CoreWeave、Crusoe、Firmus、IREN、Lambda、Nebius、Nscale、Yotta 等 NVIDIA 云伙伴被公司列为部署 DSX Sim、MaxLPS、DSX OS 核心组件的伙伴；
- Emerald AI、Silicon Valley Power 的多 MW 电网响应试点，是 DSX Flex 的具体商业试点。

### 仍需谨慎

- 参考设计的部分详细材料需要 NVOnline 权限，外部无法完整核对全部工程参数和客户部署规模；
- Dynamic Power Software 的文档说明其只面向经批准的早期预览合作；
- “40% 更多 GPU / 1.35 倍 token”是厂商说明性场景，不是客户可审计的普遍结果；
- 公司列出伙伴采用某些组件，不等于这些伙伴全园区、全部项目均按 DSX 完整部署。

## 5. DSX 对 NVIDIA 的战略价值与风险

| 价值 | 机制 | 风险/反证 |
|---|---|---|
| 提高系统份额 | 用设施标准将 GPU、网络、冷却和软件绑定在同一交付方案 | 客户可能只采用参考设计的一部分，或转用开放标准/竞争对手方案 |
| 更快投产 | 预仿真、验证架构和标准运维缩短集成与排错 | 项目仍可能卡在许可、变电站、施工和供应链 |
| 提高每 MW 收入 | 在相同已获电力下容纳更多 GPU / token | 需要特定推理负载、冷却和功率控制条件；非线性收益不保证 |
| 形成运行数据与接口黏性 | 连接 BMS、GPU、网络、调度和电网信号 | 数据主权、网络安全和客户自有控制平面可能限制接入深度 |
| 帮助融资/并网 | 可将 AI Factory 设计成更高效、可响应的负荷 | 实际金融信用和电网审批仍由资本方、监管者和公用事业决定 |

## 6. 研究时应追踪的具体问题

1. 哪些 AI 云仅采用 DSX OS，哪些已部署 Exchange、MaxLPS 与 Flex？后者才代表 NVIDIA 进入设施和电网接口。
2. Flex 试点能否披露削峰容量、响应速度、项目因此增加的接电容量，以及对客户 SLA/收入的影响？
3. MaxLPS 的“更多 GPU/每 MW”能否在第三方项目中复现，且是否适用于训练与推理的混合负载？
4. DSX Marketplace 的验证产品、实际安装量和运营软件附着率是否增长？
5. DSX 是否提高 NVIDIA 网络、软件和机柜内容价值，或只是免费参考架构来促进 GPU 销售？

## 来源

1. **NVIDIA DSX 产品页**：平台定义、六大组件、目标和适用客户。[产品页](https://www.nvidia.com/en-us/data-center/products/dsx/)
2. **NVIDIA DSX 文档**：组件、DSX OS 的具体运行模块、Exchange/Flex 的接口和部署信息。[文档首页](https://docs.nvidia.com/dsx)
3. **DSX MaxLPS 文档**：固定 MW 的设计逻辑、MaxP/MaxQ/MaxLPS 区分及说明性性能情景。[MaxLPS](https://docs.nvidia.com/dsx/maxlps/overview)
4. **DSX Exchange 架构文档**：NATS/MQTT、BMS 集成及四类实际信号路径。[Exchange 架构](https://docs.nvidia.com/dsx-exchange/architecture)
5. **NVIDIA DSX 发布稿**：参考设计、生态伙伴、云伙伴组件采用与 Flex 多 MW 试点。[发布稿](https://nvidianews.nvidia.com/news/dsx-infrastructure-ai-factory)
