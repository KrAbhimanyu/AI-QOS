"""AI Reports & Analytics Center — Executive Quality Intelligence Center.

Premium enterprise workspace reusing the AI-QOS UI Foundation (design tokens
from themes/tokens.py and shared components from components/shared.py).
Business logic, session state, mock data, and all component signatures are
preserved — no breaking changes.
"""

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from utils.reports_data import (
    REPORTS_INFO,
    EXECUTIVE_REPORT,
    COVERAGE_REPORT,
    QUALITY_REPORT,
    AI_PERFORMANCE_REPORT,
    FLAKY_REPORT,
    RISK_REPORT,
    RECENT_REPORTS,
    SCHEDULED_REPORTS,
    REPORT_TEMPLATES,
    TREND_DATA,
)
from components.reports_components import (
    init_reports_state,
    metric_card,
    metric_gauge,
    report_card,
    coverage_chart,
    trend_chart,
    pie_chart,
    progress_bar_section,
    risk_matrix,
    report_generator,
    scheduled_reports_table,
    export_panel,
    ai_insights,
    comparison_chart,
    reports_hero_header,
    reports_kpi_strip,
    ai_executive_summary,
    quality_score_center,
    quality_trend_center,
    coverage_intelligence,
    business_flow_quality,
    bug_intelligence,
    execution_intelligence,
    ai_performance_intelligence,
    flaky_intelligence,
    release_readiness_panel,
    quality_gates_matrix,
    quality_risk_matrix_panel,
    ai_recommendations_panel,
    report_library_panel,
    report_generator_panel,
    export_center,
    release_comparison_panel,
    reports_quick_actions,
    reports_timeline,
    bottom_workspace_tabs,
    # token helpers reused in this view
    _hex_to_rgb,
    _escape,
    _coverage_color,
    _severity_color,
)
from components.shared import section_header, spacer

try:
    from frontend.themes.tokens import COLORS, SPACING, TYPOGRAPHY, BORDERS
except ImportError:  # pragma: no cover - fallback for direct execution
    from themes.tokens import COLORS, SPACING, TYPOGRAPHY, BORDERS


def render_header(info: dict[str, Any]) -> None:
    """Render the page header (preserved; delegates to premium hero)."""
    reports_hero_header(info)


def render_overview_tab() -> None:
    """Render overview tab (preserved) with token styling."""
    section_header("Key Metrics", icon="📈")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Tests", "1,247", "978 automated", "+12%", "🧪")
    with col2:
        metric_card("Coverage", "78.5%", "Target: 85%", "+5.2%", "📊")
    with col3:
        metric_card("Pass Rate", "94.2%", "Last 30 days", "+1.3%", "✅")
    with col4:
        metric_card("Flaky Rate", "2.3%", "Target: <2%", "-0.5%", "📳")

    spacer(1)
    col1, col2 = st.columns(2)
    with col1:
        trend_chart(TREND_DATA["coverage_trend"], "Coverage %", COLORS.SUCCESS)
    with col2:
        trend_chart(TREND_DATA["pass_rate_trend"], "Pass Rate %", COLORS.SECONDARY)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("AI Agents", "16", "12 active", "+2", "🤖")
    with col2:
        metric_card("Tasks Done", "4,587", "This month", "+23%", "✅")
    with col3:
        metric_card("Execution", "45m", "Avg time", "-8m", "⏱️")
    with col4:
        metric_card("Defects", "43", "This month", "-15%", "🐛")

    ai_insights([
        "Test coverage increased by 5.2% this month - on track to reach 85% target by Q4",
        "Flaky test rate dropped to 2.3% - best performance in 6 months",
        "AI agent efficiency improved by 18% with new model routing strategy",
        "Payment processing coverage gap identified - recommend focus area",
    ])


