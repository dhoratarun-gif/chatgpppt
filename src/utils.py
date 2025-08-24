import os
from datetime import datetime

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def today_str():
    return datetime.now().strftime("%Y-%m-%d")
