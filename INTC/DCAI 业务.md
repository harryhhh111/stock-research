可以。先给结论：

> **DCAI 目前本质上仍然是一门“服务器 CPU 生意”，不是一门以 AI GPU 为核心的生意。**

Intel 财报对 DCAI 实际只给我们拆到两层：**Server** 和 **Other DCAI**。([英特尔][1])

### 2026 Q2：DCAI $62.62 亿到底是什么

| DCAI 内部        |        Q2 2026 |  大约占 DCAI |
| -------------- | -------------: | --------: |
| **Server**     | **约 $53.11 亿** | **约 85%** |
| **Other DCAI** |    **$9.51 亿** | **约 15%** |
| **合计**         |   **$62.62 亿** |      100% |

其中 $53.11 亿的 Server 数字，是用 DCAI 总收入 $62.62 亿减去 Intel 明确披露的 Other DCAI $9.51 亿得到的。Intel 明确表示，DCAI 的增长主要来自服务器收入。([英特尔][1])

所以第一件最重要的事已经清楚了：

> **DCAI ≈ 85% 服务器业务 + 15% 其他数据中心芯片。**

---

## 1. Server：DCAI 真正的核心

这里最重要的产品就是：

**Intel Xeon**

也就是 Intel 的服务器 CPU。

对应关系非常简单：

> PC → Core / Core Ultra
> 服务器 → **Xeon**

Xeon 被用于：

* 云计算服务器
* AWS、Azure、Google 等 hyperscaler 数据中心
* 企业数据中心
* 电信网络
* HPC
* AI 服务器中的通用 CPU

Intel 自己明确说，DCAI 的数据中心业务是以 **Xeon 系列服务器 CPU 为核心**的。([英特尔][2])

所以你现在可以把 Intel Products 两块非常直观地理解成：

> **CCPG：卖 PC CPU**
>
> **DCAI：主要卖服务器 CPU**

只是 DCAI 还附带了一些其他数据中心芯片。

---

## 2. Other DCAI：剩下的 $9.51 亿是什么？

这部分就比较杂了。

主要包括三类。

**第一类：ASIC / Purpose-built Silicon**

也就是针对某个客户、某个用途专门设计的芯片。

Intel 现在非常重视这个方向，希望利用自己的芯片设计能力，帮外部客户开发定制 ASIC。Intel 2026 Q2 明确说，Other DCAI 增长主要就是因为 **purpose-built silicon / ASIC 需求增加**。([英特尔][1])

这个业务以后值得单独研究，因为它有点像 Broadcom 的定制 AI 芯片业务。

**第二类：网络芯片**

例如：

* Ethernet Controller
* Network Adapter / NIC
* 数据中心网络相关芯片

CPU负责：

> **计算**

网络芯片负责：

> **在服务器之间搬数据**

Intel 自己说，Ethernet 产品是 Xeon 的补充：Xeon 跑 workload，而 Ethernet controller 负责把数据在网络中高效传输。([英特尔][2])

**第三类：AI Accelerator / 数据中心 GPU**

比如之前的：

**Gaudi**

以及 Intel 正在开发的 inference GPU。

但是这里有一个非常重要的事实：

> **这不是 Intel 当前 DCAI 爆发增长的核心。**

Intel 自己在 2025 年 10-K 里已经非常明确地承认，它在 AI accelerator 市场**至今没有成为有意义的参与者**，Gaudi 的尝试并不成功；2024、2025 还分别产生了大量 Gaudi 库存相关费用。([英特尔][2])

所以千万不要看到：

> Data Center **and AI**

就理解成：

> “这是 Intel 的 Nvidia 业务。”

**不是。**

---

# 3. 那 DCAI +59% 到底是谁贡献的？

这个特别关键。

2025 Q2 DCAI：

**$39.39 亿**

2026 Q2：

**$62.62 亿**

增加：

**约 $23.23 亿。**

Intel 明确说：

> **Server revenue 增加约 $20 亿。**

Other DCAI：

> 增加约 **$3.04 亿**。([英特尔][1])

也就是说，DCAI 增加的约 $23 亿收入中：

