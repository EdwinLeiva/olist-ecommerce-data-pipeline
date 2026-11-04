from sqlalchemy import text

from src.load_orders import get_database_engine
from src.transform_products import (
    load_products,
    transform_products,
)


def load_products_to_database(df, engine):
    """Load transformed products into PostgreSQL."""

    print("Loading products into PostgreSQL...")

    expected_rows = len(df)

    df.to_sql(
        name="products",
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=5000,
        method="multi",
    )

    # Verify the actual number of rows in PostgreSQL
    with engine.connect() as connection:
        actual_rows = connection.execute(
            text("SELECT COUNT(*) FROM products")
        ).scalar_one()

    print(f"Rows expected: {expected_rows:,}")
    print(f"Rows verified in PostgreSQL: {actual_rows:,}")

    if actual_rows != expected_rows:
        raise ValueError(
            f"Row count mismatch: expected {expected_rows}, "
            f"found {actual_rows}"
        )

    print("Products table created and verified successfully.")

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

        print(
            f"Successfully loaded {rows_loaded:,} products into Neon!"
        )

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()