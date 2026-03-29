from fastapi import FastAPI
from app.db import init_db, seed_characters
from app.repositories.character_repository import get_all_characters
from contextlib import asynccontextmanager
from app.models import DiscussionRequest
from app.agent import run_character_discussion, build_summary
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_characters()
    print("DB initialized")

    yield

    print("App shutdown")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "CharaAgent API is running"}

@app.get("/characters")
def characters():
    rows = get_all_characters()

    return [
        {
            "id": chara.id,
            "name": chara.name,
            "role": chara.role,
            "tone": chara.tone,
            "personality": chara.personality,
            "speaking_style": chara.speaking_style
        }
        for chara in rows
    ]

@app.post("/discussion")
def discussion(request: DiscussionRequest):
    replies = run_character_discussion(request.user_message)
    summary = build_summary(request.user_message, replies)

    return {
        "user_message": request.user_message,
        "replies": [
            {
                "character_id": reply.character_id,
                "character_name": reply.character_name,
                "reply": reply.reply
            }
            for reply in replies
        ],
        "summary": summary
    }