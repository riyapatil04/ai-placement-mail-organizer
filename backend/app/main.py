from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {
        "message": "AI Mail Organizer backend is running",
        "status": "ok"
    }