import streamlit as st
import openai

# OpenAI API 키 설정 (환경 변수 또는 직접 입력)
openai.api_key = 'YOUR_OPENAI_API_KEY'

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

def main():
    st.title("음식 추천 프로그램")
    
    # 질문 1: 음식 종류
    cuisine = st.selectbox("어떤 종류의 요리를 원하시나요?", ["한식", "중식", "일식", "양식"])
    
    # 질문 2: 재료
    ingredient = st.selectbox("특정한 재료가 필요하신가요?", ["고기", "생선", "채소", "상관없음"])
    
    # 질문 3: 매운 음식
    spicy = st.radio("매운 음식을 좋아하시나요?", ["네", "아니오"])
    
    # 질문 4: 식이 제한
    dietary_restriction = st.selectbox("특정한 식이 제한이 있으신가요?", ["상관없음", "채식", "글루텐 프리"])

    if st.button("음식 추천 받기"):
        recommendation = recommend_food_via_openai(cuisine, ingredient, spicy, dietary_restriction)
        st.write("추천 음식:", recommendation)

if __name__ == "__main__":
    main()
