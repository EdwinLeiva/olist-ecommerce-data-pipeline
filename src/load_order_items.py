from sqlalchemy import text

from src.load_orders import get_database_engine
from src.transform_order_items import (
    load_order_items,
    transform_order_items,
)


def load_order_items_to_database(df, engine):
    """Load transformed order items into PostgreSQL."""

    print("Loading order items into PostgreSQL...")

    expected_rows = len(df)

    df.to_sql(
        name="order_items",
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=5000,
        method="multi",
    )

    # Verify the actual number of rows in PostgreSQL
    with engine.connect() as connection:
        actual_rows = connection.execute(
            text("SELECT COUNT(*) FROM order_items")
        ).scalar_one()

    print(f"Rows expected: {expected_rows:,}")
    print(f"Rows verified in PostgreSQL: {actual_rows:,}")

    if actual_rows != expected_rows:
        raise ValueError(
            f"Row count mismatch: expected {expected_rows}, "
            f"found {actual_rows}"
        )

    print("Order items table created and verified successfully.")

    return actual_rows


def main():
    print("Extracting order items...")

    order_items = load_order_items()

    print(f"Rows extracted: {len(order_items):,}")

    print("Transforming order items...")

    transformed_items = transform_order_items(order_items)

    print(f"Rows transformed: {len(transformed_items):,}")

    engine = get_database_engine()

    try:
        rows_loaded = load_order_items_to_database(
            transformed_items,
            engine,
        )

        print(
            f"Successfully loaded {rows_loaded:,} order items into Neon!"
        )

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()