"""
01_ETL_Build_SQLite_FactPrices.py

Automates extraction, cleaning, and loading (ETL) of daily stock price data.
Reads multiple CSV files, infers ticker symbols, validates columns,
and loads cleaned data into a SQLite data warehouse table (fact_prices)
with primary keys and indexes for analytical querying.
"""

import os
import glob
import sqlite3
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

RAW_DATA_DIR = "data/raw"                 # folder containing CSV files
OUTPUT_DB = "output/stocks_dw.sqlite"     # SQLite database file

EXPECTED_COLUMNS = [
    "Date", "Open", "High", "Low", "Close", "Volume"
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def infer_ticker_from_filename(filename: str) -> str:
    """
    Infers stock ticker from filename.
    Example: MSFT_5y_1d.csv -> MSFT
    """
    base = os.path.basename(filename)
    return base.split("_")[0].upper()


def load_and_clean_csv(file_path: str) -> pd.DataFrame:
    """
    Loads a Yahoo Finance–style CSV and cleans column structure.
    """
    df = pd.read_csv(file_path)

    # Standardise column names
    df.columns = [col.strip().title() for col in df.columns]

    # Validate required columns
    missing_cols = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing columns in {file_path}: {missing_cols}")

    # Convert date column
    df["Date"] = pd.to_datetime(df["Date"])

    # Sort by date
    df = df.sort_values("Date")

    return df


# ============================================================
# ETL PROCESS
# ============================================================

def run_etl():
    # Connect to SQLite database
    conn = sqlite3.connect(OUTPUT_DB)
    cursor = conn.cursor()

    # Create fact table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_prices (
            ticker TEXT,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            PRIMARY KEY (ticker, date)
        )
    """)

    # Index for faster analytical queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_fact_prices_ticker
        ON fact_prices (ticker)
    """)

    # Process all CSV files
    csv_files = glob.glob(os.path.join(RAW_DATA_DIR, "*.csv"))

    for file_path in csv_files:
        ticker = infer_ticker_from_filename(file_path)
        df = load_and_clean_csv(file_path)

        df["Ticker"] = ticker

        df_to_load = df[[
            "Ticker", "Date", "Open", "High", "Low", "Close", "Volume"
        ]]

        df_to_load.columns = [
            "ticker", "date", "open", "high", "low", "close", "volume"
        ]

        df_to_load.to_sql(
            "fact_prices",
            conn,
            if_exists="append",
            index=False
        )

        print(f"Loaded {len(df_to_load)} rows for {ticker}")

    conn.commit()
    conn.close()
    print("ETL process completed successfully.")


# ============================================================
# SCRIPT ENTRY POINT
# ============================================================

if __name__ == "__main__":
    run_etl()
