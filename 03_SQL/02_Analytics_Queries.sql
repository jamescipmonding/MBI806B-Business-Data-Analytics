-- 02_Analytics_Queries.sql
-- Analytics queries for time-series stock data in fact_prices (SQLite)

----------------------------------------------------------------------
-- Q1) Row count and date range per ticker
----------------------------------------------------------------------
SELECT
  Ticker,
  COUNT(*) AS RowCount,
  MIN(Date) AS StartDate,
  MAX(Date) AS EndDate
FROM fact_prices
GROUP BY Ticker
ORDER BY Ticker;

----------------------------------------------------------------------
-- Q2) Latest available close per ticker
----------------------------------------------------------------------
WITH max_date AS (
  SELECT Ticker, MAX(Date) AS MaxDate
  FROM fact_prices
  GROUP BY Ticker
)
SELECT f.Ticker, f.Date, f.Close
FROM fact_prices f
JOIN max_date m
  ON f.Ticker = m.Ticker AND f.Date = m.MaxDate
ORDER BY f.Ticker;

----------------------------------------------------------------------
-- Q3) Daily returns per ticker (window function)
-- DailyReturn = (Close / PrevClose) - 1
----------------------------------------------------------------------
WITH r AS (
  SELECT
    Date,
    Ticker,
    Close,
    LAG(Close) OVER (PARTITION BY Ticker ORDER BY Date) AS PrevClose
  FROM fact_prices
)
SELECT
  Date,
  Ticker,
  Close,
  PrevClose,
  CASE
    WHEN PrevClose IS NULL OR PrevClose = 0 THEN NULL
    ELSE (Close / PrevClose) - 1
  END AS DailyReturn
FROM r
ORDER BY Ticker, Date;

----------------------------------------------------------------------
-- Q4) Average daily return and volatility by ticker
-- Volatility = sqrt( E[r^2] - (E[r])^2 )
----------------------------------------------------------------------
WITH returns AS (
  SELECT
    Date,
    Ticker,
    CASE
      WHEN LAG(Close) OVER (PARTITION BY Ticker ORDER BY Date) IS NULL
        OR LAG(Close) OVER (PARTITION BY Ticker ORDER BY Date) = 0
      THEN NULL
      ELSE (Close / LAG(Close) OVER (PARTITION BY Ticker ORDER BY Date)) - 1
    END AS r
  FROM fact_prices
),
stats AS (
  SELECT
    Ticker,
    COUNT(r) AS Observations,
    AVG(r) AS AvgDailyReturn,
    AVG(r * r) AS AvgSqReturn
  FROM returns
  WHERE r IS NOT NULL
  GROUP BY Ticker
)
SELECT
  Ticker,
  Observations,
  AvgDailyReturn,
  (AvgSqReturn - (AvgDailyReturn * AvgDailyReturn)) AS Variance,
  SQRT(AvgSqReturn - (AvgDailyReturn * AvgDailyReturn)) AS Volatility
FROM stats
ORDER BY Volatility DESC;

----------------------------------------------------------------------
-- Q5) 20-day moving average of Close per ticker
----------------------------------------------------------------------
SELECT
  Date,
  Ticker,
  Close,
  AVG(Close) OVER (
    PARTITION BY Ticker
    ORDER BY Date
    ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
  ) AS MA20
FROM fact_prices
ORDER BY Ticker, Date;
