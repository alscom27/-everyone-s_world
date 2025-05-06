import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# from models.base import Base

# 테이블 모델 import
from models.base import Base
from models.user import User
from models.games import Game
from models.game_progress import GameProgress
from models.game_stage import GameStage
from data.init_games import init_games


# .env 파일 불러오기
load_dotenv()

# 환경변수에서 db 정보 읽기
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# sqlalchemy 엔진 생성 (mysql 연결 문자열)
DB_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print("========================")
engine = create_engine(DB_URL, echo=True)  # echo=True : sql문 출력

# 세션 팩토리 만들기
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 테이블 생성 (처음 한 번만 실행)
def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    init_games()
    print("========================")


def get_db():
    return SessionLocal
