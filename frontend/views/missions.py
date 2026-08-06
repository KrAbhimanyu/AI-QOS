"""Missions page for AI-QOS."""
import streamlit as st
from datetime import datetime
from components.core_components import (
    page_header,
    search_bar,
    filter_dropdown,
    status_badge,
    mission_card,
    empty_state,
)


def render_missions() -> None:
    """Render the missions page."""
    page_header(
        title="Missions",
        subtitle="Manage AI-powered quality missions",
        icon="🎯",
        actions=["+ New Mission"],
    )
    
    # Filters row
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        search_query = search_bar("Search missions...")
    with col2:
        status_filter = st.selectbox("Status", ["All", "Active", "Completed", "Pending", "Failed"])
    with col3:
        agent_filter = st.selectbox("Agent", ["All Agents", "Code Reviewer", "Tester", "Deployer"])
    with col4:
        sort_by = st.selectbox("Sort", ["Recent", "Name A-Z", "Priority"])
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["All Missions", "🎯 Active", "✅ Completed", "📋 Pending"])
    
    with tab1:
        render_mission_list()
    
    with tab2:
        render_mission_list(filter_status="active")
    
    with tab3:
        render_mission_list(filter_status="completed")
    
    with tab4:
        render_mission_list(filter_status="pending")


def render_mission_list(filter_status: str = None) -> None:
    """Render a list of missions with optional filter."""
    # Sample missions data
    missions = [
        {
            "title": "PR #234 - Authentication Module Review",
            "description": "Comprehensive code review of the new authentication module including OAuth2 integration",
            "status": "completed",
            "agent": "Code Reviewer",
            "progress": 100,
            "created_at": datetime.now(),
        },
        {
            "title": "API Integration Testing",
            "description": "Run end-to-end tests for all API endpoints with various payloads",
            "status": "running",
            "agent": "Tester",
            "progress": 65,
            "created_at": datetime.now(),
        },
        {
            "title": "Staging Deployment v2.1.0",
            "description": "Deploy release version 2.1.0 to staging environment with health checks",
            "status": "pending",
            "agent": "Deployer",
            "progress": 0,
            "created_at": datetime.now(),
        },
        {
            "title": "Weekly Code Quality Scan",
            "description": "Automated code analysis and quality metrics collection",
            "status": "completed",
            "agent": "Code Reviewer",
            "progress": 100,
            "created_at": datetime.now(),
        },
        {
            "title": "Security Vulnerability Check",
            "description": "Scan dependencies and code for known security vulnerabilities",
            "status": "running",
            "agent": "Security Scanner",
            "progress": 30,
            "created_at": datetime.now(),
        },
    ]
    
    # Apply filter
    if filter_status:
        missions = [m for m in missions if m["status"] == filter_status]
    
    if missions:
        for mission in missions:
            mission_card(
                title=mission["title"],
                description=mission["description"],
                status=mission["status"],
                agent=mission["agent"],
                created_at=mission["created_at"],
                progress=mission.get("progress"),
            )
    else:
        empty_state(
            icon="🎯",
            title="No missions found",
            description="Create your first mission to get started with AI-powered quality assurance",
            action_label="Create Mission",
        )
