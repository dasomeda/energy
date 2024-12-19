import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import koreanize-matplotlib

# Main App Tabs
st.set_page_config(page_title="데이터 이해 및 분석", layout="wide")
st.title(":bar_chart: 데이터 이해 및 분석")


# Sub-tabs for "데이터 이해 및 분석"
tabs = st.tabs([
    "☀️ 태양광 발전으로 생기는 전력량",
    "💡 보안등이 쓰는 전력량 비율"
])

# Tab 1: 태양광 발전으로 생기는 전력량
with tabs[0]:
    st.markdown("""
<div style='text-align: center; background-color: #FFD700; border-radius: 10px; padding: 10px;'>
<h1 style='color: #FFA500;'>✨ 태양광 발전으로 생기는 전력량 ✨</h1>
</div>
""", unsafe_allow_html=True)

    # CSV 파일 경로
    file_path = "서울특별시 강서구_공공태양광 발전량 현황_20231207.csv"

    
    # 데이터 로드
    try:
        solar_data = pd.read_csv(file_path, encoding='cp949')
    except Exception as e:
        st.error(f"파일 로드 중 오류가 발생했습니다: {e}")
        solar_data = None

    if solar_data is not None:
        # 지도 생성
        map_center = [37.5509, 126.8495]  # 강서구 중심 좌표
        m = folium.Map(location=map_center, zoom_start=13)

        for _, row in solar_data.iterrows():
            folium.Marker(
                location=[row['위도'], row['경도']],
                popup=f"{row['태양광발전시설명']}\n설비용량: {row['설비용량(kW)']} kW",
                tooltip=row['태양광발전시설명'],
                icon=folium.Icon(color='orange', icon='sun')
            ).add_to(m)

        folium.Circle(
            location=[37.553074018209, 126.87192741366],  # 염창중학교 좌표
            radius=300,  # 300m 반경
            color='yellow',
            fill=True,
            fill_opacity=0.3
        ).add_to(m)

        st.markdown("""
<div style='margin: 20px 0; font-size: 1.2em; color: #32CD32;'>
📍 1. 지도에서 태양광 발전소의 위치를 탐색하세요. 우리동네에 있나요? 📍
</div>
""", unsafe_allow_html=True)

        st_folium(m, width=700, height=500)

        st.markdown("""
<div style='margin: 10px 0; font-size: 0.9em; color: #FFD700; text-align: center;'>
우리동네에 태양광 발전시설이 없어서 우리 학교에 태양광발전기(25kW)가 생긴다고 해요!! \n
                    지도에 나타난 '서울특별시 강서구_공공태양광 발전량 현황' 자료를 그래프로 나타내어 분석해봐요
</div>
""", unsafe_allow_html=True)

        # 그래프 그리기
        st.markdown("""
<div style='text-align: center; background-color: #B0E0E6; border-radius: 8px; padding: 10px;'>
<h3 style='color: #4682B4;'>✨ 2. 자료를 그래프로 나타내고 학교 태양발전기를 위한 공공태양광 발전량 분석하기 ✨</h3>
</div>
""", unsafe_allow_html=True)

        x_axis = st.selectbox("X축을 선택하세요", ['위도', '경도','설치연도', '설비용량(kW)'], key="x_axis")
        y_axis = st.selectbox("Y축을 선택하세요", ['22년 발전량(kWh)', '23년 발전량(kWh)'], key="y_axis")

        if x_axis and y_axis:
            x = pd.to_numeric(solar_data[x_axis], errors='coerce')
            y = pd.to_numeric(solar_data[y_axis], errors='coerce')

            fig, ax = plt.subplots()
            valid_indices = x.notna() & y.notna()
            ax.scatter(x[valid_indices], y[valid_indices], label="데이터 점", color='orange')

            # 추세선 그리기
            coeffs = np.polyfit(x[valid_indices], y[valid_indices], 1)
            trendline = np.polyval(coeffs, x[valid_indices])
            ax.plot(x[valid_indices], trendline, label=f"추세선: y = {coeffs[0]:.2f}x + {coeffs[1]:.2f}", color='blue')

            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            ax.set_title("태양광 발전량 그래프")
            ax.legend()

            st.pyplot(fig)

        # 질문 섹션 추가
        st.markdown("""
### 질문
1. 발전량과 가장 상관관계가 있는 변인은?
""", unsafe_allow_html=True)
        user_choice = st.selectbox("X축을 선택하면서 확인해봐라 ", ['위도', '경도','설치연도', '설비용량(kW)'], key="question1")
        if st.button("제출", key="submit1"):
            if user_choice == '설비용량(kW)':
                st.success("정답입니다!")
            else:
                st.error("틀렸습니다. 다시 시도해 보세요.")

        st.markdown("""
2. "설비용량에 따른 발전량 그래프"에서 기울기는 무엇을 의미하는가?
""", unsafe_allow_html=True)
        user_answer = st.text_area("답변을 작성하세요", key="question2")
        if st.button("제출", key="submit2"):
            st.markdown(f"**답**: 태양광 발전을 한 시간")

        st.markdown("""
3. "22년과 23년 하루동안 발전한 평균 시간은 얼마일까(계산기 사용 가능)?
""", unsafe_allow_html=True)
        user_avg = st.text_input("답변을 작성하세요", key="question3")
        if st.button("제출", key="submit3"):
            st.markdown(f"**답**: 약 2시간")





