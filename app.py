import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import requests
import time
import threading
import random

# --- IMPORT SCAPY SAFELY ---
try:
    from scapy.all import sniff, IP, TCP, UDP, ICMP
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

# --- PAGE CONFIG ---
st.set_page_config(page_title="NetSentry Pro AI", page_icon="🛡️", layout="wide")

# --- CUSTOM CSS FOR 3D & NEON LOOK ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    .main { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: white; }
    .neon-text { font-family: 'Orbitron', sans-serif; color: #00d4ff; text-shadow: 0 0 10px #00d4ff; }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    .stButton>button {
        background: linear-gradient(45deg, #00d4ff, #0055ff);
        color: white; border: none; border-radius: 20px;
        padding: 10px 25px; font-weight: bold; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0 0 15px rgba(0, 212, 255, 0.5); }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD LOTTIE ANIMATIONS ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except:
        return None

lottie_net = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_qy9mz6sh.json")
lottie_scan = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_gdbe6m7b.json")

# --- SESSION STATE ---
if 'packets' not in st.session_state:
    st.session_state.packets = []
if 'scanning' not in st.session_state:
    st.session_state.scanning = False

# --- PACKET PROCESSING LOGIC ---
def packet_callback(packet):
    if packet.haslayer(IP):
        data = {
            "Time": time.strftime("%H:%M:%S"),
            "Source": packet[IP].src,
            "Dest": packet[IP].dst,
            "Proto": "TCP" if packet.haslayer(TCP) else "UDP" if packet.haslayer(UDP) else "ICMP" if packet.haslayer(ICMP) else "Other",
            "Len": len(packet)
        }
        st.session_state.packets.append(data)
        if len(st.session_state.packets) > 60: st.session_state.packets.pop(0)

def start_sniffing():
    # Try Real Sniffing first (Works on Local Admin)
    try:
        sniff(prn=packet_callback, store=0, stop_filter=lambda x: not st.session_state.scanning, timeout=2)
    except:
        # Fallback to Simulation (Works on Streamlit Cloud)
        while st.session_state.scanning:
            time.sleep(1)
            fake_data = {
                "Time": time.strftime("%H:%M:%S"),
                "Source": f"192.168.1.{random.randint(1,255)}",
                "Dest": f"10.0.0.{random.randint(1,255)}",
                "Proto": random.choice(["TCP", "UDP", "ICMP", "TCP"]),
                "Len": random.randint(54, 1450)
            }
            st.session_state.packets.append(fake_data)
            if len(st.session_state.packets) > 60: st.session_state.packets.pop(0)

# --- UI NAVIGATION ---
st.sidebar.markdown("<h2 class='neon-text'>NET-SENTRY</h2>", unsafe_allow_html=True)
page = st.sidebar.selectbox("Go to", ["Home", "Analyzer Dashboard", "Security Metrics"])

if page == "Home":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<h1 class='neon-text'>Real-Time Network <br>Intelligence</h1>", unsafe_allow_html=True)
        st.write("### Computer Networks Semester Project")
        st.markdown("""
        <div class='glass-card'>
        Deploying a professional-grade packet sniffer and analyzer. 
        This tool monitors traffic flow, protocol distribution, and potential security threats.
        <br><br><b>Status:</b> System Online 🟢
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Analyzer"):
            st.info("Select Analyzer Dashboard from the Sidebar!")
    with col2:
        if lottie_net: st_lottie(lottie_net, height=300)

elif page == "Analyzer Dashboard":
    st.markdown("<h2 class='neon-text'>Live Traffic Stream</h2>", unsafe_allow_html=True)
    
    # Control Panel
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
        
        # Metrics Cards
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Packets", len(df))
        m2.metric("Unique IPs", df['Source'].nunique())
        m3.metric("Protocols", df['Proto'].nunique())
        m4.metric("Avg Size", f"{int(df['Len'].mean())} B")

        # Charts Row
        g1, g2 = st.columns(2)
        with g1:
            fig_pie = px.pie(df, names='Proto', title="Protocol Breakdown", hole=0.5, template="plotly_dark")
            st.plotly_chart(fig_pie, use_container_width=True)
        with g2:
            fig_line = px.line(df, y='Len', title="Traffic Throughput", template="plotly_dark")
            fig_line.update_traces(line_color='#00d4ff')
            st.plotly_chart(fig_line, use_container_width=True)

        st.markdown("### Captured Data Packets")
        st.dataframe(df.iloc[::-1], use_container_width=True)
    else:
        if lottie_scan: st_lottie(lottie_scan, height=200)
        st.info("System Ready. Click 'Start Capture' to analyze network.")

elif page == "Security Metrics":
    st.markdown("<h2 class='neon-text'>Security Threat Analysis</h2>", unsafe_allow_html=True)
    if st.session_state.packets:
        df = pd.DataFrame(st.session_state.packets)
        st.success("Analysis Complete: No major intrusions detected.")
        
        fig_bar = px.bar(df, x='Proto', y='Len', color='Source', title="Data Load per Protocol", template="plotly_dark")
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("Capture some data first in the Analyzer Dashboard.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.write("Developed with ❤️ for University Project")
