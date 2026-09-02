对，我们先不要看公司，先画一张“AI 硬件产业链的产能地图”。**真正要研究的不是谁增长最快，而是谁扩产最慢、替代最难、因此最容易长期供不应求。**

可以先把整个链条粗暴地画成：

**电力/电网 → 数据中心 → 供电&冷却 → 网络 → AI 服务器 → GPU/ASIC → 先进封装 → HBM/DRAM → 晶圆制造 → 半导体设备**

其中 GPU 本身又可以拆成：

**先进制程晶圆 + HBM + CoWoS/先进封装 → 一颗可用 AI 加速器**

截至 **2026 年 8 月**，我会先这样给它们分级：

| 环节                    | 当前供需    | 我的判断                        |
| --------------------- | ------- | --------------------------- |
| **电网接入 / 变压器 / 开关设备** | 🔴 极紧   | **最容易被低估的终极瓶颈**             |
| **HBM**               | 🔴 极紧   | 半导体里面最紧缺之一                  |
| **CoWoS / 先进封装**      | 🔴 极紧   | 扩得很快，但需求追得更快                |
| **先进制程 3nm/2nm**      | 🟠 偏紧   | AI 抢先进节点，但没有 HBM/CoWoS 那么极端 |
| **液冷 / 高功率供电系统**      | 🟠 偏紧   | 随机架功率上升快速增长                 |
| **高速网络 / 光模块**        | 🟠 偏紧   | 800G→1.6T 带来新一轮升级           |
| **AI GPU / ASIC**     | 🟠 偏紧   | 实际上是上面几个瓶颈的综合体现             |
| **服务器 DRAM**          | 🟠 偏紧   | 被 AI 和 HBM 间接挤压             |
| **企业级 SSD / NAND**    | 🟠 明显改善 | 已经从过去的过剩转向偏紧                |
| CPU                   | 🟢 基本平衡 | 不是 AI 数据中心核心瓶颈              |
| PCB / 普通服务器零件         | 🟢 基本平衡 | 高端产品局部紧，但总体好扩产              |
| ODM 服务器组装             | 🟢 基本平衡 | 鸿海、广达等都能扩                   |
| 普通成熟制程芯片              | 🔵 部分过剩 | 和 AI 的先进制程完全是两个世界           |

这里面我认为最值得先抓住 **4 个真正意义上的瓶颈**。

---

### 第一名：电力，可能已经超过 GPU 成为最终瓶颈

这个非常关键。

以前大家说：

> GPU 不够，所以数据中心建不起来。

现在逐渐变成：

> **GPU 能买到，但是几百 MW 的电从哪里来？**

IEA 已经明确指出，AI 数据中心的功率密度正在远远超过传统数据中心，而且大量新项目集中在已有数据中心集群，导致**局部电网容量成为瓶颈**。([IEA][1])

甚至不仅是发电量的问题，而是：

**发电厂
↓
高压输电
↓
变电站
↓
大型变压器
↓
开关设备
↓
数据中心**

每一层都有建设周期。

2026 年美国大型变压器的交付周期甚至已经达到数年，一些公用事业公司开始提前 **3–5 年**采购设备。([Reuters][2])

所以以后我们研究 AI CAPEX，我认为必须把一个指标放得非常高：

> **新增可供电 MW / GW**

而不是只看买了多少 GPU。

---

## 第二名：HBM

这个我们以后应该重点研究。

AI GPU 不是：

> 一颗 GPU 芯片。

实际上更像：

> **GPU Logic Die + 几颗 HBM**

没有 HBM，GPU die 做出来也没有意义。

而 HBM 有一个非常邪门的特点：

**它消耗的 DRAM 晶圆面积远高于普通 DRAM。**

所以当三星、SK hynix、Micron 把更多产能转去 HBM 时，又会反过来减少普通 DRAM 的有效供给。

Micron 现在不仅大规模扩 HBM，而且已经开始用长期客户协议锁定未来供应，公司公开表示 AI 对 memory 的需求仍然非常强。([美光科技投资者关系][3])

因此 HBM 本质上有三个壁垒叠加：

**DRAM Fab

* HBM 堆叠
* 客户认证**

扩产明显比普通电子元件困难。

这是我目前最喜欢的一类“产能逻辑”。

---

## 第三名：CoWoS / 先进封装

这个东西可以理解成：

> **把 GPU Die 和几颗 HBM 真正组装成一个巨型 AI 芯片的工厂。**

所以：

**TSMC 3nm GPU wafer**

和

**SK hynix HBM**

都有了，

仍然不代表 NVIDIA 就能出货。

还缺：

**CoWoS。**

TSMC 已经连续几年疯狂扩 CoWoS，但到 2026 年中，产能仍被描述为非常紧张；最新 AI 服务器供应链仍然把 CoWoS 视为潜在出货限制因素。([DIGITIMES][4])

所以目前：

> GPU 晶圆
> HBM
> CoWoS

实际上是一个**三角形产能系统**。

少任何一个都不行。

---

## 第四名：数据中心内部的供电 + 液冷

GPU 功耗越来越恐怖之后，又出现一个新问题。

过去服务器机架可能：

**10–20 kW**

现在 AI rack 是：

**100kW+**

未来还继续提高。

于是传统：

**风扇 + 空调**

开始不够用了。

逐渐转向：

**冷板液冷
CDU
冷却液
高功率 PSU
Busbar
UPS
PDU**

Vertiv 2026 Q2 销售额同比增长 24%，并再次上调全年指引，公司明确把 AI 数据中心的 power / thermal infrastructure 作为主要需求驱动。([Vertiv][5])

所以这一层很有意思：

