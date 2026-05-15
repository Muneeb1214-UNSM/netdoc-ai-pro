import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
import time
import random
from streamlit_lottie import st_lottie
import requests

# --- ADVANCED CONFIG ---
st.set_page_config(page_title="NetSentinel AI", layout="wide", page_icon="🛡️")

# --- CYBER HUD THEME ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    .stApp { background: #000b1a; color: #00ffcc; font-family: 'Share Tech Mono', monospace; }
    .agent-box {
        border: 1px solid #00ffcc; border-radius: 5px; padding: 15px;
        background: rgba(0, 255, 204, 0.05); box-shadow: inset 0 0 10px #00ffcc;
    }
    .status-healing { color: #ff0055; font-weight: bold; animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    .header-style { text-shadow: 0 0 20px #00ffcc; font-size: 40px; text-align: center; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- AI AGENT BRAIN ---
@st.cache_resource
def initialize_agent():
    # Features: [Packet Vol, Time Gap, Connection Rate]
    X = np.array([[100, 0.5, 10], [1500, 0.1, 100], [50, 0.8, 5], [40, 0.01, 500], [1200, 0.4, 2]])
    y = np.array([0, 1, 0, 1, 0]) # 0: Healthy, 1: Attack
    model = RandomForestClassifier(n_estimators=50)
    model.fit(X, y)
    return model

sentinel_model = initialize_agent()

# --- ASSETS LOADING ---
def load_lottie(url):
    try: return requests.get(url, timeout=5).json()
    except: return None

lottie_sentinel = load_lottie("https://lottie.host/89047d28-3e4e-4f05-950c-7b1968538f97/Ym9Kj0B21s.json")

# --- INITIALIZING SESSION STATES ---
if 'logs' not in st.session_state: st.session_state.logs = []
if 'blocked_ips' not in st.session_state: st.session_state.blocked_ips = set()
if 'network_health' not in st.session_state: st.session_state.network_health = 100

# --- CORE AGENT LOGIC (Self-Healing) ---
def run_autonomous_agent():
    # Simulate incoming traffic
    ip_source = f"192.168.1.{random.randint(10, 255)}"
    vol = random.randint(40, 1600)
    gap = random.uniform(0.01, 1.0)
    rate = random.randint(1, 600)
    
    # AI Verdict
    prediction = sentinel_model.predict([[vol, gap, rate]])[0]
    verdict = "THREAT" if prediction == 1 else "HEALTHY"
    
    action = "MONITORING"
    if verdict == "THREAT" and ip_source not in st.session_state.blocked_ips:
        action = "MITIGATING (Self-Healing...)"
        st.session_state.blocked_ips.add(ip_source)
        st.session_state.network_health -= 5
    elif verdict == "HEALTHY":
        if st.session_state.network_health < 100:
            st.session_state.network_health += 1 # Healing back
            action = "HEALING SYSTEM"

    new_log = {
        "Timestamp": time.strftime("%H:%M:%S"),
        "Source_IP": ip_source,
        "Verdict": verdict,
        "Agent_Action": action,
        "Health": f"{st.session_state.network_health}%"
    }
    st.session_state.logs.append(new_log)
    if len(st.session_state.logs) > 20: st.session_state.logs.pop(0)

# --- APP LAYOUT ---
st.markdown("<h1 class='header-style'>NET-SENTINEL: AUTONOMOUS AGENT</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>AI-Powered Autonomous Threat Detection & Self-Healing System</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("<div class='agent-box'>", unsafe_allow_html=True)
    st.write("### AGENT STATUS")
    if lottie_sentinel: st_lottie(lottie_sentinel, height=150)
    st.write(f"**Mode:** Autonomous")
    st.write(f"**Uptime:** 99.99%")
    st.write(f"**IPs Blocked:** {len(st.session_state.blocked_ips)}")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    run_autonomous_agent()
    latest = st.session_state.logs[-1]
    
    # Real-time Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("SYSTEM HEALTH", latest['Health'])
    m2.metric("LATEST VERDICT", latest['Verdict'])
    m3.metric("AGENT ACTION", "BLOCKING" if "MITIGATING" in latest['Agent_Action'] else "STABLE")

    # Visualizing AI History
    df = pd.DataFrame(st.session_state.logs)
    fig = px.line(df, x="Timestamp", y="Health", title="Real-time Network Resilience (Self-Healing Graph)")
    fig.update_traces(line_color='#00ffcc', fill='toself')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="#00ffcc")
    st.plotly_chart(fig, use_container_width=True)

with col3:
    st.markdown("<div class='agent-box'>", unsafe_allow_html=True)
    st.write("### 🛡️ ACTIVE FIREWALL")
    if st.session_state.blocked_ips:
        for ip in list(st.session_state.blocked_ips)[-5:]:
            st.error(f"BLOCKED: {ip}")
    else:
        st.write("No threats detected.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.write("### 📜 AUTONOMOUS AGENT EXECUTION LOGS")
st.table(df.iloc[::-1].head(10))

# Auto-Refresh to simulate live stream
time.sleep(1.5)
st.rerun()
