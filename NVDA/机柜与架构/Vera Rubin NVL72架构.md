# NVIDIA 下一代机柜架构：Vera Rubin NVL72 全拆解

> 整理日期：2026-09-16；信息截止日：2026-09-16。本文的“下一代机柜”指相对 GB200/GB300 NVL72 的 **Vera Rubin NVL72**。官方产品页仍标注部分规格为 preliminary，性能和能效提升均为 NVIDIA 主张，量产客户数据尚待验证。

## 结论先行

Vera Rubin NVL72 的重点不是把 72 变成更多 GPU——它仍是 **72 Rubin GPU + 36 Vera CPU** 的单机柜计算域——而是把这 72 GPU 做成更高速、更易部署、更适合高密度推理的“一个大 GPU”。

相对 Blackwell NVL72，架构变化有五个：

1. **NVLink 6 规模升级**：72 张 GPU 继续全互连，但单 GPU scale-up 带宽升至 3.6TB/s、整柜 260TB/s，面向 MoE、长上下文和 agentic inference 的频繁 all-to-all 通信。
2. **计算托盘重做**：18 个计算托盘，每托盘 4 GPU、2 CPU、8 个 ConnectX-9 SuperNIC 和 1 个 BlueField-4 DPU；内部采用 PCB 中板，变成无内部线缆、无软管、无风扇的可维护模块。
3. **第三代 MGX 机柜**：四个预集成铜缆盒构成 rack spine；计算托盘、NVLink 交换托盘、电力和液冷均模块化，可在不停整柜的条件下维修部分交换托盘。
4. **电力/热设计进入芯片架构**：45°C 温水液冷、液冷母排、机柜级储能与 Intelligent Power Smoothing，将短时功率尖峰从电网侧“抹平”。
5. **外部网络与安全重新配置**：ConnectX-9 负责 scale-out，BlueField-4 负责基础设施卸载、安全、隔离与上下文存储平台；因此机柜不只是 GPU—CPU 组合，而是一个网络、安全与运营能力都预集成的执行域。

## 1. 先分清三个层级：GPU、机柜、POD

```text
Rubin GPU / Vera CPU / ConnectX-9 / BlueField-4 / NVLink 6
                         ↓
Vera Rubin NVL72：1 个机柜、72 GPU 的 scale-up 域
                         ↓
Vera Rubin POD：多种专用机柜组成的 AI 超级计算机
                         ↓
Vera Rubin Ultra NVL576：8 个 NVL72 类机柜、576 GPU 的跨机柜 scale-up 域（后续产品）
```

NVL72 是核心计算机柜，不能与整个 POD 混为一谈。POD 还可以加入低延迟推理用的 Groq 3 LPX 机柜、Vera CPU 机柜、BlueField-4 STX/上下文存储机柜和 Spectrum-X 网络机柜。NVL576 则是之后的跨八柜 NVLink 扩展，不是当前 NVL72 单柜的内部结构。

## 2. 单柜硬件结构

### 2.1 计算与交换托盘

| 模块 | 数量 | 每个模块的内容 | 作用 |
|---|---:|---|---|
| 计算托盘 | 18 | 2 个 Vera Rubin superchip = 2 Vera CPU + 4 Rubin GPU；8 个 ConnectX-9 SuperNIC；1 个 BlueField-4 DPU | 18 × 4 = 72 GPU、18 × 2 = 36 CPU；提供计算与向机柜外扩展网络的接口 |
| NVLink 交换托盘 | 9 | NVLink 6 交换芯片与管理/维护功能 | 将全柜 72 GPU 接成一个 all-to-all 的 scale-up 域 |
| 铜缆 spine | 最多 4 个模块化盒 | 约 5,000 条铜缆，整柜约两英里铜缆长度 | 把计算与交换托盘在机柜背部预集成连接 |
| 网络与基础设施 | 集成于计算托盘 | ConnectX-9 + BlueField-4 | 分别处理大规模 scale-out、网络/存储/安全与基础设施卸载 |

