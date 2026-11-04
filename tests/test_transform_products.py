import pandas as pd

from src.transform_products import transform_products


def test_transform_products_converts_numeric_columns():
    df = pd.DataFrame({
        "product_id": ["p1"],
        "product_category_name": ["electronics"],
        "product_name_lenght": ["40"],
        "product_description_lenght": ["200"],
        "product_photos_qty": ["3"],
        "product_weight_g": ["500"],
        "product_length_cm": ["20"],
        "product_height_cm": ["10"],
        "product_width_cm": ["15"],
    })

    result = transform_products(df)

    assert pd.api.types.is_numeric_dtype(
        result["product_weight_g"]
    )
    assert result["product_weight_g"].iloc[0] == 500


def test_transform_products_removes_duplicate_ids():
    df = pd.DataFrame({
        "product_id": ["p1", "p1", "p2"],
        "product_category_name": ["a", "a", "b"],
    })

    result = transform_products(df)

    assert len(result) == 2
    assert result["product_id"].is_unique


def test_transform_products_removes_missing_ids():
    df = pd.DataFrame({
        "product_id": ["p1", None, "p2"],
        "product_category_name": ["a", "b", "c"],
    })

    result = transform_products(df)

    assert len(result) == 2
    assert result["product_id"].notna().all()


def test_transform_products_preserves_missing_values():
    df = pd.DataFrame({
        "product_id": ["p1"],
        "product_category_name": [None],
        "product_weight_g": [None],
    })

    result = transform_products(df)

    assert pd.isna(result["product_category_name"].iloc[0])
    assert pd.isna(result["product_weight_g"].iloc[0])