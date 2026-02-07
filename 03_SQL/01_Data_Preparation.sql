-- 01_Data_Preparation.sql
-- SQLite schema used for the data warehouse in this project

CREATE TABLE IF NOT EXISTS fact_prices (
    Date   TEXT NOT NULL,
    Ticker TEXT NOT NULL,
    Open   REAL,
    High   REAL,
    Low    REAL,
    Close  REAL,
    Volume INTEGER,
    PRIMARY KEY (Date, Ticker)
);

CREATE INDEX IF NOT EXISTS idx_prices_ticker ON fact_prices (Ticker);
CREATE INDEX IF NOT EXISTS idx_prices_date ON fact_prices (Date);
