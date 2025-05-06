import streamlit as st
from components.auth import get_user_info
from utils.voice import (
    speech_to_text,
    text_to_speech,
    play_audio,
    record_audio,
    delete_audio_file,
)
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def show_future_self():
    user = get_user_info()
    if not user:
        st.error("로그인이 필요합니다.")
        return

    disability = user.disability_type
    st.title("미래의 나와의 대화")
    st.markdown("### 고민을 말하고 미래의 나에게 조언을 들어보세요!")

    if "dialogue" not in st.session_state:
        st.session_state.dialogue = []

    if disability in ["시각", "지체"]:
        st.subheader("고민을 음성으로 말씀해주세요.")
        if st.button("녹음 시작"):
            audio_path = record_audio(file_name="future.wav", duration=5)
            user_input = speech_to_text(audio_path)
            delete_audio_file(audio_path)

            if not user_input.strip():
                st.warning("음성이 인식되지 않았습니다. 다시 시도해주세요.")
                return

            st.session_state.dialogue.append(("나", user_input))
    else:
        user_input = st.text_input("고민을 입력하세요.")
        if st.button("입력 전송") and user_input:
            st.session_state.dialogue.append(("나", user_input))

    # GPT 응답 생성
    if st.session_state.dialogue and len(st.session_state.dialogue) % 2 == 1:
        with st.spinner("미래의 나가 답변을 준비 중입니다..."):
            messages = [
                {
                    "role": "system",
                    "content": "너는 사용자의 미래 버전이야. 조언을 따뜻하고 진심으로 해줘.",
                }
            ]
            for i, (role, text) in enumerate(st.session_state.dialogue):
                messages.append(
                    {"role": "user" if i % 2 == 0 else "assistant", "content": text}
                )

            gpt_response = client.chat.completions.create(
                model="gpt-4o", messages=messages, temperature=0.7
            )

            reply = gpt_response.choices[0].message.content
            st.session_state.dialogue.append(("미래의 나", reply))

            if disability in ["시각", "지체"]:
                audio_reply = text_to_speech(reply)
                play_audio(audio_reply)
                delete_audio_file(audio_reply)

    st.markdown("---")
    st.subheader("대화 내용")
    for speaker, message in st.session_state.dialogue:
        st.markdown(f"**{speaker}**: {message}")
