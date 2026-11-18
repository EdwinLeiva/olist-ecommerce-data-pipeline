# Olist E-commerce Data Pipeline

An end-to-end data engineering project that processes Brazilian e-commerce data using Python, Pandas, and Neon PostgreSQL.

## Overview

This project implements an ETL pipeline to extract, transform, validate, and load data from the Olist Brazilian E-commerce dataset into a cloud-hosted PostgreSQL database.

The pipeline currently processes five datasets:

| Dataset | Records |
|---|---:|
| Customers | 99,441 |
| Product Categories | 73 |
| Products | 32,951 |
| Orders | 99,441 |
| Order Items | 112,650 |
| **Total** | **344,556** |

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
| GitHub Actions | Continuous integration |

## Project Structure

```text
olist-ecommerce-data-pipeline/
├── data/
│   ├── raw/
│   └── processed/
├── logs/
├── sql/
│   ├── 01_database_inspection.sql
│   ├── ...
│   └── 10_schema_documentation.md
├── src/
│   ├── pipeline.py
│   ├── logger.py
│   ├── check_connection.py
│   ├── transform_*.py
│   └── load_*.py
├── tests/
├── .github/
│   └── workflows/
│       └── python-tests.yml
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## ETL Pipeline

The pipeline executes five stages:

1. **Extract:** Reads the source CSV datasets.
2. **Transform:** Cleans records, converts data types, and handles duplicates and missing values.
3. **Save:** Generates processed CSV files.
4. **Load:** Uses PostgreSQL UPSERT operations to insert new records and update existing ones.
5. **Verify:** Checks database record counts after loading.

Database loading is idempotent. Extraction and transformation currently process the complete CSV datasets rather than incremental changes.

Run the pipeline:

```bash
python -m src.pipeline
```

## Database Design

The project uses Neon PostgreSQL and includes five relational tables:

- `customers`
- `product_categories`
- `products`
- `orders`
- `order_items`

The database schema includes primary keys, foreign keys, check constraints, and indexes to support referential integrity and query performance.

Detailed schema documentation is available in `sql/10_schema_documentation.md`.

## Data Quality

Key validation results:

- 99,441 customers processed.
- 99,441 orders processed.
- 112,650 order items processed.
- 32,951 products processed.
- 73 product categories registered.
- No order items reference nonexistent orders.
- 2,965 orders have missing customer delivery timestamps, consistent with incomplete delivery information in the source dataset.
- ZIP code prefixes are preserved as strings to retain leading zeros.

## SQL Business Analysis

The `sql/` directory contains nine SQL analysis scripts covering:

- Database inspection and data validation.
- Monthly and overall sales performance.
- Product price distribution and outlier detection.
- Sales by product category.
- Category revenue and Pareto analysis.
- Seller performance.

Selected business metrics:

| Metric | Result |
|---|---:|
| Delivered orders | 96,478 |
| Delivered items | 110,197 |
| Product sales | $13,221,498.11 |
| Average order value | $137.04 |

*Product sales and average order value exclude freight charges.*

## Automated Testing

Pytest validates data transformations, data quality rules, and pipeline execution.

**Current results: 17 tests passed.**

Run tests locally:

```bash
python -m pytest -v
```

GitHub Actions automatically runs the test suite on pushes and pull requests targeting `main`.

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

Copy `.env.example` to `.env` and configure your Neon PostgreSQL connection:

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

- ETL pipeline implementation.
- Integration of five Olist datasets.
- Neon PostgreSQL integration.
- Idempotent UPSERT database loading.
- Logging and error handling.
- Relational database design and documentation.
- SQL business analysis.
- Automated testing with 17 passing tests.
- GitHub Actions CI workflow.

**Next Development Goal**

- Implement workflow orchestration with Apache Airflow.

## Author

**Edwin Leiva**