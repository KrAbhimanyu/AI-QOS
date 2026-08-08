"""Reports page for AI-QOS."""
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
from components.core_components import (
    page_header,
    metric_card,
    empty_state,
)


def render_reports() -> None:
    """Render the reports page."""
    page_header(
        title="Reports",
        subtitle="Generate and view quality reports",
        icon="📈",
        actions=["📄 Generate Report", "📥 Export"],
    )
    
    # Filters
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        report_type = st.selectbox("Report Type", ["Quality Summary", "Agent Performance", "Mission History", "Custom"])
    with col2:
        date_range = st.selectbox("Date Range", ["Last 7 days", "Last 30 days", "Last 90 days", "Custom"])
    with col3:
        st.text_input("Search reports...")
    
    st.markdown("---")
    
    # Report Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Reports", 45, icon="📄")
    with col2:
        metric_card("This Month", 8, icon="📅")
    with col3:
        metric_card("Avg Generation", "12s", icon="⏱️")
    with col4:
        metric_card("Storage Used", "1.2 GB", icon="💾")
    
    st.markdown("---")
    
    # Report Preview Area
    st.markdown("### Report Preview")
    
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        # Report visualization
        st.markdown("""<div style=" background: linear-gradient(135deg, #1E1E3F 0%, rgba(99, 102, 241, 0.1) 100%); border: 1px solid #334155; border-radius: 12px; padding: 2rem; text-align: center; "> <h3 style="color: #F1F5F9; margin-bottom: 1rem;">📊 Weekly Quality Summary</h3> <p style="color: #94A3B8; margin-bottom: 2rem;">Generated: July 29, 2024</p> </div>""", unsafe_allow_html=True)
        
        # Activity Chart
        st.markdown("#### Mission Activity")
        
        dates = [(datetime.now() - timedelta(days=i)) for i in range(7, -1, -1)]
        
        fig = go.Figure()
        
        # Completed
        completed = [12, 15, 18, 14, 20, 22, 19]
        fig.add_trace(go.Bar(
            x=[d.strftime("%a") for d in dates],
            y=completed,
            name="Completed",
            marker_color="#10B981",
        ))
        
        # Failed
        failed = [1, 0, 2, 1, 1, 0, 2]
        fig.add_trace(go.Bar(
            x=[d.strftime("%a") for d in dates],
            y=failed,
            name="Failed",
            marker_color="#EF4444",
        ))
        
        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=250,
            margin=dict(l=0, r=0, t=30, b=0),
            barmode="group",
            xaxis=dict(showgrid=False, color="#94A3B8"),
            yaxis=dict(showgrid=True, gridcolor="rgba(51, 65, 85, 0.5)", color="#94A3B8"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig, width='stretch', key="reports_chart")
    
    with right_col:
        # Recent Reports
        st.markdown("### Recent Reports")
        
        reports = [
            ("Weekly Quality Summary", "Jul 29, 2024", "Quality", "PDF"),
            ("Agent Performance", "Jul 28, 2024", "Analytics", "CSV"),
            ("Mission History", "Jul 27, 2024", "History", "PDF"),
            ("Code Analysis Report", "Jul 25, 2024", "Quality", "HTML"),
            ("Deployment Summary", "Jul 24, 2024", "Deployment", "JSON"),
        ]
        
        for name, date, category, format_type in reports:
            st.markdown(f"""<div style=" background: #1E1E3F; border-radius: 8px; padding: 0.75rem; margin-bottom: 0.5rem; cursor: pointer; transition: all 0.2s; "> <div style="display: flex; justify-content: space-between; align-items: start;"> <div> <p style="margin: 0; color: #F1F5F9; font-size: 0.875rem; font-weight: 500;">{name}</p> <p style="margin: 0.25rem 0 0; color: #64748B; font-size: 0.75rem;">{date}</p> </div> <span style=" background: #334155; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.65rem; color: #94A3B8; ">{format_type}</span> </div> </div>""", unsafe_allow_html=True)