# Tab 2: 보안등이 쓰는 전력량 비율
with tabs[1]:
    st.markdown("## **📊 태양광 에너지 비율 계산**")

    # 데이터 파일 경로 설정
    file_path = "서울특별시 전력사용량(홈페이지 게시용)_202405.csv"

    # 데이터 불러오기
    try:
        data = pd.read_csv(file_path, encoding='cp949')
        st.success("데이터가 성공적으로 불러와졌습니다!")
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        st.stop()

    # 구 선택
    st.subheader("** 우리동네 해당 구의 각 계약종별 전력(소비)량을 확인하고, 가로등의 전력(소비)량의 비율을 구하시오.**")
    selected_district = st.selectbox("구를 선택하세요:", data['시군구'].unique(), key="district_selection")
    filtered_data = data[data['시군구'] == selected_district]

    if not filtered_data.empty:
        st.write(f"**선택된 구:** {selected_district}")
        st.dataframe(filtered_data)

        # 사용자 입력: 가로등과 교육용 전력 소비량
        st.subheader("**1st. 우리동네 가로등 및 교육용 평균 전력(소비)량 입력(학교 발전기에서 쓰일 전력(소비)량)**")
        street_light_input = st.number_input("가로등 평균 전력(소비)량(kWh):", min_value=0.0, value=0.0, step=0.1, key="street_light")
        education_input = st.number_input("교육용 평균 전력(소비)량(kWh):", min_value=0.0, value=0.0, step=0.1, key="education")

        # 비율 계산
        total_power_input = street_light_input + education_input
        ratio = 0  # 초기화

        if total_power_input > 0:
            ratio = (street_light_input / total_power_input) * 100
            st.subheader("**2nd. 가로등 전력 소비량 비율 계산**")
            st.latex(r"비율 = \frac{\text{가로등 전력 소비량 합계}}{\text{가로등 전력 소비량 합계} + \text{교육용 전력 소비량 합계}} \times 100")
            st.write(f"**식**: {street_light_input:.2f} / ({street_light_input:.2f} + {education_input:.2f}) * 100")
            st.write(f"**계산된 비율:** {ratio:.2f}%")

            # 태양광 발전량에서 보안등에 쓰이는 전력량 계산
            st.subheader("**3rd. 우리학교에 설치(25kW)되는 태양광 발전량(Wh)에서 보안등 전력량(Wh) 계산**")
            solar_power = 25000 * 2  # 태양광 발전량: 50kW * 2시간
            lighting_power_from_solar = solar_power * (ratio / 100)
            st.write(f"**태양광 발전량:** {solar_power:.2f} Wh")
            st.write(f"**보안등 전력량 비율:** {ratio:.2f}%")
            st.write(f"**태양광 발전량에서 보안등이 사용하는 전력량:** {lighting_power_from_solar:.2f} Wh")

            # 시각화: 가로등과 교육용 전력량 비율
            st.subheader("**전력(소비)량 비율 나타내기기**")
            fig, ax = plt.subplots()
            labels = ['가로등 전력 소비량', '교육용 전력 소비량']
            values = [street_light_input, education_input]
            ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=['orange', 'blue'])
            ax.set_title("가로등 및 교육용 전력 소비량 비율")
            st.pyplot(fig)
        else:
            st.warning("입력값의 합이 0입니다. 적절한 값을 입력해 주세요.")

    else:
        st.warning("선택된 구에 대한 데이터가 없습니다.")
