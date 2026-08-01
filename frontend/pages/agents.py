"""Agents page for AI-QOS."""
import streamlit as st
from components.core_components import (
    page_header,
    search_bar,
    filter_dropdown,
    agent_card,
    metric_card,
    empty_state,
)


def render_agents() -> None:
    """Render the agents page."""
    page_header(
        title="AI Agents",
        subtitle="Manage and monitor your AI agent workforce",
        icon="🤖",
        actions=["+ Add Agent"],
    )
    
    # Filters
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = search_bar("Search agents...")
    with col2:
        status_filter = st.selectbox("Status", ["All", "Active", "Idle", "Offline"])
    with col3:
        role_filter = st.selectbox("Role", ["All Roles", "Code Reviewer", "Tester", "Deployer", "Security"])
    
    st.markdown("---")
    
    # Agent Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Agents", 8, icon="🤖")
    with col2:
        metric_card("Active Now", 5, icon="⚡")
    with col3:
        metric_card("Tasks Today", 47, icon="📋")
    with col4:
        metric_card("Avg Success", "96.2%", icon="✅")
    
    st.markdown("---")
    
    # Agent Grid
    st.markdown("### Agent Workforce")
    
    # Create two columns for agents
    col1, col2 = st.columns(2)
    
    agents = [
        {"name": "CodeMaster", "role": "Senior Code Reviewer", "status": "active", "tasks": 124, "success": 98.4},
        {"name": "TestBot", "role": "QA Testing Agent", "status": "active", "tasks": 89, "success": 94.2},
        {"name": "DeployPro", "role": "Deployment Specialist", "status": "idle", "tasks": 56, "success": 99.1},
        {"name": "SecurityScan", "role": "Security Analyst", "status": "active", "tasks": 34, "success": 96.8},
        {"name": "DocWriter", "role": "Documentation Agent", "status": "active", "tasks": 67, "success": 92.5},
        {"name": "PerfMonitor", "role": "Performance Analyzer", "status": "idle", "tasks": 45, "success": 97.3},
    ]
    
    with col1:
        for agent in agents[:3]:
            agent_card(
                name=agent["name"],
                role=agent["role"],
                status=agent["status"],
                tasks_completed=agent["tasks"],
                success_rate=agent["success"],
            )
    
    with col2:
        for agent in agents[3:]:
            agent_card(
                name=agent["name"],
                role=agent["role"],
                status=agent["status"],
                tasks_completed=agent["tasks"],
                success_rate=agent["success"],
            )
