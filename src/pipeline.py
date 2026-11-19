from pathlib import Path
from prefect import flow, get_run_logger

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
from src.load_product_categories import (
    load_product_categories_to_database,
)
from src.load_customers import load_customers_to_database


# Project directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

logger = setup_logger()


@flow(name="Olist E-commerce ETL Pipeline")
def run_pipeline():
    """
    Extract, transform, save, and load Olist datasets into Neon.
    """

    prefect_logger = get_run_logger()

    prefect_logger.info("=" * 60)
    prefect_logger.info("OLIST E-COMMERCE ETL PIPELINE")
    prefect_logger.info("=" * 60)

    # 1. Extract
    prefect_logger.info("Step 1: Extracting data...")

    orders = load_orders()
    order_items = load_order_items()
    products = load_products()
    customers = load_customers()

    logger.debug("Orders extracted: %s", f"{len(orders):,}")
    logger.debug("Order items extracted: %s", f"{len(order_items):,}")
    logger.debug("Products extracted: %s", f"{len(products):,}")
    logger.debug("Customers extracted: %s", f"{len(customers):,}")

    # 2. Transform
    prefect_logger.info("Step 2: Transforming data...")

    transformed_orders = transform_orders(orders)
    transformed_order_items = transform_order_items(order_items)
    transformed_products = transform_products(products)
    transformed_customers = transform_customers(customers)

    logger.debug("Orders transformed: %s", f"{len(transformed_orders):,}")
    logger.debug(
        "Order items transformed: %s",
        f"{len(transformed_order_items):,}",
    )
    logger.debug("Products transformed: %s", f"{len(transformed_products):,}")
    logger.debug(
        "Customers transformed: %s",
        f"{len(transformed_customers):,}",
    )

    # 3. Save processed CSV files
    prefect_logger.info("Step 3: Saving processed CSV files...")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    orders_output = PROCESSED_DIR / "orders_processed.csv"
    items_output = PROCESSED_DIR / "order_items_processed.csv"
    products_output = PROCESSED_DIR / "products_processed.csv"
    customers_output = PROCESSED_DIR / "customers_processed.csv"

    transformed_orders.to_csv(orders_output, index=False)
    transformed_order_items.to_csv(items_output, index=False)
    transformed_products.to_csv(products_output, index=False)
    transformed_customers.to_csv(customers_output, index=False)

    logger.debug("Orders CSV saved: %s", orders_output)
    logger.debug("Order items CSV saved: %s", items_output)
    logger.debug("Products CSV saved: %s", products_output)
    logger.debug("Customers CSV saved: %s", customers_output)

    # 4. Load all tables into Neon
    prefect_logger.info("Step 4: Loading data into Neon...")

    engine = get_database_engine()

    try:
        # Load parent tables before dependent tables.
        customers_loaded = load_customers_to_database(
            transformed_customers,
            engine,
        )
        logger.debug(
            "Customers loaded and verified: %s",
            f"{customers_loaded:,}",
        )

        categories_loaded = load_product_categories_to_database(
            transformed_products,
            engine,
        )
        logger.debug(
            "Product categories loaded and verified: %s",
            f"{categories_loaded:,}",
        )

        products_loaded = load_products_to_database(
            transformed_products,
            engine,
        )
        logger.debug(
            "Products loaded and verified: %s",
            f"{products_loaded:,}",
        )

        orders_loaded = load_orders_to_database(
            transformed_orders,
            engine,
        )
        logger.debug(
            "Orders loaded and verified: %s",
            f"{orders_loaded:,}",
        )

        order_items_loaded = load_order_items_to_database(
            transformed_order_items,
            engine,
        )
        logger.debug(
            "Order items loaded and verified: %s",
            f"{order_items_loaded:,}",
        )

    finally:
        engine.dispose()

    # 5. Pipeline summary
    prefect_logger.info("Pipeline summary")
    prefect_logger.info("-" * 40)

    prefect_logger.info("Customers loaded: %s", f"{customers_loaded:,}")
    prefect_logger.info("Product categories loaded: %s", f"{categories_loaded:,}")

    prefect_logger.info("Products extracted: %s", f"{len(products):,}")
    prefect_logger.info(
        "Products transformed: %s",
        f"{len(transformed_products):,}",
    )
    prefect_logger.info("Products loaded: %s", f"{products_loaded:,}")

    prefect_logger.info("Orders extracted: %s", f"{len(orders):,}")
    prefect_logger.info(
        "Orders transformed: %s",
        f"{len(transformed_orders):,}",
    )
    prefect_logger.info("Orders loaded: %s", f"{orders_loaded:,}")

    prefect_logger.info("Order items extracted: %s", f"{len(order_items):,}")
    prefect_logger.info(
        "Order items transformed: %s",
        f"{len(transformed_order_items):,}",
    )
    prefect_logger.info("Order items loaded: %s", f"{order_items_loaded:,}")

    missing_delivery_dates = (
        transformed_orders["order_delivered_customer_date"].isna().sum()
    )

    prefect_logger.warning(
        "Orders with missing customer delivery dates: %s",
        f"{missing_delivery_dates:,}",
    )

    prefect_logger.info("Orders CSV: %s", orders_output)
    prefect_logger.info("Order items CSV: %s", items_output)
    prefect_logger.info("Products CSV: %s", products_output)
    prefect_logger.info("Customers CSV: %s", customers_output)

    prefect_logger.info("ETL pipeline completed successfully!")

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