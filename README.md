# Market Auto Research — Starter Kit

An end-to-end **daily stock market research automation** + **dashboard**.

## Features
- Fetch OHLCV data via `yfinance`
- Compute RSI, MACD, Bollinger Bands, EMA/SMA
- Daily **screeners** (oversold, momentum, volume breakout)
- Auto-generate **HTML report** with charts
- **Streamlit dashboard** for watchlist, charts, and indicators
- Simple config in `config.yaml`
- Schedule with **cron** (Linux) or **Task Scheduler** (Windows)

> Note: For Indian equities on Yahoo Finance, use the `.NS` suffix (e.g., `RELIANCE.NS`, `TCS.NS`).

## Setup

```bash
# 1) Create and activate venv (recommended)
python -m venv .venv
# Windows:
.\.venv\Scripts\Activate.ps1
# Mac/Linux:
source .venv/bin/activate

# 2) Install deps
pip install -r requirements.txt
