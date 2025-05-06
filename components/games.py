from sqlalchemy.orm import Session
from models.games import Game
from schemas.games import GameCreate, GameUpdate


def create_game(db: Session, data: GameCreate) -> Game:
    game = Game(
        game_type=data.game_type,
        title=data.title,
        description=data.description,
        thumbnail_path=data.thumbnail_path,
        age_limit=data.age_limit,
    )

    db.add(game)
    db.commit()
    db.refresh(game)
    return game


def get_game(db: Session, game_id: int) -> Game | None:
    return db.query(Game).filter(Game.id == game_id).first()


def list_games(db: Session) -> list[Game]:
    return db.query(Game).all()


def updata_game(db: Session, game_id: int, update_data: GameUpdate) -> Game | None:
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        return None

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(game, key, value)

    db.commit()
    db.refresh(game)
    return game


def delete_game(db: Session, game_id: int) -> bool:
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        return False

    db.delete(game)
    db.commit()
    return True
