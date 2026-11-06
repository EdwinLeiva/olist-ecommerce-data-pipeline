# Olist E-commerce Data Pipeline

An end-to-end data engineering project that transforms Brazilian e-commerce data into structured, analysis-ready datasets using Python, Pandas, and Neon PostgreSQL.

## Overview

This project implements an ETL pipeline to extract, transform, validate, and load data from the Olist Brazilian E-commerce dataset into a cloud-hosted PostgreSQL database.

The current pipeline processes three datasets:

| Dataset | Records |
|---|---:|
| Orders | 99,441 |
| Order Items | 112,650 |
| Products | 32,951 |
| **Total** | **245,042** |

The project also includes data quality checks, automated tests, and SQL queries to analyze business performance.

## Architecture

```text
Olist CSV Files
      |
      v
Python + Pandas
      |
      v
Extract and Transform
      |
      v
Data Validation
      |
      +----------------+
      |                |
      v                v
Processed CSV    Neon PostgreSQL
                       |
                       v
                  SQL Analysis
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | ETL development |
| Pandas | Data processing |
| PostgreSQL | Relational database |
| Neon | Cloud database hosting |
| SQLAlchemy | Database connectivity |
| Psycopg | PostgreSQL driver |
| python-dotenv | Environment configuration |
| Pytest | Automated testing |
| Git and GitHub | Version control |

## Data Source

The project uses the Olist Brazilian E-commerce dataset, which contains nine CSV files covering orders, customers, products, sellers, payments, reviews, and other e-commerce information.

Raw files are stored locally in `data/raw/` and excluded from Git.

The current pipeline processes:

- `orders`
- `order_items`
- `products`

## Project Structure

```text
olist-ecommerce-data-pipeline/
|
├── data/
│   ├── raw/
│   └── processed/
|
├── sql/
│   ├── 01_database_inspection.sql
│   ├── 02_monthly_sales.sql
│   ├── 03_global_sales_metrics.sql
│   ├── 04_product_price_distribution.sql
│   ├── 05_product_price_outliers.sql
│   ├── 06_sales_by_category.sql
│   ├── 07_category_sales_percentage.sql
│   ├── 08_category_pareto_analysis.sql
│   └── 09_top_sellers.sql
|
├── src/
│   ├── transform_orders.py
│   ├── transform_order_items.py
│   ├── transform_products.py
│   ├── load_orders.py
│   ├── load_order_items.py
│   ├── load_products.py
│   └── pipeline.py
|
├── tests/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## ETL Pipeline

The main orchestration module is `src/pipeline.py`.

It performs five stages:

1. **Extract:** Reads the original orders, order items, and products CSV files.
2. **Transform:** Converts data types, removes invalid identifiers, and handles duplicate records.
3. **Save:** Generates processed CSV files in `data/processed/`.
4. **Load:** Loads the transformed datasets into Neon PostgreSQL.
5. **Verify:** Compares database row counts with the expected records.

Run the pipeline:

```bash
python -m src.pipeline
```

Each execution performs a full refresh of the three database tables. Existing table contents are replaced rather than incrementally updated.

## Data Quality and Validation

The pipeline applies checks for missing identifiers, duplicate records, data types, and date conversions.

Key findings:

- All 99,441 orders and 112,650 order items were processed.
- 98,666 orders have associated items.
- 775 orders have no associated items.
- No order items reference nonexistent orders.
- 2,965 orders have missing customer delivery timestamps.
- All 32,951 product records were preserved.
- Missing product metadata is retained as null rather than replaced with arbitrary values.

These checks help preserve the original information while identifying records that may require further investigation.

## Database Integration

The project uses Neon PostgreSQL with SQLAlchemy and Psycopg.

Database credentials are configured through environment variables using `python-dotenv`. Sensitive credentials are kept outside version control.

### Latest successful ETL execution