def render_coverage_tab() -> None:
    """Render test coverage tab (preserved) with token styling."""
    section_header("Test Coverage Analysis", icon="🧪")
    col1, col2 = st.columns([1, 2])
    with col1:
        metric_gauge(78.5, 100, "Overall Coverage", "%", COLORS.SUCCESS)
    with col2:
        coverage_chart(COVERAGE_REPORT["by_module"], "Coverage by Module")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        section_header("Coverage by Test Type", icon="🧪")
        for test_type, data in COVERAGE_REPORT["by_type"].items():
            test_name = test_type.replace("_", " ").title()
            coverage = data["coverage"]
            count = data["count"]
            color = _coverage_color(coverage)
            st.markdown(f"""
            <div style="margin-bottom:{SPACING.SPACE_4};">
                <div style="display:flex;justify-content:space-between;margin-bottom:{SPACING.SPACE_1};">
                    <span style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_PRIMARY};">{test_name} ({count})</span>
                    <span style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{color};font-weight:600;">{coverage}%</span>
                </div>
                <div style="width:100%;height:8px;background:rgba({COLORS.SURFACE_RGB},0.8);border-radius:4px;overflow:hidden;">
                    <div style="width:{coverage}%;height:100%;background:{color};border-radius:4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    with col2:
        section_header("Test Distribution", icon="📊")
        distribution = {
            "Unit Tests": 456, "Integration": 234, "E2E Tests": 123,
            "API Tests": 89, "Visual Tests": 67,
        }
        pie_chart(distribution, "Test Types")

    st.markdown("---")
    section_header("Coverage Gaps", icon="⚠️")
    for gap in COVERAGE_REPORT["gaps"]:
        color = {"high": COLORS.ERROR, "medium": COLORS.WARNING, "low": COLORS.INFO}.get(gap["priority"], COLORS.TEXT_MUTED)
        st.markdown(f"""
        <div style="padding:{SPACING.SPACE_4};background:rgba({COLORS.SURFACE_RGB},0.6);border-left:3px solid {color};border-radius:0 {BORDERS.RADIUS_MD} {BORDERS.RADIUS_MD} 0;margin-bottom:{SPACING.SPACE_3};">
            <div style="display:flex;justify-content:space-between;">
                <span style="font-size:{TYPOGRAPHY.FONT_SIZE_BASE};color:{COLORS.TEXT_PRIMARY};font-weight:600;">{_escape(gap['module'])}</span>
                <span style="padding:2px 8px;background:rgba({_hex_to_rgb(color)},0.2);color:{color};border-radius:{BORDERS.RADIUS_SM};font-size:{TYPOGRAPHY.FONT_SIZE_XS};font-weight:600;">{gap['priority'].upper()}</span>
            </div>
            <div style="margin-top:{SPACING.SPACE_2};">
                <span style="font-size:{TYPOGRAPHY.FONT_SIZE_2XL};font-weight:700;color:{COLORS.ERROR};">{gap['gap']}%</span>
                <span style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_SECONDARY};margin-left:{SPACING.SPACE_2};">coverage gap</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_quality_tab() -> None:
    """Render quality metrics tab (preserved) with token styling + go import fix."""
    section_header("Quality Metrics", icon="✅")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Code Quality", "87/100", "Grade: B+", "+2%", "📝")
    with col2:
        metric_card("Test Effectiveness", "92%", "Excellent", "+3%", "🎯")
    with col3:
        metric_card("Defect Density", "0.8", "Per 1K LOC", "-15%", "📉")
    with col4:
        metric_card("MTTD", "4.2h", "Mean Time to Detect", "-18%", "⏱️")

    st.markdown("---")
    section_header("Quality by Category", icon="📊")
    by_category = QUALITY_REPORT["by_category"]
    col1, col2 = st.columns(2)
    with col1:
        categories = [c["category"] for c in by_category]
        scores = [c["score"] for c in by_category]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=categories, y=scores,
            marker_color=[COLORS.SUCCESS if s >= 90 else COLORS.WARNING if s >= 75 else COLORS.ERROR for s in scores],
            text=scores, textposition="outside",
        ))
        fig.update_layout(
            height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=COLORS.TEXT_PRIMARY), showlegend=False, yaxis=dict(range=[0, 100]),
        )
        st.plotly_chart(fig, use_container_width=True, key="reports_quality_category_bar")
    with col2:
        section_header("Defect Distribution", icon="📉")
        for defect in QUALITY_REPORT["defect_distribution"]:
            color = _severity_color(defect["severity"])
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {color};">
                <span style="color:{color};font-weight:600;">{_escape(defect['severity'])}</span>
                <span style="color:{COLORS.TEXT_PRIMARY};font-weight:700;">{defect['count']}</span>
                <span style="color:{COLORS.SUCCESS};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{_escape(defect['trend'])}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    section_header("Quality Metrics Summary", icon="📋")
    metrics = QUALITY_REPORT["metrics"]
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Code Quality Score", f"{metrics['code_quality_score']}/100")
        st.metric("Test Effectiveness", f"{metrics['test_effectiveness']}%")
        st.metric("Defect Density", f"{metrics['defect_density']}/K LOC")
    with col2:
        st.metric("Mean Time to Detect", metrics['mean_time_to_detect'])
        st.metric("Mean Time to Resolve", metrics['mean_time_to_resolve'])
        st.metric("Escaped Defects", metrics['escaped_defects'])


