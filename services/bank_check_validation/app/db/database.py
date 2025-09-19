import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

if not DB_HOST:
    raise ValueError("DB_HOST environment variable is not set.")
if not DB_PORT:
    raise ValueError("DB_PORT environment variable is not set.")
if not DB_USER:
    raise ValueError("DB_USER environment variable is not set.")
if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD environment variable is not set.")
if not DB_NAME:
    raise ValueError("DB_NAME environment variable is not set.")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()