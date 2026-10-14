# GPU 直连 SSD 与 CMX 存储：产业推进进度、参与者与跟踪台账

> 整理日期：2026-09-16；信息截止日：2026-09-16。本文覆盖两条技术线：成熟的 **GPUDirect Storage（GDS）**，以及 2026 年发布、面向 agentic inference KV cache 的 **BlueField-4 STX / CMX**。严格区分“兼容/认证”“联合发布”“计划采用”和“已披露生产部署”。

## 结论先行

| 技术线 | 当前阶段 | 最可靠的证据 | 仍缺少什么 |
|---|---|---|---|
| GPUDirect Storage | 软件与生态已成熟，可在本地 NVMe、NVMe-oF、NFS/并行文件系统中部署 | NVIDIA 有持续更新的驱动/API、文件系统支持矩阵、Kubernetes GPU Operator 集成与认证存储清单 | 各客户实际启用比例、真实 I/O 利用率、按供应商拆分的收入规模 |
| BlueField-4 STX / CMX | 产品定义、参考架构与伙伴阵营已公布；处于首批伙伴供货/导入窗口 | 2026-03 发布；NVIDIA 称伙伴 STX 平台将在 2026 年下半年可用；列出早期采用者与制造/存储伙伴 | 公开的生产部署规模、CMX 每 POD 配置、真实 p99 延迟、KV-cache hit rate、第三方性能/ROI |

所以投资上不能把 CMX 当作已经像 GDS 一样成熟、广泛产生收入的存储标准。GDS 代表现有可验证的软件生态；CMX 代表对未来推理存储层的架构押注。

## 1. GPUDirect Storage：谁在推动，推进到哪一步

### 1.1 NVIDIA：技术标准和软件入口

NVIDIA 是 GDS 的主导方：它提供 CUDA 生态中的 cuFile（文件系统）和 cuObject（对象存储）接口、`nvidia-fs` 内核集成、GPU Operator/Network Operator 的云原生部署方式，并维护支持矩阵。GDS 的基础路径是让 NVMe、RAID 控制器或 NIC 的 DMA 引擎直接读写 GPU HBM，避免 CPU DRAM bounce buffer。

截至最新公开资料，GDS 不只是实验功能：

- 支持矩阵持续更新，包含 AWS FSx for Lustre、DDN EXAScaler、Dell PowerScale、Hammerspace、Hitachi HCSF、HPE Data Fabric/ClusterStor/GreenLake、IBM Spectrum Scale、NetApp ONTAP、Pure FlashBlade、VAST Universal Storage、WekaFS 等；
- GPU Operator 已有 GDS 的 Kubernetes 部署与网络组件说明；
- cuObject 的 1.3.0 在 2026-08 发布，说明 GDS 已从传统文件 I/O 扩展至对象存储数据路径。

这证明 GDS 的核心障碍已不是技术是否存在，而是客户是否有高 I/O、GPU 直接消费数据的工作负载，且愿意为拓扑、文件系统和应用进行优化。

### 1.2 参与者按角色划分

| 角色 | 主要公司/产品 | 证据等级与实际意义 |
|---|---|---|
| 平台与软件 | NVIDIA：CUDA、cuFile、cuObject、`nvidia-fs`、GPU Operator | **已可部署**；GDS 的标准和开发入口 |
| 并行/高性能文件系统 | DDN EXAScaler、IBM Spectrum Scale、WekaFS、VAST Universal Storage、HPE Cray ClusterStor | **支持矩阵兼容**；最贴近 AI/HPC 大吞吐训练、检查点、数据湖场景 |
| 企业 NAS/对象/文件 | Dell PowerScale、NetApp ONTAP、Pure FlashBlade、HPE GreenLake File Storage、Hitachi HCSF、Hammerspace、AWS FSx for Lustre | **支持矩阵兼容**；降低企业数据接入 GPU 的摩擦 |
| 应用/框架 | RAPIDS cuDF、DALI、MONAI、Clara Parabricks、NIXL I/O backend | **软件已启用**；决定 GDS 能否真正被工作负载调用 |
| 系统与存储硬件 | Dell、HPE、IBM、Hitachi 等；以及 NVMe/网卡/RAID 组件生态 | 有认证和参考架构，但单个节点是否形成最优 PCIe 直连仍须核验 |

“被支持”不等于每次读取都走 GDS。若应用未用 cuFile/cuObject、文件不是 `O_DIRECT`、存储/NIC 与 GPU 的 PCIe 拓扑较差，或 I/O 不是瓶颈，系统可能回退或根本不体现收益。

### 1.3 当前可观测的进展指标

