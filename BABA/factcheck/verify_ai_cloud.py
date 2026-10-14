#!/usr/bin/env python3
"""复算阿里 AI/云分部指标。单位：人民币亿元；只做算术，不抓取数据。

原始值：阿里 FY2026 全年及 FY2027Q1 业绩公告，见 BABA/AI与云业务.md。
"""

fy26_cloud_revenue = 1581.3
fy26_cloud_ebita = 142.7
q1_cloud_revenue = 484.37
q1_cloud_revenue_prev = 334.18
q1_cloud_ebita = 56.28
q1_cloud_ebita_prev = 24.19
q1_ai_product_revenue = 123.76
q1_labs_revenue = 33.38
q1_labs_ebita = -138.61
q1_labs_ebita_prev = -32.24
q1_group_capex = 676.78
q1_group_cfo = 229.45
q1_group_fcf = -446.70

print(f"FY2026旧云分部经调整EBITA利润率: {fy26_cloud_ebita / fy26_cloud_revenue:.1%}")
print(f"FY2027Q1新云与算力收入同比: {q1_cloud_revenue / q1_cloud_revenue_prev - 1:.1%}")
print(f"FY2027Q1新云与算力经调整EBITA利润率: {q1_cloud_ebita / q1_cloud_revenue:.1%}")
print(f"上年同期重述利润率: {q1_cloud_ebita_prev / q1_cloud_revenue_prev:.1%}")
print(f"AI相关产品占云与算力分部收入: {q1_ai_product_revenue / q1_cloud_revenue:.1%}")
print(f"AI相关产品季度收入简单乘四: {q1_ai_product_revenue * 4:.2f}亿元/年（年化速度，非合同ARR）")
print(f"按管理层‘占外部收入约35%’反推外部云收入: {q1_ai_product_revenue / .35:.1f}亿元（近似推算）")
print(f"云收入减上述外部估算: {q1_cloud_revenue - q1_ai_product_revenue / .35:.1f}亿元（近似内部收入）")
print(f"云与算力 + AI实验室合计经调整EBITA: {q1_cloud_ebita + q1_labs_ebita:.2f}亿元（分部和，非合并AI利润）")
print(f"上年同期重述分部和: {q1_cloud_ebita_prev + q1_labs_ebita_prev:.2f}亿元")
print(f"集团CFO减集团FCF: {q1_group_cfo - q1_group_fcf:.2f}亿元；集团披露CapEx: {q1_group_capex:.2f}亿元")
