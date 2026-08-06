"""Executions page for AI-QOS."""
import streamlit as st
from datetime import datetime
from components.core_components import (
    page_header,
    search_bar,
    filter_dropdown,
    execution_card,
    metric_card,
    status_badge,
    empty_state,
)


def render_executions() -> None:
    """Render the executions page."""
    page_header(
        title="Executions",
        subtitle="Monitor and track mission execution history",
        icon="⚡",
        actions=["▶️ Run Mission", "⏸️ Stop All"],
    )
    
    # Filters
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        search_query = search_bar("Search executions...")
    with col2:
        status_filter = st.selectbox("Status", ["All", "Running", "Completed", "Failed", "Pending"])
    with col3:
        time_filter = st.selectbox("Time Range", ["Last 24h", "Last 7 days", "Last 30 days", "All time"])
    with col4:
        view_type = st.selectbox("View", ["List", "Timeline", "Grid"])
    
    st.markdown("---")
    
    # Execution Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Running", 3, icon="⚡")
    with col2:
        metric_card("Completed Today", 24, icon="✅")
    with col3:
        metric_card("Failed", 2, icon="❌")
    with col4:
        metric_card("Avg Duration", "2m 12s", icon="⏱️")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📋 All Executions", "⚡ Running", "📜 History"])
    
    with tab1:
        render_execution_list()
    
    with tab2:
        st.markdown("### Currently Running")
        render_execution_list(filter_status="running")
    
    with tab3:
        render_execution_list(filter_status="completed")


def render_execution_list(filter_status: str = None) -> None:
    """Render execution list with optional filter."""
    executions = [
        {"id": "exe_001", "name": "PR #234 Review", "status": "running", "duration": "2m 34s"},
        {"id": "exe_002", "name": "API Test Suite", "status": "completed", "duration": "5m 12s"},
        {"id": "exe_003", "name": "Security Scan", "status": "running", "duration": "45s"},
        {"id": "exe_004", "name": "Deploy to Staging", "status": "pending", "duration": "-"},
        {"id": "exe_005", "name": "Code Analysis", "status": "completed", "duration": "1m 23s"},
        {"id": "exe_006", "name": "Unit Tests", "status": "failed", "duration": "3m 01s"},
    ]
    
    if filter_status:
        executions = [e for e in executions if e["status"] == filter_status]
    
    if executions:
        for exec_data in executions:
            execution_card(
                execution_id=exec_data["id"],
                mission_name=exec_data["name"],
                status=exec_data["status"],
                duration=exec_data["duration"],
            )
    else:
        empty_state(
            icon="⚡",
            title="No executions found",
            description="Start a mission to see execution details here",
            action_label="Start Mission",
        )
