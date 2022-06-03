from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from ..utils.config import get_settings

# Potential: create a class to contain following variable
# instead of exposing them as global variables

# TODO: check for None and create default SQLite database
database_url = get_settings().DATABASE_URL

engine = create_engine(
    database_url, connect_args={"check_same_thread": False}
)
print(f"connected to {database_url}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_session_generator():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_session() -> Session:
    Base.metadata.create_all(bind=engine)
    return SessionLocal()
