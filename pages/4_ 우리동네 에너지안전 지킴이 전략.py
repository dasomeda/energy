import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# Page Configuration
st.set_page_config(page_title="우리동네 에너지안전 지킴이", layout="wide")

# 제목 설정
st.markdown(
    """
    <h1 style='text-align: center; color: #fffff0; font-size: 2.5em; margin-top: 10px;'>
        🏘️ 우리동네 에너지안전 지킴이 전략
    </h1>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if "locations" not in st.session_state:
    st.session_state["locations"] = []

# 보안등 종류별 색상 정의
LIGHT_COLORS = {
    "스마트 보안등 (300W)": "yellow",
    "나트륨 보안등 (250W)": "orange",
    "LED 보안등 (80W)": "blue"
}

# 지도 설정 및 염창중 반경 300m 원 표시
st.markdown(
    "<h5 style='text-align: center; color: #FFA000;'>우리동네 에너지안전을 지키기 위해 각각의 종류마다 설치할 보안등의 위치를 나타내고 전략과 이유를 쓰시오.</h5>",
    unsafe_allow_html=True
)

# 지도 생성
map_center = [37.553074018209, 126.87192741366]
m = folium.Map(location=map_center, zoom_start=15)

# 염창중 반경 300m 원 표시
folium.Circle(
    location=map_center,
    radius=300,
    color="green",
    fill=True,
    fill_opacity=0.3,
).add_to(m)

# 저장된 위치를 지도에 추가
for loc in st.session_state["locations"]:
    folium.Marker(
        [loc["위도"], loc["경도"]],
        popup=f"{loc['종류']}",
        icon=folium.Icon(color=LIGHT_COLORS.get(loc["종류"], "gray"))
    ).add_to(m)

# 보안등 종류 선택
light_type = st.selectbox("설치할 보안등 종류를 선택하고 위치를 입력하거나 클릭하시오.", list(LIGHT_COLORS.keys()))

# 사용자 입력으로 위도와 경도 받기
st.markdown("### 앞의 해결방안 설계에서 위도와 경도를 보고 위치를 입력하시오.")
input_lat = st.number_input("위도 입력", format="%.6f", value=37.553074)
input_lon = st.number_input("경도 입력", format="%.6f", value=126.871927)
add_location_button = st.button("위치 추가")

# 입력된 좌표로 위치 추가
if add_location_button:
    if not any(loc["위도"] == input_lat and loc["경도"] == input_lon for loc in st.session_state["locations"]):
        st.session_state["locations"].append({
            "위도": input_lat,
            "경도": input_lon,
            "종류": light_type
        })
        st.success(f"{light_type}가 추가되었습니다!")
    else:
        st.warning("이미 추가된 위치입니다.")

# 지도 클릭 이벤트로 위치 추가
st.markdown("### 지도에서 위치를 클릭해서 보안등을 추가하세요")
result = st_folium(m, width=700, height=500, key="unique_map")  # **유일한 지도 표시**

if result and "last_clicked" in result and result["last_clicked"]:
    clicked_lat = result["last_clicked"]["lat"]
    clicked_lon = result["last_clicked"]["lng"]

    if not any(loc["위도"] == clicked_lat and loc["경도"] == clicked_lon for loc in st.session_state["locations"]):
        st.session_state["locations"].append({
            "위도": clicked_lat,
            "경도": clicked_lon,
            "종류": light_type
        })
        st.success(f"지도 클릭 위치에 {light_type}가 추가되었습니다!")
    else:
        st.warning("이미 추가된 위치입니다.")

# 보안등 개수 합계 표시
st.markdown("### 보안등 종류별 개수 합계")
if st.session_state["locations"]:
    summary_df = pd.DataFrame(st.session_state["locations"])
    light_summary = summary_df["종류"].value_counts().reset_index()
    light_summary.columns = ["보안등 종류", "개수"]
    st.table(light_summary)

# 질문 섹션
st.markdown("### 설치된 보안등 개수와 설치 이유 작성")
user_answer = st.text_area("우리동네 에너지안전을 지키기 위한 전략과 이유를 앞에서 탐구했던 용어를 바탕으로 작성하세요.")
if st.button("제출"):
    st.success("수고했습니다! 이제 서로 피드백하도록 합시다!")


