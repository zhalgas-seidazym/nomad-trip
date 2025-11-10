from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

from src.config import settings

DATABASE_URL = settings.db_url

engine = create_engine(DATABASE_URL, echo=True, future=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_connection():
    try:
        with engine.connect():
            return True
    except OperationalError as e:
        raise RuntimeError(f"DB connection failed: {e}")
