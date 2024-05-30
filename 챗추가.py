import streamlit as st
import openai
from PIL import Image
import requests

openai.api_key = ""

class SessionState:
    def __init__(self):
        self.api_key = None
        self.prompt = None

def initialize():
    state = SessionState()
    return state

def set_api_key(state, api_key):
    state.api_key = api_key
    openai.api_key = api_key

def set_prompt(state, prompt):
    state.prompt = prompt

@st.cache(allow_output_mutation=True)
def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        model="text-dalle-003", 
        num_images=1  
    )
    image_url = response.images[0].url
    image = Image.open(requests.get(image_url, stream=True).raw)
    return image

def chat_interface():
    st.title("Chat with OpenAI Assistant")

    # 채팅 스레드 초기화
    if 'chat_thread' not in st.session_state:
        st.session_state.chat_thread = ChatThread()

    # 채팅 스레드 생성
    if st.button("Start Chat"):
        st.session_state.chat_thread.create_assistant()
        st.success("Chat started!")

    # 사용자 입력 받기
    user_input = st.text_input("You:", "")

    # 사용자 입력을 스레드에 추가
    if st.button("Send"):
        st.session_state.chat_thread.add_message({"role": "user", "content": user_input})

    # 채팅 실행
    if st.button("Run"):
        if st.session_state.chat_thread.assistant:
            response = st.session_state.chat_thread.assistant.messages[-1].get("content", "")
            st.write("Assistant:", response)
        else:
            st.error("Chat not started yet!")

    # 채팅 스레드 초기화
    if st.button("Clear"):
        st.session_state.chat_thread.clear_thread()
        st.session_state.chat_thread.create_assistant()
        st.success("Chat cleared!")

    # 채팅 나가기
    if st.button("Exit Chat"):
        st.session_state.chat_thread.clear_thread()
        st.session_state.chat_thread.delete_assistant()
        st.success("Chat exited!")

def main():
    st.title('DALL-E Image Generator')

    if 'state' not in st.session_state:
        st.session_state.state = initialize()

    api_key = st.text_input('Enter your OpenAI API Key:', type="password")
    if st.button('Save API Key'):
        if api_key:
            set_api_key(st.session_state.state, api_key)
            st.success('API Key saved successfully!')

    prompt = st.text_area('Enter your prompt for DALL-E:')
    if st.button('Generate Image'):
        if prompt:
            set_prompt(st.session_state.state, prompt)
            st.success('Prompt saved successfully!')

    if st.session_state.state.prompt:
        image = generate_image(st.session_state.state.prompt)
        st.image(image, caption='Generated Image', use_column_width=True)

    chat_interface()

if __name__ == '__main__':
    main()
