import streamlit as st
import openai
from PIL import Image

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
