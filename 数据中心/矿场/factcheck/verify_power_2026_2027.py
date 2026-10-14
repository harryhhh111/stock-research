"""复算研究笔记中的容量小计；无第三方依赖，不写文件。单位 MW。"""

released_2026 = {
    "Cipher Black Pearl 已运营矿业容量": 150,
    "Keel 美国退出矿业站点额定容量": 18 + 60 + 63 + 110,
    "TeraWulf 矿业容量下降": 245 - 145,
}

# 原矿场园区口径：包括园区扩建，不是严格的旧矿业电力释放量。
# 2026 是已披露运营容量与明确年内目标组成的保守计入小计，非全年预测。
campus_it_2026 = {
    "Core Scientific 已计费容量锚": 437,
    "IREN 全年交付目标": 300,
    "TeraWulf 已投运容量锚": 102,
    "Galaxy Helios Phase I": 133,
    "Bitdeer Tydal 合同第一阶段": 121 / 2,
    "Riot AMD": 25 + 10,
}

# 2027 是按计划完成的情景，非已交付/全行业预测。
# IREN 600 = 800 全公司目标 - Sweetwater 新园区初期 200；是研究者桥接假设。
campus_it_2027 = {
    "Core Scientific 仅 CoreWeave 合同": 590,
    "IREN 既有园区桥接假设": 800 - 200,
    "TeraWulf Lake Mariner": 438,
    "Galaxy 仅 Helios Phase I": 133,
    "Bitdeer Tydal + WA + TN": 121 + 42.7 + 10 + 55,
    "Riot AMD 与 AI lab 首期": 50 + 96,
    "Cipher Black Pearl": 216,
}

if __name__ == "__main__":
    for title, rows in [
        ("2026 退出矿业站点容量小计（非实际平均用电下降）", released_2026),
        ("2026 年末原矿场园区 AI IT 保守计入小计", campus_it_2026),
        ("2027 年末原矿场园区 AI IT 排期情景", campus_it_2027),
    ]:
        print(title)
        for name, mw in rows.items():
            print(f"  {name}: {mw:g} MW")
        print(f"  合计: {sum(rows.values()):.1f} MW = {sum(rows.values()) / 1000:.4f} GW\n")
