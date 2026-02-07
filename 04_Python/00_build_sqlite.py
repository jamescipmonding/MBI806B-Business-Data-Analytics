import os
import sqlite3
import pandas as pd
import glob

# =====================================================
# CONFIGURATION
# =====================================================

# Script is inside: project/data_raw/
RAW_DIR = "."
OUT_DB = os.path.join("..", "output", "stocks_dw.sqlite")

EXPECTED_COLS = ["Date", "Open", "High", "Low", "Close", "Volume"]

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def infer_ticker_from_filename(filename: str) -> str:
    """
    Example: MSFT_5y_1d.csv -> MSFT
    """
    base = os.path.basename(filename)
    return base.split("_")[0].upper()


def load_one_csv(path: str) -> pd.DataFrame:
    """
    Loads one Yahoo Finance-style CSV.
    Your files have columns like:
    Price, Close, High, Low, Open, Volume
    where 'Price' is actually the Date.
    """
    df = pd.read_csv(path)

    # Clean column names
    df.columns = [c.strip() for c in df.columns]

    # Rename Price -> Date (based on your dataset)
    if "Price" in df.columns and "Date" not in df.columns:
        df = df.rename(columns={"Price": "Date"})

    # Validate required columns
    missing = [c for c in EXPECTED_COLS if c not in df.columns]
    if missing:
        raise ValueError(
            f"Missing columns in {os.path.basename(path)}: {missing}. "
            f"Found: {list(df.columns)}"
        )

    # Keep only expected columns
    df = df[EXPECTED_COLS].copy()

    # Convert data types
    df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce",
    format="%Y-%m-%d"
).dt.date

    for c in ["Open", "High", "Low", "Close"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["Volume"] = pd.to_numeric(df["Volume"], errors="coerce")

    # Drop invalid rows
    df = df.dropna(subset=["Date", "Close"])

    return df


# =====================================================
# MAIN ETL PROCESS (INCREMENTAL)
# =====================================================

def main():
    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUT_DB), exist_ok=True)

    # Locate CSV files
    files = sorted(glob.glob(os.path.join(RAW_DIR, "*.csv")))
    if not files:
        raise Exception("❌ No CSV files found in data_raw folder")

    # Load and combine all CSVs
    all_data = []
    for path in files:
        ticker = infer_ticker_from_filename(path)
        df = load_one_csv(path)
        df.insert(1, "Ticker", ticker)  # Date, Ticker, OHLCV
        all_data.append(df)

    fact_prices = pd.concat(all_data, ignore_index=True)
    fact_prices = fact_prices.drop_duplicates(subset=["Date", "Ticker"])

    # Convert Date to string for SQLite compatibility
    fact_prices["Date"] = fact_prices["Date"].astype(str)

    # Connect to SQLite database
    conn = sqlite3.connect(OUT_DB)
    cur = conn.cursor()

    # Create table if it does not exist (NO DROP)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fact_prices (
            Date TEXT,
            Ticker TEXT,
            Open REAL,
            High REAL,
            Low REAL,
            Close REAL,
            Volume INTEGER,
            PRIMARY KEY (Date, Ticker)
        );
    """)

    # Incremental insert (ignore duplicates automatically)
    cur.executemany("""
        INSERT OR IGNORE INTO fact_prices
        (Date, Ticker, Open, High, Low, Close, Volume)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, fact_prices.values.tolist())

    # Indexes (safe to re-run)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_prices_ticker ON fact_prices(Ticker);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_prices_date ON fact_prices(Date);")

    conn.commit()
    conn.close()

    print("✅ Incremental update completed successfully")
    print("📍 Database location:", os.path.abspath(OUT_DB))
    print("📊 Total records processed:", len(fact_prices))
    print("📈 Tickers:", sorted(fact_prices["Ticker"].unique()))


# =====================================================
# SCRIPT ENTRY POINT
# =====================================================

if __name__ == "__main__":
    main()
