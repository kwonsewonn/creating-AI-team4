import streamlit as st
import openai
from PIL import Image
import requests

openai.api_key = "YOUR_OPENAI_API_KEY"

# 세션 상태 클래스 정의
class SessionState:
    def __init__(self):
        self.api_key = None
        self.prompt = None
        self.assistant = None

# 초기화 함수 정의
def initialize():
    state = SessionState()
    return state

# API 키 설정 함수 정의
def set_api_key(state, api_key):
    state.api_key = api_key
    openai.api_key = api_key

# 대화 시작 함수 정의
def start_chat(state):
    state.assistant = openai.ChatCompletion.create(
        model="gpt-4o"
    )

# 사용자 입력을 Assistant에 전달하고 응답을 반환하는 함수 정의
def send_message(state, message):
    if state.assistant:
        state.assistant.append_message(message)
        response = state.assistant.get_next_response()
        return response.choices[0].text.strip()
    else:
        return "Please start the chat first."

# 이미지 생성 함수 정의
def generate_image(prompt, model="dall-e-3"):
    response = openai.Image.create(
        prompt=prompt,
        model=model,
        num_images=1
    )
    image_url = response.images[0].url
    image = Image.open(requests.get(image_url, stream=True).raw)
    return image

# 메인 함수 정의
def main():
    st.title('OpenAI Chatbot with Image Generator')

    # 세션 상태 초기화
    if 'state' not in st.session_state:
        st.session_state.state = initialize()

    # OpenAI API 키 입력
    api_key = st.text_input('Enter your OpenAI API Key:', type="password")
    if st.button('Save API Key'):
        if api_key:
            set_api_key(st.session_state.state, api_key)
            st.success('API Key saved successfully!')

    # DALL-E 이미지 생성
    prompt = st.text_area('Enter your prompt for DALL-E:')
    if st.button('Generate Image'):
        if prompt:
            st.session_state.state.prompt = prompt
            image = generate_image(prompt)
            st.image(image, caption='Generated Image', use_column_width=True)

    # Code Interpreter 기능 추가
    code_input = st.text_area("Input your code here:")
    if st.button("Run Code"):
        code_output = openai.Completion.create(
            engine="davinci-codex",
            prompt=code_input,
            max_tokens=100
        )
        st.code(code_output.choices[0].text)

    # 챗봇 기능 추가
    st.title("OpenAI Assistant Chatbot")

    # 대화 시작 버튼
    if st.button("Start Chat"):
        start_chat(st.session_state.state)
        st.success("Chat started!")

    # 사용자 입력
    user_input = st.text_input("You:", "")

    # 사용자 입력을 Assistant에 전달하고 응답 출력
    if st.button("Send"):
        response = send_message(st.session_state.state, user_input)
        st.write("Assistant:", response)

if __name__ == '__main__':
    main()
