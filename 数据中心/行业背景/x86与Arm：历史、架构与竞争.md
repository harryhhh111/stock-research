# x86 与 Arm：历史、架构与竞争

> 整理/核对日期：2026-11-04。跨公司架构背景专题；由此前 AMD 讨论及术语表中的长篇解释整理。历史事实以原始公告、年报和技术文档为依据；商业含义标为解释或推演。本篇解释架构与产业关系，行情、动态份额仍见公司研究，不将不同日期的统计混为当前事实。

**阅读起点**：x86 与 Arm 是两套 CPU 指令集架构。最初的 x86 来自 Intel，今天主流的 64 位 x86 扩展来自 AMD；Arm 提供另一套指令集及授权生态。架构决定软硬件如何交互，不能单独决定一颗芯片的速度、能效或商业竞争力。

## 1. 先分清指令集、微架构和制程

| 层次 | 回答的问题 | 例子 |
|---|---|---|
| 指令集架构 ISA | 软件能要求 CPU 执行什么操作，结果应是什么？ | x86-64、Arm AArch64 |
| 微架构 | CPU 内部怎样实现这些操作？ | AMD Zen；不同的 Arm CPU 核心设计 |
| 制程 | 怎样把设计制造成晶体管与互连？ | 以 2nm、3nm 等命名的工艺代际 |

可以把指令集类比为“工作语言”，微架构类比为工厂的组织和设备。工厂讲同一种语言，效率也可能相差很大。AMD 与 Intel 都做 x86 CPU，不意味着它们的电路设计相同；两款 Arm CPU 也可能定位、价格和性能完全不同。工艺代际名称不能直接换算性能倍数。

