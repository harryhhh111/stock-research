# eSSD 产品拆解：铠侠与 Sandisk

> 整理日期：2026-09-14；最近更新：2026-09-23。产品与市场信息截至 2026-09-23。本文的“eSSD”指用于云数据中心、企业服务器及存储系统的 enterprise/data-center SSD，不把 PC/消费级 SSD 混入。产品规格以厂商公开资料为准；产品收入、毛利和客户份额若未披露，明确标为不可得。

## 结论先行

**eSSD 不是“普通盘 + 更大容量盘”两类，而是一张二维表：写入负载/延迟在一轴，容量/单位 TB 成本在另一轴。** 目前两家的主流产品可以粗略分为：

| 层级（研究分类，不是统一行业标准） | 常见容量观察值 | NAND / 耐久特征 | 为何客户购买 | 两家公司当前例子 |
|---|---:|---|---|---|
| 计算/性能型 | 1.6–15.36TB | 多为 TLC；1 或 3 DWPD | 低延迟、高随机 IOPS、稳定 QoS、数据库/训练/推理热数据 | Kioxia CM9-V/R、CD9P-V/R、XD8；Sandisk SN861 |
| 容量型 TLC | 30.72–61.44TB | TLC；通常约 1 DWPD | 在仍需较高写入耐久、双端口/高可用的前提下，提高 rack 密度 | Kioxia CM9-R；Sandisk SN655 |
| 超大容量 QLC | 30.72–122.88TB 已列入产品，245.76TB 已公开 | QLC；约 0.3–0.35 DWPD，偏读多写少 | 以更少盘位、电力和机架交付热数据集、对象存储、数据湖 | Kioxia LC9；Sandisk SN670 / UltraQLC 路线 |
| 存储级/极低延迟 | 0.8–3.2TB | XL-FLASH/SCM；60 DWPD | 写日志、缓存、延迟敏感的关键路径 | Kioxia FL6 |

这里的“常见容量”不是硬门槛。**同为 30TB，可能是 1 DWPD 的 TLC 容量盘，也可能是 0.3 DWPD 的 QLC 容量盘；它们的可承受写入、成本和价值完全不同。** 反过来，245.76TB 的 QLC 盘每天允许写入的绝对 TB 数可能不低，但它仍不适合无差别替代 3 DWPD 的数据库/日志盘，因为耐久额定的工作负载、延迟与写放大容忍度不同。

---

## 1. 先把“普通”和“大容量”说清楚

### 1.1 容量并不是企业 SSD 的核心分类标准

企业客户先问的通常不是“几 TB”，而是以下四件事：

1. **写入强度（DWPD）**：五年等额定寿命内，每天可把整盘重写多少次。3 DWPD 表示每天约三次全盘写入；1 DWPD 适合读多写少或一般用途；0.3–0.35 DWPD 则典型用于容量/读密集型工作负载。实际耐久度还取决于随机/顺序、4KiB/16KiB I/O、过度预留和写放大，不能只拿一个 DWPD 数字横比。
2. **延迟与 QoS**：训练喂数、在线交易、向量检索、元数据和 checkpoint 的瓶颈常是尾延迟与随机 I/O，不只是顺序 GB/s。企业盘需要在长期稳态、满盘和并发下保持表现。
3. **可用性与认证**：掉电保护（PLP）、端到端数据保护、固件、加密、遥测、故障恢复、服务器/OEM 认证以及长期供货，才是 eSSD 相对消费盘的主要溢价来源。
4. **系统密度/TCO**：盘数、U 位、PCIe 槽位、电力、散热和运维人力。大容量 SSD 的价值不是“单 TB 绝对价格低”，而是可能用更少盘位提供足够快的在线容量。

因此可将“普通 eSSD”理解成**性能/通用型的 1.92–15.36TB 主力规格**，而不是低端盘；它经常反而是单位 GB 附加值更高的产品。30.72–61.44TB 是已经成熟的高容量 TLC 区间；122.88TB 及以上则更多转入 QLC 超大容量路线，但没有一条放之四海皆准的容量分界线。

### 1.2 TLC 与 QLC：为什么大容量盘大多走 QLC

TLC 每个 cell 存 3 bit，QLC 存 4 bit。其他条件相同时，QLC 的裸 bit 密度约多三分之一，因此能降低每 TB 的 NAND 成本、把单盘做得更大；代价是电压状态更多，编程、纠错、耐久和持续写入管理更难。厂商通过控制器、错误校正、动态写入管理、过度预留及数据保留策略弥补，但没有消灭物理取舍。

**“同属 NAND”不等于“同一种可互换的产品”。** NAND 是底层的非易失性存储介质；TLC/QLC 是它把数据写进 cell 的不同方式：TLC 需区分 8 个电压状态（3 bit），QLC 需区分 16 个状态（4 bit）。QLC 获得约三分之一的理论 bit 密度增益，却牺牲了电压裕量、写入耐久与部分持续性能。最终的 eSSD 还叠加 controller、firmware、ECC、PLP、过度预留、接口、外形、散热、双端口和客户认证。因此“把一块高容量 QLC 盘换成性能 TLC 盘”不是把同样 NAND 换个标签，而是改变整套系统的成本、容量、延迟和可靠性取舍。

所以：

