"""
Data sourcing and cleaning for CFM301 Project 1.

Downloads monthly total-return series for a universe of regional equity ETFs
from Yahoo Finance's v8 chart API (one ticker at a time, paced to respect
rate limits), converts non-CAD series to Canadian dollars, and writes a
trimmed CSV of monthly returns that the analysis reads (no downloads needed
at run time).
"""
import time
import pandas as pd
import requests

# Universe: regional equity ETFs (all risky assets, 100% equities frontier)
TICKERS = {
    "XIU.TO": "Canada",        # iShares S&P/TSX 60 (CAD-denominated)
    "SPY": "US Large Cap",     # SPDR S&P 500 (USD)
    "IWM": "US Small Cap",     # iShares Russell 2000 (USD)
    "EFA": "Dev ex-NA",        # iShares MSCI EAFE (USD)
    "EEM": "Emerging",         # iShares MSCI Emerging Markets (USD)
}
FX_TICKER = "CAD=X"            # USD/CAD spot rate
PERIOD1 = 1041379200           # 2003-01-01 (EEM inception Apr-2003)
PERIOD2 = 1790625600           # ~2026-09
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}


def fetch_monthly_adjclose(ticker, retries=6):
    """Month-end adjusted closes via Yahoo v8 chart API, paced + retried."""
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
           f"?interval=1mo&period1={PERIOD1}&period2={PERIOD2}")
    last = None
    for attempt in range(retries):
        try:
            r = requests.get(url, headers=UA, timeout=30)
            if r.status_code == 200:
                j = r.json()["chart"]["result"][0]
                ts = pd.to_datetime(j["timestamp"], unit="s", utc=True)
                adj = j["indicators"]["adjclose"][0]["adjclose"]
                s = pd.Series(adj, index=ts).dropna()
                # Normalize to month-end labels (Yahoo stamps monthly bars at
                # month-start for ETFs, month-end for 24h FX) and drop the
                # still-incomplete current month.
                per = s.index.tz_convert("America/Toronto").to_period("M")
                s.index = per
                s = s[~s.index.duplicated(keep="last")]
                cur = pd.Timestamp.now(tz="America/Toronto").to_period("M")
                s = s[s.index < cur]
                s.index = s.index.to_timestamp("M")
                return s
            last = f"HTTP {r.status_code}"
        except Exception as e:  # noqa: BLE001 - transient network errors
            last = repr(e)
        time.sleep(4 * (attempt + 1))
    raise RuntimeError(f"Yahoo download failed for {ticker}: {last}")


def download_monthly_prices():
    series = {}
    for i, tkr in enumerate(list(TICKERS) + [FX_TICKER]):
        series[tkr] = fetch_monthly_adjclose(tkr)
        print(f"  {tkr}: OK ({len(series[tkr])} months)", flush=True)
        if i < len(TICKERS):  # pace requests; no sleep needed after the last
            time.sleep(3)
    monthly = pd.DataFrame(series).dropna()
    return monthly


def to_cad_returns(monthly):
    """Simple monthly total returns; USD series converted to CAD.

    R_CAD,t = (P_usd,t / P_usd,t-1) * (FX_t / FX_t-1) - 1,  FX = CAD per USD.
    XIU.TO is already CAD-denominated.
    """
    fx = monthly[FX_TICKER]
    rets = {}
    for tkr, name in TICKERS.items():
        r_usd = monthly[tkr].pct_change()
        if tkr == "XIU.TO":
            rets[name] = r_usd
        else:
            fx_ret = fx.pct_change()
            rets[name] = (1 + r_usd) * (1 + fx_ret) - 1
    out = pd.DataFrame(rets).dropna()
    out.index.name = "date"
    return out


def build_dataset(out_path="data/monthly_returns_cad.csv"):
    monthly = download_monthly_prices()
    rets = to_cad_returns(monthly)
    rets.to_csv(out_path)
    print(f"Wrote {out_path}: {rets.shape[0]} months, "
          f"{rets.index[0].date()} to {rets.index[-1].date()}")
    return rets


if __name__ == "__main__":
    build_dataset()
