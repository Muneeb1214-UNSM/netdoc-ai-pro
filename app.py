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
st.set_page_config(page_title="NetDoc AI Pro", layout="wide", page_icon="保护")

# --- DARK CYBERPUNK CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Rajdhani', sans-serif; background-color: #020617; color: #f8fafc; }
    .stApp { background: radial-gradient(circle at 50% -20%, #1e293b 0%, #020617 80%); }
    .glass-card {
        background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(20px);
        border-radius: 20px; padding: 30px; border: 1px solid rgba(0, 245, 212, 0.2);
        box-shadow: 0 0 20px rgba(0, 245, 212, 0.05); margin-bottom: 25px;
    }
    .neon-title {
        font-size: 60px; font-weight: 700; text-align: center; color: #00f5d4;
        text-shadow: 0 0 20px rgba(0, 245, 212, 0.6); margin-bottom: 5px;
    }
    .report-paper {
        background: #0f172a; border: 1px dashed #00f5d4; padding: 30px;
        border-radius: 5px; color: #94a3b8; font-family: 'Courier New', Courier, monospace;
    }
    header {visibility: hidden;} footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- AI DIAGNOSIS ENGINE ---
@st.cache_resource
def train_physician_ai():
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
        if lottie_doc: st_lottie(lottie_doc, height=220, key="doc_main")
        else: st.markdown("<h1 style='text-align:center;'>🩺</h1>", unsafe_allow_html=True)
        
        if st.button("🚀 INITIATE SCAN"):
            with st.spinner("Decoding Network DNA..."):
                time.sleep(2)
                lat, loss, jit, devs, sig = random.randint(10, 380), random.randint(0, 12), random.randint(2, 60), random.randint(1, 30), random.randint(20, 99)
                pred = ai_model.predict([[lat, loss, jit, devs, sig]])[0]
                
                diag_map = {
                    0: ("System Optimum", "Network DNA is pure. Throughput is stable.", "🟢"),
                    1: ("Hyper-Congestion", "Pathways clogged by excessive node interference.", "🟡"),
                    4: ("Gateway Failure", "Critical ISP routing degradation detected.", "🔴")
                }
                st.session_state.doc_data = {
                    "v": diag_map.get(pred, diag_map[1])[0],
                    "p": diag_map.get(pred, diag_map[1])[1],
                    "i": diag_map.get(pred, diag_map[1])[2],
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
            st.markdown(f"<div style='background:rgba(0,245,212,0.05); padding:15px; border-radius:10px; border-left:5px solid #00f5d4; margin-top:15px;'><b>Rx Finding:</b> {data['p']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Awaiting scan input...")

# --- TAB 2: NEURAL PULSE ---
with tabs[1]:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    pulse_df = pd.DataFrame(np.random.randint(20, 100, size=(25, 2)), columns=['Uplink', 'Downlink'])
    fig_pulse = px.area(pulse_df, template="plotly_dark", color_discrete_sequence=['#00f5d4', '#f15bb5'], title="Neural Stability Trend")
    fig_pulse.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_pulse, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: FORENSIC LAB ---
with tabs[2]:
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        # Fixed Sunburst
        df_sun = pd.DataFrame({"Layer": ["TCP", "TCP", "UDP", "App"], "Prot": ["Clean", "Retry", "Stream", "HTTP"], "Val": [40, 10, 30, 20]})
        fig_sun = px.sunburst(df_sun, path=['Layer', 'Prot'], values='Val', title="Traffic Anatomy")
        fig_sun.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_family="Rajdhani")
        st.plotly_chart(fig_sun, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col_b:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.write("#### Hardware Vitality")
        st.write("Processing Load"); st.progress(65)
        st.write("Signal Integrity"); st.progress(88)
        st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 4: MEDICAL AUDIT ---
with tabs[3]:
    if 'doc_data' in st.session_state:
        d = st.session_state.doc_data
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='report-paper'>
            <h2 style='color:#00f5d4; text-align:center;'>NETWORK HEALTH AUDIT</h2>
            <p style='text-align:center;'>SESSION: {random.randint(1000,9999)} | DATE: {d['t']}</p>
            <hr style='border-color:#1e293b;'>
            <h3>1. EXECUTIVE SUMMARY</h3>
            <p>Subject network exhibits <b>{d['v']}</b>. Neural patterns confirm: {d['p']}</p>
            <h3>2. VITAL STATS</h3>
            <p>- Latency: {d['s'][0]} ms <br> - Packet Loss: {d['s'][1]} % <br> - Active Nodes: {d['s'][3]}</p>
        </div>
        """, unsafe_allow_html=True)
        st.download_button("📥 DOWNLOAD REPORT", f"NetDoc Audit\nVerdict: {d['v']}\nStats: {d['s']}", file_name="Audit_Report.txt")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Please conduct a Clinic Scan first.")

# --- SIDEBAR ---
if st.sidebar.button("🗑️ PURGE CLINIC"):
    st.session_state.clear()
    st.rerun()
                <
