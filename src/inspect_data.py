from pathlib import Path

import pandas as pd


# Define the directory containing the raw CSV files
RAW_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def inspect_csv_files():
    """Display basic information about each CSV file."""
    csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))

    if not csv_files:
        print("No CSV files found in the raw data directory.")
        return

    for file_path in csv_files:
        print("\n" + "=" * 60)
        print(f"File: {file_path.name}")

        df = pd.read_csv(file_path, nrows=1000)

        print(f"Rows inspected: {len(df)}")
        print(f"Columns: {len(df.columns)}")
        print("\nColumn names:")
        print(df.columns.tolist())

        print("\nMissing values in the inspected sample:")
        print(df.isnull().sum())

    print("\nInspection completed.")


if __name__ == "__main__":
    inspect_csv_files()