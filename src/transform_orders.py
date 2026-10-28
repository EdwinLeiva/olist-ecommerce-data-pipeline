from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ORDERS_FILE = PROJECT_ROOT / "data" / "raw" / "olist_orders_dataset.csv"

DATE_COLUMNS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]


def load_orders(file_path=ORDERS_FILE):
    """Load the original orders CSV without modifying the source file."""
    return pd.read_csv(file_path)


def transform_orders(df):
    """Convert date columns and apply basic data quality rules."""
    orders = df.copy()

    # Convert date columns to pandas datetime values.
    for column in DATE_COLUMNS:
        orders[column] = pd.to_datetime(
            orders[column],
            errors="coerce",
        )

    # Remove rows only when the order ID is missing or duplicated.
    orders = orders.dropna(subset=["order_id"])
    orders = orders.drop_duplicates(subset=["order_id"], keep="first")

    return orders


def main():
    orders = load_orders()
    transformed_orders = transform_orders(orders)

    print(f"Original rows: {len(orders):,}")
    print(f"Transformed rows: {len(transformed_orders):,}")
    print(
        "Purchase timestamps converted:",
        pd.api.types.is_datetime64_any_dtype(
            transformed_orders["order_purchase_timestamp"]
        ),
    )
    print(
        "Duplicate order IDs:",
        transformed_orders["order_id"].duplicated().sum(),
    )
    print(
        "Missing customer delivery dates:",
        transformed_orders["order_delivered_customer_date"].isna().sum(),
    )


if __name__ == "__main__":
    main()