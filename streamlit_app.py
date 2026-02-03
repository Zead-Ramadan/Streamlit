import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np

# ============ SETUP GOD MODE THEME ============
st.set_page_config(
    page_title="مخزن مقاولات - GOD MODE",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS ناري
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
        color: #00ffcc;
        font-family: 'Share Tech Mono', monospace;
    }
    
    .main-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        text-align: center;
        background: linear-gradient(90deg, #00ffcc, #00ccff, #ff00cc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(0, 255, 204, 0.5);
        margin-bottom: 0;
        animation: glow 2s infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(0, 255, 204, 0.5); }
        to { text-shadow: 0 0 30px rgba(0, 204, 255, 0.8), 0 0 40px rgba(255, 0, 204, 0.6); }
    }
    
    .metric-card {
        background: rgba(20, 25, 45, 0.9);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #00ffcc;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.3);
        margin: 10px;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.6);
        border-color: #ff00cc;
    }
    
    .warning-box {
        background: rgba(255, 50, 50, 0.2);
        border: 2px solid #ff3366;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        animation: pulse-red 2s infinite;
    }
    
    @keyframes pulse-red {
        0% { border-color: #ff3366; }
        50% { border-color: #ff0066; box-shadow: 0 0 20px rgba(255, 51, 102, 0.5); }
        100% { border-color: #ff3366; }
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc, #00ccff);
        color: black;
        font-weight: bold;
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        font-family: 'Orbitron', sans-serif;
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #ff00cc, #ff3366);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ============ LOAD DATA ============
@st.cache_data
def load_data():
    # هنا هحول الـ Excel لـ DataFrame
    data = pd.read_excel("تكاليف مقاولات.xlsx")
    data['date'] = pd.to_datetime(data['date'])
    data['cost'] = data['quantity'] * data['price']  # لو مكنش في column cost
    return data

data = load_data()
