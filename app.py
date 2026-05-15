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
st.set_page_config(page_title="NetDoc AI Pro | Cyber-Physician", layout="wide", page_icon="🩺")

# --- CUSTOM CSS (THE WOW FACTOR) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Glassmorphism Design */
    .glass-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(15px);
        border-radius: 24px;
        padding: 35px;
        border: 1px solid rgba(255, 255, 255, 0.6);
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }

    .neon-title {
        font-size: 60px; font-weight: 800; text-align: center;
        background: linear-gradient(to right, #1e3a8a, #3b82f6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    .prescription-paper {
        background: white; border: 2px solid #e2e8f0;
        border-radius: 10px; padding: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        font-family: 'Courier New', Courier, monospace;
    }

    .pulse-btn {
        background: linear-gradient(90deg, #3b82f6, #1d4ed8);
        color: white !important; border: none; border-radius: 50px;
        padding: 15px 40px; font-weight: bold; font-size: 18px;
        transition: 0.3s ease;
    }
    
    header {visibility: hidden;} footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- AI DIAGNOSIS ENGINE ---
@st.cache_resource
def train_physician_ai():
    # Latency, Loss, Jitter, Devices, Signal
    X = np.array([[20, 0, 2, 3, 95], [180, 8, 35, 12, 35], [45, 1, 6, 2, 88], [350, 15, 60, 5, 25], [90, 0, 12, 28, 80], [12, 0, 1, 1, 99]])
    y = np.array([0, 1, 0, 4, 1, 0]) # 0: Healthy, 1: Congested, 4: ISP Issue
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    return model

ai_model = train_physician_ai()

# --- ASSETS LOADING ---
def load_lottie(url):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except: return None

lottie_doc = load_lottie("https://lottie.host/8553641b-10f7-434a-9524-71e98822588c/OayXwS3S0R.json")
lottie_scanning = load_lottie("https://lottie.host/57a731d6-d3a3-4809-9683-16a707165089/y8Z9Fk1G4R.json")

# --- APP LAYOUT ---
st.markdown("<h1 class='neon-title'>NetDoc AI Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#475569; font-size:18px;'>Autonomous Neural Network Diagnostics & Digital Forensic Laboratory</p>", unsafe_allow_html=True)

tabs = st.tabs(["🏥 Cyber-Clinic", "🧬 Neural Pulse", "🧪 Forensic Lab", "📜 Professional Report"])

# --- TAB 1: CLINIC ---
with tabs[0]:
    col_l, col_r = st.columns([1, 1.2])
    
    with col_l:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        if lottie_doc: st_lottie(lottie_doc, height=250, key="doc_main")
        else: st.markdown("<h1 style='text-align:center;'>🩺</h1>", unsafe_allow_html=True)
        
        st.write("### New Patient Diagnosis")
        if st.button("🚀 INITIATE SCAN"):
            with st.spinner("Conducting Deep Bio-Metric Scan..."):
                time.sleep(3)
                lat, loss, jit, devs, sig = random.randint(15, 380), random.randint(0, 15), random.randint(2, 65), random.randint(1, 35), random.randint(15, 99)
                pred = ai_model.predict([[lat, loss, jit, devs, sig]])[0]
                
                diagnosis_map = {
                    0: ("Optimum Health", "System DNA is clean. All vitals within normal range.", "🟢"),
                    1: ("Hyper-Congestion", "Network respiratory pathways clogged by excessive device load.", "🟡"),
                    4: ("ISP Degradation", "Detected high-level gateway failure. Signal routing is unstable.", "🔴")
                }
                st.session_state.data = {
                    "v": diagnosis_map.get(pred, diagnosis_map[1])[0],
                    "p": diagnosis_map.get(pred, diagnosis_map[1])[1],
                    "i": diagnosis_map.get(pred, diagnosis_map[1])[2],
                    "s": [lat, loss, jit, devs, sig],
                    "time": time.strftime("%Y-%m-%d %H:%M:%S")
                }
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r:
        if 'data' in st.session_state:
            res = st.session_state.data
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.write(f"## {res['i']} Diagnosis: {res['v']}")
            
            # Metrics Visuals
            c1, c2, c3 = st.columns(3)
            c1.metric("Latency", f"{res['stats'][0]}ms")
            c2.metric("Loss", f"{res['stats'][1]}%")
            c3.metric("Nodes", f"{res['stats'][3]}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='prescription-paper'>
                <h4 style='color:#1e3a8a;'>PRESCRIPTION (Urgent)</h4>
                <p><b>Rx:</b> {res['p']}</p>
                <p><b>Advice:</b> {random.choice(['Change Wi-Fi Channel to 11', 'Enable QoS Prioritization', 'Reboot ONT Gateway'])}</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            if lottie_scanning: st_lottie(lottie_scanning, height=350, key="scan_l")
            st.info("The AI Physician is awaiting a scan request.")

# --- TAB 2: NEURAL PULSE ---
with tabs[1]:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.write("### 🧬 Real-Time Neural Pulse (Stability Trend)")
    pulse_data = pd.DataFrame(np.random.randint(20, 100, size=(25, 2)), columns=['Download Mbps', 'Upload Mbps'])
    fig_pulse = px.line(pulse_data, template="plotly_white", color_discrete_sequence=['#3b82f6', '#10b981'])
    fig_pulse.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_pulse, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: FORENSIC LAB ---
with tabs[2]:
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.write("#### 🧪 Traffic Anatomy")
        # Fixed Sunburst
        df_sun = pd.DataFrame({
            "Layer": ["L4-TCP", "L4-TCP", "L4-UDP", "L7-App", "L7-App"],
            "Protocol": ["Clean", "Retry", "Streaming", "HTTPS", "DNS"],
            "Vol": [40, 15, 25, 50, 10]
        })
        fig_sun = px.sunburst(df_sun, path=['Layer', 'Protocol'], values='Vol', color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(fig_sun, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col_b:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.write("#### 📡 Gateway Health")
        st.write("Memory Utilization"); st.progress(62)
        st.write("Signal Integrity"); st.progress(89)
        st.write("Encryption Strength"); st.progress(98)
        st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 4: PROFESSIONAL REPORT ---
with tabs[3]:
    if 'data' in st.session_state:
        res = st.session_state.data
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        s
