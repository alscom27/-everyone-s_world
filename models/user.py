from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime


# 베이스를 상속해서 테이블 정의
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)  # pk
    login_id = Column(String(50), unique=True, nullable=False)  # 로그인 id
    password = Column(String(255), nullable=False)  # 비밀번호
    name = Column(String(50), nullable=False)  # 사용자 이름
    age = Column(Integer, nullable=False)  # 나이
    disability_type = Column(String(50), nullable=False)  # 불편한 타입

    # 데이터 생성 시간(utcnow : 서버 지역 상관없이 국제 표준시간 기준으로 기록)
    created_at = Column(DateTime, default=datetime.utcnow)
    # 수정 시간
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    progresses = relationship("GameProgress", back_populates="user")
    game_stage = relationship("GameStage", back_populates="user")
