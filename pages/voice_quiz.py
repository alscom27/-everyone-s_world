import streamlit as st
from components.auth import get_user_info
from utils.voice import (
    text_to_speech,
    play_audio,
    record_audio,
    speech_to_text,
    delete_audio_file,
)
import random


# 퀴즈 문제 (예시)
QUIZ_DATA = [
    {"character": "아이언맨", "hint": "나는 부자이고, 슈트를 입고 하늘을 날아."},
    {"character": "해리포터", "hint": "나는 호그와트에서 마법을 배워."},
    {"character": "피카츄", "hint": "찌릿찌릿! 나는 전기를 쓰는 귀여운 포켓몬이야."},
]


def show_voice_quiz():
    user = get_user_info()
    if not user:
        st.error("로그인이 필요합니다.")
        return

    disability = user.disability_type
    st.title("음성 연기 퀴즈")

    quiz = random.choice(QUIZ_DATA)

    # 힌트를 음성으로 제공 (시각 또는 지체 장애인)
    if disability in ["시각", "지체"]:
        st.markdown("힌트를 음성으로 듣고 캐릭터를 맞혀보세요!")
        audio_path = text_to_speech(quiz["hint"])
        play_audio(audio_path)
        delete_audio_file(audio_path)

        if st.button("정답 녹음 시작"):
            path = record_audio(file_name="voice_quiz.wav", duration=4)
            answer = speech_to_text(path)
            delete_audio_file(path)
            st.markdown(f"당신의 대답: {answer}")
            if quiz["character"] in answer:
                st.success("정답입니다!")
            else:
                st.error(f"오답입니다. 정답은 {quiz['character']}였습니다.")

    else:
        st.markdown("힌트: ")
        st.info(quiz["hint"])
        answer = st.text_input("누구일까요?")
        if answer:
            if quiz["character"] in answer:
                st.success("정답입니다!")
            else:
                st.error(f"오답입니다. 정답은 {quiz['character']}였습니다.")
