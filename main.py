# main.py
import os
import streamlit as st
from dotenv import load_dotenv
from calculator import calculate_space_cost
from ai_core import analyze_item_with_ai

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="미니멀리스트 AI 어드바이저", page_icon="🗑️", layout="centered")

st.title("🗑️ Minimalist AI Advisor")
st.subheader("버릴까 말까 고민되는 물건, AI가 냉정하게 판결해 드립니다.")
st.markdown("---")

st.markdown("#### 📦 어떤 물건을 비워낼까요?")
item_desc = st.text_area(
    "물건의 이름과 사연을 적어주세요.", 
    placeholder="예) 매일 강의 필기할 때 쓰는 아이패드와 애플펜슬",
    height=100
)

col1, col2 = st.columns(2)

with col1:
    monthly_rent = st.number_input(
        "💸 대략적인 월세 (0 입력 시 공간 계산 제외)", 
        min_value=0, 
        value=500000, 
        step=50000,
        format="%d"
    )

with col2:
    size_category = st.selectbox(
        "📏 물건의 대략적인 크기", 
        [
            "초소형 (스마트폰, 필기구, 지갑 등)", # 추가된 옵션
            "소형 (서랍 한 칸, 선반 일부)", 
            "중형 (사과 박스 1~2개 크기)", 
            "대형 (소형 가구, 실내 자전거 등)"
        ]
    )

if st.button("⚖️ AI에게 판결 받기", type="primary"):
    # 환경 변수 누락 예외 처리
    if not api_key:
        st.error("서버 오류: `.env` 파일에 `OPENAI_API_KEY`가 설정되지 않았습니다.")
    elif not item_desc.strip():
        st.warning("물건에 대한 설명을 입력해주세요.")
    else:
        with st.spinner("AI가 객관적인 가치와 기회비용을 분석 중입니다..."):
            # 1. 기회 비용 계산 모듈 호출
            space_cost_info = calculate_space_cost(monthly_rent, size_category)
            
            # 2. AI 판결 코어 모듈 호출
            result_markdown = analyze_item_with_ai(api_key, item_desc, space_cost_info)
            
            # 3. 결과 출력
            st.success("분석이 완료되었습니다!")
            
            with st.container(border=True):
                st.markdown(result_markdown)