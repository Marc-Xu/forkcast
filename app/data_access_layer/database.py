"""
Setup SQLAlchemy engine and session factory.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import Settings

settings = Settings()

# Engine configuration
engine = create_engine(
    settings.db_url,
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for models
Base = declarative_base()


# Dependency to provide a database session
def get_db():
    """
    Dependency to provide a database session and close it after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
