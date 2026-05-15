import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from streamlit_lottie import st_lottie
import requests
import time
import random

# --- ADVANCED UI CONFIG ---
st.set_page_config(page_title="NetDoc AI Pro", layout="wide", page_icon="🩺")

# --- HIGH-END CSS (Cyber-Clinic Design) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background: #f8fafc; }
    .stApp { background: radial-gradient(circle at 10% 20%, rgba(216, 241, 230, 0.46) 0.1%, rgba(233, 226, 226, 0.28) 90.1%); }
    .glass-card {
        background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(12px);
        border-radius: 25px; padding: 30px; border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 15px 35px rgba(0,0,0,0.05); margin-bottom: 25px;
    }
    .title-text {
        font-size: 50px; font-weight: 800; text-align: center;
        background: linear-gradient(90deg, #0f172a, #3b82f6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .prescription-box {
        background: #ecfdf5; border-radius: 15px; padding: 20px;
        border-left: 8px solid #10b981; color: #065f46;
    }
    header {visibility: hidden;} footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- AI DIAGNOSIS CORE ---
@st.cache_resource
def train_ai_doc():
    X = np.array([[20, 0, 2, 3, 95], [150, 5, 20, 15, 40], [40, 2, 5, 2, 90], [300, 10, 50, 4, 30], [80, 0, 10, 25, 85], [15, 0, 1, 1, 99]])
    y = np.array([0, 1, 2, 4, 1, 0])
    model = RandomForestClassifier(n_estimators=50)
    model.fit(X, y)
    return model

ai_doc = train_ai_doc()

# --- SAFE ASSETS LOADING ---
def load_lottie(url):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except: return None

lottie_doc = load_lottie("https://lottie.host/8553641b-10f7-434a-9524-71e98822588c/OayXwS3S0R.json")

# --- APP LAYOUT ---
st.markdown("<h1 class='title-text'>NetDoc AI PRO</h1>", unsafe_allow_html=True)

tabs = st.tabs(["🏥 AI Clinic", "🧬 Neural Vitals", "🧪 Lab Reports", "📡 Outage Map"])

# --- TAB 1: AI CLINIC ---
with tabs[0]:
    col1, col2 = st.columns([1, 1.3])
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        if lottie_doc: st_lottie(lottie_doc, height=250, key="doc_anim")
        else: st.markdown("<h1 style='text-align:center;'>🩺</h1>", unsafe_allow_html=True)
        
        if st.button("🚀 INITIATE BIO-SCAN"):
            with st.spinner("Analyzing DNA..."):
                time.sleep(2)
                lat, loss, jit, devs, sig = random.randint(15, 300), random.randint(0, 10), random.randint(2, 50), random.randint(1, 20), random.randint(30, 99)
                pred = ai_doc.predict([[lat, loss, jit, devs, sig]])[0]
                
                diags = {
                    0: ("Healthy", "Peak physical condition.", "🟢"),
                    1: ("Congested", "Too many active devices.", "🟡"),
                    2: ("Security Risk", "Suspicious signatures detected.", "🔴"),
                    4: ("ISP Failure", "High latency at Gateway level.", "🔵")
                }
                st.session_state.result = {"verdict": diags.get(pred, diags[1])[0], "presc": diags.get(pred, diags[1])[1], "icon": diags.get(pred, diags[1])[2], "stats": [lat, loss, jit, devs, sig]}
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        if 'result' in st.session_state:
            res = st.session_state.result
            st.markdown(f"<div class='glass-card'>", unsafe_allow_html=True)
            st.write(f"## {res['icon']} AI Verdict: {res['verdict']}")
            m1, m2, m3 = st.columns(3)
            m1.metric("Latency", f"{res['stats'][0]}ms")
            m2.metric("Loss", f"{res['stats'][1]}%")
            m3.metric("Jitter", f"{res['stats'][2]}ms")
            st.markdown(f"<div class='prescription-box'><b>Prescription:</b> {res['presc']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Initiate scan to begin diagnosis.")

# --- TAB 2: NEURAL VITALS ---
with tabs[1]:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    vitals_data = pd.DataFrame(np.random.randint(20, 100, size=(24, 2)), columns=['Download', 'Upload'])
    fig_vitals = px.line(vitals_data, title="Stability Pulse (24h)", template="plotly_white")
    st.plotly_chart(fig_vitals, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: LAB REPORTS (FIXED SUNBURST) ---
with tabs[2]:
    st.write("### 🧪 Forensic Lab Reports")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        # FIXED SUNBURST LOGIC
        sunburst_df = pd.DataFrame({
            "Traffic": ["TCP", "TCP", "UDP", "ICMP"],
            "Subtype": ["Clean", "Retry", "Stream", "Echo"],
            "Value": [45, 10, 30, 15]
        })
        fig_pie = px.sunburst(sunburst_df, path=['Traffic', 'Subtype'], values='Value', title="Packet Anatomy")
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col_b:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.write("#### Hardware Health")
        st.write("CPU: 45%"); st.progress(45)
        st.write("Signal: 92%"); st.progress(92)
        st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 4: OUTAGE MAP ---
with tabs[3]:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    map_df = pd.DataFrame({'lat': [30.3753, 51.5074, 40.7128], 'lon': [69.3451, -0.1278, -74.0060], 'status': ['Stable', 'Outage', 'Slow']})
    fig_map = px.scatter_geo(map_df, lat='lat', lon='lon', color='status', title="Global Status")
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("NetDoc HQ")
if st.sidebar.button("🗑️ Reset Clinic"):
    for key in st.session_state.keys(): del st.session_state[key]
    st.rerun()
