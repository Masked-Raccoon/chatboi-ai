import streamlit as st
import requests

# Streamlit secrets 사용
AIRTABLE_API_KEY = st.secrets["AIRTABLE_API_KEY"]
AIRTABLE_BASE_ID = st.secrets["AIRTABLE_BASE_ID"]
AIRTABLE_TABLE_NAME = st.secrets["AIRTABLE_TABLE_NAME"]

HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json"
}

# 태그 매핑
category_map = {
    "동영상 생성": "video-gen",
    "챗봇(글쓰기)": "writing",
    "이미지 생성": "image-gen",
    "이미지 편집": "image-edit",
    "회의/기록": "meeting",
    "AI 아바타": "avatar",
    "3D 생성": "3d-model",
    "연구 및 리서치": "research",
    "AI 모델": "model",
    "자동화": "automation",
    "코드": "code",
    "노코드 개발": "nocode",
    "PPT": "presentation",
    "리서치": "market-research",
    "음악 생성": "music",
    "웹페이지 제작": "website"
}

tag_map = {
    "쉬운 거": "easy",
    "적당한 난이도": "intermediate",
    "전문가 수준": "advanced",
    "무료": "free",
    "무료 체험": "free-trial",
    "유료": "paid"
}

# Streamlit UI
def main():
    st.title("🤖 나에게 맞는 AI 툴 추천기")

    category = st.selectbox("어떤 목적의 AI 툴이 필요하세요?", list(category_map.keys()))
    difficulty = st.radio("어느 정도 난이도를 원하세요?", list(tag_map.keys())[:3])
    price = st.radio("가격은 어떻게?", list(tag_map.keys())[3:])

    if st.button("추천 받기"):
        with st.spinner("추천 중입니다..."):
            filter_tags = [
                category_map.get(category, ""),
                tag_map.get(difficulty, ""),
                tag_map.get(price, "")
            ]
            # Airtable filterByFormula 생성
            formula = "AND(" + ",".join([f"FIND('{tag}', {{Tags}})" for tag in filter_tags if tag]) + ")"
            url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
            params = {"filterByFormula": formula}

            response = requests.get(url, headers=HEADERS, params=params)
            data = response.json().get("records", [])

            if data:
                st.success(f"추천된 AI 툴 {len(data)}개")
                for r in data[:3]:
                    fields = r.get("fields", {})
                    st.subheader(fields.get("Tool Name", "(이름 없음)"))
                    st.write(fields.get("Description", "(설명 없음)"))
                    st.markdown(f"[🔗 바로가기]({fields.get('Link', '#')})")
            else:
                st.warning("조건에 맞는 툴을 찾지 못했어요 😢")

if __name__ == "__main__":
    main()