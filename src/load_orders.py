import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_database_engine():
    """Create and return a SQLAlchemy database engine."""

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL was not found in the .env file")

    return create_engine(DATABASE_URL)



def load_orders_to_database(df, engine):
    """Load transformed orders into PostgreSQL."""

    print("Loading orders into PostgreSQL...")

    expected_rows = len(df)

    df.to_sql(
        name="orders",
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=5000,
        method="multi",
    )

    # Verify the actual number of rows in PostgreSQL
    from sqlalchemy import text

    with engine.connect() as connection:
        actual_rows = connection.execute(
            text("SELECT COUNT(*) FROM orders")
        ).scalar_one()

    print(f"Rows expected: {expected_rows:,}")
    print(f"Rows verified in PostgreSQL: {actual_rows:,}")

    if actual_rows != expected_rows:
        raise ValueError(
            f"Row count mismatch: expected {expected_rows}, "
            f"found {actual_rows}"
        )

    print("Orders table created and verified successfully.")

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

    # 3. Load
    print("\nStep 3: Loading orders into Neon...")
    engine = get_database_engine()

    try:
        rows_loaded = load_orders_to_database(
            transformed_orders,
            engine,
        )
        print(f"\nSuccessfully loaded {rows_loaded:,} orders!")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()