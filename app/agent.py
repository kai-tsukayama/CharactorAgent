from app.models import CharacterReply
from app.repositories.character_repository import get_all_characters

def build_reply_by_character(character, user_message: str) -> str:
    return (
        f"{character.name}です。"
        f"私は{character.role}として答えると、"
        f"『{user_message}』については、"
        f"{character.personality}という視点から考えるのが大切です。"
        f"話し方としては {character.speaking_style} のような雰囲気になります。"
    )

def run_character_discussion(user_message: str) -> list[CharacterReply]:
    characters = get_all_characters()

    replies = [
        CharacterReply(
            character_id=character.id,
            character_name=character.name,
            reply=build_reply_by_character(character, user_message)
        )
        for character in characters
    ]

    return replies