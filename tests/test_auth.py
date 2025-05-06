from components.db import SessionLocal
from components.auth import (
    register_user,
    authenticate_user,
    update_user_info,
    delete_user,
    change_password,
)

from schemas.user import UserCreate, UserLogin, UserUpdate, PasswordChange


def user_all_tests():
    line = "-" * 5
    db = SessionLocal()

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

    # 로그인 테스트
    print(f"{line} 로그인 테스트 {line}")
    login_result = authenticate_user(
        db, UserLogin(login_id="tester", password="123456")
    )
    if login_result:
        print("로그인 성공 :", login_result.name)
        user_id = login_result.id
    else:
        print("로그인 실패")
        return

    # 회원정보 수정 테스트
    print(f"{line} 회원 정보 수정 테스트 {line}")
    update_result = update_user_info(db, user_id, UserUpdate(name="김준순"))
    if update_result:
        print("수정 성공 :", update_result.name)
    else:
        print("수정 실패")

    # 비밀번호 변경 테스트
    print(f"{line} 비밀번호 변경 테스트 {line}")
    pw_changed = change_password(
        db, user_id, PasswordChange(current_password="123456", new_password="654321")
    )
    print("비밀번호 변경 성공" if pw_changed else "비밀번호 변경 실패")

    # 회원 탈퇴 테스트
    print(f"{line} 회원 탈퇴 테스트 {line}")
    delete_result = delete_user(db, user_id)
    print("탈퇴 성공" if delete_result else "탈퇴 실패")

    db.close()


if __name__ == "__main__":
    user_all_tests()
