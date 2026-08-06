"""AI Reports & Analytics Components for AI-QOS."""

from datetime import datetime
from typing import Any, Optional
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# ============================================================================
# Session State Management
# ============================================================================

def init_reports_state() -> None:
    """Initialize reports session state."""
    defaults = {
        "reports_selected_report": None,
        "reports_date_range": "Last 30 days",
        "reports_view_mode": "dashboard",
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ============================================================================
# Metric Cards Component
# ============================================================================

def metric_card(title: str, value: str | int, subtitle: str = "", trend: str = "", icon: str = "📊") -> None:
    """Render a metric card."""
    trend_color = "#10b981" if trend.startswith("+") else "#ef4444" if trend.startswith("-") else "#64748b"
    
    st.markdown(f"""
    <div style="
        padding: 20px;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 16px;
        margin-bottom: 16px;
    ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <div style="font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">
                    {title}
                </div>
                <div style="font-size: 32px; font-weight: 700; color: #f8fafc; font-family: 'JetBrains Mono', monospace;">
                    {value}
                </div>
                {f'<div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">{subtitle}</div>' if subtitle else ''}
            </div>
            <div style="text-align: right;">
                <div style="font-size: 28px; margin-bottom: 8px;">{icon}</div>
                {f'<div style="font-size: 14px; font-weight: 600; color: {trend_color};">{trend}</div>' if trend else ''}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def metric_gauge(value: float, max_value: float, label: str, unit: str = "%", color: str = "#6366f1") -> None:
    """Render a circular gauge metric."""
    percentage = min((value / max_value) * 100, 100)
    
    st.markdown(f"""
    <div style="text-align: center; padding: 16px;">
        <div style="
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background: conic-gradient({color} {percentage}%, rgba(30, 41, 59, 0.8) 0%);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 12px;
        ">
            <div style="
                width: 80px;
                height: 80px;
                border-radius: 50%;
                background: rgba(15, 23, 42, 0.95);
                display: flex;
                align-items: center;
                justify-content: center;
            ">
                <span style="font-size: 20px; font-weight: 700; color: #f8fafc;">{value:.0f}{unit}</span>
            </div>
        </div>
        <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase;">{label}</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# Report Card Component
# ============================================================================

def report_card(report: dict[str, Any], compact: bool = False) -> None:
    """Render a report card."""
    type_icons = {
        "Executive Summary": "📈",
        "Test Coverage": "🧪",
        "Quality Metrics": "✅",
        "AI Performance": "🤖",
        "Regression Analysis": "🔄",
        "Flaky Test Analysis": "📳",
        "Trend Analysis": "📊",
        "Risk Assessment": "⚠️",
        "Compliance Report": "🛡️",
        "Custom Report": "📝",
    }
    
    icon = type_icons.get(report.get("type", ""), "📄")
    time_ago = _get_time_ago(report.get("created", datetime.now()))
    
    with st.container():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"**{icon} {report.get('title', 'Untitled')}**")
            st.markdown(f"<span style='font-size: 11px; color: #64748b;'>{report.get('type', '')} • {time_ago}</span>", unsafe_allow_html=True)
        
        with col2:
            status_colors = {"generated": "#10b981", "scheduled": "#f59e0b", "failed": "#ef4444", "draft": "#64748b"}
            status = report.get("status", "generated")
            st.markdown(f"<span style='padding: 2px 8px; background: {status_colors.get(status, '#64748b')}20; color: {status_colors.get(status, '#64748b')}; border-radius: 4px; font-size: 11px;'>{status.upper()}</span>", unsafe_allow_html=True)
        
        if not compact:
            st.markdown("---")


def _get_time_ago(dt: datetime) -> str:
    """Get human-readable time ago string."""
    diff = datetime.now() - dt
    if diff.total_seconds() < 3600:
        return f"{int(diff.total_seconds() / 60)}m ago"
    elif diff.total_seconds() < 86400:
        return f"{int(diff.total_seconds() / 3600)}h ago"
    else:
        return f"{int(diff.total_seconds() / 86400)}d ago"


# ============================================================================
# Coverage Chart Component
# ============================================================================

def coverage_chart(data: list[dict[str, Any]], title: str = "Test Coverage") -> None:
    """Render a horizontal bar chart for coverage."""
    if not data:
        st.info("No coverage data available.")
        return
    
    df_data = {
        "Module": [d["name"] for d in data],
        "Coverage": [d["coverage"] for d in data],
    }
    
    fig = px.bar(
        df_data,
        y="Module",
        x="Coverage",
        orientation="h",
        title=title,
        color="Coverage",
        color_continuous_scale=["#ef4444", "#f59e0b", "#10b981"],
        range_color=[0, 100],
    )
    
    fig.update_layout(
        height=max(300, len(data) * 50),
        paper_bgcolor="transparent",
        plot_bgcolor="transparent",
        font=dict(color="#f8fafc"),
        xaxis_title="Coverage %",
        yaxis_title="",
        showlegend=False,
    )
    
    fig.update_traces(
        marker_line_color="#1e293b",
        marker_line_width=1,
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# Trend Line Chart Component
# ============================================================================

def trend_chart(data: list[dict[str, Any]], title: str = "Trend", color: str = "#6366f1") -> None:
    """Render a line chart for trends."""
    if not data:
        st.info("No trend data available.")
        return
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=[d["date"] for d in data],
        y=[d["value"] for d in data],
        mode="lines+markers",
        line=dict(color=color, width=3),
        marker=dict(size=8, color=color, line=dict(color="#fff", width=2)),
        fill="tonexty" if len(data) > 1 else None,
        fillcolor=f"rgba{tuple(list(int(color[i:i+2], 16) for i in (1, 3, 5)) + [0.1])}",
    ))
    
    fig.update_layout(
        height=300,
        paper_bgcolor="transparent",
        plot_bgcolor="transparent",
        font=dict(color="#f8fafc", size=12),
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            linecolor="rgba(148, 163, 184, 0.2)",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(148, 163, 184, 0.1)",
            linecolor="rgba(148, 163, 184, 0.2)",
        ),
        margin=dict(l=40, r=20, t=40, b=40),
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# Pie Chart Component
# ============================================================================

