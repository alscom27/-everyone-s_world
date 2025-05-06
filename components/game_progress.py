from sqlalchemy.orm import Session
from models.game_progress import GameProgress
from schemas.game_progress import GameProgressCreate, GameProgressUpdate
from models.game_stage import GameStage
from schemas.game_stage import GameStageCreate
from datetime import datetime


# 게임 진행 정보 생성
def create_game_progress(db: Session, data: GameProgressCreate) -> GameProgress:
    progress = GameProgress(
        user_id=data.user_id,
        game_type=data.game_type,
        current_stage=data.current_stage,
        game_state_json=data.game_state_json,
        image_path=data.image_path,
        audio_path=data.audio_path,
        last_played_at=datetime.utcnow(),
    )

    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress


# 게임 진행 정보 조회
def get_game_progress(db: Session, user_id: int, game_type: str) -> GameProgress | None:
    return (
        db.query(GameProgress).filter_by(user_id=user_id, game_type=game_type).first()
    )


# 게임 진행 업데이트
def update_game_progress(
    db: Session, progress: GameProgress, update_data: GameProgressUpdate
) -> GameProgress:
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(progress, key, value)

    progress.last_played_at - datetime.utcnow()
    db.commit()
    db.refresh(progress)
    return progress


# 게임 진행 삭제
def delete_game_progress(db: Session, user_id: int, game_type: str) -> bool:
    progress = (
        db.query(GameProgress).filter_by(user_id=user_id, game_type=game_type).first()
    )
    if not progress:
        return False

    db.delete(progress)
    db.commit()
    return True


# 게임 스테이지 생성
def create_game_stage(db: Session, data: GameStageCreate) -> GameStage:
    stage = GameStage(
        game_id=data.game_id,
        stage_number=data.stage_number,
        description=data.description,
        image_path=data.image_path,
        audio_path=data.audio_path,
    )

    db.add(stage)
    db.commit()
    db.refresh(stage)
    return stage


# 게임 스테이지 불러오기
def get_stages_by_game(db: Session, game_id: int) -> list[GameStage]:
    return (
        db.query(GameStage)
        .filter_by(game_id=game_id)
        .order_by(GameStage.stage_number)
        .all()
    )


# 스테이지 삭제
def delete_stage(db: Session, stage_id: int) -> bool:
    stage = db.query(GameStage).filter_by(id=stage_id).first()
    if not stage:
        return False
    db.delete(stage)
    db.commit()
    return True
