#!/usr/bin/env python3
"""数据中心气电需求测算：未来3年(2026-2028)美国新增数据中心需要多少天然气。

口径说明（关键简化，判定见结论文档）：
- 新增数据中心 GW 一律按"平均负荷 GW"处理，不再细分 PUE（计划/存量数据本身口径混合，误差大于 PUE 修正）。
- 气耗强度按"每 GW 平均负荷"直接折算：Bcf/d = 1e6 kW × 24h × 热耗(Btu/kWh) / 1.037e12 Btu/Bcf。
- 新增负荷分两部分：表后气电（BTM，按容量 1/3）全部烧气；电网直供部分按边际气电份额 50% 烧气。
"""
import csv
from pathlib import Path

DATA = Path(__file__).parent / "data" / "assumptions.csv"

def load():
    p = {}
    with open(DATA, encoding="utf-8") as f:
        for row in csv.reader(f):
            if not row or row[0].startswith("#") or row[0] == "parameter":
                continue
            p[row[0]] = float(row[1])
    return p

BTU_PER_BCF = 1.037e12

def bcf_per_gw(heatrate):
    """每 GW 平均负荷（24/7 满载）的天然气消耗，Bcf/d。"""
    return 1e6 * 24 * heatrate / BTU_PER_BCF

def main():
    p = load()
    cc = bcf_per_gw(p["heatrate_cc"])
    sc = bcf_per_gw(p["heatrate_sc"])
    btm = p["btm_cc_share"] * cc + (1 - p["btm_cc_share"]) * sc   # 表后混合机队
    grid = cc * p["grid_marginal_gas_share"]                       # 电网侧（边际份额内全按CC）
    btm_share = p["btm_share_capacity"]

    print(f"气耗强度：联合循环 {cc:.3f} | 简单循环 {sc:.3f} | 表后混合 {btm:.3f} Bcf/d 每GW")
    print(f"电网侧边际气耗 {grid:.3f} Bcf/d 每GW（边际气电份额 {p['grid_marginal_gas_share']:.0%}）\n")

    years = [2026, 2027, 2028, 2029]
    scen = {
        "低·451存量口径": [p["dc_stock_2026"] - p["dc_stock_2025"],
                        (p["dc_stock_2028"] - p["dc_stock_2026"]) / 2,
                        (p["dc_stock_2028"] - p["dc_stock_2026"]) / 2,
                        (p["dc_stock_2030"] - p["dc_stock_2028"]) / 2],
        "中·GS计划×按期率": [p["dc_add_2026_plan"],
                        p["dc_add_2027_plan"] * p["ontime_rate_1yr"],
                        p["dc_add_2028_assume"] * p["ontime_rate_2yr"],
                        p["dc_add_2029_mid"]],
        "高·全按期(用户假设)": [p["dc_add_2026_plan"], p["dc_add_2027_plan"],
                        p["dc_add_2028_assume"], p["dc_add_2029_high"]],
    }

    prod = {2025: p["us_prod_2025"], 2026: p["us_prod_2026"], 2027: p["us_prod_2027"],
            2028: p["us_prod_2028"], 2029: p["us_prod_2029"]}
    prod_growth = {y: prod[y] - prod[y - 1] for y in years}

    print(f"{'情景':<18}{'4年新增GW':>9}{'表后GW':>8}{'累计气耗Bcf/d':>13}{'占29年产量':>11}{'表后燃机需求GW':>13}")
    results = {}
    for name, adds in scen.items():
        cum = sum(adds)
        btm_gw = cum * btm_share
        grid_gw = cum * (1 - btm_share)
        gas = btm_gw * btm + grid_gw * grid
        turb = btm_gw / p["capacity_factor"]  # 90%容量因子→装机GW
        results[name] = dict(adds=adds, cum=cum, gas=gas, turb=turb)
        print(f"{name:<18}{cum:>9.1f}{btm_gw:>8.1f}{gas:>13.2f}{gas/prod[2029]:>10.1%}{turb:>13.1f}")

    print("\n逐年新增气耗 vs 美国产量年增（Bcf/d）：")
    print(f"{'情景':<18}" + "".join(f"{y+'气耗':>10}{y+'产增':>8}" for y in []))
    hdr = f"{'情景':<18}" + "".join(f"{y}:气耗/产增".rjust(16) for y in years)
    print(hdr)
    for name, r in results.items():
        cells = ""
        prev = 0.0
        for y, a in zip(years, r["adds"]):
            g = a * btm_share * btm + a * (1 - btm_share) * grid
            cells += f"{g:>7.2f}/{prod_growth[y]:<7.1f} "
        print(f"{name:<18}{cells}")

    print("\n参照：EIA 供需平衡预测 2026: +0.5 / 2027: -1.6 Bcf/d（缺口，主因LNG出口+9%/+11%）")
    print(f"表后气电已宣布盘子 {p['btm_gas_announced']:.0f}GW（RBC），若全落地≈{p['btm_gas_announced']/p['capacity_factor']*btm:.1f} Bcf/d ≈ 美国产量{p['btm_gas_announced']/p['capacity_factor']*btm/prod[2028]:.0%}")

    # 电源结构拆分：气 vs 非气（物理口径，4 年累计新增容量）
    gf = p["btm_gas_fraction"]   # 表后中燃气占比 ~90%（RBC 技术拆分）
    ms = p["grid_marginal_gas_share"]  # 电网侧边际气电份额
    print("\n电源结构拆分（4年累计新增GW，物理口径）：")
    print(f"{'情景':<18}{'表后燃气':>9}{'表后非气':>9}{'电网·气':>9}{'电网·非气':>10}{'气合计':>8}{'气占比':>8}")
    for name, r in results.items():
        cum = r["cum"]
        btm_g = cum * btm_share * gf
        btm_o = cum * btm_share * (1 - gf)
        grd_g = cum * (1 - btm_share) * ms
        grd_o = cum * (1 - btm_share) * (1 - ms)
        tot_g = btm_g + grd_g
        print(f"{name:<18}{btm_g:>9.1f}{btm_o:>9.1f}{grd_g:>9.1f}{grd_o:>10.1f}{tot_g:>8.1f}{tot_g/cum:>8.0%}")

    # 设备需求测算（3 年窗口 2026-2028，仅气电增量）
    blk = p["cc_block_gw"]; unit = p["ha_unit_gw"]
    gt_cc = 2 / blk          # 每GW联合循环的重型燃机台数 (1.54)
    st_cc = 1 / blk          # 每GW的汽轮机 (0.77)
    hrsg_cc = 2 / blk        # 每GW的余热锅炉 (1.54)
    gt_sc = 1 / unit         # 每GW简单循环的重型燃机 (2.33)
    print("\n设备需求（3年窗口2026-28，气电增量对应）：")
    print(f"{'情景':<18}{'气电GW':>7}{'重型燃机':>9}{'内燃机':>8}{'汽轮机':>7}{'余热锅炉':>8}{'大型变压器':>9}{'EPC capex':>10}")
    for name, r in results.items():
        cum3 = sum(r["adds"][:3])
        btm_t = cum3 * btm_share * p["btm_turbine_share"]      # 表后燃机路线
        btm_e = cum3 * btm_share * p["btm_engine_share"]       # 表后内燃机路线
        grd = cum3 * (1 - btm_share) * ms                       # 电网侧气电（全CC）
        cc_gw = btm_t * p["btm_cc_share"] + grd                 # 联合循环部分
        sc_gw = btm_t * (1 - p["btm_cc_share"])                 # 简单循环部分
        gt = cc_gw * gt_cc + sc_gw * gt_sc
        eng = btm_e * p["engines_per_gw"]
        st = cc_gw * st_cc
        hrsg = cc_gw * hrsg_cc
        gsu = (btm_t + btm_e + grd) * p["gsu_per_gw"]
        capex = (btm_t + btm_e + grd) * p["capex_per_gw"]
        print(f"{name:<18}{btm_t+btm_e+grd:>7.1f}{gt:>9.0f}{eng:>8.0f}{st:>7.0f}{hrsg:>8.0f}{gsu:>9.0f}{capex:>9.0f}B")
    print(f"\n供给侧参照：全行业燃机产能 2028 年 ~{p['turbine_supply_2028']:.0f} GW/年（GEV 24 + 西门子 ~20 + 三菱 ~15 + 其他），"
          f"折合 9HA 级 ~{p['turbine_supply_2028']/unit:.0f} 台/年；但 2028 前 slot 已售罄，新单排 2030 后。")
    print("大型升压变压器：行业交期 2-3 年（Hitachi Energy/西门子能源/Prolec GE），同样供不应求。")

    # GW 口径设备链（4 年窗口 2026-2029）
    gt_share_cc = 0.86 / blk   # 联合循环中燃机容量占比 (2×0.43/1.3 = 66%)
    st_share_cc = (blk - 0.86) / blk  # 汽轮机容量占比 (34%)
    print("\nGW 口径设备链（4年累计2026-29）：")
    print(f"{'情景':<16}{'新增DC':>7}{'气电':>6}{'燃机GW':>7}{'汽轮机GW':>8}{'内燃机GW':>8}{'HRSG等容':>8}{'变压器GW':>8}{'管道Bcf/d':>9}{'非气负荷':>8}")
    for name, r in results.items():
        cum = r["cum"]
        btm_t = cum * btm_share * p["btm_turbine_share"]
        btm_e = cum * btm_share * p["btm_engine_share"]
        grd = cum * (1 - btm_share) * ms
        cc_gw = btm_t * p["btm_cc_share"] + grd
        sc_gw = btm_t * (1 - p["btm_cc_share"])
        gt_gw = cc_gw * gt_share_cc + sc_gw
        st_gw = cc_gw * st_share_cc
        gas_gw = btm_t + btm_e + grd
        non_gas = cum - cum * btm_share * gf - grd
        print(f"{name:<16}{cum:>7.1f}{gas_gw:>6.1f}{gt_gw:>7.1f}{st_gw:>8.1f}{btm_e:>8.1f}{cc_gw:>8.1f}{gas_gw:>8.1f}{r['gas']:>9.2f}{non_gas:>8.1f}")
    print("注：HRSG 按服务的联合循环 GW 等容计；变压器按气电 GW 1:1（台数见上表）；"
          "非气负荷若全靠光伏自建需 ~4× 名义装机（CF 25%）。")

    # 敏感性：边际气电份额 / 表后占比
    print("\n敏感性（高情景累计气耗 Bcf/d）：")
    print(f"{'':<12}" + "".join(f"边际气电{s:.0%}".rjust(12) for s in (0.4, 0.5, 0.6)))
    cum = results["高·全按期(用户假设)"]["cum"]
    for bs in (0.25, 0.33, 0.40):
        row = f"表后{bs:.0%}".ljust(12)
        for ms in (0.4, 0.5, 0.6):
            g = cum * bs * btm + cum * (1 - bs) * cc * ms
            row += f"{g:>12.2f}"
        print(row)

if __name__ == "__main__":
    main()
