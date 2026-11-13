import pandas as pd
import pytest

from src.transform_customers import transform_customers


@pytest.fixture
def sample_customers():
    return pd.DataFrame({
        "customer_id": ["C001", "C002", "C003", "C003"],
        "customer_unique_id": ["U001", "U002", "U003", "U003"],
        "customer_zip_code_prefix": ["12345", "23456", "34567", "34567"],
        "customer_city": ["Sao Paulo", "Rio", "Curitiba", "Curitiba"],
        "customer_state": ["SP", "RJ", "PR", "PR"],
    })


def test_transform_customers_removes_duplicates(sample_customers):
    result = transform_customers(sample_customers)

    assert len(result) == 3
    assert result["customer_id"].is_unique


def test_transform_customers_preserves_columns(sample_customers):
    result = transform_customers(sample_customers)

    expected_columns = [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state",
    ]

    assert list(result.columns) == expected_columns


def test_transform_customers_preserves_zip_code_as_string(sample_customers):
    result = transform_customers(sample_customers)

    assert result["customer_zip_code_prefix"].dtype == "string"


def test_transform_customers_missing_required_column(sample_customers):
    sample_customers = sample_customers.drop(columns=["customer_city"])

    with pytest.raises(ValueError, match="Missing required columns"):
        transform_customers(sample_customers)