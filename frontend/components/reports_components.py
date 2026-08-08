"""AI Reports & Analytics Components for AI-QOS.

Premium Executive Quality Intelligence Center components built on the
AI-QOS UI Foundation. All styling derives from design tokens
(themes/tokens.py) and shared foundation components (components/shared.py).
Public function names and signatures are preserved for backward
compatibility — no breaking changes. New components are additive.
"""

from datetime import datetime
from typing import Any, Optional
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

try:
    from frontend.themes.tokens import (
        COLORS, SPACING, TYPOGRAPHY, BORDERS, SHADOWS, ANIMATIONS,
        get_status_color, get_confidence_color, get_health_color, get_priority_color,
    )
    from frontend.components.shared import (
        section_header, glass_panel, glass_card, metric_card as _shared_metric_card,
        status_badge, priority_badge, progress_bar, health_bar, confidence_bar,
        empty_state, spacer, divider, pulse_dot, timeline_item, notification,
    )
    from frontend.mock.reports import (
        REPORTS_HERO_KPIS, REPORTS_KPI_METRICS, AI_EXECUTIVE_SUMMARY,
        QUALITY_SCORES, BUSINESS_FLOW_QUALITY, BUG_INTELLIGENCE,
        EXECUTION_INTELLIGENCE, AI_PERFORMANCE_INTEL, RELEASE_READINESS,
        QUALITY_GATES, COVERAGE_INTELLIGENCE, FLAKY_CATEGORIES,
        QUALITY_RISK_MATRIX, AI_RECOMMENDATIONS, QUALITY_TIMELINE,
        RELEASE_COMPARISON, REPORT_LIBRARY, REPORTS_QUICK_ACTIONS,
        REPORTS_BOTTOM_TABS, TREND_VIEWS,
    )
except ImportError:  # pragma: no cover - fallback for direct execution
    from themes.tokens import (
        COLORS, SPACING, TYPOGRAPHY, BORDERS, SHADOWS, ANIMATIONS,
        get_status_color, get_confidence_color, get_health_color, get_priority_color,
    )
    from shared import (
        section_header, glass_panel, glass_card, metric_card as _shared_metric_card,
        status_badge, priority_badge, progress_bar, health_bar, confidence_bar,
        empty_state, spacer, divider, pulse_dot, timeline_item, notification,
    )
    from mock.reports import (
        REPORTS_HERO_KPIS, REPORTS_KPI_METRICS, AI_EXECUTIVE_SUMMARY,
        QUALITY_SCORES, BUSINESS_FLOW_QUALITY, BUG_INTELLIGENCE,
        EXECUTION_INTELLIGENCE, AI_PERFORMANCE_INTEL, RELEASE_READINESS,
        QUALITY_GATES, COVERAGE_INTELLIGENCE, FLAKY_CATEGORIES,
        QUALITY_RISK_MATRIX, AI_RECOMMENDATIONS, QUALITY_TIMELINE,
        RELEASE_COMPARISON, REPORT_LIBRARY, REPORTS_QUICK_ACTIONS,
        REPORTS_BOTTOM_TABS, TREND_VIEWS,
    )


# ============================================================================
# Token shortcuts
# ============================================================================

_SEMANTIC_COLORS = {
    "primary": COLORS.PRIMARY,
    "secondary": COLORS.SECONDARY,
    "accent": COLORS.ACCENT,
    "info": COLORS.INFO,
    "success": COLORS.SUCCESS,
    "warning": COLORS.WARNING,
    "error": COLORS.ERROR,
    "muted": COLORS.TEXT_MUTED,
}


def _hex_to_rgb(hex_color: str) -> str:
    h = hex_color.lstrip('#')
    return f"{int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}"


_SEMANTIC_RGB = {
    "primary": COLORS.PRIMARY_RGB,
    "secondary": COLORS.SECONDARY_RGB,
    "accent": COLORS.ACCENT_RGB,
    "info": COLORS.INFO_RGB,
    "success": COLORS.SUCCESS_RGB,
    "warning": COLORS.WARNING_RGB,
    "error": COLORS.ERROR_RGB,
    "muted": _hex_to_rgb(COLORS.TEXT_MUTED),
}

_GLASS_PANEL_BG = f"linear-gradient(135deg, {COLORS.SURFACE} 0%, rgba({COLORS.PRIMARY_RGB}, 0.12) 100%)"
_GLASS_PANEL_BORDER = f"rgba({COLORS.PRIMARY_RGB}, 0.25)"
_PANEL_BORDER = COLORS.BORDER
_CHART_PAPER_BG = "rgba(0,0,0,0)"
_CHART_GRID = f"rgba({COLORS.BORDER_RGB}, 0.2)"


def _semantic(name: str) -> str:
    return _SEMANTIC_COLORS.get(name, COLORS.PRIMARY)


def _semantic_rgb(name: str) -> str:
    return _SEMANTIC_RGB.get(name, COLORS.PRIMARY_RGB)


def _status_color(status: str) -> str:
    return get_status_color(status)


def _risk_color(risk: str) -> str:
    return {
        "low": COLORS.SUCCESS,
        "medium": COLORS.WARNING,
        "high": COLORS.ERROR,
        "critical": COLORS.ERROR,
    }.get(risk, COLORS.TEXT_MUTED)


def _coverage_color(coverage: float) -> str:
    if coverage >= 80:
        return COLORS.SUCCESS
    if coverage >= 60:
        return COLORS.WARNING
    return COLORS.ERROR


def _severity_color(severity: str) -> str:
    sev = severity.lower()
    return {
        "critical": COLORS.ERROR,
        "high": COLORS.WARNING,
        "medium": COLORS.INFO,
        "low": COLORS.TEXT_MUTED,
    }.get(sev, COLORS.TEXT_MUTED)


