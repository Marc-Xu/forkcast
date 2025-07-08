import os
import tempfile

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.data_access_layer.database import Base
from app.main import app


# Create a temporary SQLite database for tests
@pytest.fixture(scope="session")
def db_engine():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    engine = create_engine(
        f"sqlite:///{path}", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    try:
        yield engine
    finally:
        engine.dispose()
        if os.path.exists(path):
            os.remove(path)


@pytest.fixture
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine, autoflush=False, autocommit=False)
    session = Session()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def client(db_session, monkeypatch):
    # Override the get_db dependency to use the test session
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    monkeypatch.setattr("app.data_access_layer.database.get_db", override_get_db)
    return TestClient(app)
