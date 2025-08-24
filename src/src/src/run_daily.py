import os, yaml
from utils import ensure_dir
from data_fetch import fetch_many
from tech_indicators import add_indicators
from screener import run_screener
from report import build_report

def main():
    cfg_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
    with open(cfg_path, "r") as f:
        cfg = yaml.safe_load(f)

    watchlist = cfg.get("watchlist", [])
    idx = cfg.get("index_tickers", {})
    lookback = cfg.get("data", {}).get("lookback_days", 365)
    interval = cfg.get("data", {}).get("interval", "1d")
    report_cfg = cfg.get("report", {})
    out_dir = os.path.join(os.path.dirname(__file__), "..", report_cfg.get("out_dir", "reports"))
    top_n = int(report_cfg.get("top_n", 10))

    ensure_dir(out_dir)

    print(f"[INFO] Fetching watchlist ({len(watchlist)}) ...")
    wl_map = fetch_many(watchlist, period_days=lookback, interval=interval)
    print(f"[INFO] Fetching indexes ({len(idx)}) ...")
    idx_map = fetch_many(idx.values(), period_days=lookback, interval=interval)

    print("[INFO] Adding indicators ...")
    wl_ind = {t: add_indicators(df) for t, df in wl_map.items()}

    print("[INFO] Running screener ...")
    top_df = run_screener(wl_ind)
    if top_df is not None and not top_df.empty:
        print(top_df.head(15).to_string(index=False))

    print("[INFO] Building report ...")
    idx_named = dict(zip(idx.keys(), idx_map.values()))
    out_path = build_report(out_dir, top_df, idx_named, wl_map, top_n=top_n)
    print(f"[DONE] Report saved to: {out_path}")

if __name__ == "__main__":
    main()