def _escape(text: Any) -> str:
    if text is None:
        return ""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _apply_chart_theme(fig: go.Figure, height: int = 300, show_legend: bool = False) -> go.Figure:
    """Apply the enterprise chart theme (tokens) to a plotly figure."""
    fig.update_layout(
        height=height,
        paper_bgcolor=_CHART_PAPER_BG,
        plot_bgcolor=_CHART_PAPER_BG,
        font=dict(color=COLORS.TEXT_PRIMARY, size=12),
        showlegend=show_legend,
        legend=dict(font=dict(color=COLORS.TEXT_PRIMARY), bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(showgrid=False, linecolor=_CHART_GRID),
        yaxis=dict(showgrid=True, gridcolor=f"rgba({COLORS.BORDER_RGB}, 0.1)", linecolor=_CHART_GRID),
        margin=dict(l=40, r=20, t=40, b=40),
    )
    return fig


# ============================================================================
# Session State Management (preserved keys + additive keys)
# ============================================================================

def init_reports_state() -> None:
    """Initialize reports session state (preserved keys)."""
    defaults = {
        "reports_selected_report": None,
        "reports_date_range": "Last 30 days",
        "reports_view_mode": "dashboard",
        "reports_bottom_tab": "Dashboard",
        "reports_selected_flow": "flow_login",
        "reports_trend_view": "Weekly",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ============================================================================
# Metric Cards Component (preserved signature) — token-driven
# ============================================================================

def metric_card(title: str, value: str | int, subtitle: str = "", trend: str = "", icon: str = "📊") -> None:
    """Render a metric card (preserved signature) with token styling."""
    if trend.startswith("+"):
        trend_color = COLORS.SUCCESS
    elif trend.startswith("-"):
        trend_color = COLORS.ERROR
    else:
        trend_color = COLORS.TEXT_MUTED

    st.markdown(f"""<div style=" padding:{SPACING.SPACE_6}; background:{_GLASS_PANEL_BG}; border:{BORDERS.WIDTH_THIN} solid {_GLASS_PANEL_BORDER}; border-radius:{BORDERS.RADIUS_LG}; margin-bottom:{SPACING.SPACE_4}; box-shadow:{SHADOWS.CARD}; "> <div style="display:flex;justify-content:space-between;align-items:flex-start;"> <div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;letter-spacing:1px;margin-bottom:{SPACING.SPACE_2};"> {_escape(title)} </div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_3XL};font-weight:700;color:{COLORS.TEXT_PRIMARY};font-family:{TYPOGRAPHY.FONT_MONO};"> {_escape(str(value))} </div> {f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_SECONDARY};margin-top:{SPACING.SPACE_1};">{_escape(subtitle)}</div>' if subtitle else ''} </div> <div style="text-align:right;"> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_2XL};margin-bottom:{SPACING.SPACE_2};">{icon}</div> {f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_BASE};font-weight:600;color:{trend_color};">{trend}</div>' if trend else ''} </div> </div> </div>""", unsafe_allow_html=True)


def metric_gauge(value: float, max_value: float, label: str, unit: str = "%", color: str = COLORS.PRIMARY) -> None:
    """Render a circular gauge metric (preserved signature) with token styling."""
    percentage = min((value / max_value) * 100, 100) if max_value else 0
    color_rgb = _hex_to_rgb(color)

    st.markdown(f"""<div style="text-align:center;padding:{SPACING.SPACE_4};"> <div style=" width:110px;height:110px;border-radius:50%; background:conic-gradient({color} {percentage}%, rgba({COLORS.SURFACE_RGB},0.8) 0%); display:flex;align-items:center;justify-content:center; margin:0 auto {SPACING.SPACE_3}; box-shadow:0 0 20px rgba({color_rgb},0.3); "> <div style=" width:84px;height:84px;border-radius:50%; background:{COLORS.SURFACE}; display:flex;align-items:center;justify-content:center; "> <span style="font-size:{TYPOGRAPHY.FONT_SIZE_XL};font-weight:700;color:{COLORS.TEXT_PRIMARY};">{value:.0f}{unit}</span> </div> </div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_SECONDARY};text-transform:uppercase;">{_escape(label)}</div> </div>""", unsafe_allow_html=True)


# ============================================================================
# Report Card Component (preserved signature) — token-driven
# ============================================================================

def report_card(report: dict[str, Any], compact: bool = False) -> None:
    """Render a report card (preserved signature) with token styling."""
    type_icons = {
        "Executive Summary": "📈", "Test Coverage": "🧪", "Quality Metrics": "✅",
        "AI Performance": "🤖", "Regression Analysis": "🔄",
        "Flaky Test Analysis": "📳", "Trend Analysis": "📊",
        "Risk Assessment": "⚠️", "Compliance Report": "🛡️", "Custom Report": "📝",
    }
    icon = type_icons.get(report.get("type", ""), "📄")
    time_ago = _get_time_ago(report.get("created", datetime.now()))
    status_colors = {
        "generated": COLORS.SUCCESS, "scheduled": COLORS.WARNING,
        "failed": COLORS.ERROR, "draft": COLORS.TEXT_MUTED,
    }
    status = report.get("status", "generated")
    status_str = status.value if hasattr(status, "value") else str(status)
    color = status_colors.get(status_str, COLORS.TEXT_MUTED)
    color_rgb = _hex_to_rgb(color)
    type_str = report.get("type", "")
    type_display = type_str.value if hasattr(type_str, "value") else str(type_str)

    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{icon} {_escape(report.get('title', 'Untitled'))}**")
            st.markdown(
                f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">'
                f'{_escape(type_display)} • {time_ago}</span>',
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f'<span style="padding:2px 8px;background:rgba({color_rgb},0.2);color:{color};'
                f'border-radius:{BORDERS.RADIUS_SM};font-size:{TYPOGRAPHY.FONT_SIZE_XS};font-weight:600;">'
                f'{status_str.upper()}</span>',
                unsafe_allow_html=True,
            )
        if not compact:
            st.markdown("---")


def _get_time_ago(dt: datetime) -> str:
    """Get human-readable time ago string (preserved)."""
    diff = datetime.now() - dt
    if diff.total_seconds() < 3600:
        return f"{int(diff.total_seconds() / 60)}m ago"
    elif diff.total_seconds() < 86400:
        return f"{int(diff.total_seconds() / 3600)}h ago"
    else:
        return f"{int(diff.total_seconds() / 86400)}d ago"


# ============================================================================
# Coverage Chart Component (preserved signature) — token-driven
# ============================================================================

def coverage_chart(data: list[dict[str, Any]], title: str = "Test Coverage") -> None:
    """Render a horizontal bar chart for coverage (preserved signature)."""
    section_header(title, icon="📊")
    if not data:
        empty_state(icon="📊", title="No Coverage Data", description="No coverage data available.")
        return

    df_data = {
        "Module": [d["name"] for d in data],
        "Coverage": [d["coverage"] for d in data],
    }
    fig = px.bar(
        df_data, y="Module", x="Coverage", orientation="h",
        color="Coverage",
        color_continuous_scale=[COLORS.ERROR, COLORS.WARNING, COLORS.SUCCESS],
        range_color=[0, 100],
    )
    fig.update_layout(
        height=max(300, len(data) * 50),
        paper_bgcolor=_CHART_PAPER_BG, plot_bgcolor=_CHART_PAPER_BG,
        font=dict(color=COLORS.TEXT_PRIMARY),
        xaxis_title="Coverage %", yaxis_title="", showlegend=False,
    )
    fig.update_traces(marker_line_color=COLORS.SURFACE, marker_line_width=1)
    st.plotly_chart(fig, use_container_width=True, key=f"reports_cov_chart_{title}")


# ============================================================================
# Trend Line Chart Component (preserved signature) — token-driven
# ============================================================================

def trend_chart(data: list[dict[str, Any]], title: str = "Trend", color: str = COLORS.PRIMARY) -> None:
    """Render a line chart for trends (preserved signature)."""
    if not data:
        empty_state(icon="📈", title="No Trend Data", description="No trend data available.")
        return

    fig = go.Figure()
    color_rgb = _hex_to_rgb(color)
    fig.add_trace(go.Scatter(
        x=[d["date"] for d in data],
        y=[d["value"] for d in data],
        mode="lines+markers",
        line=dict(color=color, width=3),
        marker=dict(size=8, color=color, line=dict(color=COLORS.TEXT_PRIMARY, width=2)),
        fill="tonexty" if len(data) > 1 else None,
        fillcolor=f"rgba({color_rgb}, 0.1)",
    ))
    _apply_chart_theme(fig, height=300)
    st.plotly_chart(fig, use_container_width=True, key=f"reports_trend_chart_{title}_{color}")


# ============================================================================
# Pie Chart Component (preserved signature) — token-driven
# ============================================================================

def pie_chart(data: dict[str, Any], title: str = "Distribution") -> None:
    """Render a pie/donut chart (preserved signature)."""
    if not data:
        empty_state(icon="📊", title="No Data", description="No data available.")
        return

    palette = [COLORS.PRIMARY, COLORS.SECONDARY, COLORS.SUCCESS, COLORS.WARNING,
               COLORS.ACCENT, COLORS.INFO, COLORS.TEXT_MUTED]
    fig = go.Figure(go.Pie(
        labels=list(data.keys()), values=list(data.values()), hole=0.4,
        marker=dict(colors=palette[:len(data)]),
        textfont=dict(color=COLORS.TEXT_PRIMARY),
    ))
    _apply_chart_theme(fig, height=300)
    st.plotly_chart(fig, use_container_width=True, key=f"reports_pie_chart_{title}")


# ============================================================================
# Progress Bar Section (preserved signature) — token-driven
# ============================================================================

def progress_bar_section(data: list[dict[str, Any]], title: str = "Progress") -> None:
    """Render a section of progress bars (preserved signature)."""
    section_header(title, icon="📊")
    for item in data:
        label = item.get("label", item.get("name", ""))
        value = item.get("value", item.get("coverage", 0))
        color = _semantic(item.get("color", "primary"))
        progress_bar(value, 100, color, "8px")


# ============================================================================
# Data Table (preserved signature) — token-driven
# ============================================================================

def data_table(data: list[dict[str, Any]], columns: list[str], title: str = "") -> None:
    """Render a data table (preserved signature) with token styling."""
    if title:
        section_header(title, icon="📋")
    if not data:
        empty_state(icon="📋", title="No Data", description="No rows to display.")
        return

    header_html = "<tr>"
    for col in columns:
        header_html += f"<th style='padding:{SPACING.SPACE_3};text-align:left;border-bottom:2px solid {COLORS.BORDER};color:{COLORS.TEXT_SECONDARY};font-size:{TYPOGRAPHY.FONT_SIZE_XS};text-transform:uppercase;'>{_escape(col)}</th>"
    header_html += "</tr>"

    rows_html = ""
    for row in data:
        rows_html += "<tr>"
        for col in columns:
            value = row.get(col.lower().replace(" ", "_"), row.get(col, ""))
            rows_html += f"<td style='padding:{SPACING.SPACE_3};border-bottom:1px solid rgba({COLORS.BORDER_RGB},0.2);color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};'>{_escape(str(value))}</td>"
        rows_html += "</tr>"

    st.markdown(f"""<div style="overflow-x:auto;"> <table style="width:100%;border-collapse:collapse;"> <thead>{header_html}</thead> <tbody>{rows_html}</tbody> </table> </div>""", unsafe_allow_html=True)


# ============================================================================
# Risk Matrix (preserved signature) — token-driven
# ============================================================================

def risk_matrix(risks: list[dict[str, Any]], title: str = "Risk Matrix") -> None:
    """Render a risk matrix visualization (preserved signature)."""
    section_header(title, icon="⚠️")
    for risk in risks:
        score = risk.get("score", 0)
        area = risk.get("area", "Unknown")
        factors = risk.get("factors", [])
        if score >= 70:
            color, level = COLORS.ERROR, "Critical"
        elif score >= 50:
            color, level = COLORS.WARNING, "High"
        elif score >= 30:
            color, level = COLORS.INFO, "Medium"
        else:
            color, level = COLORS.SUCCESS, "Low"
        with st.expander(f"⚠️ {_escape(area)} ({level} - {score})"):
            st.markdown(f"**Risk Score:** {score}")
            st.markdown("**Factors:**")
            for factor in factors:
                st.markdown(f"- {_escape(factor)}")
            st.markdown(f"**Level:** <span style='color:{color};font-weight:600;'>{level}</span>", unsafe_allow_html=True)


# ============================================================================
# Report Generator (preserved signature) — token-driven
# ============================================================================

def report_generator(templates: list[dict[str, Any]]) -> None:
    """Render report generator UI (preserved signature)."""
    section_header("Generate New Report", icon="📝")
    col1, col2 = st.columns(2)
    with col1:
        report_type = st.selectbox("Report Type", options=[
            "Executive Summary", "Test Coverage", "Quality Metrics",
            "AI Performance", "Flaky Test Analysis", "Trend Analysis", "Risk Assessment",
        ])
        period = st.selectbox("Time Period", options=[
            "Last 7 days", "Last 14 days", "Last 30 days", "Last 90 days", "Custom",
        ])
    with col2:
        modules = st.multiselect("Modules to Include", options=[
            "Authentication", "Product Catalog", "Shopping Cart",
            "Checkout", "Payment", "Search", "User Profile",
        ], default=["Authentication", "Product Catalog", "Shopping Cart"])
        format_type = st.selectbox("Export Format", options=["HTML", "PDF", "CSV", "JSON"])
    if st.button("🚀 Generate Report", use_container_width=True, key="reports_generate_btn"):
        st.success(f"Report generation started: {report_type}")
        st.info(f"Report will be exported as {format_type}")


# ============================================================================
# Scheduled Reports Table (preserved signature) — token-driven
# ============================================================================

def scheduled_reports_table(scheduled: list[dict[str, Any]]) -> None:
    """Render scheduled reports table (preserved signature)."""
    section_header("Scheduled Reports", icon="⏰")
    for report in scheduled:
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.markdown(f"**{_escape(report.get('title', 'Untitled'))}**")
                st.markdown(
                    f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">'
                    f'Next: {_get_time_ago(report.get("next_run", datetime.now()))}</span>',
                    unsafe_allow_html=True,
                )
            with col2:
                st.markdown(
                    f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_SECONDARY};">'
                    f'{_escape(report.get("schedule", ""))}</span>',
                    unsafe_allow_html=True,
                )
            with col3:
                st.markdown(
                    f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_PRIMARY};">'
                    f'👥 {report.get("recipients", 0)}</span>',
                    unsafe_allow_html=True,
                )
            with col4:
                if st.button("Run Now", key=f"run_{report['id']}", use_container_width=True):
                    st.toast(f"Running {report.get('title')}", icon="⏰")
            st.markdown("---")


