import streamlit as st


def select_disability_type():
    if "disability_type" not in st.session_state:
        st.session_state["disability_type"] = None

    st.markdown("### 장애 유형을 선택해주세요.")
    disability_type = st.radio(
        "사용자의 장애 유형을 선택해주세요.",
        ("시각", "청각", "지체", "해당 없음"),
        index=3,
    )

    if st.button("선택 완료"):
        st.session_state["disability_type"] = disability_type
        st.success(f"선택된 장애 유형 : {disability_type}")
