import streamlit as st
import pandas as pd
import plotly.express as px
from scapy.all import sniff, IP, TCP, UDP, ICMP
import threading
import time
import socket

# --- Page Config ---
st.set_page_config(page_title="Net-Sentry Pro", page_icon="🌐", layout="wide")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- Global Data Storage ---
if 'packet_list' not in st.session_state:
    st.session_state.packet_list = []
if 'is_sniffing' not in st.session_state:
    st.session_state.is_sniffing = False

# --- Backend: Packet Sniffer Logic ---
def process_packet(packet):
    if packet.haslayer(IP):
        packet_info = {
            "Timestamp": time.strftime("%H:%M:%S"),
            "Source": packet[IP].src,
            "Destination": packet[IP].dst,
            "Protocol": "TCP" if packet.haslayer(TCP) else "UDP" if packet.haslayer(UDP) else "ICMP" if packet.haslayer(ICMP) else "Other",
            "Size (Bytes)": len(packet),
        }
        st.session_state.packet_list.append(packet_info)
        # Limit list size to last 100 packets to keep it fast
        if len(st.session_state.packet_list) > 100:
            st.session_state.packet_list.pop(0)

def start_sniffing():
    sniff(prn=process_packet, store=False, stop_filter=lambda x: not st.session_state.is_sniffing)

# --- UI: Sidebar ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
st.sidebar.title("Net-Sentry Control")
st.sidebar.info("This tool monitors real-time network traffic and analyzes protocols.")

start_btn = st.sidebar.button("▶️ Start Monitoring")
stop_btn = st.sidebar.button("⏹️ Stop Monitoring")

if start_btn:
    st.session_state.is_sniffing = True
    # Run sniffing in a separate thread so it doesn't block the UI
    thread = threading.Thread(target=start_sniffing, daemon=True)
    thread.start()
    st.sidebar.success("Sniffer Started!")

if stop_btn:
    st.session_state.is_sniffing = False
    st.sidebar.warning("Sniffer Stopped.")

# --- UI: Main Dashboard ---
st.title("🌐 Real-Time Network Traffic Analyzer")
st.markdown("---")

# Metrics Top Row
if st.session_state.packet_list:
    df = pd.DataFrame(st.session_state.packet_list)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Packets", len(df))
    col2.metric("Unique IPs", df['Source'].nunique())
    col3.metric("TCP Packets", len(df[df['Protocol'] == 'TCP']))
    col4.metric("Avg Packet Size", f"{round(df['Size (Bytes)'].mean(), 2)} B")

    st.markdown("### 📊 Network Analytics")
    
    # Graphs Row
    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        # Protocol Distribution Pie Chart
        fig_pie = px.pie(df, names='Protocol', title="Protocol Distribution", hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)

    with g_col2:
        # Traffic Volume Line Chart
        fig_line = px.line(df, y='Size (Bytes)', title="Packet Size Over Time",
                           line_shape='spline', render_mode='svg')
        st.plotly_chart(fig_line, use_container_width=True)

    # Packet Data Table
    st.markdown("### 📝 Live Packet Log")
    st.dataframe(df.iloc[::-1], use_container_width=True) # Show latest packets first

    # Download Button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Export Capture Data (CSV)", data=csv, file_name='network_log.csv', mime='text/csv')

else:
    st.warning("No traffic detected. Click 'Start Monitoring' in the sidebar to begin.")
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJpbmZ6bmZ6bmZ6bmZ6bmZ6bmZ6bmZ6bmZ6bmZ6bmZ6bmZ6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKMGpxxHGG0pEHe/giphy.gif", width=400)

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Built for University Semester Project | Computer Networks Lab</p>", unsafe_allow_html=True)
