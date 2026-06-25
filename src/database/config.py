import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://test_user:test_password@localhost:5432/ticketfast_test"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
