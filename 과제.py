pip install streamlit openai requests beautifulsoup4 geopy folium streamlit-folium

import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static

# Dining Code 웹사이트에서 맛집 데이터를 스크래핑하는 함수
def get_restaurant_data(query):
    url = f"https://www.diningcode.com/list.dc?query={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    restaurants = []
    for item in soup.select('.DcList > .ListItem'):
        name = item.select_one('.Info .Btxt').text
        address = item.select_one('.Info .Stxt').text
        restaurants.append((name, address))

    return restaurants

# 주소를 위도와 경도로 변환하는 함수
def get_coordinates(address):
    geolocator = Nominatim(user_agent="restaurant_locator")
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

# OpenAI API를 사용하여 음식 추천을 받는 함수
def get_food_recommendation(prompt, api_key):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f'{prompt}와 관련된 음식 한가지를 추천해줘'},
        ]
    )
    return response.choices[0].message['content']

st.header("음식 메뉴 추천")

apikey = st.text_input("API key를 입력하세요", type="password")
prompti = st.text_input("키워드")

if st.button("start"):
    if apikey and prompti:
        food_recommendation = get_food_recommendation(prompti, apikey)
        st.markdown(f"추천 음식: {food_recommendation}")

        # 음식 관련 맛집 정보 가져오기
        query = "부경대 " + food_recommendation
        restaurants = get_restaurant_data(query)

        if restaurants:
            st.write(f"'{food_recommendation}'와 관련된 추천 맛집:")

            # 지도 생성
            map_center = (35.1335, 129.1052)  # 부경대 좌표
            m = folium.Map(location=map_center, zoom_start=15)

            for name, address in restaurants:
                st.write(f"- {name}, {address}")
                coordinates = get_coordinates(address)
                if coordinates:
                    folium.Marker(location=coordinates, popup=f"{name}\n{address}").add_to(m)

            # folium 지도를 Streamlit에 표시
            folium_static(m)
        else:
            st.write(f"'{food_recommendation}'와 관련된 추천 맛집이 없습니다.")
    else:
        st.write("API key와 키워드를 입력하세요.")

