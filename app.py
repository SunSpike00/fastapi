import streamlit as st
import pandas as pd
import requests

# 프론트엔드

# '''
# if st.button("광고 문구 생성하기"):
#     try:
#         response = requests.post(url,
#         json={
#             "product_name": product_name,
#             "details": details,
#             "tone_and_manner": options
#         })
#     except:
#         st.error("연결 실패!")
# '''

st.title("광고 문구를 생성 해주는 앱")
generate_ad_url = "http://127.0.0.1:8000/create_ad"

product_name = st.text_input('제품 이름')
details = st.text_input('주요 내용')

options = st.multiselect("광고 문구의 느낌", ['기본', '재밌게', '차분하게', '과장스럽게', '참신하게', '고급스럽게', '센스있게', '아름답게'], default=['기본'])

if st.button("광고문구 생성하기"):
    try:
        response = requests.post(
            generate_ad_url,
            json={"product_name": product_name,
                  "details": details,
                  "tone_and_manner": ", ".join(options)})

        ad = response.json()['ad']
        st.success(ad)

        item_log = response.json()['json_data']
        df = pd.DataFrame(item_log)
        df.columns = ['제품명', '주요 내용', '광고 문구의 느낌', '광고 내용 결과']
        st.table(df)
    except:
        st.error("연결 실패!")
