from components.db import SessionLocal, init_db
from components.game_progress import (
    create_game_progress,
    get_game_progress,
    update_game_progress,
    delete_game_progress,
)
from components.auth import UserCreate, register_user
from schemas.game_progress import GameProgressCreate, GameProgressUpdate
from models.user import User
import json

# db 초기화
init_db()
db = SessionLocal()

# 테스트
line = "-" * 5

# 회원가입 테스트
print(f"{line} 회원가입 테스트 {line}")
new_user = UserCreate(
    login_id="tester",
    password="123456",
    name="김준선",
    age=29,
    disability_type="미각",
)
result = register_user(db, new_user)
print("가입 성공" if result else "가입 실패")

# 회원조회
user = db.query(User).filter_by(login_id="tester").first()

user_id = user.id
game_type = "escape_room"
print(f"{line} 게임 진행 생성 테스트 {line}")
create_data = GameProgressCreate(
    user_id=user_id,
    game_type=game_type,
    current_stage=1,
    game_state_json=json.dumps({"inventory": [], "door_unlocked": False}),
    image_path="assets/images/escape1.png",
    audio_path="assets/audio/escape2.mp3",
)
progress = create_game_progress(db, create_data)
print("생성 완료:", progress.id)

print(f"{line} 게임 진행 조회 테스트 {line}")
fetched = get_game_progress(db, user_id, game_type)
print("조회 결과 :", fetched.current_stage)

print(f"{line} 게임 진행 수정 테스트 {line}")
update_data = GameProgressUpdate(current_stage=2)
updated = update_game_progress(db, fetched, update_data)
print("수정된 스테이지 :", updated.current_stage)

print(f"{line} 게임 진행 삭제 테스트 {line}")
deleted = delete_game_progress(db, user_id, game_type)
print("삭제 성공 여부 :", deleted)

db.close()
