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
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background: #f0f4f8;
    }
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(216, 241, 230, 0.46) 0.1%, rgba(233, 226, 226, 0.28) 90.1%);
    }

    /* Glassmorphism Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 15px 35px rgba(0,0,0,0.05);
        margin-bottom: 25px;
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

    .doctor-badge {
        background: #3b82f6; color: white; padding: 5px 15px;
        border-radius: 50px; font-size: 12px; font-weight: bold;
    }

    header {visibility: hidden;} footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- AI DIAGNOSIS CORE ---
@st.cache_resource
def train_ai_doc():
    # Features: [Latency, PacketLoss, Jitter, Devices, Signal]
    # Labels: 0: Healthy, 1: Congested, 2: Security Risk, 3: HW Failure, 4: ISP Issue
    X = np.array([
        [20, 0, 2, 3, 95], [150, 5, 20, 15, 40], 
        [40, 2, 5, 2, 90], [300, 10, 50, 4, 30],
        [80, 0, 10, 25, 85], [15, 0, 1, 1, 99]
    ])
    y = np.array([0, 1, 2, 4, 1, 0])
    model = RandomForestClassifier(n_estimators=50)
    model.fit(X, y)
    return model

ai_doc = train_ai_doc()

# --- SAFE ASSETS ---
def load_lottie(url):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except: return None

lottie_doc = load_lottie("https://lottie.host/8553641b-10f7-434a-9524-71e98822588c/OayXwS3S0R.json")
lottie_scan = load_lottie("https://lottie.host/57a731d6-d3a3-4809-9683-16a707165089/y8Z9Fk1G4R.json")

# --- APP NAVIGATION ---
st.markdown("<h1 class='title-text'>NetDoc AI PRO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#64748b;'>Autonomous Neural Network Diagnostics & Self-Healing Agent</p>", unsafe_allow_html=True)

tabs = st.tabs(["🏥 AI Clinic", "🧬 Neural Vitals", "🧪 Lab Reports", "📡 Outage Map"])

# --- TAB 1: AI CLINIC ---
with tabs[0]:
    col1, col2 = st.columns([1, 1.3])
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.write("<span class='doctor-badge'>AI PHYSICIAN ONLINE</span>", unsafe_allow_html=True)
        if lottie_doc: st_lottie(lottie_doc, height=250, key="doc")
        
        st.write("### Start Patient Diagnosis")
        if st.button("🚀 INITIATE SYSTEM BIO-SCAN"):
            with st.spinner("Analyzing Network DNA..."):
                time.sleep(3)
                # Simulating realistic network metrics
                lat, loss, jit, devs, sig = random.randint(15, 350), random.randint(0, 12), random.randint(2, 60), random.randint(1, 30), random.randint(20, 99)
                
                # AI Inference
                prediction = ai_doc.predict([[lat, loss, jit, devs, sig]])[0]
                
                diagnoses = {
                    0: ("System Healthy", "Your network is in peak physical condition. No treatment required.", "🟢"),
                    1: ("Network Congestion", "Patient is overcrowded. Too many active devices are choking the bandwidth.", "🟡"),
                    2: ("Security Infection", "Suspicious packet signatures detected. Potential unauthorized intrusion.", "🔴"),
                    3: ("Hardware Fatigue", "Router CPU is overheating. Physical maintenance required.", "🟠"),
                    4: ("ISP Respiratory Failure", "High latency at the Gateway level. Problem lies with the Service Provider.", "🔵")
                }
                
                st.session_state.result = {
                    "verdict": diagnoses[prediction][0],
                    "presc": diagnoses[prediction][1],
                    "icon": diagnoses[prediction][2],
                    "stats": [lat, loss, jit, devs, sig]
                }
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        if 'result' in st.session_state:
            res = st.session_state.result
            st.markdown(f"<div class='glass-card'>", unsafe_allow_html=True)
            st.write(f"## {res['icon']} AI Verdict: {res['verdict']}")
            
            # Metrics Visual
            m1, m2, m3 = st.columns(3)
            m1.metric("Latency", f"{res['stats'][0]}ms")
            m2.metric("Packet Loss", f"{res['stats'][1]}%")
            m3.metric("Jitter", f"{res['stats'][2]}ms")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='prescription-box'>
                <b>🩺 DIGITAL PRESCRIPTION:</b><br>
                {res['presc']}<br><br>
                <b>Recommended Action:</b> {random.choice(['Reboot Gateway', 'Enable WPA3', 'Limit IoT Bandwidth', 'Switch to 5GHz Channel'])}
            </div>
            """, unsafe_allow_html=True)
            
            # Advice in Urdu
            st.info(f"💡 **Urdu Translation:** Is maslay ka hal ye hai ke: {res['presc']}")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            if lottie_scan: st_lottie(lottie_scan, height=300, key="scan")
            st.info("The Doctor is ready. Click 'Initiate Scan' to analyze your network's health.")

# --- TAB 2: NEURAL VITALS ---
with tabs[1]:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.write("### 🧬 Network Neural Activity (Live Vitals)")
    
    # Complex Plotly Chart
    vitals_data = pd.DataFrame(np.random.randint(20, 100, size=(24, 4)), 
                              columns=['Security', 'Throughput', 'Latency', 'Reliability'])
    
    fig = px.area(vitals_data, facet_col_wrap=2, title="Network Pulse Over 24 Hours", 
                  color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b', '#ef4444'])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_family='Plus Jakarta Sans')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: LAB REPORTS ---
with tabs[2]:
    st.write("### 🧪 Detailed Forensic Lab Reports")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.write("#### Packet Anatomy")
        fig_pie = px.sunburst(path=['Type', 'Status'], values=[40, 10, 20, 30], 
                             names=['TCP (Clean)', 'TCP (Retry)', 'UDP', 'ICMP'],
                             color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_b:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.write("#### Device Hardware Health")
        st.write("Router CPU: 45%")
        st.progress(45)
        st.write("Memory Usage: 78%")
        st.progress(78)
        st.write("Signal Quality: 92%")
        st.progress(92)
        st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 4: OUTAGE MAP ---
with tabs[3]:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.write("### 📡 Global Outage Surveillance (Real-Time)")
    map_data = pd.DataFrame({
        'lat': [30.3753, 51.5074, 40.7128, 35.6895],
        'lon': [69.3451, -0.1278, -74.0060, 139.6917],
        'status': ['Stable', 'ISP Outage', 'Maintenance', 'Stable'],
        'intensity': [10, 50, 30, 5]
    })
    fig_map = px.scatter_geo(map_data, lat='lat', lon='lon', color='status', size='intensity',
                            projection="natural earth", title="Worldwide Service Status")
    fig_map.update_layout(paper_bgcolor='rgba(0,0,0,0)', geo=dict(bgcolor= 'rgba(0,0,0,0)'))
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
st.sidebar.title("NetDoc HQ")
st.sidebar.write("---")
st.sidebar.markdown("**Patient ID:** XP-7721-NET")
st.sidebar.markdown("**AI Agent:** Dr. Sentinel v4.0")
st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Reset Clinic Memory"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

st.sidebar.info("NetDoc AI uses advanced Random Forest models to provide clinical-grade network diagnosis.")
