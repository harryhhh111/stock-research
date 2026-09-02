有，而且现在 Intel 的 PC 芯片竞争格局其实比几年前复杂很多。

如果我们研究的是 **Intel 的 Core / Core Ultra 这类 PC 处理器业务**，我会把竞争对手分成四档：

| 公司                    | 产品/架构                | 与 Intel 的关系         | 威胁程度        |
| --------------------- | -------------------- | ------------------- | ----------- |
| **AMD**               | Ryzen / Ryzen AI，x86 | 最直接的同类竞争            | **★★★★★**   |
| **Apple**             | M 系列，ARM             | 抢走整个 Mac 市场         | **★★★★★**   |
| **Qualcomm**          | Snapdragon X，ARM     | 进攻 Windows PC       | **★★★★**    |
| **NVIDIA + MediaTek** | RTX Spark，ARM        | 2026 新进入 Windows PC | **潜在★★★★★** |

### 第一名毫无疑问是 AMD

AMD 是 Intel **最直接、最传统的竞争对手**。

两家公司卖的东西几乎一一对应：

> Intel Core Ultra ↔ AMD Ryzen AI
> Intel Core ↔ AMD Ryzen
> Intel x86 ↔ AMD x86

而且 AMD 同样覆盖笔记本、台式机、游戏 PC、商用 PC 等市场。AMD 当前 Ryzen 产品仍然覆盖完整的 laptop 和 desktop 产品线。([AMD][1])

假设 Lenovo 要设计一款 Windows 笔记本，它通常可以选择：

> Lenovo Yoga
> → Intel Core Ultra

或者：

> Lenovo Yoga
> → AMD Ryzen AI

对于 OEM 来说，这是非常直接的替代关系。

所以以后分析 Intel PC 业务，**最重要的对标公司就是 AMD。**

---

### 第二个其实是 Apple，而且 Apple 对 Intel 造成过一次非常真实的重创

Apple 比较特殊，因为它**不把 M 芯片卖给 Dell、HP、Lenovo**。

它是：

> Apple 自己设计 M 系列芯片
> → 装进自己的 Mac
> → 卖整台电脑。

但这仍然是在抢 Intel 的 PC CPU 市场。

因为以前 Mac 是：

> MacBook
> **Intel CPU**

2020 年以后 Apple 开始转向 Apple Silicon，现在 MacBook Air、MacBook Pro、iMac、Mac mini 等产品已经全面采用 Apple 自己的芯片。([苹果支持][2])

这相当于：

> Intel 曾经拥有的一个大型 PC 客户
> ↓
> **直接消失了。**

而且 Apple Silicon 的意义还不只是丢了 Apple 这个客户。

它向整个行业证明了一件事：

> **高性能 PC 不一定非得用 x86。**

现在 MacBook Pro 已经发展到 M5 / M5 Pro / M5 Max，并继续强调性能、续航和本地 AI。([Apple][3])

这个事情给 Intel 带来的长期影响非常深。

---

# 第三个：Qualcomm

Qualcomm 是现在 Windows PC 市场非常值得 Intel 警惕的一家公司。

它原来大家最熟悉的是：

> Snapdragon
> → Android 手机

但现在 Qualcomm 已经正式把 Snapdragon 带入 PC。

主要产品：

**Snapdragon X 系列**

例如：

> Snapdragon X Elite
> Snapdragon X2 Elite / Extreme

它采用的不是 Intel/AMD 的 **x86**，而是 **ARM 架构**。Qualcomm 当前 Snapdragon X 产品已经明确覆盖 Windows 笔记本，并开始扩展到 mini desktop PC。([高通][4])

所以现在 Windows PC 已经变成：

**以前：**

> Windows
> ↓
> Intel / AMD x86

**现在：**

> Windows
> ↓
> Intel x86
> AMD x86
> **Qualcomm ARM**

这对 Intel 的意义非常大。

因为 Intel 过去几十年的核心护城河之一其实就是：

> **Windows + x86 生态。**

Qualcomm 如果把 Windows on ARM 真正做成熟，相当于是在攻击 Intel 一个非常底层的护城河。

---

# 第四个，而且是刚刚发生的大变化：NVIDIA

这个我们研究 Intel 时以后可能会非常重要。

截至 **2026 年 8 月**，NVIDIA 已经正式宣布进入 Windows PC 处理器市场。

今年 5 月底 NVIDIA 发布：

**RTX Spark**

这是一个：

> ARM CPU
>
> * NVIDIA Blackwell RTX GPU
> * AI Tensor Core

集成的 PC 芯片。

