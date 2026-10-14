# 1GW AI 数据中心 SSD 需求模型：本地 SSD / CMX / 共享存储

> 整理/核对日期：2026-08-21。由 `SSD.md` 与 `CMX.md` 合并而成。
> 研究动机：判断 Rubin 时代 NAND 需求（铠侠/Samsung/Micron），必须把 SSD 拆成三层，不能混为一个数字。
> 2026-09-15 更新：2/4/8/16TB/GPU 的 CMX 情景现已补充为可复算的 KV 分层推导，见 [KV缓存分层需求测算.md](KV缓存分层需求测算.md)。

## 0. 三层框架

| 层 | 内容 | 能否按 GPU 固定配置 |
|---|---|---|
| **① 普通本地 NVMe SSD** | compute tray 内 data/cache 盘 + boot 盘 | ✅ 可以，每 tray 固定 |
| **② CMX Context SSD** | KV Cache 专用共享存储（BlueField-4 STX / CMX rack） | ⚠️ 取决于推理负载形态，是情景变量 |
| **③ Shared AI Storage** | checkpoint / 训练数据 / 共享文件与对象存储 | ❌ 不能——NVIDIA 明确随模型、dataset、性能目标高度变化，WEKA 的 GB300 参考设计按吞吐量而非固定 TB/GPU 配置。([NVIDIA Docs][7]) |

**核心结论先行**：排除 CMX 后，Rubin 普通本地 SSD 需求**反而低于** GB300（每 GW GPU/tray 数减少约 35%）；市场上"Rubin 拉动 SSD 暴增"的叙事，几乎全部来自第②层 CMX。

---

## 1. 第①层：普通本地 NVMe SSD

### GB300：~2.0–3.9 EB / GW

1GW GB300 ≈ 46 万 GPU ≈ 6,390 个 NVL72 rack ≈ **115,000 个 compute tray**（1 tray = 4 GPU）。NVIDIA 有两种公开配置：

| 配置 | 每 tray | 1GW 容量 | 1GW SSD 块数 |
|---|---|---:|---:|
| DGX GB300 实际配置 | 4×3.84TB E1.S + 1×1.92TB M.2 = **17.28TB，5块** ([NVIDIA Docs][1]) | **~1.99 EB** | **~57.5万** |
| Enterprise RA 高配 | 8×4TB E1.S + 1×2TB M.2 = **34TB，9块** ([NVIDIA Docs][2]) | **~3.91 EB** | **~103.5万** |

### Rubin：~1.3 EB / GW（估算）

- GIGABYTE 已公布 Vera Rubin NVL72 compute tray 实物规格：**4 × E1.S Gen6 data 盘位 + 1 × E1.S Gen5 boot 盘位 = 5 块普通 NVMe / tray**，每 rack 18 tray = **90 块**。([GIGABYTE][3])
- **容量未公布**——只公布了盘位数。用 GB300 典型容量做透明假设（4×3.84TB + 1×1.92TB = 17.28TB/tray；若未来上 4TB+2TB 则 18TB/tray）。
- GPU 基数采用 NVIDIA GTC 2026 官方 1GW Vera Rubin 尺度 **~30 万 GPU/GW**([2Slides][5])：→ 4,167 rack → **75,000 tray** → **~37.5 万块 SSD** → **~1.30 EB/GW**（估算值，非官方容量）。
  - ⚠️ 口径注意：30 万对应"训练为主"场景；`../数据中心/数据中心1GW.md` 的完整 Agentic 型（Supermicro 蓝图）为 23 万 GPU/GW，若用该口径本地 SSD 按比例降至 ~1.0 EB。

### 两代对比（第①层）

| 1 GW IT | **GB300** | **Vera Rubin** |
|---|---:|---:|
| GPU | ~460k | ~300k |
| Compute tray | ~115k | ~75k |
| 普通 SSD / tray | 5～9 | **5** |
| 普通 SSD 块数 | ~57.5万～103.5万 | **~37.5万** |
| 普通本地 SSD 容量 | **~2.0–3.9 EB** | **~1.3 EB（估算）** |