# ============================================================================
# Export Panel (preserved signature) — token-driven
# ============================================================================

def export_panel() -> None:
    """Render export options panel (preserved signature)."""
    section_header("Export Options", icon="📤")
    formats = [
        ("📄 PDF", "Exporting as PDF..."),
        ("📊 CSV", "Exporting as CSV..."),
        ("📋 JSON", "Exporting as JSON..."),
        ("📧 Email", "Email export configured..."),
    ]
    cols = st.columns(len(formats))
    for col, (label, msg) in zip(cols, formats):
        with col:
            if st.button(label, use_container_width=True, key=f"export_{label}"):
                st.toast(msg, icon="📤")


# ============================================================================
# AI Insights (preserved signature) — token-driven
# ============================================================================

def ai_insights(insights: list[str]) -> None:
    """Render AI-generated insights (preserved signature) with token styling."""
    section_header("AI Insights", icon="💡")
    icons = ["🎯", "📈", "⚠️", "💡"]
    for i, insight in enumerate(insights):
        icon = icons[i % len(icons)]
        st.markdown(f"""<div style=" padding:{SPACING.SPACE_4}; background:rgba({COLORS.SURFACE_RGB},0.6); border-left:3px solid {COLORS.PRIMARY}; border-radius:0 {BORDERS.RADIUS_MD} {BORDERS.RADIUS_MD} 0; margin-bottom:{SPACING.SPACE_3}; "> <span style="font-size:16px;margin-right:{SPACING.SPACE_2};">{icon}</span> <span style="color:{COLORS.TEXT_PRIMARY};">{_escape(insight)}</span> </div>""", unsafe_allow_html=True)


# ============================================================================
# Comparison Chart (preserved signature) — token-driven
# ============================================================================

def comparison_chart(data: dict[str, list], title: str = "Comparison") -> None:
    """Render a comparison chart with multiple metrics (preserved signature)."""
    section_header(title, icon="📊")
    fig = go.Figure()
    colors = [COLORS.PRIMARY, COLORS.SECONDARY, COLORS.SUCCESS, COLORS.WARNING, COLORS.ACCENT]
    for i, (metric, values) in enumerate(data.items()):
        fig.add_trace(go.Scatter(
            x=list(range(len(values))), y=values, mode="lines+markers", name=metric,
            line=dict(color=colors[i % len(colors)], width=2), marker=dict(size=6),
        ))
    _apply_chart_theme(fig, height=300, show_legend=True)
    st.plotly_chart(fig, use_container_width=True, key=f"reports_comparison_{title}")


# ============================================================================
# NEW ADDITIVE COMPONENTS — Executive Quality Intelligence Center
# ============================================================================

def reports_hero_header(info: dict[str, Any]) -> None:
    """Display the premium executive hero header with KPI chips."""
    quality = 87
    quality_color = get_health_color(quality)
    quality_rgb = _hex_to_rgb(quality_color)
    readiness = RELEASE_READINESS["score"]
    readiness_color = get_health_color(readiness)
    readiness_rgb = _hex_to_rgb(readiness_color)

    stat_chips = "".join(
        f'<div style="display:flex;flex-direction:column;align-items:center;gap:2px;'
        f'padding:{SPACING.SPACE_2} {SPACING.SPACE_4};'
        f'background:rgba({COLORS.SURFACE_RGB},0.7);'
        f'border:1px solid {_GLASS_PANEL_BORDER};'
        f'border-radius:{BORDERS.RADIUS_MD};min-width:96px;">'
        f'<span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};'
        f'text-transform:uppercase;letter-spacing:1px;">{_escape(k["label"])}</span>'
        f'<span style="color:{_semantic(k["color"])};font-size:{TYPOGRAPHY.FONT_SIZE_SM};'
        f'font-weight:600;display:flex;align-items:center;gap:4px;">'
        f'<span style="font-size:0.9rem;">{k["icon"]}</span>{_escape(str(k["value"]))}'
        f'</span></div>'
        for k in REPORTS_HERO_KPIS
    )

    st.markdown(f"""<div style=" background:{_GLASS_PANEL_BG}; border:1px solid {_GLASS_PANEL_BORDER}; border-radius:{BORDERS.RADIUS_XL}; padding:{SPACING.SPACE_6}; margin-bottom:{SPACING.SPACE_4}; box-shadow:{SHADOWS.CARD}; position:sticky;top:0;z-index:10; backdrop-filter:blur(12px); "> <div style="display:flex;align-items:center;justify-content:space-between; flex-wrap:wrap;gap:{SPACING.SPACE_4};margin-bottom:{SPACING.SPACE_4};"> <div> <div style="display:flex;align-items:center;gap:{SPACING.SPACE_2};margin-bottom:{SPACING.SPACE_2};"> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">🏠 Dashboard</span> <span style="color:{COLORS.TEXT_MUTED};">›</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">Reports & Analytics</span> <span style="color:{COLORS.TEXT_MUTED};">›</span> <span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">Executive Intelligence</span> </div> <div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};flex-wrap:wrap;"> <h1 style="margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_2XL};color:{COLORS.TEXT_PRIMARY};font-weight:600;"> 📊 Executive Quality Intelligence Center </h1> <span style="display:inline-flex;align-items:center;gap:{SPACING.SPACE_2}; padding:{SPACING.SPACE_1} {SPACING.SPACE_3}; background:rgba({quality_rgb},0.2);color:{quality_color}; border:1px solid rgba({quality_rgb},0.4); border-radius:{BORDERS.RADIUS_FULL}; font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;"> <span style="width:8px;height:8px;border-radius:50%;background:{quality_color};animation:{ANIMATIONS.PULSE};"></span> Quality {quality}% </span> <span style="display:inline-flex;align-items:center;gap:{SPACING.SPACE_2}; padding:{SPACING.SPACE_1} {SPACING.SPACE_3}; background:rgba({readiness_rgb},0.2);color:{readiness_color}; border:1px solid rgba({readiness_rgb},0.4); border-radius:{BORDERS.RADIUS_FULL}; font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;"> 🚀 Release {readiness}% </span> </div> <p style="margin:{SPACING.SPACE_2} 0 0;color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};"> Enterprise Quality Operating Center • {info.get('total_reports', 0)} reports • {info.get('dashboards', 0)} dashboards • Last updated 5m ago </p> </div> <div style="display:flex;align-items:center;gap:{SPACING.SPACE_2};flex-wrap:wrap;"> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};border:1px solid {_PANEL_BORDER};border-radius:{BORDERS.RADIUS_MD};padding:{SPACING.SPACE_1} {SPACING.SPACE_3};" title="Search reports">🔍 Search…</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};border:1px solid {_PANEL_BORDER};border-radius:{BORDERS.RADIUS_MD};padding:{SPACING.SPACE_1} {SPACING.SPACE_3};" title="Command palette">⌘K Command</span> <span style="color:{COLORS.TEXT_MUTED};font-size:1rem;cursor:pointer;" title="Notifications">🔔</span> <span style="color:{COLORS.TEXT_MUTED};font-size:1rem;cursor:pointer;" title="Fullscreen">⛶</span> </div> </div> <div style="display:flex;gap:{SPACING.SPACE_2};flex-wrap:wrap;">{stat_chips}</div> </div>""", unsafe_allow_html=True)