def render_ai_performance_tab() -> None:
    """Render AI performance tab (preserved) with token styling + go import fix."""
    section_header("AI Agent Performance", icon="🤖")
    stats = AI_PERFORMANCE_REPORT["agent_stats"]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Agents", stats['total_agents'], "16 types", "", "🤖")
    with col2:
        metric_card("Active Now", stats['active_agents'], f"{stats['active_agents']/stats['total_agents']*100:.0f}%", "", "✅")
    with col3:
        metric_card("Uptime", stats['avg_uptime'], "Excellent", "", "📈")
    with col4:
        metric_card("Response Time", stats['avg_response_time'], "P95 latency", "", "⚡")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        section_header("Model Usage Distribution", icon="🧠")
        for model in AI_PERFORMANCE_REPORT["model_usage"]:
            color = COLORS.PRIMARY if model["model"] == "GPT-4" else COLORS.SECONDARY if model["model"] == "Claude" else COLORS.SUCCESS
            st.markdown(f"""
            <div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};">
                <div style="display:flex;justify-content:space-between;margin-bottom:{SPACING.SPACE_1};">
                    <span style="color:{COLORS.TEXT_PRIMARY};font-weight:600;">{_escape(model['model'])}</span>
                    <span style="color:{COLORS.TEXT_SECONDARY};">{model['requests']:,} requests</span>
                </div>
                <div style="width:100%;height:6px;background:rgba({COLORS.BORDER_RGB},0.4);border-radius:3px;overflow:hidden;">
                    <div style="width:{model['percentage']}%;height:100%;background:{color};border-radius:3px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    with col2:
        section_header("Token Usage", icon="🔢")
        token = AI_PERFORMANCE_REPORT["token_usage"]
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Total", token['total'])
        with col_b:
            st.metric("Input", token['input'])
        with col_c:
            st.metric("Output", token['output'])
        st.metric("Cost", token['cost'])

    st.markdown("---")
    section_header("Performance by Agent Type", icon="📊")
    by_type = AI_PERFORMANCE_REPORT["by_agent_type"]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[a["type"] for a in by_type], y=[a["tasks"] for a in by_type],
        marker_color=COLORS.PRIMARY, text=[a["tasks"] for a in by_type], textposition="outside",
    ))
    fig.update_layout(
        height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS.TEXT_PRIMARY), showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, key="reports_ai_perf_by_type")


def render_flaky_tests_tab() -> None:
    """Render flaky tests analysis tab (preserved) with token styling + go import fix."""
    section_header("Flaky Test Analysis", icon="📳")
    summary = FLAKY_REPORT["summary"]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Flaky", summary['total_flaky'], "Tests", "", "📳")
    with col2:
        metric_card("Flaky Rate", f"{summary['flaky_rate']}%", "Target: <2%", "", "📊")
    with col3:
        metric_card("Fixed", summary['fixed_this_week'], "This week", "+3", "✅")
    with col4:
        metric_card("Pending", summary['pending_fix'], "Awaiting fix", "-2", "⏳")

    st.markdown("---")
    section_header("Top Flaky Tests", icon="🔝")
    for test in FLAKY_REPORT["top_flaky_tests"]:
        rate_color = COLORS.ERROR if test["rate"] >= 10 else COLORS.WARNING
        st.markdown(f"""
        <div style="padding:{SPACING.SPACE_4};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_3};border-left:3px solid {rate_color};">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-size:{TYPOGRAPHY.FONT_SIZE_BASE};color:{COLORS.TEXT_PRIMARY};font-family:{TYPOGRAPHY.FONT_MONO};">{_escape(test['name'])}</div>
                    <div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_SECONDARY};margin-top:{SPACING.SPACE_1};">Reason: {_escape(test['reason'])}</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:{TYPOGRAPHY.FONT_SIZE_2XL};font-weight:700;color:{rate_color};">{test['rate']}%</div>
                    <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Fails: {test['fails']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        section_header("Root Causes", icon="🔍")
        causes = FLAKY_REPORT["root_causes"]
        fig = go.Figure(go.Pie(
            labels=[c["cause"] for c in causes], values=[c["count"] for c in causes], hole=0.4,
            marker=dict(colors=[COLORS.ERROR, COLORS.WARNING, COLORS.INFO, COLORS.SUCCESS, COLORS.PRIMARY]),
            textfont=dict(color=COLORS.TEXT_PRIMARY),
        ))
        fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True, key="reports_flaky_root_causes")
    with col2:
        section_header("By Module", icon="📦")
        for module in FLAKY_REPORT["by_module"]:
            color = {"critical": COLORS.ERROR, "high": COLORS.WARNING, "medium": COLORS.INFO, "low": COLORS.SUCCESS}.get(module["impact"], COLORS.TEXT_MUTED)
            st.markdown(f"""
            <div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {color};">
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:{COLORS.TEXT_PRIMARY};">{_escape(module['module'])}</span>
                    <span style="color:{color};font-weight:600;">{module['flaky_count']} tests ({module['rate']}%)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_reports_center() -> None:
    """Main page render function (preserved entry point)."""
    init_reports_state()

    # Sticky glass Hero Header
    render_header(REPORTS_INFO)

    # Executive KPI Strip (MetricCard grid)
    reports_kpi_strip()
    spacer(1)

    # Main Tabs — preserved tab structure with premium additive workspace
    tabs = st.tabs([
        "📈 Overview",
        "🧪 Coverage",
        "✅ Quality",
        "🤖 AI Performance",
        "📳 Flaky Tests",
        "📝 Reports",
        "🏢 Executive Workspace",
    ])

    with tabs[0]:
        render_overview_tab()
    with tabs[1]:
        render_coverage_tab()
    with tabs[2]:
        render_quality_tab()
    with tabs[3]:
        render_ai_performance_tab()
    with tabs[4]:
        render_flaky_tests_tab()
    with tabs[5]:
        section_header("Recent Reports", icon="📄")
        for report in RECENT_REPORTS:
            report_card(report)
        spacer(1)
        scheduled_reports_table(SCHEDULED_REPORTS)
        spacer(1)
        report_generator(REPORT_TEMPLATES)
        spacer(1)
        export_panel()
    with tabs[6]:
        # Premium Executive Quality Intelligence Center
        ai_executive_summary()
        spacer(1)

        # 3-column: Report Library | Quality Analytics | AI Executive Intelligence
        col_a, col_b, col_c = st.columns(3, gap="medium")
        with col_a:
            report_library_panel(key_prefix="reports_exec_lib")
        with col_b:
            quality_score_center()
        with col_c:
            ai_recommendations_panel()

        st.markdown("---")
        section_header("Quality Analytics", icon="📈")
        quality_trend_center(key_prefix="reports_exec_trend")

        st.markdown("---")
        # Coverage | Bugs | Executions | Flaky | AI Performance
        coverage_intelligence(key_prefix="reports_exec_cov")
        spacer(1)
        business_flow_quality()

        st.markdown("---")
        release_readiness_panel()
        spacer(1)
        quality_gates_matrix()
        spacer(1)
        quality_risk_matrix_panel(key_prefix="reports_exec_risk")
        spacer(1)
        release_comparison_panel()

        # Bottom executive workspace (glass tabs)
        st.markdown("---")
        section_header("Executive Workspace", icon="🏢")
        bottom_workspace_tabs()
        spacer(2)

        # Quick Actions
        reports_quick_actions()


def main() -> None:
    """Entry point."""
    render_reports_center()


if __name__ == "__main__":
    main()

