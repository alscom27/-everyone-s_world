# validation

#
# BaseModel : 모든 pydantic 스키마는 이걸 상속해야함.
# Field() : 필드에 기본값, 설명, 제약조건 등을 설정
# Optional : 값이 없어도 되는 필드를 정의할 때 사용.
#
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


#
# Field(...) : 필수 입력 필드
# ge=0 : 음수 나의 방지
#
class UserCreate(BaseModel):
    login_id: str = Field(..., min_length=4, max_length=20)
    password: str = Field(..., min_length=6)
    name: str = Field(..., min_length=1, max_length=20)
    age: int = Field(..., ge=0)
    disability_type: str = Field(..., min_length=1)


class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    disability_type: Optional[str] = None


class UserLogin(BaseModel):
    login_id: str
    password: str


class PasswordChange(BaseModel):
    current_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)


class UserOut(BaseModel):
    id: int
    login_id: str
    name: str
    age: int
    disability_type: str
    created_at: datetime
    updated_at: datetime

    # db에서 가져온 user 객체를 json으로 응답할 때 사용
    # orm_mode = True이 있어야 sqlalchemy 모델 기반으로 자동 변환 가능
    # orm_mode : pydantic v1버전 -> from_attributes = True : v2버전
    class Config:
        from_attributes = True
