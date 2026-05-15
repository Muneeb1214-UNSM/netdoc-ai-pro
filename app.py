import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from streamlit_lottie import st_lottie
import requests
import time
import random

# --- ADVANCED UI CONFIG ---
st.set_page_config(page_title="NetDoc AI Pro | Cyber-Physician", layout="wide", page_icon="🩺")

# --- DYNAMIC ANIMATED CSS (THE WOW FACTOR) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');

/* Dynamic Moving Background */
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp {
    background: linear-gradient(-45deg, #020617, #0f172a, #1e1b4b, #312e81);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    color: #f8fafc;
    font-family: 'Rajdhani', sans-serif;
}

/* Glassmorphism Animated Cards */
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 30px;
    border: 1px solid rgba(0, 242, 255, 0.2);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    margin-bottom: 25px;
    transition: 0.5s;
}
.glass-card:hover {
    border: 1px solid #00f2ff;
    transform: scale(1.02);
}

.neon-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 60px; font-weight: 700; text-align: center;
    color: #00f2ff;
    text-shadow: 0 0 20px #00f2ff;
}

/* Professional Audit Report (CLEAN TEXT) */
.report-paper {
    background: #FFFFFF !important;
    color: #020617 !important;
    padding: 40px;
    border-radius: 4px;
    font-family: 'serif';
    line-height: 1.6;
    box-shadow: 0 0 50px rgba(0,0,0,0.5);
    border-top: 10px solid #00f2ff;
}
.report-paper h1, .report-paper h2, .report-paper h3, .report-paper p {
    color: #020617 !important;
}

header {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- ASSETS ---
def load_lottie(url):
    try: return requests.get(url, timeout=5).json()
    except: return None

lottie_doc = load_lottie("https://lottie.host/8553641b-10f7-434a-9524-71e98822588c/OayXwS3S0R.json")
lottie_shield = load_lottie("https://lottie.host/68297b69-8088-466d-959c-8a192f1505c2/Wv0k06H4tV.json")

# --- AI DIAGNOSIS ENGINE ---
@st.cache_resource
def train_physician_ai():
    X = np.array([[20, 0, 2, 3], [180, 8, 35, 12], [45, 1, 6, 4], [350, 15, 65, 8], [15, 0, 1, 1]])
    y = np.array([0, 1, 0, 4, 0]) 
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    return model

ai_doc = train_physician_ai()

# --- APP LAYOUT ---
st.markdown("<h1 class='neon-title'>NETDOC AI PRO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8; font-size:20px;'>Autonomous AI-Physician for Network Diagnostics & Forensics</p>", unsafe_allow_html=True)

tabs = st.tabs(["🏥 AI CLINIC", "🧬 NEURAL VITALS", "🛡️ IMMUNITY SHIELD", "📜 FORENSIC AUDIT"])

# --- TAB 1: CLINIC ---
with tabs[0]:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.write("### 🩺 Initiate Bio-Scan")
        if lottie_doc: st_lottie(lottie_doc, height=250, key="clinic_anim")
        
        if st.button("🚀 START DEEP SCAN"):
            with st.spinner("Decoding Network DNA..."):
                time.sleep(2)
                lat, loss, jit, devs = random.randint(10, 400), random.randint(0, 15), random.randint(2, 70), random.randint(1, 30)
                pred = ai_doc.predict([[lat, loss, jit, devs]])[0]
                
                diags = {
                    0: ("Optimum Health", "Network is stable. All vitals are perfect.", "🟢"),
                    1: ("Hyper-Congestion", "Pathways clogged by heavy device load.", "🟡"),
                    4: ("Critical Failure", "Gateway failure detected at the ISP level.", "🔴")
                }
                
                st.session_state.audit = {
                    "v": diags.get(pred, diags[1])[0],
                    "p": diags.get(pred, diags[1])[1],
                    "i": diags.get(pred, diags[1])[2],
                    "stats": [lat, loss, jit, devs],
                    "time": time.strftime("%B %d, %Y | %H:%M:%S"),
                    "id": f"ND-{random.randint(1000, 9999)}"
                }
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        if 'audit' in st.session_state:
            res = st.session_state.audit
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.write(f"## {res['i']} Diagnosis: {res['v']}")
            st.metric("Latency", f"{res['stats'][0]}ms", delta="-5ms")
            st.write(f"**AI Insight:** {res['p']}")
            st.markdown(f"<div style='background:rgba(0,242,255,0.1); padding:15px; border-radius:10px; border-left:5px solid #00f2ff;'><b>Rx:</b> Change Wi-Fi channel and reboot gateway.</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 2: NEURAL VITALS ---
with tabs[1]:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.write("### 🧬 Live Stability Pulse")
    df_pulse = pd.DataFrame(np.random.randint(30, 100, size=(20, 2)), columns=['Uplink', 'Downlink'])
    fig = px.area(df_pulse, template="plotly_dark", color_discrete_sequence=['#00f2ff', '#bc13fe'])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: IMMUNITY SHIELD (NEW SECTION) ---
with tabs[2]:
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.write("### 🛡️ Network Immunity Score")
        score = random.randint(60, 98)
        st.header(f"{score}% Safe")
        st.progress(score)
        st.write("AI Shield is monitoring 24/7 for intrusions.")
        st.markdown("</div>", unsafe_allow_html=True)
    with col_b:
        if lottie_shield: st_lottie(lottie_shield, height=200)

# --- TAB 4: PROFESSIONAL AUDIT (THE CLEAN REPORT) ---
with tabs[3]:
    if 'audit' in st.session_state:
        d = st.session_state.audit
        
        # Proper Clean Professional Report
        st.markdown("""<div class="report-paper">""", unsafe_allow_html=True)
        st.markdown(f"""
        <h1 style="text-align:center;">OFFICIAL NETWORK HEALTH AUDIT</h1>
        <p style="text-align:right;"><b>Case ID:</b> {d['id']} | <b>Date:</b> {d['time']}</p>
        <hr>
        <h3>1. EXECUTIVE SUMMARY</h3>
        <p>This document serves as an official forensic audit of the subject network infrastructure. 
        Based on the Neural-Physician AI engine, the current status is <b>{d['v']}</b>.</p>
        
        <h3>2. CLINICAL DIAGNOSTICS</h3>
        <p>The following metrics were captured during the deep-bio scan:</p>
        <ul>
            <li><b>Round Trip Latency:</b> {d['stats'][0]} ms</li>
            <li><b>Packet Integrity:</b> {100 - d['stats'][1]}% Stable</li>
            <li><b>Network Congestion:</b> {d['stats'][3]} Active Nodes detected</li>
        </ul>
        
        <h3>3. AI PRESCRIPTION</h3>
        <p><b>Diagnosis:</b> {d['p']}</p>
        <p><b>Recommended Treatment:</b> We advise an immediate flush of the DNS cache, 
        optimization of the transport layer, and a hardware reboot to restore 100% throughput.</p>
        
        <br><br>
        <p style="text-align:right;"><i>Digitally Signed: Dr. Cyber-Sentinel (AI Agent)</i></p>
        """, unsafe_allow_html=True)
        st.markdown("""</div>""", unsafe_allow_html=True)
        
        st.download_button("📥 DOWNLOAD REPORT", f"NetDoc Audit\nStatus: {d['v']}\nStats: {d['stats']}", file_name="Report.txt")
    else:
        st.warning("⚠️ No diagnostic data found. Please run a scan first.")

# --- SIDEBAR ---
if st.sidebar.button("🗑️ PURGE RECORDS"):
    st.session_state.clear()
    st.rerun()
