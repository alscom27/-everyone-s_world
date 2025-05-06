#
# SQLAlchemy는 코드로 db 데이터를 다룰 수 있게 해줌
# Pydantic은 타입 검증 + 자바의 dto역할을 해줌
#

from sqlalchemy.orm import declarative_base

Base = declarative_base()
