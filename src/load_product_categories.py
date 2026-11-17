from sqlalchemy import text


def load_product_categories_to_database(df, engine):
    """Load unique product categories into PostgreSQL using UPSERT."""

    print("Loading product categories into PostgreSQL...")

    categories = (
        df["product_category_name"]
        .dropna()
        .drop_duplicates()
    )

    if categories.empty:
        print("No product categories to load.")
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

    print(f"Unique categories received: {len(records):,}")
    print(f"Categories currently in PostgreSQL: {actual_rows:,}")
    print("Product categories loaded successfully.")

    return actual_rows