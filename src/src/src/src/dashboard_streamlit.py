import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Market Auto Research", layout="wide")
st.title("📊 Market Auto Research — Dashboard")

ticker = st.text_input("Enter ticker (e.g., RELIANCE.NS)", "RELIANCE.NS")
period = st.selectbox("History", ["6mo", "1y", "2y", "5y"], index=1)
interval = st.selectbox("Interval", ["1d", "1h", "1wk"], index=0)

@st.cache_data(ttl=600)
def load_data(ticker, period, interval):
    df = yf.download(ticker, period=period, interval=interval, progress=False)
    df = df.rename(columns=str.title)
    return df

if ticker:
    df = load_data(ticker, period, interval)
    if df is None or df.empty:
        st.warning("No data for this ticker.")
    else:
        left, right = st.columns([2,1])
        with left:
            st.subheader(f"Price - {ticker}")
            st.line_chart(df["Close"])

        with right:
            st.metric("Last Close", f"{df['Close'].iloc[-1]:.2f}")
            chg = df['Close'].pct_change().iloc[-1] * 100
            st.metric("Change (1 bar)", f"{chg:.2f}%")

        with st.expander("Raw Data (tail)"):
            st.dataframe(df.tail())

        # RSI (simple)
        close = df["Close"]
        delta = close.diff()
        up = delta.clip(lower=0).rolling(14).mean()
        down = (-delta.clip(upper=0)).rolling(14).mean()
        rs = up / (down.replace(0, 1e-9))
        rsi = 100 - (100 / (1 + rs))
        st.subheader("RSI(14)")
        st.line_chart(rsi.dropna())
        st.caption("Heuristic: RSI < 30 oversold, > 70 overbought (context matters).")
