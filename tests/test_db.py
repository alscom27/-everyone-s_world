from components.db import SessionLocal
from sqlalchemy import text


def test_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))  # db 접속이 되는지만 확인
        print("db 연결 성공")
    except Exception as e:
        print("db 연결 실패", e)
    finally:
        db.close()


if __name__ == "__main__":
    test_connection()
