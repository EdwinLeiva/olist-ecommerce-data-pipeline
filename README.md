# Olist E-commerce Data Pipeline

An end-to-end data engineering project that transforms Brazilian e-commerce data into analysis-ready datasets using Python, Pandas, and Neon PostgreSQL.

## Overview

This project implements an ETL pipeline to extract, transform, validate, and load data from the Olist Brazilian E-commerce dataset into a cloud-hosted PostgreSQL database.

The current pipeline processes four datasets:

| Dataset | Records |
|---|---:|
| Orders | 99,441 |
| Order Items | 112,650 |
| Products | 32,951 |
| Customers | 99,441 |
| **Total** | **344,483** |

## Architecture

```text
Olist CSV Files
      |
      v
Python + Pandas
      |
      v
Extract & Transform
      |
      v
Data Validation
      |
      v
Processed CSV Files
      |
      v
Neon PostgreSQL
      |
      v
SQL Business Analysis
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | ETL development |
| Pandas | Data transformation |
| PostgreSQL | Relational database |
| Neon | Cloud database hosting |
| SQLAlchemy | Database connectivity |
| Psycopg | PostgreSQL driver |
| python-dotenv | Environment configuration |
| Pytest | Automated testing |
| Git & GitHub | Version control |

## Project Structure

```text
olist-ecommerce-data-pipeline/
├── data/
│   ├── raw/
│   └── processed/
├── logs/
├── sql/
├── src/
│   ├── logger.py
│   ├── pipeline.py
│   ├── transform_orders.py
│   ├── transform_order_items.py
│   ├── transform_products.py
│   ├── transform_customers.py
│   ├── load_orders.py
│   ├── load_order_items.py
│   ├── load_products.py
│   └── load_customers.py
├── tests/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## ETL Pipeline

The pipeline performs five stages:

1. **Extract:** Reads the original orders, order items, products, and customers CSV files.
2. **Transform:** Cleans records, converts data types, and handles duplicates and missing values.
3. **Save:** Generates processed CSV files.
4. **Load:** Uses PostgreSQL UPSERT operations to insert new records and update existing ones.
5. **Verify:** Checks database record counts after loading.

The UPSERT implementation makes database loading idempotent and preserves existing primary keys. Extraction and transformation currently process the complete CSV datasets.

Run the pipeline:

```bash
python -m src.pipeline
```

## Database and Logging

The project uses Neon PostgreSQL with SQLAlchemy and Psycopg.

Database credentials are managed through environment variables and excluded from version control.

The logging system records pipeline execution events, warnings, and errors in the console and `logs/pipeline.log`.

## Data Quality

Key validation results:

- 99,441 orders processed.
- 112,650 order items processed.
- 32,951 products processed.
- 99,441 customers processed.
- 775 orders have no associated items.
- No order items reference nonexistent orders.
- 2,965 orders have missing customer delivery timestamps.
- Customer ZIP code prefixes are preserved as strings to retain leading zeros.

## SQL Business Analysis

The `sql/` directory contains nine queries covering:

- Database inspection and data validation.
- Monthly and overall sales performance.
- Product price distribution and outlier detection.
- Sales by product category.
- Category revenue and Pareto analysis.
- Seller performance.

Selected findings:

| Business Metric | Result |
|---|---:|
| Delivered orders | 96,478 |
| Delivered items | 110,197 |
| Product sales | $13,221,498.11 |
| Average order value | $137.04 |

*Product sales and average order value exclude freight charges.*

## Automated Testing

The project uses Pytest to validate data transformations, quality rules, and pipeline execution.

Current test results: **17 passed, 0 failed.**

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

### 5. Add the dataset

Place the original Olist CSV files in `data/raw/`.

### 6. Run the pipeline

```bash
python -m src.pipeline
```

### 7. Run automated tests

```bash
python -m pytest -v
```

**Security:** Never commit `.env` files or database credentials.

## Project Status

**Completed**

- Project setup and GitHub integration.
- Data inspection and validation.
- ETL transformations for four datasets.
- Neon PostgreSQL integration.
- Idempotent UPSERT database loading.
- Logging and pipeline error handling.
- SQL business analysis.
- Automated tests (17 passing).

**Next Development Goals**

- Extend the pipeline to additional Olist datasets.
- Improve database schema design and data modeling.
- Implement automated testing with GitHub Actions.

## Author

**Edwin Leiva**