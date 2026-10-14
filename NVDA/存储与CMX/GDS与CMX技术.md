# GPU 直连 SSD 在 NVIDIA AI Factory 中体现在哪里：GPUDirect Storage 与 Rubin CMX 的区别

> 整理日期：2026-09-16；信息截止日：2026-09-16。先给结论：不要把 **GPUDirect Storage（GDS）** 和 **CMX Context Memory Storage** 混为同一技术。前者是通用的数据搬运优化；后者是 Rubin POD 中面向推理 KV cache 的独立存储层。NVIDIA 公开资料没有说明 Vera Rubin NVL72 的本地 SSD 采用了 GDS 或披露其 SSD 拓扑。

## 一句话结论

你在 Vera Rubin NVL72 的机柜图里看不到“GPU 直连 SSD”，因为它不是 NVLink 机柜内部的核心拓扑：

- **GDS** 可以让本地 NVMe、远程 NVMe-oF 或其他支持的存储，通过 DMA 直接读写 GPU HBM，绕开 CPU DRAM 的 bounce buffer；但 CPU 仍负责发起和管理 I/O 的控制路径。
- **CMX** 不是一块装在 NVL72 计算托盘旁的 SSD。它是通过**独立的 BlueField-4 STX 存储机柜**构成的、经以太网连接的 POD 级闪存上下文层，用来存放和共享推理的 KV cache。
- 两者可以在同一 AI Factory 共存，但公开资料没有证明 CMX 的数据路径就是 cuFile/GDS，也没有证明 NVL72 每张 GPU 与特定 SSD 形成直接点对点连接。

## 1. GDS：真正的“GPU 直连 SSD”到底是什么意思

### 1.1 传统路径与 GDS 路径

```text
传统 I/O（数据路径）
NVMe SSD → PCIe / CPU → CPU DRAM bounce buffer → PCIe → GPU HBM

GPUDirect Storage（数据路径）
NVMe SSD / 存储控制器 / NIC DMA → PCIe（可能经 switch）→ GPU BAR1 → GPU HBM
                                     ↑
                           CPU 仍负责控制路径、发起 I/O
```

GDS 的“直连”是指**数据不必先落到 CPU DRAM 再复制到 GPU HBM**，而不是 CPU 被完全从系统中删除，更不是 GPU 自己像 CPU 一样执行文件系统调用。应用仍在 CPU 上以 cuFile API 发起显式 I/O；`nvidia-fs.ko` 等内核组件协助把 GPU 内存地址交给存储侧的 DMA 引擎。

### 1.2 为什么有效

传统路径至少有两次数据拷贝，CPU 内存带宽、CPU 负载与 DMA 编排都会形成瓶颈。GDS 使 NVMe SSD、RAID 控制器或远端存储 NIC 的 DMA 引擎可以直接写入/读出 GPU 显存，因此可能：

- 减少一次 bounce-buffer 拷贝，降低端到端延迟；
- 让更多 NVMe/NIC 带宽并行汇入 GPU；
- 降低 CPU 为 I/O 搬运数据的负担；
- 让 GPU 以更高吞吐读取超出 HBM 容量的数据集。

效益取决于真实 I/O 是否是瓶颈。小型、缓存命中或 CPU 处理本身占主导的负载，未必因 GDS 明显变快。

### 1.3 GDS 成立的条件

| 条件 | 为什么需要 |
|---|---|
| 支持 GDS 的数据中心 GPU、驱动、CUDA 与 `nvidia-fs` | GPU 显存地址须能被外设 DMA 正确访问 |
| 本地 NVMe 或远端 NVMe-oF/分布式文件系统 + 支持的驱动 | 本地通常由 NVMe DMA，远端通常由 NIC RDMA 承担数据搬运 |
| `O_DIRECT` 与 cuFile / cuObject 等显式接口 | 避免文件系统页缓存重新把数据放回 CPU DRAM |
| 合理 PCIe 拓扑 | GPU 与 SSD/NIC 在同一 PCIe switch 下通常带宽更好；跨 root complex 也可能直接传，但吞吐更受限 |
| 足够并发、足够多驱动器 | 单块 NVMe 很难填满高端 GPU 的 PCIe 链路，应用需并发 I/O |

