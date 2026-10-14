# Kioxia 项目 主线任务1: wafer -> bit NAND 全球供给模型
# 校准锚点: Counterpoint Q2 2026 bit 份额 × TechInsights 2026 总需求插值 1,216 EB
# 前推: wafer 产能时间表(公开报道) × TB/wafer 制程迁移增速(各家世代路线图)

# ---------- 2026 校准 ----------
demand = {2025: 997, 2026: 1216, 2027: 1484, 2028: 1807, 2029: round(1807*1.22)}  # EB; 2026/27/29 为插值/外推
shares = {'Samsung': .25, 'SK/Solidigm': .22, 'JV(Kioxia+SanDisk)': .25, 'Micron': .13, 'YMTC': .14}  # JV=Kioxia~14%+SanDisk11%
eb2026 = {k: v*demand[2026] for k,v in shares.items()}

# 2026 年均 wafer 产能 (千片/月) — 公开报道最佳估计
wafers2026 = {'Samsung': 420, 'SK/Solidigm': 350, 'JV(Kioxia+SanDisk)': 475, 'Micron': 275, 'YMTC': 200}

print("=== 2026 校准: 隐含 TB/wafer ===")
tbw = {}
for k in shares:
    tbw[k] = eb2026[k]*1000/(wafers2026[k]*12)  # EB->TB
    print(f"{k:22s} EB={eb2026[k]:6.0f}  wafers={wafers2026[k]}k/月  ->  {tbw[k]:.0f} TB/wafer")

# ---------- 前推假设 ----------
# TB/wafer 年增速(制程迁移): 各家世代路线
g_base = {'Samsung': .20, 'SK/Solidigm': .25, 'JV(Kioxia+SanDisk)': .25, 'Micron': .22, 'YMTC': .25}

# wafer 产能路径 (千片/月, 年均) 三情景
W = {
 'base': {
   'Samsung':            {2026:420, 2027:430, 2028:460, 2029:490},   # P5 部分 NAND 2028 起
   'SK/Solidigm':        {2026:350, 2027:355, 2028:360, 2029:380},   # M17 2029H1 才运营
   'JV(Kioxia+SanDisk)': {2026:475, 2027:520, 2028:570, 2029:630},   # K2 爬坡+四日市扩产(2029 产能翻倍目标)
   'Micron':             {2026:275, 2027:280, 2028:300, 2029:340},   # 新加坡 2028H2 首批
   'YMTC':               {2026:200, 2027:250, 2028:300, 2029:375}},  # Reuters 路径+Fab4 部分
 'bull_supply': {  # 供给激进(价格下行风险)
   'Samsung':            {2026:420, 2027:445, 2028:500, 2029:560},
   'SK/Solidigm':        {2026:350, 2027:360, 2028:380, 2029:430},
   'JV(Kioxia+SanDisk)': {2026:475, 2027:530, 2028:600, 2029:680},
   'Micron':             {2026:275, 2027:285, 2028:320, 2029:400},
   'YMTC':               {2026:200, 2027:280, 2028:380, 2029:480}},   # Fab3 快爬坡+Fab4/5 落地
 'bear_supply': {  # 供给保守(紧张延续)
   'Samsung':            {2026:420, 2027:425, 2028:440, 2029:460},
   'SK/Solidigm':        {2026:350, 2027:352, 2028:355, 2029:365},
   'JV(Kioxia+SanDisk)': {2026:475, 2027:505, 2028:545, 2029:590},
   'Micron':             {2026:275, 2027:278, 2028:290, 2029:315},
   'YMTC':               {2026:200, 2027:225, 2028:260, 2029:300}},   # 接近发向工厂研究所路径
}

def run(scenario, gmult=1.0):
    out = {}
    for y in [2026,2027,2028,2029]:
        tot = 0
        for k in shares:
            tb = tbw[k]*(1+g_base[k]*gmult)**(y-2026)
            tot += W[scenario][k][y]*12*tb/1000
        out[y] = tot
    return out

print("\n=== 全球 NAND 供给 vs 需求 (EB/年) ===")
print(f"{'情景':14s}" + "".join(f"{y:>10d}" for y in [2026,2027,2028,2029]))
for sc in ['bear_supply','base','bull_supply']:
    s = run(sc)
    print(f"{sc:14s}" + "".join(f"{s[y]:10.0f}" for y in s))
print(f"{'需求':14s}" + "".join(f"{demand[y]:10.0f}" for y in [2026,2027,2028,2029]))

