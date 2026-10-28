from pathlib import Path

import pandas as pd


# Locate the raw orders dataset
RAW_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
ORDERS_FILE = RAW_DATA_DIR / "olist_orders_dataset.csv"


def validate_orders():
    """Validate order dates and basic data quality rules."""
    df = pd.read_csv(ORDERS_FILE)

    print("=" * 60)
    print("ORDER DATA QUALITY VALIDATION")
    print("=" * 60)

    # 1. Check required identifiers
    missing_order_ids = df["order_id"].isna().sum()
    duplicate_order_ids = df["order_id"].duplicated().sum()

    print("\n1. Order identifiers")
    print(f"Missing order IDs: {missing_order_ids}")
    print(f"Duplicate order IDs: {duplicate_order_ids}")

    # 2. Convert date columns to datetime
    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for column in date_columns:
        df[column] = pd.to_datetime(df[column], errors="coerce")

    print("\n2. Missing dates after datetime conversion")
    print(df[date_columns].isna().sum())

    # 3. Check approval dates before purchase dates
    invalid_approval_dates = (
        df["order_approved_at"].notna()
        & df["order_purchase_timestamp"].notna()
        & (
            df["order_approved_at"]
            < df["order_purchase_timestamp"]
        )
    )

    print("\n3. Approval before purchase")
    print(f"Invalid records: {invalid_approval_dates.sum()}")

    # 4. Check carrier delivery before purchase
    invalid_carrier_dates = (
        df["order_delivered_carrier_date"].notna()
        & df["order_purchase_timestamp"].notna()
        & (
            df["order_delivered_carrier_date"]
            < df["order_purchase_timestamp"]
        )
    )

    print("\n4. Carrier delivery before purchase")
    print(f"Invalid records: {invalid_carrier_dates.sum()}")

    # 5. Check customer delivery before purchase
    invalid_customer_delivery_dates = (
        df["order_delivered_customer_date"].notna()
        & df["order_purchase_timestamp"].notna()
        & (
            df["order_delivered_customer_date"]
            < df["order_purchase_timestamp"]
        )
    )

    print("\n5. Customer delivery before purchase")
    print(f"Invalid records: {invalid_customer_delivery_dates.sum()}")

    # 6. Check customer delivery after estimated delivery
    late_delivery_comparison = (
        df["order_delivered_customer_date"].notna()
        & df["order_estimated_delivery_date"].notna()
    )

    delivered_after_estimate = (
        late_delivery_comparison
        & (
            df["order_delivered_customer_date"]
            > df["order_estimated_delivery_date"]
        )
    )

    print("\n6. Customer delivery after estimated date")
    print(f"Records delivered after estimate: {delivered_after_estimate.sum()}")

    # 7. Investigate carrier delivery dates before purchase
    print("\nExamples of carrier dates before purchase:")

    invalid_carrier_records = df.loc[
        invalid_carrier_dates,
        [
            "order_id",
            "order_status",
            "order_purchase_timestamp",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
        ],
    ]

    print(f"Total inconsistent records: {len(invalid_carrier_records)}")

    print(
        invalid_carrier_records
        .head(10)
        .to_string(index=False)
    )

    print("\nValidation completed. No records were modified or deleted.")


if __name__ == "__main__":
    validate_orders()