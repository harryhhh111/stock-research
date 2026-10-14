# KV cache 分层需求测算：从并发与上下文推导 HBM / DRAM / SSD

> 整理/核对日期：2026-09-15。数据截止：2026-09-15。  
> 复算脚本：[factcheck/kv_tier_model.py](factcheck/kv_tier_model.py)。  
> 目的：把 `SSD与CMX需求模型.md` 中 2/4/8/16TB/GPU 的 CMX 情景，改写成可被并发、上下文、模型架构和缓存保留期检验的容量链条。
> **2026-09-16 口径更正：** 第 2 节的“10,000 活跃请求”表是**教学型敏感性演算，不是市场需求预测**。其中 10,000 并发、8K/32K/128K context 与 DRAM/SSD 倍数均非运营商披露；不得用于 Sandisk/Kioxia 的基准收入、NAND bit 或 CMX 装机预测。

## 结论

**可以外推，但 HBM、DRAM、SSD 之间没有固定配比。** 只有 HBM 活跃 KV 可由“同时 decode 的会话数 × 每会话已缓存 token × 每 token KV 字节”直接计算；DRAM 和 SSD 取决于有多少已退出 HBM 的 KV 在多长时间内仍值得重用。高并发本身只推高 HBM，不能自动推高 SSD。

对 Sandisk / CMX 投资叙事，最关键的参数不是“AI 请求数”，而是：

`SSD persistent KV = active sessions × cached tokens/session × KV bytes/token × retained-and-reusable multiple`

最后一个 `retained-and-reusable multiple`（保留且可复用倍数）尚没有 hyperscaler 公开实测；因此结果必须是情景区间，而不能写成市场事实。

## 1. 先算每 token 有多大：模型架构决定数量级

常规 GQA 模型的 BF16 KV 字节数为：

`2(K 与 V) × layers × KV heads × head dimension × 2 bytes`

以 Llama-3.1-70B 为例：80 层、8 个 KV heads、每 head 128 维，因此：

`2 × 80 × 8 × 128 × 2 = 327,680 bytes/token = 320 KiB/token`

