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

# --- CUSTOM CSS (Clean, Professional, Medical-Tech Look) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;600&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; color: #1e293b; }
    .stApp { background: #ffffff; }
    .doc-card {
        background: #ffffff; border-radius: 20px; padding: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #f1f5f9;
        margin-bottom: 20px;
    }
    .prescription {
        background: #f0fdf4; border-left: 5px solid #22c55e;
        padding: 15px; border-radius: 10px; color: #166534;
    }
    .status-pulse {
        height: 15px; width: 15px; background-color: #22c55e;
        border-radius: 50%; display: inline-block;
        box-shadow: 0 0 8px #22c55e; animation: pulse 2s infinite;
    }
    @keyframes pulse { 0% { transform: scale(0.95); } 70% { transform: scale(1.1); } 100% { transform: scale(0.95); } }
    </style>
    """, unsafe_allow_html=True)

# --- AI DIAGNOSIS ENGINE (Pre-trained Logic) ---
@st.cache_resource
def train_physician():
    # Features: [Latency, PacketLoss, ConnectedDevices, SignalStrength]
    # Labels: 0: Healthy, 1: Congested, 2: Security Threat, 3: ISP Issue
    X = np.array([[20, 0, 2, 90], [150, 5, 12, 40], [300, 2, 4, 85], [40, 0, 15, 95]])
    y = np.array([0, 1, 3, 2])
    model = RandomForestClassifier(n_estimators=10)
    model.fit(X, y)
    return model

physician = train_physician()

# --- ASSETS ---
def load_lottie(url):
    try: return requests.get(url, timeout=5).json()
    except: return None

lottie_doc = load_lottie("https://lottie.host/8553641b-10f7-434a-9524-71e98822588c/OayXwS3S0R.json")

# --- UI LAYOUT ---
st.markdown("<h1 style='text-align:center; color:#0f172a;'>🩺 NetDoc AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#64748b;'>Your Autonomous Network Physician & Optimization Agent</p>", unsafe_allow_html=True)

# Main Navigation
tab1, tab2, tab3 = st.tabs(["🏥 Check-up Clinic", "📊 Vital Signs", "📜 Health Report"])

with tab1:
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown("<div class='doc-card'>", unsafe_allow_html=True)
        st.write("### 🩺 Start Diagnosis")
        st_lottie(lottie_doc, height=200)
        
        if st.button("Run Full System Scan"):
            with st.spinner("Analyzing network vitals..."):
                time.sleep(3)
                # Simulated Real-time Data
                lat, loss, devs, sig = random.randint(20, 250), random.randint(0, 10), random.randint(1, 20), random.randint(30, 95)
                
                # AI Verdict
                diag_idx = physician.predict([[lat, loss, devs, sig]])[0]
                verdicts = ["Healthy Network", "Network Congestion", "Security Risk Detected", "ISP Level Throttling"]
                prescriptions = [
                    "Everything looks great! No action needed.",
                    "Diagnosis: Too many devices. Action: Disconnect unused IoT devices.",
                    "Diagnosis: Suspicious packets found. Action: Change WPA3 password immediately.",
                    "Diagnosis: High latency from ISP. Action: Contact your provider regarding routing."
                ]
                
                st.session_state.result = (verdicts[diag_idx], prescriptions[diag_idx], lat, loss)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        if 'result' in st.session_state:
            res, presc, lat, loss = st.session_state.result
            st.markdown(f"<div class='doc-card'>", unsafe_allow_html=True)
            st.write(f"### 📋 Diagnosis: **{res}**")
            st.write(f"**Latency:** {lat}ms | **Packet Loss:** {loss}%")
            st.markdown(f"<div class='prescription'><b>Doctor's Prescription:</b><br>{presc}</div>", unsafe_allow_html=True)
            
            # Advice in Urdu for better accessibility
            st.info(f"💡 **Mashwara:** {presc.split(':')[-1]}")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Click 'Run Full System Scan' to begin your network check-up.")

with tab2:
    st.write("### 📈 Network Heart Rate (Vital Signs)")
    chart_data = pd.DataFrame(np.random.randn(20, 2), columns=['Download', 'Upload'])
    fig = px.line(chart_data, title="Stability Pulse", template="plotly_white")
    fig.update_traces(line_color='#3b82f6')
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.write("### 📜 Monthly Network Health Certificate")
    st.markdown("""
    <div class='doc-card' style='text-align:center;'>
        <h2 style='color:#22c55e;'>GRADE: A-</h2>
        <p>Your network uptime was 99.2% this month.</p>
        <p><b>Top Patient Insight:</b> Most congestion occurs at 9 PM during streaming hours.</p>
        <button style='background:#0f172a; color:white; border-radius:5px; padding:10px;'>Download Full Medical Report</button>
    </div>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("### <span class='status-pulse'></span> System Status: Online", unsafe_allow_html=True)
st.sidebar.write("---")
st.sidebar.write("**Patient ID:** NET-99281")
st.sidebar.write("**AI Model:** Neural-Physician v2.1")
st.sidebar.button("Reset Physician Memory")