def pie_chart(data: dict[str, Any], title: str = "Distribution") -> None:
    """Render a pie/donut chart."""
    if not data:
        st.info("No data available.")
        return
    
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        labels=list(data.keys()),
        values=list(data.values()),
        hole=0.4,
        marker=dict(colors=["#6366f1", "#22d3ee", "#10b981", "#f59e0b", "#ec4899", "#8b5cf6"]),
        textinfo="label+percent",
        textfont=dict(color="#f8fafc"),
    ))
    
    fig.update_layout(
        height=300,
        paper_bgcolor="transparent",
        showlegend=True,
        legend=dict(
            font=dict(color="#f8fafc"),
            bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(l=20, r=20, t=40, b=20),
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# Progress Bars Component
# ============================================================================

def progress_bar_section(data: list[dict[str, Any]], title: str = "Progress") -> None:
    """Render progress bars for multiple items."""
    st.markdown(f"#### {title}")
    
    for item in data:
        name = item.get("name", "Item")
        value = item.get("value", item.get("coverage", 0))
        max_val = item.get("max", 100)
        percentage = min((value / max_val) * 100, 100) if max_val else value
        
        color = "#10b981" if percentage >= 80 else "#f59e0b" if percentage >= 60 else "#ef4444"
        
        st.markdown(f"""
        <div style="margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="font-size: 13px; color: #f8fafc;">{name}</span>
                <span style="font-size: 13px; color: #94a3b8;">{value:.0f}%</span>
            </div>
            <div style="
                width: 100%;
                height: 8px;
                background: rgba(30, 41, 59, 0.8);
                border-radius: 4px;
                overflow: hidden;
            ">
                <div style="
                    width: {percentage}%;
                    height: 100%;
                    background: linear-gradient(90deg, {color}, {color}cc);
                    border-radius: 4px;
                    transition: width 0.3s ease;
                "></div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# Data Table Component
# ============================================================================

def data_table(data: list[dict[str, Any]], columns: list[str], title: str = "") -> None:
    """Render a styled data table."""
    if title:
        st.markdown(f"#### {title}")
    
    if not data:
        st.info("No data available.")
        return
    
    # Create table HTML
    header_html = "<tr>"
    for col in columns:
        header_html += f"<th style='padding: 12px; text-align: left; border-bottom: 2px solid #334155; color: #94a3b8; font-size: 11px; text-transform: uppercase;'>{col}</th>"
    header_html += "</tr>"
    
    rows_html = ""
    for row in data:
        rows_html += "<tr>"
        for col in columns:
            value = row.get(col.lower().replace(" ", "_"), row.get(col, ""))
            rows_html += f"<td style='padding: 12px; border-bottom: 1px solid rgba(148, 163, 184, 0.1); color: #f8fafc; font-size: 13px;'>{value}</td>"
        rows_html += "</tr>"
    
    st.markdown(f"""
    <div style="overflow-x: auto;">
        <table style="width: 100%; border-collapse: collapse;">
            <thead>{header_html}</thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# Risk Matrix Component
# ============================================================================

def risk_matrix(risks: list[dict[str, Any]], title: str = "Risk Matrix") -> None:
    """Render a risk matrix visualization."""
    st.markdown(f"### {title}")
    
    for risk in risks:
        score = risk.get("score", 0)
        area = risk.get("area", "Unknown")
        factors = risk.get("factors", [])
        
        # Color based on score
        if score >= 70:
            color = "#ef4444"
            level = "Critical"
        elif score >= 50:
            color = "#f59e0b"
            level = "High"
        elif score >= 30:
            color = "#3b82f6"
            level = "Medium"
        else:
            color = "#10b981"
            level = "Low"
        
        with st.expander(f"⚠️ {area} ({level} - {score})"):
            st.markdown(f"**Risk Score:** {score}")
            st.markdown("**Factors:**")
            for factor in factors:
                st.markdown(f"- {factor}")
            
            st.markdown(f"**Level:** <span style='color: {color};'>{level}</span>", unsafe_allow_html=True)


# ============================================================================
# Report Generator Component
# ============================================================================

def report_generator(templates: list[dict[str, Any]]) -> None:
    """Render report generator UI."""
    st.markdown("### 📝 Generate New Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.selectbox(
            "Report Type",
            options=[
                "Executive Summary",
                "Test Coverage",
                "Quality Metrics",
                "AI Performance",
                "Flaky Test Analysis",
                "Trend Analysis",
                "Risk Assessment",
            ],
        )
        
        period = st.selectbox(
            "Time Period",
            options=["Last 7 days", "Last 14 days", "Last 30 days", "Last 90 days", "Custom"],
        )
    
    with col2:
        modules = st.multiselect(
            "Modules to Include",
            options=["Authentication", "Product Catalog", "Shopping Cart", "Checkout", "Payment", "Search", "User Profile"],
            default=["Authentication", "Product Catalog", "Shopping Cart"],
        )
        
        format_type = st.selectbox(
            "Export Format",
            options=["HTML", "PDF", "CSV", "JSON"],
        )
    
    if st.button("🚀 Generate Report", use_container_width=True):
        st.success(f"Report generation started: {report_type}")
        st.info(f"Report will be exported as {format_type}")


# ============================================================================
# Scheduled Reports Component
# ============================================================================

def scheduled_reports_table(scheduled: list[dict[str, Any]]) -> None:
    """Render scheduled reports table."""
    st.markdown("### ⏰ Scheduled Reports")
    
    for report in scheduled:
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.markdown(f"**{report.get('title', 'Untitled')}**")
                st.markdown(f"<span style='font-size: 11px; color: #64748b;'>Next: {_get_time_ago(report.get('next_run', datetime.now()))}</span>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"<span style='font-size: 12px; color: #94a3b8;'>{report.get('schedule', '')}</span>", unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"<span style='font-size: 12px;'>👥 {report.get('recipients', 0)}</span>", unsafe_allow_html=True)
            
            with col4:
                if st.button("Run Now", key=f"run_{report['id']}", use_container_width=True):
                    st.info(f"Running {report.get('title')}")
            
            st.markdown("---")


# ============================================================================
# Export Panel Component
# ============================================================================

def export_panel() -> None:
    """Render export options panel."""
    st.markdown("### 📤 Export Options")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📄 PDF", use_container_width=True):
            st.info("Exporting as PDF...")
    
    with col2:
        if st.button("📊 CSV", use_container_width=True):
            st.info("Exporting as CSV...")
    
    with col3:
        if st.button("📋 JSON", use_container_width=True):
            st.info("Exporting as JSON...")
    
    with col4:
        if st.button("📧 Email", use_container_width=True):
            st.info("Email export configured...")


# ============================================================================
# AI Insights Component
# ============================================================================

def ai_insights(insights: list[str]) -> None:
    """Render AI-generated insights."""
    st.markdown("### 💡 AI Insights")
    
    for i, insight in enumerate(insights):
        icon = "🎯" if i == 0 else "📈" if i == 1 else "⚠️" if i == 2 else "💡"
        
        st.markdown(f"""
        <div style="
            padding: 14px;
            background: rgba(30, 41, 59, 0.6);
            border-left: 3px solid #6366f1;
            border-radius: 0 8px 8px 0;
            margin-bottom: 12px;
        ">
            <span style="font-size: 16px; margin-right: 8px;">{icon}</span>
            <span style="color: #f8fafc;">{insight}</span>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# Comparison Chart Component
# ============================================================================

def comparison_chart(data: dict[str, list], title: str = "Comparison") -> None:
    """Render a comparison chart with multiple metrics."""
    fig = go.Figure()
    
    colors = ["#6366f1", "#22d3ee", "#10b981", "#f59e0b", "#ec4899"]
    
    for i, (metric, values) in enumerate(data.items()):
        fig.add_trace(go.Scatter(
            x=list(range(len(values))),
            y=values,
            mode="lines+markers",
            name=metric,
            line=dict(color=colors[i % len(colors)], width=2),
            marker=dict(size=6),
        ))
    
    fig.update_layout(
        height=300,
        paper_bgcolor="transparent",
        plot_bgcolor="transparent",
        font=dict(color="#f8fafc"),
        legend=dict(
            font=dict(color="#f8fafc"),
            bgcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(
            showgrid=False,
            linecolor="rgba(148, 163, 184, 0.2)",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(148, 163, 184, 0.1)",
        ),
    )
    
    st.plotly_chart(fig, use_container_width=True)
