import streamlit as st
from components.auth import authenticate_user
from schemas.user import UserLogin

# from streamlit_extras.switch_page_button import switch_page


def show_login():
    st.title("로그인")
    login_id = st.text_input("아이디", placeholder="아이디")
    password = st.text_input("비밀번호", type="password", placeholder="비밀번호")

    cols = st.columns(2)

    with cols[0]:
        login_btn = st.button("로그인")
    with cols[1]:
        if st.button("회원가입"):
            st.session_state.page = "register"

    # 페이지 초기 진입 시 이게 왜 true인지 도무지 모르겠음...
    if login_btn:
        if not login_id or not password:
            # if (login_id == "" or password == "") and (login_id or password):
            st.warning("아이디와 비밀번호를 모두 입력해주세요.")
            return

        data = UserLogin(login_id=login_id, password=password)
        SessionLocal = st.session_state["db"]
        db = SessionLocal()
        user = authenticate_user(db, data)

        if user:
            st.session_state["user"] = user
            st.success("로그인 성공")
            st.session_state.page = "main"
            st.rerun()
        else:
            st.error("아이디 또는 비밀번호가 일치하지 않습니다.")

    # if st.button("로그인"):
    #     data = UserLogin(login_id=login_id, password=password)
    #     SessionLocal = st.session_state["db"]
    #     db = SessionLocal()
    #     user = authenticate_user(db, data)
    #     if user:
    #         st.session_state["user"] = user
    #         st.success("로그인 성공")
    #         st.session_state.page = "main"
    #     else:
    #         st.error("아이디 또는 비밀번호가 일치하지 않습니다.")
