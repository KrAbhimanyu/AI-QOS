"""Quality page for AI-QOS."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from components.core_components import (
    page_header,
    metric_card,
    status_badge,
)


def render_quality() -> None:
    """Render the quality assurance page."""
    page_header(
        title="Quality Assurance",
        subtitle="Code quality metrics and testing coverage",
        icon="✅",
        actions=["📊 Generate Report", "⚙️ Configure Rules"],
    )
    
    # Quality Overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Code Coverage", "87%", icon="🧪")
    with col2:
        metric_card("Code Quality", "A+", icon="📏")
    with col3:
        metric_card("Technical Debt", "2.3 days", icon="💳")
    with col4:
        metric_card("Issues Found", 12, icon="🐛")
    
    st.markdown("---")
    
    # Charts Row
    left_col, right_col = st.columns(2)
    
    with left_col:
        st.markdown("### Quality Score Trend")
        
        # Quality score over time
        fig = go.Figure()
        
        dates = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        scores = [85, 87, 86, 89, 91, 90, 92]
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=scores,
            mode="lines+markers+text",
            name="Quality Score",
            line=dict(color="#6366F1", width=3),
            marker=dict(size=12),
            text=scores,
            textposition="top center",
            textfont=dict(color="#F1F5F9"),
        ))
        
        # Add threshold line
        fig.add_hline(y=90, line_dash="dash", line_color="#10B981", annotation_text="Target: 90%")
        
        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=280,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis=dict(showgrid=False, color="#94A3B8"),
            yaxis=dict(showgrid=True, gridcolor="rgba(51, 65, 85, 0.5)", color="#94A3B8", range=[70, 100]),
        )
        st.plotly_chart(fig, width='stretch', key="quality_risk_chart")
    
    with right_col:
        st.markdown("### Issue Distribution")
        
        fig2 = go.Figure(data=[go.Bar(
            x=["Critical", "High", "Medium", "Low", "Info"],
            y=[2, 5, 18, 32, 15],
            marker_color=["#EF4444", "#F59E0B", "#6366F1", "#22D3EE", "#64748B"],
        )])
        
        fig2.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=280,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis=dict(showgrid=False, color="#94A3B8"),
            yaxis=dict(showgrid=True, gridcolor="rgba(51, 65, 85, 0.5)", color="#94A3B8"),
        )
        st.plotly_chart(fig2, width='stretch', key="quality_trend_chart")
    
    st.markdown("---")
    
    # Quality Metrics Details
    st.markdown("### Quality Metrics")
    
    metrics_data = [
        {"category": "Code Complexity", "score": 92, "change": "+3%"},
        {"category": "Code Duplication", "score": 78, "change": "+5%"},
        {"category": "Documentation", "score": 85, "change": "-2%"},
        {"category": "Security", "score": 96, "change": "+1%"},
        {"category": "Performance", "score": 88, "change": "+4%"},
        {"category": "Test Coverage", "score": 87, "change": "+7%"},
    ]
    
    for metric in metrics_data:
        color = "#10B981" if metric["score"] >= 90 else "#F59E0B" if metric["score"] >= 70 else "#EF4444"
        st.markdown(f"""<div style=" background: #1E1E3F; border-radius: 8px; padding: 1rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center; "> <span style="color: #F1F5F9;">{metric['category']}</span> <div style="display: flex; align-items: center; gap: 1rem;"> <div style="width: 150px; height: 6px; background: #334155; border-radius: 3px;"> <div style="width: {metric['score']}%; height: 100%; background: {color}; border-radius: 3px;"></div> </div> <span style="color: {color}; font-weight: 600; width: 50px; text-align: right;">{metric['score']}%</span> <span style="color: #10B981; width: 50px; text-align: right;">{metric['change']}</span> </div> </div>""", unsafe_allow_html=True)
