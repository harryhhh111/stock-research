[![EdgeCore to build 1.1GW data center in Virginia | Dan Cordwell posted on the topic | LinkedIn](https://images.openai.com/static-rsc-4/cjOF2Nr8TLdoEnE0GyzEM0yTq0diobw9HhN1N5umqtvSAVN8rDp0JeZh0hrmamFVdQ4fpRrcB1hsJK2YxTho7vYrlEkak1TKpva-Z5Zm11iA3n0LBG6dAJjAEzaTG0xR7gz7Y9UDY764TOp7y7evcGkiq134K8ndRHel49LttLc?purpose=inline)](https://www.linkedin.com/posts/dan-cordwell-6171751a0_ai-datacenters-datacentre-activity-7343668984099008512-_0oq?utm_source=chatgpt.com)

可以。这个问题我查了一圈之后，先给你一个很重要的结论：

> **全球数据中心实际上是高度集中在美国和中国的。**
>
> 而且到了 AI 时代，比较数据中心规模最实用的指标已经不是“面积”或者“服务器数量”，而是 **IT 电力容量 MW/GW**。

“算力 FLOPS”反而不适合跨国家直接比较，因为 H100、B200、TPU、昇腾等芯片的精度口径不同；但 **1 GW IT load 就是 1 GW IT load**，非常适合衡量一个地区能塞多少计算设备。IEA也主要用电力容量和用电量来衡量这个产业。([IEA][1])

## 一、全球格局其实非常集中

2024 年，全球数据中心一共消耗大约 **415 TWh** 电力，其中：

| 地区      |   2024数据中心用电 |    全球占比 |
| ------- | -----------: | ------: |
| 🇺🇸 美国 | **约187 TWh** | **45%** |
| 🇨🇳 中国 | **约104 TWh** | **25%** |
| 🇪🇺 欧洲 |  **约62 TWh** | **15%** |
| 其他地区    |      ~62 TWh |    ~15% |
| **全球**  |  **415 TWh** |    100% |

也就是说：

> **美国 + 中国 ≈ 全球数据中心用电量的70%。**

而且未来增长还是主要来自这两个国家。IEA预计到2030年，美国数据中心用电比2024年再增加约 **240 TWh**，中国增加约 **175 TWh**。([IEA][2])

---

# 二、按现有数据中心电力容量来看

这里不同机构的统计口径会有明显差别，比如有的只统计 commercial/colocation，有的把 hyperscaler 自建机房也算进去。因此不要把几十 MW 的差异看得太精确。

比较可靠的大致数量级是：

| 国家          |        当前运营数据中心规模 | 特点             |
| ----------- | ----------------: | -------------- |
| 🇺🇸 **美国** |       **约50 GW+** | 世界绝对第一         |
| 🇨🇳 **中国** | **约32 GW（2025末）** | 世界第二           |
| 🇩🇪 德国     |         **约3 GW** | 欧洲最大市场之一       |
| 🇬🇧 英国     |       **约2–3 GW** | London 是欧洲核心枢纽 |
| 🇯🇵 日本     |    **约1.5–2 GW级** | 东京+大阪高度集中      |
| 🇮🇳 印度     |       **约1.5 GW** | 正快速扩张          |
| 🇸🇬 新加坡    |       **>1.4 GW** | 国家极小但密度惊人      |

中国是目前增长最快的大型市场之一。Rystad预计中国数据中心装机容量从 **2025年底约32 GW** 增长到 **2026年底约40 GW**。([Rystad Energy][3])

德国2025年的数据中心 IT connection capacity 大约 **2.98 GW**，全年耗电约 **21 TWh**。([Borderstep Institute][4])

英国因为统计口径不同，大约在 **2–3 GW**：一项2026年的研究统计截至2025年底约 **2.0 GW operational capacity**，而Oxford Economics的估算约为 **2.9 GW**。([包容性贸易政策中心][5])

印度截至2025年已经达到约 **1.4–1.5 GW** 运营容量，而且另外还有约1.4 GW在建以及约5 GW规划。([CBRE][6])

新加坡则非常夸张：IMDA截至2026年给出的总容量已经 **超过1.4 GW**。考虑到新加坡只有那么一点面积，它可能是全球数据中心功率密度最高的国家之一。([IMDA][7])

---

# 三、但是美国的领先程度比这个表看起来还夸张

因为美国不是均匀分布。

真正的超级核心是：

## 🇺🇸 Northern Virginia

也就是：

**Ashburn / Loudoun County / Prince William County 一带。**

这里长期被称为：

> **Data Center Alley**

CBRE统计，Northern Virginia 仅2025年底数据中心 inventory 就达到：

# **4.04 GW**

而且一年增加了超过 **1 GW**。它仍然是全球最大的成熟数据中心市场。([CBRE][8])

注意：

**4 GW 是已经建成的数据中心 inventory。**

这已经相当于：

> 4座大型核电机组持续满功率输出。

而且Virginia未来的排队量更加惊人。Dominion Energy 2026年3月披露，与数据中心相关的 **contracted capacity 接近51 GW**——这里绝对不能理解成已经运行51 GW，而是签约/排队的未来负荷。([Reuters][9])

这反而说明了我们前面聊的问题：

> **AI数据中心现在最大的限制开始从GPU转向“电什么时候能接上”。**

---

# 四、接下来出现的数据中心，会比Northern Virginia现有机房还夸张

这是AI时代真正发生巨大变化的地方。

过去：

**100 MW**

已经算巨型数据中心。

IEA现在的分类大概是：

* 普通传统数据中心：10–25 MW
* Hyperscale AI DC：**100 MW+**
* 最大在建项目：约 **2 GW**
* 最大规划项目：已经达到 **5 GW级**

([IEA][1])

现在正在进入：

> **一个园区 = 几 GW**

的时代。

---

# 五、目前全球最夸张的几个 AI 数据中心项目

这张表你可以重点看：

| 项目                          | 国家       |          规划容量 | 状态    |
| --------------------------- | -------- | ------------: | ----- |
| **Meta Hyperion Louisiana** | 🇺🇸 美国  |      **5 GW** | 建设/扩建 |
| **Stargate UAE**            | 🇦🇪 阿联酋 |    **5 GW园区** | 分阶段建设 |
| **OpenAI Stargate美国计划**     | 🇺🇸 美国  | **10 GW整体目标** | 多园区   |
| **Microsoft Pecos Texas**   | 🇺🇸 美国  |      **2 GW** | 规划建设  |
| **Nanto/Toyama cluster**    | 🇯🇵 日本  |    **3.1 GW** | 规划    |
| **Northern Virginia**       | 🇺🇸 美国  |   **~4 GW现有** | 已运营集群 |

其中最值得注意的是 Meta。

### Meta Hyperion

Meta今年7月确认，Louisiana Richland Parish 的 Hyperion 数据中心最终将扩展到：

# **5 GW compute capacity**

这是单一 AI 数据中心园区级别的5GW，不是全美国。([Facebook][10])

你可以想象一下：

中国目前整个德国数据中心行业也就大约 **3 GW**。

Meta现在：

> **一家公司，在Louisiana一个园区，目标5 GW。**

这就是AI数据中心和传统数据中心时代最大的尺度变化之一。

---

# 六、OpenAI更夸张

OpenAI的Stargate不是一个数据中心，而是一系列大型AI园区。

2025年OpenAI与Oracle宣布增加 **4.5 GW** Stargate容量，加上Texas Abilene等项目，使Oracle/OpenAI相关Stargate建设规模超过：

**5 GW**

对应官方说法：

> **超过200万颗芯片。**

([OpenAI][11])

之后OpenAI公布的整体目标是：

# **10 GW**

以及：

**$500 billion**

AI基础设施投资。([OpenAI][12])

这个数据非常有用，因为终于给我们建立了：

> **GW ↔ AI芯片**

之间的大概尺度。

5 GW → 200万+芯片

非常粗略地说：

### 1 GW ≈ 40万颗AI芯片

不过这里千万不能直接理解成40万颗GB300 GPU。

因为这5GW里面包含：

* GPU
* CPU
* 网络
* 存储
* 冷却
* 电气损耗

而且“chips”也不一定全部是GPU。

后面我们可以专门把它算准确。

---

# 七、阿联酋也是一个非常值得关注的新玩家

这个可能会有点出乎意料。

Abu Dhabi 正在建设的AI园区最终规划：

# **5 GW**

整个园区约26平方公里。

其中第一阶段 **Stargate UAE** 本身规划1 GW，2026年首先上线约：

**200 MW**

预计第一批使用大约：

**100,000颗 NVIDIA Grace Blackwell GB300相关芯片。** ([Reuters][13])

所以中东为什么突然在AI数据中心里面出现？

原因非常简单：

> **能源。**

以前数据中心首先考虑的是：

网络在哪里
客户在哪里

AI训练时代越来越变成：

> **便宜而且稳定的5 GW电在哪里？**

于是美国Texas、Louisiana、中国内蒙古/西部、UAE这些原来并非传统互联网中心的地方，开始变得非常有吸引力。([金融时报][14])

---

# 八、中国是另外一种模式

中国不像美国这么容易拿到Meta、Microsoft每个园区具体多少GPU的数据。

但是国家级数据更完整。

截至2025年底，中国已经建成：

**42个万卡级智算集群**

智能算力：

# **>1,590 EFLOPS**

而且八大国家算力枢纽的智算规模已经占全国的 **80%以上**。([国务院新闻办公室][15])

但这里必须提醒你：

> **中国的1590 EFLOPS，不能直接拿来跟NVIDIA公布的某块GPU TFLOPS然后简单相除。**

因为涉及：

FP16 / BF16 / FP8
稀疏算力
理论峰值
实际有效算力
国产AI芯片统计口径

这些都会造成巨大差异。

所以在我们后面的投资研究里，我宁愿用：

**MW / GW**

作为主要尺度。

---

## 不过中国有一个很有意思的公开案例

中国联通青海西宁的数据中心已经部署约：

**23,000颗国产AI芯片**

当前算力：

**3,579 PFLOPS**

最终规划：

# **20,000 PFLOPS**

主要包含阿里平头哥等国产AI芯片。([Reuters][16])

这个项目后面非常值得拿来和：

**H100/B200/GB300数据中心**

做比较。

因为我们可以算：

> 相同1 MW电力，中国国产芯片集群和NVIDIA集群分别能产生多少有效AI算力。

这个问题比单纯比较芯片参数有意义得多。

---

# 九、所以全球格局可以简化成这样

我现在会把世界分成三层：

### 第一层：美国、中国

这是绝对的两个超级中心。

**美国：50 GW级**

**中国：30–40 GW级**

两者远远领先其他单一国家。美国优势主要来自 NVIDIA + hyperscaler +资本，中国则有巨大的电力系统、算力基础设施建设和国内需求。([Rystad Energy][3])

### 第二层：欧洲、日本

德国、英国、日本等基本还是：

**1–3 GW级单一国家市场。**

已经很大，但跟美国、中国不是一个数量级。([Borderstep Institute][4])

### 第三层：新兴AI基础设施国家

最值得关注：

**印度、UAE、沙特、马来西亚等。**

这里的特点不是当前存量特别大，而是未来项目动辄：

**500 MW / 1 GW / 5 GW。**

例如印度现在运营规模大约1.5GW左右，但仅未来五年AI数据中心预计就可能新增约 **6.5 GW**。([Reuters][17])

---

# 十、这里其实暴露出了一个非常重要的投资线索

JLL预计全球数据中心容量到2030年可能达到：

# **~200 GW**

未来五年新增接近：

**100 GW**

也就是几乎再造一个今天的全球数据中心行业。([仲量联行][18])

而且2025年AI工作负载大概还只占数据中心 workload 的 **约1/4**，JLL预计2030年可能达到一半。([仲量联行][18])

所以现在我认为我们下一步应该不要再继续泛泛看“数据中心有多少”。

而是把这 **100 GW新增产能** 拆开：

> **美国新增多少 GW**
>
> **中国新增多少 GW**
>
> **欧洲/中东/印度新增多少 GW**
>
> ↓
>
> 每新增 **1 GW**
>
> 需要多少 GPU、HBM、光模块、变压器、UPS、液冷、天然气轮机
>
> ↓
>
> **最后算出未来5年每条产业链到底对应多大的真实需求。**

这就开始直接和我们研究 **NVIDIA、AMD、Micron、铠侠、Vertiv、Eaton、Arista、GE Vernova** 这些公司的收入联系起来了。

这些数字变化很快，我也可以定期帮你更新各国AI数据中心GW建设进度。

[1]: https://www.iea.org/reports/energy-and-ai/understanding-the-energy-ai-nexus?utm_source=chatgpt.com "Understanding the energy-AI nexus – Energy and AI – Analysis - IEA"
[2]: https://www.iea.org/reports/energy-and-ai/executive-summary%C2%A0?utm_source=chatgpt.com "Executive summary – Energy and AI – Analysis - IEA"
[3]: https://www.rystadenergy.com/news/chinas-data-center-capacity-doubling-of-power?utm_source=chatgpt.com "China's data center capacity set to top 60 GW by 2030, driving a ..."
[4]: https://www.borderstep.org/data-digits/?utm_source=chatgpt.com "Data Digits - Borderstep Institute"
[5]: https://citp.ac.uk/publications/mapping-the-uks-data-centres-build-out-implications-for-digital-sovereignty?utm_source=chatgpt.com "Mapping the UK's data centres build-out"
[6]: https://www.cbre.co.in/insights/reports/india-s-data-centre-market-in-a-new-era?utm_source=chatgpt.com "India's Data Centre Market in a New Era"
[7]: https://www.imda.gov.sg/resources/blog/blog-articles/2025/02/red-dot-analytics-help-data-centres-be-cool?utm_source=chatgpt.com "IMDA-accredited company advances green data centres"
[8]: https://www.cbre.com/insights/reports/global-data-center-trends-2025?utm_source=chatgpt.com "Global Data Center Trends 2025"
[9]: https://www.reuters.com/business/energy/dominion-beats-quarterly-profit-estimates-higher-virginia-power-demand-2026-05-01/?utm_source=chatgpt.com "Dominion beats quarterly profit estimates on higher Virginia power demand"
[10]: https://about.fb.com/news/2026/07/teachers-local-businesses-win-as-meta-expands-louisiana-data-center/?utm_source=chatgpt.com "Teachers and Local Businesses Win as Meta Expands Louisiana ..."
[11]: https://openai.com/index/stargate-advances-with-partnership-with-oracle/?utm_source=chatgpt.com "Stargate advances with 4.5 GW partnership with Oracle"
[12]: https://openai.com/index/five-new-stargate-sites/?utm_source=chatgpt.com "OpenAI, Oracle, and SoftBank expand Stargate with five ..."
[13]: https://www.reuters.com/business/media-telecom/stargate-uae-ai-datacenter-begin-operation-2026-2025-05-22/?utm_source=chatgpt.com "'Stargate UAE' AI datacenter to begin operation in 2026"
[14]: https://www.ft.com/content/99ce2860-42ce-4396-8d76-68dee3ac1c9b?utm_source=chatgpt.com "How to power data centres"
[15]: https://www.scio.gov.cn/gxzl/srxxxjptzglz/srjd/202603/t20260313_961434.html?utm_source=chatgpt.com "牢牢掌握人工智能发展和治理主动权"
[16]: https://www.reuters.com/business/media-telecom/china-spotlights-major-data-centre-project-using-domestic-chips-2025-09-17/?utm_source=chatgpt.com "China spotlights major data centre project using domestic chips"
[17]: https://www.reuters.com/world/asia-pacific/brookfield-sees-65-gw-ai-data-centre-capacity-coming-online-india-2026-07-28/?utm_source=chatgpt.com "Brookfield sees 6.5 GW of AI data-centre capacity coming online in India"
[18]: https://www.jll.com/en-us/insights/market-outlook/data-center-outlook "2026 Market Outlook for Global Data Centers | JLL Research"