同口径（5 块/tray）比较：1.99 EB → 1.30 EB，**下降约 35%**。原因：每 tray 普通 SSD 数没增加，但 Rubin 每 GW 的 tray 数少了 35%。

---

## 2. 第②层：CMX 是什么

**CMX（Context Memory eXtension / Context Memory Storage）**是 NVIDIA 2026 年推出的上下文内存存储平台，专为 **AI 推理 KV Cache** 设计的新型存储层。([英伟达][8])

- **定位**：HBM 太贵太小、普通 SSD 太慢不懂 AI，CMX 在两者之间加一层 **Pod 级共享**的 context tier——不只单张 GPU 用，整个 Pod 都能访问。
- **硬件组成**：NVMe SSD + BlueField-4 DPU + Spectrum-X 网络 + 软件栈（DOCA/Dynamo）。BF-4 直接负责数据搬运、存储服务、加密和完整性检查，尽量避免 CPU 介入；Dynamo 知道每个请求的 KV Cache 在哪，把请求调度到合适的 GPU。
- **不是给模型参数扩内存**：1T 参数模型装不进 GPU，不能简单"把权重放 CMX"。CMX 核心用途是 KV Cache / inference context。
- **官方宣称收益**：KV-cache 密集、长上下文、Agentic 推理场景下最高 **~5× tokens/s、~5× 能效**——不是说 GPU 本身快 5 倍，而是减少 GPU 等数据和重复计算。([NVIDIA Developer][9])

类比：**HBM = GPU 的工作台；CMX = 旁边存放"进行中的 AI 思考状态"的高速仓库；普通 SSD/HDD = 长期档案库。**

```
                 AI Pod
        ┌───────────┴───────────┐
   Rubin GPU Rack          Rubin GPU Rack
        │  HBM                   │  HBM
        └──────────┬────────────┘
              Spectrum-X
          ┌────────▼────────┐
          │   CMX / KV Cache │
          └────────┬────────┘
               NVMe SSD
```

**市场上流传的"16TB SSD/GPU、1.152PB NAND/Rubin rack"就是这一层**（Context Memory/ICMS），与第①层本地 SSD 是两回事，不能混算。([IT之家][4])

---

## 3. CMX 容量怎么定：情景模型

基准假设：1GW Rubin ≈ 30 万 GPU，其中 **50% 长期用于推理** → **15 万推理 GPU**。按一台 STX/CMX rack 有效容量 ~9.2PB 换算：

| 推理负载形态 | CMX / 推理GPU | 总 CMX 容量 | 约 CMX rack | 推理NVL72 : CMX rack |
|---|---:|---:|---:|---:|
| 普通聊天/API 为主 | 2TB | 300PB | ~33 | ~63 : 1 |
| **混合推理（base case）** | **4TB** | **600PB** | **~65** | **~32 : 1** |
| Agent / 长上下文较多 | 8TB | 1.2EB | ~130 | ~16 : 1 |
| NVIDIA Agentic 满配 | 16TB | 2.4EB | ~260 | ~8 : 1 |

**为什么 base case 选 4TB 而不是 NVIDIA 的 16TB**：

- 一颗 Rubin GPU 只有 288GB HBM4。4TB CMX ≈ **14× HBM** 的 warm context 池；8TB ≈ 28×；16TB ≈ **56×**。
- 如果一半 GPU 做推理、且推理里混有搜索/代码补全/图片/短对话/RAG 等大量短生命周期任务，给所有推理 GPU 配 56× HBM 的 KV Cache 存储明显激进。
- 16TB/GPU 只在"大量长期运行 Agent、几十万到几百万 token context、暂停几小时后恢复、旧 KV Cache 仍值得保存"的世界里成立。NVIDIA 的 16TB 更像展示 CMX 扩展能力上限，而非所有 GPU 必须满配。([英伟达][8])
- 普通 ChatGPT 式请求（几十 K context、会话结束后 KV 很快失去价值）根本不需要几 TB CMX。

