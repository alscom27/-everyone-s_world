# 사용자 관련 모든 기능
# 회원가입/로그인/정보수정/탈퇴/비밀번호 변경

from sqlalchemy.orm import Session  # sqlalchemy 세션, db 연결 및 트랜잭션 수행 객체
from models.user import User
from schemas.user import UserCreate, UserLogin, UserUpdate, PasswordChange

# 해쉬비밀번호
import bcrypt


# 회원가입
def register_user(db: Session, user_data: UserCreate) -> bool:
    # id 중복 체크
    if db.query(User).filter(User.login_id == user_data.login_id).first():
        return False

    # 비밀번호 암호화
    # gensalt() : 비밀번호 해싱에 사용할 소금값을 생성(항상 다른 해시가 생성되게)
    hashed_pw = bcrypt.hashpw(user_data.password.encode(), bcrypt.gensalt())

    # User 객체 생성
    new_user = User(
        login_id=user_data.login_id,
        password=hashed_pw.decode(),
        name=user_data.name,
        age=user_data.age,
        disability_type=user_data.disability_type,
    )

    # db 저장
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return True


# 로그인
def authenticate_user(db: Session, user_data: UserLogin) -> User | None:
    user = db.query(User).filter(User.login_id == user_data.login_id).first()

    if not user:
        return None

    # 비밀번호 확인
    if not bcrypt.checkpw(user_data.password.encode(), user.password.encode()):
        return None

    return user


# # 회원 정보 조회
def get_user_info(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


# 회원 정보 수정
def update_user_info(db: Session, user_id: int, update_data: UserUpdate) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()

    # exclude_unset=True : 입력된 필드만 추출, 없으면 None으로 덮어쓸 수도 있음.
    # setattr() : 해당 속성만 수정
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


# 회원 탈퇴
def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False

    db.delete(user)
    db.commit()
    return True


# 비밀번호 변경
def change_password(db: Session, user_id: int, pw_data: PasswordChange) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False

    # 현재 비밀번호 확인
    if not bcrypt.checkpw(pw_data.current_password.encode(), user.password.encode()):
        return False

    # 새 비밀번호 암호화 저장
    hashed_new_pw = bcrypt.hashpw(pw_data.new_password.encode(), bcrypt.gensalt())
    user.password = hashed_new_pw.decode()

    db.commit()
    return True
