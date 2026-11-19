from sqlalchemy import text

from src.logger import setup_logger


logger = setup_logger()


def load_product_categories_to_database(df, engine):
    """Load unique product categories into PostgreSQL using UPSERT."""

    logger.debug("Loading product categories into PostgreSQL...")

    categories = (
        df["product_category_name"]
        .dropna()
        .drop_duplicates()
    )

    if categories.empty:
        logger.debug("No product categories to load.")
        return 0

    records = [
        {"product_category_name": category}
        for category in categories
    ]

    insert_statement = text("""
        INSERT INTO product_categories (
            product_category_name
        )
        VALUES (
            :product_category_name
        )
        ON CONFLICT (product_category_name)
        DO NOTHING
    """)

    with engine.begin() as connection:
        connection.execute(insert_statement, records)

        actual_rows = connection.execute(
            text("SELECT COUNT(*) FROM product_categories")
        ).scalar_one()

    logger.debug("Unique categories received: %s", f"{len(records):,}")
    logger.debug(
        "Categories currently in PostgreSQL: %s",
        f"{actual_rows:,}",
    )
    logger.debug("Product categories loaded successfully.")

    return actual_rows