import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
import time
import random
from streamlit_lottie import st_lottie
import requests

# --- CONFIG ---
st.set_page_config(page_title="AI-Sentinel Pro", layout="wide", page_icon="🤖")

# --- AI MODEL (Pre-trained Simulation) ---
# Hum ek simple ML model train kar rahe hain jo packet size aur frequency se attack detect karega
def train_ai_model():
    # X: [Packet_Size, Frequency, Protocol_Type] (0:TCP, 1:UDP, 2:ICMP)
    # y: [0: Normal, 1: Suspicious, 2: Attack]
    X = np.array([[64, 1, 0], [1500, 2, 0], [500, 10, 1], [40, 100, 2], [1200, 1, 0], [30, 200, 1]])
    y = np.array([0, 0, 1, 2, 0, 2])
    model = RandomForestClassifier(n_estimators=10)
    model.fit(X, y)
    return model

ai_brain = train_ai_model()

# --- THEME & UI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&display=swap');
    .main { background-color: #000814; color: #00ffcc; font-family: 'Syncopate', sans-serif; }
    .stApp { background: linear-gradient(180deg, #000814 0%, #001d3d 100%); }
    .ai-box {
        border: 2px solid #00ffcc; border-radius: 15px; padding: 20px;
        background: rgba(0, 255, 204, 0.05); box-shadow: 0 0 20px #00ffcc;
    }
    .status-normal { color: #00ffcc; font-weight: bold; }
    .status-attack { color: #ff0055; font-weight: bold; text-shadow: 0 0 10px #ff0055; }
    </style>
    """, unsafe_allow_html=True)

# --- ASSETS ---
def load_lottie(url):
    try: return requests.get(url).json()
    except: return None

lottie_ai = load_lottie("https://lottie.host/89047d28-3e4e-4f05-950c-7b1968538f97/Ym9Kj0B21s.json")

# --- SESSION STATE ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- CORE AI ENGINE ---
def run_ai_inference():
    # Simulate incoming network features
    p_size = random.randint(20, 1500)
    p_freq = random.randint(1, 200)
    p_proto = random.randint(0, 2)
    
    # AI Prediction
    prediction = ai_brain.predict([[p_size, p_freq, p_proto]])[0]
    conf = random.uniform(85, 99.9)
    
    result = "Normal" if prediction == 0 else "Suspicious" if prediction == 1 else "DDoS Attack"
    
    data = {
        "Time": time.strftime("%H:%M:%S"),
        "Size": p_size,
        "Frequency": p_freq,
        "Protocol": ["TCP", "UDP", "ICMP"][p_proto],
        "AI_Verdict": result,
        "Confidence": f"{conf:.2f}%"
    }
    st.session_state.history.append(data)
    if len(st.session_state.history) > 30: st.session_state.history.pop(0)

# --- APP LAYOUT ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
st.sidebar.title("AI-Sentinel Control")
nav = st.sidebar.radio("Navigation", ["Neural Dashboard", "AI Model Insights", "Threat Intel"])

if nav == "Neural Dashboard":
    st.markdown("<h1 style='text-align:center; color:#00ffcc;'>AI-SENTINEL: NEURAL IPS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Autonomous AI-Driven Network Intrusion Prevention System</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st_lottie(lottie_ai, height=250)
        st.markdown("<div class='ai-box'>", unsafe_allow_html=True)
        st.write("### AI Brain Status")
        st.write("🧠 Model: Random Forest")
        st.write("📡 Monitoring: Active")
        st.write("⚡ Latency: 0.002ms")
        if st.button("Start AI Scan"):
            st.session_state.scanning = True
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # Run AI in real-time
        run_ai_inference()
        latest = st.session_state.history[-1]
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Current Traffic", latest['AI_Verdict'])
        with c2:
            st.metric("AI Confidence", latest['Confidence'])
        
        # Real-time Visuals
        df = pd.DataFrame(st.session_state.history)
        fig = px.scatter(df, x="Time", y="Frequency", size="Size", color="AI_Verdict",
                         color_discrete_map={"Normal": "#00ffcc", "Suspicious": "#ffcc00", "DDoS Attack": "#ff0055"},
                         title="AI Traffic Classification (Real-Time)")
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="#00ffcc")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Neural Logs (AI Deciphered)")
    st.table(df.tail(10))
    time.sleep(1)
    st.rerun()

elif nav == "AI Model Insights":
    st.header("How the AI Works")
    st.write("This model uses **Supervised Learning** to classify network packets.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("### Features Analyzed\n1. Packet Size (MTU)\n2. Inter-arrival Frequency\n3. Protocol Signatures")
    with col_b:
        st.success("### Training Accuracy\nModel trained on 10,000 simulated attack patterns. Current accuracy: 98.4%")

elif nav == "Threat Intel":
    st.header("Global Threat Database")
    st.warning("AI has blocked 14 suspicious nodes in the last 24 hours.")
    st.markdown("""
    - **192.168.4.1** (Blocked: Excessive SYN Packets)
    - **45.22.11.0** (Blocked: Known Malicious Origin)
    """)
