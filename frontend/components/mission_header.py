"""MissionHeader Component - Top header with mission stats."""

from datetime import datetime
from typing import Any
import streamlit as st


def format_elapsed_time(start_time: datetime) -> str:
    """Format elapsed time from start."""
    elapsed = datetime.now() - start_time
    hours, remainder = divmod(int(elapsed.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"


def render_mission_header(
    mission_name: str,
    environment: str,
    agent_count: int,
    running_count: int,
    execution_time: datetime,
    auto_refresh: bool = True
) -> None:
    """Render the mission control header."""
    
    elapsed = format_elapsed_time(execution_time)
    
    # Environment color
    env_colors = {
        "production": "#ef4444",
        "staging": "#f59e0b",
        "development": "#10b981",
    }
    env_color = env_colors.get(environment.lower(), "#6366f1")
    
    st.markdown(f"""<style> .mission-header {{ background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95)); border: 1px solid rgba(148, 163, 184, 0.1); border-radius: 16px; padding: 20px 24px; margin-bottom: 24px; }} .mission-title {{ display: flex; align-items: center; gap: 16px; margin-bottom: 20px; }} .mission-title h1 {{ font-size: 24px; font-weight: 700; color: #f8fafc; margin: 0; }} .mission-badge {{ padding: 6px 14px; background: {env_color}20; border: 1px solid {env_color}40; border-radius: 20px; font-size: 12px; font-weight: 600; color: {env_color}; text-transform: uppercase; }} .mission-stats {{ display: flex; gap: 16px; flex-wrap: wrap; }} .stat-card {{ flex: 1; min-width: 120px; padding: 14px 18px; background: rgba(51, 65, 85, 0.5); border: 1px solid rgba(148, 163, 184, 0.1); border-radius: 12px; text-align: center; }} .stat-value {{ font-size: 28px; font-weight: 700; font-family: 'JetBrains Mono', monospace; color: #f8fafc; margin-bottom: 4px; }} .stat-label {{ font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; }} .stat-card.primary {{ background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(99, 102, 241, 0.1)); border-color: rgba(99, 102, 241, 0.3); }} .stat-card.primary .stat-value {{ color: #818cf8; }} .stat-card.success {{ background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.1)); border-color: rgba(16, 185, 129, 0.3); }} .stat-card.success .stat-value {{ color: #10b981; }} .stat-card.warning {{ background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(245, 158, 11, 0.1)); border-color: rgba(245, 158, 11, 0.3); }} .stat-card.warning .stat-value {{ color: #f59e0b; }} </style>""", unsafe_allow_html=True)
    
    st.markdown(f"""<div class="mission-header"> <div class="mission-title"> <h1>🎛️ {mission_name}</h1> <span class="mission-badge">{environment}</span> </div> <div class="mission-stats"> <div class="stat-card primary"> <div class="stat-value">{agent_count}</div> <div class="stat-label">Total Agents</div> </div> <div class="stat-card success"> <div class="stat-value">{running_count}</div> <div class="stat-label">Running</div> </div> <div class="stat-card"> <div class="stat-value">{elapsed}</div> <div class="stat-label">Execution Time</div> </div> <div class="stat-card"> <div class="stat-value">5s</div> <div class="stat-label">Refresh</div> </div> </div> </div>""", unsafe_allow_html=True)


def render_refresh_controls(auto_refresh: bool, refresh_interval: int) -> None:
    """Render refresh control buttons."""
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button(
            "▶️ Start" if not auto_refresh else "⏸️ Pause",
            width='stretch',
            type="secondary"
        ):
            st.session_state.auto_refresh = not auto_refresh
            st.rerun()
    
    with col2:
        if st.button("🔄 Refresh", width='stretch', type="secondary"):
            st.rerun()
    
    with col3:
        selected_interval = st.selectbox(
            "Interval",
            [3, 5, 10, 30],
            index=[3, 5, 10, 30].index(refresh_interval) if refresh_interval in [3, 5, 10, 30] else 1,
            label_visibility="collapsed",
        )
        st.session_state.refresh_interval = selected_interval
    
    with col4:
        if st.button("📊 Export", width='stretch', type="secondary"):
            st.info("Export functionality coming soon!")
