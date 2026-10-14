#!/usr/bin/env python3
"""KV cache 分层容量的透明教学型敏感性演算；仅使用标准库。

口径：容量均为逻辑 KV 容量（未含 SSD OP/RAID/副本），二进制 TiB/PiB。
警告：10,000 并发、context buckets、DRAM/SSD multipliers 均为未验证的示例参数，
不得将输出当作运营商实际容量或 NAND 市场需求预测。
运行：python3 SSD/factcheck/kv_tier_model.py
"""

from dataclasses import dataclass

GIB = 1024**3
TIB = 1024**4
PIB = 1024**5


@dataclass(frozen=True)
class Architecture:
    name: str
    layers: int
    cached_elements_per_layer_token: int
    bytes_per_element: int

    @property
    def bytes_per_token(self) -> int:
        return self.layers * self.cached_elements_per_layer_token * self.bytes_per_element


@dataclass(frozen=True)
class Workload:
    name: str
    concurrent_active_sessions: int
    cached_tokens_per_session: int
    dram_warm_multiple: float
    ssd_persistent_multiple: float


ARCHITECTURES = (
    # 2(K,V) * 8 KV heads * 128 head dimension = 2,048 cached values/layer/token.
    Architecture("Llama-3.1-70B GQA / BF16", 80, 2 * 8 * 128, 2),
    # DeepSeek-V3 MLA: 512 latent KV + 64 RoPE values/layer/token.
    Architecture("DeepSeek-V3 MLA / BF16", 61, 512 + 64, 2),
)

# 以下并发、context 与 three 个倍数是教学情景假设，并非厂商实测：
# DRAM 仅放 active KV 之外的 warm KV；SSD 仅放有复用价值的 persistent KV。
WORKLOADS = (
    Workload("短对话 / 共享前缀", 10_000, 8_192, 0.25, 0.05),
    Workload("RAG、代码与多轮会话", 10_000, 32_768, 1.00, 2.00),
    Workload("长上下文、长期 Agent", 10_000, 131_072, 2.00, 10.00),
)


def fmt_capacity(value: float) -> str:
    if value >= PIB:
        return f"{value / PIB:.2f} PiB"
    if value >= TIB:
        return f"{value / TIB:.1f} TiB"
    return f"{value / GIB:.1f} GiB"


def main() -> None:
    print("# KV cache tier sensitivity model (NOT a market forecast)")
    print("All capacities are logical; no SSD OP/RAID/replication included.")
    print("Concurrency, contexts, and DRAM/SSD multipliers are unvalidated example inputs.\n")

    for arch in ARCHITECTURES:
        print(f"## {arch.name}")
        print(
            f"bytes/token = {arch.layers} layers × "
            f"{arch.cached_elements_per_layer_token} cached elements × "
            f"{arch.bytes_per_element} bytes = "
            f"{arch.bytes_per_token:,} bytes "
            f"({arch.bytes_per_token / 1024:.3f} KiB)"
        )
        print("| workload | active HBM KV | warm DRAM KV | persistent SSD KV |")
        print("|---|---:|---:|---:|")
        for workload in WORKLOADS:
            active = (
                workload.concurrent_active_sessions
                * workload.cached_tokens_per_session
                * arch.bytes_per_token
            )
            dram = active * workload.dram_warm_multiple
            ssd = active * workload.ssd_persistent_multiple
            print(
                f"| {workload.name} | {fmt_capacity(active)} | "
                f"{fmt_capacity(dram)} | {fmt_capacity(ssd)} |"
            )
        print()

    # A Rubin GPU has 288 GB HBM4. 192 GiB remaining for KV is a planning assumption,
    # after model weights/runtime; this derives the concurrency impact of that assumption.
    hbm_kv_per_gpu = 192 * GIB
    rack_gpu_count = 72
    rack_kv = hbm_kv_per_gpu * rack_gpu_count
    print("## Rubin NVL72 active-KV sensitivity")
    print("Assumption: 192 GiB KV headroom/GPU; 72 GPUs -> 13.5 TiB logical active KV headroom.")
    print("| architecture | 8K context sessions/rack | 32K | 128K |")
    print("|---|---:|---:|---:|")
    for arch in ARCHITECTURES:
        values = []
        for tokens in (8_192, 32_768, 131_072):
            per_session = tokens * arch.bytes_per_token
            values.append(f"{rack_kv / per_session:,.0f}")
        print(f"| {arch.name} | {' | '.join(values)} |")

    print("\n## CMX multiplier interpretation")
    print("A CMX allocation of X TB/GPU is not implied by concurrency; it embeds a retained-KV multiple.")
    print("| CMX allocation | multiple of 288 GB raw HBM | multiple of 192 GiB usable KV headroom |")
    print("|---|---:|---:|")
    for tb in (2, 4, 8, 16):
        # Use decimal TB to match SSD product capacity conventions.
        bytes_capacity = tb * 1_000_000_000_000
        print(
            f"| {tb} TB/GPU | {bytes_capacity / (288 * GIB):.1f}x | "
            f"{bytes_capacity / hbm_kv_per_gpu:.1f}x |"
        )


if __name__ == "__main__":
    main()