def reports_kpi_strip() -> None:
    """Display the executive KPI strip as a MetricCard grid."""
    for i in range(0, len(REPORTS_KPI_METRICS), 4):
        row = REPORTS_KPI_METRICS[i:i + 4]
        cols = st.columns(len(row))
        for col, m in zip(cols, row):
            with col:
                metric_card(
                    title=m["title"], value=m["value"],
                    subtitle=m.get("subtitle", ""), trend=m.get("trend", ""),
                    icon=m.get("icon", ""),
                )


def ai_executive_summary() -> None:
    """Render the premium AI executive intelligence panel."""
    section_header("AI Executive Summary", icon="🧠")
    s = AI_EXECUTIVE_SUMMARY
    conf_color = get_confidence_color(s["confidence"])
    conf_rgb = _hex_to_rgb(conf_color)

    # Overall assessment
    st.markdown(f"""<div style="padding:{SPACING.SPACE_4};background:linear-gradient(135deg, rgba({COLORS.PRIMARY_RGB},0.15), rgba({COLORS.SECONDARY_RGB},0.15));border:1px solid rgba({COLORS.PRIMARY_RGB},0.3);border-radius:{BORDERS.RADIUS_LG};margin-bottom:{SPACING.SPACE_4};"> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;margin-bottom:{SPACING.SPACE_2};">Overall Assessment</div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_BASE};color:{COLORS.TEXT_PRIMARY};line-height:1.5;">{_escape(s["overall_assessment"])}</div> </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(_summary_list("Key Findings", s["key_findings"], COLORS.PRIMARY), unsafe_allow_html=True)
        spacer(1)
        st.markdown(_summary_list("Positive Trends", s["positive_trends"], COLORS.SUCCESS), unsafe_allow_html=True)
    with col2:
        st.markdown(_summary_list("Top Risks", s["top_risks"], COLORS.ERROR), unsafe_allow_html=True)
        spacer(1)
        st.markdown(_summary_list("Critical Issues", s["critical_issues"], COLORS.WARNING), unsafe_allow_html=True)

    # Release recommendation
    rec_color = COLORS.SUCCESS if s["release_recommendation"] == "GO" else COLORS.WARNING if "RISKS" in s["release_recommendation"] else COLORS.ERROR
    rec_rgb = _hex_to_rgb(rec_color)
    st.markdown(f"""<div style="padding:{SPACING.SPACE_4};background:rgba({rec_rgb},0.1);border:1px solid rgba({rec_rgb},0.3);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_3};"> <div style="display:flex;justify-content:space-between;align-items:center;"> <div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">Release Recommendation</div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_LG};font-weight:700;color:{rec_color};margin-top:4px;">{_escape(s["release_recommendation"])}</div> </div> <div style="text-align:right;"> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">AI Confidence</div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XL};font-weight:700;color:{conf_color};">{s["confidence"]}%</div> </div> </div> </div>""", unsafe_allow_html=True)

    st.markdown("#### Recommended Actions")
    for action in s["recommended_actions"]:
        st.markdown(
            f'<div style="padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);'
            f'border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {COLORS.SUCCESS};">'
            f'<span style="color:{COLORS.SUCCESS};">✅</span> '
            f'<span style="color:{COLORS.TEXT_PRIMARY};">{_escape(action)}</span></div>',
            unsafe_allow_html=True,
        )


def _summary_list(title: str, items: list[str], color: str) -> str:
    """Return HTML for a titled bullet list."""
    items_html = "".join(
        f'<li style="color:{COLORS.TEXT_PRIMARY};margin-bottom:{SPACING.SPACE_1};">{_escape(item)}</li>'
        for item in items
    )
    return (
        f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);'
        f'border-radius:{BORDERS.RADIUS_MD};border-left:3px solid {color};">'
        f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;margin-bottom:{SPACING.SPACE_2};">{title}</div>'
        f'<ul style="margin:0;padding-left:{SPACING.SPACE_4};">{items_html}</ul></div>'
    )


def quality_score_center() -> None:
    """Render the premium quality score visualization center."""
    section_header("Quality Score Center", icon="🎯")

    col_gauge, col_scores = st.columns([1, 2])
    with col_gauge:
        overall = next((q for q in QUALITY_SCORES if q["dimension"] == "Overall Quality"), QUALITY_SCORES[0])
        metric_gauge(overall["score"], 100, "Overall Quality", "%", _semantic(overall["color"]))
    with col_scores:
        cols = st.columns(3)
        for i, q in enumerate(QUALITY_SCORES):
            if q["dimension"] == "Overall Quality":
                continue
            with cols[(i - 1) % 3]:
                c = _semantic(q["color"])
                c_rgb = _hex_to_rgb(c)
                target_met = "✓" if q["score"] >= q["target"] else "⚠"
                st.markdown(f"""<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {c};"> <div style="display:flex;justify-content:space-between;align-items:center;"> <span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;">{_escape(q["dimension"])}</span> <span style="color:{c};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{target_met}</span> </div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XL};font-weight:700;color:{c};margin-top:4px;">{q["score"]}<span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">/{q["target"]}</span></div> <div style="height:6px;background:rgba({COLORS.BORDER_RGB},0.4);border-radius:3px;margin-top:6px;overflow:hidden;"><div style="width:{q["score"]}%;height:100%;background:{c};border-radius:3px;"></div></div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};margin-top:4px;">Target {q["target"]} • {_escape(q["trend"])}</div> </div>""", unsafe_allow_html=True)


def quality_trend_center(key_prefix: str = "reports_trend") -> None:
    """Render the premium quality trend analytics with view selector."""
    section_header("Quality Trend Center", icon="📈")

    view = st.radio("View", options=list(TREND_VIEWS.keys()), horizontal=True,
                    key=f"{key_prefix}_radio", label_visibility="collapsed")
    st.session_state.reports_trend_view = view
    data = TREND_VIEWS[view]

    metrics = [
        ("Quality Score", "quality", COLORS.PRIMARY),
        ("Pass Rate", "pass_rate", COLORS.SUCCESS),
        ("Failure Rate", "failure_rate", COLORS.ERROR),
        ("Automation Coverage", "coverage", COLORS.SECONDARY),
        ("Flaky Rate", "flaky_rate", COLORS.WARNING),
        ("Defect Rate", "defect_rate", COLORS.ACCENT),
        ("AI Confidence", "ai_confidence", COLORS.INFO),
    ]

    selected = st.selectbox("Compare metrics", options=[m[0] for m in metrics],
                            index=0, key=f"{key_prefix}_metric")
    sel_key = next(m[1] for m in metrics if m[0] == selected)
    sel_color = next(m[2] for m in metrics if m[0] == selected)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[d["date"] for d in data], y=[d[sel_key] for d in data],
        mode="lines+markers", name=selected,
        line=dict(color=sel_color, width=3),
        marker=dict(size=8, color=sel_color, line=dict(color=COLORS.TEXT_PRIMARY, width=2)),
        fill="tonexty", fillcolor=f"rgba({_hex_to_rgb(sel_color)}, 0.1)",
    ))
    _apply_chart_theme(fig, height=320)
    st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_chart_{view}_{sel_key}")

    # Multi-metric comparison
    st.markdown("#### Multi-Metric Comparison")
    fig2 = go.Figure()
    for label, key, color in metrics:
        fig2.add_trace(go.Scatter(
            x=[d["date"] for d in data], y=[d[key] for d in data],
            mode="lines+markers", name=label,
            line=dict(color=color, width=2), marker=dict(size=5),
        ))
    _apply_chart_theme(fig2, height=300, show_legend=True)
    st.plotly_chart(fig2, use_container_width=True, key=f"{key_prefix}_multi_{view}")


def coverage_intelligence(key_prefix: str = "reports") -> None:
    """Render coverage intelligence by area with gap visualization."""
    section_header("Coverage Intelligence", icon="🧪")

    for item in COVERAGE_INTELLIGENCE:
        c = _semantic(item["color"])
        with st.expander(f"{_escape(item['area'])} — {item['covered']}% covered ({_escape(item['risk'])} risk)", key=f"{key_prefix}_cov_exp_{item['area']}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SUCCESS_RGB},0.1);border-radius:{BORDERS.RADIUS_MD};text-align:center;"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XL};font-weight:700;color:{COLORS.SUCCESS};">{item["covered"]}%</div><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Covered</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.WARNING_RGB},0.1);border-radius:{BORDERS.RADIUS_MD};text-align:center;"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XL};font-weight:700;color:{COLORS.WARNING};">{item["partial"]}%</div><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Partial</div></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.ERROR_RGB},0.1);border-radius:{BORDERS.RADIUS_MD};text-align:center;"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XL};font-weight:700;color:{COLORS.ERROR};">{item["missing"]}%</div><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Missing</div></div>', unsafe_allow_html=True)
            st.markdown(
                f'<div style="display:flex;gap:{SPACING.SPACE_4};margin-top:{SPACING.SPACE_2};">'
                f'<span style="color:{COLORS.TEXT_SECONDARY};">Risk: <span style="color:{c};font-weight:600;">{_escape(item["risk"])}</span></span>'
                f'<span style="color:{COLORS.TEXT_SECONDARY};">Trend: <span style="color:{COLORS.SUCCESS};">{_escape(item["trend"])}</span></span></div>',
                unsafe_allow_html=True,
            )
            st.markdown(f"**AI Recommendation:** {_escape(item['recommendation'])}")

    # Gap visualization
    st.markdown("#### Coverage Gap Visualization")
    fig = go.Figure()
    areas = [c["area"] for c in COVERAGE_INTELLIGENCE]
    fig.add_trace(go.Bar(name="Covered", x=areas, y=[c["covered"] for c in COVERAGE_INTELLIGENCE], marker_color=COLORS.SUCCESS))
    fig.add_trace(go.Bar(name="Partial", x=areas, y=[c["partial"] for c in COVERAGE_INTELLIGENCE], marker_color=COLORS.WARNING))
    fig.add_trace(go.Bar(name="Missing", x=areas, y=[c["missing"] for c in COVERAGE_INTELLIGENCE], marker_color=COLORS.ERROR))
    fig.update_layout(barmode="stack")
    _apply_chart_theme(fig, height=320, show_legend=True)
    st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_coverage_gap_viz")


def business_flow_quality() -> None:
    """Render business flow quality with selectable inspector."""
    section_header("Business Flow Quality", icon="🔀")

    flow_ids = [f["id"] for f in BUSINESS_FLOW_QUALITY]
    selected_id = st.session_state.get("reports_selected_flow", flow_ids[0])
    selected = next((f for f in BUSINESS_FLOW_QUALITY if f["id"] == selected_id), BUSINESS_FLOW_QUALITY[0])

    col_list, col_detail = st.columns([2, 1])
    with col_list:
        for flow in BUSINESS_FLOW_QUALITY:
            risk_c = _risk_color(flow["risk"])
            cov_c = _coverage_color(flow["coverage"])
            is_sel = flow["id"] == selected_id
            bg = f"rgba({COLORS.PRIMARY_RGB},0.22)" if is_sel else f"rgba({COLORS.SURFACE_RGB},0.5)"
            border_w = "2px" if is_sel else "1px"
            st.markdown(f"""<div style="padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:{bg};border-left:{border_w} solid {risk_c};border-radius:0 {BORDERS.RADIUS_MD} {BORDERS.RADIUS_MD} 0;margin-bottom:{SPACING.SPACE_1};"> <div style="display:flex;justify-content:space-between;align-items:center;"> <span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;">{flow["icon"]} {_escape(flow["name"])}</span> <div style="display:flex;gap:{SPACING.SPACE_2};"> <span style="color:{cov_c};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{flow["coverage"]}%</span> <span style="color:{risk_c};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{_escape(flow["risk"]).upper()}</span> </div> </div> </div>""", unsafe_allow_html=True)
            if st.button("Select", key=f"flow_sel_{flow['id']}", use_container_width=True, help=f"Inspect {flow['name']}"):
                st.session_state.reports_selected_flow = flow["id"]
                st.rerun()
    with col_detail:
        risk_c = _risk_color(selected["risk"])
        cov_c = _coverage_color(selected["coverage"])
        st.markdown(f"""<div style="padding:{SPACING.SPACE_4};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_LG};border:1px solid rgba({_hex_to_rgb(risk_c)},0.3);"> <div style="display:flex;align-items:center;gap:{SPACING.SPACE_2};margin-bottom:{SPACING.SPACE_3};"> <span style="font-size:24px;">{selected["icon"]}</span> <span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_LG};font-weight:600;">{_escape(selected["name"])}</span> </div> <div style="display:grid;grid-template-columns:1fr 1fr;gap:{SPACING.SPACE_2};"> <div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_MD};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Coverage</div><div style="color:{cov_c};font-weight:700;">{selected["coverage"]}%</div></div> <div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_MD};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Pass Rate</div><div style="color:{COLORS.SUCCESS};font-weight:700;">{selected["pass_rate"]}%</div></div> <div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_MD};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Failures</div><div style="color:{COLORS.ERROR};font-weight:700;">{selected["failures"]}</div></div> <div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_MD};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Risk</div><div style="color:{risk_c};font-weight:700;">{_escape(selected["risk"]).upper()}</div></div> <div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_MD};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Impact</div><div style="color:{COLORS.TEXT_PRIMARY};font-weight:700;">{_escape(selected["impact"])}</div></div> <div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_MD};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">AI Confidence</div><div style="color:{COLORS.PRIMARY};font-weight:700;">{selected["confidence"]}%</div></div> </div> <div style="margin-top:{SPACING.SPACE_2};font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Automation: {selected["automation"]}% • Last run: {_escape(selected["last_execution"])}</div> </div>""", unsafe_allow_html=True)


