import os
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from jinja2 import Template
from .utils import ensure_dir, today_str

TEMPLATE_HTML = r'''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Daily Market Report - {{ date }}</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; }
    h1 { margin-bottom: 0; }
    .subtitle { color: #555; margin-top: 4px; }
    table { border-collapse: collapse; width: 100%; margin: 16px 0; }
    th, td { border: 1px solid #ccc; padding: 8px; text-align: left; font-size: 14px; }
    th { background: #f3f3f3; }
    img { max-width: 100%; height: auto; }
    .note { color: #666; font-size: 12px; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  </style>
</head>
<body>
  <h1>Daily Market Report</h1>
  <div class="subtitle">{{ date }}</div>

  <h2>Top Picks ({{ top_n }})</h2>
  {{ top_table }}

  <div class="note">Signals are heuristic and educational. Do your own due diligence.</div>

  <h2>Index Overview</h2>
  <div class="grid">
    {% for item in index_charts %}
    <div>
      <h3>{{ item.title }}</h3>
      <img src="{{ item.path }}" alt="{{ item.title }} chart">
    </div>
    {% endfor %}
  </div>

  <h2>Watchlist Snapshots</h2>
  <div class="grid">
    {% for item in wl_charts %}
    <div>
      <h3>{{ item.title }}</h3>
      <img src="{{ item.path }}" alt="{{ item.title }} chart">
    </div>
    {% endfor %}
  </div>
</body>
</html>'''

def save_line_chart(df: pd.DataFrame, out_path: str, title: str):
    # single-plot, no custom colors/styles
    plt.figure()
    plt.plot(df.index, df['Close'])
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Close")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def dataframe_to_html_table(df: pd.DataFrame) -> str:
    return df.to_html(index=False, border=0, classes="table")

def build_report(out_dir: str, top_df: pd.DataFrame, index_map: dict, wl_map: dict, top_n: int = 10) -> str:
    ensure_dir(out_dir)
    date = today_str()
    img_dir = os.path.join(out_dir, f"imgs_{date}")
    ensure_dir(img_dir)

    # Index charts
    index_charts = []
    for name, df in index_map.items():
        if df is None or df.empty:
            continue
        path = os.path.join(img_dir, f"index_{name}.png")
        save_line_chart(df.tail(120), path, f"{name.upper()} - 6M Trend")
        index_charts.append({"title": name.upper(), "path": os.path.relpath(path, out_dir)})

    # Watchlist charts (last 90 days each)
    wl_charts = []
    for ticker, df in wl_map.items():
        if df is None or df.empty:
            continue
        safe_t = ticker.replace('.', '_')
        path = os.path.join(img_dir, f"{safe_t}.png")
        save_line_chart(df.tail(90), path, f"{ticker} - Last 90D")
        wl_charts.append({"title": ticker, "path": os.path.relpath(path, out_dir)})

    # Top table
    top_html = dataframe_to_html_table(top_df.head(top_n).round(2)) if (top_df is not None and not top_df.empty) else "<p>No picks today.</p>"

    html = Template(TEMPLATE_HTML).render(
        date=date,
        top_n=top_n,
        top_table=top_html,
        index_charts=index_charts,
        wl_charts=wl_charts,
    )

    out_path = os.path.join(out_dir, f"daily_report_{date}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    return out_path