因此 GDS 是“需要硬件、软件、文件系统和应用配合”的数据路径，不是把一块普通消费级 SSD 插入机器就自动打开的功能。

## 2. 它在 NVL72 中体现在哪里？答案是：公开规格没有直接体现

Vera Rubin NVL72 的公开产品页重点披露了 GPU、Vera CPU、NVLink 6、ConnectX-9、BlueField-4 与 Mission Control；没有列出本地 NVMe 数量、PCIe switch 拓扑，也没有宣布 NVL72 本地 SSD 的 GDS 认证或带宽指标。

所以可以确认的只有两件事：

1. Rubin 是数据中心 GPU 平台，理论上可部署 GDS 软件栈；
2. **不能**根据“NVL72 有 BlueField-4”或“有 HBM4”推导出某块 SSD 已经 GPU 直连。

此前 GB300 NVL72 的公开参考架构曾列出每个计算托盘的本地 M.2 系统盘和 E1.S NVMe 缓存盘，但 Rubin NVL72 的公开资料未给出对应配置。不能把 GB300 的托盘存储配置直接套到 Rubin。

## 3. Rubin 真正新增的存储架构：CMX，而非柜内 GDS SSD

### 3.1 CMX 解决什么问题

生成式推理会产生 KV cache：模型已处理过的 token 的键和值。对长上下文、多轮对话、RAG 和多 agent 工作流，重新计算历史 context 的成本会很高；但把所有 KV cache 永久留在稀缺的 GPU HBM 也很贵。

CMX 的设计是在 HBM 与传统通用存储之间增加一个“G3.5”层：

```text
最快、最贵             GPU HBM：当前 token 的活跃 KV cache
                              ↕
                 CMX：POD 级共享、高带宽闪存 context tier
                              ↕
慢、容量最大           通用对象/文件/数据库/持久化存储
```

CMX 的核心价值不是训练数据 ingest，而是将被逐出 HBM 的、可复用的短暂 KV context 以低延迟方式保存和预取，供同一 POD 内不同节点、会话或 agent 复用，避免 GPU 因等待 context 而空转。

### 3.2 它在物理架构中的位置

```text
Vera Rubin NVL72 计算机柜（GPU + CPU）
                 │
       Spectrum-X Ethernet / POD 网络
                 │
BlueField-4 STX 存储机柜
  └─ CMX：高带宽、共享的闪存 KV-cache context tier
```

NVIDIA 将 BlueField-4 STX 描述为由 Vera CPU、ConnectX-9 SuperNIC、Spectrum-X Ethernet、DOCA 和 AI Enterprise 支撑的模块化存储参考架构；CMX 是其首个机柜级实现。也就是说，CMX 的 SSD/闪存、存储处理和网络接口在**单独的 STX 存储机柜**中，而非 72 GPU 的 NVL72 柜内。

### 3.3 CMX 是否等于“GPU 直接访问 SSD”？

不是严格等同。

- CMX 的公开描述是“高带宽、POD 级共享 context layer”，通过 BlueField-4 和以太网实现 KV cache 的共享、复用和卸载；
- GDS 的公开定义则是经 cuFile/cuObject 等路径，使存储 DMA 直接进出 GPU HBM，绕开 CPU bounce buffer；
- NVIDIA 尚未在公开 CMX/STX 材料中披露 CMX 使用 cuFile、GDS、`O_DIRECT`，或将 SSD DMA 直接映射到 Rubin GPU HBM 的实现细节。

因此正确表述是：**CMX 是为 GPU 推理提供高性能闪存上下文层的系统架构；它可能使用多种低开销数据路径，但不能在没有资料时把它等同于 GDS。**

## 4. 两条技术线的分工

