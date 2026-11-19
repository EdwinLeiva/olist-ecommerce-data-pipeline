import logging

import pandas as pd
from sqlalchemy import text

from src.load_orders import get_database_engine
from src.transform_customers import (
    load_customers,
    transform_customers,
)
from src.logger import setup_logger


logger = setup_logger()


def load_customers_to_database(df, engine):
    """Load customers into PostgreSQL using UPSERT."""

    logger.debug("Loading customers into PostgreSQL...")

    if df.empty:
        logger.debug("No customers to load.")
        return 0

    # Convert missing values to None for PostgreSQL.
    df = df.astype(object).where(pd.notna(df), None)
    records = df.to_dict(orient="records")

    insert_statement = text("""
        INSERT INTO customers (
            customer_id,
            customer_unique_id,
            customer_zip_code_prefix,
            customer_city,
            customer_state
        )
        VALUES (
            :customer_id,
            :customer_unique_id,
            :customer_zip_code_prefix,
            :customer_city,
            :customer_state
        )
        ON CONFLICT (customer_id)
        DO UPDATE SET
            customer_unique_id = EXCLUDED.customer_unique_id,
            customer_zip_code_prefix = EXCLUDED.customer_zip_code_prefix,
            customer_city = EXCLUDED.customer_city,
            customer_state = EXCLUDED.customer_state
    """)

    batch_size = 1000

    with engine.begin() as connection:
        for start in range(0, len(records), batch_size):
            batch = records[start:start + batch_size]
            connection.execute(insert_statement, batch)

        actual_rows = connection.execute(
            text("SELECT COUNT(*) FROM customers")
        ).scalar_one()

    logger.debug("Rows received: %s", f"{len(records):,}")
    logger.debug("Rows currently in PostgreSQL: %s", f"{actual_rows:,}")
    logger.debug("Customers incrementally loaded successfully.")

    return actual_rows


def main():
    logger.info("Extracting customers...")

    customers = load_customers()

    logger.info("Rows extracted: %s", f"{len(customers):,}")

    logger.info("Transforming customers...")

    transformed_customers = transform_customers(customers)

    logger.info(
        "Rows transformed: %s",
        f"{len(transformed_customers):,}",
    )

    engine = get_database_engine()

    try:
        rows_loaded = load_customers_to_database(
            transformed_customers,
            engine,
        )

        logger.info(
            "Total customers in database: %s",
            f"{rows_loaded:,}",
        )

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