因此 NVL72 不是 72 台独立服务器堆在一个柜内：从 GPU scale-up 的角度看，它更接近一个拥有 72 加速器的大型共享计算域。托盘仍是可替换的物理模块，而不是整柜报废后才可维修。

### 2.2 核心硅片与存储层次

- **Rubin GPU**：官方资料称每 GPU 配备 HBM4；产品页披露整柜 GPU 内存 20.7TB，约合每 GPU 288GB。HBM4 的目的不仅是提高模型规模，也针对长上下文和推理时 KV cache 的带宽压力。
- **Vera CPU**：36 颗 CPU，官方称每颗拥有 88 个自研 Olympus 核，使用 Armv9.2 兼容架构，并以 NVLink-C2C 与 GPU 紧耦合。CPU 在 agentic 工作负载中承担编排、工具调用、沙箱和数据预处理等非纯 GPU 任务。
- **NVLink 6**：机柜内的 scale-up fabric，官方称每 GPU 3.6TB/s、整柜合计 260TB/s。它解决的是 GPU 间高频交换，并不等同于机柜到机柜的以太网/InfiniBand 网络。
- **ConnectX-9**：用于 scale-out 网络。NVL72 产品页列出超过 144 个单端口 800Gb/s ConnectX-9 VPI 接口；按每个计算托盘 8 个接口理解，18 个托盘共 144 个。
- **BlueField-4**：每托盘 1 个、共 18 个。它将网络、存储、安全和基础设施服务从主机 CPU/GPU 上卸载。需要区分：POD 级 CMX 上下文存储由**独立的 BlueField-4 STX 存储机柜**承载，并非这 18 个计算托盘 DPU 本身就构成 CMX；详见 [`GDS与CMX技术.md`](../存储与CMX/GDS与CMX技术.md)。

## 3. 真正的架构变化：从“服务器机柜”变成“机柜级计算机”

### 3.1 NVLink 6 的含义

GB300 NVL72 已能通过 NVLink 把 72 GPU 形成单域；Rubin 沿用单柜 72 GPU 的形态，但把网络带宽和适用场景显著推进。官方将其定位为针对四类扩展规律：预训练、后训练、test-time scaling、agentic scaling。

这在工程上尤其服务于两类负载：

1. **MoE 路由**：每个 token 可能要在专家之间跨 GPU 传递激活值；GPU 间带宽和延迟会直接影响吞吐。
2. **长上下文/多步推理**：模型推理不会只生成一个短答案，而是反复检索、调用工具、写入或读取 context；CPU、GPU、网络和 KV cache 都需持续协作。

因此 NVIDIA 不只用“峰值 FLOPS”销售 Rubin，而试图以 token cost、token/MW 与 agentic workload 的持续吞吐来定义性能。

### 3.2 机柜机械与维修结构

第三代 MGX 的重要但容易忽略的变化是机械工程：单宽 19 英寸机柜中，托盘用 PCB 中板连接，计算与 NVLink 托盘宣称无内部线缆、无软管、无风扇。大量原本需要人工插接的连接被转移到预验证的机柜 spine。

NVIDIA 的技术博客称，这使计算托盘组装从接近两小时降至约五分钟；这是厂商描述的组装/服务时间，不是客户端实际整机交付周期。架构上的实质收益是减少人工布线、冷却接头和风扇等故障/装配点，并让托盘和部分交换托盘可模块化更换。

### 3.3 电力：从静态“最大功率预留”转为动态功率包络

Rubin 机柜采用两层策略：

- **Dynamic power steering**：在 CPU、GPU 与 NVLink 交换托盘之间，随负载把可用功率给更需要的组件；
- **Intelligent Power Smoothing**：机柜内电容储能在负载突发时供电、负载骤降时充电，平缓上游电网看到的功率变化。

