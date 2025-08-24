import pandas as pd
import yfinance as yf

def fetch_ohlcv(ticker: str, period_days: int = 365, interval: str = "1d") -> pd.DataFrame:
    period = f"{period_days}d"
    df = yf.download(ticker, period=period, interval=interval, auto_adjust=False, progress=False)
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.rename(columns=str.title)
    df.index = pd.to_datetime(df.index)
    return df

def fetch_many(tickers, period_days=365, interval="1d"):
    out = {}
    for t in tickers:
        try:
            df = fetch_ohlcv(t, period_days, interval)
            out[t] = df
        except Exception as e:
            print(f"[WARN] {t}: {e}")
    return out