CPU 部分由 NVIDIA 与 **MediaTek** 合作设计。([NVIDIA Newsroom][5])

而且合作厂商不是几个小品牌，包括：

* Dell
* HP
* Lenovo
* ASUS
* Microsoft
* Acer
* Gigabyte
* MSI

计划从 **2026 年秋季**开始进入笔记本和小型桌面 PC。([NVIDIA][6])

这意味着 NVIDIA 不再只是：

> Intel CPU + NVIDIA GPU

以后它可能变成：

> **NVIDIA CPU + NVIDIA GPU**

直接把 Intel 从系统里拿掉。

这对 Intel 的潜在威胁其实非常大。

---

## 所以 PC CPU 行业已经发生了一个很重要的变化

如果我们倒退十几年：

**Windows PC CPU**

基本就是：

> **Intel**
>
> AMD

Intel 是绝对主角。

然后行业发生了三件事情：

### 第一波

AMD Zen / Ryzen 崛起：

> Intel
> ↓
> **AMD 抢份额**

但还是 x86 内战。

### 第二波

Apple Silicon：

> Intel x86
> ↓
> **Apple ARM**

证明 ARM 可以做高性能 PC。

### 第三波

现在：

> Qualcomm ARM
> NVIDIA + MediaTek ARM

开始直接进入 **Windows PC**。Qualcomm 当前已经有完整 Snapdragon X Windows PC 产品线，而 NVIDIA/MediaTek 的 RTX Spark 正准备在 2026 年秋季进入市场。([高通][7])

所以现在 Intel 面临的不再只是：

> **“我的 CPU 能不能打赢 AMD？”**

而是更深的一层：

> **“未来 PC 是否还必须使用 x86？”**

---

## 但这里有一个非常重要的区别

如果我们要研究 Intel 的实际营收风险，不能把这四家公司简单等权。

我现在会这样排：

**AMD = 最直接现实威胁**

因为同样是 x86，用户、OEM、软件基本不用换生态就可以从 Intel 换 AMD。AMD 自己也强调 Ryzen AI PRO 继续运行于成熟的 Windows x86 平台。([AMD][8])

**Apple = 已经造成巨大损失，但进一步增量影响有限**

因为 Apple 已经把 Mac 从 Intel 迁走了。未来 Apple Mac 卖得越多当然仍然会侵蚀 Windows PC，但 Intel 不会再“第二次失去 Apple CPU 订单”。([苹果支持][2])

**Qualcomm = 最大的现有架构级挑战者**

因为它正在证明：

> Windows + ARM

是可以商业化的。([高通][4])

**NVIDIA + MediaTek = 最大的新变量**

因为 NVIDIA 不仅有 CPU，还有 GPU、CUDA 和 AI 生态；RTX Spark 已经宣布，但截至现在大规模 PC 产品仍计划从 2026 年秋季开始上市，因此它对 Intel 的实际份额冲击还需要观察。([NVIDIA Newsroom][5])

---

所以如果我们接着研究 Intel，我认为**下一步最应该先研究 AMD**。

因为 Intel PC 业务过去五年到底发生了什么，最简单的问题就是：

> **PC 市场本身有没有萎缩？**
>
> 还是
>
> **Intel 的东西卖不动，是因为 AMD 把它的份额抢走了？**

这两个答案对 Intel 的投资逻辑完全不同。

[1]: https://www.amd.com/en/products/processors/laptop/ryzen.html?utm_source=chatgpt.com "AMD Ryzen™ Processors for Laptops"
[2]: https://support.apple.com/en-us/116943?utm_source=chatgpt.com "Mac computers with Apple silicon"
[3]: https://www.apple.com/sg/macbook-pro/?utm_source=chatgpt.com "MacBook Pro - Apple (SG)"
[4]: https://www.qualcomm.com/snapdragon/laptops?utm_source=chatgpt.com "Snapdragon X Series Laptops"
[5]: https://nvidianews.nvidia.com/news/nvidia-microsoft-windows-pcs-agents-rtx-spark?utm_source=chatgpt.com "NVIDIA and Microsoft Reinvent Windows PCs for the Age ..."
[6]: https://www.nvidia.com/en-sg/products/rtx-spark/?utm_source=chatgpt.com "Slim Laptops & Small Desktops | NVIDIA RTX Spark"
[7]: https://www.qualcomm.com/snapdragon/laptops-and-tablets?utm_source=chatgpt.com "Snapdragon Laptops & Tablets | Performance, AI, Battery Life"
[8]: https://www.amd.com/en/products/processors/laptop/ryzen-for-business.html?utm_source=chatgpt.com "Ryzen Processors for Business Laptops"