官方称 Rubin NVL72 的机柜级储能较前代增加 6 倍，达到每 GPU 400J，并可将峰值电流需求最多降低 25%。这不是降低总耗电量的魔法，而是降低短时尖峰与静态冗余预留，使同一园区电力预算可以容纳更多有效 IT 负载。

### 3.4 冷却：45°C 温水和液冷母排

NVL72 以液冷为前提。第三代 MGX 采用内部托盘歧管、UQD08 机柜歧管和可支持 5,000A 的液冷母排；设计为可使用 45°C 入水温度。较高的入水温度有利于在许多气候下使用干冷器/自由冷却，减少压缩机制冷占用的园区功率。

NVIDIA 估计这可在相同园区功率预算中增加最多 10% 的 Vera Rubin NVL72 机柜。这个数字取决于气候、原有冷却设计、负载曲线、PUE 和机房条件；不能将其当作所有数据中心的确定 CAPEX 回报。

### 3.5 功率密度：设施已成为机柜的一部分

DSX 设施参考架构显示，Vera Rubin NVL72 的 cabinet TDP 可至 330kW，而此前 MGX Gen 1.1 约 198kW。这说明客户购买 Rubin 不只是升级服务器：变电、配电、CDU、管路、热排放、机房结构和安全运维都会随之升级。

所以“可插入现有数据中心 footprint”需要谨慎理解：机柜占地可能保持可兼容，但**拥有适配的电力、液冷和网络设施**才是前提。缺少这些条件的传统机房并不能直接接入 330kW 级机柜。

### 3.6 “GPU 直连内存”具体体现在哪里

这个说法容易混淆。它至少包含四条完全不同的路径：

| 路径 | Rubin NVL72 中的位置 | 是否经过 CPU 内存 | 解决的问题 |
|---|---|---|---|
| GPU 本地 HBM | 每张 Rubin GPU 封装旁的 HBM4 | 否 | GPU 核心读写模型权重、激活值和 KV cache |
| GPU ↔ GPU peer memory | NVLink 6 + 9 个交换托盘 | 否 | 柜内 72 GPU 间的张量、激活值和专家路由交换 |
| NIC ↔ GPU memory | ConnectX-9（按部署启用 GPUDirect RDMA） | 数据面不经过；CPU仍参与控制面 | 跨机柜 RDMA、KV cache 与张量传输 |
| Storage ↔ GPU memory | NVMe/NVMe-oF/远端存储，经 GPUDirect Storage（GDS） | 数据面不经过；CPU仍发起/管理 I/O | 模型、检查点、数据或上下文读入时避免 CPU bounce buffer |

**第一层：本地 HBM4，才是最字面的“GPU 直连内存”。** Rubin GPU 的 HBM4 直接服务 GPU 内存控制器，官方资料称每 GPU 288GB、带宽最高 22TB/s；整柜为 20.7TB。它是 GPU 的本地显存，并不是 CPU DIMM，也不是可被 72 张 GPU 无代价共享的统一 DRAM。

**第二层：NVLink 6 让 GPU 直接访问其他 GPU 的显存。** 柜内 72 GPU 通过 NVLink 6 形成 scale-up 域。此时 MoE 路由或模型分片所需的数据可以在 GPU 间走 NVLink，而不必先复制到 CPU 内存再转发。需要强调：软件仍需处理张量切分、通信和一致性；NVLink 高带宽不意味着所有 GPU 显存自动变成一块没有延迟差别的共享内存。

**第三层：GPUDirect RDMA 是 NIC 直达 GPU 显存。** ConnectX-9 是这条路径的硬件基础之一。GPUDirect RDMA 允许支持它的 NIC/DPU 用 DMA 直接读写 GPU 显存，避免“NIC → CPU 内存 → GPU 显存”的两段复制。它尤其适合跨节点的 KV cache 迁移、分离式 prefill/decode 和多机柜训练通信；但需要 RDMA 网络、正确 PCIe/拓扑、驱动、CUDA 内存注册和工作负载软件支持，不能从“机柜配置了 ConnectX-9”直接推断每个客户都已启用。

