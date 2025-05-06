import streamlit as st

# from pages.main import show_main
from pages import (
    main,
    login,
    register,
    escape_room,
    wizard_duel,
    future_self,
    voice_quiz,
)
from components.db import get_db
from models import Game, GameProgress

# 초기값 설정
if "page" not in st.session_state:
    st.session_state.page = "main"

if "db" not in st.session_state:
    st.session_state["db"] = get_db()

# 라우팅
if st.session_state.page == "main":
    main.show_main()
elif st.session_state.page == "login":
    login.show_login()
elif st.session_state.page == "register":
    register.show_register()
elif st.session_state.page == "escape_room":
    escape_room.show_escape_room()
elif st.session_state.page == "wizard_duel":
    wizard_duel.show_wizard_duel()
elif st.session_state.page == "future_self":
    future_self.show_future_self()
elif st.session_state.page == "voice_quiz":
    voice_quiz.show_voice_quiz()

# def main():
#     show_main()


# if __name__ == "__main__":
#     main()
