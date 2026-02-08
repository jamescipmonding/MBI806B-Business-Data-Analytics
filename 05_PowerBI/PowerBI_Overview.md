# Power BI Dashboard Overview

## Purpose
The Power BI dashboard was created to visualise historical stock price data
and support exploratory analysis and business-focused insights.

The dashboard enables users to quickly assess price trends, volatility,
and comparative performance across different stock tickers.

---

## Key Visuals Included
The dashboard includes the following key visual components:

- Time-series line charts showing historical closing prices
- Summary metrics for price movement and volume
- Comparative views across multiple stock tickers
- Interactive filters to enable focused analysis

---

## Analytical Focus
The Power BI visuals were designed to support:

- Identification of long-term price trends
- Comparison of performance between different stocks
- Detection of periods of higher volatility
- High-level insights suitable for non-technical stakeholders

---

## Notes
Due to file size limitations, the Power BI (.pbix) file is not included
directly in this repository. Screenshots of key dashboard views are provided
to demonstrate analytical outputs and design intent.
---

## Dashboard Pages and What They Show

> Screenshots are stored in this folder as evidence of dashboard design and analytical outputs.

### 1) Market Overview (`dashboard_01_market_overview.png`)
Provides a high-level comparison of stock performance and volatility across
multiple tickers.

Key views:
- Stock closing prices over time (multi-ticker comparison)
- **20-day volatility (%)** by stock
- Short-term trend view using **5-day and 20-day moving averages**
- Summary cards showing latest price, average daily return, and latest trading date

---

### 2) Risk & Return (`dashboard_02_risk_return.png`)
Summarises performance using a portfolio-style risk–return framework.

Key views:
- Scatter plot of **Average Daily Return vs 20-Day Volatility**
- Risk-adjusted return comparison by stock
- Cumulative return by year
- Volatility trends by year and ticker

---

### 3) Momentum & Trend-Based Decision Analysis (`dashboard_03_momentum_trend.png`)
Highlights short-term momentum and longer-term trend direction using moving
average signals.

Key indicators:
- Close price vs **MA_20** and **MA_60**
- Trend direction label (e.g., *Bullish* / *Bearish*)
- Trend strength vs MA_60 (% difference)
- Short-term momentum vs MA_20 (% difference)
- Decision support label (e.g., *Caution*)

---

### 4) Indicative Stock Valuation Overview (`dashboard_04_indicative_valuation.png`)
Provides a valuation-focused snapshot showing whether a stock is trading near
its **indicative fair value**.

Key indicators shown:
- **Latest Stock Price**
- **Indicative Fair Value (MA_60)**
- **Indicative Valuation Index (IVI = Price ÷ MA_60)**
- **Valuation Premium/Discount (%)**
- Valuation remark (e.g., *Fairly Valued*, *Overvalued*, *Undervalued*)
