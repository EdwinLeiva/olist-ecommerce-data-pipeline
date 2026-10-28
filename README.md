# Olist E-commerce Data Pipeline

## Overview

This project is a data engineering pipeline built using the Olist Brazilian E-commerce dataset. Its goal is to develop a reproducible workflow for inspecting, validating, and transforming e-commerce data, with plans to load the processed data into PostgreSQL and perform analytical queries.

## Objectives

- Explore and understand the source datasets.
- Identify missing values, duplicate records, and data quality issues.
- Build reusable data loading and transformation modules.
- Validate transformations using automated tests.
- Store structured data in PostgreSQL.
- Develop SQL queries to analyze orders and e-commerce performance.

## Technology Stack

- Python
- Pandas
- PostgreSQL
- SQLAlchemy
- Psycopg
- python-dotenv
- Pytest
- Git and GitHub

## Data Source

The project uses the Olist Brazilian E-commerce dataset, which contains information about customers, orders, order items, payments, reviews, products, sellers, geolocation, and product category translations.

The raw CSV files are stored locally in `data/raw/` and are excluded from Git version control to avoid uploading large datasets to the repository.

## Project Structure

```text
olist-ecommerce-data-pipeline/
├── data/
│   ├── raw/
│   └── processed/
├── sql/
├── src/
│   ├── __init__.py
│   ├── analyze_orders.py
│   ├── inspect_data.py
│   ├── transform_orders.py
│   └── validate_orders.py
├── tests/
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
- Inspected the columns and missing values in the nine CSV files.
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

The initial analysis found 166 records where the carrier delivery timestamp precedes the purchase timestamp, and 7,827 delivered orders with delivery timestamps later than their estimated dates. These observations require careful interpretation before defining corrective rules.

### 5. Orders Transformation

The module `src/transform_orders.py` currently:

- Loads the orders CSV.
- Creates a copy of the input DataFrame before transforming it.
- Converts the five order-related timestamp columns to Pandas datetime values.
- Removes rows with missing order IDs.
- Removes duplicate order IDs, keeping the first occurrence.
- Preserves missing delivery timestamps.

The initial execution processed 99,441 rows and returned 99,441 rows, with no duplicate order IDs. The original CSV remains unchanged.

## Planned Work

- Add automated tests for the transformation module.
- Refine data quality rules based on the initial findings.
- Build a repeatable ETL workflow.
- Load transformed data into PostgreSQL.
- Create SQL analytics queries.
- Add automated testing to GitHub Actions.

## Configuration

Copy `.env.example` to `.env` and configure `DATABASE_URL` with your PostgreSQL connection details when database integration is implemented.

Do not commit `.env` files, passwords, or other credentials.

## Current Status

**In progress:** Dataset exploration, orders validation, and the initial orders transformation module.

Database integration, analytical SQL, and automated CI workflows are planned next.