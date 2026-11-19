import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from src.logger import setup_logger


# Configure logger
logger = setup_logger()

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_database_engine():
    """Create and return a SQLAlchemy database engine."""

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL was not found in the .env file")

    return create_engine(DATABASE_URL)


def load_orders_to_database(df, engine):
    """Incrementally load orders into PostgreSQL using UPSERT."""

    logger.debug("Loading orders into PostgreSQL...")

    if df.empty:
        logger.debug("No orders to load.")
        return 0

    expected_rows = len(df)

    # Convert DataFrame records into dictionaries
    df = df.astype(object).where(pd.notna(df), None)
    records = df.to_dict(orient="records")

    # Build PostgreSQL UPSERT statement
    insert_statement = text("""
        INSERT INTO orders (
            order_id,
            customer_id,
            order_status,
            order_purchase_timestamp,
            order_approved_at,
            order_delivered_carrier_date,
            order_delivered_customer_date,
            order_estimated_delivery_date
        )
        VALUES (
            :order_id,
            :customer_id,
            :order_status,
            :order_purchase_timestamp,
            :order_approved_at,
            :order_delivered_carrier_date,
            :order_delivered_customer_date,
            :order_estimated_delivery_date
        )
        ON CONFLICT (order_id)
        DO UPDATE SET
            customer_id = EXCLUDED.customer_id,
            order_status = EXCLUDED.order_status,
            order_purchase_timestamp = EXCLUDED.order_purchase_timestamp,
            order_approved_at = EXCLUDED.order_approved_at,
            order_delivered_carrier_date = EXCLUDED.order_delivered_carrier_date,
            order_delivered_customer_date = EXCLUDED.order_delivered_customer_date,
            order_estimated_delivery_date = EXCLUDED.order_estimated_delivery_date
    """)

    # Execute UPSERT in batches
    batch_size = 1000

    with engine.begin() as connection:
        for start in range(0, len(records), batch_size):
            batch = records[start:start + batch_size]
            connection.execute(insert_statement, batch)

        actual_rows = connection.execute(
            text("SELECT COUNT(*) FROM orders")
        ).scalar_one()

    logger.debug("Rows received: %s", f"{expected_rows:,}")
    logger.debug("Rows currently in PostgreSQL: %s", f"{actual_rows:,}")
    logger.debug("Orders incrementally loaded successfully.")

    return actual_rows


def main():
    """Load transformed Olist orders into Neon."""

    from src.transform_orders import load_orders, transform_orders

    logger.info("=" * 60)
    logger.info("LOADING OLIST ORDERS INTO NEON")
    logger.info("=" * 60)

    # 1. Extract
    logger.info("Step 1: Extracting orders...")
    orders = load_orders()
    logger.info("Rows extracted: %s", f"{len(orders):,}")

    # 2. Transform
    logger.info("Step 2: Transforming orders...")
    transformed_orders = transform_orders(orders)
    logger.info(
        "Rows transformed: %s",
        f"{len(transformed_orders):,}",
    )

    # 3. Incremental Load
    logger.info("Step 3: Loading orders into Neon...")
    engine = get_database_engine()

    try:
        rows_loaded = load_orders_to_database(
            transformed_orders,
            engine,
        )
        logger.info(
            "Total orders in database: %s",
            f"{rows_loaded:,}",
        )
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()