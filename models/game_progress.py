# 게임 진행도
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base


class GameProgress(Base):
    __tablename__ = "game_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # fk
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    current_stage_id = Column(Integer, ForeignKey("game_stage.id"), nullable=False)
    last_played_at = Column(DateTime, default=datetime.utcnow)
    game_state_json = Column(
        Text, nullable=True
    )  # 게임 진행에 따른 상태정보(인벤토리, 등) json 형식으로 저장할 예정

    user = relationship("User", back_populates="progresses")
    game = relationship("Game", back_populates="progresses")
    game_stage = relationship("GameStage", back_populates="progresses")
