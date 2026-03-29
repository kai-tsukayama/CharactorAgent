from dataclasses import dataclass

@dataclass
class Character:
    id: int
    name: str
    role: str
    tone: str
    personality: str
    speaking_style: str
    