import os
from sqlalchemy import create_engine, Engine

def connect_db() -> Engine:
    # Build DATABASE_URL from environment variables
    pg_user = os.getenv('PGUSER')
    pg_password = os.getenv('PGPASSWORD')
    pg_host = os.getenv('PGHOST')
    pg_port = os.getenv('PGPORT')
    pg_database = os.getenv('PGDATABASE')
    DATABASE_URL = f"postgresql+psycopg2://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"

    return create_engine(DATABASE_URL)
