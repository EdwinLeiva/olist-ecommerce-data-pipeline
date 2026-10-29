import pandas as pd

from src.transform_orders import transform_orders


def test_transform_orders_converts_dates():
    df = pd.DataFrame({
        "order_id": ["order_1"],
        "order_status": ["delivered"],
        "order_purchase_timestamp": ["2018-01-01 10:00:00"],
        "order_approved_at": ["2018-01-01 11:00:00"],
        "order_delivered_carrier_date": ["2018-01-02 10:00:00"],
        "order_delivered_customer_date": ["2018-01-03 10:00:00"],
        "order_estimated_delivery_date": ["2018-01-05 10:00:00"],
    })

    result = transform_orders(df)

    assert pd.api.types.is_datetime64_any_dtype(
        result["order_purchase_timestamp"]
    )


def test_transform_orders_removes_duplicate_ids():
    df = pd.DataFrame({
        "order_id": ["order_1", "order_1", "order_2"],
        "order_status": ["delivered", "delivered", "shipped"],
        "order_purchase_timestamp": [
            "2018-01-01 10:00:00",
            "2018-01-01 10:00:00",
            "2018-01-02 10:00:00",
        ],
        "order_approved_at": [None, None, None],
        "order_delivered_carrier_date": [None, None, None],
        "order_delivered_customer_date": [None, None, None],
        "order_estimated_delivery_date": [None, None, None],
    })

    result = transform_orders(df)

    assert len(result) == 2
    assert result["order_id"].is_unique


def test_transform_orders_preserves_missing_delivery_dates():
    df = pd.DataFrame({
        "order_id": ["order_1"],
        "order_status": ["shipped"],
        "order_purchase_timestamp": ["2018-01-01 10:00:00"],
        "order_approved_at": [None],
        "order_delivered_carrier_date": [None],
        "order_delivered_customer_date": [None],
        "order_estimated_delivery_date": ["2018-01-05 10:00:00"],
    })

    result = transform_orders(df)

    assert pd.isna(result.iloc[0]["order_delivered_customer_date"])
    assert len(result) == 1