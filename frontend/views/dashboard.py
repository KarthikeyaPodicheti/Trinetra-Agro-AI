"""Dashboard page — KPI overview."""

import streamlit as st
from frontend.api_client import api_get
import pandas as pd
import random


def show():
    st.markdown("### 📊 Farm Intelligence Dashboard")
    st.markdown("Welcome to your centralized farm management command center.")

    st.markdown("#### 🚀 Quick Actions")
    q1, q2, q3, q4 = st.columns(4)
    if q1.button("🌱 Crop Advice", use_container_width=True):
        st.session_state.page = "ai_advisor"; st.rerun()
    if q2.button("🔬 Scan Disease", use_container_width=True):
        st.session_state.page = "disease_scanner"; st.rerun()
    if q3.button("📈 Market Prices", use_container_width=True):
        st.session_state.page = "market_intelligence"; st.rerun()
    if q4.button("💬 AI Chatbot", use_container_width=True):
        st.session_state.page = "chatbot"; st.rerun()

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("System Status", "Online", "All systems nominal")
    c2.metric("Active Crops", "4", "Monitored")
    c3.metric("AI Analyses", "127", "Total run")
    c4.metric("Market Alerts", "3", "Active", delta_color="inverse")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🌾 Simulated Market Trends (Last 7 Days)**")
        dates = pd.date_range(end=pd.Timestamp.today(), periods=7)
        data = pd.DataFrame({
            'Wheat (₹/Q)': [2100, 2120, 2150, 2140, 2180, 2200, 2210],
            'Rice (₹/Q)': [2800, 2790, 2820, 2850, 2880, 2860, 2900]
        }, index=dates)
        st.line_chart(data)

    with col2:
        st.markdown("**💧 Resource Usage (Estimated)**")
        data2 = pd.DataFrame({
            'Water Index': [60, 65, 70, 68, 55, 60, 62],
            'Soil Health': [80, 80, 79, 81, 82, 82, 83]
        }, index=dates)
        st.area_chart(data2)

    st.markdown("---")
    tips = [
        "Check soil moisture before irrigating — overwatering reduces yield.",
        "Rotate crops each season to maintain soil health and reduce pests.",
        "Use drip irrigation to save 30-50% water compared to flood method.",
        "Monitor market prices weekly for best selling window.",
        "Apply mulch to reduce water evaporation by 25-30%.",
    ]
    st.info(f"💡 **Today's Farming Tip:** {random.choice(tips)}")
