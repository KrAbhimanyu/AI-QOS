"""Agent Control Tower - AI-QOS."""
import streamlit as st
from components.agent_components import (
    init_agent_state,
    get_agent_data,
    set_agent_data,
    MOCK_AGENTS,
    agent_header,
    agent_card,
    agent_categories,
    communication_graph,
    agent_queue,
    resource_dashboard,
    ai_model_panel,
    event_stream,
    mission_health,
    agent_drawer,
)


def render_agent_control_tower() -> None:
    """Render the Agent Control Tower page."""
    init_agent_state()
    
    # Count running agents
    running_count = sum(1 for a in MOCK_AGENTS if a["status"] == "running")
    
    # Page Header
    agent_header(
        mission="E2E Regression v2.1",
        environment="Staging",
        running_agents=running_count,
        total_agents=len(MOCK_AGENTS),
        health=94,
        exec_time="5m 32s",
    )
    
    # Action Buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    with col2:
        status_filter = st.selectbox("Status", ["All", "Running", "Idle", "Paused", "Failed"], label_visibility="collapsed")
    
    with col3:
        category_filter = st.selectbox("Category", ["All Categories", "Intelligence", "Testing", "Documentation", "Security", "Learning", "Support"], label_visibility="collapsed")
    
    with col4:
        if st.button("🔍 Search Agents", use_container_width=True):
            st.info("Search functionality")
    
    st.markdown("<hr style='margin: 1rem 0; border-color: #334155;'>", unsafe_allow_html=True)
    
    # Main Content - Three Column Layout
    left_col, center_col, right_col = st.columns([1, 2.5, 1])
    
    # LEFT SIDEBAR
    with left_col:
        agent_categories()
        mission_health()
    
    # CENTER PANEL
    with center_col:
        # Communication Graph
        communication_graph()
        
        # Agent Grid
        st.markdown("<h3 style='color: #F1F5F9; margin: 1.5rem 0 1rem;'>🤖 Active Agents</h3>", unsafe_allow_html=True)
        
        # Filter agents
        filtered_agents = MOCK_AGENTS
        if status_filter != "All":
            filtered_agents = [a for a in filtered_agents if a["status"] == status_filter.lower()]
        if category_filter != "All Categories":
            filtered_agents = [a for a in filtered_agents if a["category"] == category_filter]
        
        # Display agent cards in grid
        cols = st.columns(3)
        for i, agent in enumerate(filtered_agents):
            with cols[i % 3]:
                agent_card(agent)
                if st.button(f"Details", key=f"agent_{agent['id']}", use_container_width=True):
                    set_agent_data("selected_agent", agent["id"])
                st.markdown("")  # Spacer
        
        # Agent Queue
        st.markdown("<h4 style='color: #F1F5F9; margin: 1.5rem 0 1rem;'>📋 Agent Queue</h4>", unsafe_allow_html=True)
        agent_queue()
    
    # RIGHT SIDEBAR
    with right_col:
        resource_dashboard()
        ai_model_panel()
        event_stream()
    
    # Bottom Section - Agent Details
    st.markdown("<hr style='margin: 1.5rem 0; border-color: #334155;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #F1F5F9; margin: 0 0 1rem;'>🔍 Agent Details</h3>", unsafe_allow_html=True)
    
    # Display all agent drawers
    cols = st.columns(2)
    for i, agent in enumerate(MOCK_AGENTS[:4]):  # Show first 4 agents
        with cols[i % 2]:
            agent_drawer(agent)