> **约 $20 亿来自服务器业务。**

换句话说：

**大约 86% 的增量来自 Server。**

所以这波 +59% 的核心根本不是：

> Intel Gaudi 突然打赢 Nvidia。

而是：

> **Intel Xeon 服务器 CPU 突然卖得非常好。**

这个区别非常重要。

---

# 4. Xeon 为什么突然卖这么好？

Intel 又进一步给我们拆了。

Q2 2026 Server：

**销量 +9%**

但是：

**ASP（平均售价）+48%。**

而 ASP 暴涨主要是因为客户购买了更多：

> **premium、高核心数、高端服务器 CPU**

其次才是 Intel 主动涨价。([英特尔][1])

所以实际上不是：

> Intel 卖了 59% 更多 CPU。

而更接近：

> **卖了约 9% 更多 CPU，同时客户大量转向昂贵的高端 Xeon。**

这才导致 Server revenue 大爆发。

---

# 5. 谁在买？

Intel 给出的最重要信息是：

> **Server volume 增长主要由 hyperscaler demand 推动。**

而且市场需求一度**超过 Intel 能提供的产品供应量**。([英特尔][1])

Hyperscaler 就是：

* Amazon AWS
* Microsoft Azure
* Google Cloud
* Meta
* 大型云基础设施公司

这一类巨型数据中心运营商。

于是 AI 和 Intel 之间真正的传导链条开始清楚了：

> **AI 爆发**
>
> ↓
>
> hyperscaler 大建数据中心
>
> ↓
>
> 不仅需要 NVIDIA GPU
>
> ↓
>
> 也需要大量 CPU、网络、存储等基础设施
>
> ↓
>
> **高端 Xeon 需求增加**
>
> ↓
>
> Intel DCAI 爆发

这才是 Intel **目前真正已经兑现的 AI 收益**。

---

## 6. 而且 DCAI 现在非常赚钱

这一点也值得注意。

2025 Q2：

> DCAI Revenue **$3.939B**
> Operating Income **$633M**
> Operating Margin **16%**

2026 Q2：

> Revenue **$6.262B**
> Operating Income **$2.474B**
> Operating Margin **40%**

也就是说营业利润：

**$6.33 亿 → $24.74 亿**

接近四倍。([英特尔][1])

Intel明确表示，这个利润改善主要来自**更高的服务器收入**。([英特尔][1])

这比 +59% 营收本身还重要。

因为这说明高端 Xeon 不仅带来收入，而且带来了非常强的利润杠杆。

---

# 所以现在我们可以把 DCAI 固定成这张图

> **DCAI — $62.62 亿**
>
> **① Server：约 $53.1 亿，约 85%**
>
> → 核心是 **Xeon CPU**
>
> → Q2 增长的绝对主力
>
> → hyperscaler / 企业 / 云 / 电信客户
>
> **② Other DCAI：$9.51 亿，约 15%**
>
> → ASIC / purpose-built silicon
>
> → Ethernet / NIC 等网络芯片
>
> → AI accelerator / 数据中心 GPU
>
> → 其他数据中心芯片

而且 Intel **没有继续公开把这 $9.51 亿拆成 ASIC、网络、GPU 各多少钱**，所以我们不能自己编一个比例。([英特尔][1])

最重要的结论只有一句：

> **Intel 2026 年 DCAI 的爆发，本质上首先是 Xeon 服务器 CPU 的爆发，而不是 Intel 自己的 AI GPU 爆发。**

这一下其实把我们前面“Intel 为什么受益于 AI”的问题推进了一大步。下一步真正值得研究的就是：**为什么 AI 时代大家已经疯狂买 NVIDIA GPU，却反而让 Intel Xeon CPU 价格上涨 48%、甚至供不应求？**这才是 Intel 最近业绩突然起来的核心机制。

[1]: https://www.intc.com/filings-reports/all-sec-filings/content/0000050863-26-000157/intc-20260627.htm "intc-20260627"
[2]: https://www.intc.com/filings-reports/all-sec-filings/content/0000050863-26-000011/intc-20251227.htm "intc-20251227"
