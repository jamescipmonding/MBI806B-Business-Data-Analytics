"""
01_ETL_Build_SQLite_FactPrices.py

Automates extraction, cleaning, and loading (ETL) of daily stock price data.
Reads multiple CSV files, infers ticker symbols, validates columns,
and loads cleaned data into a SQLite data warehouse table (fact_prices)
with primary keys and indexes for analytical querying.
"""