def bug_intelligence(key_prefix: str = "reports") -> None:
    """Render premium bug analytics."""
    section_header("Bug Intelligence", icon="🐛")
    s = BUG_INTELLIGENCE["summary"]

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        metric_card("Total Bugs", s["total"], "This month", "-15%", "🐛")
    with col2:
        metric_card("Critical", s["critical"], "Zero escaped", "-100%", "🔴")
    with col3:
        metric_card("High", s["high"], "Open", "-50%", "🟠")
    with col4:
        metric_card("New", s["new"], "This week", "", "➕")
    with col5:
        metric_card("Regression", s["regression"], "Watch", "", "🔄")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Severity Distribution")
        fig = go.Figure(go.Pie(
            labels=[d["severity"] for d in BUG_INTELLIGENCE["severity_distribution"]],
            values=[d["count"] for d in BUG_INTELLIGENCE["severity_distribution"]],
            hole=0.4,
            marker=dict(colors=[_semantic(d["color"]) for d in BUG_INTELLIGENCE["severity_distribution"]]),
            textfont=dict(color=COLORS.TEXT_PRIMARY),
        ))
        _apply_chart_theme(fig, height=280)
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_bug_severity")
    with col2:
        st.markdown("#### Bug Trend")
        fig = go.Figure(go.Scatter(
            x=[t["date"] for t in BUG_INTELLIGENCE["trend"]],
            y=[t["bugs"] for t in BUG_INTELLIGENCE["trend"]],
            mode="lines+markers", line=dict(color=COLORS.ERROR, width=3),
            marker=dict(size=8, color=COLORS.ERROR),
        ))
        _apply_chart_theme(fig, height=280)
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_bug_trend")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Module Distribution")
        fig = go.Figure(go.Bar(
            x=[m["module"] for m in BUG_INTELLIGENCE["by_module"]],
            y=[m["count"] for m in BUG_INTELLIGENCE["by_module"]],
            marker_color=[_semantic(m["color"]) for m in BUG_INTELLIGENCE["by_module"]],
            text=[m["count"] for m in BUG_INTELLIGENCE["by_module"]], textposition="outside",
        ))
        _apply_chart_theme(fig, height=280)
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_bug_module")
    with col2:
        st.markdown("#### Root Causes")
        fig = go.Figure(go.Bar(
            x=[r["cause"] for r in BUG_INTELLIGENCE["root_causes"]],
            y=[r["count"] for r in BUG_INTELLIGENCE["root_causes"]],
            marker_color=[_semantic(r["color"]) for r in BUG_INTELLIGENCE["root_causes"]],
            text=[r["count"] for r in BUG_INTELLIGENCE["root_causes"]], textposition="outside",
        ))
        _apply_chart_theme(fig, height=280)
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_bug_rootcause")

    st.markdown("#### Top Recurring Defects")
    for bug in BUG_INTELLIGENCE["top_recurring"]:
        c = _severity_color(bug["severity"])
        st.markdown(
            f'<div style="padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);'
            f'border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {c};">'
            f'<div style="display:flex;justify-content:space-between;">'
            f'<span style="color:{COLORS.TEXT_PRIMARY};font-family:{TYPOGRAPHY.FONT_MONO};">{_escape(bug["name"])}</span>'
            f'<div><span style="color:{c};font-size:{TYPOGRAPHY.FONT_SIZE_XS};font-weight:600;">{_escape(bug["severity"]).upper()}</span>'
            f' <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">×{bug["occurrences"]}</span></div></div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("#### 🧠 AI Root-Cause Summary")
    st.info(BUG_INTELLIGENCE["ai_summary"])


def execution_intelligence(key_prefix: str = "reports") -> None:
    """Render execution intelligence."""
    section_header("Execution Intelligence", icon="⚡")
    s = EXECUTION_INTELLIGENCE["summary"]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Executions", s["total"], "Last 30 days", "", "⚡")
    with col2:
        metric_card("Passed", s["passed"], f"{s['passed']/s['total']*100:.1f}%", "", "✅")
    with col3:
        metric_card("Failed", s["failed"], f"{s['failed']/s['total']*100:.1f}%", "", "❌")
    with col4:
        metric_card("Retries", s["retries"], "Auto-retried", "", "🔄")

    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Avg Duration", s["avg_duration"], "Per suite", "-8m", "⏱️")
    with col2:
        metric_card("P95 Duration", s["p95_duration"], "Tail latency", "", "📈")
    with col3:
        metric_card("Parallelization", s["parallelization"], "Parallel workers", "", "🔀")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Execution Trend")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[t["date"] for t in EXECUTION_INTELLIGENCE["trend"]], y=[t["executions"] for t in EXECUTION_INTELLIGENCE["trend"]], mode="lines+markers", name="Executions", line=dict(color=COLORS.PRIMARY, width=2)))
        fig.add_trace(go.Scatter(x=[t["date"] for t in EXECUTION_INTELLIGENCE["trend"]], y=[t["passed"] for t in EXECUTION_INTELLIGENCE["trend"]], mode="lines+markers", name="Passed", line=dict(color=COLORS.SUCCESS, width=2)))
        _apply_chart_theme(fig, height=280, show_legend=True)
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_exec_trend")
    with col2:
        st.markdown("#### Browser Distribution")
        fig = go.Figure(go.Pie(
            labels=[b["browser"] for b in EXECUTION_INTELLIGENCE["browser_distribution"]],
            values=[b["count"] for b in EXECUTION_INTELLIGENCE["browser_distribution"]],
            hole=0.4,
            marker=dict(colors=[_semantic(b["color"]) for b in EXECUTION_INTELLIGENCE["browser_distribution"]]),
            textfont=dict(color=COLORS.TEXT_PRIMARY),
        ))
        _apply_chart_theme(fig, height=280)
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_exec_browser")

    st.markdown("#### Environment Distribution")
    env_data = {e["env"]: e["count"] for e in EXECUTION_INTELLIGENCE["env_distribution"]}
    pie_chart(env_data, f"{key_prefix}_Environments")


def ai_performance_intelligence(key_prefix: str = "reports") -> None:
    """Render AI performance intelligence."""
    section_header("AI Performance Intelligence", icon="🤖")
    s = AI_PERFORMANCE_INTEL["summary"]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Agents", s["agents"], "12 active", "+2", "🤖")
    with col2:
        metric_card("Executions", f"{s['executions']:,}", "This month", "+23%", "✅")
    with col3:
        metric_card("Success Rate", f"{s['success_rate']}%", "Excellent", "", "📈")
    with col4:
        metric_card("Confidence", f"{s['confidence']}%", "High", "+3%", "🧠")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Model Usage")
        for model in AI_PERFORMANCE_INTEL["model_usage"]:
            c = _semantic(model["color"])
            c_rgb = _hex_to_rgb(c)
            st.markdown(f"""<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};"> <div style="display:flex;justify-content:space-between;margin-bottom:{SPACING.SPACE_1};"> <span style="color:{COLORS.TEXT_PRIMARY};font-weight:600;">{_escape(model["model"])}</span> <span style="color:{COLORS.TEXT_SECONDARY};">{model["requests"]:,} req</span> </div> <div style="width:100%;height:6px;background:rgba({COLORS.BORDER_RGB},0.4);border-radius:3px;overflow:hidden;"> <div style="width:{model["percentage"]}%;height:100%;background:{c};border-radius:3px;"></div> </div> </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("#### Tool Usage")
        fig = go.Figure(go.Bar(
            x=[t["tool"] for t in AI_PERFORMANCE_INTEL["tool_usage"]],
            y=[t["count"] for t in AI_PERFORMANCE_INTEL["tool_usage"]],
            marker_color=[_semantic(t["color"]) for t in AI_PERFORMANCE_INTEL["tool_usage"]],
            text=[t["count"] for t in AI_PERFORMANCE_INTEL["tool_usage"]], textposition="outside",
        ))
        _apply_chart_theme(fig, height=280)
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_ai_tools")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Top Performing Agents")
        for agent in AI_PERFORMANCE_INTEL["top_performers"]:
            c = _semantic(agent["color"])
            st.markdown(f"""<div style="padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {c};"> <div style="display:flex;justify-content:space-between;"> <span style="color:{COLORS.TEXT_PRIMARY};">{_escape(agent["agent"])}</span> <span style="color:{c};font-weight:600;">{agent["success"]}%</span> </div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">{agent["tasks"]} tasks</div> </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("#### Underperforming Agents")
        for agent in AI_PERFORMANCE_INTEL["underperformers"]:
            c = _semantic(agent["color"])
            st.markdown(f"""<div style="padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {c};"> <div style="display:flex;justify-content:space-between;"> <span style="color:{COLORS.TEXT_PRIMARY};">{_escape(agent["agent"])}</span> <span style="color:{c};font-weight:600;">{agent["success"]}%</span> </div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">{agent["tasks"]} tasks</div> </div>""", unsafe_allow_html=True)


def flaky_intelligence() -> None:
    """Render flaky test intelligence with categories."""
    section_header("Flaky Test Intelligence", icon="📳")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Flaky", "28", "Tests", "", "📳")
    with col2:
        metric_card("Flaky Rate", "2.3%", "Target <2%", "-0.5%", "📊")
    with col3:
        metric_card("Fixed", "5", "This week", "+3", "✅")
    with col4:
        metric_card("Pending", "23", "Awaiting fix", "-2", "⏳")

    st.markdown("---")
    st.markdown("#### Flaky Categories & AI Recommendations")
    for cat in FLAKY_CATEGORIES:
        c = _semantic(cat["color"])
        st.markdown(f"""<div style="padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {c};"> <div style="display:flex;justify-content:space-between;align-items:center;"> <span style="color:{COLORS.TEXT_PRIMARY};font-weight:500;">{_escape(cat["category"])}</span> <span style="color:{c};font-weight:600;">{cat["count"]} tests</span> </div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_SECONDARY};margin-top:4px;">🧠 {_escape(cat["recommendation"])}</div> </div>""", unsafe_allow_html=True)


def release_readiness_panel() -> None:
    """Render premium release readiness panel."""
    section_header("Release Readiness", icon="🚀")
    r = RELEASE_READINESS
    status_color = COLORS.SUCCESS if r["status"] == "GO" else COLORS.WARNING if "RISKS" in r["status"] else COLORS.ERROR
    status_rgb = _hex_to_rgb(status_color)

    col_score, col_gates = st.columns([1, 2])
    with col_score:
        metric_gauge(r["score"], 100, "Release Score", "%", get_health_color(r["score"]))
        st.markdown(f"""<div style="text-align:center;padding:{SPACING.SPACE_3};background:rgba({status_rgb},0.1);border:1px solid rgba({status_rgb},0.3);border-radius:{BORDERS.RADIUS_MD};margin-top:{SPACING.SPACE_2};"> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">Status</div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_LG};font-weight:700;color:{status_color};">{_escape(r["status"])}</div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};margin-top:4px;">Risk: {_escape(r["risk_level"])} • AI {r["ai_confidence"]}%</div> </div>""", unsafe_allow_html=True)
    with col_gates:
        st.markdown("#### Quality Gates")
        cols = st.columns(4)
        for i, gate in enumerate(r["gates"]):
            with cols[i % 4]:
                c = _semantic(gate["color"])
                icon = "✓" if gate["status"] == "pass" else "⚠"
                st.markdown(f"""<div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {c};text-align:center;"> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_LG};color:{c};">{icon}</div> <div style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_XS};font-weight:500;">{_escape(gate["name"])}</div> <div style="color:{c};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;">{gate["score"]}</div> <div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">≥ {gate["threshold"]}</div> </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Readiness Breakdown")
    cols = st.columns(len(r["readiness_breakdown"]))
    for col, item in zip(cols, r["readiness_breakdown"]):
        c = _semantic(item["color"])
        with col:
            st.markdown(f"""<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};text-align:center;"> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XL};font-weight:700;color:{c};">{item["score"]}%</div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">{_escape(item["label"])}</div> <div style="height:6px;background:rgba({COLORS.BORDER_RGB},0.4);border-radius:3px;margin-top:6px;overflow:hidden;"><div style="width:{item["score"]}%;height:100%;background:{c};border-radius:3px;"></div></div> </div>""", unsafe_allow_html=True)


def quality_gates_matrix() -> None:
    """Render enterprise quality gate matrix."""
    section_header("Quality Gates Matrix", icon="🚦")
    cols = st.columns(4)
    for i, gate in enumerate(QUALITY_GATES):
        with cols[i % 4]:
            c = _semantic(gate["color"])
            icon = "✅" if gate["status"] == "pass" else "⚠️"
            st.markdown(f"""<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {c};"> <div style="display:flex;justify-content:space-between;align-items:center;"> <span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;">{icon} {_escape(gate["gate"])}</span> </div> <div style="display:flex;justify-content:space-between;margin-top:{SPACING.SPACE_1};"> <span style="color:{c};font-weight:700;">{gate["score"]}</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">≥ {gate["threshold"]}</span> </div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};margin-top:4px;">👤 {_escape(gate["owner"])} • {_escape(gate["last_run"])}</div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_SECONDARY};margin-top:2px;">🧠 {_escape(gate["recommendation"])}</div> </div>""", unsafe_allow_html=True)


def quality_risk_matrix_panel(key_prefix: str = "reports") -> None:
    """Render quality risk matrix panel."""
    section_header("Quality Risk Matrix", icon="⚠️")
    for risk in QUALITY_RISK_MATRIX:
        c = _semantic(risk["color"])
        with st.expander(f"⚠️ {_escape(risk['risk'])} — {_escape(risk['severity']).upper()} ({risk['probability']}% prob)", key=f"{key_prefix}_risk_exp_{risk['risk']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Severity:** <span style='color:{c};font-weight:600;'>{_escape(risk['severity']).upper()}</span>", unsafe_allow_html=True)
                st.markdown(f"**Probability:** {risk['probability']}%")
                st.markdown(f"**Impact:** {_escape(risk['impact'])}")
            with col2:
                st.markdown(f"**Owner:** {_escape(risk['owner'])}")
                st.markdown(f"**Status:** {_escape(risk['status'])}")
                st.markdown(f"**AI Recommendation:** {_escape(risk['recommendation'])}")


def ai_recommendations_panel() -> None:
    """Render AI recommendations panel."""
    section_header("AI Recommendations", icon="💡")
    for rec in AI_RECOMMENDATIONS:
        c = _semantic(rec["color"])
        c_rgb = _hex_to_rgb(c)
        st.markdown(f"""<div style="padding:{SPACING.SPACE_4};background:rgba({COLORS.SURFACE_RGB},0.6);border-left:3px solid {c};border-radius:0 {BORDERS.RADIUS_MD} {BORDERS.RADIUS_MD} 0;margin-bottom:{SPACING.SPACE_3};"> <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:{SPACING.SPACE_2};"> <span style="padding:2px 8px;background:rgba({c_rgb},0.2);color:{c};border-radius:{BORDERS.RADIUS_SM};font-size:{TYPOGRAPHY.FONT_SIZE_XS};font-weight:600;text-transform:uppercase;">{_escape(rec["priority"])}</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">AI confidence: {rec["confidence"]}%</span> </div> <div style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_BASE};margin-bottom:{SPACING.SPACE_1};"><strong>Finding:</strong> {_escape(rec["finding"])}</div> <div style="color:{COLORS.TEXT_SECONDARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};margin-bottom:{SPACING.SPACE_1};"><strong>Recommendation:</strong> {_escape(rec["recommendation"])}</div> <div style="color:{COLORS.SUCCESS};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">Expected improvement: {_escape(rec["expected"])}</div> </div>""", unsafe_allow_html=True)


def report_library_panel(key_prefix: str = "reports") -> None:
    """Render premium report library."""
    section_header("Report Library", icon="📚")
    categories = ["All", "Executive", "QA", "Automation", "API", "Performance", "Security", "Accessibility", "Release"]
    selected_cat = st.selectbox("Filter by category", options=categories, key=f"{key_prefix}_lib_cat")
    filtered = REPORT_LIBRARY if selected_cat == "All" else [r for r in REPORT_LIBRARY if r["category"] == selected_cat]

    cols = st.columns(3)
    for i, report in enumerate(filtered):
        with cols[i % 3]:
            c = _semantic(report["color"])
            c_rgb = _hex_to_rgb(c)
            status_c = COLORS.SUCCESS if report["status"] == "generated" else COLORS.WARNING
            st.markdown(f"""<div style="padding:{SPACING.SPACE_4};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_LG};margin-bottom:{SPACING.SPACE_3};border:1px solid rgba({c_rgb},0.3);"> <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:{SPACING.SPACE_2};"> <span style="color:{c};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;">{_escape(report["category"])}</span> <span style="padding:2px 8px;background:rgba({_hex_to_rgb(status_c)},0.2);color:{status_c};border-radius:{BORDERS.RADIUS_SM};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{_escape(report["status"]).upper()}</span> </div> <div style="color:{COLORS.TEXT_PRIMARY};font-weight:600;margin-bottom:{SPACING.SPACE_1};">{_escape(report["name"])}</div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};margin-bottom:{SPACING.SPACE_2};">👤 {_escape(report["author"])} • {_escape(report["created"])}</div> <div style="display:flex;gap:{SPACING.SPACE_3};font-size:{TYPOGRAPHY.FONT_SIZE_XS};"> <span style="color:{COLORS.TEXT_SECONDARY};">📊 Coverage: {report["coverage"]}%</span> <span style="color:{COLORS.TEXT_SECONDARY};">✅ Quality: {report["quality"]}</span> </div> </div>""", unsafe_allow_html=True)
            bcol1, bcol2 = st.columns(2)
            with bcol1:
                if st.button("View", key=f"{key_prefix}_lib_view_{report['name']}", use_container_width=True):
                    st.toast(f"Viewing {report['name']}", icon="📄")
            with bcol2:
                if st.button("Export", key=f"{key_prefix}_lib_export_{report['name']}", use_container_width=True):
                    st.toast(f"Exporting {report['name']}", icon="📤")


def report_generator_panel(key_prefix: str = "reports") -> None:
    """Render premium report generation panel."""
    section_header("Report Generator", icon="📝")
    col1, col2 = st.columns(2)
    with col1:
        report_type = st.selectbox("Report Type", options=[
            "Executive Report", "Regression Report", "Automation Report",
            "API Report", "Security Report", "Performance Report",
            "Accessibility Report", "Release Report",
        ], key=f"{key_prefix}_gen_type")
        date_range = st.selectbox("Date Range", options=[
            "Last 7 days", "Last 14 days", "Last 30 days", "Last 90 days", "Custom",
        ], key=f"{key_prefix}_gen_range")
        environment = st.selectbox("Environment", options=["Production", "Staging", "Development"], key=f"{key_prefix}_gen_env")
    with col2:
        mission = st.selectbox("Mission", options=["E2E Regression v2.1", "Smoke Test", "Full Regression"], key=f"{key_prefix}_gen_mission")
        application = st.selectbox("Application", options=["E-Commerce Platform", "Admin Portal", "API Gateway"], key=f"{key_prefix}_gen_app")
        st.markdown("**Options:**")
        inc_screenshots = st.checkbox("Include Screenshots", value=True, key=f"{key_prefix}_gen_ss")
        inc_logs = st.checkbox("Include Logs", value=True, key=f"{key_prefix}_gen_logs")
        inc_ai = st.checkbox("Include AI Summary", value=True, key=f"{key_prefix}_gen_ai")
        inc_recs = st.checkbox("Include Recommendations", value=True, key=f"{key_prefix}_gen_recs")
    if st.button("🚀 Generate Report", use_container_width=True, type="primary", key=f"{key_prefix}_gen_btn"):
        st.toast(f"Generating {report_type} for {application}", icon="🚀")
        st.success(f"Report generation started: {report_type} ({date_range}, {environment})")


def export_center(key_prefix: str = "reports") -> None:
    """Render export center with multiple formats."""
    section_header("Export Center", icon="📤")
    formats = [
        ("PDF", "📄", "Portable document format"),
        ("HTML", "🌐", "Web-viewable report"),
        ("CSV", "📊", "Spreadsheet data export"),
        ("JSON", "📋", "Machine-readable export"),
        ("Excel", "📗", "Microsoft Excel workbook"),
        ("Markdown", "📝", "Lightweight markup export"),
    ]
    cols = st.columns(3)
    for i, (fmt, icon, desc) in enumerate(formats):
        with cols[i % 3]:
            if st.button(f"{icon} {fmt}", key=f"{key_prefix}_export_center_{fmt}", use_container_width=True, help=desc):
                st.toast(f"Exporting as {fmt}...", icon=icon)
                st.success(f"Mock export: {fmt} prepared ({desc})")


def release_comparison_panel() -> None:
    """Render release comparison panel."""
    section_header("Release Comparison", icon="⚖️")
    rc = RELEASE_COMPARISON
    st.markdown(
        f'<div style="display:flex;justify-content:space-between;padding:{SPACING.SPACE_3};'
        f'background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_4};">'
        f'<div><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Current</div>'
        f'<div style="color:{COLORS.SUCCESS};font-weight:600;">{_escape(rc["current"])}</div></div>'
        f'<div style="text-align:right;"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Previous</div>'
        f'<div style="color:{COLORS.TEXT_SECONDARY};font-weight:600;">{_escape(rc["previous"])}</div></div></div>',
        unsafe_allow_html=True,
    )
    for m in rc["metrics"]:
        diff = m["current"] - m["previous"]
        if m["unit"] == "%":
            improved = diff > 0
            # For failure/bug/flaky metrics, lower is better — but here all are "improved" per mock
            status = "improved" if (diff > 0) else ("regressed" if diff < 0 else "unchanged")
        else:
            improved = diff < 0  # fewer bugs/failures is better
            status = "improved" if improved else ("regressed" if diff > 0 else "unchanged")
        status_color = COLORS.SUCCESS if status == "improved" else COLORS.ERROR if status == "regressed" else COLORS.TEXT_MUTED
        arrow = "↑" if diff > 0 else "↓" if diff < 0 else "→"
        diff_disp = round(abs(diff), 2)
        st.markdown(f"""<div style="display:flex;justify-content:space-between;align-items:center;padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {status_color};"> <span style="color:{COLORS.TEXT_PRIMARY};font-weight:500;">{_escape(m["metric"])}</span> <div style="display:flex;gap:{SPACING.SPACE_4};align-items:center;"> <span style="color:{COLORS.TEXT_SECONDARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{m["previous"]}{m["unit"]}</span> <span style="color:{COLORS.TEXT_MUTED};">→</span> <span style="color:{COLORS.TEXT_PRIMARY};font-weight:700;">{m["current"]}{m["unit"]}</span> <span style="color:{status_color};font-weight:600;font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{arrow} {diff_disp}{m["unit"]}</span> </div> </div>""", unsafe_allow_html=True)


def reports_quick_actions() -> None:
    """Render premium quick actions as glass buttons."""
    section_header("Quick Actions", icon="⚡")
    for i in range(0, len(REPORTS_QUICK_ACTIONS), 4):
        row = REPORTS_QUICK_ACTIONS[i:i + 4]
        cols = st.columns(len(row))
        for col, action in zip(cols, row):
            with col:
                if st.button(
                    f"{action['icon']} {action['name']}",
                    key=f"reports_qa_{i}_{action['name']}",
                    use_container_width=True, help=action["description"],
                ):
                    st.toast(action["description"], icon=action["icon"])


def reports_timeline() -> None:
    """Render quality timeline."""
    section_header("Quality Timeline", icon="📅")
    for i, step in enumerate(QUALITY_TIMELINE):
        c = _semantic(step["color"])
        is_last = i == len(QUALITY_TIMELINE) - 1
        st.markdown(
            f'<div style="display:flex;gap:{SPACING.SPACE_3};margin-bottom:{0 if is_last else SPACING.SPACE_3};">'
            f'<div style="display:flex;flex-direction:column;align-items:center;">'
            f'<div style="width:32px;height:32px;border-radius:50%;background:rgba({_hex_to_rgb(c)},0.2);'
            f'display:flex;align-items:center;justify-content:center;font-size:16px;border:1px solid rgba({_hex_to_rgb(c)},0.4);'
            f'{"animation:" + ANIMATIONS.PULSE + ";" if i == 0 else ""}">{step["icon"]}</div>'
            + ("" if is_last else f'<div style="width:2px;flex:1;background:linear-gradient(180deg,{c},{COLORS.BORDER});min-height:20px;"></div>')
            + f'</div>'
            f'<div><div style="display:flex;gap:{SPACING.SPACE_3};">'
            f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_PRIMARY};font-weight:500;">{_escape(step["step"])}</span>'
            f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">{_escape(step["time"])}</span></div>'
            f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_SECONDARY};">{_escape(step["detail"])}</div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )


def bottom_workspace_tabs() -> None:
    """Render the bottom executive workspace tabs (lazy)."""
    tabs = st.tabs(REPORTS_BOTTOM_TABS)
    tab_map = dict(zip(REPORTS_BOTTOM_TABS, tabs))
    with tab_map["Dashboard"]:
        _render_dashboard_tab()
    with tab_map["Trends"]:
        quality_trend_center(key_prefix="reports_bottom_trend")
    with tab_map["Coverage"]:
        coverage_intelligence(key_prefix="reports_bottom_cov")
    with tab_map["Quality"]:
        quality_score_center()
        spacer(1)
        quality_gates_matrix()
    with tab_map["Bugs"]:
        bug_intelligence(key_prefix="reports_bottom_bug")
    with tab_map["Executions"]:
        execution_intelligence(key_prefix="reports_bottom_exec")
    with tab_map["AI Performance"]:
        ai_performance_intelligence(key_prefix="reports_bottom_ai")
    with tab_map["Flaky Tests"]:
        flaky_intelligence()
    with tab_map["Release"]:
        release_readiness_panel()
        spacer(1)
        release_comparison_panel()
    with tab_map["Reports"]:
        report_library_panel(key_prefix="reports_bottom_lib")
        spacer(1)
        report_generator_panel(key_prefix="reports_bottom_gen")
        spacer(1)
        export_center(key_prefix="reports_bottom_export")


def _render_dashboard_tab() -> None:
    """Render the dashboard summary tab."""
    ai_executive_summary()
    spacer(1)
    col1, col2 = st.columns(2)
    with col1:
        reports_timeline()
    with col2:
        quality_risk_matrix_panel(key_prefix="reports_bottom_risk")
    spacer(1)
    ai_recommendations_panel()
