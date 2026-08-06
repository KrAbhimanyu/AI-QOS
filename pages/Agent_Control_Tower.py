"""
Agent Control Tower - Enterprise AI Agent Monitoring Dashboard

A comprehensive command center for observing and managing AI agents
working together in the AI-QOS system.

Features:
- Real-time agent monitoring
- Communication pipeline visualization
- Resource utilization tracking
- AI model routing
- Health monitoring
- Event stream
- Agent queue management
"""

import time
from datetime import datetime
from typing import Any

import streamlit as st

# Import AI-QOS components
from src.data.mock_data import (
    get_all_agents,
    COMMUNICATION_PIPELINE,
    get_system_metrics,
    get_mission_health,
    generate_live_event,
    AgentCategory,
)
from src.styles.theme import GLASSMORPHISM_CSS
from src.utils.session import SessionState, AutoRefresh

# Import UI components
from src.components.agent_card import agent_card
from src.components.agent_drawer import agent_drawer
from src.components.communication_graph import render_simple_communication_flow
from src.components.resource_panel import resource_panel
from src.components.model_panel import model_panel
from src.components.event_stream import event_stream
from src.components.agent_queue import agent_queue
from src.components.health_gauge import render_health_dashboard
from src.components.search_bar import search_bar
from src.components.mission_header import render_mission_header, render_refresh_controls
from src.components.left_sidebar import left_sidebar, render_category_stats
from src.components.timeline import timeline


def inject_custom_css() -> None:
    """Inject custom CSS styling."""
    st.markdown(GLASSMORPHISM_CSS, unsafe_allow_html=True)
    
    # Additional page-specific styles
    st.markdown("""
    <style>
    /* Page layout */
    .main-content {
        padding: 20px;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(99, 102, 241, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(99, 102, 241, 0.7);
    }
    
    /* Agent grid animation */
    .agent-card {
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95));
        border-right: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(51, 65, 85, 0.3);
        border-radius: 8px;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(51, 65, 85, 0.3);
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(99, 102, 241, 0.2);
        border-bottom: 2px solid #6366f1;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Loading animation */
    .loading-pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    </style>
    """, unsafe_allow_html=True)


def initialize_session() -> None:
    """Initialize session state with data."""
    SessionState.initialize()
    
    # Load agents if not loaded
    if not st.session_state.agents:
        st.session_state.agents = get_all_agents()
        st.session_state.mission_start = datetime.now()
    
    # Generate initial events if not present
    if not st.session_state.events:
        for _ in range(15):
            st.session_state.events.append(generate_live_event())


def render_main_layout() -> None:
    """Render the main application layout."""
    
    # Initialize session
    initialize_session()
    
    # Inject CSS
    inject_custom_css()
    
    # Auto refresh check
    if AutoRefresh.should_refresh():
        # Refresh data
        st.session_state.agents = get_all_agents()
        
        # Add a new event occasionally
        if len(st.session_state.events) < 50:
            st.session_state.events.insert(0, generate_live_event())
        
        AutoRefresh.update_timestamp()
    
    agents = st.session_state.agents
    events = st.session_state.events
    metrics = get_system_metrics()
    health = get_mission_health()
    
    # Count running agents
    running_count = sum(1 for a in agents if a["status"].value == "running")
    
    # Mission header
    render_mission_header(
        mission_name=st.session_state.mission_name,
        environment=st.session_state.environment,
        agent_count=len(agents),
        running_count=running_count,
        execution_time=st.session_state.execution_start,
        auto_refresh=st.session_state.auto_refresh,
    )
    
    # Main layout: 3 columns
    col_sidebar, col_main, col_right = st.columns([0.25, 1, 0.35], gap="medium")
    
    # Left Sidebar
    with col_sidebar:
        st.markdown("### 🎯 Categories")
        selected_category = left_sidebar(
            agents=agents,
            selected_category=st.session_state.filter_category,
            on_category_change=lambda x: SessionState.set_filter(category=x),
        )
        
        # Update filter if changed
        if selected_category != st.session_state.filter_category:
            SessionState.set_filter(category=selected_category)
            st.rerun()
        
        st.markdown("")
        render_category_stats(agents)
    
    # Main content area
    with col_main:
        # Search and filter
        search_query, filter_category, filter_status = search_bar(
            agents=agents,
            categories=[cat.value for cat in AgentCategory],
            statuses=["running", "waiting", "paused", "failed", "completed", "idle"],
        )
        
        # Update filters
        if filter_category != st.session_state.filter_category:
            SessionState.set_filter(category=filter_category)
        if filter_status.lower() != st.session_state.filter_status.lower():
            SessionState.set_filter(status=filter_status.lower())
        if search_query != st.session_state.search_query:
            SessionState.set_search(search_query)
        
        # Get filtered agents
        filtered_agents = SessionState.get_filtered_agents(agents)
        
        # Communication Pipeline
        with st.expander("🔀 Communication Pipeline", expanded=True):
            render_simple_communication_flow(COMMUNICATION_PIPELINE, agents)
        
        st.markdown("")  # Spacer
        
        # Agent Grid
        st.markdown(f"### 🤖 Agent Grid ({len(filtered_agents)} agents)")
        
        if filtered_agents:
            # Create grid layout
            for i, agent in enumerate(filtered_agents):
                agent_card(agent, key=f"agent_{i}")
        else:
            st.info("No agents match your search criteria.")
        
        st.markdown("")  # Spacer
        
        # Bottom Timeline
        timeline(agents, events)
    
    # Right sidebar
    with col_right:
        # Refresh controls
        render_refresh_controls(
            auto_refresh=st.session_state.auto_refresh,
            refresh_interval=st.session_state.refresh_interval,
        )
        
        st.markdown("")  # Spacer
        
        # Agent Queue
        agent_queue(agents)
        
        st.markdown("")  # Spacer
        
        # Mission Health
        render_health_dashboard(health)
        
        st.markdown("")  # Spacer
        
        # Resource Dashboard
        with st.expander("📊 Resource Dashboard", expanded=True):
            resource_panel(metrics)
        
        st.markdown("")  # Spacer
        
        # AI Model Panel
        with st.expander("🤖 AI Model Panel", expanded=True):
            model_panel(metrics["model_usage"])
        
        st.markdown("")  # Spacer
        
        # Event Stream
        with st.expander("🔔 Event Stream", expanded=True):
            event_stream(events, max_display=10)
    
    # Agent Drawer (modal overlay)
    if st.session_state.drawer_open and st.session_state.selected_agent:
        agent_drawer(st.session_state.selected_agent)


def main() -> None:
    """Main application entry point."""
    render_page_config()
    render_main_layout()


def render_page_config() -> None:
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Agent Control Tower - AI-QOS",
        page_icon="🎛️",
        layout="wide",
        initial_sidebar_state="collapsed",
    )


if __name__ == "__main__":
    main()
