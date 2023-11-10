import os
from absl import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

ENV = os.getenv("ENV")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")

if "postgres" in DATABASE_URL:
    if ENV == "dev":
        logging.warning(
            "Using a postgres database while in development mode. Make sure you have configured your environment variables correctly."
        )
    engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
else:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
