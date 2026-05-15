import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
import time
import random

# --- CONFIG ---
st.set_page_config(page_title="CogniNet AI", layout="wide", page_icon="🕸️")

# --- UI STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    .stApp { background: #00040a; color: #00d4ff; font-family: 'Orbitron', sans-serif; }
    .glass-panel {
        background: rgba(0, 212, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 20px; padding: 25px;
    }
    .neon-glow {
        color: #00d4ff; text-shadow: 0 0 10px #00d4ff;
        text-align: center; font-weight: bold;
    }
    header {visibility: hidden;} footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZATION (Robust Check) ---
if 'nodes' not in st.session_state:
    # Explicitly creating the DataFrame with all necessary columns
    data = {
        'id': list(range(8)),
        'x': [1, 2, 4, 5, 2, 4, 1, 5],
        'y': [2, 4, 4, 2, 0, 0, 0, 4],
        'status': ['Active'] * 8,
        'load': [random.randint(20, 80) for _ in range(8)]
    }
    st.session_state.nodes = pd.DataFrame(data)

if 'history' not in st.session_state:
    st.session_state.history = [50.0]

# --- LOAD LOTTIE ---
def load_lottie(url):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except:
        return None

lottie_neural = load_lottie("https://lottie.host/8553641b-10f7-434a-9524-71e98822588c/OayXwS3S0R.json")

# --- AI SELF-HEALING LOGIC ---
def evolve_network():
    # Making sure we are working with a fresh copy of session state
    nodes = st.session_state.nodes.copy()
    
    # 1. Random Failure Simulation
    if random.random() < 0.15:
        fail_id = random.randint(0, 7)
        nodes.at[fail_id, 'status'] = 'Offline'
        nodes.at[fail_id, 'load'] = 0
    
    # 2. AI Healing: Find active nodes and redistribute load
    # Check if 'status' column exists before accessing
    if 'status' in nodes.columns:
        active_mask = nodes['status'] == 'Active'
        offline_mask = nodes['status'] == 'Offline'
        
        if offline_mask.any():
            # AI healing logic
            nodes.loc[active_mask, 'load'] += 3
            # Self-heal back to active occasionally
            if random.random() < 0.3:
                nodes.loc[offline_mask, 'status'] = 'Active'
                nodes.loc[offline_mask, 'load'] = 20
        
        # Calculate Average Load for history
        current_avg_load = nodes[nodes['status'] == 'Active']['load'].mean()
        st.session_state.history.append(float(current_avg_load))
    
    if len(st.session_state.history) > 20:
        st.session_state.history.pop(0)
    
    # Update back to session state
    st.session_state.nodes = nodes

# --- APP LAYOUT ---
st.markdown("<h1 class='neon-glow'>COGNINET // NEURAL MESH</h1>", unsafe_allow_html=True)

col_ctrl, col_viz = st.columns([1, 2.5])

with col_ctrl:
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.write("### AI CORE")
    if lottie_neural:
        st_lottie(lottie_neural, height=150, key="main_anim")
    
    # Run the logic
    evolve_network()
    
    nodes_df = st.session_state.nodes
    active_count = len(nodes_df[nodes_df['status'] == 'Active'])
    
    st.metric("NODES ONLINE", f"{active_count}/8")
    st.metric("AI OPTIMIZATION", "STABLE" if active_count > 6 else "HEALING")
    
    if st.button("RESET NETWORK"):
        data = {
            'id': list(range(8)),
            'x': [1, 2, 4, 5, 2, 4, 1, 5],
            'y': [2, 4, 4, 2, 0, 0, 0, 4],
            'status': ['Active'] * 8,
            'load': [random.randint(20, 80) for _ in range(8)]
        }
        st.session_state.nodes = pd.DataFrame(data)
        st.session_state.history = [50.0]
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col_viz:
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    
    # Create the Visual Mesh
    nodes = st.session_state.nodes
    edge_x, edge_y = [], []
    
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            if nodes.at[i, 'status'] == 'Active' and nodes.at[j, 'status'] == 'Active':
                edge_x.extend([nodes.at[i, 'x'], nodes.at[j, 'x'], None])
                edge_y.extend([nodes.at[i, 'y'], nodes.at[j, 'y'], None])

    fig = go.Figure()
    # Connections
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, line=dict(width=1, color='#00d4ff'), mode='lines', hoverinfo='none'))
    # Nodes
    fig.add_trace(go.Scatter(
        x=nodes['x'], y=nodes['y'], mode='markers+text',
        text=nodes['id'], textposition="top center",
        marker=dict(size=25, color=np.where(nodes['status'] == 'Active', '#00d4ff', '#ff0055'),
                    symbol='hexagon', line=dict(width=2, color='white'))
    ))

    fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      margin=dict(l=0, r=0, b=0, t=0), xaxis=dict(visible=False), yaxis=dict(visible=False))
    st.plotly_chart(fig, use_container_width=True)
    
    # History Graph
    st.write("### AI EFFICIENCY HISTORY")
    st.line_chart(st.session_state.history)
    st.markdown("</div>", unsafe_allow_html=True)

# Explanation
st.markdown("<br>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
c1.info("🛠️ **Self-Healing:** AI detects node failures (Red) and redistributes data load to healthy nodes.")
c2.success("📈 **Evolution:** The neural mesh constantly reconfigures connections for optimal throughput.")

# Auto-refresh
time.sleep(2)
st.rerun()