即单个 128K-token 请求约 **40 GiB** 逻辑 KV。配置可见 [Llama 3.1 70B 的开源配置](https://huggingface.co/meta-llama/Llama-3.1-70B-Instruct/raw/main/config.json)；KV 随 context 线性增长也由 Meta 的推理工程文章明确说明。[Meta](https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/)

但不能把这一数字套给所有模型。DeepSeek-V3 的 MLA 将每层每 token 存储压缩为 `512 latent KV + 64 RoPE = 576` 个 BF16 元素：

`61 × 576 × 2 = 70,272 bytes/token = 68.625 KiB/token`

因此其 128K-token 请求约 **8.6 GiB** KV，约为上述 Llama GQA 例子的五分之一。这个差异说明，模型架构（GQA、MLA、KV quantization）会直接改变存储 TAM，而参数量、token 数或 GPU 数本身都不足以推算 KV。[DeepSeek-V3 配置](https://huggingface.co/deepseek-ai/DeepSeek-V3/blob/main/config.json)；[DeepSeek MLA 技术报告](https://arxiv.org/abs/2412.19437)

## 2. 教学型敏感性演算：每 10,000 个同时活跃请求（非市场预测）

**这张表的目的仅是展示变量的数量级和线性关系。** 容量为逻辑 KV，不含 SSD over-provisioning、RAID/纠删码、跨节点副本和缓存索引开销。所有情景均设 10,000 个正在 decode 的会话；这只是易读的归一化分母，**没有任何公开资料显示某家运营商以此作为平均或峰值并发**。DRAM / SSD 乘数也是为说明“保留倍数的影响”而人为设定，非厂商披露。

| 输入项 | 表中取值来自哪里 | 可靠性 | 可否用于预测 |
|---|---|---|---|
| Llama-3.1-70B / DeepSeek-V3 的 layer、KV head、head dim / MLA latent dim | 模型公开配置；自己复算 | **高**：对指定模型、BF16 的逻辑 KV bytes/token 有效 | 可作为模型层面的物理输入；仍需按实际 KV dtype、实现和版本更新 |
| bytes/token → 单请求 / active HBM logical KV | 公开配置 × 明确算术 | **高**：只要上述模型、精度、token 数成立 | 可作上限/工作集测算，不能直接推经营需求 |
| 10,000 simultaneously decoding sessions | 为读表方便而选的 round number | **无外部验证** | **不可**；只能线性替换为真实并发 |
| 8K / 32K / 128K cached context | 三种假设工作负载 | **低至中**：技术上合理，缺乏运营商分布数据 | 不可作为行业均值 |
| DRAM warm multiple 0.25× / 1× / 2× | 我为演示分层而设 | **低** | 不可；需用 workload trace 的 lifetime / reuse gap 校准 |
| SSD persistent multiple 0.05× / 2× / 10× | 我为演示分层而设 | **低**，也是结果最大驱动项 | **不可**；不得写入 CMX/NAND base case |

以第一行 Llama 短对话为例，唯一的“硬计算”是：

`10,000 × 8,192 tokens × 327,680 bytes/token ÷ 2^40 = 24.4 TiB active logical KV`

其后的 `6.1 TiB DRAM = 24.4 × 0.25`，`1.2 TiB SSD = 24.4 × 0.05`，只是把人为倍数代入，并不构成对真实机房的测量。

| 假设工作负载 | 假设的每会话 cached context | **人为设定** DRAM warm KV / active KV | **人为设定** SSD persistent KV / active KV | 设定目的 |
|---|---:|---:|---:|---|
| 短对话 / 共享前缀 | 8K | 0.25× | 0.05× | 短 TTL，绝大部分会话结束即失效；主要价值是 HBM 中的 prefix reuse。 |
| RAG、代码与多轮会话 | 32K | 1× | 2× | 热会话之外保留一批可复用文档、对话或代码上下文。 |
| 长上下文、长期 Agent | 128K | 2× | 10× | 显式假设：有十倍于活跃工作集的已退出 KV 仍会被再次调用。 |

| 模型 / 假设场景 | 活跃 HBM logical KV（模型配置 × 假设并发/上下文） | warm DRAM logical KV（再乘人为倍数） | persistent SSD logical KV（再乘人为倍数） |
|---|---:|---:|---:|
| Llama-3.1-70B GQA / 短对话 | 24.4 TiB | 6.1 TiB | 1.2 TiB |
| Llama-3.1-70B GQA / RAG、代码 | 97.7 TiB | 97.7 TiB | 195.3 TiB |
| Llama-3.1-70B GQA / 长上下文 Agent | 390.6 TiB | 781.2 TiB | 3.81 PiB |
| DeepSeek-V3 MLA / 短对话 | 5.2 TiB | 1.3 TiB | 268.1 GiB |
| DeepSeek-V3 MLA / RAG、代码 | 20.9 TiB | 20.9 TiB | 41.9 TiB |
| DeepSeek-V3 MLA / 长上下文 Agent | 83.8 TiB | 167.5 TiB | 837.7 TiB |

这张表**只能**支持以下两个技术结论，不能支持任何具体市场容量结论：

1. **长上下文 + 高并发确实可迅速把活跃 KV 推到数十至数百 TiB。** 这首先是 HBM 和 DRAM 的容量/带宽问题。
2. **SSD 的 3.81PiB 并不是由“10,000 并发、128K context”自动得来的，而是来自“保存 10 倍 active workset”的假设。** 如果会话结束即丢弃，SSD 一项接近零；如果保留期或复用率扩大，SSD 线性上升。
3. **同一流量下 MLA 把容量压低约 4.7 倍。** 若主流模型向 MLA、低位宽 KV 或更激进的 eviction 演进，Sandisk 所假设的存储强度会被明显压低。

公开产品能力只支持“多轮/RAG/长文档会产生可复用上下文”，不提供全网的保留倍数：OpenAI 的共享 prompt cache 通常闲置 5–10 分钟清除、最长一小时；Gemini 显式 cache 默认 TTL 一小时；Claude 提供 5 分钟与一小时两档。[OpenAI](https://openai.com/index/api-prompt-caching/)；[Gemini](https://ai.google.dev/gemini-api/docs/generate-content/caching)；[Anthropic](https://platform.claude.com/docs/en/about-claude/pricing)

因此，**现阶段不能用第 2 节的 3.81PiB、837.7TiB 或任何其派生数，声称“10,000 个长 context agent 会需要这么多 SSD”。** 它们应当仅被保留为“若保留倍数为 X，容量将线性等于 Y”的灵敏度函数。要升格为研究输入，必须由真实 workload trace（active concurrency、context-length distribution、TTL、reuse gap、hit rate、SSD write/read bytes）替换假设。

### 2.1 公开可复核的实测/配置：有，但不是运营商全网遥测

用户所问的“某模型、某配置下，多少并发占用多少 HBM/DRAM”，**已有一部分公开答案**，主要来自开源框架、云厂商 demo 与硬件商联合验证。到 2026-09-16，仍未找到 OpenAI、Google、Anthropic 等运营商披露的同一生产集群的“请求并发 × HBM 实占 × DRAM 实占 × SSD 实占”全套遥测。因此下表的用途是锚定数量级与验证计算式，**不能混合后求一个行业平均值**。

| 公开案例 | 模型与测试配置 | 并发 / 请求数据 | 已公开的 HBM / DRAM / 存储数据 | 证据强度与不能推出的内容 |
|---|---|---|---|---|
| IBM、Supermicro、NVIDIA 联合测试（2026） | `openai/gpt-oss-120b`，MXFP4 weights；单张 RTX PRO 6000 Blackwell 跑 vLLM/Dynamo，GPU memory utilization 90% | **28 并发连接**、200 requests；100 个 prompts、合计 2,400 万 tokens、825GB KV 数据 | weights + CUDA graph 约 **60.9GiB**；GPU KV pool **19.6GiB**，可存 **1,141,783 tokens**。client 的物理 host DRAM 是 768GB，但 G2 DRAM cache 被设为 0；KV 全部走 G4 共享 flash 存储。 | **较强但为供应商联合基准**：同一测试同时给出了模型、HBM KV、并发和 external KV 数据；768GB 是机器物理内存，绝不能写成“DRAM KV 占用 768GB”。 |
| vLLM / Mooncake Store 的 agent trace（2026） | Kimi K2.5，NVFP4；prefill TP4、decode DP8+EP；12 张 GB200 的 1P1D 部署 | 610 条 Codex/GPT-5.4 SWE-bench Pro agent traces；30 turn 后中位 context 约 80K；在 12→60 张 GB200 合成扩展试验中，75–375 concurrent sessions | 作者给出一个换算锚：**Kimi K2.5 的 100K-token FP8 KV 约 3.8GB**。并报告 shared cache hit 1.7%→92.2%、吞吐 3.8×。 | **对工作负载形状很有价值**，但未披露每个节点实际分配多少 DRAM；文章明确把 distributed disk offload 列为未来工作，因此不能当作 SSD 容量证据。 |
| vLLM / Novita PegaFlow（2026） | 8 个 Qwen3-8B 实例，8× RTX 5090、TP8；另一组为 DeepSeek-V3.2 MLA、TP8 | shared pool 下 Qwen3-8B 11.97 req/s、hit 52.35%；DeepSeek 1.81 req/s、hit 97.23%（文章未披露对应 trace 的活跃请求数和 context 分布） | host 共享 KV pool **500GiB**；对照为 8×62.5GiB isolated pool。SSD 仅给出 L3 local-disk 读带宽约 6.5–6.9GB/s，非 SSD KV 实际占用量。 | **工程案例而非全栈容量表**：可证明 DRAM pool 的实际配置和性能差异，不能从 500GiB 推出线上平均并发或 NAND 消耗。 |
| AWS HyperPod / Curvine demo（2026） | Qwen2-7B-Instruct，`max-model-len=16,384`、TP=1、每 pod 1 GPU、两 pod 跨节点复用 | 一个 **1,925-token** prompt 跨 pod 取回；不是并发压测披露 | 写入共享层 **0.1028GB / 10.71ms**，另一 pod 读取 **1,925 hit tokens / 55.75ms**；未给 HBM / DRAM pool 实占 | **小规模、可复核 demo**：证明跨 pod KV 可以写入和读取，不能用于 70B/120B 或运营商集群的 HBM/DRAM 推算。 |

最接近你要的“全字段”的是 IBM 的一项：它的正确读法是“**一个指定模型和指定 GPU、在指定 HBM pool 下，28 并发跑了 200 个请求；下层 storage 承接 825GB KV**”，而不是“120B 模型必然每 28 并发需要 825GB SSD”。IBM 的文中还给出了**估计**口径：GQA 的 Llama 3.1 70B 在 128K token 约 40GB KV/request，120B 在 130K 约 60–80GB/request；这和第 1 节由模型配置复算的逻辑相符，但它是 sizing guide，不是大模型运营商遥测。[IBM/Supermicro/NVIDIA 测试与配置](https://www.redbooks.ibm.com/docs/MD260021/MD260021.html)；[Mooncake trace](https://vllm-project.github.io/2026/05/06-mooncake-store/)；[PegaFlow](https://vllm-project.github.io/2026/05/18/pegaflow.html)；[AWS demo](https://aws.amazon.com/blogs/machine-learning/scale-ai-inference-with-amazon-sagemaker-hyperpod-and-lmcache/)

从研究方法上，今后应把公开资料拆成三个问题分别回答：

1. **模型物理量**：模型配置可严谨地推导 `KV bytes/token`，这一层可靠性最高。
2. **线上工作负载**：并发、context-length 分布、turn 数、reuse gap、TTL，是决定 HBM/DRAM/SSD ratio 的核心，但运营商几乎不披露；开源 trace 只能作为场景参照。
3. **系统部署**：DRAM/SSD pool 大小通常是运维策略和成本/延迟 SLO 的选择，并不是模型“天然需要”的固定配比。即便一个案例采用 500GiB DRAM，也不能外推为每张 GPU 或每个请求的标准 BOM。

### 2.2 正确推导 HBM : DRAM，而不是假定一个行业配比

本研究需要的不是整机 `physical HBM : physical DRAM`，而是下列可比较的容量比：

`R = warm-KV DRAM capacity ÷ active-and-hot KV HBM capacity`

分母必须**扣除模型权重、CUDA graph、通信 buffer 和碎片预留**。例如 IBM 的 120B 测试中，GPU 的总显存不是 19.6GiB，而真正可给 KV 的 HBM pool 才是 19.6GiB；把 host 的 768GB DRAM 直接除以 GPU 总显存，会得到没有经营意义的数字。[IBM/Supermicro/NVIDIA](https://www.redbooks.ibm.com/docs/MD260021/MD260021.html)

推导顺序应为：

1. **先锁定 HBM 工作集，而非先定 DRAM。** 对每个 GPU/TP group，计算 `weights shard + runtime reserve + active decode KV + hot prefix KV`。剩余 HBM 才是 KV pool。`active decode KV` 由真实的 simultaneous decoding sessions 和各自 cached tokens 算出。
2. **用 trace 把“已离开 HBM 的 KV”按下一次复用时间分桶。** 若一段 KV 的下一次复用早于 HBM eviction 阈值，留 HBM；若落在可预取窗口内，才值得留 DRAM；若复用很晚或概率很低，应当丢弃或放低层存储。形式化地说：`DRAM warm KV = Σ(KV bytes_i | T_HBM < reuse_gap_i ≤ T_DRAM 且 expected saved-prefill_i > transfer cost_i)`。
3. **以 P95 而非平均值配置容量。** 平均并发下的 ratio 会掩盖 agent burst；对每 1 分钟/5 分钟窗口分别算 HBM active occupancy 与 DRAM warm occupancy，取满足 TTFT SLO 的 P95/P99，并预留索引、复制和故障转移空间。

因此，ratio 的经济含义很清楚：`R=2` 不是“每 GB HBM 配 2GB DDR”，而是“在 HBM 正承载 1 单位活跃/热 KV 时，另有 2 单位历史 KV 在 DRAM 中仍有足够复用价值”。它首先取决于多轮会话和 prefix reuse，而不是模型参数量。

| 工作负载形状 | 在尚无客户 trace 时可用于实验的**起始假设** | 对 ratio 的方向 | 不能把它当成 |
|---|---|---|---|
| 一次性短问答、低 reuse | 少量 hot prefix；短 idle TTL | `R` 可能接近 0–1× | “AI 推理必然需要大 DRAM cache” |
| RAG、代码补全、多轮对话 | 复用共享文档 / system prompt；session 会短暂回访 | 可先测试 `R=1–3×` | 行业平均或 BOM 标准 |
| 长上下文 Agent、跨 replica 路由 | 长会话、有工具循环、历史 prefix 可在多个 worker 使用 | 应测试 `R=3–6×`；再大的冷库存通常须由 SSD/共享层承担 | HBM 不足可以无限用 DRAM 替代 |

上表是**待验证的敏感性区间，不是公开运营商数据**。公开材料只能证明其两端的工程可行性：Mooncake 的 agent trace 显示 30 turn 后 context 中位数约 80K，说明长会话可能形成很大的 warm inventory；PegaFlow 实际配置过 500GiB shared host KV pool，说明 DRAM pool 可以被设成远大于单个 GPU 的 KV pool，但二者均没有公布足以计算最终 `R` 的生产 trace。[Mooncake](https://vllm-project.github.io/2026/05/06-mooncake-store/)；[PegaFlow](https://vllm-project.github.io/2026/05/18/pegaflow.html)

要将区间收敛为公司研究可用的结论，最短路径是 replay 一条公开 agent trace（如 Mooncake 所用 SWE-bench Pro 多轮轨迹），在固定模型、TP、KV dtype 和目标 SLO 下记录：`active cached tokens`、`GPU eviction time`、`reuse gap CDF`、`DRAM hit rate` 和 `H2D prefetch latency`。这将直接给出 `R` 的 P50/P95；之后才能再问“高于该 ratio 的冷 KV 中，有多少值得进入 SSD”。

### 2.3 直接算例：1,000 个并发 agent 在 GB200 / GB300 / Vera Rubin NVL72

下面不再假设 10,000 请求。采用 Mooncake 公布的 610 条 agent trace 的两个输入：初始 context 约 12K token、每 turn 平均新增 2,242 token；因此一个 agent 在第 `t` 轮后的缓存 token 近似为：

`C(t) = 12,000 + 2,242 × t`

第 30 轮为 79,260 token，恰好与该 trace 披露的约 80K 中位 context 交叉核对。**以下假定 1,000 个 agent 都仍活跃、都保留全量 KV**，故是 1,000 并发下的 KV 工作集上限；agent 正在等工具调用、已结束或被淘汰的情形会更低。

| 每 agent 已完成轮数 | 每 agent cached tokens | 1,000 agent 合计 tokens | Llama-3.1-8B GQA、BF16（128KiB/token） | Llama-3.1-70B GQA、BF16（320KiB/token） | DeepSeek-V3 MLA、BF16（68.625KiB/token） | Kimi K2.5、FP8（100K token ≈3.8GB） |
|---:|---:|---:|---:|---:|---:|---:|
| 10 | 34,420 | 34.420M | **4.10TiB** | **10.26TiB** | **2.20TiB** | **1.308TB** |
| 20 | 56,840 | 56.840M | **6.78TiB** | **16.94TiB** | **3.63TiB** | **2.160TB** |
| 30 | 79,260 | 79.260M | **9.45TiB** | **23.62TiB** | **5.07TiB** | **3.012TB** |
| 33（trace 中位 turn 数） | 85,986 | 85.986M | **10.25TiB** | **25.63TiB** | **5.50TiB** | **3.267TB** |
| 50 | 124,100 | 124.100M | **14.79TiB** | **36.98TiB** | **7.93TiB** | **4.716TB** |
| 100 | 236,200 | 236.200M | **28.16TiB** | **70.39TiB** | **15.10TiB** | **8.976TB** |

四列与第 2.4 节 10,000-agent 放大情景采用**完全相同的模型与 KV 字节口径**：Llama-8B / 70B 来自公开配置复算，DeepSeek-V3 来自 MLA 配置复算，Kimi 列直接按 Mooncake 披露的 FP8 byte/token 换算。巨大差异不是计算误差，而是 GQA、MLA、KV dtype 与模型配置不同；**不能把任一列当作所有“大模型”的 KV 强度**。[Llama-3.1-8B config](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct/raw/main/config.json)；[Llama-3.1-70B config](https://huggingface.co/meta-llama/Llama-3.1-70B-Instruct/raw/main/config.json)；[DeepSeek-V3 config](https://huggingface.co/deepseek-ai/DeepSeek-V3/blob/main/config.json)；[Mooncake trace 与 Kimi KV 锚点](https://vllm-project.github.io/2026/05/06-mooncake-store/)

按项目内 [`NVDA/平台与机柜对比.md`](../NVDA/机柜与架构/平台与机柜对比.md) 的整柜参数，1,000 agent / 30 turn 的 **23.62TiB Llama-70B BF16 KV** 与三代 rack 的容量关系如下。这里的“单 rack HBM 占用”是假设硬塞到一个 rack；已明显超过一柜容量。表中的 raw rack 数仅为容量下限，未扣模型权重和 runtime。

| 72-GPU rack | 整柜 HBM | 整柜 CPU DRAM | **物理 HBM:DRAM** | 单 rack 容纳 30-turn KV？ | raw HBM 容量下限 | 纯 KV 达到单 rack raw HBM 的轮数* |
|---|---:|---:|---:|---:|---:|---:|
| GB200 NVL72 | 13.4TB | 17.0TB | **1 : 1.27** | **否**；23.62TiB = raw HBM 的 194% | **2 rack**（实际至少 3） | ~13 turn |
| GB300 NVL72 | 20.7TB | 17.3TB | **1 : 0.84** | **否**；23.62TiB = raw HBM 的 125% | **2 rack** | ~23 turn |
| Vera Rubin NVL72 | 20.7TB | 54.0TB | **1 : 2.61** | **否**；23.62TiB = raw HBM 的 125% | **2 rack** | ~23 turn |

\* 采用同一条 `KV(T) = 3.576TiB + 0.668TiB × T` 曲线，**未扣模型权重、runtime、fragmentation 或 batch headroom，故只可看作物理上限，不能用于生产配置**。实际可用 HBM 拐点会更早。

因此，在 Llama-70B 的高 KV 强度假设下，1,000 个 agent 到第 30 轮共 23.62TiB KV，**一台 GB200、GB300 或 Vera Rubin NVL72 都放不下**。纯 HBM 的数学下限是 2 柜；但 GB200 若以两个 rack、18 个 TP=8 replica 分摊，KV 已约 168GiB/GPU，几乎吃完约 186GB HBM，连 70B 权重分片都放不下，所以至少需要 3 柜或采用 KV quantization/offload。GB300/Rubin 的 288GB/GPU 在 2 柜下尚有约 100GiB/GPU 留给模型与 runtime，是否足够仍取决于实际 serving 配置。Rubin 相比 GB300 并不增加 HBM bit，却将 CPU DRAM 从 17.3TB 跳至 54TB、HBM 带宽大幅增加；这才是其更适合 agent warm-cache/offload 的硬件变化。Kimi FP8 情景下 30 turn 是 3.012TB KV，一柜就可容纳纯 KV，但仍需为模型权重与 runtime 预留空间。[GB200 NVL72 规格](https://www.nvidia.com/en-in/data-center/gb200-nvl72/)；[Vera Rubin NVL72 规格](https://www.nvidia.com/en-eu/data-center/dgx-vera-rubin-nvl72/)

反过来，若将 1,000 个 30-turn Llama 请求只压在一个 TP=8 group，23.62TiB KV 是 GB200 8 GPU 原始 HBM（约 1.35TiB）的 17 倍、GB300/Rubin 的 8 GPU 原始 HBM（约 2.30TB）的约 10 倍；必然需要更多 replica/rack、KV quantization、DRAM offload，或淘汰重算。结论是：**1,000 并发开始，KV 是否进 DRAM 的分水岭不再是“一个 rack 有没有内存”，而是单个 TP replica 分配多少 agent，以及需要保留多少闲置会话。**

### 2.3.1 直接回答：一柜能同时服务多少个 70B agent？

若将“同时服务”定义为：agent 都仍持有 KV、可以被调度进入 decode，且 **KV 不下沉到 DRAM/SSD**，则可以给出一个可复算的 HBM 并发估算。这里用 Llama-3.1-70B/BF16、TP=8；一台 NVL72 因而有 9 个 TP=8 replica。为模型权重、runtime、CUDA graph、碎片和 batch 留余量，**明确假设**每 GPU 可给 KV 的 HBM 为 GB200 的 128GiB、GB300/Rubin 的 192GiB：

`agent 数 = floor(72 × 每 GPU KV headroom ÷ 单 agent KV)`

| 同一条 Mooncake agent 轨迹 | 单 agent Llama-70B KV | GB200 NVL72：9TiB KV headroom | GB300 NVL72：13.5TiB KV headroom | Vera Rubin NVL72：13.5TiB KV headroom |
|---|---:|---:|---:|---:|
| 第 10 turn（34,420 token） | 10.44GiB | **约 880** | **约 1,320** | **约 1,320** |
| 第 30 turn（79,260 token） | 24.19GiB | **约 380** | **约 570** | **约 570** |
| 第 50 turn（124,100 token） | 37.87GiB | **约 240** | **约 360** | **约 360** |

因此最该记住的数是：**在这个 70B、50-turn、全 KV 留 HBM 的苛刻情景中，一柜不是同时跑 10,000 个 agent，而大致是 GB200 约 240 个、GB300/Rubin 约 360 个。** 这是 KV 容量上限，而非 GPU 计算吞吐承诺。GB300 与 Rubin 的并发数相同，是因为二者整柜 HBM 都是 20.7TB；Rubin 更强之处是 HBM 带宽、CPU DRAM 与互连，只有在 decode 吞吐、DRAM offload 或更复杂的多节点调度中才会显现。

还必须过第二道门：若每个正在 decode 的 agent 要求 `r` 个 output token/s，而实测整柜 decode 吞吐为 `Q` token/s，则真正可同时 decode 的 agent 数为：

`min(HBM 容量上限, floor(Q ÷ r))`

例如，对 50-turn 70B agent，若目标是每 agent 10 token/s，要真正用满上述容量，GB200 至少要持续输出约 **2,400 token/s**，GB300/Rubin 至少约 **3,600 token/s**。没有锁定模型精度、TP/EP、输入/输出长度分布、TTFT/TPOT SLO 和 serving engine 的实际压测，不能把 HBM 上限冒充为“保证的实时并发”。实际生产中的 agent 大量时间在等待工具调用；这时它们仍占 KV 容量，但不同时消耗 decode tokens/s，容量上限反而比实时 decode 并发更有解释力。

### 2.3.2 GB300 与 Rubin：容量 agent 相同，不代表实际服务能力相同

前表的 360 个是 **resident-HBM session 数**，不是“每秒能处理的 agent 数”。对同一个 70B、50-turn、KV 全留 HBM 的 workload，GB300 和 Rubin 都有 20.7TB HBM，故这项容量指标必然相同；若只拿它评价，购买价格更高的 Rubin 没有任何经济意义。

真正要比较的是 decode service rate。每生成一个 token，attention 至少须从 HBM 读取该 agent 已有的 **37.87GiB KV**。先只计算这部分 KV 读取、不计权重、激活值、kernel 效率与通信，得到每柜的乐观带宽上限：

| 50-turn Llama-70B / BF16 KV | GB300 NVL72 | Vera Rubin NVL72 |
|---|---:|---:|
| 整柜 HBM 带宽 | 576TB/s | 1,580TB/s |
| `HBM 带宽 ÷ 37.87GiB KV` 的 KV-only decode 上限 | **约 14,200 output token/s** | **约 38,900 output token/s** |
| 相对 GB300 | 1.0× | **2.74×** |
| 360 个 resident agent、每个 10 token/s 的 KV 读取负载 | 3,600 token/s，约 peak 的 25% | 3,600 token/s，约 peak 的 9% |
| 360 个 resident agent、每个 30 token/s 的 KV 读取负载 | 10,800 token/s，约 peak 的 76% | 10,800 token/s，约 peak 的 28% |

这不是实测吞吐，反而是一个重要的**上界/压力测试**：实际可持续 TPS 必低于该数，因为还要读取模型权重、做 attention/MLP、处理调度与通信，且不可能持续跑满 HBM。它却足以说明方向：在 10 token/s 的较宽松 agent 响应目标下，GB300 的瓶颈未必已经是 HBM；在 30 token/s、长 context、所有会话持续 decode 的高交互目标下，GB300 的 KV 读取本身就接近 HBM 峰值，而 Rubin 仍有大量带宽余量。此处 Rubin 的潜在收益是约 **2.7× 更多长-context decode 服务量/更低 TPOT**，而不是 2.7× 更多 50-turn KV 常驻会话。

Rubin 的第二个差异在工具等待期。若仍以 70B/50-turn 的 37.87GiB/agent 为例，并仅为说明量级而假设 CPU DRAM 的 70% 能留给 warm KV，则 GB300 的 17.3TB CPU DRAM 可额外留约 **300** 个 agent，Rubin 的 54TB 可额外留约 **930** 个；加上约 360 个 HBM-resident agent，即约 **660 vs 1,290** 个可恢复的 agent 上下文。它们不是同时 decode 的 agent：处于 DRAM 的 session 必须在下一次生成前预取回 HBM。Rubin 的 NVLink-C2C 也从上一代的 900GB/s 双向升至 1.8TB/s 双向，故同一 50-turn KV 的理想 DRAM→HBM 预取下限约从 90ms 降到 45ms。真正适用的场景是 agent 长时间等待网页/API/tool；连续不断地 reasoning/decode 的 session 仍主要吃 HBM 和 HBM 带宽。

因此，若 Rubin 的采购价约为 GB300 的 2 倍，投资/采购上的正确门槛不是“能否多放 KV”，而是：在目标模型和 SLO 下，它能否提供至少约 2 倍的**可交付 token/s**、或借更高 DRAM 容量和更快预取把总 agent 工作流吞吐提高至少约 2 倍。硬件规格给出长 context decode 的 **2.74× HBM 带宽、约 3.33× NVFP4 算力、2× NVLink、约 3.1× CPU DRAM**，所以对超大 MoE、长 context、高 TPS 的 agentic serving，这一门槛在物理上有可能达到；但对 70B、低 TPS、工具等待占比高且 GB300 已够用的 workload，Rubin 的价格溢价并不自动成立。

还必须剔除 NVIDIA 营销口径的误用：其“最高 10× agentic throughput”是相对于 **GB200/Blackwell**、内部 **2T MoE** workload 且按单位能耗衡量的图表，并非 GB300→Rubin 的 70B 实测，不能用于本表的价格比较。[NVIDIA Rubin 架构说明](https://developer.nvidia.com/blog/inside-nvidia-rubin-gpu-architecture-powering-the-era-of-agentic-ai/)；[GB300 官方规格](https://www.nvidia.com/en-us/data-center/gb300-nvl72/)；[Vera Rubin 官方规格](https://www.nvidia.com/en-us/data-center/vera-rubin-nvl72/)

### 2.3.3 公开实测锚点：GB300 / Rubin 实际可承载多少 agent client？

前两节的 Llama-70B 数字只是在回答“若每个 agent 的 50-turn KV 都常驻 HBM，最多能留住多少 session”。更贴近运营的公开答案来自 InferenceX 的 **AgentX**：它重放经匿名处理的 Claude Code 多轮/工具调用 trace，而不是固定 8K/1K prompt。v1.0 使用 393 条 session；请求的中位输入为 **142K token**、中位输出为 **444 token**，44% session 含 subagent。其 `concurrency` 明确是 concurrent agent **client**，而非某一瞬间正在 decode 的固定 batch。[AgentX 方法](https://inferencex.semianalysis.com/agentx)

截至 2026-09-10，公开 API 中存在同一 **DeepSeek V4 Pro 0813（1.6T MoE）、FP4、AgentX trace** 的 GB300 与 Vera Rubin 结果。下表保留运行时的真实差异，而不伪装成控制变量实验：GB300 用 Dynamo-SGLang 且开启约 721GB CPU DRAM offload；Rubin 用 TensorRT-LLM，记录为不使用 CPU DRAM offload。

| 运行平台 | 并发 agent client | 中位交互速度（output token/s/user） | 整柜 output throughput | 中位 TTFT | GPU KV pool 使用率 |
|---|---:|---:|---:|---:|---:|
| GB300 NVL72 | **960** | **78** | 22,594 token/s | 14.2s | 53% |
| GB300 NVL72 | 1,440 | 58 | 33,004 token/s | 10.4s | 72% |
| GB300 NVL72 | 1,920 | 43 | 40,612 token/s | 9.4s | 100% |
| Vera Rubin NVL72 | 934 | **145** | 34,932 token/s | 4.2s | 47% |
| Vera Rubin NVL72 | **2,572** | **78** | 75,400 token/s | 7.3s | 97% |

因此，若把“实际工况”暂定义为这条长 context、带 tool wait 的 frontier-MoE agent trace，并把约 **78 token/s/user** 作为同一交互档位，最好的公开锚点是：**GB300 约 1,000 个 concurrent agent client；Rubin 约 2,500 个，约 2.7×。** Rubin 同时输出约 3.3× 更多 token，TTFT 约减半。这个结果终于解释了高价 Rubin 的经济逻辑；但它**不能**被转述为“Rubin 对任何模型都能多服务 2.7× agent”：两台机器的 serving engine 和 DRAM offload 配置不同，而且 1.6T MoE 的 EP/通信/长 context 特征远重于 dense 70B。

相反，对我们此前的 dense Llama-70B / 50-turn / 全 KV 常驻 HBM 假设，目前没有同口径 GB300-vs-Rubin 公共 agent benchmark。对此只能写：GB300/Rubin 的 resident session 上限都约 360；真实 concurrent agent client 可以高于 360（因为多数 agent 等待工具、KV 在 HBM/DRAM 间移动），但必须由其模型、tool-wait 分布、TPOT 和实际 cache/offload 策略单独压测，不能把上表 1,000/2,500 生搬过去。公开结果可通过 [InferenceX API 文档](https://github.com/SemiAnalysisAI/InferenceX/blob/main/docs/results-and-ingestion.md) 的 `agentic_traces` 数据复核。

**DeepSeek V4 Pro 开启 DRAM KV offload 后会不会增加并发？会，但增加的是可同时在线/可恢复的 agent client，不是 HBM 中同时 decode 的 session 数。** AgentX 的 GB300 高并发档（960 / 1,440 / 1,920 client）本身就启用了约 721GB CPU DRAM offload；当 client 增至 1,920 时，GPU KV pool 已达 100%，说明 DRAM tier 正在承接 HBM 之外的 warm KV。但该公开表没有同一配置的“offload 关闭”对照，因此**不能严谨地把 1,920 与某个无 offload 并发数相减，得出 DRAM 精确多带来多少 agent**。

一项更干净的 AgentX 对照说明了条件性：B300 在 384 条 DeepSeek V4 Pro agent trace、3TB DRAM offload 下，HBM hit 为 91%，DRAM hit 仅 1.36%，因为 HBM 工作集尚够；B200 在其他参数相同、196 条 trace 下，HBM hit 降至 73%，DRAM offload hit 接近 20%。结论不是“DRAM 永远翻倍并发”，而是**HBM 未满时 DRAM 几乎无效；HBM 已满时它能延后拒绝/重算、提高在线 client 数，但过度依赖会恶化尾延迟。**该研究还指出 write-through DRAM cache 往往需要约 HBM KV pool 的 1.5–3 倍容量才真正有效。[InferenceX 对照与遥测](https://inferencex.semianalysis.com/blog/deepseek-v4-pro-agentx-b200-vs-b300-kv-working-set)

DeepSeek V4 Pro 的 CSA/HCA 将 KV 沿序列维压缩，因此其 long-context KV 远小于传统 GQA；这会令 DRAM 能保留更多等待工具的 session，也同时降低“不得不下沉到 SSD”的压力。工程上应写成：`总 agent client ≈ HBM active sessions + DRAM warm sessions`，但实时 decode 并发仍受 HBM、HBM 带宽、预取和 TPOT SLO 约束。**对 NAND 的含义偏中性甚至偏空头**：DRAM offload 能支持更多 agent workload，却可能先替代一部分本应假设进入 SSD 的容量；只有 DRAM warm tier 也满、且历史 KV 仍有高复用时，SSD 才成为下一层。

### 2.3.4 为什么 DeepSeek 的 context cache 可留数小时至数天，而 Claude 默认仅 5 分钟？

先纠正常见说法：DeepSeek **没有承诺固定超过 1 天的 TTL**。其官方表述是：未再使用的 context disk cache “一般为数小时到数天”后会自动清理，且缓存是 best-effort、不保证命中。Claude API 默认 TTL 是 **5 分钟**，但可以付费选择 **1 小时**；每次读写都会刷新 TTL，计时从请求开始而非响应结束。故这不是“DeepSeek 永久保存 KV、Anthropic 只能不到 10 分钟”的对比。[DeepSeek 官方说明](https://www.deepseek.com/news/context-caching/)；[Claude prompt caching 文档](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)

两家公司缓存的本质都属于可复用 prompt prefix 的内部 KV / working state，用于绕过重复 prefill；区别是**DeepSeek 明确把预计会复用的 context state 下沉到分布式硬盘阵列**，而 Anthropic 对 API 用户提供的是标为 `ephemeral` 的短 TTL 产品。DeepSeek 还明确指出，它采用的 MLA 将 KV 状态显著压缩，从而把保存容量和传输带宽降到可用低成本磁盘承载的水平；缓存以 64-token block 保存，只有从第 0 token 开始完全相同的 prefix 才可能命中。公司展示的案例是 128K 重复输入的 TTFT 从约 13 秒降至约 0.5 秒，并不意味着 disk 中的 KV 可以逐 token 直接供 attention 使用。[DeepSeek](https://www.deepseek.com/news/context-caching/)

正确的工程理解是：

1. **热路径仍在 HBM。** 命中 disk cache 后，系统须把需要的 state 取回/预取到服务 worker，再继续 decode；它节省的是重复 prefill，而非让 GPU 用硬盘带宽执行 attention。
2. **MLA 改变经济性。** 同为 BF16 KV 的示例中，DeepSeek-V3 MLA 的 68.625KiB/token 约为 Llama-3.1-70B GQA 的 320KiB/token 的 21%；较小 state 才较可能保留更久、跨机器转移更快。
3. **长 TTL 是服务商的容量、P99 与隔离策略，不是模型天赋。** Anthropic 完全可以在内部另做更长的持久化层，但其公开 API 对短 TTL 给出明确成本和命中行为；DeepSeek 选择把“未使用则数小时到数天清理”的容量风险留在自建 disk-cache 系统中。后一句是基于两家公司公开产品设计的推断，并非 Anthropic 公开披露的内部存储架构。

对 SSD 投资也不能直接跳结论：DeepSeek 的公告只说“分布式硬盘阵列”，未披露介质是 enterprise SSD、HDD 还是多层混合；因此它证明 **可长期保存可复用 KV 的需求与软件可行性**，不证明对应容量必然采购某一家 eSSD。真正要落到 NAND TAM，还需知道命中率、保留时长、每 token KV 字节、复制数、热/冷层比例和底层介质。

DeepSeek 对该技术的公开资料可分三层：

1. **接口/行为文档（最详细的公开说明）**：[Context Caching](https://api-docs.deepseek.com/guides/kv_cache/) 已披露缓存写入和命中的规则。每次请求会在 user input 末端、model output 末端各形成一个 cache-prefix unit；系统也会识别多请求共同 prefix 并把它独立持久化，长输入/输出会在固定 token 间隔切分 unit。因 Sliding Window Attention，后来的请求须完整匹配一个既有 unit，不能任意从中间匹配。cache 构建需数秒，命中只复用 user-input prefix，输出仍需重新推理。
2. **生产运行概览（官方仓库，但不是实现代码）**：[DeepSeek-V3/R1 Inference System Overview](https://github.com/deepseek-ai/open-infra-index/blob/main/202502OpenSourceWeek/day_6_one_more_thing_deepseekV3R1_inference_system_overview.md) 披露过一个 24 小时样本：608B input token 中 342B、即 **56.3%** 命中 on-disk KV cache；并描述 prefill/decode 分离、EP144 decode、KV usage load balancing 与 H800 集群吞吐。
3. **尚未开源的生产 cache service**：截至 2026-09-17，没有发现 DeepSeek 官方 repo 公开用于 API 的 KV 序列化格式、索引/一致性协议、跨节点 placement、驱逐/TTL 算法、磁盘介质或预取调度代码。DeepSeek 开源的 [3FS](https://github.com/deepseek-ai/3FS) 是分布式文件系统，不能据此断言就是 API KV cache 的后端；MLA 模型与权重仓库也只解释“为什么 KV 更小”，不是磁盘缓存服务。

### 2.4 直接放大：10,000 个 agent、每个 50 turn

沿用完全相同的 agent 行为：`C(50)=124,100 tokens/agent`。若 **10,000 个 agent 都仍活跃并保留全量 KV**，总 token 为：

`10,000 × 124,100 = 1.241 billion cached tokens`

下面是四种模型/架构的直接容量结果。Llama-8B 的 GQA BF16 KV 为 `2×32 layers×8 KV heads×128 head dim×2 bytes=128KiB/token`；Llama-70B 为 320KiB/token；DeepSeek-V3 MLA 为 68.625KiB/token；Kimi K2.5 FP8 采用 Mooncake 披露的 3.8GB/100K token。[Llama-3.1-8B config](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct/raw/main/config.json)；[Llama-3.1-70B config](https://huggingface.co/meta-llama/Llama-3.1-70B-Instruct/raw/main/config.json)；[DeepSeek-V3 config](https://huggingface.co/deepseek-ai/DeepSeek-V3/blob/main/config.json)；[Mooncake](https://vllm-project.github.io/2026/05/06-mooncake-store/)

| 模型 / KV 类型 | KV bytes/token | 10,000 agent × 50 turn 的总 KV | 将全部 KV 留在 HBM 所需的 **raw rack 数**：GB200 | GB300 | Vera Rubin |
|---|---:|---:|---:|---:|---:|
| Llama-3.1-8B、GQA BF16 | 128KiB | **147.94TiB**（162.66TB） | **13** | **8** | **8** |
| Llama-3.1-70B、GQA BF16 | 320KiB | **369.85TiB**（406.65TB） | **31** | **20** | **20** |
| DeepSeek-V3、MLA BF16 | 68.625KiB | **79.31TiB**（87.21TB） | **7** | **5** | **5** |
| Kimi K2.5、FP8 | 38,000 bytes | **42.89TiB**（47.16TB） | **4** | **3** | **3** |

表中 rack 数向上取整，且**只按 raw HBM 容量**，尚未扣模型权重、runtime、KV block fragmentation、batch headroom、复制和故障预留；实际部署所需计算 rack 会更多。它回答的是“这批 KV 的容量下限”，不是“这批 agent 的算力或吞吐需求”。

最关键的量级结论是：10,000 个 50-turn agent 若以 Llama-70B/BF16 的 KV 强度运行，会形成约 **370TiB** 的 KV 工作集；这已不是单个 NVL72 能靠 DRAM 扩展解决的问题，而是至少约 **20 个 GB300/VR rack 的 raw HBM 容量**。如果其中只有小部分 agent 真正处于 decode、其余等待工具调用或很久才重用，才有经济动机把非活跃部分下沉到 DRAM/SSD；否则应横向加 replica/rack。

### 2.5 KV 从 HBM 下沉到 DRAM / SSD：传输时间到底差多少

以 30-turn 的单个 Llama-70B/BF16 agent 为例，79,260 token 对应 **24.19GiB KV**。下表计算的是把这整段 KV **搬出去或预取回 HBM 一次**的纯数据搬运时间；不是一次 decode 的完整延迟。

| 路径 | 可用带宽口径 | 24.19GiB 单向搬运的理论时间 | offload + reload 两次搬运 | 判断 |
|---|---:|---:|---:|---|
| GB200：HBM ↔ Grace LPDDR5X | NVLink-C2C 标称 900GB/s **双向**；按 450GB/s 单向满速计算 | **约 58ms** | **约 116ms** | 实际可能更慢：同一 Grace CPU 连两张 GPU，且有其他 DMA / CPU 内存流量竞争；但数量级是几十毫秒。 |
| Vera Rubin：HBM ↔ Vera LPDDR5X | NVLink-C2C 标称 1.8TB/s **双向**；按 900GB/s 单向满速计算 | **约 29ms** | **约 58ms** | 同样是理想满速下限；Rubin 的 CPU-GPU 分层移动约比 GB200 快一倍。 |
| HBM ↔ 单块本地 NVMe SSD（GDS） | vLLM/PegaFlow 工程案例的单盘稳定读约 6.5GB/s；现代高端盘/拓扑更优时可更高 | **约 4.0s**（按 6.5GB/s） | **约 8.0s** | 这是 GB200 DRAM tier 的约 70 倍单向时间；适合异步冷存，不适合临界 decode 路径。 |
| HBM ↔ 4 块 NVMe 并行条带（GDS） | NVIDIA 指出至少 4 块 x4 NVMe 才能接近 GPU x16 PCIe 链路饱和；若按 4×6.5≈26GB/s 近似 | **约 1.0s** | **约 2.0s** | 仍比 GB200↔DRAM 慢约 17 倍；实际取决于 PCIe affinity、queue depth、写入性能和是否竞争。 |

GB200 的 900GB/s 和 Vera Rubin 的 1.8TB/s 均为**双向链路规格**，表中已保守地按一半作为单向搬运上限；因此这些毫秒数不是承诺的实测 P99。GPU 访问 HBM 的带宽则分别约 8TB/s（GB200）和 22TB/s（Rubin），远高于 C2C；所以 DRAM 的正确用法仍是提前搬回 HBM，而不是把全量 active KV 长期留在 DRAM 上做 attention。[GB200 C2C 与 HBM 规格](https://www.nvidia.com/en-us/data-center/gb200-nvl72/)；[NVIDIA 对 GB200 / Rubin host-offload 的说明](https://developer.nvidia.com/blog/reducing-high-bandwidth-memory-bottlenecks-in-jax-based-llm-training-with-host-offloading/)

SSD 数字也不能理解成“GPU 直接读取 SSD 后就能 decode”。GDS 可以绕开 CPU DRAM bounce buffer，使 NVMe DMA 直接抵达 GPU memory，但**SSD 带宽和 I/O 延迟本身没有消失**；NVIDIA 的设计指南明确指出，需要至少 4 块 x4 NVMe 并行才接近 x16 GPU 链路，PCIe 拓扑不佳还会显著降速。vLLM 的 PegaFlow 案例对 local SSD 观测到约 6.5–6.9GB/s 的单盘持续读，适合作为本表的保守工程锚点。[NVIDIA GDS 设计指南](https://docs.nvidia.com/gpudirect-storage/design-guide/)；[NVIDIA GDS 基准指南](https://docs.nvidia.com/gpudirect-storage/configuration-guide/)；[PegaFlow](https://vllm-project.github.io/2026/05/18/pegaflow.html)

对投资判断最有用的是：**DRAM cache 是几十毫秒级的 warm tier；本地 SSD 是约 1–4 秒级（取决于单盘或条带）的 cold/persistent tier。** 写出可以在 agent 等待工具调用时异步隐藏；下一轮请求来临时的 reload 才会直接拉高 TTFT。若未能在这段时间内预取完成，系统通常应选择重算 prompt，而不应让 decode 等待 SSD。

### 2.6 假设 SSD offload 可用：究竟有多少 KV 会溢出到 SSD？

容量关系的直接公式是：

`SSD-resident KV minimum = max(0, retained KV − allocatable HBM KV − allocatable DRAM KV)`

下表先给出一个**对 SSD 最不利、因而最保守的物理下限**：假设每个 rack 的所有 HBM 和所有 CPU DRAM 都可 100% 用于 KV（现实中不成立，模型权重、runtime、OS、网络 buffer、fragmentation 都会挤占容量）。采用第 2.3 节的 **1,000 agent × 50 turn**，即每个 agent 124,100 cached token。

| 模型 / KV 类型 | retained KV 总量 | GB200：HBM+DRAM = 27.65TiB 后的 SSD 下限 | GB300：34.56TiB 后的 SSD 下限 | Vera Rubin：67.94TiB 后的 SSD 下限 |
|---|---:|---:|---:|---:|
| Llama-3.1-8B、GQA BF16 | 14.79TiB | 0 | 0 | 0 |
| Llama-3.1-70B、GQA BF16 | **36.98TiB** | **9.34TiB**（25%） | **2.42TiB**（6.6%） | 0 |
| DeepSeek-V3、MLA BF16 | 7.93TiB | 0 | 0 | 0 |
| Kimi K2.5、FP8 | 4.29TiB（4.716TB） | 0 | 0 | 0 |

这个表的正确读法是：在单个 rack 承载 1,000 个 50-turn Llama-70B agent 的极端设定下，即使把 HBM 和 CPU DRAM 都填满，GB200 至少还有约 **9.3TiB**、GB300 至少还有约 **2.4TiB** 的 KV 只能去 SSD 或被淘汰/重算；Vera Rubin 的 54TB CPU DRAM 则在**纯容量**上足以接住这批 cache。实际 SSD 溢出会更大，因为“100% 内存给 KV”不可能成立。

但这不能反推“10,000 agent 就必然需要数百 TiB SSD”。例如 10,000 个 50-turn Llama-70B agent 产生约 369.85TiB KV，单个 rack 的物理溢出下限确实为 GB200 342.2TiB、GB300 335.3TiB、Vera Rubin 301.9TiB；可是实际运行这批 active agent 已需要至少约 31 / 20 / 20 个 raw-HBM rack。若 KV 随计算 replica 均衡分布，20 个 GB300 rack 的合计 HBM+DRAM 约 691TiB，20 个 Vera Rubin rack 约 **1.33PiB**，**总物理内存反而足以容纳 370TiB**。

所以，SSD offload 成功不会自动把“超出单 GPU HBM 的所有 KV”变为 SSD 需求。真正会进入 SSD 的，是：**已不值得占 HBM、但又不值得占有限 DRAM、且预期会在 TTL 内复用的那部分 retained KV**。这取决于每个 replica 的 agent 密度、DRAM 是否被模型/工具 sandbox 占用、cache TTL、跨 replica 共享和预取成功率；它是 SSD TAM 最重要、但尚未被运营商公开的数据。

### 2.7 这个反证很重要：在当前 agent 假设下，CMX 并非容量必需品

第 2.6 节的结果推导出一个必须正视的结论：**若 retained KV 只等于活跃 agent 的当前上下文、并且随 compute replica 均衡分布，HBM+CPU DRAM 本身可能已足够，CMX/SSD 没有必然的容量需求。**

以 10,000 agent × 50 turn、Llama-70B/BF16 的 **369.85TiB active KV** 为例。表中的 `31×/20×` 是下面这个**只为容纳 KV 而算的 raw-HBM 容量下限**，不是 NVIDIA 出货量、客户实际部署量或完整服务所需的 compute rack 数：

`raw-HBM rack 下限 = ceil(369.85TiB ÷ 单 rack 的 raw HBM 容量)`

- GB200：每 rack 13.4TB = **12.19TiB raw HBM**，故 `ceil(369.85 ÷ 12.19) = 31`。
- GB300 / Vera Rubin：每 rack 20.7TB = **18.83TiB raw HBM**，故 `ceil(369.85 ÷ 18.83) = 20`。

模型权重、runtime、fragmentation、batch headroom 和实际 tokens/s 都没有计入；因此真实服务需要的 rack 通常会更多。为给 SSD 的容量判断设一个最有利于 SSD 的反证，以下再临时假设这批**下限 rack**的全部 HBM+CPU DRAM 都可用于 KV：

| KV-only raw-HBM rack 下限 | 这批 rack 合计 HBM+DRAM | 相对于 369.85TiB active KV 的 retained-capacity 倍数 | 在所有 memory 都给 KV 时，新增多少可复用历史 KV 才开始需要 SSD |
|---|---:|---:|---:|
| 31 × GB200 | 857TiB | **2.32×** | **487TiB**（总 retained KV > 857TiB） |
| 20 × GB300 | 691TiB | **1.87×** | **321TiB**（总 retained KV > 691TiB） |
| 20 × Vera Rubin | 1.33PiB | **3.67×** | **989TiB**（总 retained KV > 1.33PiB） |

这不是说上述内存真的都能给 KV：HBM 要留模型权重、CUDA graph 和 batch headroom；CPU DRAM 被 OS、tool sandbox、prefill buffer、网络 buffer 和其他服务占用；每个 Grace/Vera CPU 的 DRAM 也有 locality，不能像单一无损共享内存那样被所有 GPU 随意使用。这些因素会降低表中的倍数。

但它们**不能反转方向**：我们不能因为“有 GDS/CMX”就假设所有超过 HBM 的 KV 会进入 SSD。对于私有、一次性的 agent 对话，正确策略往往是让 KV 过期或重算；对于短间隔复用，先用本地 DRAM；只有当 retained-and-reusable inventory 超出可用 DRAM，或共享/持久化的经济收益高于额外 DRAM 与预取成本，SSD/CMX 才有容量理由。

这也解释 GDS 和 CMX 的不同角色：GDS 是通用 GPU-to-storage 数据路径，服务模型加载、训练/推理数据、RAG、checkpoint 等，并非只为 KV；CMX 的核心价值是跨节点共享、cache-aware routing、持久化和把 DRAM/HBM 从长尾历史 KV 中释放出来，**不是证明每个 agentic rack 都必须有数 TB SSD/GPU**。[NVIDIA GDS](https://docs.nvidia.com/gpudirect-storage/)；[NVIDIA CMX](https://developer.nvidia.com/blog/?p=111143)

因此，本研究对 Sandisk/Kioxia 的正确 base case 应是：**在上述 10,000-agent / 50-turn 情景中，若没有“历史 KV 库存至少高于 active KV 约 1.9–3.7 倍且仍有高复用”的证据，就不应把 CMX SSD 计入必然需求。** 这不是 CMX 技术无价值，而是把它从“GPU 出货自动附带的 BOM”降回“需要由 retention、reuse 与 DRAM 经济性证明的可选 tier”。

## 3. 换算到 Rubin NVL72：HBM 能容纳多少活跃请求

NVIDIA 公布 Vera Rubin NVL72 具 72 块 Rubin GPU、总 HBM4 20.7TB，即每 GPU 288GB。[NVIDIA](https://www.nvidia.com/en-eu/data-center/vera-rubin-nvl72/)

以下不是官方配置，而是为计算留下模型权重、runtime、通信和碎片空间后，**假设每 GPU 留 192GiB 给 KV**：全 rack 有约 13.5TiB 逻辑 active-KV headroom。按此假设，单 rack 大致能同时容纳：

| 模型 | 8K context | 32K context | 128K context |
|---|---:|---:|---:|
| Llama-3.1-70B GQA / BF16 | ~5,530 会话 | ~1,382 | ~346 |
| DeepSeek-V3 MLA / BF16 | ~25,755 会话 | ~6,439 | ~1,610 |

这些是**只看 KV 的上限**，不代表可达到的 tokens/s：真实系统还会受模型权重、TP/EP 配置、batching、prefill/decode 分离、网络、延迟 SLO 和调度策略限制。它仍说明：用 72 GPU rack 支撑高并发 128K context，HBM 首先就变成很稀缺的工作集；但这不能反推每 GPU 必须搭配 16TB SSD。

## 4. 如何理解市场所说的 2 / 4 / 8 / 16TB CMX 每 GPU

CMX 容量可以理解为“一个 GPU 的 active-KV headroom 之外，还愿意为可复用历史 KV 留多少倍库存”。按产品标称的十进制 SSD 容量，并以 288GB raw HBM / 192GiB 可用 KV headroom 为参照：

| CMX / GPU | 相当于 raw HBM | 相当于 192GiB KV headroom | 所隐含的 retained-KV 倍数 |
|---|---:|---:|---|
| 2TB | 6.5× | 9.7× | 中等程度的 warm/persistent 保留 |
| 4TB | 12.9× | 19.4× | 需存在可观的跨会话复用或长保留 |
| 8TB | 25.9× | 38.8× | 假设推理 workload 中长上下文/agent 占比较高 |
| 16TB | 51.7× | 77.6× | 不是普通聊天的默认 BOM；需要极高的保留与复用库存 |

因此原 `SSD与CMX需求模型.md` 的 **4TB/GPU base case**，应被理解为“CMX 中大约有 19 倍于可用 HBM KV 工作集的历史 KV 有经济价值”，而非架构必然要求。16TB/GPU 则等同于约 78 倍，必须由真实的留存时长、复用命中率、agent 并发和预取成功率证明。

## 5. 与现实公开案例的边界校验

- Novita AI 与 vLLM 的生产导向案例已经使用一个 host **500GiB** 的外置 KV pool，并在内部生产集群对大型 prefix read 测到平均 194GB/s；这验证“KV 可越过 GPU/进到远端与 SSD 层”是真实工程方向，但远不是 EB 级部署量披露。[Novita/vLLM](https://vllm-project.github.io/2026/05/18/pegaflow.html)
- AWS 的 HyperPod demo 中，4 轮、2,048-token 对话生成 109MB KV 并写至 NVMe 相关层；其值受模型和精度影响，不能拿来直接校准 Llama/DeepSeek 的绝对字节数，但方向一致。[AWS](https://aws.amazon.com/blogs/machine-learning/tiered-kv-cache-for-large-llms-on-sagemaker-hyperpod-with-curvine/)
- NVIDIA 将 active KV 放在 HBM，DRAM、本地 SSD 和 CMX 用于下层存储并通过预取回到上层。这支持分层模型，却不提供每层的容量配置比例。[NVIDIA CMX 技术说明](https://developer.nvidia.com/blog/?p=111143)

## 6. KV 卸载到 SSD 的技术成熟度

“KV offload to SSD”不能理解为 decode 的每个 token 都从 SSD 随机读取。**decode 临界路径的 KV 仍必须在 HBM；SSD 的正确用途是写入已完成 prefill 的 warm/persistent KV，在下一次调用前异步读出、预取到 DRAM/HBM。** 若 SSD 取回耗时超过重算 prefill，系统应回退到重算而非等待。

| 层级 / 用法 | 成熟度判断（截至 2026-09-15） | 证据与限制 |
|---|---|---|
| HBM 内 paged / prefix KV cache | **✅ 成熟，生产默认能力** | vLLM 等 serving engine 已提供 cache lifecycle、hit rate、eviction 与复用指标。它解决 GPU 内部调度，不增加 NAND 需求。|
| GPU → CPU DRAM offload | **✅ 可生产使用，但受延迟与 PCIe/网络约束** | 适合短时间 warm cache、prefill/decode 解耦；仍必须预取，不宜承担 token-by-token decode。|
| GPU/DRAM → 本地 NVMe SSD | **🟡 已可部署、适合命中率高的 long-prefix/RAG/agent 场景；尚非通用默认** | LMCache 已支持 local disk、SSD、对象存储等后端；AWS 的 HyperPod 测试把多轮 KV 写入节点 NVMe 层。经济性取决于命中率、写放大、耐久和预取。|
| 多节点 RDMA + DRAM/SSD 共享池 | **🟡 生产导向试点，软件仍快速演进** | vLLM/Mooncake 在 agent trace 中给出 12–60 GPU 的评测和 >92% cache hit；Novita/vLLM 展示 500GiB host pool 与生产集群读带宽。缺少 hyperscaler 规模、SLA、故障恢复的公开数据。|
| NVIDIA CMX（Pod 级 NVMe + BlueField-4） | **⚠️ 新架构/导入期，不可当存量标准配置** | NVIDIA 已定义产品与性能目标，但未找到 CSP 披露的常规 CMX rack 规模、容量配置或客户实际 SSD 出货量。|

软件与硬件路径不是纸上谈兵：LMCache 明确支持 local disk（SSD）、Redis、Mooncake、对象存储、NIXL/GDS 等层；vLLM 与 Mooncake 已让 GPU HBM 与分布式 DRAM/SSD pool 经 RDMA 迁移 KV。[LMCache](https://github.com/LMCache/LMCache)；[vLLM/Mooncake](https://vllm-project.github.io/2026/05/06-mooncake-store/)。AWS 的测试中，四轮、2,048-token 对话把 109MB KV 写入下层，并显示在节点之间复用可降低延迟。[AWS](https://aws.amazon.com/blogs/machine-learning/tiered-kv-cache-for-large-llms-on-sagemaker-hyperpod-with-curvine/)

但“有代码可跑”不等于成熟的持久化存储产品。开源栈目前仍显示三个投资上重要的限制：

1. **性能边界**：SSD 只在 cache hit 且可及时预取时节省 prefill；慢读时应回退重算。LMCache 2026-09 的公开 RFC 仍在补 L2 load timeout / recompute fallback，说明这个调度边界仍需运维调参。[LMCache RFC](https://github.com/LMCache/LMCache/issues/4945)
2. **耐久与写放大**：KV 是大量短生命周期、小块、反复覆盖的写入。LMCache 自身针对 NVMe offload 提出的 SSD wear RFC，直接把高写量、随机写与寿命列为问题；这使 QLC 是否合适取决于 admission policy，而不是容量单价。[LMCache wear RFC](https://github.com/LMCache/LMCache/issues/2739)
3. **正确性与容错**：近期公开 issue 仍报告 local-disk backend 在跨请求 KV 隔离、重启恢复和部分读取等场景的问题。它们是开源用户报告，不代表所有实现都会出错，但足以说明“长期持久化 KV”尚没有像数据库那样标准化、低风险的运维成熟度。[cross-request issue](https://github.com/LMCache/LMCache/issues/4385)；[restart issue](https://github.com/LMCache/LMCache/issues/4492)

因此最准确的产业判断是：**KV-to-SSD 的“技术可行性”已成熟；本地 warm-cache 的“产品可用性”已进入早期生产；跨节点/跨 rack、长保留且高可靠的 persistent KV，仍处于导入和优化阶段。** 它支持 eSSD 的增量需求方向，但尚不足以支持“所有 AI 推理集群很快标配多 TB CMX/GPU”的基准预测。

## 7. GPU、DRAM 与 SSD 的通信技术：进步在哪里，边界在哪里

### 7.1 三条完全不同的链路

| 链路 | 当前主要技术 | 它解决什么 | 它没有解决什么 |
|---|---|---|---|
| GPU compute ↔ **HBM** | GPU 封装内 HBM4、GPU memory controller | 活跃 KV 的逐 token attention；极高带宽与低延迟 | HBM 容量昂贵且有限，不能保存大量闲置 KV |
| GPU ↔ **CPU 系统内存** | PCIe / Unified Memory；在 Grace Hopper 等紧耦合系统为 coherent NVLink-C2C | 将较大但较慢的系统内存变为 GPU 可访问的扩展层；减少显式 copy | 仍显著慢于 HBM，不能无代价承担所有 decode KV |
| GPU ↔ **NVMe SSD** | GPUDirect Storage（GDS）/ cuFile、NVMe DMA、NVMe-oF + GPUDirect RDMA | 绕开 CPU DRAM bounce buffer，把大块数据直接 DMA 至 GPU memory；降低 CPU 占用与额外 copy | SSD 不是 coherent byte-addressable HBM；读回为有延迟的 block I/O，必须异步、批量、预取 |

首先要纠正常见说法：GPU 从来不是“直接和普通 DDR 内存同速通信”。真正最快的是 GPU 自己封装内的 HBM；CPU DRAM 是第二层；SSD 是 I/O / cache tier。NVIDIA Rubin 单 GPU 的 HBM4 标称容量为 288GB、带宽最高 22TB/s。[NVIDIA Rubin](https://developer.nvidia.com/blog/inside-nvidia-rubin-gpu-architecture-powering-the-era-of-agentic-ai/)

### 7.2 GPU ↔ DRAM：确实被大幅加强，但只限特定系统

传统 x86 GPU 服务器里，GPU 与 host DRAM 主要通过 PCIe 和 CUDA 的显式 copy / Unified Memory 工作，带宽和延迟受 CPU root complex、PCIe topology、NUMA 与软件迁移策略影响。它不是 HBM 的直接等价物。

NVIDIA 的重大变化是 Grace Hopper / Grace Blackwell 一类紧耦合 CPU-GPU 设计：Grace CPU 与 Hopper GPU 使用 **coherent NVLink-C2C**，标称总双向带宽 **900GB/s**，使 CPU/GPU 线程可访问对方内存，并让 GPU 可将 CPU LPDDR5X 作为更大的可寻址内存层。900GB/s 仍只约为 Rubin 22TB/s HBM 的一小部分，但相对传统 PCIe 是数量级改善。[NVIDIA Grace Hopper](https://developer.nvidia.com/blog/?p=57192)

所以“GPU 和 DRAM 通信加强”这个判断是对的，但精确表述应是：**在紧耦合 superchip 中，GPU 可更快、更一致地访问 CPU memory；它让 DRAM 更适合 warm KV / oversubscription，而不是让 DRAM 取代 HBM 承担活跃 decode。**

### 7.3 GPU ↔ SSD：已经从两次 copy 变成可直通 DMA，但仍是 I/O

传统路径是 `SSD → CPU DRAM page/bounce buffer → GPU HBM`，数据至少多一次拷贝，并占用 CPU/DRAM 带宽。GDS 通过 cuFile 与 DMA，使本地 NVMe（或远端 NIC）能把数据直接搬入/搬出 GPU memory，绕开 CPU memory 的 bounce buffer。GDS 对 local NVMe 和 NVMe-oF 都适用；local storage 由 NVMe 执行 DMA，remote storage 由 NIC 经 RDMA 执行 DMA，文件需以 `O_DIRECT` 打开才可走真正的 direct path。[GDS 概览](https://developer.nvidia.com/gpudirect)；[GDS O_DIRECT 要求](https://docs.nvidia.com/gpudirect-storage/o-direct-guide/)

这项技术非常重要，但它的含义是：

`SSD / NVMe-oF ──（DMA, RDMA, 大块异步传输）──> GPU HBM`

而不是：

`GPU 每生成一个 token 都同步从 SSD load KV`

GDS 官方设计指南明确指出，local storage 要靠**多块 x4 NVMe 并行**才接近 GPU x16 PCIe 链路饱和；PCIe topology 决定实际表现，GPU 和盘挂在同一 PCIe switch 下会明显更好。[GDS Design Guide](https://docs.nvidia.com/gpudirect-storage/design-guide/)

### 7.4 CMX 的新意：不是让单块 SSD 变 HBM，而是让整个 pod 的数据路径变快

NVIDIA CMX 把 NVMe SSD、BlueField-4、DOCA Memos、Dynamo 和 Spectrum-X RDMA 网络组合成 pod-level KV tier：DPU 管理 NVMe、数据完整性与 KV routing，Dynamo 让请求尽量落到 KV 已存在的位置，RDMA 网络负责高带宽搬运。[NVIDIA CMX](https://www.nvidia.com/en-in/data-center/ai-storage/cmx/)

下面的标称数字不可直接横比（有的为双向、有的为链路峰值），但足以说明层级差异：

| 例子 | 标称接口量级 | 对 KV 的含义 |
|---|---:|---|
| Rubin GPU HBM4 | 22TB/s | decode 的工作台 |
| Grace Hopper NVLink-C2C | 900GB/s 双向 | 系统内存可成为较快的 warm tier |
| BlueField-4 DPU | 800Gb/s ≈ 100GB/s | 负责 storage/network 的数据路径与卸载，不等于单盘速度 |
| Vera BlueField-4 STX / ConnectX-9 | 最高 1.6Tb/s ≈ 200GB/s | rack/pod 级 RDMA KV 迁移的网络上限，实际还受 SSD 阵列和软件调度约束 |

BlueField-4 的 800Gb/s、STX/ConnectX-9 最高 1.6Tb/s 是 NVIDIA 当前公开规格。[BlueField](https://www.nvidia.com/en-us/networking/products/data-processing-unit/)；[Vera Rubin NVL72](https://www.nvidia.com/en-us/data-center/vera-rubin-nvl72/)

### 7.5 对 SSD 研究的直接结论

1. **DRAM tier 的增强反而是 SSD 的竞争因素。** NVLink-C2C 和更大 CPU memory 能先吸收一部分 warm KV，因此“KV 超出 HBM”不等于立刻写 SSD。
2. **GDS 是 eSSD 的必要技术基础，但非充分条件。** 它消除了额外 copy，却没有消除 NAND / PCIe / 网络的延迟；只有 cache hit、预取与重算对比有经济性时 SSD 才被使用。
3. **CMX 的价值在系统工程而非单盘参数。** 多盘并行、DPU、RDMA、KV-aware routing 才可能把 SSD 放入推理数据路径；这也解释了为什么 CMX 需要企业级盘、网络和软件栈，而不是一块消费级 SSD。
4. **尚未达到“SSD 可替代 DRAM”的状态。** 因而对 Sandisk/Kioxia 的 NAND 需求，应把 persistent/shared KV 当作可选增量，而不能按 GPU HBM 容量机械外推。

### 7.6 除 HBF 外，GPU 直连 SSD 的技术地图

“GPU 直连 SSD”不是单一产品名，而是**数据路径、软件栈、SSD 介质与系统架构**四层的组合。当前最成熟且已可部署的基础是 NVIDIA GPUDirect Storage（GDS）；HBF 则是另一条近封装 NAND 路线，不是 NVMe SSD。

| 层级 / 技术 | 数据路径 | 成熟度 | 对 KV / SSD 研究的含义 |
|---|---|---|---|
| **PCIe P2P DMA + NVIDIA GDS / cuFile** | 本地 NVMe 的 DMA engine 直接读写 GPU HBM，绕过 CPU DRAM bounce buffer；需 `O_DIRECT`、GPU memory registration 与正确 PCIe affinity | **✅ 可部署** | 这是“GPU 直连本地 SSD”的标准基础设施；仍是 block I/O，适合异步大块 transfer / prefetch，不使 SSD 成为 HBM。 |
| **GPUDirect RDMA + NVMe-oF / RDMA filesystem** | 远端 SSD → storage NIC → RDMA fabric → client NIC → GPU HBM；NIC 而非本地 NVMe 执行面向 GPU 的 DMA | **✅ 可部署，但系统复杂** | 把 KV 从单机盘扩展为共享池；容量和复用范围更大，但叠加网络拥塞、tail latency 与一致性/故障处理。 |
| **BaM / GPU-Initiated Direct Storage（GIDS）** | GPU kernel 自行提交 NVMe queue / doorbell，GPU 驱动 I/O，而非 CPU 为每次 I/O 发起请求 | **🟡 研究/原型为主** | 针对 KV/向量检索的细粒度随机 I/O；普通 GDS 的 CPU control-path 仍可能是瓶颈。并非通用 NVIDIA 产品承诺。 |
| **Kioxia GP / GP1 + XL-FLASH** | PCIe 6.0 NVMe SSD，面向 GPU direct access 与 GPU-initiated / 小块随机 I/O；底层仍可配合上述 P2P/GDS/BaM 路径 | **🟡 样品导入期** | 是“为 GPU 直连而特化 SSD”的产品路线：低延迟 XL-FLASH、512B random read、10M IOPS、50 DWPD；与 HBF 的近封装 NAND 不同。 |
| **NVIDIA CMX + BlueField-4 + DOCA Memos + Dynamo** | 多块 NVMe + DPU + RDMA 网络组成 pod-level shared KV tier；软件按 KV block 做 routing、placement 与预取 | **🟡 新平台导入** | 不是一块 SSD 直连一张 GPU，而是把 SSD 做成可共享的 context memory；最直接对应长 context / multi-agent 的 eSSD 增量情景。 |
| **CXL memory / CXL + flash module** | CPU 经 CXL.mem 使用外部 memory expansion；GPU 通常经 CPU memory 或软件搬运访问 | **🟡 DRAM expansion 已导入，flash 方案早期** | CXL 是协议而非 GPU-SSD P2P。它可扩充 host memory tier，但不等于 GDS，也不能让 SSD 在 GPU decode 中替代 HBM。 |

NVIDIA 的 GDS 文档明确区分：**本地**路径由 NVMe device DMA；**远端**路径由 NIC 经 RDMA DMA；两者都需避免文件系统把 payload 重新带回 CPU memory。GDS 支持 NVMe、NVMe-oF、NFS/RDMA 及多种 RDMA distributed file system。[GDS requirements](https://docs.nvidia.com/gpudirect-storage/o-direct-guide/)；[nvidia-fs 支持矩阵](https://docs.nvidia.com/gpudirect-storage/nvidia_fs/index.html)

Kioxia 的 GP1 是目前最明确的 eSSD 产品锚：官方称其为 PCIe 6.0、GPU direct access 优化，使用 XL-FLASH Gen2，目标 512B 随机读 10M IOPS、最高 50 DWPD；但截至 2026-09-16 仍为向 select customers 提供的 evaluation samples，不能算作大规模出货。Kioxia 也公开把 BaM 用于其 GPU-to-SSD direct access 展示；BaM 的上游开源实现要求 PCIe P2P、数据中心级 NVIDIA GPU 与专门系统配置，证实它仍不是开箱即用的通用服务。[Kioxia GP1](https://europe.kioxia.com/en-europe/business/news/2026/20260804-2.html)；[Kioxia 的 BaM 展示](https://www.kioxia.com/ja-jp/business/news/2026/20260611-1.html)；[BaM repository](https://github.com/ZaidQureshi/bam)

## 8. 可复现实验：如何把假设变成数据

### 7.1 当前机器与实验边界

本工作机为 Apple M3 Pro（Metal），不是 NVIDIA CUDA；截至核对时工作盘仅余约 4.9GiB。vLLM 文档显示 Apple Silicon 可通过 vLLM-Metal/MLX 做基础 inference/serving，但这不是验证 CUDA + RDMA + LMCache local-disk / GDS / CMX 路径的等价环境。[vLLM 支持平台](https://docs.vllm.ai/en/stable/getting_started/installation/gpu/)

因此分为两类实验：

| 实验 | 最低环境 | 能回答什么 | 不能回答什么 |
|---|---|---|---|
| **A. Mac 本地容量/I-O 微基准** | 释放至少 10GiB；无需下载大模型也可模拟 KV tensor 分块写入与读取 | 每 token KV 字节公式、chunk size 对写量、SSD 顺序/随机读写、缓存命中与重算的临界延迟 | 真实 GPU HBM、CUDA DMA、vLLM 调度、RDMA、生产吞吐 |
| **B. CUDA 真实 serving 实验（推荐）** | Linux + 1 块 NVIDIA GPU（建议 ≥24GB VRAM）、≥50GB 空闲 NVMe；Qwen/Llama 3B–8B + vLLM + LMCache | GPU-only、DRAM、local-NVMe KV 三者的 TTFT、ITL、cache hit、写入量、读回时间和吞吐差异 | hyperscaler / CMX 的 EB 级容量与跨 rack SLA |

### 7.2 必须做成 A/B/C 的实验矩阵

同一个模型、相同精度、相同 prompt、相同并发，只改变存储层。推荐先用一个支持 32K–128K context 的 3B–8B 开源模型；小模型的绝对 KV 容量较小，但缓存的**相对行为**可测，最后再按每 token KV 字节数换算到目标模型。

| 组别 | 配置 | 目的 |
|---|---|---|
| A：GPU-only baseline | 只使用 HBM KV / prefix cache | 得到冷启动 prefill 与 HBM-hit 的 TTFT、ITL、tokens/s 基线。|
| B：CPU DRAM tier | vLLM native `kv_offloading_size` 或 LMCache local CPU tier | 测“从 DRAM 恢复”相对重算 prefill 是否更快。|
| C：local NVMe tier | LMCache local CPU + local disk；开启预取 | 测真实 SSD 写入、L2 hit read、L2 miss 重算和尾延迟。|

每组至少运行以下三类流量，而不能只重复同一条 prompt：

| 负载 | 示例 | 要测的核心变量 |
|---|---|---|
| 共享长 prefix | 20K–64K 系统提示词/代码库，后接不同短问题 | prefix hit rate、冷/热 TTFT、写入一次后的读回次数。|
| 多轮会话 | 每轮增加 1K–2K token，间隔 5 秒、60 秒、10 分钟 | KV lifetime、reuse gap、TTL / eviction 后重算比例。|
| 多 session Agent | 50–200 会话，轮转到不同 replica 或人为清 HBM | DRAM/SSD hit、预取耗时、磁盘写量、P50/P99 TTFT。|

### 7.3 要记录的不是“是否跑通”，而是这八个数

1. `KV bytes/token`：从模型配置按层数、KV heads、head dim、KV dtype **自己复算**。
2. `active cached tokens` 与 GPU KV pool 利用率。
3. token-level 与 request-level cache hit rate。
4. KV block lifetime、idle-before-eviction、reuse gap。
5. GPU→CPU、CPU→GPU、CPU→disk、disk→CPU 的字节数与耗时。
6. 冷启动 / HBM hit / DRAM hit / SSD hit 的 P50、P95、P99 TTFT 和 ITL。
7. SSD 实际 bytes written、写放大、读带宽、queue depth 与设备温度/利用率。
8. L2 慢读时“等待”与“重算”的 break-even：当 `SSD read + prefetch > prefill recompute`，应记录为 cache miss 的经济结果。

vLLM 已公开提供 `--kv-cache-metrics` 采样，用于 KV block lifetime、idle time、reuse gap；并提供 prefix cache hit 及 offload bytes/time 的 Prometheus 指标。LMCache 的 local disk 后端用异步写入和预取到 CPU tier；这正适合上述 A/B/C 对照。[vLLM observability](https://docs.vllm.ai/en/stable/design/metrics/)；[vLLM offload configuration](https://docs.vllm.ai/en/stable/api/vllm/config/cache)；[LMCache local disk](https://github.com/lmcache/lmcache/blob/dev/docs/source/kv_cache/storage_backends/local_storage.rst)

### 7.4 如何将小模型结果外推到 Sandisk 所关心的量

小模型实测得到 `hit rate (h)`、`retention multiple (r)`、`SSD read/write bytes per active KV byte (w)` 后，只替换目标模型的 bytes/token 与目标的并发/上下文：

`target persistent SSD = target active sessions × target cached tokens/session × target KV bytes/token × r`

不能把 3B 模型的绝对 TB 直接乘到 70B、DeepSeek MLA 或闭源模型；但可以把实测的 **TTL、命中率、保留倍数、预取是否胜过重算、写放大**作为行为参数迁移。这样能把“4TB/GPU”转换成一个可被实验反驳的 `r`，而不是停留在营销规格。

## 9. 对 Sandisk / NAND 研究的可交易结论

**✅ 可确认：** KV cache 的增大、复用和跨节点迁移会提高 HBM/DRAM/高速闪存需求；RAG、代码、多轮对话与 agent 是 SSD 层最相关的场景。

**🟡 仅为情景：** 2/4/8/16TB CMX/GPU、Sandisk 的 35% workload split，均隐含很大的 retained-KV 倍数。它们不由 GPU 出货或推理 token 自动推出。

**做空所需跟踪的验证指标：** CSP/模型运营方的 active concurrency、平均 cached context、cache hit rate、TTL、跨节点迁移比例、CMX rack 出货，以及实际 NVMe/QLC bit/revenue。若这些指标没有出现，4TB/GPU 不应作为基准；若长上下文 agent 的 retained-KV 库存逼近可用 HBM 的 20–80 倍，CMX/NAND 的上行情景才开始被数据支持。
