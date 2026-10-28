from pathlib import Path

import pandas as pd


# Define the path to the raw orders dataset
RAW_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
ORDERS_FILE = RAW_DATA_DIR / "olist_orders_dataset.csv"


def analyze_orders():
    """Analyze order statuses and missing delivery dates."""
    df = pd.read_csv(ORDERS_FILE)

    print("=" * 60)
    print("ORDER DATASET ANALYSIS")
    print("=" * 60)

    # 1. Dataset dimensions
    print(f"\nTotal orders: {len(df):,}")
    print(f"Total columns: {len(df.columns)}")

    # 2. Distribution of order statuses
    print("\nOrder status distribution:")
    print(df["order_status"].value_counts(dropna=False))

    # 3. Missing values in date columns
    date_columns = [
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    print("\nMissing values in order date columns:")
    print(df[date_columns].isnull().sum())

    # 4. Missing delivery dates grouped by order status
    print("\nMissing customer delivery dates by order status:")
    missing_delivery = df[df["order_delivered_customer_date"].isnull()]

    print(
        missing_delivery["order_status"]
        .value_counts(dropna=False)
    )

    # 5. Investigate delivered orders without customer delivery dates
    print("\nDelivered orders without customer delivery dates:")

    delivered_missing_date = df[
        (df["order_status"] == "delivered")
        & (df["order_delivered_customer_date"].isnull())
    ]

    columns_to_display = [
        "order_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    print(delivered_missing_date[columns_to_display].to_string(index=False))

    # 6. Check duplicate order IDs
    print("\nDuplicate order ID analysis:")

    duplicate_count = df["order_id"].duplicated().sum()

    print(f"Total duplicate order IDs: {duplicate_count}")

    if duplicate_count > 0:
        print("\nExample duplicate orders:")
        print(
            df[df["order_id"].duplicated(keep=False)]
            .sort_values("order_id")
            .head(10)[["order_id", "order_status"]]
            .to_string(index=False)
        )
    else:
        print("All order IDs are unique.")

    print("\nAnalysis completed.")


if __name__ == "__main__":
    analyze_orders()