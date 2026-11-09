import pandas as pd
from sqlalchemy import text

from src.load_orders import get_database_engine
from src.transform_products import (
    load_products,
    transform_products,
)


def load_products_to_database(df, engine):
    """Load products into PostgreSQL using UPSERT."""

    print("Loading products into PostgreSQL...")

    if df.empty:
        print("No products to load.")
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

    print(f"Rows received: {len(records):,}")
    print(f"Rows currently in PostgreSQL: {actual_rows:,}")
    print("Products incrementally loaded successfully.")

    return actual_rows


def main():
    print("Extracting products...")

    products = load_products()

    print(f"Rows extracted: {len(products):,}")

    print("Transforming products...")

    transformed_products = transform_products(products)

    print(f"Rows transformed: {len(transformed_products):,}")

    engine = get_database_engine()

    try:
        rows_loaded = load_products_to_database(
            transformed_products,
            engine,
        )

        print(f"Total products in database: {rows_loaded:,}")

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()