from pathlib import Path

import pandas as pd

from src import pipeline


def test_run_pipeline_returns_transformed_orders(monkeypatch, tmp_path):
    """Test the pipeline without connecting to the real database."""

    # Arrange: create sample orders
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

    # Arrange: isolate the output file in a temporary directory
    output_dir = tmp_path / "processed"
    output_file = output_dir / "orders_processed.csv"

    monkeypatch.setattr(pipeline, "PROCESSED_DIR", output_dir)
    monkeypatch.setattr(pipeline, "OUTPUT_FILE", output_file)

    # Arrange: simulate database operations
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
        "get_database_engine",
        lambda: FakeEngine(),
    )

    monkeypatch.setattr(
        pipeline,
        "load_orders_to_database",
        lambda df, engine: len(df),
    )

    # Act: run the pipeline
    result = pipeline.run_pipeline()

    # Assert: verify the transformed data
    assert len(result) == 2
    assert result["order_id"].nunique() == 2

    # Assert: verify the processed CSV was created
    assert output_file.exists()

    saved_data = pd.read_csv(output_file)

    assert len(saved_data) == 2
    assert saved_data["order_id"].nunique() == 2