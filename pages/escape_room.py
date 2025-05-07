import streamlit as st
from components.auth import get_user_info
from components.db import SessionLocal
from models.games import Game
from models.game_stage import GameStage
from models.game_progress import GameProgress
from datetime import datetime
from utils.voice import (
    speech_to_text,
    text_to_speech,
    play_audio,
    record_audio,
    delete_audio_file,
    analyze_image_with_vision,
)
from components.game_stage import create_stage_and_update_progress, is_game_cleared


def stage_to_dict(stage: GameStage):
    return {
        "id": stage.id,
        "stage_number": stage.stage_number,
        "image_path": stage.image_path,
        "description": stage.description,
    }


def show_escape_room():
    db = SessionLocal()
    user = get_user_info(db, st.session_state["user"].id)
    if not user:
        st.error("로그인이 필요합니다.")
        db.close()
        return

    game = db.query(Game).filter_by(game_type="escape_room").first()
    progress = (
        db.query(GameProgress).filter_by(user_id=user.id, game_id=game.id).first()
    )

    st.title("방탈출")
    st.write(f"사용자 정보 : {user.disability_type} 장애")

    if "game_mode" not in st.session_state:
        st.session_state["game_mode"] = None
    if "current_stage" not in st.session_state:
        st.session_state["current_stage"] = None

    if st.session_state["game_mode"] is None:
        if progress:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("이어하기"):
                    st.session_state["game_mode"] = "continue"
                    st.rerun()
            with col2:
                if st.button("새로하기"):
                    # 먼저 진행 중인 progress 삭제 후 커밋
                    db.delete(progress)
                    db.commit()
                    # 그 다음 외래키 대상인 stage 삭제
                    db.query(GameStage).filter_by(game_id=game.id).delete()
                    db.commit()
                    st.session_state["game_mode"] = "new"
                    st.rerun()
        else:
            if st.button("게임 시작"):
                st.session_state["game_mode"] = "new"
                st.rerun()
        db.close()
        return

    if (
        st.session_state["game_mode"] == "new"
        and st.session_state["current_stage"] is None
    ):
        st.subheader("원하는 방의 테마를 입력하세요:")
        st.caption("예: 고대 이집트의 비밀 사원, 미래 도시 감옥, 유령의 저택 등")

        if user.disability_type in ["시각", "지체"]:
            theme_guide_audio = text_to_speech(
                "원하는 방의 테마를 말씀해주세요. 예를 들어, 유령의 저택, 고대 이집트의 사원 등입니다."
            )
            play_audio(theme_guide_audio)
            delete_audio_file(theme_guide_audio)

            if st.button("테마 말하기 (녹음 시작)"):
                audio_path = record_audio(seconds=5)
                theme = speech_to_text(audio_path)
                delete_audio_file(audio_path)
            else:
                theme = ""
        else:
            theme = st.text_input("테마 입력", key="theme_input")

        if theme:
            stage = create_stage_and_update_progress(db, user.id, game, theme)
            st.session_state["current_stage"] = stage_to_dict(stage)
            st.rerun()
        db.close()
        return

    if (
        st.session_state["game_mode"] == "continue"
        and st.session_state["current_stage"] is None
    ):
        stage = db.query(GameStage).filter_by(id=progress.current_stage_id).first()
        if stage:
            st.session_state["current_stage"] = stage_to_dict(stage)
            st.rerun()
        db.close()
        return

    stage = st.session_state["current_stage"]
    st.image(
        stage["image_path"],
        caption=f"{stage['stage_number']}단계",
        use_container_width=True,
    )
    st.markdown(stage["description"])

    if user.disability_type not in ["시각", "지체"]:
        if st.button("힌트"):
            hint = analyze_image_with_vision(db, game.id, user.id)
            st.markdown(f"**힌트:** {hint}")

    command = ""
    if user.disability_type in ["시각", "지체"]:
        desc_audio = text_to_speech(stage["description"])
        play_audio(desc_audio)
        delete_audio_file(desc_audio)

        guide_audio = text_to_speech(
            "이제 행동을 말씀해주세요. 예를 들어, 책장을 연다."
        )
        play_audio(guide_audio)
        delete_audio_file(guide_audio)

        if st.button("행동 말하기 (녹음 시작)"):
            audio_path = record_audio(seconds=5)
            command = speech_to_text(audio_path)
            delete_audio_file(audio_path)
    else:
        use_voice = st.checkbox("텍스트 대신 음성으로 안내받기")
        if use_voice:
            audio_path = text_to_speech("무엇을 하시겠습니까?")
            play_audio(audio_path)
            delete_audio_file(audio_path)
            if st.button("행동 녹음 시작"):
                audio_path = record_audio(seconds=5)
                command = speech_to_text(audio_path)
                delete_audio_file(audio_path)

        command = st.text_input("무엇을 하시겠습니까?", key="command_input")

    if command:
        st.success(f"입력된 명령: {command}")
        if user.disability_type in ["시각", "지체"] and (
            "힌트" in command or "도움" in command
        ):
            hint = analyze_image_with_vision(db, game.id, user.id)
            st.markdown(f"**힌트:** {hint}")
            hint_audio = text_to_speech(hint)
            play_audio(hint_audio)
            delete_audio_file(hint_audio)
        else:
            stage = create_stage_and_update_progress(db, user.id, game, command)
            st.session_state["current_stage"] = stage_to_dict(stage)
            st.session_state.pop("command_input", None)
            st.rerun()

    if st.button("현재 단계 저장하기"):
        progress = (
            db.query(GameProgress).filter_by(user_id=user.id, game_id=game.id).first()
        )
        if progress:
            progress.current_stage_id = stage["id"]
            progress.last_played_at = datetime.utcnow()
            db.commit()
            st.success("현재 스테이지가 저장되었습니다.")

    if is_game_cleared(stage):
        st.balloons()
        st.success("축하합니다! 방을 탈출하셨습니다.")

    db.close()