| Dataset | Extracted | Transformed | Loaded |
|---|---:|---:|---:|
| Orders | 99,441 | 99,441 | 99,441 |
| Order Items | 112,650 | 112,650 | 112,650 |
| Products | 32,951 | 32,951 | 32,951 |
| **Total** | **245,042** | **245,042** | **245,042** |

All three database tables were successfully loaded and verified.

## SQL Business Analysis

The `sql/` directory contains nine queries for database inspection and business analysis.

The analysis covers monthly sales, overall performance, product price distribution, price outliers, category revenue, Pareto analysis, and seller performance.

### Key findings

**Overall sales performance**

| Metric | Result |
|---|---:|
| Delivered orders | 96,478 |
| Delivered items | 110,197 |
| Product sales | $13,221,498.11 |
| Average order value | $137.04 |
| Average item price | $119.98 |

*Product sales and average order value exclude freight charges.*

**Monthly performance**

- November 2017 recorded the highest monthly product sales, with $987,765.37.
- May 2018 followed closely with $977,544.69.
- Sales increased considerably throughout 2017 and remained strong during the first five months of 2018.

**Product categories**

The three leading categories by delivered product revenue were:

| Category | Product Sales |
|---|---:|
| Beauty & Health | $1,233,131.72 |
| Watches & Gifts | $1,166,176.98 |
| Bed, Bath & Table | $1,023,434.76 |

Together, these categories represented approximately 25.89% of delivered product sales.

The Pareto analysis showed that:

- 8 categories accounted for approximately 54.49% of revenue.
- 13 categories accounted for approximately 71.97%.
- 18 categories accounted for approximately 81.29%.

**Product price distribution**

| Metric | Result |
|---|---:|
| Average item price | $120.65 |
| Median item price | $74.99 |
| 25th percentile | $39.90 |
| 75th percentile | $134.90 |
| Upper outlier threshold | $277.40 |

The analysis identified 8,427 items above the statistical outlier threshold, representing 7.48% of all items and 35.61% of total product sales.

These records were retained because high prices do not necessarily indicate data quality problems.

**Seller performance**

The seller analysis identified differences between sales volume and revenue. For example, the highest-volume seller recorded 1,949 items, while the highest-revenue seller generated $226,987.93 from 1,148 items.

This demonstrates why seller performance should be evaluated using multiple business metrics.

## Automated Testing

The project uses Pytest to validate transformations, data quality rules, and pipeline execution.

The test suite covers:

- Date and numeric conversions.
- Duplicate identifier removal.
- Missing value handling.
- Product data transformations.
- Required column validation.
- Pipeline execution using sample data without connecting to the production database.

**Latest test results: 13 passed, 0 failed.**

Run the tests:

```bash
python -m pytest -v
```

## Installation and Configuration

### 1. Clone the repository

```bash
git clone https://github.com/EdwinLeiva/olist-ecommerce-data-pipeline.git

cd olist-ecommerce-data-pipeline
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and configure your Neon connection:

```dotenv
DATABASE_URL="postgresql+psycopg://USER:PASSWORD@HOST/DATABASE?sslmode=require"
```

Replace the placeholders with your database credentials.

**Security:** Never commit `.env` files, passwords, or database credentials to GitHub.

### 5. Add the dataset

Download the Olist Brazilian E-commerce dataset and place the original CSV files in:

```text
data/raw/
```

### 6. Run the pipeline

```bash
python -m src.pipeline
```

### 7. Run automated tests

```bash
python -m pytest -v
```

## Project Status

### Completed

- Project setup and GitHub integration.
- Dataset inspection and data quality validation.
- ETL transformations for orders, order items, and products.
- Neon PostgreSQL integration.
- Successful loading and verification of 245,042 records.
- Automated test suite with 13 passing tests.
- SQL analysis covering sales, categories, prices, and sellers.

### Next Development Goals

- Implement incremental data loading.
- Improve logging and error handling.
- Extend the pipeline to additional Olist datasets.
- Improve database schema design and data modeling.
- Implement automated testing with GitHub Actions.

## Author

**Edwin Leiva**