"""AI Reports & Analytics Center.

This page provides comprehensive reporting and analytics
for AI-powered quality engineering.
"""

from typing import Any
import streamlit as st

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
)


def render_header(info: dict[str, Any]) -> None:
    """Render the page header."""
    st.markdown("""
    <style>
    .reports-header {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95));
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="reports-header">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 8px;">
                    <span style="font-size: 48px;">📊</span>
                    <div>
                        <h1 style="margin: 0; font-size: 28px; color: #f8fafc;">
                            AI Reports & Analytics
                        </h1>
                        <p style="margin: 4px 0 0; font-size: 14px; color: #64748b;">
                            Enterprise Quality Intelligence • Data-Driven Decisions
                        </p>
                    </div>
                </div>
            </div>
            <div style="display: flex; gap: 12px;">
                <span style="
                    padding: 6px 14px;
                    background: rgba(99, 102, 241, 0.2);
                    border: 1px solid rgba(99, 102, 241, 0.3);
                    border-radius: 20px;
                    font-size: 12px;
                    color: #818cf8;
                ">
                    {info.get('total_reports', 0)} Reports
                </span>
                <span style="
                    padding: 6px 14px;
                    background: rgba(16, 185, 129, 0.2);
                    border: 1px solid rgba(16, 185, 129, 0.3);
                    border-radius: 20px;
                    font-size: 12px;
                    color: #10b981;
                ">
                    {info.get('dashboards', 0)} Dashboards
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("Total Reports", info.get('total_reports', 0))
    with col2:
        st.metric("Generated Today", info.get('generated_today', 0))
    with col3:
        st.metric("Scheduled", info.get('scheduled_reports', 0))
    with col4:
        st.metric("Metrics", info.get('total_metrics', 0))
    with col5:
        st.metric("Dashboards", info.get('dashboards', 0))
    with col6:
        st.metric("Report Types", info.get('report_types', 0))


def render_overview_tab() -> None:
    """Render overview tab."""
    
    # Key Metrics Row
    st.markdown("### 📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_card("Total Tests", "1,247", "978 automated", "+12%", "🧪")
    with col2:
        metric_card("Coverage", "78.5%", "Target: 85%", "+5.2%", "📊")
    with col3:
        metric_card("Pass Rate", "94.2%", "Last 30 days", "+1.3%", "✅")
    with col4:
        metric_card("Flaky Rate", "2.3%", "Target: <2%", "-0.5%", "📳")
    
    st.markdown("")
    
    # Trend Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Coverage Trend")
        trend_chart(TREND_DATA["coverage_trend"], "Coverage %", "#10b981")
    
    with col2:
        st.markdown("### 📈 Pass Rate Trend")
        trend_chart(TREND_DATA["pass_rate_trend"], "Pass Rate %", "#22d3ee")
    
    # More Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_card("AI Agents", "16", "12 active", "+2", "🤖")
    with col2:
        metric_card("Tasks Done", "4,587", "This month", "+23%", "✅")
    with col3:
        metric_card("Execution", "45m", "Avg time", "-8m", "⏱️")
    with col4:
        metric_card("Defects", "43", "This month", "-15%", "🐛")
    
    # AI Insights
    ai_insights([
        "Test coverage increased by 5.2% this month - on track to reach 85% target by Q4",
        "Flaky test rate dropped to 2.3% - best performance in 6 months",
        "AI agent efficiency improved by 18% with new model routing strategy",
        "Payment processing coverage gap identified - recommend focus area",
    ])


def render_coverage_tab() -> None:
    """Render test coverage tab."""
    
    st.markdown("### 🧪 Test Coverage Analysis")
    
    # Overall Coverage
    col1, col2 = st.columns([1, 2])
    
    with col1:
        metric_gauge(78.5, 100, "Overall Coverage", "%", "#10b981")
    
    with col2:
        coverage_chart(COVERAGE_REPORT["by_module"], "Coverage by Module")
    
    st.markdown("---")
    
    # Coverage by Type
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Coverage by Test Type")
        by_type = COVERAGE_REPORT["by_type"]
        
        for test_type, data in by_type.items():
            test_name = test_type.replace("_", " ").title()
            coverage = data["coverage"]
            count = data["count"]
            
            color = "#10b981" if coverage >= 80 else "#f59e0b" if coverage >= 60 else "#ef4444"
            
            st.markdown(f"""
            <div style="margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                    <span style="font-size: 13px; color: #f8fafc;">{test_name} ({count})</span>
                    <span style="font-size: 13px; color: {color};">{coverage}%</span>
                </div>
                <div style="width: 100%; height: 8px; background: rgba(30, 41, 59, 0.8); border-radius: 4px;">
                    <div style="width: {coverage}%; height: 100%; background: {color}; border-radius: 4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Test Distribution")
        distribution = {
            "Unit Tests": 456,
            "Integration": 234,
            "E2E Tests": 123,
            "API Tests": 89,
            "Visual Tests": 67,
        }
        pie_chart(distribution, "Test Types")
    
    st.markdown("---")
    
    # Coverage Gaps
    st.markdown("### ⚠️ Coverage Gaps")
    
    gaps = COVERAGE_REPORT["gaps"]
    for gap in gaps:
        priority_colors = {"high": "#ef4444", "medium": "#f59e0b", "low": "#3b82f6"}
        color = priority_colors.get(gap["priority"], "#64748b")
        
        st.markdown(f"""
        <div style="
            padding: 14px;
            background: rgba(30, 41, 59, 0.6);
            border-left: 3px solid {color};
            border-radius: 0 8px 8px 0;
            margin-bottom: 12px;
        ">
            <div style="display: flex; justify-content: space-between;">
                <span style="font-size: 14px; color: #f8fafc; font-weight: 600;">{gap['module']}</span>
                <span style="padding: 2px 8px; background: {color}20; color: {color}; border-radius: 4px; font-size: 11px;">{gap['priority'].upper()}</span>
            </div>
            <div style="margin-top: 8px;">
                <span style="font-size: 24px; font-weight: 700; color: #ef4444;">{gap['gap']}%</span>
                <span style="font-size: 13px; color: #94a3b8; margin-left: 8px;">coverage gap</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_quality_tab() -> None:
    """Render quality metrics tab."""
    
    st.markdown("### ✅ Quality Metrics")
    
    # Quality Scores
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
    
    # Quality by Category
    st.markdown("### 📊 Quality by Category")
    
    by_category = QUALITY_REPORT["by_category"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart
        categories = [c["category"] for c in by_category]
        scores = [c["score"] for c in by_category]
        trends = [c["trend"] for c in by_category]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=categories,
            y=scores,
            marker_color=["#10b981" if s >= 90 else "#f59e0b" if s >= 75 else "#ef4444" for s in scores],
            text=scores,
            textposition="outside",
        ))
        
        fig.update_layout(
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc"),
            showlegend=False,
            yaxis=dict(range=[0, 100]),
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Defect distribution
        st.markdown("#### Defect Distribution")
        defects = QUALITY_REPORT["defect_distribution"]
        
        for defect in defects:
            color = "#ef4444" if defect["severity"] == "Critical" else "#f59e0b" if defect["severity"] == "High" else "#64748b"
            
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; margin-bottom: 8px;">
                <span style="color: {color};">{defect['severity']}</span>
                <span style="color: #f8fafc; font-weight: 600;">{defect['count']}</span>
                <span style="color: #10b981; font-size: 12px;">{defect['trend']}</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key Metrics Table
    st.markdown("### 📋 Quality Metrics Summary")
    
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
    """Render AI performance tab."""
    
    st.markdown("### 🤖 AI Agent Performance")
    
    # Agent Stats
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
    
    # Model Usage
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Model Usage Distribution")
        model_usage = AI_PERFORMANCE_REPORT["model_usage"]
        
        for model in model_usage:
            color = "#6366f1" if model["model"] == "GPT-4" else "#22d3ee" if model["model"] == "Claude" else "#10b981"
            
            st.markdown(f"""
            <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                    <span style="color: #f8fafc; font-weight: 600;">{model['model']}</span>
                    <span style="color: #94a3b8;">{model['requests']:,} requests</span>
                </div>
                <div style="width: 100%; height: 6px; background: rgba(30, 41, 59, 0.8); border-radius: 3px;">
                    <div style="width: {model['percentage']}%; height: 100%; background: {color}; border-radius: 3px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Token Usage")
        
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
    
    # Performance by Agent Type
    st.markdown("### 📊 Performance by Agent Type")
    
    by_type = AI_PERFORMANCE_REPORT["by_agent_type"]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[a["type"] for a in by_type],
        y=[a["tasks"] for a in by_type],
        marker_color="#6366f1",
        text=[a["tasks"] for a in by_type],
        textposition="outside",
    ))
    
    fig.update_layout(
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        showlegend=False,
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_flaky_tests_tab() -> None:
    """Render flaky tests analysis tab."""
    
    st.markdown("### 📳 Flaky Test Analysis")
    
    # Summary
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
    
    # Top Flaky Tests
    st.markdown("### 🔝 Top Flaky Tests")
    
    top_flaky = FLAKY_REPORT["top_flaky_tests"]
    
    for test in top_flaky:
        rate_color = "#ef4444" if test["rate"] >= 10 else "#f59e0b"
        
        st.markdown(f"""
        <div style="padding: 14px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 14px; color: #f8fafc; font-family: monospace;">{test['name']}</div>
                    <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Reason: {test['reason']}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 24px; font-weight: 700; color: {rate_color};">{test['rate']}%</div>
                    <div style="font-size: 11px; color: #64748b;">Fails: {test['fails']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Root Causes
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Root Causes")
        causes = FLAKY_REPORT["root_causes"]
        
        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=[c["cause"] for c in causes],
            values=[c["count"] for c in causes],
            hole=0.4,
            marker=dict(colors=["#ef4444", "#f59e0b", "#3b82f6", "#10b981", "#6366f1"]),
        ))
        
        fig.update_layout(
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### By Module")
        by_module = FLAKY_REPORT["by_module"]
        
        for module in by_module:
            impact_colors = {"critical": "#ef4444", "high": "#f59e0b", "medium": "#3b82f6", "low": "#10b981"}
            color = impact_colors.get(module["impact"], "#64748b")
            
            st.markdown(f"""
            <div style="padding: 10px; background: rgba(30, 41, 59, 0.6); border-radius: 6px; margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #f8fafc;">{module['module']}</span>
                    <span style="color: {color};">{module['flaky_count']} tests ({module['rate']}%)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_reports_center() -> None:
    """Main page render function."""
    
    # Initialize state
    init_reports_state()
    
    # Header
    render_header(REPORTS_INFO)
    
    # Main Tabs
    tabs = st.tabs([
        "📈 Overview",
        "🧪 Coverage",
        "✅ Quality",
        "🤖 AI Performance",
        "📳 Flaky Tests",
        "📝 Reports",
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
        # Recent Reports
        st.markdown("### 📄 Recent Reports")
        
        for report in RECENT_REPORTS:
            report_card(report)
        
        st.markdown("")
        
        # Scheduled Reports
        scheduled_reports_table(SCHEDULED_REPORTS)
        
        st.markdown("")
        
        # Report Generator
        report_generator(REPORT_TEMPLATES)
        
        st.markdown("")
        
        # Export Panel
        export_panel()


def main() -> None:
    """Entry point."""
    render_reports_center()


if __name__ == "__main__":
    main()