同一份程序源代码，可分别编译为 x86-64 和 Arm64 机器码，完成同一任务；CPU 执行的编码不同。因此“软件功能相同”和“同一个二进制文件可以原生运行”是两回事。[Arm：ISA 与微架构的定义](https://www.arm.com/glossary/isa)

## 2. x86 到底由 Intel 还是 AMD 提出？

### 2.1 Intel 建立基础，AMD 推动 64 位扩展

| 阶段 | 主要贡献 | 意义 |
|---|---|---|
| 1978 年 Intel 8086 | 建立后来 x86 家族的基础 | 后续产品沿着兼容软件的路径发展 |
| Intel 80386 等产品 | 推进 32 位 IA-32 架构 | 形成成熟的 32 位 PC/服务器软件基础 |
| 2003 年 AMD Opteron、Athlon 64 商用 | 将 AMD64，即 x86-64 扩展带入产品 | 在既有 x86 基础上增加 64 位能力，并保留旧软件运行路径 |
| 2004 年 Intel EM64T | 实现兼容 AMD64 的 64 位扩展，后来称 Intel 64 | 两家主流产品走向共同的 64 位软件生态 |

AMD 年报明确：Opteron 于 2003 年 4 月推出，Athlon 64 于同年 9 月推出。因此“AMD 到 2004 年才首次推出 64 位 x86 产品”不准确；架构设计/规范公开与首批产品上市还须区分。[Intel 8086 历史](https://timeline.intel.com/1978/the-beginning-of-a-legend%3A-the-8086)、[AMD 2003 年报，2004-03 披露](https://ir.amd.com/financial-information/sec-filings/content/0001193125-04-037179/d10k.htm)、[Dell 2004 年 EM64T 技术白皮书](https://i.dell.com/sites/content/business/solutions/whitepapers/en/documents/wp-2004_em64t.pdf)

`x64`、`x86_64` 和 `amd64` 通常指这套 64 位 x86 架构；Intel 处理器也能运行匹配平台的 amd64 软件。名称保留 AMD 的架构贡献，不是 AMD 品牌专用安装包。

### 2.2 IA-64 不是 x86-64

Intel 与 HP 的 IA-64（Itanium）是另一套架构，不能因为也叫“64 位”就与 AMD64、Intel 64 混同。AMD64 的重要特点是渐进扩展既有 x86 软件体系；Intel 后来的 EM64T/Intel 64 属于兼容这一路线的主流实现。[2004 年 IBM/Lenovo 对三种实现的说明](https://lenovopress.lenovo.com/tips0475)

### 2.3 今天谁决定 x86 的发展？

现代 x86 包含共同的软件基础，以及两家公司持续增加的扩展和平台特性。不能简单说成“全部由 Intel 定义”或“全部由 AMD 定义”，也不能推导所有功能在两家的所有产品上完全相同。

Intel 与 AMD 于 2024 年建立 x86 生态咨询小组，目标包括协调兼容性与后续演进。这是产业协作机制，不代表第三方因此自动获得 CPU 设计/制造授权。[联合公告，2024-10-15](https://www.intel.com/content/www/us/en/newsroom/news/october-2024-intel-news.html)

## 3. x86 与 Arm 的技术差异怎样理解？

x86 传统上归入 CISC（复杂指令集），使用变长指令编码；现代 64 位 Arm 使用的 A64 指令采用固定 32 位编码，主要遵循 load/store 设计，通常归入 RISC（精简指令集）。load/store 指通过相应指令在内存和寄存器之间搬运数据，再在寄存器等资源中计算。

这些差别影响取指、解码和编译器安排代码，但不能直接换算成“Arm 更快”或“x86 更耗电”。现代高性能 CPU 都采用复杂的缓存、预测和执行机制。复杂指令可能在内部拆成多个操作；多条简单指令也可能被并行安排，不能只数指令条数判断任务耗时。

尤其注意：A64 的“32 位编码”说的是一条指令的长度，处理器仍可操作 64 位数据；也不能把 A64 的定长特征推广到所有历史 Arm 指令集。[Arm A64 编码说明](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/the-a64-isa-and-compilers)、[Intel 指令集参考](https://www.intel.com/content/www/us/en/content-details/671110/intel-64-and-ia-32-architectures-software-developer-s-manual-combined-volumes-2a-2b-2c-and-2d-instruction-set-reference-a-z.html)

## 4. 为什么软件不能随意换 CPU？

相同源代码可以针对不同架构编译，但现成的 x86-64 二进制通常不能在 Arm64 上原生执行。可行路径包括取得原生版本、重新编译，或使用受支持的翻译/仿真环境。

即使同属一种指令集，还须匹配操作系统、ABI（二进制接口约定）、库、驱动和指令扩展。不能仅凭 Windows 和 Linux 都运行于 x86，就认为两个系统的程序可以直接互通。浏览器访问远程网页服务则一般不要求客户端与服务器采用同一 CPU 架构。

对企业，真正的迁移范围包括数据库、内部软件、商业授权、驱动、监控、安全工具、测试及上线流程。Google 的迁移经验说明，成熟开源生态降低了部分重新编译障碍，但大规模测试、工程系统与生产验证仍需投入。[Google：指令集迁移与自动化](https://cloud.google.com/blog/topics/systems/using-ai-and-automation-to-migrate-between-instruction-sets/)

## 5. 为何云厂商自研 CPU 常选 Arm？

**第一，设计授权路径成熟。** Arm 可授权处理器设计，也可按相应协议提供架构授权，使厂商自研兼容核心；“自研芯片”可能大量采用授权 IP，不代表每一部分从零设计。x86 的主流商业路径是采购 Intel/AMD 成品或特定合作方案，不能假定第三方可随意取得同等范围、自由选择实现和代工的授权。

但“x86 绝不授权”也不准确：Intel 曾在代工战略中明确规划包含 x86 核心的 IP 组合，具体权利仍取决于协议。[Arm 授权说明](https://www.arm.com/products/licensing)、[Intel 年报相关说明](https://www.intc.com/filings-reports/all-sec-filings/content/0000050863-24-000055/a2024ars202310k.htm)

**第二，云厂商能围绕内部任务优化系统。【我的推演】** 厂商掌握自己的负载，可选择核心、缓存、内存和网络设计，并安排路线图；大规模部署有机会摊薄研发、流片和迁移成本。比较总成本时还须计入授权、验证、制造、维护及失败风险，自研不等于只付代工费。

**第三，软件控制力不同。【我的推演】** 云厂商能逐批修改、测试并迁移内部服务，传统企业更可能受旧二进制、第三方软件与认证约束。因此同一款新芯片，可能对云厂商划算，对其他客户并不划算。

## 6. Arm CPU 与自研 AI 芯片是什么关系？

| 厂商 | 通用 CPU，采用 Arm 路线 | 专用 AI 加速器 |
|---|---|---|
| AWS | Graviton | Trainium |
| Google | Axion | TPU |
| Microsoft | Cobalt | Maia |

CPU 执行通用程序并承担部分调度等任务；AI 加速器用专门计算单元承担大量张量运算。AI 芯片含有 Arm 控制核心，或系统配套 Arm 主机，都不代表主要 AI 计算单元本身就是 Arm CPU。Google 明确将 TPU 与配套 Axion CPU 分别介绍。

来源：[AWS Graviton](https://aws.github.io/graviton/)、[Trainium 架构](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trainium.html)、[Google TPU 与 Axion](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/eighth-generation-tpu-agentic-era/)、[微软 Cobalt 与 Maia 定位](https://news.microsoft.com/source/features/ai/in-house-chips-silicon-to-service-to-meet-ai-demand/)。

CPU 的指令集与 GPU 的 CUDA/ROCm 编程栈属于不同层。Arm 主机也可配 GPU，CPU 换成 Arm 不自动消除 CUDA 的转换成本。

## 7. 怎样比较能效，怎样用于公司研究？

手机省电不能单独证明 Arm 服务器胜过 EPYC。能效取决于具体微架构、制程、频率、内存系统和软件负载。比较需匹配工作量、吞吐量、尾延迟和内存容量，并区分芯片功耗、整机能耗及总成本。功率低但完成任务更慢，不一定节能；单价低但迁移维护成本高，也不一定便宜。

【我的推演】对 AMD，需要同时看 EPYC 对 Intel 的份额竞争与 Arm 对 x86 的替代；对 Intel，还须结合制造和产品执行；对 Arm，架构采用量不等于等额的芯片销售或授权收入。CPU 颗数、核心数、整机台数、整机收入、CPU 收入及存量装机是不同分母。

最新机构数据与统计边界见 [AMD 研究](../../AMD/AMD.md)第 6.2.1 节。本文保留基础解释，动态数据在公司研究中维护。

## 更新记录

- 2026-11-04：按用户要求从术语表迁出历史、比较和产业关系解释，形成独立专题；术语表仅保留精简定义与本文链接，AMD 主文档改为引用。
