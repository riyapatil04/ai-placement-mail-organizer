from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./placement.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # required for SQLite in multi-threaded FastAPI
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()