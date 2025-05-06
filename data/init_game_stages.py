# init_game_stages.py

from components.db import SessionLocal
from models.games import Game
from models.game_stage import GameStage


def create_stages():
    db = SessionLocal()

    # 방탈출 예시
    escape_game = db.query(Game).filter_by(game_type="escape_room").first()
    if escape_game:
        stages = [
            GameStage(
                game_id=escape_game.id,
                stage_number=1,
                description="당신은 어두운 방에 갇혀 있습니다. 불빛 하나가 희미하게 보입니다.",
                gpt_prompt="어두운 방에서 첫 단서를 찾기 위해 할 행동은?",
            ),
            GameStage(
                game_id=escape_game.id,
                stage_number=2,
                description="책상 위에 수상한 열쇠가 보입니다.",
                gpt_prompt="열쇠를 어떻게 사용할 것인가요?",
            ),
        ]
        db.add_all(stages)

    # 다른 게임도 비슷하게 추가 가능

    db.commit()
    db.close()
    print("스테이지 데이터 삽입 완료")


if __name__ == "__main__":
    create_stages()
