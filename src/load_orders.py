import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.dialects.postgresql import insert


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

    print("Loading orders into PostgreSQL...")

    if df.empty:
        print("No orders to load.")
        return 0

    expected_rows = len(df)

    # Convert DataFrame records into dictionaries
    df = df.astype(object).where(pd.notna(df), None)
    records = df.to_dict(orient="records")

    # Build PostgreSQL UPSERT statement
    orders_table = "orders"

    columns = list(df.columns)

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

    print(f"Rows received: {expected_rows:,}")
    print(f"Rows currently in PostgreSQL: {actual_rows:,}")
    print("Orders incrementally loaded successfully.")

    return actual_rows


def main():
    """Load transformed Olist orders into Neon."""

    from src.transform_orders import load_orders, transform_orders

    print("=" * 60)
    print("LOADING OLIST ORDERS INTO NEON")
    print("=" * 60)

    # 1. Extract
    print("\nStep 1: Extracting orders...")
    orders = load_orders()
    print(f"Rows extracted: {len(orders):,}")

    # 2. Transform
    print("\nStep 2: Transforming orders...")
    transformed_orders = transform_orders(orders)
    print(f"Rows transformed: {len(transformed_orders):,}")

    # 3. Incremental Load
    print("\nStep 3: Loading orders into Neon...")
    engine = get_database_engine()

    try:
        rows_loaded = load_orders_to_database(
            transformed_orders,
            engine,
        )
        print(f"\nTotal orders in database: {rows_loaded:,}")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()