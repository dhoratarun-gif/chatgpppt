import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator, SMAIndicator
from ta.volatility import BollingerBands

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return df.copy()
    out = df.copy()

    close = out['Close']

    # RSI
    out['RSI_14'] = RSIIndicator(close, window=14).rsi()

    # MACD
    macd = MACD(close)
    out['MACD'] = macd.macd()
    out['MACD_SIGNAL'] = macd.macd_signal()
    out['MACD_HIST'] = macd.macd_diff()

    # EMA / SMA
    out['EMA_20'] = EMAIndicator(close, window=20).ema_indicator()
    out['SMA_50'] = SMAIndicator(close, window=50).sma_indicator()
    out['SMA_200'] = SMAIndicator(close, window=200).sma_indicator()

    # Bollinger Bands
    bb = BollingerBands(close, window=20, window_dev=2)
    out['BB_MIDDLE'] = bb.bollinger_mavg()
    out['BB_UPPER'] = bb.bollinger_hband()
    out['BB_LOWER'] = bb.bollinger_lband()
    out['BB_WIDTH'] = (out['BB_UPPER'] - out['BB_LOWER']) / out['BB_MIDDLE']

    # Returns
    out['RET_1D'] = close.pct_change(1)
    out['RET_5D'] = close.pct_change(5)
    out['RET_20D'] = close.pct_change(20)

    # Volume changes
    out['VOL_5D_AVG'] = out['Volume'].rolling(5).mean()
    out['VOL_SPIKE'] = (out['Volume'] > 1.5 * out['VOL_5D_AVG']).astype(int)

    return out
