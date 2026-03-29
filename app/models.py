from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class Character:
    id: int
    name: str
    role: str
    tone: str
    personality: str
    speaking_style: str

@dataclass
class CharacterReply:
    character_id: int
    character_name: str
    reply: str

class DiscussionRequest(BaseModel):
    user_message: str