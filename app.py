import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
import time
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="QoS-Flow AI", layout="wide", page_icon="⚡")

# --- ULTRA-MODERN CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500&display=swap');
    
    /* Background & Global Styles */
    .stApp {
        background: radial-gradient(circle at center, #0a192f 0%, #02050a 100%);
        color: #e0e0e0;
        font-family: 'Rajdhani', sans-serif;
    }

    /* Glassmorphism Card Style */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(0, 242, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        transition: 0.3s ease-in-out;
    }
    .glass-card:hover {
        border: 1px solid rgba(0, 242, 255, 0.5);
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
    }

    /* Neon Titles */
    .neon-title {
        font-family: 'Orbitron', sans-serif;
        color: #00f2ff;
        text-shadow: 0 0 10px #00f2ff, 0 0 20px #00f2ff;
        text-align: center;
        letter-spacing: 2px;
    }

    /* Custom Metrics */
    .metric-value {
        font-size: 30px;
        font-weight: bold;
        color: #00f2ff;
    }
    
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- ASSETS LOADING ---
def load_lottie(url):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except:
        return None

# Naya fast aur stable animation
lottie_ai_brain = load_lottie("https://lottie.host/8553641b-10f7-434a-9524-71e98822588c/OayXwS3S0R.json")

# --- DATA STATE ---
if 'qos_history' not in st.session_state:
    st.session_state.qos_history = pd.DataFrame(columns=["Time", "App", "Priority", "Ping", "Allocated_BW"])

def run_ai_logic(mode):
    # Simulated Network Behavior
    apps = ["Discord (Voice)", "Zoom Meeting", "Steam (Gaming)", "Netflix 4K", "Windows Update"]
    app = random.choice(apps)
    
    # Priority Logic based on User Choice
    if mode == "Gaming Mode" and "Steam" in app:
        priority, ping, bw = "⚡ CRITICAL", random.randint(15, 30), random.randint(85, 98)
    elif mode == "Work Mode" and ("Zoom" in app or "Discord" in app):
        priority, ping, bw = "💎 HIGH", random.randint(30, 60), random.randint(70, 90)
    else:
        priority = "🔹 NORMAL"
        ping = random.randint(100, 250)
        bw = random.randint(10, 40)

    new_data = {
        "Time": time.strftime("%H:%M:%S"),
        "App": app,
        "Priority": priority,
        "Ping": ping,
        "Allocated_BW": bw
    }
    
    st.session_state.qos_history = pd.concat([st.session_state.qos_history, pd.DataFrame([new_data])], ignore_index=True)
    if len(st.session_state.qos_history) > 15:
        st.session_state.qos_history = st.session_state.qos_history.iloc[1:]
    return new_data

# --- APP LAYOUT ---
st.markdown("<h1 class='neon-title'>QoS-FLOW AI COMMANDER</h1>", unsafe_allow_html=True)

# Sidebar with glass look
st.sidebar.markdown("<h2 style='color:#00f2ff; font-family:Orbitron;'>CONTROL PANEL</h2>", unsafe_allow_html=True)
st.sidebar.write("Configure AI Priority Level:")
mode = st.sidebar.selectbox("Optimization Profile", ["Auto AI", "Gaming Mode", "Work Mode", "Silent Background"])

st.sidebar.markdown("---")
st.sidebar.info("🤖 AI is currently re-routing packets through the fastest gateway to minimize jitter.")

# Main Dashboard
col_main, col_side = st.columns([2, 1])

with col_side:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.write("### AI STATUS")
    if lottie_ai_brain:
        st_lottie(lottie_ai_brain, height=180, key="brain")
    else:
        st.markdown("<h1 style='text-align:center;'>🧠</h1>", unsafe_allow_html=True)
    
    current = run_ai_logic(mode)
    
    st.write(f"**Detecting Activity:**")
    st.markdown(f"<p class='metric-value'>{current['App']}</p>", unsafe_allow_html=True)
    st.write(f"**AI Assigned Priority:**")
    st.write(current['Priority'])
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Latency Meter
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.write("### NETWORK PING")
    fig_ping = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = current['Ping'],
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [None, 300], 'tickcolor': "#00f2ff"},
                 'bar': {'color': "#00f2ff"},
                 'steps': [
                     {'range': [0, 60], 'color': "rgba(0, 255, 0, 0.1)"},
                     {'range': [60, 150], 'color': "rgba(255, 255, 0, 0.1)"},
                     {'range': [150, 300], 'color': "rgba(255, 0, 0, 0.1)"}]}
    ))
    fig_ping.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Rajdhani"}, height=200, margin=dict(l=20, r=20, t=30, b=0))
    st.plotly_chart(fig_ping, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_main:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.write("### LIVE BANDWIDTH OPTIMIZATION")
    
    df = st.session_state.qos_history
    if not df.empty:
        fig_line = px.area(df, x="Time", y="Allocated_BW", title="Real-time Resource Allocation",
                          color_discrete_sequence=['#00f2ff'])
        fig_line.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="#e0e0e0",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        )
        st.plotly_chart(fig_line, use_container_width=True)
    
    st.write("### TRANSACTION LOGS")
    st.dataframe(df.iloc[::-1], use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Bottom Section
st.markdown("<br>", unsafe_allow_html=True)
b1, b2 = st.columns(2)
with b1:
    st.markdown("<div class='glass-card'><h4>💡 System Tip</h4>AI has detected a background Windows Update and throttled it to save 40% bandwidth for your Meeting.</div>", unsafe_allow_html=True)
with b2:
    st.markdown("<div class='glass-card'><h4>🛡️ Efficiency</h4>The current QoS profile is reducing jitter by 12ms using Predictive Queuing.</div>", unsafe_allow_html=True)

# Smooth auto-refresh
time.sleep(2)
st.rerun()
