from pathlib import Path

from src.transform_orders import load_orders, transform_orders
from src.load_orders import get_database_engine, load_orders_to_database


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = PROCESSED_DIR / "orders_processed.csv"


def run_pipeline():
    """Extract, transform, save to CSV, and load into Neon."""

    print("=" * 60)
    print("OLIST E-COMMERCE ETL PIPELINE")
    print("=" * 60)

    # 1. Extract
    print("\nStep 1: Extracting orders...")
    orders = load_orders()
    print(f"Rows extracted: {len(orders):,}")

    # 2. Transform
    print("\nStep 2: Transforming orders...")
    transformed_orders = transform_orders(orders)
    print(f"Rows transformed: {len(transformed_orders):,}")

    # 3. Save processed CSV
    print("\nStep 3: Saving processed orders to CSV...")
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    transformed_orders.to_csv(OUTPUT_FILE, index=False)
    print(f"Processed file saved: {OUTPUT_FILE}")

    # 4. Load into Neon
    print("\nStep 4: Loading orders into Neon...")
    engine = get_database_engine()

    try:
        rows_loaded = load_orders_to_database(
            transformed_orders,
            engine,
        )
        print(f"Successfully loaded {rows_loaded:,} orders into Neon!")
    finally:
        engine.dispose()

    # 5. Pipeline summary
    print("\nPipeline summary")
    print("-" * 30)
    print(f"Extracted rows: {len(orders):,}")
    print(f"Transformed rows: {len(transformed_orders):,}")
    print(f"Unique order IDs: {transformed_orders['order_id'].nunique():,}")
    print(
        "Missing customer delivery dates:",
        transformed_orders["order_delivered_customer_date"].isna().sum(),
    )
    print(f"CSV output: {OUTPUT_FILE}")
    print(f"PostgreSQL table: orders")
    print(f"Rows verified in Neon: {rows_loaded:,}")

    print("\nETL pipeline completed successfully!")

    return transformed_orders


if __name__ == "__main__":
    run_pipeline()