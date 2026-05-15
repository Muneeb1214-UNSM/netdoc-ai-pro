import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_lottie import st_lottie
import requests
import time
import random

# --- SETTING UP MODERN THEME ---
st.set_page_config(page_title="NetGuard AI", layout="wide", page_icon="🛡️")

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0e1117; color: white; }
    .status-card {
        background: #161b22; border-radius: 15px; padding: 20px;
        border: 1px solid #30363d; margin-bottom: 20px;
    }
    .score-high { color: #238636; font-size: 40px; font-weight: bold; }
    .score-low { color: #da3633; font-size: 40px; font-weight: bold; }
    header {visibility: hidden;} footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- LOAD ASSETS ---
def load_lottie(url):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except:
        return None

lottie_secure = load_lottie("https://lottie.host/8553641b-10f7-434a-9524-71e98822588c/OayXwS3S0R.json")

# --- DATA SIMULATION ENGINE ---
def get_device_data():
    devices = [
        {"Device": "Smart TV", "IP": "192.168.1.10", "Activity": "Streaming", "Risk": "Low", "Data_Sent": "1.2 GB"},
        {"Device": "CCTV Camera", "IP": "192.168.1.15", "Activity": "Unknown Server Sync", "Risk": "High", "Data_Sent": "450 MB"},
        {"Device": "iPhone 15", "IP": "192.168.1.5", "Activity": "Browsing", "Risk": "Low", "Data_Sent": "80 MB"},
        {"Device": "Smart Fridge", "IP": "192.168.1.20", "Activity": "Idle", "Risk": "Medium", "Data_Sent": "5 MB"}
    ]
    return pd.DataFrame(devices)

# --- NAVIGATION ---
st.sidebar.title("🛡️ NetGuard AI")
menu = st.sidebar.radio("Navigation", ["Home Dashboard", "Privacy Scan", "AI Assistant"])

if menu == "Home Dashboard":
    st.markdown("<h1 style='text-align:center;'>NetGuard AI Guardian</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    privacy_score = random.randint(55, 98)
    
    with col1:
        st.markdown("<div class='status-card'>", unsafe_allow_html=True)
        st.write("### Privacy Score")
        if privacy_score > 70:
            st.markdown(f"<p class='score-high'>{privacy_score}%</p>", unsafe_allow_html=True)
            st.write("Status: Secure")
        else:
            st.markdown(f"<p class='score-low'>{privacy_score}%</p>", unsafe_allow_html=True)
            st.write("Status: Warning")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        if lottie_secure:
            st_lottie(lottie_secure, height=150, key="home_anim")
        else:
            st.markdown("<h1 style='text-align:center;'>🛡️</h1>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='status-card'>", unsafe_allow_html=True)
        st.write("### AI Analysis")
        if privacy_score > 75:
            st.success("✅ Your home network is currently safe.")
        else:
            st.warning("⚠️ High data usage detected in CCTV.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("### Network Devices")
    df = get_device_data()
    st.dataframe(df, use_container_width=True)

    fig = px.pie(df, names='Device', values=[1.2, 0.45, 0.08, 0.005], title="Traffic Distribution", hole=0.4)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Privacy Scan":
    st.header("Deep Network Scan")
    if st.button("Start AI Scan"):
        with st.spinner("Analyzing traffic patterns..."):
            time.sleep(2)
            st.error("Alert: CCTV Camera (192.168.1.15) is sending data to a blacklisted IP in Russia.")
            st.info("Suggestion: Update camera firmware and change password.")

elif menu == "AI Assistant":
    st.header("NetGuard AI Assistant")
    user_query = st.text_input("Ask about your network safety:")
    if user_query:
        st.write("🤖 **NetGuard AI:** I analyzed your Smart TV. It's only connecting to Netflix and YouTube servers, which is 100% safe.")
