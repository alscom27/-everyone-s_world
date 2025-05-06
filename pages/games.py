import streamlit as st
from components.auth import get_user_info
from components.games import list_games
from streamlit_extras.switch_page_button import switch_page
from utils.visual import text_feedback
from utils.voice import text_to_speech, play_audio


def show_game_list():
    user = get_user_info()
    if not user:
        st.warning("로그인이 필요합니다.")
        switch_page("login")
        return

    st.title("게임 목록")
    disability = user.disability_type

    # 게임 목록 불러오기
    db = st.session_state["db"]
    games = list_games(db)

    if disability == "시각" or disability == "지체":
        path = text_to_speech("원하는 게임을 선택해주세요.")
        play_audio(path)

    st.markdown("---")

    for game in games:
        text_feedback(game.title, game.thumbnail_path)
        if st.button(f"{game.title} 시작하기", key=game.id):
            switch_page(game.title)
