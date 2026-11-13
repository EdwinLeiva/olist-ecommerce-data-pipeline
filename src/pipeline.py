from pathlib import Path
from src.logger import setup_logger

from src.transform_orders import load_orders, transform_orders
from src.transform_order_items import (
    load_order_items,
    transform_order_items,
)
from src.transform_products import (
    load_products,
    transform_products,
)

from src.transform_customers import (
    load_customers,
    transform_customers,
)

from src.load_orders import (
    get_database_engine,
    load_orders_to_database,
)
from src.load_order_items import load_order_items_to_database
from src.load_products import load_products_to_database
from src.load_customers import load_customers_to_database

# Project directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

logger = setup_logger()


def run_pipeline():
    """
    Extract, transform, save, and load Olist datasets into Neon.
    """
    logger.info("=" * 60)
    logger.info("OLIST E-COMMERCE ETL PIPELINE")
    logger.info("=" * 60)
    

    # 1. Extract
    logger.info("Step 1: Extracting data...")

    orders = load_orders()
    order_items = load_order_items()
    products = load_products()

    logger.info("Orders extracted: %s", f"{len(orders):,}")
    logger.info("Order items extracted: %s", f"{len(order_items):,}")
    logger.info("Products extracted: %s", f"{len(products):,}")

    logger.info("Extracting customers...")
    customers = load_customers()
    logger.info(f"Customers extracted: {len(customers):,}")

    # 2. Transform
    logger.info("Step 2: Transforming data...")

    transformed_orders = transform_orders(orders)
    transformed_order_items = transform_order_items(order_items)
    transformed_products = transform_products(products)

    logger.info("Orders transformed: %s", f"{len(transformed_orders):,}")
    logger.info("Order items transformed: %s", f"{len(transformed_order_items):,}")
    logger.info("Products transformed: %s", f"{len(transformed_products):,}")
    logger.info("Transforming customers...")
    transformed_customers = transform_customers(customers)
    logger.info(
        f"Customers transformed: {len(transformed_customers):,}"
    )

    # 3. Save processed CSV files
    logger.info("Step 3: Saving processed CSV files...")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    orders_output = PROCESSED_DIR / "orders_processed.csv"
    items_output = PROCESSED_DIR / "order_items_processed.csv"
    products_output = PROCESSED_DIR / "products_processed.csv"

    transformed_orders.to_csv(orders_output, index=False)
    transformed_order_items.to_csv(items_output, index=False)
    transformed_products.to_csv(products_output, index=False)

    logger.info("Orders CSV saved: %s", orders_output)
    logger.info("Order items CSV saved: %s", items_output)
    logger.info("Products CSV saved: %s", products_output)

    customers_output = PROCESSED_DIR / "customers_processed.csv"
    transformed_customers.to_csv(customers_output, index=False)
    logger.info(f"Processed customers saved to: {customers_output}")

    # 4. Load all tables into Neon
    logger.info("Step 4: Loading data into Neon...")

    engine = get_database_engine()

    try:
        orders_loaded = load_orders_to_database(
            transformed_orders,
            engine,
        )
        logger.info("Orders loaded and verified: %s", f"{orders_loaded:,}")

        order_items_loaded = load_order_items_to_database(
            transformed_order_items,
            engine,
        )
        logger.info("Order items loaded and verified: %s", f"{order_items_loaded:,}")

        products_loaded = load_products_to_database(
            transformed_products,
            engine,
        )
        logger.info("Products loaded and verified: %s", f"{products_loaded:,}")

        customers_loaded = load_customers_to_database(
            transformed_customers,
            engine,
        )
        logger.info(
            f"Customers loaded into database: {customers_loaded:,}"
        )

    finally:
        engine.dispose()

    # 5. Pipeline summary
    logger.info("Pipeline summary")
    logger.info("-" * 40)

    logger.info("Orders extracted: %s", f"{len(orders):,}")
    logger.info("Orders transformed: %s", f"{len(transformed_orders):,}")
    logger.info("Orders loaded: %s", f"{orders_loaded:,}")

    logger.info("Order items extracted: %s", f"{len(order_items):,}")
    logger.info("Order items transformed: %s", f"{len(transformed_order_items):,}")
    logger.info("Order items loaded: %s", f"{order_items_loaded:,}")

    logger.info("Products extracted: %s", f"{len(products):,}")
    logger.info("Products transformed: %s", f"{len(transformed_products):,}")
    logger.info("Products loaded: %s", f"{products_loaded:,}")

    missing_delivery_dates = (
        transformed_orders["order_delivered_customer_date"].isna().sum()
    )

    logger.warning(
        "Orders with missing customer delivery dates: %s",
        f"{missing_delivery_dates:,}",
    )

    logger.info("Orders CSV: %s", orders_output)
    logger.info("Order items CSV: %s", items_output)
    logger.info("Products CSV: %s", products_output)
    logger.info(f"Customers loaded: {customers_loaded:,}")
    logger.info("ETL pipeline completed successfully!")

    return (
        transformed_orders,
        transformed_order_items,
        transformed_products,
        transformed_customers,
    )
if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception:
        logger.exception("ETL pipeline failed.")
        raise