> **GPU 越强 → 功耗越高 → 每 1 美元 GPU 带来的电力/冷却 CAPEX 反而越来越高。**

这是一条非常强的二阶逻辑。

---

# 然后是第二梯队：网络

很多人低估这一块。

假设你有：

**100,000 张 GPU**

它们如果不能高速互相通信，实际就不是一台超级计算机，而是：

> 100,000 台各干各的电脑。

所以 AI 集群越来越依赖：

**NVLink / NVSwitch
InfiniBand
Ethernet Switch
NIC
800G 光模块
1.6T 光模块
DSP
激光器**

NVIDIA FY2027 Q1 的数据中心 networking 收入达到 **148 亿美元，同比增长 199%**，增长甚至明显快于 compute。([NVIDIA投资者网站][6])

Broadcom 的 AI 收入同样很大程度来自：

**Custom ASIC + Ethernet networking。**([Broadcom Inc.][7])

所以：

> **GPU 数量越多，网络复杂度不是线性增长那么简单。**

Scale-up / Scale-out 正在让网络在整套 AI 系统中的价值量不断提高。

不过这里不像 HBM 那样整个行业统一缺货。

而是：

> **最先进的交换芯片、DSP、800G/1.6T 光模块局部紧缺。**

因此我暂时把它放 **🟠，而不是 🔴**。

---

# 再说我们刚刚研究过的 NAND

这里恰好可以看到产业链为什么**不同步**。

过去 NAND 最大的问题是：

> **严重供过于求。**

三星、铠侠、SK hynix、Micron 都能疯狂堆 bit。

但 AI 出来以后，需求开始变化。

不是 AI GPU 自己直接吃很多 NAND，而是：

**AI 数据集
模型 checkpoint
RAG 数据
KV cache
训练数据
推理数据**

都需要大量存储。

于是：

> 普通消费 NAND
> ↓
> Enterprise SSD

价值发生转移。

2026 年企业级 SSD 已经成为 NAND 非常重要的需求来源，AI 数据中心需求正在明显改善 NAND 的供需环境和 ASP。([S&P Global][8])

所以像我们刚刚看的铠侠，我暂时不会把它归类为：

> **AI 核心稀缺资产**

而更像：

> **AI 把一个原本严重周期过剩的行业重新拉入上行周期。**

这两个逻辑差别非常大。

---

# 所以整个 AI 产业链，我现在会画成这样

```text
                    AI需求
                      │
                      ▼
                GPU / ASIC
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      先进制程       HBM       CoWoS
      TSMC        SK hynix      TSMC
      3nm/2nm      Micron
          │           │           │
          └───────────┼───────────┘
                      ▼
                  AI服务器
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
         高速网络              存储
      Switch/Optics         SSD/NAND
            │
            ▼
          AI集群
            │
       ┌────┴────┐
       ▼         ▼
     电力       液冷
       │
       ▼
电网/变压器/发电厂
```

而**稀缺程度**，我现在粗略排：

**第一梯队**

> 🔴 电力接入 / 变压器
> 🔴 HBM
> 🔴 CoWoS

**第二梯队**

> 🟠 先进制程
> 🟠 液冷 / AI 电源
> 🟠 高速网络 / 光通信
> 🟠 GPU / AI ASIC

**第三梯队**

> 🟡 Enterprise SSD / NAND
> 🟡 Server DRAM

**基本不缺**

> 🟢 CPU
> 🟢 普通服务器组装
> 🟢 普通 PCB / 机箱 / 零部件

这张图后面其实可以直接变成我们的**AI 产业链研究框架**。

我建议下一步就从最关键的问题开始：**把这些环节分别算出“2026 年产能 → 2027/2028 新产能什么时候出来 → 需求增长多少”**。这样我们就可以真正找出来，**未来两年到底哪个瓶颈最难解除，而不是看谁现在最火。**

[1]: https://www.iea.org/reports/energy-and-ai/executive-summary?utm_source=chatgpt.com "Executive summary – Energy and AI – Analysis"
[2]: https://www.reuters.com/business/energy/us-power-companies-scramble-secure-equipment-surging-data-center-demand-strains-2026-07-09/?utm_source=chatgpt.com "US power companies scramble to secure equipment as surging data center demand strains supplies"
[3]: https://investors.micron.com/node/50671?utm_source=chatgpt.com "Micron Technology, Inc. Reports Record Results for the Third Quarter of Fiscal 2026 | Micron Technology"
[4]: https://www.digitimes.com/news/a20260717PD220/tsmc-taiwan-capacity-cowos-earnings.html?utm_source=chatgpt.com "TSMC's CoWoS capacity remains 'extremely tight' as OSAT ..."
[5]: https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Second-Quarter-2026-with-Diluted-EPS-Growth-of-53-Adjusted-Diluted-EPS-Growth-of-60-Raises-Full-Year-2026-Guidance-Across-All-Key-Metrics/default.aspx?utm_source=chatgpt.com "Vertiv Holdings Co. - Vertiv Reports Strong Second Quarter 2026 with Diluted EPS Growth of 53% (Adjusted Diluted EPS Growth of +60%); Raises Full Year 2026 Guidance Across All Key Metrics"
[6]: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-First-Quarter-Fiscal-2027/default.aspx?utm_source=chatgpt.com "NVIDIA Announces Financial Results for First Quarter ..."
[7]: https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-fourth-quarter-and-fiscal-year-2025?utm_source=chatgpt.com "Broadcom Inc. Announces Fourth Quarter and Fiscal Year ..."
[8]: https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/07/ai-driven-nand-pricing-surge-set-to-fuel-kioxia-s-growth?utm_source=chatgpt.com "AI-driven NAND pricing surge set to fuel Kioxia's growth | S&P Global"
