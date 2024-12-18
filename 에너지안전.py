import streamlit as st
import time
from streamlit_extras.switch_page_button import switch_page

# Main Page (우리동네 에너지안전 지킴이이.py)
st.set_page_config(page_title="우리동네 에너지안전 지킴이", page_icon=":bulb:", layout="wide")

# Header Section
st.markdown("""
<div style="text-align: center; font-family: 'Arial Black', sans-serif; background: linear-gradient(to right, #FFD700, #FFA500); -webkit-background-clip: text; color: transparent; font-size: 3em;">
✨ 우리동네 에너지안전 지킴이 ✨
</div>
<div style="text-align: center; color: black; font-size: 1.2em;">
스마트 보안등과 태양광 발전으로 안전하고 효율적인 동네 만들기
</div>
""", unsafe_allow_html=True)

# Add Image
st.image("image\\first.webp", use_container_width=True, caption="🌟 우리동네 에너지안전 지킴이 프로젝트 🌟")

st.divider()

# Login System
if 'name' not in st.session_state:
    st.session_state['name'] = ''

if 'pw' not in st.session_state:
    st.session_state['pw'] = ''

with st.form("로그인"):
    col1, col2 = st.columns(2)
    with col1:
        st.session_state['name'] = st.text_input("📚 학번 입력", key="name_input")
    with col2:
        st.session_state['pw'] = st.text_input("🖋️ 이름 입력", key="pw_input")
    submitted = st.form_submit_button("🔑 로그인")

login = {
    "3001": "김일번",
    "3002": "김이번",
    "3003": "박삼번",
    "3004": "박사번",
    "3000": "박보정"
}

if submitted:
    with st.spinner('🔄 로그인중입니다...'):
        time.sleep(2)

    if st.session_state['name'] in login.keys():
        if st.session_state['pw'] == login[st.session_state['name']]:
            st.success(f"✅ {st.session_state['pw']}님 로그인 되었습니다.")
        else:
            st.error("❌ 로그인 정보가 잘못되었습니다.")
    else:
        st.error("❌ 로그인 정보가 잘못되었습니다.")