| 观察项 | 去哪里看 | 说明 |
|---|---|---|
| 软件成熟度/新增兼容 | [GDS Release Notes](https://docs.nvidia.com/gpudirect-storage/release-notes/index.html) | 看支持矩阵新增的文件系统、GPU、CUDA/OS 版本 |
| 实际可部署条件 | [GDS Design Guide](https://docs.nvidia.com/gpudirect-storage/design-guide/) | 看 NVMe/NIC、PCIe switch、BAR1、文件系统等要求 |
| 云原生渗透 | [GPU Operator GDS 文档](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/26.3/gpu-operator-rdma.html) | 看 GDS 是否已进入 Kubernetes 标准部署路径 |
| 产品化程度 | [NVIDIA Certified Storage 清单](https://docs.nvidia.com/certification-programs/certified-storage/latest/systems-list.html) | 认证的 GBx00 NVL72 / DGX SuperPOD 参考架构，比单一营销合作更有价值 |
| 用户收益 | 客户案例、基准（gdsio）、GPU 利用率、CPU 使用率、p99 I/O 延迟 | 最终需要可复现项目数据；兼容矩阵本身不是营收或性能证明 |

## 2. CMX / BlueField-4 STX：谁在推动，推进到哪一步

### 2.1 时间线与成熟度判定

| 时间 | 可核对进展 | 判断 |
|---|---|---|
| 2026-03-16 | NVIDIA 发布 BlueField-4 STX 模块化存储参考架构及 CMX context memory storage 平台 | 架构与生态启动，不等于生产部署 |
| 发布时 | NVIDIA 表示 STX 伙伴平台拟在 2026 年下半年可用 | 属于供货路线图；应等待具体 SKU/交付公告 |
| 2026-09-16 | 官方 CMX/STX 产品页已展示平台、DOCA Memos SDK 与伙伴名单 | 可确认软件/产品方向；本次检索未找到公开的第三方生产规模、POD 配置或审计级性能数据 |

CMX 是 Rubin POD 中处于 GPU HBM 和通用持久存储之间的共享闪存 context tier，主要存放可复用、易失性的 KV cache。它解决的是 agentic inference 的 context 太大、重算太贵、GPU HBM 太稀缺的问题，而不是传统训练数据读取。

### 2.2 推动 CMX 的公司与各自角色

| 角色 | 公司 | 已公开的状态 | 不能据此推导 |
|---|---|---|---|
| 核心平台 | NVIDIA | BlueField-4 STX、CMX、Vera/Rubin、ConnectX-9、Spectrum-X、DOCA/AI Enterprise | NVIDIA 已独立建成并运营所有 CMX 容量 |
| 存储与数据平台伙伴 | Cloudian、DDN、Dell、Everpure、Hitachi Vantara、HPE、IBM、MinIO、NetApp、Nutanix、VAST Data、WEKA | NVIDIA 称其参与基于 STX 的架构/基础设施共设计 | 每家都有公开可购买的 CMX SKU 或已上生产 |
| 制造伙伴 | AIC、Supermicro、QCT | NVIDIA 称其制造 STX 系统 | 已产生可量化出货量 |
| 早期采用者/潜在运营者 | CoreWeave、Crusoe、IREN、Lambda、Mistral AI、Nebius、Oracle Cloud Infrastructure、Vultr | NVIDIA 表述为 early adopters / planning to adopt | 已完成大规模 CMX 部署或有可审计容量 |
| 网络/系统生态 | Spectrum-X、DOCA、NVIDIA AI Enterprise；另有 OEM 与存储软件参与 | 必须协同才能把 KV cache 在 POD 范围共享 | 单一 SSD 厂商即可交付完整系统 |

重要缺口：截至本次检索，NVIDIA 公共资料没有披露 CMX 的闪存/NAND 供应商、每个 STX 机柜的 SSD 数量、每 POD 的 CMX 规模或单家伙伴的实际采购额。因此不能把 CMX 宣布直接映射到某一 SSD 制造商的订单。

### 2.3 CMX 软件面出现的积极信号

NVIDIA 的 CMX 产品页已把 **DOCA Memos** 描述为 BlueField-4/CMX 优化的 SDK：它以 key-value API 管理和共享 KV cache，将以太网连接的闪存变为 POD 级缓存层。这个信号很关键：CMX 不是只卖硬件机柜，而是在尝试将 KV cache 的放置、复用、生命周期和隔离抽象成软件接口。

但截至目前，公开资料仍未展示大量独立开发者的 API 文档、开源实现、第三方 benchmark 或客户级 SLA。软件可用性、存储软件伙伴的适配程度和推理框架的实际接入速度，是 CMX 商业化的最大不确定性之一。

### 2.4 CMX 应在哪些地方持续跟踪

| 需要验证的事件 | 首选来源 | 强度 |
|---|---|---|
| STX/CMX 的可购 SKU、规格、价格与交付时间 | AIC、Supermicro、QCT 及存储伙伴的产品页/新闻稿 | 强：从路线图转为产品化 |
| 哪个云实际提供 CMX 或 context-memory 服务 | CoreWeave、Nebius、OCI、Lambda 等服务目录、技术文档和状态页 | 强：从“计划采用”转为服务可用 |
| 实际硬件和软件组合 | NVIDIA CMX/STX 产品页、DOCA release notes、伙伴架构文档 | 中：证明技术栈是否落地 |
| 性能经济性 | 客户案例的 p99 context fetch latency、KV-cache hit rate、GPU idle time、token/s、token/$ 和 token/MW | 最强：验证商业价值 |
| 真实采购与资本开支 | 云厂商 10-Q/年报/业绩会、存储公司业绩会与订单披露 | 最强：验证收入与需求 |
| 系统兼容度 | NVIDIA Certified Storage、NVIDIA Cloud Partner 认证 | 中强：比合作名单更接近可销售产品 |

## 3. 谁真正“领先”：需要按问题，而非按公司名称判断

### GDS：DDN / Weka / VAST / IBM / NetApp 等是已验证生态，而非同一赛道的同质竞争者

这些公司都在 NVIDIA 支持矩阵中，但产品侧重点不同：并行文件系统更适合 HPC/训练吞吐，企业 NAS/对象平台更适合现有数据和 RAG 接入，AI 数据平台则强调数据治理和推理工作流。对用户来说关键不是“哪家有 GDS 徽章”，而是文件系统、网卡、GPU PCIe 拓扑和应用框架能否形成直接路径。

### CMX：NVIDIA 领先的是架构整合；云厂商和存储软件商决定能否变成规模业务

NVIDIA 处于最核心位置，因为它同时拥有 Rubin GPU、BlueField-4、ConnectX-9、Spectrum-X、DOCA 和推理生态。可是 CMX 是否成功，取决于三类外部参与者：

1. 云厂商/AI 实验室是否提供长上下文、多 agent 推理并愿为 shared KV cache 付费；
2. 存储商能否把 STX/CMX 融进其数据管理、可靠性、多租户与客户支持体系；
3. OEM 是否能按时交付含闪存、DPU、网络、供电散热的完整机柜。

目前最合理的结论是“生态阵营已形成、首批采用者已点名”，而非“某一家已经赢得 CMX 市场”。

## 4. 对 NVDA 与 SSD 产业链研究的含义

- **短期（可验证）**：GDS 的受益更偏向 GPU、NIC/DPU、企业/并行文件系统、NVMe-oF 和能够提供认证系统的供应商；它是软件与系统集成能力，不直接保证 NAND bit 需求激增。
- **中期（选择权）**：CMX 若落地，会增加高性能、低延迟闪存、DPU、800G 网络和存储软件在推理 POD 中的内容价值，且需求与训练数据存储不同，更多由 KV cache 容量、复用率和 latency SLA 决定。
- **风险**：KV cache 可能继续通过 HBM 扩容、CPU DRAM、CXL 内存、模型压缩/量化、软件 paging 或客户自研方案解决；CMX 未必成为唯一标准。更高效的模型也可能减少每 token 的 context 存储需求。
- **最重要的避免项**：不要把 “up to 5× token/s” 或 “early adopter” 当作量产订单，不要把 CMX 等同于某一家 NAND 厂的已确认订单。

## 5. 资料来源

1. **NVIDIA GDS Release Notes**：支持矩阵及应用/框架支持。[Release Notes](https://docs.nvidia.com/gpudirect-storage/release-notes/index.html)
2. **NVIDIA GDS 设计/概览文档**：GDS 的 DMA、PCIe、NVMe/NIC、`O_DIRECT` 和软件条件。[设计指南](https://docs.nvidia.com/gpudirect-storage/design-guide/)；[概览](https://docs.nvidia.com/gpudirect-storage/overview-guide/)
3. **NVIDIA Certified Storage**：面向 GBx00 NVL72、DGX SuperPOD 和云伙伴的认证系统。[认证清单](https://docs.nvidia.com/certification-programs/certified-storage/latest/systems-list.html)
4. **NVIDIA STX 发布稿**：发布日期、伙伴分类、早期采用者名单和“下半年可用”的前瞻表述。[发布稿](https://nvidianews.nvidia.com/news/nvidia-launches-bluefield-4-stx-storage-architecture-with-broad-industry-adoption)
5. **NVIDIA CMX 产品页**：CMX 的 POD 级 context tier 与 DOCA Memos 说明。[CMX](https://www.nvidia.com/en-us/data-center/ai-storage/cmx/)
6. **NVIDIA AI Storage 生态页**：更广泛的 AI 存储伙伴名单，名单不代表全部采用 CMX。[生态页](https://www.nvidia.com/en-eu/data-center/ai-storage/)
