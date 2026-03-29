from app.models import CharacterReply
from app.repositories.character_repository import get_all_characters
from app.prompts import build_character_prompt
from app.llm import generate_text

def run_character_discussion(user_message: str) -> list[CharacterReply]:
    characters = get_all_characters()

    replies = []

    for character in characters:
        prompt = build_character_prompt(character, user_message)
        reply_text = generate_text(prompt)

        replies.append(
            CharacterReply(
                character_id= character.id,
                character_name= character.name,
                reply= reply_text
            )
        )

    return replies