print("\n=== 充足率 = (供给-需求)/需求 ===")
for sc in ['bear_supply','base','bull_supply']:
    s = run(sc)
    print(f"{sc:14s}" + "".join(f"{(s[y]-demand[y])/demand[y]*100:9.1f}%" for y in s))

print("\n=== 供给年增速 (base) ===")
s = run('base')
for y in [2027,2028,2029]:
    print(f"{y}: {(s[y]/s[y-1]-1)*100:.1f}%  (需求增速 ~22%)")

# 敏感性: 制程迁移增速 ±5pp
print("\n=== 敏感性: TB/wafer 增速整体 ±5pp (base 产能) ===")
for m,lab in [(0.765,'-5pp'),(1.235,'+5pp')]:
    s = run('base', m)
    print(f"{lab}: " + "".join(f"{y}:{(s[y]-demand[y])/demand[y]*100:+.1f}%  " for y in [2027,2028,2029]))

# YMTC 单变量敏感性 (评审关注点)
print("\n=== YMTC 路径敏感性 (2028/2029 充足率, base 其余不变) ===")
for yw, lab in [({2027:250,2028:300,2029:375},'Reuters路径'),
                ({2027:225,2028:260,2029:300},'保守路径'),
                ({2027:280,2028:380,2029:480},'激进路径')]:
    for y in [2028,2029]:
        tot = 0
        for k in shares:
            w = yw[y] if k=='YMTC' else W['base'][k][y]
            tb = tbw[k]*(1+g_base[k])**(y-2026)
            tot += w*12*tb/1000
        print(f"{lab} {y}: 供给 {tot:.0f} EB, 充足率 {(tot-demand[y])/demand[y]*100:+.1f}%", end="   ")
    print()

# ---------- 密度迁移 vs wafer 扩张 分解 (主线任务1追问, 2026-08-20) ----------
print("\n=== 2026→2029 供给增长分解 (base) ===")
years = [2026,2029]
def supply(wmap, density_years):
    tot = 0
    for k in shares:
        tb = tbw[k]*(1+g_base[k])**density_years
        tot += wmap[k]*12*tb/1000
    return tot

s26   = supply({k:W['base'][k][2026] for k in shares}, 0)
s29_full    = supply({k:W['base'][k][2029] for k in shares}, 3)
s29_denonly = supply({k:W['base'][k][2026] for k in shares}, 3)   # wafer 冻结在 2026
s29_waferonly = supply({k:W['base'][k][2029] for k in shares}, 0) # 密度冻结在 2026

print(f"2026 供给:            {s26:.0f} EB")
print(f"2029 全要素:          {s29_full:.0f} EB")
print(f"2029 仅密度迁移:      {s29_denonly:.0f} EB  (所有 fab 冻结在 2026 规模)")
print(f"2029 仅 wafer 扩张:   {s29_waferonly:.0f} EB  (所有制程冻结在 2026)")
d_tot = s29_full - s26; d_den = s29_denonly - s26; d_waf = s29_waferonly - s26
d_int = d_tot - d_den - d_waf
print(f"\n总增量 {d_tot:.0f} EB = 密度 {d_den:.0f} ({d_den/d_tot*100:.0f}%) + wafer {d_waf:.0f} ({d_waf/d_tot*100:.0f}%) + 交互 {d_int:.0f} ({d_int/d_tot*100:.0f}%)")
print(f"2029 需求预测:        {demand[2029]} EB")
print(f"=> 密度迁移单独造成的供给 ({s29_denonly:.0f}) vs 2029 需求 ({demand[2029]}): 充足率 {(s29_denonly-demand[2029])/demand[2029]*100:+.1f}%")

print("\n=== 各家密度迁移倍数 (2026→2029, wafer 不变) ===")
for k in shares:
    m = (1+g_base[k])**3
    print(f"{k:22s} ×{m:.2f}  ({eb2026[k]:.0f} → {eb2026[k]*m:.0f} EB)")

print("\n=== 密度增速敏感性: 仅密度迁移的 2029 供给 ===")
for g,lab in [(0.15,'+15%/年'),(0.20,'+20%/年'),(0.25,'+25%/年'),(0.30,'+30%/年')]:
    tot = sum(wafers2026[k]*12*tbw[k]*(1+g)**3/1000 for k in shares)
    print(f"{lab}: {tot:.0f} EB (vs 2029 需求 {demand[2029]}, 充足率 {(tot-demand[2029])/demand[2029]*100:+.1f}%)")
