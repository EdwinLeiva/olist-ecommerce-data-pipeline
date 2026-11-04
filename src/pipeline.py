from pathlib import Path

from src.transform_orders import load_orders, transform_orders
from src.transform_order_items import (
    load_order_items,
    transform_order_items,
)
from src.transform_products import (
    load_products,
    transform_products,
)

from src.load_orders import (
    get_database_engine,
    load_orders_to_database,
)
from src.load_order_items import load_order_items_to_database
from src.load_products import load_products_to_database


# Project directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def run_pipeline():
    """
    Extract, transform, save, and load Olist datasets into Neon.
    """

    print("=" * 60)
    print("OLIST E-COMMERCE ETL PIPELINE")
    print("=" * 60)

    # 1. Extract
    print("\nStep 1: Extracting data...")

    orders = load_orders()
    order_items = load_order_items()
    products = load_products()

    print(f"Orders extracted: {len(orders):,}")
    print(f"Order items extracted: {len(order_items):,}")
    print(f"Products extracted: {len(products):,}")

    # 2. Transform
    print("\nStep 2: Transforming data...")

    transformed_orders = transform_orders(orders)
    transformed_order_items = transform_order_items(order_items)
    transformed_products = transform_products(products)

    print(f"Orders transformed: {len(transformed_orders):,}")
    print(f"Order items transformed: {len(transformed_order_items):,}")
    print(f"Products transformed: {len(transformed_products):,}")

    # 3. Save processed CSV files
    print("\nStep 3: Saving processed CSV files...")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    orders_output = PROCESSED_DIR / "orders_processed.csv"
    items_output = PROCESSED_DIR / "order_items_processed.csv"
    products_output = PROCESSED_DIR / "products_processed.csv"

    transformed_orders.to_csv(orders_output, index=False)
    transformed_order_items.to_csv(items_output, index=False)
    transformed_products.to_csv(products_output, index=False)

    print(f"Orders CSV saved: {orders_output}")
    print(f"Order items CSV saved: {items_output}")
    print(f"Products CSV saved: {products_output}")

    # 4. Load all tables into Neon
    print("\nStep 4: Loading data into Neon...")

    engine = get_database_engine()

    try:
        orders_loaded = load_orders_to_database(
            transformed_orders,
            engine,
        )
        print(f"Orders loaded and verified: {orders_loaded:,}")

        order_items_loaded = load_order_items_to_database(
            transformed_order_items,
            engine,
        )
        print(f"Order items loaded and verified: {order_items_loaded:,}")

        products_loaded = load_products_to_database(
            transformed_products,
            engine,
        )
        print(f"Products loaded and verified: {products_loaded:,}")

    finally:
        engine.dispose()

    # 5. Pipeline summary
    print("\nPipeline summary")
    print("-" * 40)

    print(f"Orders extracted: {len(orders):,}")
    print(f"Orders transformed: {len(transformed_orders):,}")
    print(f"Orders loaded: {orders_loaded:,}")

    print(f"Order items extracted: {len(order_items):,}")
    print(f"Order items transformed: {len(transformed_order_items):,}")
    print(f"Order items loaded: {order_items_loaded:,}")

    print(f"Products extracted: {len(products):,}")
    print(f"Products transformed: {len(transformed_products):,}")
    print(f"Products loaded: {products_loaded:,}")

    print(
        "Missing customer delivery dates:",
        transformed_orders["order_delivered_customer_date"].isna().sum(),
    )

    print(f"Orders CSV: {orders_output}")
    print(f"Order items CSV: {items_output}")
    print(f"Products CSV: {products_output}")

    print("\nETL pipeline completed successfully!")

    return (
        transformed_orders,
        transformed_order_items,
        transformed_products,
    )


if __name__ == "__main__":
    run_pipeline()