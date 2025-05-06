# from components.db import SessionLocal # 서로 계속 불러오는 순환 참조 일어남
from models.games import Game
from datetime import datetime


def init_games():
    from components.db import SessionLocal

    session = SessionLocal()

    games = [
        {
            "game_type": "escape_room",
            "title": "방 탈출",
            "description": "단서를 찾아 방을 탈출하세요!",
            "thumbnail_path": "assets/images/escape_thumbnail.jpg",
            "age_limit": 10,
        },
        {
            "game_type": "wizard_duel",
            "title": "마법사와의 대결",
            "description": "마법사를 상대로 마법 주문을 외쳐 전투를 벌이는 게임입니다.",
            "thumbnail_path": "assets/images/wizard_thumbnail.jpg",
            "age_limit": 10,
        },
        {
            "game_type": "future_self",
            "title": "미래의 나",
            "description": "미래의 나와 대화하며 진로를 탐색하는 게임",
            "thumbnail_path": "assets/images/future_thumbnail.jpg",
            "age_limit": 12,
        },
        {
            "game_type": "voice_quiz",
            "title": "음성 연기 퀴즈",
            "description": "음성 힌트를 듣고 캐릭터를 맞히는 퀴즈 게임",
            "thumbnail_path": "assets/images/voice_quiz_thumbnail.jpg",
            "age_limit": 8,
        },
    ]

    for g in games:
        existing = session.query(Game).filter_by(game_type=g["game_type"]).first()
        if not existing:
            new_game = Game(**g)
            session.add(new_game)

    session.commit()
    session.close()


if __name__ == "__main__":
    init_games()
    print("게임 초기화 완료")