| 维度 | GPUDirect Storage | BlueField-4 STX / CMX |
|---|---|---|
| 本质 | GPU 与存储间的 DMA I/O 数据路径优化 | 为 agentic inference 设计的 POD 级上下文存储架构 |
| 主要数据 | 训练数据、科学数据、特征数据、通用文件/对象 I/O | 临时、可复用的推理 KV cache/context |
| 典型物理位置 | 本地 NVMe，或经 NIC 连接的远端 NVMe-oF/分布式存储 | 独立 BlueField-4 STX 存储机柜 |
| CPU 的作用 | 不走 CPU DRAM 数据缓冲，但 CPU 仍发起/管理 I/O | BlueField-4/软件负责存储处理和安全；具体内部数据路径未完整公开 |
| 对 NVL72 的关系 | 可在兼容的 Rubin 节点/存储拓扑上部署，但未作为公开单柜卖点 | NVL72 通过 POD 网络使用该共享 context tier |
| 成熟度/证据 | 有公开设计与编程文档 | 2026 年宣布的 Rubin 平台新架构，性能主要为厂商主张 |

## 5. 为什么这对 AI Factory 很重要

如果大模型只做一次性短回答，SSD 到 GPU 的路径通常不是最重要瓶颈；但 agentic inference 反复调用工具、跨会话保留 context、共享 KV cache 时，内存层级和数据搬运会决定 GPU 是否被“喂饱”。

- **GDS** 让批量数据、检查点、训练集或 RAG 数据从 SSD/远端存储更高效进入 GPU；
- **CMX** 让昂贵的 HBM 只保留最热的活跃状态，将较冷但可能复用的 context 放到高速共享闪存层；
- **BlueField-4 + Spectrum-X** 试图使这一层可在 POD 范围内共享、隔离和安全运行。

这也是 NVIDIA 将机柜扩展成 POD 的理由：GPU、网络、DPU 和存储不再是独立采购项，而共同决定 token/s、token cost 与 GPU 利用率。

## 6. 对研究与产业链的具体观察点

1. **不要仅看 SSD 出货量**：CMX 的价值取决于可实现的读写延迟、IOPS、网络吞吐、KV cache 软件策略与复用率，而非单盘容量。
2. **关注 STX/CMX 的 BOM**：BlueField-4 STX、ConnectX-9、Spectrum-X、闪存、存储软件、机柜/网络集成才是该层的完整供给链。
3. **要求可验证指标**：CMX 是否披露每 GPU 需要的闪存容量、每 POD 的 STX 柜数、p99 context fetch latency、KV-cache hit rate、GPU idle time 和真实 token/s。
4. **GDS 的验证方式不同**：需要看系统拓扑、cuFile/cuObject 是否启用、`O_DIRECT`、支持的文件系统、gdsio 基准和 CPU 利用率，而不是只看产品宣传。
5. **避免误读“5×”**：CMX 的“最高 5 倍 token/s、5 倍能效”是相对传统存储的 NVIDIA 产品主张，取决于长上下文与 KV cache 卸载，不能外推到全部 AI 推理或训练负载。

## 来源

1. **NVIDIA GPUDirect Storage 概览与设计指南**：GDS 的 DMA 路径、CPU control path、`O_DIRECT`、NVMe/NIC 和 PCIe 拓扑要求。[概览](https://docs.nvidia.com/gpudirect-storage/overview-guide/)；[设计指南](https://docs.nvidia.com/gpudirect-storage/design-guide/)
2. **NVIDIA GDS 文档首页**：cuFile 与 cuObject 的不同接口路径。[GDS 文档](https://docs.nvidia.com/gpudirect-storage/)
3. **NVIDIA CMX 产品页**：CMX 是由 BlueField-4 驱动的、POD 级共享 context tier。[CMX](https://www.nvidia.com/en-us/data-center/ai-storage/cmx/)
4. **NVIDIA BlueField-4 STX 发布稿**：STX/CMX 的独立机柜级实现、伙伴和性能主张。[发布稿](https://nvidianews.nvidia.com/news/nvidia-launches-bluefield-4-stx-storage-architecture-with-broad-industry-adoption)
5. **NVIDIA CMX 技术博客**：G3.5 闪存层和 KV cache 在 POD 内的角色。[技术解释](https://developer.nvidia.com/blog/?p=111143)
6. **NVIDIA Rubin NVL72 产品页**：公开单柜规格未列本地 NVMe/GDS 拓扑。[NVL72](https://www.nvidia.com/en-eu/data-center/dgx-vera-rubin-nvl72/)
