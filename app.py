
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
st.set_page_config(page_title="NetDoc AI Pro | Elite Cyber-Physician", layout="wide", page_icon="🩺")

# --- DARK CYBERPUNK CSS (THE WOW FACTOR) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Rajdhani', sans-serif;
        background-color: #020617;
        color: #f8fafc;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% -20%, #1e293b 0%, #020617 80%);
    }

    /* Glassmorphism Neon Cards */
    .glass-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(0, 245, 212, 0.2);
        box-shadow: 0 0 20px rgba(0, 245, 212, 0.05);
        margin-bottom: 25px;
        transition: 0.4s ease;
    }
    .glass-card:hover {
        border: 1px solid rgba(0, 245, 212, 0.5);
        box-shadow: 0 0 30px rgba(0, 245, 212, 0.15);
    }

    .neon-title {
        font-size: 65px; font-weight: 700; text-align: center;
        color: #00f5d4;
        text-shadow: 0 0 20px rgba(0, 245, 212, 0.6);
        margin-bottom: 5px;
    }

    .status-badge {
        background: rgba(0, 245, 212, 0.1);
        color: #00f5d4;
        padding: 5px 15px;
        border-radius: 50px;
        border: 1px solid #00f5d4;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .report-paper {
        background: #0f172a;
        border: 1px dashed #00f5d4;
        padding: 40px;
        border-radius: 5px;
        color: #94a3b8;
        font-family: 'Courier New', Courier, monospace;
    }

    /* Pulse Animation */
    .pulse-dot {
        height: 12px; width: 12px; background-color: #00f5d4;
        border-radius: 50%; display: inline-block;
        box-shadow: 0 0 10px #00f5d4;
        animation: pulse 1.5s infinite;
        margin-right: 10px;
    }
    @keyframes pulse { 0% { transform: scale(0.9); opacity: 1; } 70% { transform: scale(1.3); opacity: 0.5; } 100% { transform: scale(0.9); opacity: 1; } }

    header {visibility: hidden;} footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- AI DIAGNOSIS CORE ---
@st.cache_resource
def train_physician_ai():
    # Latency, Loss, Jitter, Devices, Signal
    X = np.array([[20, 0, 2, 3, 95], [210, 10, 45, 18, 30], [50, 1, 8, 4, 85], [400, 18, 70, 6, 20], [95, 0, 15, 30, 75], [12, 0, 1, 1, 99]])
    y = np.array([0, 1, 0, 4, 1, 0])
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

# --- APP LAYOUT ---
st.markdown("<h1 class='neon-title'>NETDOC AI PRO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>Autonomous Neural Forensics & Network Bio-Diagnosis Suite</p>", unsafe_allow_html=True)

tabs = st.tabs(["🏥 CYBER-CLINIC", "🧬 NEURAL PULSE", "🧪 FORENSIC LAB", "📜 MEDICAL AUDIT"])