### ⚠️ 待决策参数（两版口径不一致，暂不收敛）

- **口径 A（本文件 base case，原 CMX.md）**：15 万推理 GPU × 4TB = **0.6EB**，~65 rack。理由如上。
- **口径 B（原 SSD.md 附加段）**：推理占 2/3 = 20 万 GPU，其中一半需要 CMX = 10 万 GPU × **16TB** = **1.6EB**。
- 差异来自两个参数：推理 GPU 占比（50% vs 2/3×1/2）和单 GPU CMX 配置（4TB vs 16TB）。**在找到 CoreWeave / Nebius / NVIDIA 实际部署披露之前，两个口径都保留，预测 NAND 需求时以情景区间呈现。**

---

## 4. 汇总：1GW SSD 总需求

| SSD 用途 | GB300 | Rubin（口径A base） | Rubin（口径B） |
|---|---:|---:|---:|
| ① 本地 SSD | ~2.0 EB（5块/tray口径；高配3.9） | ~1.3 EB | ~1.3 EB |
| ② CMX Context SSD | 无 | ~0.6 EB | ~1.6 EB |
| ③ Shared Training Storage | ~0.1 EB | ~0.1 EB | ~0.1 EB |
| **合计** | **~2.1 EB** | **~2.0 EB** | **~3.0 EB** |

（③为粗略量级，本身不按 GPU 固定配置，仅供参考。）

**对 NAND/铠侠研究的关键含义**：

1. **如果 CMX 不大规模部署，Rubin 本身不会把普通 NVMe 需求拉爆**——反而比 GB300 少 35%。巨大的新增 NAND 假设几乎全部压在 CMX 一层。
2. 口径 A 下 Rubin 总 SSD 与 GB300 基本持平；口径 B 下高 ~40%，**增量全部来自 CMX**。
3. 下一步：把 0.6–1.6EB 的 CMX 区间换算成 NAND bit、占全球年度 NAND bit demand 比例、对铠侠的收入弹性——这才是判断 CMX 产业影响的关键一步。
4. 持续跟踪 NVIDIA / CoreWeave / Nebius 实际 CMX/STX 部署披露，验证现实配置更接近 2TB、4TB 还是 16TB/GPU。

[1]: https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html?utm_source=chatgpt.com "Hardware — NVIDIA DGX GB Rack Scale Systems User Guide"
[2]: https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/appendix-node-configurations.html?utm_source=chatgpt.com "Appendix B – Node Configurations — NVIDIA NVL72 AI Factory"
[3]: https://www.gigabyte.com/us/Enterprise/GIGAPOD-Rack-Scale/AI-DLC-Rack_NVIDIA-Vera-Rubin-NVL72?utm_source=chatgpt.com "NVIDIA Vera Rubin NVL72 GIGAPOD AI DLC Rack Scale Solution - GIGABYTE U.S.A."
[4]: https://www.ithome.com/0/912/680.htm?utm_source=chatgpt.com "NAND 涨价警告：花旗预测英伟达 Vera Rubin AI 系统将推动 PB 级 SSD 需求 - IT之家"
[5]: https://2slides.com/de/gallery/nvidia-gtc-2026-keynote-deck-jensen-huang-ai-factory-vision?utm_source=chatgpt.com "NVIDIA GTC 2026 Keynote Deck | 2Slides"
[7]: https://docs.nvidia.com/dsx/ncp/software-reference-guide/data-center-architecture?utm_source=chatgpt.com "Data Center Architecture | NVIDIA DSX Documentation"
[8]: https://www.nvidia.com/en-us/data-center/ai-storage/cmx/?utm_source=chatgpt.com "NVIDIA CMX Context Memory Storage Platform | NVIDIA"
[9]: https://developer.nvidia.com/blog/?p=111143&utm_source=chatgpt.com "Introducing NVIDIA BlueField-4-Powered CMX Context Memory Storage Platform | NVIDIA Technical Blog"
