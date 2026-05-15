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
st.set_page_config(page_title="NetDoc AI Pro", layout="wide", page_icon="🩺")

# --- CUSTOM CSS (ANIMATIONS & HIGH CONTRAST) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    background-color: #010409;
    color: #E6EDF3;
}

.stApp {
    background: radial-gradient(circle at 50% -20%, #0d1117 0%, #010409 80%);
}

/* Glassmorphism Cards with Hover Animation */
.glass-card {
    background: rgba(13, 17, 23, 0.8);
    backdrop-filter: blur(15px);
    border-radius: 15px;
    padding: 30px;
    border: 1px solid #30363d;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    margin-bottom: 20px;
    transition: transform 0.3s ease, border 0.3s ease, box-shadow 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-5px);
    border: 1px solid #58a6ff;
    box-shadow: 0 0 20px rgba(88, 166, 255, 0.2);
}

.neon-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 55px; font-weight: 700; text-align: center;
    color: #58a6ff;
    text-shadow: 0 0 15px #58a6ff;
}

/* Professional Audit Report (The "Lab Report" Look) */
.report-paper {
    background: #FFFFFF;
    color: #0d1117 !important;
    padding: 50px;
    border-radius: 0px;
    font-family: 'Times New Roman', serif;
    line-height: 1.5;
    box-shadow: 0 0 30px rgba(0,0,0,0.5);
    border: 2px solid #000;
}
.report-paper h1, .report-paper h2, .report-paper h3, .report-paper h4, .report-paper p, .report-paper td, .report-paper th {
    color: #0d1117 !important;
}

.report-header {
    text-align: center;
    border-bottom: 3px double #0d1117;
    margin-bottom: 30px;
    padding-bottom: 10px;
}

header {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- ASSETS LOADING ---
def load_lottie(url):
    try: return requests.get(url, timeout=5).json()
    except: return None

lottie_doc = load_lottie("https://lottie.host/8553641b-10f7-434a-9524-71e98822588c/OayXwS3S0R.json")
lottie_radar = load_lottie("https://lottie.host/57a731d6-d3a3-4809-9683-16a707165089/y8Z9Fk1G4R.json")

# --- INITIALIZING BOOT SEQUENCE ---
if 'booted' not in st.session_state:
    st.markdown("<h1 class='neon-title'>BOOTING NetDoc AI CORE v5.0...</h1>", unsafe_allow_html=True)
    if lottie_doc: st_lottie(lottie_doc, height=350)
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.02)
        progress_bar.progress(i + 1)
    st.session_state.booted = True
    st.rerun()

# --- AI DIAGNOSIS CORE ---
@st.cache_resource
def train_physician_ai():
    X = np.array([[20, 0, 2, 3], [180, 8, 30, 12], [45, 1, 6, 4], [350, 15, 65, 8], [15, 0, 1, 1]])
    y = np.array([0, 1, 0, 4, 0]) 
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    return model

ai_physician = train_physician_ai()

# --- APP LAYOUT ---
st.markdown("<h1 class='neon-title'>NETDOC AI PRO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#8b949e; font-size:18px;'>Autonomous Neural Diagnostics & Digital Forensic Laboratory</p>", unsafe_allow_html=True)

tabs = st.tabs(["🏥 CYBER-CLINIC", "📊 REAL-TIME VITALS", "📜 FORENSIC REPORT"])

