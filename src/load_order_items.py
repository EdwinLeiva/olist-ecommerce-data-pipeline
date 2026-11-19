import pandas as pd
from sqlalchemy import text

from src.load_orders import get_database_engine
from src.transform_order_items import (
    load_order_items,
    transform_order_items,
)
from src.logger import setup_logger


logger = setup_logger()


def load_order_items_to_database(df, engine):
    """Load order items into PostgreSQL using UPSERT."""

    logger.debug("Loading order items into PostgreSQL...")

    if df.empty:
        logger.debug("No order items to load.")
        return 0

    # Convert missing values (NaN/NaT) to None for PostgreSQL.
    df = df.astype(object).where(pd.notna(df), None)
    records = df.to_dict(orient="records")

    insert_statement = text("""
        INSERT INTO order_items (
            order_id,
            order_item_id,
            product_id,
            seller_id,
            shipping_limit_date,
            price,
            freight_value
        )
        VALUES (
            :order_id,
            :order_item_id,
            :product_id,
            :seller_id,
            :shipping_limit_date,
            :price,
            :freight_value
        )
        ON CONFLICT (order_id, order_item_id)
        DO UPDATE SET
            product_id = EXCLUDED.product_id,
            seller_id = EXCLUDED.seller_id,
            shipping_limit_date = EXCLUDED.shipping_limit_date,
            price = EXCLUDED.price,
            freight_value = EXCLUDED.freight_value
    """)

    batch_size = 1000

    with engine.begin() as connection:
        for start in range(0, len(records), batch_size):
            batch = records[start:start + batch_size]
            connection.execute(insert_statement, batch)

        actual_rows = connection.execute(
            text("SELECT COUNT(*) FROM order_items")
        ).scalar_one()

    logger.debug("Rows received: %s", f"{len(records):,}")
    logger.debug("Rows currently in PostgreSQL: %s", f"{actual_rows:,}")
    logger.debug("Order items incrementally loaded successfully.")

    return actual_rows


def main():
    logger.info("Extracting order items...")

    order_items = load_order_items()

    logger.info("Rows extracted: %s", f"{len(order_items):,}")

    logger.info("Transforming order items...")

    transformed_items = transform_order_items(order_items)

    logger.info(
        "Rows transformed: %s",
        f"{len(transformed_items):,}",
    )

    engine = get_database_engine()

    try:
        rows_loaded = load_order_items_to_database(
            transformed_items,
            engine,
        )

        logger.info(
            "Total order items in database: %s",
            f"{rows_loaded:,}",
        )

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()