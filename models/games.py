from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    game_type = Column(String(50), unique=True, nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    thumbnail_path = Column(String(255))
    age_limit = Column(Integer, nullable=True)

    game_stage = relationship("GameStage", back_populates="game", cascade="all, delete")
    progresses = relationship(
        "GameProgress", back_populates="game", cascade="all, delete"
    )
