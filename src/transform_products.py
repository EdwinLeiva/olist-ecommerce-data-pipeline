from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

PRODUCTS_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "olist_products_dataset.csv"
)


def load_products(file_path=PRODUCTS_FILE):
    """Load the original Olist products dataset."""
    return pd.read_csv(file_path)


def transform_products(df):
    """Clean and transform the products dataset."""

    products = df.copy()

    # Remove records without product_id
    products = products.dropna(subset=["product_id"])

    # Remove duplicate products
    products = products.drop_duplicates(
        subset=["product_id"],
        keep="first",
    )

    # Convert product dimensions and weight to numeric values
    numeric_columns = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]

    for column in numeric_columns:
        if column in products.columns:
            products[column] = pd.to_numeric(
                products[column],
                errors="coerce",
            )

    return products


def main():
    products = load_products()
    transformed_products = transform_products(products)

    print(f"Products before transformation: {len(products):,}")
    print(
        "Products after transformation:",
        f"{len(transformed_products):,}",
    )

    print("\nMissing values after transformation:")
    print(transformed_products.isna().sum())

    return transformed_products


if __name__ == "__main__":
    main()