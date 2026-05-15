import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
import time
import threading
from scapy.all import sniff, IP, TCP, UDP, ICMP

# --- PAGE CONFIG ---
st.set_page_config(page_title="NetSentry AI", page_icon="🛡️", layout="wide")

# --- CUSTOM CSS (FOR 3D & GLASSMORPISM LOOK) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
    }
    .stApp {
        background: transparent;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }
    .neon-text {
        font-family: 'Orbitron', sans-serif;
        color: #00d4ff;
        text-shadow: 0 0 10px #00d4ff, 0 0 20px #00d4ff;
    }
    .stButton>button {
        background: linear-gradient(45deg, #00d4ff, #0055ff);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 10px 30px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.6);
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD ASSETS ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

lottie_net = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_qy9mz6sh.json") # Network 3D
lottie_scan = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_gdbe6m7b.json") # Scanning

# --- SESSION STATE ---
if 'packets' not in st.session_state:
    st.session_state.packets = []
if 'scanning' not in st.session_state:
    st.session_state.scanning = False

# --- SNIFFER LOGIC ---
def packet_callback(packet):
    if packet.haslayer(IP):
        data = {
            "Time": time.strftime("%H:%M:%S"),
            "Source": packet[IP].src,
            "Dest": packet[IP].dst,
            "Proto": packet[IP].proto,
            "Len": len(packet)
        }
        st.session_state.packets.append(data)
        if len(st.session_state.packets) > 50: st.session_state.packets.pop(0)

def start_sniffing():
    sniff(prn=packet_callback, store=0, stop_filter=lambda x: not st.session_state.scanning)

# --- APP LAYOUT ---

# Horizontal Menu
menu = st.sidebar.radio("Navigation", ["🏠 Home", "📊 Real-Time Analyzer", "🛡️ Security Hub"])

if menu == "🏠 Home":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<h1 class='neon-text'>NetSentry AI</h1>", unsafe_allow_html=True)
        st.markdown("### Next-Gen Network Traffic Analysis & Security")
        st.write("Professional grade packet inspection tool developed for university research and network monitoring.")
        
        st.markdown("""
        <div class='glass-card'>
            <h4>Core Capabilities:</h4>
            <ul>
                <li>Live Packet Sniffing (TCP/UDP/ICMP)</li>
                <li>Visual Traffic Analytics</li>
                <li>Intrusion Detection Patterns</li>
                <li>Automated Protocol Breakdown</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Launch Dashboard"):
            st.info("Navigate to Analyzer from Sidebar!")
            
    with col2:
        st_lottie(lottie_net, height=350, key="net")

elif menu == "📊 Real-Time Analyzer":
    st.markdown("<h2 class='neon-text'>Network Live Stream</h2>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("▶️ Start Capture"):
            st.session_state.scanning = True
            threading.Thread(target=start_sniffing, daemon=True).start()
    with c2:
        if st.button("⏹️ Stop Capture"):
            st.session_state.scanning = False
    with c3:
        if st.button("🗑️ Clear Logs"):
            st.session_state.packets = []

    if st.session_state.packets:
        df = pd.DataFrame(st.session_state.packets)
        
        # 3D-style Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Packets Processed", len(df))
        m2.metric("Active Sources", df['Source'].nunique())
        m3.metric("Peak Bandwidth", f"{df['Len'].max()} B")

        # Visualization Row
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            fig_pie = px.sunburst(df, path=['Proto', 'Source'], values='Len', 
                                 title="Protocol Hierarchy",
                                 color_continuous_scale='RdBu')
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_right:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            fig_line = px.line(df, y='Len', title="Traffic Pulse (Real-time)",
                              line_shape="spline", render_mode="svg")
            fig_line.update_traces(line_color='#00d4ff')
            fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_line, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("### Live Packet Data Table")
        st.dataframe(df.style.set_properties(**{'background-color': '#1e293b', 'color': '#00d4ff'}))
    else:
        st_lottie(lottie_scan, height=200)
        st.info("Awaiting live traffic... Click Start Capture.")

elif menu == "🛡️ Security Hub":
    st.markdown("<h2 class='neon-text'>Security Insights</h2>", unsafe_allow_html=True)
    
    if st.session_state.packets:
        df = pd.DataFrame(st.session_state.packets)
        
        # Simple Logic to detect "Suspicious" activity
        suspicious = df[df['Len'] > 1000] # Random rule for demo
        
        st.warning(f"Found {len(suspicious)} high-payload packets (Potential Risk)")
        
        fig_bar = px.bar(df, x='Source', y='Len', color='Proto', title="Data Consumption per IP")
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.error("No data available to analyze. Please run the sniffer first.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("<small>Dev by: Your Name<br>Computer Networks Project 2024</small>", unsafe_allow_html=True)
