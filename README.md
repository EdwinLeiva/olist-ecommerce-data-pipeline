# Olist E-commerce Data Pipeline

An end-to-end data engineering project built with Python, Pandas, and Neon PostgreSQL using the Olist Brazilian E-commerce dataset.

## Overview

This project implements a reproducible ETL pipeline to extract, transform, validate, and load e-commerce data into a cloud-hosted PostgreSQL database.

The current pipeline processes three datasets:

- `orders`: 99,441 records.
- `order_items`: 112,650 records.
- `products`: 32,951 records.

A total of **245,042 records** are processed and loaded into Neon PostgreSQL.

The project includes data quality checks, automated testing, database integration, and SQL-based business analysis.

## Architecture

```text
             Olist Raw CSV Files
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
              +-------+-------+
              |               |
              v               v
        Processed CSV    Neon PostgreSQL
                              |
                              v
                         SQL Analytics
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | ETL development |
| Pandas | Data extraction and transformation |
| PostgreSQL | Relational database |
| Neon | Cloud database hosting |
| SQLAlchemy | Database connectivity |
| Psycopg | PostgreSQL driver |
| python-dotenv | Environment configuration |
| Pytest | Automated testing |
| Git and GitHub | Version control |

## Data Source

The project uses the Olist Brazilian E-commerce dataset, which contains nine CSV files covering orders, customers, products, sellers, payments, reviews, geolocation, and related information.

Raw datasets are stored locally in `data/raw/` and excluded from Git.

The current ETL implementation processes:

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
|
├── src/
│   ├── analyze_orders.py
│   ├── inspect_data.py
│   ├── validate_orders.py
│   ├── transform_orders.py
│   ├── transform_order_items.py
│   ├── transform_products.py
│   ├── load_orders.py
│   ├── load_order_items.py
│   ├── load_products.py
│   ├── pipeline.py
│   └── test_connection.py
|
├── tests/
│   ├── test_orders_integration.py
│   ├── test_pipeline.py
│   ├── test_transform_orders.py
│   ├── test_transform_order_items.py
│   ├── test_transform_products.py
│   └── test_validate_orders.py
|
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## ETL Pipeline

The main orchestration module is `src/pipeline.py`.

It executes the following stages:

1. **Extract:** Reads the original `orders`, `order_items`, and `products` CSV files.
2. **Transform:** Converts date and numeric columns, removes records with invalid identifiers, and handles duplicate records.
3. **Save:** Generates processed CSV files in `data/processed/`.
4. **Load:** Loads all three datasets into Neon PostgreSQL.
5. **Verify:** Compares expected and actual database row counts for each table.

### Run the pipeline

```bash
python -m src.pipeline
```

### Processed output

| File | Database table |
|---|---|
| `orders_processed.csv` | `orders` |
| `order_items_processed.csv` | `order_items` |
| `products_processed.csv` | `products` |

**Important:** Each execution performs a full refresh of the corresponding database tables using `if_exists="replace"`. This replaces the contents of these three tables rather than performing incremental updates.

## Data Quality and Validation

The transformation and validation modules check missing identifiers, duplicate records, date conversions, numeric data types, and timestamp inconsistencies.

### Orders and Order Items

The data quality assessment produced the following results:

| Metric | Result |
|---|---:|
| Total orders | 99,441 |
| Orders with associated items | 98,666 |
| Orders without associated items | 775 |
| Items associated with nonexistent orders | 0 |
| Orders with items coverage | 99.22% |

Additional findings:

- 603 orders with status `unavailable` have no associated items.
- All 603 have an approval timestamp.
- None have shipping or customer delivery timestamps.
- These records were preserved rather than deleted or modified.

The relationship between orders and order items has no orphan order references, although orders without associated items remain an area for further investigation.

### Products

The products transformation produced the following results:

| Metric | Result |
|---|---:|
| Original product records | 32,951 |
| Transformed product records | 32,951 |
| Records removed | 0 |
| Missing product IDs after transformation | 0 |

Product dimensions, weight, name length, description length, and photo quantity are converted to numeric types.

Missing product metadata is preserved as null rather than being replaced with arbitrary values.

## Database Integration

The project uses Neon PostgreSQL with SQLAlchemy and Psycopg.

Database credentials are managed through environment variables using `python-dotenv`.

Each dataset is loaded independently and verified using database-level row counts.

### Latest successful ETL execution

| Dataset | Extracted | Transformed | Loaded |
|---|---:|---:|---:|
| Orders | 99,441 | 99,441 | 99,441 |
| Order Items | 112,650 | 112,650 | 112,650 |
| Products | 32,951 | 32,951 | 32,951 |
| **Total** | **245,042** | **245,042** | **245,042** |

The pipeline also reported 2,965 missing customer delivery timestamps in the orders dataset.

## SQL Analysis

Initial SQL analysis has been performed using the loaded orders and order items tables.

Current analytical findings include:

- 96,478 delivered orders.
- 110,197 delivered order items.
- $13,221,498.11 in delivered product sales, excluding freight.
- $137.04 average order value, excluding freight.
- $119.98 average item price.

Price distribution analysis also identified high-value statistical outliers. These records were retained because statistical outliers do not necessarily represent data quality errors.

Further analysis will incorporate product categories to identify revenue and sales performance by category.

## Automated Testing

The project uses Pytest to validate transformations, data quality rules, and pipeline execution.

The test suite covers:

- Date conversion.
- Numeric column conversion.
- Duplicate identifier removal.
- Preservation of valid records and missing delivery dates.
- Product transformation and missing metadata handling.
- Integration with the original orders dataset.
- Required column validation.
- Integrated pipeline execution using isolated sample data without connecting to the production database.

**Latest test results: 13 passed, 0 failed.**

Run the tests with:

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

Replace the placeholders with your actual database credentials.

**Security:** Never commit `.env` files, passwords, or database credentials to GitHub.

### 5. Add the dataset

Download the Olist Brazilian E-commerce dataset and place the original CSV files in:

```text
data/raw/
```

### 6. Run the ETL pipeline

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
- Olist dataset inspection.
- Orders, order items, and products transformation modules.
- Data quality validation.
- Automated test suite.
- Neon PostgreSQL integration.
- Loading and verification of all three database tables.
- Integrated ETL pipeline.
- Processed CSV generation.
- Initial SQL analysis and referential integrity assessment.

### Next Development Goals

- Develop analytical SQL queries and business performance metrics by product category.
- Implement incremental data loading.
- Improve logging and error handling.
- Extend the pipeline to additional Olist datasets.
- Improve database schema design and data modeling.
- Implement automated testing with GitHub Actions.

## Author

**Edwin Leiva**