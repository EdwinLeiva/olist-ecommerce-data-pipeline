# Olist E-commerce Data Pipeline

## Overview

This project is an end-to-end data engineering pipeline built using the Olist Brazilian E-commerce dataset.

The pipeline extracts raw e-commerce data from CSV files, applies data transformations and quality checks using Python and Pandas, saves the processed dataset locally, and loads the resulting data into a cloud-hosted PostgreSQL database using Neon.

The main objective is to develop a reproducible and maintainable ETL workflow while applying fundamental data engineering practices, including data validation, automated testing, database integration, and SQL analytics.

## Architecture

The project currently follows this ETL workflow:

```text
Olist Raw CSV Dataset
         |
         v
     Extraction
         |
         v
 Python + Pandas
   Transformation
         |
         v
   Processed Data
         |
         +-------------------+
         |                   |
         v                   v
   Processed CSV      PostgreSQL (Neon)
                         |
                         v
                    SQL Analytics
```

## Objectives

- Explore and understand real-world e-commerce datasets.
- Identify missing values, duplicate records, and data quality issues.
- Build reusable extraction and transformation modules.
- Implement a repeatable ETL pipeline.
- Load processed data into a cloud PostgreSQL database.
- Validate transformations using automated tests.
- Develop SQL queries to analyze orders and e-commerce performance.
- Apply version control and software development best practices.

## Technology Stack

- **Python 3.13** – Pipeline development.
- **Pandas** – Data manipulation and transformation.
- **PostgreSQL** – Relational database.
- **Neon** – Cloud-hosted PostgreSQL database.
- **SQLAlchemy** – Database connectivity and interaction.
- **Psycopg** – PostgreSQL database driver.
- **python-dotenv** – Environment variable management.
- **Pytest** – Automated testing.
- **Git and GitHub** – Version control and project hosting.

## Data Source

The project uses the Olist Brazilian E-commerce dataset, which contains information about:

- Customers
- Orders
- Order items
- Payments
- Reviews
- Products
- Sellers
- Geolocation
- Product category translations

The raw CSV files are stored locally in `data/raw/` and excluded from Git version control to avoid uploading large datasets to the repository.

The current ETL pipeline focuses on the orders dataset, which contains 99,441 records.

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
│   ├── __init__.py
│   ├── analyze_orders.py
│   ├── inspect_data.py
│   ├── validate_orders.py
│   ├── transform_orders.py
│   ├── load_orders.py
│   ├── pipeline.py
│   └── test_connection.py
|
├── tests/
│   ├── test_orders_integration.py
│   ├── test_pipeline.py
│   ├── test_transform_orders.py
│   └── test_validate_orders.py
|
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Work Completed

### 1. Project Setup

- Initialized the Git repository and connected it to GitHub.
- Created and activated a Python virtual environment.
- Installed the project dependencies.
- Configured `.gitignore` to exclude the virtual environment, environment variables, cache files, and local datasets.
- Added `.env.example` as a template for database configuration.

### 2. Dataset Inspection

- Downloaded and extracted the Olist dataset.
- Inspected the columns and missing values in all nine CSV files.
- Stored the raw CSV files locally without adding them to Git.

### 3. Orders Analysis

The orders dataset contains **99,441 records**.

Initial analysis identified:

- No duplicate `order_id` values.
- Missing timestamps in several date columns.
- Orders in different lifecycle states, including delivered, shipped, canceled, and unavailable.
- Eight orders marked as delivered without a customer delivery timestamp.
- Records where the carrier delivery timestamp precedes the purchase timestamp.
- Delivered orders whose actual delivery occurred after the estimated date.

These findings are retained for further investigation. Missing dates and potentially inconsistent timestamps are not automatically treated as grounds for deleting records.

### 4. Data Validation

The validation module checks for:

- Missing order identifiers.
- Duplicate order identifiers.
- Missing or unparseable dates.
- Approval timestamps preceding purchase timestamps.
- Carrier delivery timestamps preceding purchase timestamps.
- Customer delivery timestamps preceding purchase timestamps.
- Deliveries occurring after their estimated dates.

Initial validation identified:

- 166 records where the carrier delivery timestamp precedes the purchase timestamp.
- 7,827 delivered orders with delivery timestamps later than their estimated delivery dates.

These observations require careful interpretation before defining corrective rules.

### 5. Orders Transformation

The module `src/transform_orders.py` currently:

