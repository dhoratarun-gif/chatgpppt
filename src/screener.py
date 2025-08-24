import pandas as pd

def latest_row(df: pd.DataFrame) -> pd.Series:
    if df is None or df.empty:
        return pd.Series()
    return df.iloc[-1]

def screen_rules(latest: pd.Series) -> dict:
    signals = {}

    # Oversold / Overbought (RSI)
    rsi = latest.get('RSI_14', None)
    if rsi is not None:
        if rsi <= 30:
            signals['RSI'] = 'Oversold (<=30)'
        elif rsi >= 70:
            signals['RSI'] = 'Overbought (>=70)'

    # MACD cross (hist > 0 bullish, < 0 bearish as a simple proxy)
    macd_hist = latest.get('MACD_HIST', None)
    if macd_hist is not None:
        if macd_hist > 0:
            signals['MACD'] = 'Bullish momentum (hist > 0)'
        elif macd_hist < 0:
            signals['MACD'] = 'Bearish momentum (hist < 0)'

    # Price vs moving averages
    close = latest.get('Close', None)
    sma50 = latest.get('SMA_50', None)
    sma200 = latest.get('SMA_200', None)
    if close is not None and sma50 is not None:
        if close > sma50:
            signals['MA_50'] = 'Above 50SMA (uptrend bias)'
        else:
            signals['MA_50'] = 'Below 50SMA (weakness)'

    if close is not None and sma200 is not None:
        if close > sma200:
            signals['MA_200'] = 'Above 200SMA (long-term uptrend)'
        else:
            signals['MA_200'] = 'Below 200SMA (long-term weakness)'

    # Volume spike
    if latest.get('VOL_SPIKE', 0) == 1:
        signals['VOLUME'] = 'Volume spike (>1.5x 5D avg)'

    return signals

def score_stock(latest: pd.Series) -> float:
    """Simple score (0-100) combining momentum and trend proxies."""
    score = 50.0
    if latest.get('MACD_HIST', 0) > 0:
        score += 10
    if latest.get('RSI_14', 50) > 55:
        score += 10
    if latest.get('Close', 0) > latest.get('SMA_50', 0):
        score += 10
    if latest.get('Close', 0) > latest.get('SMA_200', 0):
        score += 10
    if latest.get('VOL_SPIKE', 0) == 1:
        score += 5
    return max(0, min(100, score))

def run_screener(indicator_map: dict) -> pd.DataFrame:
    rows = []
    for ticker, df in indicator_map.items():
        if df is None or df.empty:
            continue
        latest = latest_row(df)
        signals = screen_rules(latest)
        score = score_stock(latest)
        rows.append({
            "Ticker": ticker,
            "Close": latest.get("Close", float('nan')),
            "RSI_14": latest.get("RSI_14", float('nan')),
            "MACD_HIST": latest.get("MACD_HIST", float('nan')),
            "SMA_50": latest.get("SMA_50", float('nan')),
            "SMA_200": latest.get("SMA_200", float('nan')),
            "VOL_SPIKE": latest.get("VOL_SPIKE", 0),
            "Signals": ", ".join(f"{k}:{v}" for k, v in signals.items()) if signals else "",
            "Score": score
        })
    df = pd.DataFrame(rows).sort_values("Score", ascending=False)
    return df
