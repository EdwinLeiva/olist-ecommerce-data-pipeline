# Olist E-commerce Data Pipeline

An end-to-end data engineering project that transforms Brazilian e-commerce data using Python, Pandas, Prefect, and Neon PostgreSQL.

## Overview

This project implements an ETL pipeline to extract, transform, validate, and load data from the Olist Brazilian E-commerce dataset into a cloud-hosted PostgreSQL database.

The pipeline processes five datasets:

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

Prefect orchestrates and monitors the ETL flow.
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | ETL development |
| Pandas | Data processing |
| PostgreSQL | Relational database |
| Neon | Cloud database hosting |
| SQLAlchemy & Psycopg | Database connectivity |
| Prefect 3 | Workflow orchestration |
| Prefect Cloud | Flow monitoring |
| Pytest | Automated testing |
| GitHub Actions | Continuous integration |

## Key Features

- **ETL pipeline:** Extracts, transforms, validates, and loads five datasets.
- **Idempotent loading:** Uses PostgreSQL UPSERT operations to insert and update records safely.
- **Data modeling:** Relational schema with primary keys, foreign keys, constraints, and indexes.
- **Error handling:** Handles pipeline failures and database resource cleanup.
- **Orchestration:** Uses Prefect to organize and monitor pipeline executions.
- **SQL analysis:** Includes nine scripts for data exploration and business analysis.
- **Automated testing:** 17 tests covering transformations and data quality.
- **CI/CD:** GitHub Actions automatically runs tests on pushes and pull requests to `main`.

**Note:** Database loading is idempotent, but extraction and transformation currently process the complete CSV datasets rather than incremental changes.

## Database Design

The PostgreSQL database contains five relational tables:

- `customers`
- `product_categories`
- `products`
- `orders`
- `order_items`

Detailed schema documentation is available in `sql/10_schema_documentation.md`.

## Data Quality

Key validation results:

- 99,441 customers processed.
- 99,441 orders processed.
- 112,650 order items processed.
- 32,951 products processed.
- 73 product categories registered.
- ZIP code prefixes preserved as strings.
- 2,965 orders have missing customer delivery timestamps, consistent with incomplete delivery information in the source dataset.

## SQL Business Analysis

The `sql/` directory contains nine analysis scripts covering:

- Sales performance and monthly trends.
- Product prices and outlier detection.
- Sales by product category.
- Revenue distribution and Pareto analysis.
- Seller performance.
- Database inspection and data validation.

Selected business metrics:

| Metric | Result |
|---|---:|
| Delivered orders | 96,478 |
| Delivered items | 110,197 |
| Product sales | $13,221,498.11 |
| Average order value | $137.04 |

*Product sales and average order value exclude freight charges.*

## Project Structure

```text
olist-ecommerce-data-pipeline/
├── data/
│   ├── raw/
│   └── processed/
├── logs/
├── sql/
├── src/
│   ├── pipeline.py
│   ├── logger.py
│   ├── transform_*.py
│   └── load_*.py
├── tests/
├── .github/workflows/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Installation and Usage

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

The pipeline can also be monitored through the configured Prefect Cloud workspace.

**Security:** Never commit `.env` files or database credentials.

## Project Status

**Implemented:**
- ETL pipeline and integration of five datasets.
- Neon PostgreSQL integration.
- Idempotent database loading.
- Logging and error handling.
- Relational database design.
- SQL business analysis.
- Automated testing and GitHub Actions.
- Prefect flow orchestration and Prefect Cloud monitoring.

**Next development goals:**
- Configure Prefect deployments and workers.
- Explore scheduled and automated pipeline execution.
- Learn Apache Airflow.

## Author

**Edwin Leiva**