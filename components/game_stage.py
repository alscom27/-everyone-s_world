from datetime import datetime
from models.game_stage import GameStage
from models.game_progress import GameProgress
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_room_image(prompt: str):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url


def create_stage_and_update_progress(db, user_id: int, game, user_command: str):
    # 기존 유저 스테이지 조회
    past_stages = (
        db.query(GameStage)
        .filter_by(game_id=game.id, user_id=user_id)
        .order_by(GameStage.stage_number.asc())
        .all()
    )

    stage_number = past_stages[-1].stage_number + 1 if past_stages else 1

    # 이전 스테이지 기록 생성
    stage_history = (
        "\n".join(
            f"[{s.stage_number}단계]: {s.description.strip()}" for s in past_stages[-5:]
        )
        if past_stages
        else "없음"
    )

    prompt = f"""
당신은 방탈출 게임의 마스터입니다.

지금까지의 게임 진행 요약: {stage_history}

현재 게임은 {stage_number}스테이지 입니다.
사용자가 '{user_command}' 행동을 시도했습니다.

아래 지침을 따라 다음 **한 개의 스테이지만** 생성해 주세요:
- 방의 배경 및 분위기 묘사
- 주변의 단서, 퍼즐 또는 인터랙션 설명
- 사용자가 다음에 취할 수 있는 행동 유도

조건:
- 현재 진행중인 스테이지가 몇 번째 스테이지인지 스테이지 x: 형식으로 나타내주세요.
- 행동 유도에는 숫자로 구분지어서 알려줘도 됩니다.
- 이전 내용을 바탕으로 숫자를 입력해도 해당 행동 유도를 실행한 것으로 간주합니다.
- 마지막 스테이지는 **최소 3 스테이지 이후** 등장해야 합니다.
- 마지막 스테이지일 경우에만 탈출 성공 메시지를 포함해주세요.
- 아직 마지막 스테이지가 아니라면 탈출 메시지/성공 문구는 절대 포함하지 마세요.
- **4 스테이지 이상**부터는 사용자의 입력이 매우 적절하고 핵심 퍼즐을 푼 경우에만 마지막 스테이지로 간주하세요.
- 마지막 스테이지는 **10 스테이지를** 넘기지 않습니다.
- 마지막 스테이지에는 행동 문구에 '열쇠를 돌린다', '비밀 통로를 연다', '제단에 주문을 외운다' 등의 **클리어 가능성이 높은 행동 문구를 한 개만 추가해주세요.
- 마지막 스테이지에서 클리어 가능성이 높은 행동 문구 혹은 행동 문구의 번호를 입력했다면 클리어입니다.
- 마지막 스테이지를 클리어하면 반드시 **'탈출에 성공했습니다. 게임 종료.'**라는 단어를 포함시켜 주세요.
"""

    #     - '스테이지 x:'같은 숫자나 단계를 붙이지 마세요.
    # - '1단계', '2단계' 등도 사용하지 마세요.(화

    res = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "너는 방탈출 게임 마스터야. 상황 묘사와 다음 행동 유도를 포함해서 한 개 스테이지만 생성해줘.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    description = res.choices[0].message.content.strip()
    image_url = generate_room_image(description[:100])

    new_stage = GameStage(
        game_id=game.id,
        user_id=user_id,
        stage_number=stage_number,
        description=description,
        image_path=image_url,
        gpt_prompt=prompt,
    )
    db.add(new_stage)
    db.commit()
    db.refresh(new_stage)

    progress = (
        db.query(GameProgress).filter_by(user_id=user_id, game_id=game.id).first()
    )
    if not progress:
        progress = GameProgress(
            user_id=user_id,
            game_id=game.id,
            current_stage_id=new_stage.id,
            last_played_at=datetime.utcnow(),
            game_state_json="{}",
        )
        db.add(progress)
    else:
        progress.current_stage_id = new_stage.id
        progress.last_played_at = datetime.utcnow()

    db.commit()
    return new_stage


def get_current_stage(db, progress: GameProgress):
    return db.query(GameStage).filter_by(id=progress.current_stage_id).first()


def is_game_cleared(stage: dict) -> bool:
    return (
        stage
        and stage["stage_number"] >= 3
        and "탈출에 성공했습니다." in stage["description"]
    )


def reset_game_progress(db, user_id: int, game_id: int):
    progress = (
        db.query(GameProgress).filter_by(user_id=user_id, game_id=game_id).first()
    )
    if progress:
        db.delete(progress)
    db.query(GameStage).filter_by(user_id=user_id, game_id=game_id).delete()
    db.commit()
