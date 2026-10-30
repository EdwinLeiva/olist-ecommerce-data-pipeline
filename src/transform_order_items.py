from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

ORDER_ITEMS_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "olist_order_items_dataset.csv"
)

DATE_COLUMNS = ["shipping_limit_date"]


def load_order_items(file_path=ORDER_ITEMS_FILE):
    """Load the original order items CSV."""
    return pd.read_csv(file_path)


def transform_order_items(df):
    """Convert date columns and apply basic data quality rules."""

    order_items = df.copy()

    # Convert date columns
    for column in DATE_COLUMNS:
        order_items[column] = pd.to_datetime(
            order_items[column],
            errors="coerce",
        )

    # Remove rows without essential identifiers
    order_items = order_items.dropna(
        subset=["order_id", "order_item_id"]
    )

    # Remove duplicate items within the same order
    order_items = order_items.drop_duplicates(
        subset=["order_id", "order_item_id"],
        keep="first",
    )

    return order_items


def main():
    order_items = load_order_items()

    transformed_items = transform_order_items(order_items)

    print(f"Original rows: {len(order_items):,}")
    print(f"Transformed rows: {len(transformed_items):,}")

    print(
        "Shipping dates converted:",
        pd.api.types.is_datetime64_any_dtype(
            transformed_items["shipping_limit_date"]
        ),
    )

    print(
        "Duplicate order items:",
        transformed_items.duplicated(
            subset=["order_id", "order_item_id"]
        ).sum(),
    )


if __name__ == "__main__":
    main()