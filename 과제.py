import streamlit as st
import openai
from openai import OpenAI

# OpenAI API 키 입력
apikey = st.text_input("API 키를 입력하세요", type="password")

if apikey:
    openai.api_key = apikey

    st.header("음식 메뉴 추천 프로그램")

    # 음식 종류 선택
    cuisine = st.selectbox("어떤 종류의 요리를 원하시나요?", ["한식", "중식", "일식", "양식"])

    # 특정 재료 선택
    ingredient = st.selectbox("특정한 재료가 필요하신가요?", ["고기", "생선", "채소", "상관없음"])

    # 매운 음식 선호 여부
    spicy = st.radio("매운 음식을 좋아하시나요?", ["네", "아니오"])

    # 식이 제한 선택
    dietary_restriction = st.selectbox("특정한 식이 제한이 있으신가요?", ["상관없음", "채식", "글루텐 프리"])

    def recommend_food_via_openai(cuisine, ingredient, spicy, dietary_restriction):
        prompt = f"""
        나는 당신의 요리 추천사입니다. 다음 조건에 맞는 음식을 추천해 주세요.
        - 요리 종류: {cuisine}
        - 특정한 재료: {ingredient}
        - 매운 음식 선호 여부: {spicy}
        - 식이 제한: {dietary_restriction}

        추천 음식:
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 요리 추천사입니다."},
                {"role": "user", "content": prompt}
            ]
        )
        
        recommendation = response.choices[0].message['content'].strip()
        return recommendation

    @st.cache_data()
    def draw(prompt):
        client = OpenAI(api_key=apikey)
        response = client.images.generate(model="dall-e-3", prompt=f'{prompt}와 관련된 음식 메뉴 하나를 그려줘')
        image_url = response.data[0].url
        return image_url

    if st.button("음식 추천 받기"):
        recommendation = recommend_food_via_openai(cuisine, ingredient, spicy, dietary_restriction)
        st.write("추천 음식:", recommendation)

        if st.button("이미지 생성"):
            image_url = draw(recommendation)
            st.image(image_url, caption=recommendation)
else:
    st.warning("API 키를 입력하세요.")