- Loads the original orders CSV.
- Creates a copy of the input DataFrame before transforming it.
- Converts five order-related timestamp columns to Pandas datetime values.
- Removes rows with missing order IDs.
- Removes duplicate order IDs, keeping the first occurrence.
- Preserves missing delivery timestamps.

The transformation processes all 99,441 records without modifying the original CSV.

### 6. Automated Testing

Automated tests have been implemented using Pytest.

The test suite validates:

- Conversion of timestamp columns to Pandas datetime values.
- Removal of duplicate order identifiers.
- Preservation of orders with missing customer delivery timestamps.
- Integration with the real Olist orders dataset.
- Required column validation.
- Pipeline execution using isolated sample data.

**Latest test results: 6 passed, 0 failed.**

### 7. PostgreSQL and Neon Integration

The project is connected to a cloud-hosted PostgreSQL database using Neon.

The implementation includes:

- Database connection through SQLAlchemy.
- PostgreSQL connectivity using Psycopg.
- Secure configuration through environment variables.
- A standalone database connection test.
- A reusable data loading module in `src/load_orders.py`.

The processed orders are loaded into a PostgreSQL table named `orders`.

The loading process uses Pandas `to_sql()` with batch insertion (`chunksize=5000`) and replaces the existing table during each full refresh.

A database-level verification query checks the actual number of records stored in PostgreSQL:

```sql
SELECT COUNT(*) AS total_orders
FROM orders;
```

The initial full load was successfully verified:

| Metric | Result |
|---|---:|
| Expected records | 99,441 |
| Records in PostgreSQL | 99,441 |
| Unique order IDs | 99,441 |
| Missing customer delivery dates | 2,965 |

### 8. End-to-End ETL Pipeline

The main orchestration module is `src/pipeline.py`.

It executes the following steps:

1. **Extract:** Reads the original orders CSV.
2. **Transform:** Applies the data transformation rules.
3. **Save:** Exports the processed dataset to `data/processed/orders_processed.csv`.
4. **Load:** Loads the transformed records into Neon PostgreSQL.
5. **Verify:** Executes a database query to confirm the number of stored records.
6. **Summary:** Reports the main execution metrics.

The complete pipeline can be executed with a single command:

```bash
python -m src.pipeline
```

The latest successful execution processed and verified all 99,441 orders in PostgreSQL.

## Installation and Configuration

### 1. Clone the repository

```bash
git clone https://github.com/EdwinLeiva/olist-ecommerce-data-pipeline.git

cd olist-ecommerce-data-pipeline
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and configure the Neon PostgreSQL connection string:

```dotenv
DATABASE_URL="postgresql+psycopg://USER:PASSWORD@HOST/DATABASE?sslmode=require"
```

Replace the placeholders with the connection details provided by Neon.

**Important:** Never commit `.env` files, passwords, or database credentials to GitHub.

### 5. Add the Olist dataset

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

## Current Status

**Completed:**

- Dataset exploration and inspection.
- Orders analysis and data quality validation.
- Reusable orders transformation module.
- Automated unit and integration tests.
- Neon PostgreSQL database connection.
- Orders table creation and initial full data load.
- End-to-end ETL pipeline.
- Database-level row count verification.

**Next Development Goals:**

- Implement incremental data loading instead of replacing the entire table.
- Improve pipeline logging and error handling.
- Develop analytical SQL queries and business performance metrics.
- Extend the pipeline to additional Olist datasets.
- Implement automated testing with GitHub Actions.
- Improve database schema design and data modeling.

## Data Quality and Referential Integrity

### Orders and Order Items Validation

As part of the data quality assessment, the `orders` and `order_items` tables were analyzed to verify their consistency and relationship.

**Validation results:**

| Validation | Result |
|---|---:|
| Total orders | 99,441 |
| Orders with associated items | 98,666 |
| Orders without associated items | 775 |
| Orders with items but no matching order | 0 |
| Orders with items coverage | 99.22% |

### Key Findings

- 98,666 orders (99.22%) have at least one associated item in the `order_items` table.
- 775 orders (0.78%) do not have associated records in `order_items`.
- No orphan records were found: every `order_id` in `order_items` matches an existing order in `orders`.
- Among the 775 orders without items, 603 have the status `unavailable`. All 603 have an approval timestamp, but none have shipping or delivery timestamps.

### Conclusion

The relationship between `orders` and `order_items` is consistent from the perspective of orphan records. However, the 775 orders without associated items represent an exception worth investigating.

These records were preserved in the dataset rather than deleted or modified, since they may provide useful information about canceled, unavailable, or otherwise unfulfilled orders.

## Author

**Edwin Leiva**