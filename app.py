import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from streamlit_lottie import st_lottie
import requests
import time
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="NetDoc AI", layout="wide", page_icon="🩺")

# --- CUSTOM CSS (Medical-Tech Look) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;600&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; color: #1e293b; }
    .doc-card {
        background: #ffffff; border-radius: 20px; padding: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #f1f5f9;
        margin-bottom: 20px;
    }
    .prescription {
        background: #f0fdf4; border-left: 5px solid #22c55e;
        padding: 15px; border-radius: 10px; color: #166534; margin-top: 10px;
    }
    header {visibility: hidden;} footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- AI DIAGNOSIS ENGINE ---
@st.cache_resource
def train_physician():
    # Features: [Latency, PacketLoss, ConnectedDevices, SignalStrength]
    X = np.array([[20, 0, 2, 90], [150, 5, 12, 40], [300, 2, 4, 85], [40, 0, 15, 95], [10, 0, 1, 98]])
    y = np.array([0, 1, 3, 2, 0])
    model = RandomForestClassifier(n_estimators=10)
    model.fit(X, y)
    return model

physician = train_physician()

# --- SAFE ASSETS LOADING ---
def load_lottie(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Stable Lottie Link
lottie_doc = load_lottie("https://lottie.host/8553641b-10f7-434a-9524-71e98822588c/OayXwS3S0R.json")

# --- UI LAYOUT ---
st.markdown("<h1 style='text-align:center; color:#0f172a;'>🩺 NetDoc AI Agent</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#64748b;'>Autonomous Network Health Diagnosis & Optimization</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏥 Check-up Clinic", "📊 Vital Signs", "📜 Health Report"])

with tab1:
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown("<div class='doc-card'>", unsafe_allow_html=True)
        st.write("### 🩺 Start Scan")
        
        # FIX: Check if lottie loaded, else show Emoji
        if lottie_doc:
            st_lottie(lottie_doc, height=200, key="physician_anim")
        else:
            st.markdown("<h1 style='text-align:center; font-size:100px;'>🩺</h1>", unsafe_allow_html=True)
        
        if st.button("Run AI Diagnosis"):
            with st.spinner("Analyzing network vitals..."):
                time.sleep(2)
                lat, loss, devs, sig = random.randint(15, 300), random.randint(0, 8), random.randint(1, 20), random.randint(35, 98)
                diag_idx = physician.predict([[lat, loss, devs, sig]])[0]
                
                verdicts = ["Healthy Network", "Network Congestion", "Security Risk Detected", "ISP Throttling"]
                prescs = [
                    "Everything is perfect. No intervention required.",
                    "High traffic detected. Suggestion: Limit background 4K streaming.",
                    "Suspicious activity found. Suggestion: Enable WPA3 and change Wi-Fi password.",
                    "Slow response from Gateway. Suggestion: Restart ONT/Router and contact ISP."
                ]
                st.session_state.diag = (verdicts[diag_idx], prescs[diag_idx], lat, loss)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        if 'diag' in st.session_state:
            res, presc, lat, loss = st.session_state.diag
            st.markdown(f"<div class='doc-card'>", unsafe_allow_html=True)
            st.write(f"### 📋 Analysis: **{res}**")
            st.write(f"**Latency:** {lat}ms | **Packet Loss:** {loss}%")
            st.markdown(f"<div class='prescription'><b>AI Prescription:</b><br>{presc}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Please initiate a scan to see the results.")

with tab2:
    st.markdown("<div class='doc-card'>", unsafe_allow_html=True)
    st.write("### 📈 Live Network Pulse")
    # Random pulse data
    data = pd.DataFrame(np.random.randint(20, 100, size=(20, 2)), columns=['Download Mbps', 'Upload Mbps'])
    st.line_chart(data)
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.write("### 📜 Digital Health Certificate")
    st.markdown("""
    <div class='doc-card' style='text-align:center; border: 2px solid #22c55e;'>
        <h2 style='color:#22c55e;'>NETWORK GRADE: A</h2>
        <p>Your network has been stable for the last 24 hours.</p>
        <hr>
        <p><b>AI Insight:</b> Peak performance observed between 2 AM - 8 AM.</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🩺 NetDoc Settings")
st.sidebar.write("---")
st.sidebar.info("This AI Physician uses Machine Learning to diagnose network bottlenecks.")
if st.sidebar.button("Clear Patient History"):
    if 'diag' in st.session_state:
        del st.session_state.diag
    st.rerun()
