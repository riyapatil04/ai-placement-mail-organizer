from fastapi import FastAPI

from app.database.db import Base, engine
from app.models.email import Email  # noqa: F401  (import to ensure table is registered)

# Create all tables (runs at startup)
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {
        "message": "AI Placement Mail Organizer backend is running",
        "status": "ok"
    }