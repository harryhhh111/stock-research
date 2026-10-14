#!/usr/bin/env python3
"""从 SEC companyfacts JSON 提取阿里巴巴(Alibaba Group, CIK 1577552)关键年度财务数据。
口径：US GAAP，20-F 年度数据。金额原始单位 USD，输出按标签分年度列出（$B）。
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "baba_companyfacts.json")

# 关注字段（us-gaap）
FIELDS = {
    "Revenues": "营收",
    "RevenueFromContractWithCustomerExcludingAssessedTax": "营收(履约口径)",
    "NetIncomeLoss": "净利润",
    "ProfitLoss": "利润(含少数股东)",
    "NetCashProvidedByUsedInOperatingActivities": "经营现金流",
    "PaymentsToAcquirePropertyPlantAndEquipment": "CapEx",
    "PaymentsToAcquireProductiveAssets": "CapEx(生产性资产)",
    "Assets": "总资产",
    "StockholdersEquity": "股东权益",
    "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest": "权益(含少数股东)",
    "ShareBasedCompensation": "SBC",
    "PaymentsForRepurchaseOfCommonStock": "回购",
    "PaymentsOfDividends": "分红",
    "PaymentsOfDividendsCommonStock": "分红(普通股)",
    "ResearchAndDevelopmentExpense": "研发费用",
    "OperatingIncomeLoss": "营业利润",
    "GrossProfit": "毛利",
    "EarningsPerShareDiluted": "EPS摊薄",
    "WeightedAverageNumberOfDilutedSharesOutstanding": "摊薄股数",
    "CashAndCashEquivalentsAtCarryingValue": "现金及等价物",
    "ShortTermInvestments": "短期投资",
    "MarketableSecuritiesCurrent": "流动证券",
}

with open(DATA) as f:
    facts = json.load(f)

gaap = facts.get("facts", {}).get("us-gaap", {})
entity = facts.get("entityName", "?")
print(f"entity: {entity}, cik: {facts.get('cik')}")


def annual(items):
    """取 FY duration 数据（frame 为年度，无 frame 也行但取 fp=FY/20-F）。"""
    out = []
    for it in items:
        if it.get("form") != "20-F":
            continue
        # start/end 为期初/期末；财年 = end 的日历年
        out.append((it.get("end"), it.get("start"), it.get("val"), it.get("fy"), it.get("filed")))
    return out


for field, cn in FIELDS.items():
    node = gaap.get(field)
    if not node:
        continue
    units = node.get("units", {})
    unit = "USD" if "USD" in units else list(units.keys())[0]
    rows = annual(units[unit])
    if not rows:
        continue
    print(f"\n## {field} ({cn})  unit={unit}")
    seen = set()
    for end, start, val, fy, filed in sorted(rows):
        if start is None:  # instant
            key = (end, val)
            if key in seen:
                continue
            seen.add(key)
            print(f"  {end}  {val/1e9:,.3f} B   (filed {filed})")
        else:
            print(f"  FY{end[:4]} ({start}~{end})  {val/1e9:,.3f} B   (filed {filed})")
