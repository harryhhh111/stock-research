import pandas as pd, json, os

D = os.path.dirname(os.path.abspath(__file__)) + "/data"

def prices(t):
    df = pd.read_csv(f"{D}/{t}.csv", parse_dates=["Date"])
    df = df.dropna(subset=["Close"]).sort_values("Date").reset_index(drop=True)
    return df

def dev_row(t, date=None):
    df = prices(t)
    df["ma200"] = df["Close"].rolling(200).mean()
    df["dev"] = df["Close"] / df["ma200"] - 1
    last = df.iloc[-1]
    out = {
        "ticker": t,
        "last_date": str(last["Date"].date()),
        "last_close": round(last["Close"], 2),
        "ma200": round(last["ma200"], 2) if pd.notna(last["ma200"]) else None,
        "dev_now_%": round(last["dev"] * 100, 1) if pd.notna(last["dev"]) else None,
        "max_dev_2y_%": round(df["dev"].max() * 100, 1),
        "max_dev_2y_date": str(df.loc[df["dev"].idxmax(), "Date"].date()),
    }
    if date:
        row = df[df["Date"] <= date]
        if len(row):
            r = row.iloc[-1]
            out[f"close@{date}"] = round(r["Close"], 2)
            out[f"dev@{date}_%"] = round(r["dev"] * 100, 1) if pd.notna(r["dev"]) else None
    return out

rows = []
for t in ["^SOX", "MU", "CAT", "NVDA", "PLTR", "AMAT", "SOXX", "TSLA", "ADBE", "ADSK"]:
    rows.append(dev_row(t, date="2026-06-30"))
res = pd.DataFrame(rows)
print(res.to_string(index=False))

# valuation metrics
info_rows = []
for t in ["CAT", "MU", "NVDA", "PLTR", "AMAT", "TSLA", "ADBE", "ADSK", "SOXX"]:
    df = pd.read_csv(f"{D}/info_{t}.csv")
    r = df.iloc[0]
    def g(k):
        return r[k] if k in df.columns and pd.notna(r[k]) else None
    info_rows.append({
        "ticker": t,
        "price": g("currentPrice"),
        "trailingPE": g("trailingPE"),
        "forwardPE": g("forwardPE"),
        "P/S_ttm": g("priceToSalesTrailing12Months"),
        "200DMA_yahoo": g("twoHundredDayAverage"),
        "52w_high": g("fiftyTwoWeekHigh"),
        "52w_low": g("fiftyTwoWeekLow"),
    })
info = pd.DataFrame(info_rows)
print()
print(info.to_string(index=False))
res.to_csv(f"{D}/computed_dev.csv", index=False)
info.to_csv(f"{D}/computed_info.csv", index=False)
