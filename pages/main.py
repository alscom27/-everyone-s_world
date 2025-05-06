import streamlit as st

# from components.auth import get_user_info
from utils.voice import play_audio, text_to_speech, speech_to_text
from utils.visual import text_feedback
from models.games import Game
from components.db import SessionLocal


def show_main():
    st.set_page_config(
        page_title="Everyone's World",
        layout="wide",
        # menu_items={"Get help": None, "Report a bug": None, "About": None},
        initial_sidebar_state="collapsed",
    )
    user = st.session_state.get("user")

    # if "btn_clicked" not in st.session_state:
    #     st.session_state.btn_clicked = False

    # 헤더
    with st.container():
        cols = st.columns([1, 4, 4, 4, 4, 4, 4])

        with cols[1]:
            if st.button("공지 사항"):
                # st.switch_page("notice")
                st.session_state.page = "notice"
        with cols[2]:
            if st.button("게임 목록"):
                # st.switch_page("games")
                st.session_state.page = "games"

        with cols[3]:
            if st.button("키즈 놀이터"):
                # st.switch_page("kids")
                st.session_state.page = "kids"
        with cols[4]:
            if st.button("커뮤니티"):
                # st.switch_page("comunity")
                st.session_state.page = "comunity"
        with cols[5]:
            if st.button("마이 페이지"):
                # st.switch_page("mypage")
                st.session_state.page = "mypage"

        if user:
            with cols[6]:
                col_user_id, col_logout = st.columns(2)
                col_user_id.markdown(f"{user.login_id}")
                if col_logout.button("로그아웃"):
                    st.session_state["user"] = None
                    st.rerun()
        else:
            with cols[6]:
                col_login, col_register = st.columns(2)
                if col_login.button("로그인"):
                    # switch_page("login")
                    st.session_state.page = "login"
                if col_register.button("회원가입"):
                    # switch_page("register")
                    st.session_state.page = "register"

    st.markdown("---")

    st.image("assets/images/banner.jpg", use_container_width=True)

    st.markdown("---")
    st.subheader("BEST 게임")

    db = SessionLocal()
    games = (
        db.query(Game).order_by(Game.id).limit(5).all()
    )  # 게임 데이터에서 가져오기 ex.플레이 횟수 가장 많은 순위 5개, 현재는 그냥 있는거중 5개 제한으로 불러옴..

    game_cols = st.columns(len(games))

    for i, game in enumerate(games):
        with game_cols[i]:
            st.image(
                game.thumbnail_path,
                caption=game.title,
                use_container_width=True,
            )
            if st.button(game.title, key=f"game_{i}"):
                if not user:
                    st.warning("로그인이 필요합니다.")
                    # switch_page("login")
                    st.session_state.page = "login"
                    st.rerun()
                else:
                    st.success(f"{game.title} 게임으로 이동합니다.")
                    # switch_page(f"{game}_page")
                    st.session_state.page = f"{game.game_type}"
                    st.rerun()

    db.close()
