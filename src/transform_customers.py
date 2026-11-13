from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_customers():
    """Load raw customers data."""
    file_path = RAW_DATA_DIR / "olist_customers_dataset.csv"

    return pd.read_csv(
        file_path,
        dtype={
            "customer_id": "string",
            "customer_unique_id": "string",
            "customer_zip_code_prefix": "string",
            "customer_city": "string",
            "customer_state": "string",
        },
    )


def transform_customers(df):
    """Clean and validate customers data."""
    df = df.copy()

    required_columns = [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state",
    ]

    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    df = df[required_columns]

    df = df.dropna(subset=["customer_id"])
    df = df.drop_duplicates(subset=["customer_id"])

    return df