**第四层：GPUDirect Storage 是存储直达 GPU 显存。** 本地 NVMe 或远端 NVMe-oF/NFS 等存储可通过 DMA 将数据直接送入 GPU 内存，绕开 CPU 内存 bounce buffer。它适合 I/O 真正在关键路径上的模型加载、检查点、数据流或上下文读取；需要 cuFile 等显式 API、合适文件系统/设备拓扑以及固定（pinned）GPU 缓冲区。若应用本身必须由 CPU 解码或处理数据，GDS 并不会带来这条路径的收益。

可把“没有 GPU Direct”与“有 GPU Direct”的差异理解为：

```text
传统跨节点路径：GPU A → CPU 内存 → NIC → 网络 → NIC → CPU 内存 → GPU B
GPUDirect RDMA： GPU A 显存 ↔ NIC → 网络 → NIC ↔ GPU B 显存

传统读存储路径：存储 → CPU 内存 bounce buffer → GPU 显存
GPUDirect Storage：存储 / 存储侧 NIC → GPU 显存
```

Vera CPU 与 Rubin GPU 之间的 NVLink-C2C 则是另一条直接互连路径，主要用于 CPU—GPU 紧耦合；它不应与 HBM4、GPU 间 NVLink peer memory 或 GPUDirect RDMA 混为同一个概念。BlueField-4 和更大 POD 的 Context Memory Storage 平台能帮助上下文存储、隔离和基础设施卸载，但它们也不等于把外部存储自动变成 GPU 本地 HBM。

## 4. 机柜内、机柜外网络分别干什么

| 网络层 | 主要元件 | 解决的问题 | 不应混淆为 |
|---|---|---|---|
| Scale-up（柜内） | NVLink 6 + 9 个交换托盘 | 72 GPU 作为一个共享计算/内存域，处理高频 all-to-all 通信 | 普通以太网交换网络 |
| Scale-out（柜外） | ConnectX-9 + InfiniBand / Ethernet | 多机柜训练、推理、存储和集群扩展 | NVLink 单柜带宽 |
| 基础设施/安全 | BlueField-4、管理网络、Mission Control | 隔离、供应、网络/存储卸载、运行与故障管理；CMX 则由独立 STX 存储机柜提供 | 应用模型的业务逻辑 |

这三层分离非常重要：即使单柜已有 72 GPU 的高速 NVLink，成千上万 GPU 的 AI Factory 仍需要高速以太网或 InfiniBand。NVIDIA 因此把 ConnectX、BlueField、Spectrum-X、Mission Control 和 DSX 一同打包，而不是只卖 NVLink 机柜。

## 5. 和 Blackwell NVL72 的可核对对比

| 维度 | GB300 NVL72（当前/前代） | Vera Rubin NVL72（下一代） | 对客户的含义 |
|---|---|---|---|
| 计算规模 | 72 B300 GPU + 36 Grace CPU | 72 Rubin GPU + 36 Vera CPU | GPU 数不变，单 GPU、CPU 与内存代际升级 |
| 计算托盘 | 18 托盘，每托盘 4 GPU、2 CPU | 18 托盘，每托盘 4 GPU、2 CPU | 维持模块化单柜规模，减少扩容改变 |
| GPU 内存 | 前代为 HBM3e 系列 | 整柜 20.7TB HBM4，约 288GB/GPU | 更适配大型模型、长上下文与推理 KV cache |
| 柜内互连 | NVLink 5 | NVLink 6，3.6TB/s/GPU、260TB/s/柜 | 强化 MoE 和高并行推理通信 |
| scale-out 网卡 | ConnectX-8 | ConnectX-9，官方列 >144 × 800Gb/s 接口 | 更高外部网络吞吐与更低拥塞风险 |
| DPU | BlueField-3 | BlueField-4 | 设施/安全/存储卸载与多租户能力升级 |
| 机柜结构 | 早代 MGX/NVL 架构 | 第三代 MGX，预集成铜缆 spine、无内部线缆/软管/风扇托盘 | 缩短装配与维护时间，降低现场集成复杂度 |
| 电力与热 | 液冷、高功率机柜 | 45°C 温水、液冷母排、功率平滑/动态分配 | 需要更高等级设施，但可提高每 MW 有效产出 |

