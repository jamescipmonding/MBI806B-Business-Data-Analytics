# MBI806B – Business Data Analytics Project

## Project Overview
This project was completed as part of **MBI806B – Business Data Analytics** at Yoobee Colleges.
It demonstrates an end-to-end data analytics workflow, from raw data ingestion and cleaning
through to structured storage, analysis, and insight generation.

The project focuses on historical stock price data and applies data engineering,
SQL analytics, and business intelligence techniques to support analytical decision-making.

---

## Objectives
- Design a structured data pipeline for raw time-series data
- Apply ETL processes to clean and validate datasets
- Store analytical data in a relational data warehouse
- Perform SQL-based analysis on structured data
- Present insights using business intelligence principles

---

## Data Overview
- **Source:** Yahoo Finance (CSV exports)
- **Data Type:** Historical daily stock prices
- **Granularity:** Daily, per stock ticker
- **Core Fields:** Date, Open, High, Low, Close, Volume

Detailed data assumptions and preparation steps are documented in:
02_Data/Data_Notes.md

---

## Technical Architecture
The project follows a layered analytics architecture:

Raw CSV Files  
↓  
Python ETL (Cleaning & Validation)  
↓  
SQLite Data Warehouse (fact_prices)  
↓  
SQL Analysis  
↓  
Power BI Visualisation & Insights  

---

## Tools & Technologies
- **Python** – ETL pipeline (pandas, sqlite3)
- **SQLite** – Data warehouse storage
- **SQL** – Schema design and analytical queries
- **Power BI** – Data visualisation and dashboarding
- **GitHub** – Version control and project documentation

---

## Repository Structure
01_Project_Overview/        Project context and scope  
02_Data/                    Data notes and assumptions  
03_SQL/                     SQL schema and queries  
04_Python/                  Python ETL pipeline  
05_PowerBI/                 Dashboard screenshots and notes  
06_Insights_and_Findings/   Analytical insights and conclusions  

---

## Key Outputs
- Automated Python ETL script for structured data loading
- Relational fact table with enforced data integrity
- SQL queries supporting analytical exploration
- Business-focused insights derived from historical price trends

---

## Learning Outcomes
This project demonstrates:
- Practical data engineering and ETL design
- Understanding of data warehousing concepts
- Ability to translate raw data into structured insights
- Clear documentation and analytical communication

---

## Disclaimer
This project was completed for **educational purposes only**.
The analysis is not intended for live trading or investment decision-making.

## Project Summary
This project demonstrates an end-to-end business analytics workflow,
from data preparation and transformation to visual analysis and
business-oriented interpretation.

