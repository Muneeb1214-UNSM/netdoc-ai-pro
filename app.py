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
st.set_page_config(page_title="Fed-Sentinel AI", layout="wide", page_icon="🔐")

# --- CUSTOM CSS (PRIVACY THEME: PURPLE & NEON) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Share+Tech+Mono&display=swap');
    
    .stApp {
        background: radial-gradient(circle at top right, #1a1a2e 0%, #020205 100%);
        color: #e0e0ff;
        font-family: 'Share Tech Mono', monospace;
    }

    .glass-box {
        background: rgba(138, 43, 226, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(138, 43, 226, 0.3);
        box-shadow: 0 0 20px rgba(138, 43, 226, 0.2);
    }

    .neon-title {
        font-family: 'Syncopate', sans-serif;
        color: #bc13fe;
        text-shadow: 0 0 10px #bc13fe, 0 0 20px #bc13fe;
        text-align: center;
    }

    .privacy-badge {
        background: #00ff88;
        color: black;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 12px;
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- LOAD ASSETS ---
def load_lottie(url):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except:
        return None

lottie_security = load_lottie("https://lottie.host/68297b69-8088-466d-959c-8a192f1505c2/Wv0k06H4tV.json")

# --- INITIALIZING SESSION DATA ---
if 'round' not in st.session_state:
    st.session_state.round = 1
    st.session_state.accuracy = [0.1]
    st.session_state.nodes = pd.DataFrame({
        'Node_ID': ['Node_A', 'Node_B', 'Node_C', 'Node_D'],
        'Data_Samples': [120, 450, 230, 800],
        'Privacy_Status': ['Encrypted', 'Encrypted', 'Encrypted', 'Encrypted']
    })

# --- FEDERATED LOGIC (SIMULATION) ---
def simulate_training_round():
    time.sleep(1.5)
    st.session_state.round += 1
    new_acc = st.session_state.accuracy[-1] + random.uniform(0.05, 0.15)
    if new_acc > 0.98: new_acc = 0.99
    st.session_state.accuracy.append(new_acc)

# --- APP UI ---
st.markdown("<h1 class='neon-title'>FED-SENTINEL AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Privacy-First Federated Learning Network Simulator</p>", unsafe_allow_html=True)

col_info, col_viz = st.columns([1, 2])

with col_info:
    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.write("### 🤖 AGGREGATOR STATUS")
    if lottie_security:
        st_lottie(lottie_security, height=180)
    
    st.write(f"**Current Round:** {st.session_state.round}")
    st.write(f"**Global Accuracy:** {st.session_state.accuracy[-1]*100:.1f}%")
    
    st.markdown("<span class='privacy-badge'>RAW DATA LEAK: 0%</span>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if st.button("🚀 EXECUTE NEXT TRAINING ROUND"):
        simulate_training_round()
        st.rerun()
    
    if st.button("🔄 RESET NETWORK"):
        st.session_state.round = 1
        st.session_state.accuracy = [0.1]
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col_viz:
    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.write("### 🌐 NETWORK NODE TOPOLOGY")
    
    # Visualizing Nodes on a Radar/Map
    nodes_df = st.session_state.nodes
    fig_nodes = px.scatter(nodes_df, x='Node_ID', y='Data_Samples', size='Data_Samples', 
                          color='Node_ID', title="Active Edge Devices (Data Localized)",
                          template="plotly_dark")
    fig_nodes.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_nodes, use_container_width=True)
    
    # Training Progress Graph
    st.write("### 📈 GLOBAL MODEL CONVERGENCE")
    fig_acc = px.line(y=st.session_state.accuracy, x=range(len(st.session_state.accuracy)),
                     labels={'x': 'Rounds', 'y': 'Accuracy'}, title="Federated Learning Accuracy Curve")
    fig_acc.update_traces(line_color='#bc13fe', mode='lines+markers')
    fig_acc.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_acc, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- THE "UNIQUE" EXPLANATION SECTION ---
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("<div class='glass-box'><h4>🔐 Privacy Layer</h4>Data stays on Node_A, Node_B, etc. Only gradients (mathematical updates) are sent via SSL/TLS.</div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='glass-box'><h4>⚙️ Decentralized Training</h4>Each device uses its local CPU/GPU to train, reducing server-side load and latency.</div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='glass-box'><h4>🤝 Secure Aggregation</h4>The Central Server (Aggregator) averages the updates to improve the Global Model.</div>", unsafe_allow_html=True)

# Footer
st.sidebar.title("FED-CORE v1.0")
st.sidebar.write("Advanced Privacy Agent")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=100)
