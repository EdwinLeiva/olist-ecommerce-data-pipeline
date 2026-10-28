# Olist E-commerce Data Pipeline

## Overview

An end-to-end data engineering project built with Python, pandas, and PostgreSQL to process and analyze the Olist Brazilian e-commerce dataset.

The project aims to develop a reliable ETL pipeline that extracts data from CSV files, validates and transforms records, loads related datasets into PostgreSQL, and supports business analysis through SQL queries.

## Objectives

- Build a reproducible ETL pipeline.
- Practice data cleaning and quality validation.
- Model relational data in PostgreSQL.
- Analyze e-commerce orders, payments, products, and deliveries using SQL.
- Implement automated tests with pytest.
- Automate quality checks with GitHub Actions.

## Technology Stack

- Python 3.13
- pandas
- PostgreSQL
- SQLAlchemy
- psycopg
- pytest
- Git and GitHub
- GitHub Actions

## Planned Project Structure

```text
olist-ecommerce-data-pipeline/
├── data/
│   ├── raw/
│   └── processed/
├── src/
├── tests/
├── sql/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Data Source

The project will use the public Olist Brazilian E-Commerce dataset, which contains related information about orders, customers, products, sellers, payments, and reviews.

The dataset will be downloaded separately and stored locally. Raw data files will not be committed to the repository.

## Planned ETL Workflow

1. Extract data from the source CSV files.
2. Inspect schemas, data types, missing values, and duplicates.
3. Transform and validate the datasets.
4. Load the data into PostgreSQL.
5. Run SQL queries to analyze business metrics.
6. Execute automated tests and quality checks.

## Security

- Store database credentials in a local `.env` file.
- Never commit real credentials to GitHub.
- Exclude raw and processed datasets from version control.

## Project Status

**In progress:** repository setup and initial project configuration.

## Author

**Edwin Leiva**

Data engineering portfolio project focused on ETL pipelines, relational databases, data quality, and SQL analytics.
