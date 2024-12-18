import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="해결방안 설계", layout="wide")
st.title(":bulb: **해결방안 설계**")

# Tabs for 각각의 해결방안
tabs = st.tabs([
    "✨ [해결방안설계1] 보안등 설치 개수 정하기",
    "📊 [해결방안설계2] 효율 정의 및 계산",
    "🗺️ [해결방안설계3] 보안등 설치 장소 정하기"
])

# Initialize session state for storing values
if "saved_data" not in st.session_state:
    st.session_state["saved_data"] = []

if "locations" not in st.session_state:
    st.session_state["locations"] = []

if "best_efficiency_data" not in st.session_state:
    st.session_state["best_efficiency_data"] = {}

# Tab 1: 보안등 설치 개수 정하기
with tabs[0]:
    st.markdown("""
    <div style='text-align: center; background-color: #FFEBB2; border-radius: 10px; padding: 10px;'>
        <h2 style='color: #FF5733;'>✨ 보안등 설치 개수 및 전력량 계산 ✨</h2>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("보안등 개수 입력")
    smart_security = st.number_input("스마트 보안등 300W 개수(하루 5시간)", min_value=0, step=1, key="smart_security")
    sodium_security = st.number_input("나트륨 보안등 250W 개수(하루 10시간)", min_value=0, step=1, key="sodium_security")
    led_security = st.number_input("LED 보안등 80W 개수(하루 10시간)", min_value=0, step=1, key="led_security")

    # Calculation
    daily_power_smart = smart_security * 300 * 5
    daily_power_sodium = sodium_security * 250 * 10
    daily_power_led = led_security * 80 * 10
    total_daily_power = daily_power_smart + daily_power_sodium + daily_power_led
    solar_power = 18754.42/2
    solar_percentage = (total_daily_power / solar_power) * 100

    # Display Results
    st.write(f"**하루에 필요한 총 전력량:** {total_daily_power:.2f} Wh")
    st.write(f"**태양광 발전량:** {solar_power:.2f} Wh")
    st.write(f"**태양광 발전량 대비 충당 비율:** {solar_percentage:.2f}%")

    # Visualization
    st.subheader("시뮬레이션 결과 시각화")
    fig, ax = plt.subplots()
    labels = ["스마트 보안등", "나트륨 보안등", "LED 보안등", "총 전력량", "태양광 발전량"]
    values = [daily_power_smart, daily_power_sodium, daily_power_led, total_daily_power, solar_power]
    ax.bar(labels, values, color=["orange", "blue", "green", "purple", "red"], label="전력량")
    ax.axhline(solar_power, color='r', linestyle='--', label="태양광 발전량 기준선")
    ax.set_ylabel("전력량 (Wh)")
    ax.set_title("보안등 종류별 및 총 전력량 비교")
    ax.legend()
    st.pyplot(fig)

        
# Tab 2: 효율 정의 및 계산
with tabs[1]:
    st.markdown("""
    <div style='text-align: center; background-color: #CDEAFF; border-radius: 10px; padding: 10px;'>
        <h2 style='color: #2B85C9;'>📊 보안등 효율 정의 및 계산 📊</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**효율**은 다음과 같이 정의됩니다:")
    st.latex(r"효율 = \frac{스마트가로등 \times 3 + 나트륨 보안등 + LED 보안등}{하루에 필요한 총 전력량}*100")

    # Tap1에서 저장된 보안등 개수 불러오기
    if st.session_state["saved_data"]:
        saved = st.session_state["saved_data"][0]
        smart_security_2 = saved["스마트 보안등"]
        sodium_security_2 = saved["나트륨 보안등"]
        led_security_2 = saved["LED 보안등"]
    else:
        # 기본값 설정
        smart_security_2 = st.number_input("스마트 보안등 개수", min_value=0, step=1, key="smart_security_2")
        sodium_security_2 = st.number_input("나트륨 보안등 개수", min_value=0, step=1, key="sodium_security_2")
        led_security_2 = st.number_input("LED 보안등 개수", min_value=0, step=1, key="led_security_2")

    # 안전지수 및 효율 계산
    safety_index = (smart_security_2 * 3) + sodium_security_2 + led_security_2
    total_daily_power = (smart_security_2 * 300 * 5) + (sodium_security_2 * 250 * 10) + (led_security_2 * 80 * 10)

    if total_daily_power > 0:
        efficiency = safety_index / total_daily_power *10000
    else:
        efficiency = 0

    # 결과 표시
    st.subheader("계산 결과")
    st.write(f"**스마트 보안등 개수:** {smart_security_2}")
    st.write(f"**나트륨 보안등 개수:** {sodium_security_2}")
    st.write(f"**LED 보안등 개수:** {led_security_2}")
    st.write(f"**안전지수:** {safety_index}")
    st.write(f"**하루에 필요한 총 전력량:** {total_daily_power} Wh")
    st.write(f"**효율:** {efficiency:.4f}")

    # 효율 결과 저장
    if st.button("효율 결과 저장"):
        st.session_state["best_efficiency_data"] = {
            "스마트 보안등 개수": smart_security_2,
            "나트륨 보안등 개수": sodium_security_2,
            "LED 보안등 개수": led_security_2,
            "안전지수": safety_index,
            "총 전력량": total_daily_power,
            "효율": efficiency
        }
        st.success("효율 결과가 저장되었습니다!")
    
# Tab 3: 보안등 설치 장소 정하기
with tabs[2]:
    st.markdown("""
    <div style='text-align: center; background-color: #FFE4B2; border-radius: 10px; padding: 10px;'>
        <h2 style='color: #D2691E;'>🗺️ 보안등 설치 장소 정하기 🗺️</h2>
    </div>
    """, unsafe_allow_html=True)

    # 네이버지도 거리뷰 링크 제공
    st.write("네이버 지도의 우리동네(우리학교 근처) 거리뷰와 해결방안 설계2의 총 보안등 수를 통해 보안등이 필요한 곳을 정하고 필요한 총 수 대비 설치 장소를 정해보세요.")
    st.subheader("네이버 거리뷰에서 보안등 확인")
    st.markdown("[네이버지도 염창중 근처 거리뷰](https://map.naver.com/p/search/%EC%97%BC%EC%B0%BD%EC%A4%91%ED%95%99%EA%B5%90?c=15.89,0,0,0,adh&p=sY_XfqWohJeNEA5rEgpj8Q,-90,10,80,Float)")

    # Tap2 효율 결과
    if st.session_state["best_efficiency_data"]:
        st.subheader("해결방안 설계2에서 계산된 효율 결과")
        st.table(pd.DataFrame([st.session_state["best_efficiency_data"]]))

    # 지도 생성 및 초기화
    st.subheader("지도에서 설치하고픈 보안등 위치 클릭하기 ")
    map_center = [37.553074018209, 126.87192741366]
    m = folium.Map(location=map_center, zoom_start=15)

    # 반경 300m 원 표시
    folium.Circle(
        location=map_center,
        radius=300,
        color="green",
        fill=True,
        fill_opacity=0.3
    ).add_to(m)

    # 저장된 위치를 지도에 표시
    for loc in st.session_state["locations"]:
        folium.Marker(
            [loc["위도"], loc["경도"]],
            popup=loc.get("이름", "이름 없음"),
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    # 지도 클릭한 위치 처리
    result = st_folium(m, width=700, height=500)

    # 클릭 이벤트 처리
    if result and "last_clicked" in result and result["last_clicked"]:
        lat = result["last_clicked"]["lat"]
        lon = result["last_clicked"]["lng"]

        # 중복된 위치 방지
        if not any(loc['위도'] == lat and loc['경도'] == lon for loc in st.session_state["locations"]):
            location_name = f"장소 {len(st.session_state['locations']) + 1}"
            st.session_state["locations"].append({
                "위도": lat, 
                "경도": lon, 
                "이름": location_name
            })
            st.success(f"위치가 저장되었습니다: {location_name}")

    # 저장된 위치를 표로 표시
    if st.session_state["locations"]:
        st.subheader("저장된 보안등 위치 목록")
        st.table(pd.DataFrame(st.session_state["locations"]))
