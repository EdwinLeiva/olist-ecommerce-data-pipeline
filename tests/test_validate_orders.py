import pandas as pd
import pytest

from src import validate_orders


def test_validate_orders_fails_when_required_column_is_missing(
    tmp_path, monkeypatch
):
    # Create a temporary CSV missing the order_status column
    df = pd.DataFrame({
        "order_id": ["order_1"],
        "customer_id": ["customer_1"],
        "order_purchase_timestamp": ["2018-01-01 10:00:00"],
        "order_approved_at": ["2018-01-01 11:00:00"],
        "order_delivered_carrier_date": [None],
        "order_delivered_customer_date": [None],
        "order_estimated_delivery_date": ["2018-01-05 10:00:00"],
    })

    csv_path = tmp_path / "orders.csv"
    df.to_csv(csv_path, index=False)

    # Make the validation function use the temporary CSV
    monkeypatch.setattr(validate_orders, "ORDERS_FILE", csv_path)

    # Expect a clear error identifying the missing column
    with pytest.raises(
        ValueError,
        match="order_status",
    ):
        validate_orders.validate_orders()