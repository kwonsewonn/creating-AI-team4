import streamlit as st
from openai import OpenAI
import requests
from bs4 import BeautifulSoup

def draw(prompt):
    response = client.images.generate(model="dall-e-3", prompt= prompt)
    image_url = response.data[0].url
    image = f"![alt text]({image_url})"
    return image

def download_and_save(url, filename):
    rq = requests.get(url)
    soup = BeautifulSoup(rq.text, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    with open(filename,'w') as fo:
        fo.write(text)

apikey = st.text_input("api key를 입력하세요", type="password")
client = OpenAI(api_key=apikey)

st.header("음식 메뉴 추천")
prompti = st.text_input("키워드")

if st.button("start"):
    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f'{prompti}와 관련된 음식 한가지를 추천해주고 그 음식의 레시피도 추천해줘'},
      ]
    )

    r = response.choices[0].message.content
    st.markdown(r)
    img = draw(r)
    st.markdown(img)
    url = "https://blog.naver.com/dodoti/223136463284"
    filename1 = '1.txt'
    download_and_save(url, filename1)
    url = "https://www.gqkorea.co.kr/2022/06/08/%EC%97%AC%EB%A6%84%EC%9D%B4%EB%8B%88%EA%B9%8C-%EB%B6%80%EC%82%B0-%EB%A8%B9%ED%82%B7-%EB%A6%AC%EC%8A%A4%ED%8A%B8-50/"
    filename2 = '2.txt'
    download_and_save(url, filename2)
    url = "https://m.blog.naver.com/perience/223172217155"
    filename3 = '3.txt'
    download_and_save(url, filename3)
    url = "https://livecomfort.tistory.com/entry/%EB%B6%80%EC%82%B0%ED%86%A0%EB%B0%95%EC%9D%B4%EC%97%90%EA%B2%8C-%EC%A0%84%EC%88%98%EB%B0%9B%EC%9D%80-%EB%B6%80%EC%82%B0-%EB%A7%9B%EC%A7%91-%EB%A6%AC%EC%8A%A4%ED%8A%B8TOP20"
    filename4 = '4.txt'
    download_and_save(url, filename4)
    url = "https://tastedongmin.tistory.com/entry/%EB%B6%80%EC%82%B0-%ED%98%84%EC%A7%80%EC%9D%B8-%EB%A7%9B%EC%A7%91-%EB%B8%94%EB%A1%9C%EA%B1%B0%EA%B0%80-%EB%BD%91%EC%9D%80-%EB%B6%80%EC%82%B0-%EB%A7%9B%EC%A7%91-%EB%A6%AC%EC%8A%A4%ED%8A%B8-Best12-1%ED%83%84-2023ver"
    filename5 = '5.txt'
    download_and_save(url, filename5)
    url = "https://blog.naver.com/PostView.naver?blogId=kyungdongbu&logNo=222146667907&parentCategoryNo=&categoryNo=8&viewDate=&isShowPopularPosts=true&from=search"
    filename6 = '6.txt'
    download_and_save(url, filename6)
    url = "https://www.bluer.co.kr/magazine/344"
    filename7 = '7.txt'
    download_and_save(url, filename7)
    url = "https://m.blog.naver.com/dodoti/222014667621"
    filename8 = '8.txt'
    download_and_save(url, filename8)
    url = "https://m.diningcode.com/list.dc?query=%EB%B6%80%EC%82%B0"
    filename9 = '9.txt'
    download_and_save(url, filename9)
    url = "https://www.junsungki.com/magazine/post-detail.do?id=606https://www.junsungki.com/magazine/post-detail.do?id=606"
    filename10 = '10.txt'
    download_and_save(url, filename10)
    filename11 = '11.txt'
    download_and_save(url, filename11)
    url = "https://haeng.kr/%EB%B6%80%EC%82%B0-%EC%B9%B4%ED%8E%98/"
    filename12 = '12.txt'
    download_and_save(url, filename12)
    url = "https://m.blog.naver.com/seosomang/223189360966?isInf=true"
    filename13 = '13.txt'
    download_and_save(url, filename13)
    url = "https://honeytip.kr/432/"

    vector_store = client.beta.vector_stores.create(name="a")
    file_paths = [filename1,filename2]
    file_streams = [open(path, "rb") for path in file_paths]

    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(vector_store_id=vector_store.id, files=file_streams)
    assistant = client.beta.assistants.create(
        instructions="당신은 음식 추천 매니저입니다.", 
        model="gpt-4-turbo-preview", 
        tools=[{"type": "file_search"}],
        tool_resources={
            "file_search":{
                "vector_store_ids": [vector_store.id]
            }
        }
    )

    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user", 
                "content": f'{r}을 하는 식당을 첨부된 파일에서 하나 추천해줘. 만약 없다면 최대한 비슷한 음식을 하는 식당을 쳠부된 파일에서 반드시 무조건 추천해줘',
            }
        ]
    )

    run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)
    thread_messages = client.beta.threads.messages.list(thread.id, run_id=run.id)

    for msg in thread_messages.data:
        st.markdown(f"{msg.role}: {msg.content[0].text.value}")
