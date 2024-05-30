import streamlit as st
import openai
from PIL import Image
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

if __name__ == '__main__':
    main()


class ConversationThread:
    def __init__(self):
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

    def clear_messages(self):
        self.messages = []

    def get_latest_message(self):
        return self.messages[-1] if self.messages else None


if "messages" not in st.session_state: 
 st.session_state.messages = [] 
# 저장한 메시지 사용자/응답 구분해서 보여주기
for msg in st.session_state.messages: 
 with st.chat_message(msg["role"]): 
 st.markdown(msg["content"])


if prompt := st.chat_input("What is up?"): 
 # 사용자 메시지 보여주기
 st.chat_message("user").markdown(prompt) 
 # 메모리에 사용자 메시지 저장
 st.session_state.messages.append({"role": "user", "content": prompt}) 
 # Assistant API Thread의 마지막 Message 가져오는 기능 추가 필요
 response = f"Echo: {prompt}" 
 # LLM 응답 보여주기
 with st.chat_message("assistant"): 
 st.markdown(response) 
 # 메모리에 LLM 응답 저장
 st.session_state.messages.append({"role": "assistant", "content": response})

# 대화 스레드 생성
conversation_thread = ConversationThread()

# OpenAI Assistant 생성
assistant = openai.Assistant.create(
    model="gpt-4o",
    messages=conversation_thread.messages
)

# 사용자 입력/응답 UI
st.title("OpenAI Assistant 챗봇")

# 사용자 입력 받기
user_input = st.text_input("사용자 입력")

# 사용자 입력을 스레드에 추가
if st.button("전송"):
    conversation_thread.add_message({"role": "user", "content": user_input})

# 대화 실행 및 응답 출력
if st.button("Run"):
    assistant.append_message(user_input)
    assistant_response = assistant.message()
    conversation_thread.add_message({"role": "assistant", "content": assistant_response["choices"][0]["message"]["content"]})
    st.text_area("Assistant 응답", value=assistant_response["choices"][0]["message"]["content"])

# Clear 버튼
if st.button("Clear"):
    conversation_thread.clear_messages()
    assistant.reset()

# 대화 종료 버튼
if st.button("대화 종료"):
    conversation_thread = None
    assistant = None