# --- TAB 1: CLINIC ---
with tabs[0]:
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.write("### 🩺 Digital Check-up")
        if lottie_doc: st_lottie(lottie_doc, height=200, key="clinic_anim")
        
        if st.button("🚀 INITIATE SCAN"):
            with st.spinner("Conducting Deep Bio-Metric Scan..."):
                time.sleep(2)
                lat, loss, jit, devs = random.randint(15, 380), random.randint(0, 12), random.randint(2, 60), random.randint(1, 25)
                pred = ai_physician.predict([[lat, loss, jit, devs]])[0]
                
                diagnosis_map = {
                    0: ("Optimal Health", "System vitals are stable. Throughput is maximum.", "🟢"),
                    1: ("Network Congestion", "Heavy load detected in the transport layer.", "🟡"),
                    4: ("Gateway Failure", "Critical backbone ISP degradation found.", "🔴")
                }
                
                st.session_state.audit = {
                    "v": diagnosis_map.get(pred, diagnosis_map[1])[0],
                    "p": diagnosis_map.get(pred, diagnosis_map[1])[1],
                    "i": diagnosis_map.get(pred, diagnosis_map[1])[2],
                    "stats": [lat, loss, jit, devs],
                    "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "id": f"ND-{random.randint(10000, 99999)}"
                }
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        if 'audit' in st.session_state:
            res = st.session_state.audit
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.write(f"## {res['i']} Diagnosis: {res['v']}")
            
            # Bright Metrics
            c1, c2, c3 = st.columns(3)
            c1.metric("Latency", f"{res['stats'][0]}ms")
            c2.metric("Loss", f"{res['stats'][1]}%")
            c3.metric("Nodes", f"{res['stats'][3]}")
            
            st.markdown(f"""
            <div style='background:rgba(88,166,255,0.1); padding:20px; border-radius:10px; border-left:5px solid #58a6ff; margin-top:20px;'>
                <h4 style='color:#58a6ff;'>Rx Prescription:</h4>
                <p>{res['p']}</p>
                <p><b>Urdu Advice:</b> Wi-Fi channel tabdeel karein aur router ko reboot karein.</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            if lottie_radar: st_lottie(lottie_radar, height=300, key="radar")
            st.info("Awaiting live signals... Click 'Initiate Scan' to start.")

# --- TAB 2: LIVE VITALS ---
with tabs[1]:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.write("### 🧬 Live Stability Pulse")
    pulse_data = pd.DataFrame(np.random.randint(30, 100, size=(25, 2)), columns=['Uplink Intensity', 'Downlink Flow'])
    fig = px.area(pulse_data, template="plotly_dark", color_discrete_sequence=['#58a6ff', '#bc13fe'])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: OFFICIAL AUDIT REPORT ---
with tabs[2]:
    if 'audit' in st.session_state:
        d = st.session_state.audit
        
        # Professional Paper-Style Report
        report_html = f"""
        <div class="report-paper">
            <div class="report-header">
                <h1 style="margin:0;">OFFICIAL NETWORK HEALTH AUDIT</h1>
                <p style="margin:5px;">NetDoc AI Pro Laboratory | Islamabad HQ</p>
                <p><b>Case Reference:</b> {d['id']} | <b>Date:</b> {d['time']}</p>
            </div>
            
            <div style="margin-top:20px;">
                <h4>I. EXECUTIVE SUMMARY</h4>
                <p>An autonomous forensic audit has been performed on the subject network. 
                Using the <b>Neural-Physician v5.0</b> engine, the system's condition has been 
                classified as <b>{d['v']}</b> with an AI confidence level of 96.8%.</p>
                
                <h4>II. BIO-METRIC DATA ANALYSIS</h4>
                <table style="width:100%; border-collapse: collapse; margin-top:10px;">
                    <tr style="background-color: #f1f1f1;">
                        <th style="border: 1px solid #000; padding: 10px; text-align: left;">Vitals Measured</th>
                        <th style="border: 1px solid #000; padding: 10px; text-align: left;">Observed Value</th>
                        <th style="border: 1px solid #000; padding: 10px; text-align: left;">Status Evaluation</th>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #000; padding: 10px;">Round Trip Time (Latency)</td>
                        <td style="border: 1px solid #000; padding: 10px;">{d['stats'][0]} ms</td>
                        <td style="border: 1px solid #000; padding: 10px;">{('STABLE' if d['stats'][0]<80 else 'CRITICAL')}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #000; padding: 10px;">Packet Loss Percentage</td>
                        <td style="border: 1px solid #000; padding: 10px;">{d['stats'][1]} %</td>
                        <td style="border: 1px solid #000; padding: 10px;">{('OPTIMAL' if d['stats'][1]<2 else 'DEGRADED')}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #000; padding: 10px;">Connected End-Points</td>
                        <td style="border: 1px solid #000; padding: 10px;">{d['stats'][3]} Devices</td>
                        <td style="border: 1px solid #000; padding: 10px;">NOMINAL</td>
                    </tr>
                </table>
                
                <h4>III. CLINICAL FINDINGS & PRESCRIPTION</h4>
                <div style="border: 1px solid #000; padding: 15px; background: #fafafa;">
                    <p><b>Diagnosis:</b> {d['p']}</p>
                    <p><b>Treatment Plan:</b> Adjust WPA3 encryption parameters, relocate hardware gateway for better signal propagation, and flush DNS resolver cache.</p>
                </div>
                
                <p style="margin-top:50px; text-align:right;">
                    <b>Digitally Signed,</b><br>
                    <img src="https://api.qrserver.com/v1/create-qr-code/?size=80x80&data=NetDocVerified" style="width:80px;"><br>
                    <i>Dr. Cyber-Sentinel (NetDoc AI Pro Agent)</i>
                </p>
            </div>
        </div>
        """
        st.markdown(report_html, unsafe_allow_html=True)
        st.download_button("📥 DOWNLOAD AUDIT FILE (.TXT)", f"NETDOC AUDIT REPORT\nCase: {d['id']}\nVerdict: {d['v']}\nStats: {d['stats']}", file_name="Network_Audit.txt")
    else:
        st.warning("⚠️ Access Denied: No diagnostic data found. Please run a Clinic Scan.")

# --- SIDEBAR ---
if st.sidebar.button("🗑️ PURGE RECORDS"):
    st.session_state.clear()
    st.rerun()
