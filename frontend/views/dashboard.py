"""Dashboard page for AI-QOS."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from components.core_components import (
    page_header,
    metric_card,
    mission_card,
    status_badge,
    empty_state,
)


def render_dashboard() -> None:
    """Render the main dashboard page."""
    page_header(
        title="Dashboard",
        subtitle="AI Quality Operating System Overview",
        icon="📊",
    )
    
    # Key Metrics Row
    st.markdown("### Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_card("Total Missions", 127, delta="+12%", icon="🎯")
    with col2:
        metric_card("Active Agents", 8, delta="+2", icon="🤖")
    with col3:
        metric_card("Success Rate", "94.2%", delta="+2.1%", icon="✅")
    with col4:
        metric_card("Avg Execution", "2m 34s", delta="-15s", icon="⚡")
    
    st.markdown("---")
    
    # Two column layout
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        # Performance Chart
        st.markdown("### Performance Trend")
        
        # Generate sample data
        dates = [(datetime.now() - timedelta(days=i)) for i in range(7, -1, -1)]
        values = [75, 78, 82, 79, 85, 88, 91, 94]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[d.strftime("%b %d") for d in dates],
            y=values,
            mode="lines+markers",
            name="Success Rate",
            line=dict(color="#6366F1", width=3),
            marker=dict(size=10, color="#6366F1"),
            fill="tozeroy",
            fillcolor="rgba(99, 102, 241, 0.2)",
        ))
        
        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=300,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis=dict(
                showgrid=False,
                color="#94A3B8",
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(51, 65, 85, 0.5)",
                color="#94A3B8",
                range=[0, 100],
            ),
            hoverlabel=dict(
                bgcolor="#1E1E3F",
                bordercolor="#6366F1",
            ),
        )
        st.plotly_chart(fig, use_container_width=True, key="dashboard_perf_chart")
        
        # Mission Distribution
        st.markdown("### Mission Distribution")
        
        fig2 = go.Figure(data=[go.Pie(
            labels=["Code Review", "Testing", "Deployment", "Documentation", "Analysis"],
            values=[35, 28, 18, 12, 7],
            hole=0.6,
            marker=dict(colors=["#6366F1", "#22D3EE", "#F472B6", "#10B981", "#F59E0B"]),
        )])
        
        fig2.update_layout(
            template="plotly_dark",
            height=280,
            margin=dict(l=0, r=0, t=30, b=0),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(color="#94A3B8"),
            ),
        )
        st.plotly_chart(fig2, use_container_width=True, key="dashboard_mission_chart")
    
    with right_col:
        # Recent Missions
        st.markdown("### Recent Missions")
        
        recent_missions = [
            {"title": "PR #234 - Auth Module Review", "desc": "Review authentication changes", "status": "completed", "time": "5 min ago"},
            {"title": "API Testing Pipeline", "desc": "Run integration tests", "status": "running", "time": "2 min ago"},
            {"title": "Deploy to Staging", "desc": "Deploy v2.1.0 to staging", "status": "pending", "time": "10 min ago"},
            {"title": "Code Analysis Run", "desc": "Weekly code quality scan", "status": "completed", "time": "1 hour ago"},
        ]
        
        for mission in recent_missions:
            st.markdown(f"""<div style=" background: #1E1E3F; border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 0.5rem; border-left: 3px solid {'#10B981' if mission['status'] == 'completed' else '#6366F1' if mission['status'] == 'running' else '#F59E0B'}; "> <div style="display: flex; justify-content: space-between; align-items: center;"> <div> <p style="margin: 0; color: #F1F5F9; font-size: 0.875rem; font-weight: 500;">{mission['title']}</p> <p style="margin: 0.25rem 0 0; color: #64748B; font-size: 0.75rem;">{mission['desc']}</p> </div> <span style="color: #64748B; font-size: 0.7rem;">{mission['time']}</span> </div> </div>""", unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown("### Quick Actions")
        
        quick_actions = [
            ("🚀", "New Mission", "#6366F1"),
            ("📊", "View Reports", "#22D3EE"),
            ("⚙️", "Configure", "#F472B6"),
        ]
        
        for icon, label, color in quick_actions:
            st.button(
                f"{icon} {label}",
                use_container_width=True,
                type="secondary",
            )
