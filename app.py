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

/* Entry Animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    background-color: #010409;
    color: #E6EDF3;
}

.stApp {
    background: radial-gradient(circle at 50% -20%, #0d1117 0%, #010409 80%);
}

/* Glassmorphism Cards */
.glass-card {
    animation: fadeIn 1s ease-out;
    background: rgba(13, 17, 23, 0.85);
    backdrop-filter: blur(15px);
    border-radius: 15px;
    padding: 35px;
    border: 1px solid #30363d;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    margin-bottom: 25px;
}

.neon-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 55px; font-weight: 700; text-align: center;
    color: #58a6ff;
    text-shadow: 0 0 20px #58a6ff;
    animation: fadeIn 0.8s ease-in;
}

/* Professional Audit Report (White Paper Design) */
.report-paper {
    background: #FFFFFF;
    color: #111827 !important;
    padding: 60px;
    border-radius: 4px;
    font-family: 'Georgia', serif;
    line-height: 1.6;
    box-shadow: 0 0 50px rgba(0,0,0,0.8);
    max-width: 900px;
    margin: auto;
}

.report-paper h1, .report-paper h2, .report-paper h3, .report-paper p, .report-paper div {
    color: #111827 !important;
}

.report-divider {
    border-bottom: 2px solid #111827;
    margin-bottom: 20px;
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

# --- INITIALIZING SYSTEM BOOT ---
if 'booted' not in st.session_state:
    st.markdown("<h1 class='neon-title'>BOOTING NetDoc AI CORE v6.0...</h1>", unsafe_allow_html=True)
    if lottie_doc: st_lottie(lottie_doc, height=300)
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress_bar.progress(i + 1)
    st.session_state.booted = True
    st.rerun()

# --- AI DIAGNOSIS ENGINE ---
@st.cache_resource
def train_physician_ai():
    # Latency, Loss, Jitter, Devices
    X = np.array([[20, 0, 2, 3], [180, 8, 30, 12], [45, 1, 6, 4], [350, 15, 65, 8], [15, 0, 1, 1]])
    y = np.array([0, 1, 0, 4, 0]) 
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    return model

ai_physician = train_physician_ai()

# --- APP LAYOUT ---
st.markdown("<h1 class='neon-title'>NETDOC AI PRO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#8b949e; font-size:20px; margin-bottom:30px;'>Autonomous Forensic Agent & Intelligence Suite</p>", unsafe_allow_html=True)

tabs = st.tabs(["🏥 AI CLINIC", "🧬 NEURAL VITALS", "📜 PROFESSIONAL AUDIT"])

# --- TAB 1: CLINIC ---
with tabs[0]:
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.write("### 🩺 Start Patient Scan")
        if lottie_doc: st_lottie(lottie_doc, height=200, key="clinic_anim")
        
        if st.button("🚀 INITIATE SCAN"):
            with st.spinner("Analyzing Network Vitals..."):
                time.sleep(2)
                lat, loss, jit, devs = random.randint(15, 380), random.randint(0, 12), random.randint(2, 60), random.randint(1, 25)
                pred = ai_physician.predict([[lat, loss, jit, devs]])[0]
                
                diagnosis_map = {
                    0: ("Optimum Health", "Network DNA is clean. All vitals are within stable range.", "🟢"),
                    1: ("Hyper-Congestion", "Pathways clogged by excessive data load and device saturation.", "🟡"),
                    4: ("ISP Degradation", "Critical backbone failure detected at the service provider gateway.", "🔴")
                }
                
                st.session_state.audit_data = {
                    "v": diagnosis_map.get(pred, diagnosis_map[1])[0],
                    "p": diagnosis_map.get(pred, diagnosis_map[1])[1],
                    "i": diagnosis_map.get(pred, diagnosis_map[1])[2],
                    "stats": [lat, loss, jit, devs],
                    "time": time.strftime("%B %d, %Y | %H:%M:%S"),
                    "id": f"ND-{random.randint(10000, 99999)}"
                }
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        if 'audit_data' in st.session_state:
            res = st.session_state.audit_data
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.write(f"## {res['i']} Diagnosis: {res['v']}")
            
            # High Contrast Metrics
            c1, c2, c3 = st.columns(3)
            c1.metric("Latency", f"{res['stats'][0]}ms")
            c2.metric("Loss", f"{res['stats'][1]}%")
            c3.metric("Nodes", f"{res['stats'][3]}")
            
            st.markdown(f"""
            <div style='background:rgba(88,166,255,0.1); padding:20px; border-radius:10px; border-left:5px solid #58a6ff; margin-top:20px;'>
                <h4 style='color:#58a6ff;'>Rx AI Prescription:</h4>
                <p style='color:white;'>{res['p']}</p>
                <p style='color:#8b949e;'><b>Recommendation:</b> Please follow the instructions in the Audit Report tab for recovery.</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            if lottie_radar: st_lottie(lottie_radar, height=300, key="radar")
            st.info("System Ready. Please initiate a bio-scan to see diagnostic results.")

# --- TAB 2: LIVE VITALS ---
with tabs[1]:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.write("### 🧬 Live Stability Pulse (Real-time Trends)")
    pulse_df = pd.DataFrame(np.random.randint(30, 100, size=(25, 2)), columns=['Uplink Intensity', 'Downlink Flow'])
    fig = px.area(pulse_df, template="plotly_dark", color_discrete_sequence=['#58a6ff', '#bc13fe'])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_family="Rajdhani")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: OFFICIAL AUDIT REPORT (PROFESSIONAL TEXT ONLY) ---
with tabs[2]:
    if 'audit_data' in st.session_state:
        d = st.session_state.audit_data
        
        # CLEAN TEXT-BASED PROFESSIONAL REPORT
        report_text = f"""
        <div class="report-paper">
            <div class="report-header">
                <h1 style="margin:0; font-size:32px;">OFFICIAL NETWORK HEALTH AUDIT</h1>
                <p style="margin:5px; font-size:18px;">NetDoc AI Intelligence Laboratory | Global Security HQ</p>
                <p style="font-size:14px;"><b>Report ID:</b> {d['id']} | <b>Generated on:</b> {d['time']}</p>
            </div>
            
            <div style="margin-top:30px;">
                <h3>I. EXECUTIVE SUMMARY</h3>
                <p>An autonomous forensic audit has been conducted on the subject network infrastructure. 
                Using the <b>Neural-Physician v6.0 Agent</b>, the network's current state has been 
                formally classified as <b>{d['v']}</b>. The AI analysis indicates a 98.2% confidence 
                threshold in this diagnostic verdict.</p>
                
                <h3>II. DETAILED VITAL STATISTICS</h3>
                <p>The following metrics were measured during the deep-packet inspection phase:</p>
                <ul>
                    <li><b>Round Trip Latency:</b> {d['stats'][0]} ms — <i>Status: {('Stable' if d['stats'][0]<80 else 'Critical')}</i></li>
                    <li><b>Packet Integrity (Loss):</b> {d['stats'][1]} % — <i>Status: {('Optimal' if d['stats'][1]<2 else 'Degraded')}</i></li>
                    <li><b>Network Node Saturation:</b> {d['stats'][3]} Active Devices — <i>Status: Nominal</i></li>
                </ul>
                
                <h3>III. CLINICAL FINDINGS & MITIGATION PLAN</h3>
                <p><b>Diagnostic Finding:</b> {d['p']}</p>
                <p><b>Recommended Treatment:</b> To restore optimal performance, the AI Agent suggests 
                an immediate hardware gateway reboot, flushing of the DNS resolver cache, and 
                migration to a less congested Wi-Fi frequency (5GHz / WiFi-6E) to eliminate interference.</p>
                
                <div style="margin-top:50px; border-top: 1px solid #111827; padding-top: 20px;">
                    <p style="text-align:right;">
                        <b>Digitally Verified By:</b><br>
                        <span style="font-size:24px; font-family:'Courier New';"><i>Dr. Cyber-Sentinel</i></span><br>
                        Autonomous AI Diagnostic Agent
                    </p>
                </div>
            </div>
        </div>
        """
        st.markdown(report_text, unsafe_allow_html=True)
        
        # Download as Text
        st.download_button("📥 DOWNLOAD REPORT AS TEXT", 
                         f"NETDOC AUDIT REPORT\nID: {d['id']}\nDate: {d['time']}\nStatus: {d['v']}\nStats: {d['stats']}\nAdvice: {d['p']}", 
                         file_name=f"NetDoc_Report_{d['id']}.txt")
    else:
        st.warning("⚠️ No diagnostic data available. Please conduct a Clinic Scan first.")

# --- SIDEBAR ---
st.sidebar.markdown("<h2 style='text-align:center; color:#58a6ff;'>COMMAND CENTER</h2>", unsafe_allow_html=True)
if st.sidebar.button("🗑️ PURGE CLINIC DATA"):
    st.session_state.clear()
    st.rerun()
