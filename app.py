"""
AI-QOS - Agent Control Tower

Enterprise AI Agent Monitoring Dashboard

A comprehensive command center for observing and managing AI agents
working together in real-time.

Quick Start:
    streamlit run app.py

Navigate to:
    http://localhost:8501
"""

import streamlit as st

# Set page config
st.set_page_config(
    page_title="AI-QOS - Agent Control Tower",
    page_icon="🎛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Redirect to Agent Control Tower
st.markdown("""
# 🎛️ AI-QOS Agent Control Tower

Redirecting to the Agent Control Tower...

If not redirected automatically, click the link below:

👉 **[Agent Control Tower](/Agent_Control_Tower)** 👈
""", unsafe_allow_html=True)

# Auto-redirect after delay
st.markdown("""
<script>
    setTimeout(function() {
        window.location.href = '/Agent_Control_Tower';
    }, 2000);
</script>
""", unsafe_allow_html=True)
