import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Main App Tabs
st.set_page_config(page_title="문제 발견", layout="wide")
st.title(":bulb: 문제 발견")

# Sub-tabs for "문제 발견"
tabs = st.tabs([
    "📜 뉴스를 통한 문제 발견",
    "📍 우리동네의 스마트 보안등"
])

# Tab 1: 뉴스를 통한 문제 발견
with tabs[0]:
    st.markdown("""
<div style='text-align: center; background-color: #FFE4B5; border-radius: 10px; padding: 10px;'>
<h1 style='color: #FFA500;'>✨ 뉴스를 통한 문제 발견 ✨</h1>
</div>
""", unsafe_allow_html=True)
    st.write("- **보안등의 정의**: 통상적으로 보행자의 안전을 확보하고 치안을 예방하는 데 목적을 두고 보행자 길을 조명하는 가로등입니다.")
    st.write("- 여러 가지 뉴스 자료를 통해 각 지자체가 치안과 에너지 절감을 위해 가로등을 변경하고 있는 사례를 소개합니다:")
    st.markdown("[강서구, 보안등 ·가로등 '친환경 LED'로 전면 교체](https://www.youtube.com/watch?v=GqFlohcsAs0&list=LL)")
    st.markdown("[LED 가로등으로 전면 교체…안전하고 매력적인 '서울의 밤'](https://www.yna.co.kr/view/AKR20240121010600004)")
    st.markdown("[충분한 가로등 빛 제공…범죄 예방의 '첫걸음'](http://www.sjbnews.com/news/articleView.html?idxno=455090)")
    st.markdown("['학교발전소' 전기요금 아끼고 환경교육까지](https://www.idomin.com/news/articleView.html?idxno=768662)")
    # Add Question
    st.markdown("""
<div style='margin: 20px 0; color: #FF69B4; font-size: 1.2em;'>
💡 **뉴스를 통해 우리는 무엇을 위해서 가로등을 변경하고 있는지 적으시오.** 💡
</div>
""", unsafe_allow_html=True)
    answer = st.text_area("답변을 작성하세요.")
    if st.button("제출"):
        if answer.strip():
            st.success("답변이 제출되었습니다. 감사합니다!")
        else:
            st.error("답변을 입력해주세요.")

# Tab 2: 우리동네의 스마트 보안등
with tabs[1]:
    st.markdown("""
<div style='text-align: center; background-color: #B0E0E6; border-radius: 10px; padding: 10px;'>
<h1 style='color: #00BFFF;'>✨ 우리동네의 스마트 보안등 ✨</h1>
</div>
""", unsafe_allow_html=True)

    # CSV 파일 경로
    file_path = "서울특별시_강서구_스마트가로등.csv"

    # 데이터 로드
    try:
        data = pd.read_csv(file_path, encoding='cp949')
    except Exception as e:
        st.error(f"파일 로드 중 오류가 발생했습니다: {e}")
        data = None

    if data is not None:
        # 지도 생성
        map_center = [37.5509, 126.8495]  # 강서구 중심 좌표
        m = folium.Map(location=map_center, zoom_start=13)

        # 도로명 선택 박스
        selected_road = st.selectbox("도로명을 선택하세요:", ["전체"] + list(data['도로명'].unique()))

        # 스마트 보안등 및 염창중학교, 김포공항 추가
        if selected_road == "전체":
            for _, row in data.iterrows():
                folium.Marker(
                    location=[row['위도'], row['경도']],
                    popup=f"도로명: {row['도로명']}",
                    tooltip=row['도로명'],
                    icon=folium.Icon(color='green', icon='lightbulb')
                ).add_to(m)
        else:
            filtered_data = data[data['도로명'] == selected_road]
            for _, row in filtered_data.iterrows():
                folium.Marker(
                    location=[row['위도'], row['경도']],
                    popup=f"도로명: {row['도로명']}",
                    tooltip=row['도로명'],
                    icon=folium.Icon(color='green', icon='lightbulb')
                ).add_to(m)

        # 항상 염창중학교 표시
        school_center = [37.553074018209, 126.87192741366]
        folium.Marker(
            location=school_center,
            popup="염창중학교",
            tooltip="염창중학교",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
        folium.Circle(
            location=school_center,
            radius=300,  # 300m 반경
            color='yellow',
            fill=True,
            fill_opacity=0.3
        ).add_to(m)

        # 항상 김포공항 표시
        gimpo_airport = [37.559869, 126.794972]
        folium.Marker(
            location=gimpo_airport,
            popup="김포공항",
            tooltip="김포공항",
            icon=folium.Icon(color='none', icon='none')
        ).add_to(m)

        st.markdown("""
<div style='margin: 20px 0; font-size: 1.2em; color: #32CD32;'>
📍 **지도에서 강서구를 탐색하고 스마트 보안등의 위치를 확인하세요. 염창중학교(반경 300m)가 표시됩니다.** 📍
</div>
""", unsafe_allow_html=True)
        st_folium(m, width=700, height=500)

        # 질문 추가
        st.markdown("""
<div style='margin: 20px 0; color: #FF69B4; font-size: 1.2em;'>
💡 **염창중학교 반경 300m, 즉 우리동네에 스마트 보안등이 있나요? 어떻게 생각하시나요?** 💡
</div>
""", unsafe_allow_html=True)
        response = st.text_area("답변을 작성하세요.", key="response_area")
        if st.button("제출", key="response_submit"):
            if response.strip():
                st.success("그렇죠!! 우리도 에너지와 보안 모두 잡으려면 보안등을 어떻게 설치하냐가 중요할 겁니다^^ 만약 우리 학교에 태양광발전기(25kW)가 생긴다면, 우리 동네 치안을 위해 가장 효율적으로 보안등을 설치하는 방안 찾아봅시다.")
            else:
                st.error("답변을 입력해주세요.")
