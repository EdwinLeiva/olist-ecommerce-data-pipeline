import pandas as pd
from sqlalchemy import text

from src.load_orders import get_database_engine
from src.transform_products import (
    load_products,
    transform_products,
)
from src.logger import setup_logger


logger = setup_logger()


def load_products_to_database(df, engine):
    """Load products into PostgreSQL using UPSERT."""

    logger.debug("Loading products into PostgreSQL...")

    if df.empty:
        logger.debug("No products to load.")
        return 0

    # Convert missing values (NaN/NaT) to None for PostgreSQL.
    df = df.astype(object).where(pd.notna(df), None)
    records = df.to_dict(orient="records")

    insert_statement = text("""
        INSERT INTO products (
            product_id,
            product_category_name,
            product_name_lenght,
            product_description_lenght,
            product_photos_qty,
            product_weight_g,
            product_length_cm,
            product_height_cm,
            product_width_cm
        )
        VALUES (
            :product_id,
            :product_category_name,
            :product_name_lenght,
            :product_description_lenght,
            :product_photos_qty,
            :product_weight_g,
            :product_length_cm,
            :product_height_cm,
            :product_width_cm
        )
        ON CONFLICT (product_id)
        DO UPDATE SET
            product_category_name = EXCLUDED.product_category_name,
            product_name_lenght = EXCLUDED.product_name_lenght,
            product_description_lenght = EXCLUDED.product_description_lenght,
            product_photos_qty = EXCLUDED.product_photos_qty,
            product_weight_g = EXCLUDED.product_weight_g,
            product_length_cm = EXCLUDED.product_length_cm,
            product_height_cm = EXCLUDED.product_height_cm,
            product_width_cm = EXCLUDED.product_width_cm
    """)

    batch_size = 1000

    with engine.begin() as connection:
        for start in range(0, len(records), batch_size):
            batch = records[start:start + batch_size]
            connection.execute(insert_statement, batch)

        actual_rows = connection.execute(
            text("SELECT COUNT(*) FROM products")
        ).scalar_one()

    logger.debug("Rows received: %s", f"{len(records):,}")
    logger.debug("Rows currently in PostgreSQL: %s", f"{actual_rows:,}")
    logger.debug("Products incrementally loaded successfully.")

    return actual_rows


def main():
    logger.info("Extracting products...")

    products = load_products()

    logger.info("Rows extracted: %s", f"{len(products):,}")

    logger.info("Transforming products...")

    transformed_products = transform_products(products)

    logger.info(
        "Rows transformed: %s",
        f"{len(transformed_products):,}",
    )

    engine = get_database_engine()

    try:
        rows_loaded = load_products_to_database(
            transformed_products,
            engine,
        )

        logger.info(
            "Total products in database: %s",
            f"{rows_loaded:,}",
        )

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()