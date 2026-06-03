from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@host.docker.internal:5432/telecom_ai_db"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

try:
    Base.metadata.create_all(bind=engine)
    print("Database connected successfully")
except Exception as e:
    print(f"Database connection skipped: {e}")