import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# Load environment variables from .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL was not found in the .env file")

# Create database engine
engine = create_engine(DATABASE_URL)

# Test connection
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))
        version = result.scalar()

        print("Successfully connected to Neon!")
        print("PostgreSQL version:", version)

except Exception as error:
    print("Database connection failed.")
    print("Error:", error)

finally:
    engine.dispose()