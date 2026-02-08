# Data Notes

## Data Source
The dataset used in this project consists of historical daily stock price data
downloaded from Yahoo Finance. Each CSV file represents a single stock ticker
and contains time-series price and volume information.

The data was exported in CSV format and stored locally prior to processing.

---

## Time Period Covered
The dataset covers multiple years of daily trading data per stock.
The exact coverage period varies by ticker, depending on availability
from Yahoo Finance at the time of download.

---

## Data Structure
Each raw CSV file contains the following columns:

- Date
- Open
- High
- Low
- Close
- Volume

Each file represents one stock ticker, inferred directly from the filename
(e.g., `MSFT_5y_1d.csv` → ticker = MSFT).

---

## Data Cleaning and Preparation
The following data preparation steps were applied during the ETL process:

- Standardised column naming for consistency
- Validated presence of required columns
- Converted the `Date` column to a proper date format
- Sorted records chronologically
- Appended ticker identifiers to each record
- Loaded cleaned data into a SQLite fact table (`fact_prices`)
- Enforced a composite primary key on `(ticker, date)` to prevent duplicates

---

## Data Storage
Cleaned and validated data was loaded into a SQLite data warehouse.
The primary analytical table is:

- **fact_prices**
  - ticker
  - date
  - open
  - high
  - low
  - close
  - volume

Indexes were created on key fields to support efficient analytical queries.

---

## Assumptions and Limitations
- The data reflects historical prices and does not account for dividends,
  stock splits, or corporate actions unless already adjusted by the source.
- Missing trading days correspond to non-trading days (e.g., weekends, holidays).
- The analysis is intended for educational and analytical purposes,
  not for real-time trading or investment decisions.