- **TLC** 更适合混合读写、数据库、虚拟化、训练数据准备等需要较高耐久与稳定写入的场景；
- **QLC** 更适合读多写少、数据湖、对象存储、分析、内容库和 AI 数据集的在线容量层；
- **SLC/SCM** 适合极低延迟/高写入的窄场景，并不靠容量取胜。

Sandisk 的产品选择指南也明确建议：TLC 适合平衡型企业负载，QLC 应用于低写入频率场景；并把 PLP、ECC 和端到端保护列为企业盘与消费盘在异常处理上的关键差异。[Sandisk eSSD 选择指南](https://www.sandisk.com/solutions/enterprise-ssds)

### 1.3 一个易忽略的算术

DWPD 是“按盘容量归一化”的指标。以五年额定期简单换算：

| 示例 | 标称容量 × DWPD | 名义日写入量 | 正确理解 |
|---|---:|---:|---|
| 12.8TB、3 DWPD | 12.8 × 3 | 38.4TB/日 | 小容量、高写入强度的混合负载盘 |
| 61.44TB、1 DWPD | 61.44 × 1 | 61.44TB/日 | 大容量 TLC 仍可支持可观的绝对写入量 |
| 122.88TB、0.35 DWPD | 122.88 × 0.35 | 43.0TB/日 | 容量型 QLC 的写入预算不必然很小，但写入形态、稳态 QoS 与寿命模型不同 |

这正是为什么“0.35 DWPD 的 122TB 是否比 3 DWPD 的 12.8TB 耐用”是错误问题：前者为读密集的大数据容量池而造，后者为高写入/低延迟路径而造；不能互相替代。

---

## 2. 铠侠：产品线最清楚地体现“四层结构”

铠侠官网将产品进一步分为 **Enterprise SSD** 与 **Data Center SSD**。前者更面向企业服务器、存储阵列和高可用需求；后者面向 hyperscale 的 scale-out 云部署，并对应 OCP Datacenter NVMe 的性能、功耗和散热要求。两类都属于本文 eSSD 口径，产品差别并非“企业更高端、数据中心更低端”，而是部署架构、双端口/可用性和客户认证不同。[铠侠 Enterprise SSD 产品页](https://americas.kioxia.com/en-us/business/ssd/enterprise-ssd.html)；[Data Center SSD 产品页](https://americas.kioxia.com/en-us/business/ssd/data-center-ssd.html)

| 产品线 | 定位与典型负载 | NAND / 连接 | 容量与 DWPD（公开规格） | 如何看它 |
|---|---|---|---|---|
| **CM9-V / CM9-R** | 企业混合读写 / 读密集；AI/ML、OLTP、数据仓库、虚拟化 | BiCS Gen8 TLC；PCIe 5.0 / NVMe 2.0；2.5 吋或 E3.S，双端口能力 | V：1.6–12.8TB、**3 DWPD**；R：1.92–61.44TB、**1 DWPD** | 这是“普通性能盘”到“大容量 TLC”的连续谱：V 是写入价值型，R 用更低 DWPD 换取 61.44TB。 |
| **CD9P-V / CD9P-R** | hyperscaler、CDN、流媒体、云端 OLTP、虚拟化 | BiCS Gen8 TLC；PCIe 5.0 / NVMe 2.0；2.5 吋或 E3.S | V：1.6–12.8TB、**3 DWPD**；R：1.92–61.44TB、**1 DWPD** | 与 CM9 的 NAND/容量逻辑相似，但属 data-center 系列，强调规模化云部署/OCP 适配。 |
| **XD8** | 云服务器和存储系统，前置可维护 E1.S | BiCS Gen5 TLC；PCIe 5.0 / NVMe 2.0；E1.S | 1.92 / 3.84 / 7.68TB、**1 DWPD** | 典型“常规容量、云基础设施主力盘”；价值在密度、热设计、可服务性和平台认证，不在单盘百 TB。 |
| **LC9** | 容量密集的数据湖、对象/分析、读多写少的 AI 数据层 | BiCS Gen8 **QLC**；PCIe 5.0 / NVMe 2.0，双端口 | 2.5 吋最高 122.88TB；E3.L 最高 **245.76TB**；通常 **0.3 DWPD（16KiB）** | 真正的超大容量产品。E3.L 更长的外形为容量、散热和高密度服务，不能塞进普通 M.2/U.2 的思路中理解。 |
| **FL6** | server cache、write log、分层存储读写缓存 | **XL-FLASH SCM**；PCIe 4.0 / NVMe，双端口 | 0.8 / 1.6 / 3.2TB、**60 DWPD** | 非容量路线，而是铠侠区别于一般 TLC/QLC 盘的低延迟、高耐久小众高值产品。 |

CM9/LC9 的数据表显示，CM9-R 最高 61.44TB、LC9 的 E3.L 最高 245.76TB；LC9 采用 BiCS Gen8 QLC，CM9 使用 BiCS Gen8 TLC，均具 PLP 与可选安全功能。[铠侠企业 SSD 规格表](https://www.kioxia.com/content/dam/kioxia/shared/business/ssd/enterprise-ssd/asset/datasheet/EnterpriseSSD_DataSheet_E.pdf)  
XD8 则是 E1.S、1.92–7.68TB、1 DWPD 的 Gen5 TLC 云盘，明确适配 hyperscale 数据中心。[XD8 官方产品页](https://americas.kioxia.com/en-us/business/ssd/data-center-ssd/xd8.html)  
FL6 是 XL-FLASH Storage Class Memory 路线，官方列明 60 DWPD、0.8–3.2TB，目标为缓存、日志和低延迟分层存储。[FL6 官方规格](https://kr.kioxia.com/content/dam/kioxia/shared/business/ssd/enterprise-ssd/asset/datasheet/EnterpriseSSD_DataSheet_E.pdf)

### 2.1 铠侠在超大容量上的位置

LC9 的 245.76TB 不是把 CM9 简单“扩容四倍”。它同时改变了：

- NAND：由 TLC 转 QLC；
- 外形：由 2.5 吋/E3.S 扩展至更长的 E3.L；
- 耐久定位：由 1–3 DWPD 转为读密集约 0.3 DWPD；
- 客户论证：从 IOPS/延迟优先，转为每 rack 的在线 TB、W/TB、盘位和服务器数量节省。

对铠侠的投资含义是：**LC9 是否完成 hyperscaler 认证并放量，比“有无 245TB 样品”重要得多。** TrendForce 在 2026Q1 的产业跟踪中称，铠侠正在扩大 245TB QLC eSSD 的验证，目标在 2026 年下半年加速出货；这是第三方行业信息，不是铠侠已披露的收入或出货承诺。[TrendForce 2026Q1 eSSD 市场回顾](https://www.trendforce.com/presscenter/news/20260611-13092.html)

补充：铠侠当前官网还列有 **CM10** 的 preliminary 规格，进入 PCIe 6.0 / NVMe 2.1；其 TLC mixed-use 型最高 51.2TB、3 DWPD，read-intensive 型最高 61.44TB、1 DWPD。这是下一代性能/容量 TLC 产品线，尚不应与已经有完整 LC9 规格的超大容量 QLC 盘混作已实现收入。[铠侠 Enterprise SSD 产品页](https://americas.kioxia.com/en-us/business/ssd/enterprise-ssd.html)

---

## 3. Sandisk：一条清晰的 compute / storage / UltraQLC 三层线

Sandisk 的当代官网组合比历史产品名更直观：**SN861 是 compute-class，SN655 是 storage-focused TLC，SN670 是 UltraQLC capacity-class。** 三者都能服务 AI/云，但服务的是 AI 数据生命周期中不同的位置，不应因为都被营销为“AI SSD”而假定相同 ASP、毛利或需求弹性。

| 产品线 | 定位与典型负载 | NAND / 连接 | 容量与 DWPD（公开规格） | 如何看它 |
|---|---|---|---|---|
| **SN861** | AI/ML、HPC、OLTP、训练与推理的低延迟/高吞吐 compute-class | PCIe 5.0 x4；U.2、E1.S、E3.S | 1 DWPD：0.96/1.92–15.36TB；3 DWPD：1.6–12.8TB | 与铠侠 CM9/CD9P 的性能/混合负载层最可比；高 IOPS、低延迟、FDP 与多种前置可维护形态是产品价值。 |
| **SN655** | scale-out、软件定义存储、NoSQL、数据归档、数据集准备 | BiCS5 **TLC**；PCIe 4.0 x4、双端口 U.3 | 3.84–61.44TB、**1 DWPD** | 大容量 TLC 的过渡层：容量/GB-Watt 很好，但仍具 1 DWPD 和双端口特性。 |
| **SN670** | 数据摄入、准备、快速数据湖、内容生成、分析建模 | BiCS8 **UltraQLC**；PCIe 5.0 x4、U.2 | 30.72 / 61.44 / 122.88TB、**0.35 DWPD** | 当前公开在册的容量旗舰；以容量和 TCO 为优先级，并非用来替代所有低延迟或高写入盘。 |
| **UltraQLC 256TB demo** | 更高密度的下一阶段能力展示 | UltraQLC；U.2 | 256TB 已演示 | 2025 年发布材料称拟于 2026H1 提供 128TB SN670 与 256TB UltraQLC、其后增加形态；应把它当作路线图/演示，不等同于当前公开目录中的广泛量产 SKU。 |

Sandisk 的官方 AI eSSD 手册列明：SN861 的 1 DWPD 产品最高 15.36TB、3 DWPD 产品最高 12.8TB；SN655 为 3.84–61.44TB、1 DWPD；SN670 为 30.72–122.88TB、0.35 DWPD，并分别对应 compute、storage 和 capacity 优先场景。[Sandisk《Enterprise SSDs—Empowering AI》](https://documents.sandisk.com/content/dam/asset-library/en_us/assets/public/sandisk/product/embedded-flash/brochure/brochure-enterprise-ssd-empowering-ai.pdf)  
对于 256TB，Sandisk 的 FMS 2025 新闻稿明确说已演示 256TB NVMe SSD，并称 128TB SN670 / 256TB UltraQLC 预计在 2026H1 以 U.2 形态可用；由于公开的当前产品页把 SN670 的上限列为 122.88TB，研究中不应把 256TB直接当作已广泛出货的收入产品。[Sandisk FMS 2025 公告](https://investor.sandisk.com/node/7231/pdf)；[Sandisk 当前 eSSD 产品页](https://www.sandisk.com/solutions/enterprise-ssds)

### 3.1 Sandisk 的投资含义：高容量 QLC 是增量，不等于 Datacenter 全部

Sandisk FY2026 的 Datacenter 收入为 **$5.153B（公司收入的 25.4%）**，收入同比增长 **437%**；公司只披露 Datacenter 这个终端市场的收入、bit 和 revenue/GB 变化，**未披露 SN861、SN655、SN670、TLC、QLC 或 30TB+ 各自的收入、毛利、出货 TB 或客户。**

因此下列说法必须区分：

- ✅ 可说：Sandisk 已有三层产品线；行业跟踪称其 QLC eSSD 已进入量产出货，高容量 QLC 供给紧张是增长驱动之一。[TrendForce 2026Q1 eSSD 市场回顾](https://www.trendforce.com/presscenter/news/20260611-13092.html)
- ❌ 不可说：Sandisk Datacenter 收入主要来自 SN670，或其 122TB/256TB 的毛利一定最高——公司没有披露。
- 🟡 合理推断：若高容量 QLC 完成大客户认证并提高占比，它会显著提高每盘 TB 和对 NAND bit 的拉动；但它的每 GB 定价受到 HDD/TCO 的约束，未必比性能型 TLC 盘有更高单位毛利。

Sandisk 年报对 Datacenter 的定义也只到“面向公共/私有云和企业客户的高性能企业 SSD 与软件方案”，未按产品系列拆分。任何更细的收入占比都应被视为猜测。[Sandisk FY2026 10-K](https://investor.sandisk.com/static-files/47c2209d-7ef3-488d-b9f4-62d371ad8740)

---

## 4. 两家放在一起：能比什么，不能比什么

| 问题 | 铠侠 | Sandisk | 正确结论 |
|---|---|---|---|
| 低延迟/混合读写主力 | CM9/CD9P 的 TLC 1/3 DWPD；另有 FL6 SCM | SN861 TLC 1/3 DWPD | 两家都有可比的高性能 TLC 盘；铠侠另有已公开的 XL-FLASH SCM 低延迟路线。 |
| 高容量 TLC | CM9-R 最高 61.44TB、1 DWPD | SN655 最高 61.44TB、1 DWPD | 这一层很相像：不是 QLC，但已能解决很多 rack 密度问题。 |
| 超大容量 QLC | LC9：最高 245.76TB，约 0.3 DWPD | SN670：最高 122.88TB、0.35 DWPD；256TB 为公开演示/路线图 | 铠侠公开产品规格的容量上限更高；不能据此直接判断实际出货、收入或客户认证领先。 |
| 制造基础 | 与 Sandisk 共享 Flash Ventures 的 wafer 制造/研发体系 | 同左 | 同一制造联盟不代表同一 SSD 产品、控制器、固件、客户或商业化速度。 |
| 财报可见度 | 仅披露 SSD & Storage 大类，不能拆 eSSD 系列收入 | 披露 Datacenter 总收入，但不能拆到型号/QLC | 两家公司都无法用公开报表计算“高容量 eSSD 占 eSSD 营收比例”。 |

最重要的经济学不是“谁的容量数字更大”，而是三条线的需求是否同时成立：

1. **性能型 TLC**：算力越贵，低尾延迟和写入稳定性越有价值，通常是企业 SSD 附加值最高的一层；
2. **容量型 TLC**：客户还要企业级写入耐久和高可用，但希望把 30–60TB 装进更少盘位；
3. **超大容量 QLC**：主要吃 AI 数据集、数据湖、对象/分析、热归档的 bit 需求，增长最快但最受 HDD 每 TB 成本约束。

这也解释了本轮价格为什么不能只看“eSSD”。若紧缺的是高容量 QLC，容量型产品会先涨、NAND bit 拉动也大；但性能型 TLC 与容量型 QLC 的供给、认证、价格传导和客户替代路径都不同。TrendForce 2026 年的产业跟踪将高容量 QLC eSSD 的短缺与 AI/近线 HDD 供给紧张联系起来，同时仍指出 QLC 相比 HDD 的每 GB 价差扩大可能限制其长期渗透。[TrendForce：2026Q1 eSSD](https://www.trendforce.com/presscenter/news/20260611-13092.html)；[TrendForce：2026Q3 eSSD 合约价](https://www.trendforce.com/research/download/RP260728RU)

---

## 5. “超大容量最稀缺、利润主要来自它”是否成立？

| 命题 | 判定 | 能确认的证据 | 不能越过的边界 |
|---|---|---|---|
| 高容量 QLC eSSD 是当前最紧缺的子市场之一 | **✅ 基本属实** | TrendForce 在 2026Q1 明确称行业存在高容量 QLC 存储方案短缺；Sandisk 的 QLC eSSD 已进入 volume shipment；铠侠在扩大 245TB 产品验证。近线 HDD 紧缺也把部分容量需求推向 QLC eSSD。 | 没有公开的、逐一比较所有容量/耐久 SKU 的缺货天数或未满足订单，不能量化断言“它比任何性能 TLC 都更稀缺”。 |
| 高容量 eSSD 是行业本轮收入增长的重要引擎 | **✅ 属实** | TrendForce 的 2026Q2 行业跟踪称高容量 eSSD 是需求/收入的主要增长引擎；其对 Sandisk 的跟踪也点名高容量 QLC 的量产与后续增长潜力。 | “行业增长引擎”不等同某一家公司的收入主体，更不等同利润主体。 |
| 铠侠和 Sandisk 的利润主要来自超大容量 QLC | **⚠️ 无法验证** | 两家公司都在把产品/资源向数据中心、高容量 SSD 倾斜，产品经济性通常优于消费渠道。Sandisk FY2026 Datacenter 收入 $5.153B、同比 +437%，说明数据中心是利润弹性的重要来源。 | Sandisk 未披露 SN861/SN655/SN670 或 TLC/QLC 的收入和毛利；铠侠也未披露 LC9/CM 系列收入或毛利。不能由高增长、单盘容量或行业报道倒推出“利润主要来自 QLC”。 |

最准确的说法是：**超大容量 QLC 是当前最稀缺、最能拉动 NAND bit 和增量收入的 eSSD 子市场之一；它很可能是两家公司本轮利润增量的重要来源，但公开数据不足以证明它已是利润的最大来源。**

还要区分“单位 GB 毛利”和“总利润贡献”：性能型 TLC 盘常有更高的认证、固件、QoS、耐久和低延迟附加值，可能拥有更好的单位 GB 经济性；高容量 QLC 的单盘 TB 更大、出货 bit 和绝对毛利额可能很大，但其每 TB 价格受 HDD 替代/TCO 强约束。没有分产品毛利披露，无法判断哪一方更大。

一手公司报告把 Sandisk 的 Datacenter 定义为覆盖不同容量和性能等级的 eSSD/软件方案，而不是 QLC 单一产品线；财务披露只到 Datacenter、Edge、Consumer 三个终端市场。[Sandisk FY2026 10-K](https://investor.sandisk.com/static-files/47c2209d-7ef3-488d-b9f4-62d371ad8740) 行业层面，TrendForce 确认高容量 QLC 的短缺和高容量 eSSD 对增长的贡献，但这仍是行业追踪，不是公司产品毛利表。[TrendForce 2026Q1](https://www.trendforce.com/presscenter/news/20260611-13092.html)；[TrendForce 2026Q2](https://www.trendforce.com/research/download/RP260826DG)

---

## 6. 为什么不能把所有 NAND 都投向高容量 QLC 与性能 TLC eSSD？

**厂商已经在明显倾斜，而不是完全不做。** TrendForce 观察到 2026 年 NAND 资源正由消费产品转向高毛利企业 SSD；但利润最大化不是把 wafer 按当日最高报价全部塞进一个 SKU，而是最大化“可认证、可交付、能长期卖掉”的每片 wafer 贡献利润。

| 约束 | 为什么不能全押高容量 QLC | 为什么不能全押性能 TLC | 对利润的含义 |
|---|---|---|---|
| **应用不可替代** | 0.3–0.35 DWPD QLC 不适合高频数据库写入、日志、缓存与许多虚拟化负载 | 1–3 DWPD TLC 不能以合理成本取代需要海量在线 TB 的数据湖/对象存储 | 两类产品面对的是互补需求，不能用一种盘覆盖另一种盘。 |
| **价格上限不同** | 其核心竞争对象是 nearline HDD；每 TB 成本一旦明显失去 TCO 优势，客户会延后采购或回到 HDD/分层存储 | 它的客户更重性能，但总 TB 需求小于容量层，且客户只会为实际需要的 IOPS/低延迟付费 | 把产能全压向任何一类，都会很快遭遇需求曲线与降价压力。 |
| **产品不是裸 NAND 的简单改包装** | QLC 的 NAND 架构、控制器/固件、纠错、过度预留、数据保留策略、散热和大容量外形都要匹配 | 高性能 TLC 需要 PCIe Gen5/6、PLP、QoS、双端口、企业固件及平台验证 | 真实瓶颈还包括 controller、封装/测试、固件和客户认证，不是只有 fab wafer。 |
| **客户认证与供货关系** | CSP 对 122/245TB 产品的验证并非瞬时完成；铠侠正推进 LC9 的验证 | 服务器 OEM/云客户对特定平台、外形、散热和韧体有认证要求 | 没有认证的“产能”不能立即变成可确认收入；贸然停供既有产品也会伤害下轮客户份额。 |
| **周期与组合风险** | 高容量 QLC 的供需最受 HDD 交期和 AI 数据集建设节奏影响 | 性能 TLC 的需求受服务器平台、计算部署与工作负载结构影响 | 两条线的周期并不完全同步；保留 client、移动、工业与不同 eSSD 层级，能提高 fab 利用率、减轻单一市场反转。 |

### 6.1 “把更多产能给 eSSD”与“把全部产能给一款 eSSD”是两回事

现实中，厂商能在数季尺度上调高 server/eSSD 的 wafer、controller 与封测资源优先级；这正是 2026 年发生的事。TrendForce 称主要厂商正优先配置 server storage，推动高容量 QLC eSSD 渗透，同时压缩消费供应。[TrendForce 2026Q1 NAND](https://www.trendforce.com/presscenter/news/20260525-13058.html) 但它同时也记录了客户对价格的抵触、供应改善后企业 SSD 涨价放缓，以及 QLC 相对 HDD 的每 GB 价差扩大对长期渗透的限制。[TrendForce 2026Q3 eSSD](https://www.trendforce.com/research/download/RP260728RU)

**“QLC 与 HDD 的每 GB 价差限制长期渗透”是什么意思？** HDD 和 QLC SSD 都可以承接大容量、读多写少的数据，但不是完全同质：QLC SSD 有更低延迟、更高 IOPS、较小占地、较低单 TB 功耗，HDD 有远低的介质成本。当 QLC 每 TB 贵得太多时，客户省下的机架、电力和运维成本不足以抵消多付的介质成本，便会把不需要低延迟的数据继续留在 HDD，或延迟扩容。只有数据访问频繁、机架/功耗受限、HDD 无货，或 SSD 性能能显著提高系统吞吐时，QLC 的总拥有成本才可能胜出。

这里的“限制”不是说 QLC 没有市场，而是说它**无法在长期内把所有 HDD 容量一比一替掉**。HDD 紧缺会短期把需求推向 QLC；但一旦 HDD 交期和价格正常化，纯冷数据/归档层仍会主要选择 HDD。TrendForce 的 2026Q3 报告把 QLC/HDD 的单位容量价格差扩大到约 15 倍列为高容量 QLC eSSD 的长期阻力；该数字是行业报价篮子的方向性指标，不应当作所有地区、型号和合同的精确价差。[TrendForce 2026Q3 eSSD](https://www.trendforce.com/research/download/RP260728RU)

这意味着：**短缺本身就是高利润的一部分来源。** 若一家厂商单独把所有供应投向 QLC，而同业不跟随，它可能抢走客户；若全行业都这么做，QLC 的稀缺溢价会下降，而且客户会因 HDD 的每 TB 价差选择少买或延迟买。高性能 TLC 同理：高 ASP/GB 不代表可以吸收全行业 NAND bit，因为它服务的是较小、但更重性能的工作负载池。

### 6.2 对铠侠 / Sandisk 的正确观察点

- 不是看“是否 all in QLC”，而是看 **LC9/SN670 等超大容量 QLC 的认证和出货，是否快于 QLC 的新增 bit 供给**；
- 同时看 **CM/CD/SN861 等 TLC 性能盘的 PCIe 5/6 导入与客户资格**，因为其附加值可能更高；
- 还要看 **总产品组合的 ASP/GB、bit 出货和毛利率**。若高容量 QLC bit 暴涨、但 ASP/GB 下滑更快，收入和利润未必变好；
- 这两家公司均未按 QLC/TLC/SKU 披露利润，不能从“高容量盘紧缺”跳到“全部产能都应投向它”的结论。

---

## 7. KV cache 到底需要性能盘还是高容量盘？

**结论：不能二选一。** 若问题是“离 GPU 最近、需要在下一轮 decode 前把 KV 预取回来的 SSD”，答案偏向**性能/耐久型 TLC eSSD**；若问题是“跨节点、跨会话保存大量可复用历史 KV 的共享库存”，答案才偏向**高容量 QLC eSSD**。真正的 CMX/网络 context tier 在两者之间，并会按 KV 的热度与写入强度混用。

Sandisk 在其 Investor Day 的 AI Infrastructure Outlook 中已把这个选择画得很具体：direct-attached staging 与 direct KV 标作 **TLC performance**；local-network KV 标作 **TLC endurance**；remote-network context tier 中的 fast data lakes 使用 **QLC capacity**，KV 则可以是 **QLC capacity / TLC performance**。这是一手公司产品定位，说明 Sandisk 自己也没有把 KV 看成单一的“高容量 QLC”或“高性能 TLC”市场。[Sandisk《AI Infrastructure Outlook》，p.15](https://investor.sandisk.com/static-files/9ee604b4-b810-4fba-bbd3-c4c605f690f9)

| KV 所在层级 | 数据访问特点 | 更合适的 eSSD | 为什么 | 对 NAND bit 的意义 |
|---|---|---|---|---|
| **G1：HBM 活跃 KV** | 逐 token attention 的即时工作集 | 不应使用 SSD | SSD 延迟无法进入 decode 临界路径 | 无直接 NAND 需求 |
| **G3：本地 NVMe warm KV** | 单节点短期重用；需要低尾延迟、高读带宽、及时预取 | **性能 TLC**，通常 1–3 DWPD、较中等容量 | 它替代的是重算 prefill 的时间；性能、QoS、耐久优先于 TB/$ | 单盘附加值高，但总 bit 未必大 |
| **G3.5：rack/pod 共享 KV** | 多 GPU/多节点访问；热度与写入强度混合；受 RDMA、DPU、软件路由制约 | **TLC endurance + 部分高容量 QLC 的混合池** | 高频 churn 的 KV 需要较高 DWPD；较冷、命中可预测的 KV 可下沉 QLC | 是否形成可观 eSSD 收入，取决于共享/复用是否成立 |
| **G4：长 TTL 的 persistent KV / context archive** | 读多写少；仅在后续会话/agent 重启时恢复 | **高容量 QLC**，30TB–245TB+ | 容量密度、盘数、机架和功耗优先；读取前可异步预取 | 这是把 KV 叙事转化为大量 NAND bit 的必要层 |

NVIDIA 对 CMX 的定义与此一致：它是以 NVMe SSD、BlueField-4、DOCA 和 Spectrum-X 组成的 pod 级 context tier；DPU 管理 SSD、KV routing、完整性和加密，网络提供 RDMA 低延迟访问。故 CMX 的关键不是“某一块 SSD 的标称顺序读速”，而是**大量 SSD 并行 + 网络/DPU/软件预取**能否避免 GPU stall。[NVIDIA CMX](https://www.nvidia.com/en-in/data-center/ai-storage/cmx/)

### 7.1 决定 TLC 或 QLC 的是 KV 写入强度，而不是“是否为 AI”

可用一条运营公式判断：

`实际 DWPD = 每日写入到该层的新增/更新 KV logical bytes × SSD 写放大 ÷ SSD usable capacity`

- 若大量新对话、token 增长和 eviction 使 KV 每天反复写入，实际 DWPD 高，QLC 的约 0.3–0.35 DWPD 可能不够，必须选择 TLC endurance 或减少 admission（只把预计会重用的 KV 写入 SSD）。
- 若一个长 prefix/agent context 写入一次后被大量会话读取，写入被多次读取摊薄，QLC 的容量密度开始有价值。
- 因此，**高 cache hit rate 本身不代表高 SSD 写入**：同一份 KV 被读一百次，反而是 QLC 最友好的情况；低 hit rate 下反复写入又不复用，任何 SSD 层都不经济。

LMCache 公开的 NVMe offload 讨论也把小块/随机写、写放大和耐久列为限制，说明这不是抽象的 NAND 类型问题，而是缓存 admission 与生命周期策略问题。[LMCache SSD wear RFC](https://github.com/LMCache/LMCache/issues/2739)

### 7.2 对铠侠 / Sandisk 的研究含义

1. **早期 KV 商业化首先利好性能 TLC eSSD 的单位价值，而非必然带来巨量 NAND bit。** SN861、CM9/CD9P 一类性能盘更接近本地 warm-KV 需求。
2. **高容量 QLC 才是 NAND bit 大幅扩张的后段结果。** 需要 cache 保留时间长、跨节点复用率高、SSD 读回能稳定快过重算，才会形成大规模共享库存。
3. **不要把“CMX 需要高带宽”误读成“必须全用性能 TLC”。** 高带宽可以由多盘并行、RDMA 和 DPU 实现；最热 KV 留在 HBM/DRAM/TLC，较冷但大容量的部分可用 QLC。
4. **也不要把“KV 能落 SSD”误读成“QLC 自然受益”。** 若真实 workload 是高 churn、短 TTL 的 agent，会先碰到耐久与尾延迟约束，TLC 的份额可能更高，QLC 的容量渗透反而有限。

### 7.3 CMX 对 eSSD 提出了什么新要求？

**结论：CMX 不是要求一块“更快的普通 SSD”，而是把 eSSD 变成可共享、可预取、会频繁迁移 KV block 的工作集层。** 这把评价标准从顺序读写峰值转向端到端尾延迟、并发 QoS、持续写入寿命、容量密度和每瓦有效吞吐；其中相当一部分能力由 BlueField-4、Spectrum-X 与软件栈完成，并不全部落在单盘 controller 上。

| 维度 | CMX 对系统/eSSD 的要求 | 证据状态与研究含义 |
|---|---|---|
| **端到端尾延迟与 QoS** | KV block 必须在 decode 前预取回 HBM/DRAM；多租户并发时 p99/p99.9 延迟比顺序 GB/s 更重要 | 🟡 NVIDIA 明确强调低抖动、预取和避免 GPU stall，但没有公布单盘延迟门槛；不能用某盘的峰值顺序读速替代 CMX 适配性。 |
| **并发混合 I/O** | 多 Agent 同时创建、读取、续写、淘汰不同 KV block，要求稳态随机读写与固件 QoS | 🟡 合理的系统推断；NVIDIA 未公布 I/O size、读写比、queue depth 或 CMX trace。 |
| **持续写入耐久** | KV 新增、更新和 eviction 均产生写入；热层的 DWPD、写放大和寿命可成为约束 | 🟡 重要但未给出最低 DWPD。高 DWPD 不等于高容量：需以实际写入量/可用容量复算。 |
| **PB 级容量密度与能效** | 一个 Pod 要保存大量共享 context，要求高 TB/U、TB/W 与多盘并行带宽 | ✅ NVIDIA 已公开 CMX 为 Pod 级、PB 级 flash context tier；单个 CMX rack 的有效 PB、盘数和容量仍未披露。 |
| **网络化与可编排** | 标准 NVMe/NVMe-oF、RDMA、KV 路由、预取与多节点共享 | ✅ NVIDIA 已确认由 BlueField-4、Spectrum-X、Dynamo/NIXL/DOCA Memos 协同；单盘不必直接“连 GPU”。 |
| **数据持久化** | KV 是 transient、derived、可重算；可减少传统对象/文件存储的重复制和持久化开销 | ✅ 这是 CMX 与传统企业存储最本质的区别；但“可丢数据”不等于不需要 NAND 物理写入寿命。 |

NVIDIA 已公开：CMX 通过 NVMe/NVMe-oF（包括 NVMe KV extensions）、BlueField-4 与 Spectrum-X 建立 Ethernet-attached G3.5 flash tier；Dynamo/NIXL 负责在 HBM、DRAM、本地 SSD、CMX 与网络存储之间移动 KV。它追求的是共享 KV 的预取、复用与低抖动访问，不是让 SSD 进入逐 token decode 的直接数据通路。[NVIDIA CMX 技术说明](https://developer.nvidia.com/blog/?p=111143)

这意味着 **CMX 的“高带宽”不能直接推导为“必须全用 PCIe Gen6 性能 TLC”**：800Gb/s 等级的网络、协议卸载和多盘并行主要发生在 DPU、存储托盘和 fabric 层；单盘既可能是性能/耐久 TLC，也可能是大容量 QLC。反过来，PCIe Gen6 的峰值顺序带宽也不能保证多租户 KV 场景下的 p99 延迟。

从产品组合看，最合理的架构是下列推断，而非 NVIDIA 已公布 BOM：

| CMX 内的逻辑区域 | 更可能的盘型 | 原因 | 对 NAND 的含义 |
|---|---|---|---|
| 高频写入、短 TTL、需快速预取的 hot KV | 性能 TLC / 高 DWPD TLC；极端低延迟场景可用 SCM | 优先低尾延迟、稳态 QoS、耐久；铠侠 FL6 类产品是性能上限的参照，但容量小 | 单位可用 TB 的 NAND/ASP 较高，绝对 bit 不一定大。 |
| 高复用、较长留存的 warm context | 大容量 QLC 与 TLC 的混合池 | 预取可预测、写入被多次读取摊薄时，容量密度和功耗优先 | 是 KV 叙事转化为大规模 NAND bit 的主要路径。 |
| 非即时需要的历史/日志/结果 | 对象存储、文件存储、HDD 或容量型 QLC | 不在即时 decode 临界路径，优先成本与持久化 | 不应与 CMX 的 flash context 容量混算。 |

判断某一实际 CMX 部署会偏 TLC 还是 QLC，不能只问“是不是 AI”，而要复算：

`实际 DWPD = 每日写入该层的新增/更新 KV logical bytes × SSD 写放大 ÷ SSD usable capacity`

- 高 cache hit rate **不必然**意味着高 SSD 写入：一份 KV 写一次、被读取一百次，反而更适合容量型 QLC。
- 低 hit rate、短 TTL、反复写入又不复用时，QLC 首先会受耐久和尾延迟限制；此时应使用 TLC endurance、SCM，或根本不让该 KV 进入 SSD。
- NVIDIA 已强调 KV 不需要传统企业记录的重型持久化与冗余；这可能降低数据保护开销，但不降低 NAND 的物理 program/erase 寿命要求。[NVIDIA CMX 技术说明](https://developer.nvidia.com/blog/?p=111143)

因此，当前不能写成“CMX 一定需要 X DWPD、一定用 QLC 或一定用 TLC”。真正待获取的硬数据是：**每 CMX rack 有效 PB、QLC/TLC/SCM 容量占比、每 TB 每日写入量与 DWPD、混合负载下 p99 延迟、以及每 rack 服务的推理 GPU 数。** 这些数据一旦披露，才可以把 CMX 容量情景转换成可验证的产品组合、NAND bit 与 ASP 情景。

## 8. 后续研究与监控清单

| 需回答的问题 | 目前答案 | 下一个硬证据 |
|---|---|---|
| 245TB LC9 是否已在 CSP 大规模量产？ | 仍以验证/加速出货叙事为主，未见铠侠收入拆分 | 季报中 DC/eSSD bit、客户认证、正式 availability 与客户部署公告 |
| Sandisk 256TB 是否已成为常规量产收入？ | 官方曾给 2026H1 预期；当前目录明确展示的 SN670 上限是 122.88TB | 最新产品 datasheet、earnings call、客户认证与量产表述 |
| 高容量 QLC 在 Sandisk Datacenter 中占多少？ | 无披露 | 仅能等待公司拆分或客户/第三方可信供应链数据；不能由总 Datacenter 收入倒推 |
| 两家谁更赚钱？ | 无产品线毛利/ASP | 观察公司总体 revenue/GB、bit 增速、Datacenter 收入，不能给 SKU 排名 |
| “eSSD 需求强”具体是哪一类？ | 必须分性能 TLC、容量 TLC、超大容量 QLC | 每季记录各厂新认证、容量点、QLC/TLC 产能分配、合同价分项与 HDD 交期 |
| CMX 会消耗何种 eSSD？ | NVIDIA 已确认 NVMe flash context tier，未披露盘级 BOM、DWPD 或 TB/GPU | CMX rack 有效 PB、QLC/TLC/SCM 比例、每 TB 日写入、p99 延迟、每 rack 服务 GPU 数与客户部署文档 |

## 来源与证据等级

- **一手产品规格**：Kioxia 与 Sandisk 官网/数据表，适合确认接口、容量、DWPD、外形、公开定位。
- **一手财务披露**：Sandisk FY2026 10-K，适合确认 Datacenter 收入及其披露边界。
- **二手行业追踪**：TrendForce，适合确认行业产品验证、供需与价格方向；不替代公司实际产品出货或财务数据。

**本文件不作出的结论：** 任一型号的实际 ASP、单 GB 毛利、收入占比、客户名单，或“铠侠/ Sandisk 谁的超大容量 QLC 出货更多”。这些数据当前均无充分公开披露。
