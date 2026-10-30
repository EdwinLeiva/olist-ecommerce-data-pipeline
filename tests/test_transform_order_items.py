import pandas as pd

from src.transform_order_items import transform_order_items


def test_transform_order_items_converts_dates():
    """Test that shipping dates are converted to datetime."""

    df = pd.DataFrame({
        "order_id": ["order_1"],
        "order_item_id": [1],
        "product_id": ["product_1"],
        "seller_id": ["seller_1"],
        "shipping_limit_date": ["2017-09-19 09:45:35"],
        "price": [58.90],
        "freight_value": [13.29],
    })

    result = transform_order_items(df)

    assert pd.api.types.is_datetime64_any_dtype(
        result["shipping_limit_date"]
    )


def test_transform_order_items_removes_duplicate_items():
    """Test that duplicate items within an order are removed."""

    df = pd.DataFrame({
        "order_id": ["order_1", "order_1"],
        "order_item_id": [1, 1],
        "product_id": ["product_1", "product_1"],
        "seller_id": ["seller_1", "seller_1"],
        "shipping_limit_date": [
            "2017-09-19 09:45:35",
            "2017-09-19 09:45:35",
        ],
        "price": [58.90, 58.90],
        "freight_value": [13.29, 13.29],
    })

    result = transform_order_items(df)

    assert len(result) == 1
    assert result.duplicated(
        subset=["order_id", "order_item_id"]
    ).sum() == 0


def test_transform_order_items_preserves_valid_records():
    """Test that valid records are not removed."""

    df = pd.DataFrame({
        "order_id": ["order_1", "order_2"],
        "order_item_id": [1, 1],
        "product_id": ["product_1", "product_2"],
        "seller_id": ["seller_1", "seller_2"],
        "shipping_limit_date": [
            "2017-09-19 09:45:35",
            "2017-09-20 10:00:00",
        ],
        "price": [58.90, 239.90],
        "freight_value": [13.29, 19.93],
    })

    result = transform_order_items(df)

    assert len(result) == 2
    assert result["order_id"].notna().all()