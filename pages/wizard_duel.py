import streamlit as st
from components.auth import get_user_info
from utils.voice import record_audio, speech_to_text, text_to_speech, play_audio
from openai import OpenAI
from dotenv import load_dotenv
import os

# 환경 변수 로딩 및 OpenAI 클라이언트 초기화
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# GPT 응답 생성 함수
def gpt_response(prompt: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "넌 강력한 마법사야. 사용자의 공격 주문에 반응하고 마법 전투를 이어가. 짧게 말해.",
        },
        {"role": "user", "content": prompt},
    ]
    res = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.9,
    )
    return res.choices[0].message.content


# 마법사와의 대결 페이지
def show_wizard_duel():
    user = get_user_info()
    if not user:
        st.error("로그인이 필요합니다.")
        return

    st.title("🧙 마법사와의 대결")
    disability = user.disability_type

    if disability in ["시각", "지체"]:
        st.markdown("## 마법 주문을 말해주세요!")
        seconds = st.slider("녹음 시간 선택", 2, 10, 4)
        if st.button("녹음 시작"):
            audio_path = record_audio(seconds)
            with st.spinner("음성 인식 중..."):
                prompt = speech_to_text(audio_path)
            st.success(f"인식된 주문: {prompt}")
            with st.spinner("GPT와 마법사 응답 중..."):
                reply = gpt_response(prompt)
            st.markdown(f"마법사: {reply}")
            audio_reply = text_to_speech(reply)
            play_audio(audio_reply)

    elif disability == "청각":
        st.markdown("## 마법 주문을 텍스트로 입력해주세요")
        prompt = st.text_input("마법 주문:")
        if st.button("마법 시전"):
            with st.spinner("GPT 응답 중..."):
                reply = gpt_response(prompt)
            st.markdown(f"마법사: {reply}")

    else:
        st.warning("알 수 없는 장애 유형입니다. 관리자에게 문의하세요.")
