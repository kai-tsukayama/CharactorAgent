from app.models import CharacterReply
from app.repositories.character_repository import get_all_characters
from app.prompts import build_character_prompt
from app.llm import generate_text

def run_character_discussion(user_message: str) -> list[CharacterReply]:
    characters = get_all_characters()[:2]
    replies = []
    previous_replies = []

    for character in characters:
        prompt = build_character_prompt(character, user_message, previous_replies)
        reply_text = generate_text(prompt)

        replies.append(
            CharacterReply(
                character_id= character.id,
                character_name= character.name,
                reply= reply_text
            )
        )

        previous_replies.append(f"{character.name}: {reply_text}")

    return replies

def build_summary(user_message: str, replies: list[CharacterReply]) -> str:
    joined_replies = "\n".join(
        [f"{reply.character_name}: {reply.reply}" for reply in replies]
    )

    prompt = f"""
    以下は、ユーザーの質問に対する複数キャラクターの意見です。

    【ユーザーの質問】
    {user_message}

    【キャラクターたちの意見】
    {joined_replies}

    【あなたの役割】
    あなたは議論のまとめ役です。
    全体の意見を整理して、ユーザーに分かりやすく日本語で短くまとめてください。
    """.strip()

    return generate_text(prompt)