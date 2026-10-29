
from pathlib import Path

import pandas as pd

from src.transform_orders import load_orders, transform_orders


def test_real_orders_dataset_transforms_successfully():
    project_root = Path(__file__).resolve().parent.parent
    orders_file = (
        project_root / "data" / "raw" / "olist_orders_dataset.csv"
    )

    # Skip this integration test if the local dataset is unavailable.
    if not orders_file.exists():
        import pytest
        pytest.skip("Olist orders CSV is not available locally")

    orders = load_orders(orders_file)
    transformed_orders = transform_orders(orders)

    assert len(orders) == 99_441
    assert len(transformed_orders) == len(orders)
    assert transformed_orders["order_id"].notna().all()
    assert transformed_orders["order_id"].is_unique

    date_column = "order_purchase_timestamp"
    assert pd.api.types.is_datetime64_any_dtype(
        transformed_orders[date_column]
    )

    # Missing delivery dates should remain missing.
    assert (
        transformed_orders["order_delivered_customer_date"].isna().sum()
        == orders["order_delivered_customer_date"].isna().sum()
    )
