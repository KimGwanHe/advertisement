import streamlit as st
import requests
from pymongo import MongoClient
import pandas as pd

# 프론트엔드

url = 'MongoDB URL'
client = MongoClient(url)
print(client)
database = client['aiproject']
collection = database['ad']

st.title("광고 문구를 서비스앱")
generate_ad_url = "http://127.0.0.1:8000/create_ad"

product_name = st.text_input('제품 이름')
details = st.text_input('주요 내용')
options = st.multiselect("광고 문구의 느낌", options=['기본', '재밌게', '차분하게', '과장스럽게', '참신하게', '고급스럽게', '센스있게', '아름답게'], default=['기본'])

if st.button("광고 문구 생성하기"):
    # pass
    try:
        response = requests.post(generate_ad_url,
             json={
                "product_name": product_name,
                "details": details,
                "tone_and_manner": ", ".join(options)
            })
        ad = response.json()['ad']
        st.success(ad)

        ad_data = {
            '제품 이름': product_name,
            '상세 내용': details,
            '간단 표현': options,
            '광고 문구': ad
        }
        collection.insert_one(ad_data)

        ad_documents = list(collection.find())
        if ad_documents:
            ad_df = pd.DataFrame(ad_documents)
            ad_df = ad_df.drop(columns=['_id'])  # MongoDB의 ObjectId 컬럼 제거
            st.dataframe(ad_df)
        else:
            st.write("저장된 데이터가 없습니다.")

    except:
        st.error(f"연결 실패!")

