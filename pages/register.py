import streamlit as st
from components.auth import register_user
from schemas.user import UserCreate


def show_register():
    st.title("회원가입")
    login_id = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")
    pw_check = st.text_input("비밀번호 확인", type="password")

    if st.button("비밀번호 확인"):
        if password == pw_check:
            st.success("비밀번호가 일치합니다.")
        else:
            st.error("비밀번호가 일치하지 않습니다.")
            return

    name = st.text_input("이름")
    age = st.number_input("나이", min_value=0, step=1)
    disability_type = st.selectbox("장애 유형", ["해당 없음", "시각", "청각", "지체"])

    if st.button("회원가입"):

        if not login_id or len(login_id) < 4:
            st.error("아이디는 최소 4자 이상이어야 합니다.")
            return
        if not password or len(password) < 6:
            st.error("비밀번호는 최소 6자 이상이어야 합니다.")
            return
        if not name:
            st.error("이름을 입력해주세요.")
            return

        data = UserCreate(
            login_id=login_id,
            password=password,
            name=name,
            age=age,
            disability_type=disability_type,
        )
        SessionLocal = st.session_state["db"]
        db = SessionLocal()
        if register_user(db, data):
            st.success("회원가입 완료! 로그인 페이지로 이동합니다.")
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error("이미 존재하는 아이디입니다.")