# --- TAB 1: CYBER-CLINIC ---
with tabs[0]:
    col_l, col_r = st.columns([1, 1.3])
    
    with col_l:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<div><span class='pulse-dot'></span><span class='status-badge'>Physician Online</span></div><br>", unsafe_allow_html=True)
        if lottie_doc: st_lottie(lottie_doc, height=250, key="doc_main")
        else: st.markdown("<h1 style='text-align:center;'>🩺</h1>", unsafe_allow_html=True)
        
        st.write("### AI Diagnostic Interface")
        if st.button("🚀 INITIATE BIO-SCAN"):
            with st.spinner("Decoding Network DNA..."):
                time.sleep(2.5)
                # Simulating realistic network metrics
                lat, loss, jit, devs, sig = random.randint(10, 400), random.randint(0, 15), random.randint(2, 70), random.randint(1, 40), random.randint(10, 99)
                pred = ai_model.predict([[lat, loss, jit, devs, sig]])[0]
                
                diagnosis_map = {
                    0: ("System Optimum", "Network DNA is pure. Throughput is at maximum potential.", "🟢"),
                    1: ("Hyper-Congestion", "Pathways clogged by excessive node interference.", "🟡"),
                    4: ("Gateway Failure", "Critical ISP routing degradation detected.", "🔴")
                }
                
                # FIXED: Consistent State Mapping
                st.session_state.doc_data = {
                    "v": diagnosis_map.get(pred, diagnosis_map[1])[0],
                    "p": diagnosis_map.get(pred, diagnosis_map[1])[1],
                    "i": diagnosis_map.get(pred, diagnosis_map[1])[2],
                    "s": [lat, loss, jit, devs, sig],
                    "t": time.strftime("%Y-%m-%d %H:%M:%S")
                }
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r:
        if 'doc_data' in st.session_state:
            data = st.session_state.doc_data
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.write(f"## {data['i']} Verdict: {data['v']}")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("LATENCY", f"{data['s'][0]}ms")
            c2.metric("LOSS", f"{data['s'][1]}%")
            c3.metric("NODES", f"{data['s'][3]}")
            
            st.markdown(f"""
            <div style='background:rgba(0,245,212,0.05); padding:20px; border-radius:15px; border-left:5px solid #00f5d4; margin-top:20px;'>
                <h4 style='color:#00f5d4;'>Rx Prescription</h4>
                <p><b>Finding:</b> {data['p']}</p>
                <p><b>AI Advice:</b> {random.choice(['Re-route via Layer 2 Switch', 'Flush DNS Cache', 'Enable Autonomous QoS'])}</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='glass-card' style='text-align:center;'><h3>Awaiting Bio-Metric Input...</h3><p>Click the Scan button to analyze network health.</p></div>", unsafe_allow_html=True)

# --- TAB 2: NEURAL PULSE ---
with tabs[1]:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.write("### 🧬 Neural Pulse Activity (Live Trends)")
    pulse_df = pd.DataFrame(np.random.randint(20, 100, size=(30, 2)), columns=['Uplink', 'Downlink'])
    fig_pulse = px.area(pulse_df, template="plotly_dark", color_discrete_sequence=['#00f5d4', '#f15bb5'])
    fig_pulse.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_family="Rajdhani")
    st.plotly_chart(fig_pulse, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: FORENSIC LAB ---
with tabs[2]:
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.write("#### 🧪 Traffic Anatomy")
        # FIXED Sunburst Logic
        df_sun = pd.DataFrame({
            "Layer": ["TCP", "TCP", "UDP", "Encryption", "Encryption"],
            "Protocol": ["Clean", "Retry", "Stream", "TLS 1.3", "SSL"],
            "Value": [50, 10, 25, 40, 5]
        })
        fig_sun = px.sunburst(df_sun, path=['Layer', 'Protocol'], values='Value', color_discrete_sequence=px.colors.sequential.Tealgrn)
        fig_sun.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_family="Rajdhani")
        st.plotly_chart(fig_sun, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col_b:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.write("#### 🛰️ Hardware Vitality")
        st.write("Processing Load"); st.progress(random.randint(30, 80))
        st.write("Radio Frequency Integrity"); st.progress(random.randint(60, 95))
        st.write("Buffer Saturation"); st.progress(random.randint(10, 40))
        st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 4: MEDICAL AUDIT (DETAILED REPORT) ---
with tabs[3]:
    if 'doc_data' in st.session_state:
        d = st.session_state.doc_data
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='report-paper'>
            <div style='text-align:center; border-bottom: 1px solid #00f5d4; padding-bottom:20px;'>
                <h1 style='color:#00f5d4; margin:0;'>NETWORK HEALTH AUDIT</h1>
                <p>CERTIFIED BY NETDOC AI PRO // SESSION ID: {random.randint(1000,9999)}</p>
                <p>TIMESTAMP: {d['t']}</p>
            </div>
            
            <div style='margin-top:30px;'>
                <h3 style='color:#00f5d4;'>1. EXECUTIVE SUMMARY</h3>
                <
