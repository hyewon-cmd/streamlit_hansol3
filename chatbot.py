import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="GPT-4o-mini 챗봇", page_icon="🤖")
st.title("🤖 GPT-4o-mini 챗봇")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 사이드바
with st.sidebar:
    st.header("설정")
    if st.button("대화 초기화"):
        st.session_state.messages = []
        st.rerun()

# 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 추가 및 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # GPT 응답 생성
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
