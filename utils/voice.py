#
# 시각장애인 및 손이 불편한 사용자를 위한 음성 안내 기능
# 음성 -> 텍스트 -> 음성
#
import os
from openai import OpenAI
from dotenv import load_dotenv
import uuid
import streamlit as st
import sounddevice as sd
from scipy.io.wavfile import write

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


# 음성 -> (S 텍스트 변환TT)
def speech_to_text(audio_file_path: str) -> str:
    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file
        )
    return transcription.text


# 텍스트 -> 음성 응답 (TTS)
def text_to_speech(text: str, save_dir: str = "assets/audio") -> str:
    # 저장 디렉토리 생성
    os.makedirs(save_dir, exist_ok=True)

    # 고유 파일 이름 생성
    # .hex : 16진수 문자열 변환
    filename = f"voice_{uuid.uuid4().hex}.mp3"
    file_path = os.path.join(save_dir, filename)

    # tts 기능
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text,
    )

    # 응답된 음성 데이터를 파일로 저장
    with open(file_path, "wb") as f:
        f.write(response.content)

    return file_path


# 저장된 음성 파일 재생
def play_audio(audio_path: str):
    audio_file = open(audio_path, "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")
    audio_file.close()


# 음성 파일 삭제
def delete_audio_file(path: str):
    try:
        os.remove(path)
    except Exception as e:
        print("음성 파일 삭제 실패 :", e)


# 음성 입력
# fs : 샘플링 레이트 (16KHz)
def record_audio(seconds: int = 5, fs: int = 16000) -> str:
    st.info(f"{seconds}초간 음성을 녹음합니다.")
    try:
        recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype="int16")
        sd.wait()
    except Exception as e:
        st.error(f"녹음 실패 : {e}")
        return ""

    file_name = f"temp_{uuid.uuid4().hex}.wav"
    file_path = os.path.join("assets", "audio", file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    write(file_path, fs, recording)
    st.success("녹음 완료")
    return file_path
