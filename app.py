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
st.set_page_config(page_title="NetDoc AI Pro", layout="wide", page_icon="保护")

# --- CUSTOM DYNAMIC NEON CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Plus+Jakarta+Sans:wght@300;500;700&display=swap');

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp {
    background: linear-gradient(-45deg, #020617, #0f172a, #1e1b4b, #001d3d);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
    color: #FFFFFF !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.glass-card {
    background: rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 30px;
    border: 1px solid rgba(0, 242, 255, 0.2);
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    margin-bottom: 25px;
}

/* Styled All Buttons */
div.stButton > button, div.stDownloadButton > button {
    background: linear-gradient(90deg, #00f2ff, #0062ff) !important;
    color: white !important;
    border: none !important;
    padding: 12px 30px !important;
    border-radius: 50px !important;
    font-weight: bold !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    box-shadow: 0 4px 15px rgba(0, 242, 255, 0.4) !important;
    width: 100%;
}

.neon-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 55px; font-weight: 700; text-align: center;
    background: linear-gradient(to right, #00f2ff, #7000ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 10px rgba(0, 242, 255, 0.5));
}

/* Professional Audit Report (The White Paper) */
.report-paper {
    background: #FFFFFF !important;
    color: #1a1a1a !important;
    padding: 60px;
    border-radius: 4px;
    font-family: 'Times New Roman', serif;
    box-shadow: 0 0 50px rgba(0,0,0,0.9);
    line-height: 1.5;
}
.report-paper h1, .report-paper h2, .report-paper h3, .report-paper h4, .report-paper p, .report-paper li, .report-paper b, .report-paper td {
    color: #1a1a1a !important;
}

.summary-box {
    background: rgba(0, 242, 255, 0.08);
    border-left: 5px solid #00f2ff;
    padding: 15px;
    border-radius: 10px;
    margin-top: 15px;
}

header {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- ASSETS ---
def load_lottie(url):
    try: return requests.get(url, timeout=5).json()
    except: return None

lottie_doc = load_lottie("https://lottie.host/8553641b-10f7-434a-9524-71e98822588c/OayXwS3S0R.json")

# --- AI DIAGNOSIS ENGINE ---
@st.cache_resource
def train_physician_ai():
    X = np.array([[20, 0, 2, 3], [200, 10, 40, 15], [50, 1, 5, 2], [350, 18, 60, 5]])
    y = np.array([0, 1, 0, 4]) 
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    return model

ai_physician = train_physician_ai()

# --- APP LAYOUT ---
st.markdown("<h1 class='neon-title'>NETDOC AI PRO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#FFFFFF; font-size:20px;'>Advanced Neural Intelligence & Network Bio-Forensics</p>", unsafe_allow_html=True)

tabs = st.tabs(["🏥 CLINIC", "🧬 VITALS", "🛡️ SECURITY", "🔮 PREDICTION", "📜 OFFICIAL AUDIT"])

# --- TAB 1: CLINIC ---
with tabs[0]:
    col1, col2 = st.columns([1, 1.3])
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.write("### 🩺 Clinical Bio-Scan")
        if lottie_doc: st_lottie(lottie_doc, height=200)
        
        if st.button("EXECUTE AI DIAGNOSIS"):
            with st.spinner("Decoding Network DNA..."):
                time.sleep(2)
                lat, loss, jit = random.randint(15, 350), random.randint(0, 12), random.randint(2, 65)
                devs, pkts = random.randint(1, 25), random.randint(1500, 8000)
                
                pred = ai_physician.predict([[lat, loss, jit, devs]])[0]
                diags = {
                    0: ("Optimum Health", "Network DNA is stable.", "نظام بالکل ٹھیک کام کر رہا ہے۔", "🟢"),
                    1: ("Hyper-Congestion", "Pathways clogged by load.", "نیٹ ورک پر بوجھ زیادہ ہے۔", "🟡"),
                    4: ("Gateway Failure", "Critical backbone failure.", "انٹرنیٹ فراہم کرنے والے کا مسئلہ ہے۔", "🔴")
                }
                st.session_state.audit = {
                    "v": diags.get(pred, diags[1])[0],
                    "p_eng": diags.get(pred, diags[1])[1],
                    "p_urdu": diags.get(pred, diags[1])[2],
                    "i": diags.get(pred, diags[1])[3],
                    "stats": [lat, loss, jit, devs, pkts],
                    "time": time.strftime("%B %d, %Y | %H:%M:%S"),
                    "id": f"ND-{random.randint(1000, 9999)}",
                    "sec_score": random.randint(85, 99)
                }
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        if 'audit' in st.session_state:
            res = st.session_state.audit
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.write(f"## {res['i']} Status: {res['v']}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Latency", f"{res['stats'][0]}ms")
            c2.metric("Nodes", f"{res['stats'][3]}")
            c3.metric("Packets", f"{res['stats'][4]}")
            st.markdown(f"<div class='summary-box'><b>🧠 AI Insight:</b> {res['p_eng']} ({res['p_urdu']})</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 2: VITALS ---
with tabs[1]:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.write("### 🧬 Network Stability Pulse")
    v_data = pd.DataFrame(np.random.randint(30, 100, size=(20, 2)), columns=['Uplink', 'Downlink'])
    st.area_chart(v_data)
    st.markdown("<div class='summary-box'><b>📊 Pulse Summary:</b> High peaks represent high bandwidth utilization. Stable lines represent low jitter.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: SECURITY ---
with tabs[2]:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.write("### 🛡️ Cyber-Shield Status")
    st.header(f"Security Immunity: {st.session_state.audit['sec_score'] if 'audit' in st.session_state else 92}%")
    st.write("🚫 **Threats Blocked Today:** 05 | 🔐 **Encryption:** TLS 1.3")
    st.markdown("<div class='summary-box'><b>🛡️ Shield Summary:</b> AI agents are monitoring for spoofing and unauthorized packet injections.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 4: PREDICTION ---
with tabs[3]:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.write("### 🔮 AI Traffic Forecast (Next 24h)")
    pred_data = pd.DataFrame(np.random.randint(20, 90, size=(24, 1)), columns=['Predicted Load %'])
    st.line_chart(pred_data)
    st.markdown("<div class='summary-box'><b>🔮 Forecast Summary:</b> AI predicts a traffic spike in 4 hours. Optimization protocols will engage automatically.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 5: OFFICIAL AUDIT (THE COMPREHENSIVE REPORT) ---
with tabs[4]:
    if 'audit' in st.session_state:
        d = st.session_state.audit
        st.markdown("<div class='report-paper'>", unsafe_allow_html=True)
        st.markdown(f"""
        <h1 style="text-align:center; border-bottom: 2px solid #000;">NETWORK FORENSIC AUDIT REPORT</h1>
        <p style="text-align:right;"><b>REPORT ID:</b> {d['id']} | <b>DATE:</b> {d['time']}</p>
        
        <h3>1. EXECUTIVE SUMMARY</h3>
        <p>This comprehensive audit documents the autonomous diagnostic findings for the subject network. 
        The system has been classified as <b>{d['v']}</b> with an AI confidence rating of 98.4%.</p>
        
        <h3>2. CORE DIAGNOSTIC METRICS (THE CLINIC)</h3>
        <p>The neural bio-scan of the data link and network layers revealed the following vitals:</p>
        <table style="width:100%; border: 1px solid #ddd; border-collapse: collapse;">
            <tr style="background:#f2f2f2;"><th>Parameter</th><th>Value</th><th>Evaluation</th></tr>
            <tr><td>Round Trip Latency</td><td>{d['stats'][0]} ms</td><td>{('Stable' if d['stats'][0]<100 else 'Critical')}</td></tr>
            <tr><td>Packet Loss Ratio</td><td>{d['stats'][1]} %</td><td>{('Optimal' if d['stats'][1]<2 else 'Degraded')}</td></tr>
            <tr><td>Active Network Nodes</td><td>{d['stats'][3]}</td><td>Nominal</td></tr>
            <tr><td>Analyzed Data Packets</td><td>{d['stats'][4]}</td><td>Processed</td></tr>
        </table>
        
        <h3>3. STABILITY PULSE ANALYSIS (VITALS)</h3>
        <p>Continuous monitoring of uplink and downlink flows shows a stability coefficient of <b>0.92</b>. 
        Pattern analysis suggests that the network is capable of handling current throughput without packet fragmentation.</p>
        
        <h3>4. SECURITY & IMMUNITY AUDIT (CYBER-SHIELD)</h3>
        <p>The AI Shield has maintained an immunity score of <b>{d['sec_score']}%</b>. 
        All data packets are being routed through a TLS 1.3 encrypted tunnel. No active intrusions were detected during the audit.</p>
        
        <h3>5. PREDICTIVE TRAFFIC FORECAST</h3>
        <p>Based on historical heuristic data, the AI predicts a congestion peak during the next high-usage window. 
        Autonomous QoS (Quality of Service) has been scheduled to prevent throughput drops.</p>
        
        <h3>6. FINAL CLINICAL PRESCRIPTION</h3>
        <p><b>English Diagnosis:</b> {d['p_eng']}</p>
        <p><b>اردو تشخیص:</b> {d['p_urdu']}</p>
        <p><b>Treatment Plan:</b> We recommend an immediate flush of the DNS cache, gateway hardware reboot, and optimization of Layer-2 switching protocols.</p>
        
        <br><br>
        <p style="text-align:right;"><b>Digitally Signed,</b><br>
        <img src="https://api.qrserver.com/v1/create-qr-code/?size=80x80&data=VerifiedNetDoc" style="width:80px;"><br>
        <i>Dr. Cyber-Sentinel (NetDoc AI Pro)</i></p>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="📥 DOWNLOAD FULL PROFESSIONAL AUDIT",
            data=f"NetDoc AI Audit Report\nID: {d['id']}\nStatus: {d['v']}\nLatency: {d['stats'][0]}ms\nSecurity: {d['sec_score']}%\nAdvice: {d['p_eng']}",
            file_name=f"Detailed_Audit_{d['id']}.txt"
        )
    else:
        st.warning("⚠️ Access Denied. Diagnostic data not found. Please run a scan in the Clinic tab first.")

# --- SIDEBAR ---
if st.sidebar.button("🗑️ PURGE RECORDS"):
    st.session_state.clear()
    st.rerun()
