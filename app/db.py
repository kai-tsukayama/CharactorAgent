import sqlite3
from pathlib import Path

DB_PATH = Path("data/chara_agent.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            tone TEXT NOT NULL,
            personality TEXT NOT NULL,
            speaking_style TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()

def seed_characters():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as count FROM characters")
    row = cursor.fetchone()

    if row["count"] == 0:
        characters = [
            (
                "理論派の博士",
                "論理的に考える解説役",
                "落ち着いていて丁寧",
                "論理重視で、根拠や理由を明確にする",
                "〜じゃ、〜と考んがえることが理想よのう、〜じゃよ"
            ),
             (
                "テンションの高いのアーティスト",
                "感覚や雰囲気から意見を出す役",
                "柔らかく感覚的",
                "雰囲気や世界観を大切にする",
                "〜最高だぜ！！！、〜が想像は爆発だ、〜の予感がするぜぃ"
            ),
            (
                "現実派で批判的な社長",
                "実現性やコストを考え、基本的に全ての意見を木っ端みじんに否定する役",
                "端的で現実的で論破",
                "実用性重視で、成果につながるかを考える",
                "結局、〜が大事です、実務では〜です、考えが甘い！！、幼稚な考えだな"
            ),
            (
                "精神年齢が5歳の発明家",
                "新しい発想を出す役",
                "前向きでワクワクし、常識を一切考えない発現をする",
                "新規性重視で、既存の枠にとらわれない",
                "なんで～？、どうして～？、～だったらいいじゃん、すれば～？"
            ),
            (
                "ツッコミ役の中二病",
                "場を和ませつつ鋭い視点を出すが、性格が中二病",
                "軽快で親しみやすい",
                "冗談を交えつつ本質も突く",
                "いやそれ面白いけど、〜、でも実は〜"
            )
        ]

        cursor.executemany(
                """
                INSERT INTO characters (
                name, role, tone, personality, speaking_style
                ) VALUES (?, ?, ?, ?, ?)
                """, characters
            )
        print("Character seed data inserted")
    else:
        print("Characters already exist, skipping seed")
    conn.commit()
    conn.close()
