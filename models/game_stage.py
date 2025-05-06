from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class GameStage(Base):
    __tablename__ = "game_stage"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(
        Integer, ForeignKey("games.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    stage_number = Column(Integer, nullable=False)
    image_path = Column(Text)
    audio_path = Column(Text)
    description = Column(Text)
    gpt_prompt = Column(Text)

    game = relationship("Game", back_populates="game_stage")
    user = relationship("User", back_populates="game_stage")
    progresses = relationship("GameProgress", back_populates="game_stage")
