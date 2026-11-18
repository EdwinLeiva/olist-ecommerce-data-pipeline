import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def test_database_connection():
    """Test the connection to the Neon PostgreSQL database."""

    load_dotenv()

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL was not found in the .env file")

    engine = create_engine(database_url)

    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.scalar()

            print("Successfully connected to Neon!")
            print("PostgreSQL version:", version)

    finally:
        engine.dispose()


if __name__ == "__main__":
    test_database_connection()