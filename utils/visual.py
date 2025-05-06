#
# 청각 장애인
# 텍스트 & 이미지, 음성 x
#
import streamlit as st


# 텍스트 & 이미지 피드백
def text_feedback(message: str, image_path: str | None = None):
    st.markdown(f"### {message}")
    if image_path:
        st.image(image_path, use_column_width=True)


# 선택지 시각적 입력
def visual_prompt(prompt: str, options: list[str]) -> str:
    st.markdown(f"### {prompt}")
    return st.radio("선택하세요 :", options)
