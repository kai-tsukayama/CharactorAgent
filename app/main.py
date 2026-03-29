from fastapi import FastAPI
from app.db import init_db, seed_characters
from app.repositories.character_repository import get_all_characters
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_characters()
    print("DB initialized")

    yield

    print("App shutdown")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "CharaAgent API is running"}

@app.get("/characters")
def characters():
    rows = get_all_characters()

    return [
        {
            "id": row["id"],
            "name": row["name"],
            "role": row["role"],
            "tone": row["tone"],
            "personality": row["personality"],
            "speaking_style": row["speaking_style"],
        }
        for row in rows
    ]