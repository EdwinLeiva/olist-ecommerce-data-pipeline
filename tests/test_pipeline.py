import pandas as pd

from src import pipeline


def test_run_pipeline_processes_all_datasets(
    monkeypatch,
    tmp_path,
):
    """Test the complete pipeline without connecting to the real database."""

    # 1. Arrange: create sample orders
    sample_orders = pd.DataFrame(
        {
            "order_id": ["order_1", "order_2"],
            "customer_id": ["customer_1", "customer_2"],
            "order_status": ["delivered", "shipped"],
            "order_purchase_timestamp": [
                "2017-10-02 10:00:00",
                "2017-10-03 11:00:00",
            ],
            "order_approved_at": [
                "2017-10-02 11:00:00",
                "2017-10-03 12:00:00",
            ],
            "order_delivered_carrier_date": [
                "2017-10-03 10:00:00",
                None,
            ],
            "order_delivered_customer_date": [
                "2017-10-05 14:00:00",
                None,
            ],
            "order_estimated_delivery_date": [
                "2017-10-10 00:00:00",
                "2017-10-12 00:00:00",
            ],
        }
    )

    # 2. Arrange: create sample order items
    sample_order_items = pd.DataFrame(
        {
            "order_id": ["order_1", "order_1", "order_2"],
            "order_item_id": [1, 2, 1],
            "product_id": ["product_1", "product_2", "product_3"],
            "seller_id": ["seller_1", "seller_2", "seller_1"],
            "shipping_limit_date": [
                "2017-10-03 10:00:00",
                "2017-10-03 11:00:00",
                "2017-10-04 12:00:00",
            ],
            "price": [100.0, 50.0, 75.0],
            "freight_value": [10.0, 5.0, 8.0],
        }
    )

    # 3. Arrange: create sample products
    sample_products = pd.DataFrame(
        {
            "product_id": ["product_1", "product_2", "product_3"],
            "product_category_name": [
                "electronics",
                "furniture",
                "sports",
            ],
            "product_weight_g": [500, 1200, 800],
        }
    )

    # 4. Arrange: isolate output files
    output_dir = tmp_path / "processed"
    monkeypatch.setattr(pipeline, "PROCESSED_DIR", output_dir)

    # 5. Arrange: simulate database operations
    class FakeEngine:
        def dispose(self):
            pass

    monkeypatch.setattr(
        pipeline,
        "load_orders",
        lambda: sample_orders.copy(),
    )

    monkeypatch.setattr(
        pipeline,
        "load_order_items",
        lambda: sample_order_items.copy(),
    )

    monkeypatch.setattr(
        pipeline,
        "load_products",
        lambda: sample_products.copy(),
    )

    monkeypatch.setattr(
        pipeline,
        "get_database_engine",
        lambda: FakeEngine(),
    )

    monkeypatch.setattr(
        pipeline,
        "load_orders_to_database",
        lambda df, engine: len(df),
    )

    monkeypatch.setattr(
        pipeline,
        "load_order_items_to_database",
        lambda df, engine: len(df),
    )

    monkeypatch.setattr(
        pipeline,
        "load_products_to_database",
        lambda df, engine: len(df),
    )

    # 6. Act: run the pipeline
    (
        transformed_orders,
        transformed_order_items,
        transformed_products,
    ) = pipeline.run_pipeline()

    # 7. Assert: verify orders
    assert len(transformed_orders) == 2
    assert transformed_orders["order_id"].nunique() == 2

    # 8. Assert: verify order items
    assert len(transformed_order_items) == 3
    assert not transformed_order_items.duplicated(
        subset=["order_id", "order_item_id"]
    ).any()

    # 9. Assert: verify products
    assert len(transformed_products) == 3
    assert transformed_products["product_id"].is_unique

    # 10. Assert: verify processed CSV files
    orders_output = output_dir / "orders_processed.csv"
    items_output = output_dir / "order_items_processed.csv"
    products_output = output_dir / "products_processed.csv"

    assert orders_output.exists()
    assert items_output.exists()
    assert products_output.exists()

    saved_orders = pd.read_csv(orders_output)
    saved_items = pd.read_csv(items_output)
    saved_products = pd.read_csv(products_output)

    assert len(saved_orders) == 2
    assert len(saved_items) == 3
    assert len(saved_products) == 3