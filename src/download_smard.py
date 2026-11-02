"""
Download hourly German electricity market data from SMARD (Bundesnetzagentur).

SMARD serves data in weekly JSON chunks:
  1. index:  https://www.smard.de/app/chart_data/{filter}/{region}/index_hour.json
             -> {"timestamps": [ms_epoch, ...]}  (one timestamp per weekly chunk)
  2. chunk:  https://www.smard.de/app/chart_data/{filter}/{region}/{filter}_{region}_hour_{ts}.json
             -> {"series": [[ms_epoch, value], ...]}

This script downloads every chunk that overlaps the requested period for each series,
merges them into one hourly table and saves it as data/raw/smard_hourly.csv.

Usage:
    python src/download_smard.py --start 2024-01-01 --end 2026-10-31
"""
import argparse
import time
from pathlib import Path

import pandas as pd
import requests

BASE = "https://www.smard.de/app/chart_data"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw" / "smard_hourly.csv"

# column name -> (SMARD filter id, region)
SERIES = {
    "price_eur_mwh": (4169, "DE-LU"),   # day-ahead price, bidding zone Germany/Luxembourg
    "load_mwh":      (410,  "DE"),      # total grid load (Netzlast)
    "residual_load_mwh": (4359, "DE"),  # load minus wind and solar
    "wind_onshore_mwh":  (4067, "DE"),
    "wind_offshore_mwh": (1225, "DE"),
    "solar_mwh":         (4068, "DE"),
}

session = requests.Session()
session.headers["User-Agent"] = "de-power-price-forecast (portfolio project)"


def get_json(url, retries=3):
    for attempt in range(retries):
        try:
            r = session.get(url, timeout=30)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            if attempt == retries - 1:
                raise
            print(f"  retry {attempt + 1} after error: {e}")
            time.sleep(2 * (attempt + 1))


def download_series(filter_id, region, start_ms, end_ms):
    index = get_json(f"{BASE}/{filter_id}/{region}/index_hour.json")["timestamps"]
    week_ms = 7 * 24 * 3600 * 1000
    # keep chunks that overlap [start, end]; a chunk covers [ts, ts + 1 week)
    chunks = [ts for ts in index if ts + week_ms > start_ms and ts <= end_ms]
    rows = []
    for i, ts in enumerate(chunks, 1):
        data = get_json(f"{BASE}/{filter_id}/{region}/{filter_id}_{region}_hour_{ts}.json")
        rows.extend(data["series"])
        if i % 10 == 0 or i == len(chunks):
            print(f"  {i}/{len(chunks)} weeks")
        time.sleep(0.2)  # be polite to the public server
    s = pd.DataFrame(rows, columns=["ts_ms", "value"]).dropna()
    s = s[(s.ts_ms >= start_ms) & (s.ts_ms <= end_ms)].drop_duplicates("ts_ms")
    return s.set_index("ts_ms")["value"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2024-01-01")
    ap.add_argument("--end", default="2026-10-31")
    args = ap.parse_args()

    tz = "Europe/Berlin"
    start_ms = int(pd.Timestamp(args.start, tz=tz).timestamp() * 1000)
    end_ms = int((pd.Timestamp(args.end, tz=tz) + pd.Timedelta(days=1)).timestamp() * 1000) - 1

    cols = {}
    for name, (fid, region) in SERIES.items():
        print(f"Downloading {name} (filter {fid}, {region})")
        cols[name] = download_series(fid, region, start_ms, end_ms)

    df = pd.DataFrame(cols).sort_index()
    df.index = pd.to_datetime(df.index, unit="ms", utc=True).tz_convert(tz)
    df.index.name = "timestamp"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT)

    print(f"\nSaved {len(df):,} hourly rows to {OUT}")
    print(f"Period: {df.index.min()} -> {df.index.max()}")
    print("Missing values per column:")
    print(df.isna().sum().to_string())


if __name__ == "__main__":
    main()