表中的性能提升不宜直接与 GB300 逐项相减：NVIDIA 对 Rubin 的“最高 4 倍训练、最高 10 倍推理能效”等说法依赖精度、模型、负载和软件版本；没有公开的完整第三方同条件机柜级基准可据此确认。

## 6. 下一步产品路线：不要把它们误当成当前单柜规格

| 名称 | 规模 | 架构关系 | 状态/意义 |
|---|---:|---|---|
| Vera Rubin NVL72 | 72 GPU / 柜 | 当前下一代单机柜核心 | 官方称 2026 年下半年伙伴可用；产品页仍称部分规格 preliminary |
| Vera Rubin Ultra NVL576 | 576 GPU / 8 柜 | 两层 all-to-all NVLink，铜缆加直连光学 | 后续跨机柜 scale-up 产品；非 NVL72 当前内部结构 |
| Kyber NVL144 | 144 GPU / 柜 | 为 Feynman 时代规划的更大单柜 NVLink 域 | 更远期设计，不应计入 Rubin 当期交付或供应链模型 |

## 7. 对 NVIDIA 与供应链研究的含义

### 对 NVIDIA

- 机柜从产品包装变为性能、能效、服务和生态锁定的单位；GPU 份额之外，网络、DPU、软件、液冷与工程参考设计的内容价值提高。
- 单柜集成度提高，客户迁移到替代加速器时不只替换 GPU，还需重做网络、功率、冷却与管理栈，转换成本上升。
- 反面是收入确认更依赖电力、液冷、机房施工和系统集成进度；这与 NVIDIA 介入 LPS/AI Factory 融资的原因一致。

### 对产业链

最受约束、也最值得观察的并非只有 GPU：HBM4、先进封装、NVLink 交换、ConnectX-9/BlueField-4、铜缆/光模块、冷板/CDU、液冷歧管和 330kW 级配电都变为交付关键点。机柜越集成，任何一个非 GPU 零件延迟都更可能延后整柜出货。

## 8. 资料来源与证据边界

1. **NVIDIA Vera Rubin NVL72 产品页**：72 GPU/36 CPU、内存、网络、NVLink、软件；页面明确标注规格为 preliminary。[产品页](https://www.nvidia.com/en-eu/data-center/dgx-vera-rubin-nvl72/)
2. **NVIDIA 技术博客《Vera Rubin POD》**：托盘、spine、供电、液冷、模块化服务、路线图；为厂商技术材料。[技术拆解](https://developer.nvidia.com/blog/?p=113993)
3. **NVIDIA DSX 设施参考架构**：330kW cabinet TDP、液冷和 Scalable Unit 的设施侧要求。[设施架构](https://docs.nvidia.com/dsx/facilities-infra/reference-design-overview)
4. **NVIDIA Rubin 平台新闻材料**：CPU/GPU、ConnectX-9、BlueField-4、合作伙伴与可用时间。[平台资料](https://nvidianews.nvidia.com/_gallery/download_pdf/695c39b23d633240d175d8e6/)
5. **GB300 NVL72 企业参考架构**：前代 18 托盘/72 GPU 结构，用于对比，不作为 Rubin 规格来源。[GB300 架构](https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/components.html)
6. **NVIDIA GPUDirect 官方文档**：RDMA 与 Storage 绕开 CPU bounce buffer 的条件、软件依赖与适用范围。[GPUDirect RDMA](https://docs.nvidia.com/cuda/gpudirect-rdma/)；[GPUDirect Storage](https://docs.nvidia.com/gpudirect-storage/design-guide/)
