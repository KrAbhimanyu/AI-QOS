"""Monitoring page for AI-QOS."""
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
from components.core_components import (
    page_header,
    metric_card,
    status_badge,
)


def render_monitoring() -> None:
    """Render the monitoring page."""
    page_header(
        title="System Monitoring",
        subtitle="Real-time system health and performance metrics",
        icon="📡",
        actions=["🔄 Refresh", "📊 Export"],
    )
    
    # System Health Overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("System Health", "Healthy", icon="💚")
    with col2:
        metric_card("Uptime", "99.9%", icon="⏱️")
    with col3:
        metric_card("Active Connections", 142, icon="🔗")
    with col4:
        metric_card("Memory Usage", "68%", icon="💾")
    
    st.markdown("---")
    
    # Two column layout
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        # System Metrics Chart
        st.markdown("### Resource Utilization")
        
        # Generate sample time series data
        times = [(datetime.now() - timedelta(minutes=i)) for i in range(30, 0, -1)]
        
        fig = go.Figure()
        
        # CPU line
        cpu_values = [40 + (i % 10) * 2 for i in range(30)]
        fig.add_trace(go.Scatter(
            x=[t.strftime("%H:%M") for t in times],
            y=cpu_values,
            mode="lines",
            name="CPU %",
            line=dict(color="#6366F1", width=2),
        ))
        
        # Memory line
        memory_values = [65 + (i % 8) * 1.5 for i in range(30)]
        fig.add_trace(go.Scatter(
            x=[t.strftime("%H:%M") for t in times],
            y=memory_values,
            mode="lines",
            name="Memory %",
            line=dict(color="#22D3EE", width=2),
        ))
        
        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=300,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis=dict(showgrid=False, color="#94A3B8", showticklabels=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(51, 65, 85, 0.5)", color="#94A3B8"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Throughput Chart
        st.markdown("### Request Throughput")
        
        fig2 = go.Figure()
        
        # Requests per minute
        requests = [120 + (i % 20) * 5 for i in range(30)]
        colors = ["#10B981" if r > 150 else "#F59E0B" if r > 130 else "#EF4444" for r in requests]
        
        fig2.add_trace(go.Bar(
            x=[t.strftime("%H:%M") for t in times],
            y=requests,
            marker_color=colors,
            name="Requests/min",
        ))
        
        fig2.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=250,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis=dict(showgrid=False, color="#94A3B8", showticklabels=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(51, 65, 85, 0.5)", color="#94A3B8"),
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with right_col:
        # Agent Status
        st.markdown("### Agent Status")
        
        agents = [
            ("CodeMaster", "Active", "98%"),
            ("TestBot", "Active", "95%"),
            ("DeployPro", "Idle", "100%"),
            ("SecurityScan", "Active", "97%"),
            ("DocWriter", "Active", "92%"),
            ("PerfMonitor", "Idle", "99%"),
        ]
        
        for name, status, health in agents:
            color = "#10B981" if status == "Active" else "#64748B"
            st.markdown(
                f"""
                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 0.5rem;
                    background: #1E1E3F;
                    border-radius: 8px;
                    margin-bottom: 0.5rem;
                ">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="width: 8px; height: 8px; border-radius: 50%; background: {color};"></span>
                        <span style="color: #F1F5F9;">{name}</span>
                    </div>
                    <span style="color: #64748B;">{health}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        # Logs Preview
        st.markdown("### Recent Logs")
        
        logs = [
            ("INFO", "Mission #234 started successfully"),
            ("INFO", "Agent CodeMaster assigned"),
            ("WARN", "High memory usage detected"),
            ("INFO", "Execution completed"),
            ("ERROR", "Timeout on endpoint /api/test"),
        ]
        
        for level, message in logs:
            color = "#10B981" if level == "INFO" else "#F59E0B" if level == "WARN" else "#EF4444"
            st.markdown(
                f"""
                <div style="
                    font-size: 0.75rem;
                    padding: 0.25rem 0;
                    border-bottom: 1px solid #334155;
                ">
                    <span style="color: {color}; font-weight: 600;">{level}</span>
                    <span style="color: #64748B;"> {message}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
