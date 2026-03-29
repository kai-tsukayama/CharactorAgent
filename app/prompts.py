from app.models import Character

def build_character_prompt(
        character: Character,
        user_message: str,
        previous_replies: list[str]
        ) -> str:
    
    history_text = "\n".join(previous_replies) if previous_replies else "まだ他のキャラクターの発言はありません。"

    return f"""
    あなたは以下の[# 特性]を持つキャラクターになりきって、[# ルール]に従った状態で[# ユーザーの質問]に答えてください。

    【# 特性】
    - キャラクター名: {character.name}
    - 役割: {character.role}
    - 性格: {character.personality}
    - 口調: {character.tone}
    - 話し方: {character.speaking_style}
    - これまでの他のキャラクターの発言: {history_text}

    【" ルール】
    - 必ずこのキャラクターらしく日本語で答えてください
    - 120〜180文字くらいで簡潔に答えてください
    - ユーザーの質問に対して、自分の立場から意見を述べてください
    - 他のキャラクターの発言があれば、それを踏まえて意見を述べてください

    【# ユーザーの質問】
    {user_message}
    """.strip()