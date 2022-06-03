"""
Global conftest file for shared resources among tests
"""

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.utils.config import get_settings

os.environ["codefoo-env"] = 'test'


@pytest.fixture
def api_client() -> TestClient:
    from app.simple_api.main import app
    return TestClient(app)


@pytest.fixture
def db_session() -> Session:
    db_url = get_settings().DATABASE_URL

    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False},
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()
