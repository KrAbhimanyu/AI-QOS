"""Agent Control Tower - AI-QOS Enterprise AI Organization Operating Center."""
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
    kpi_strip,
    ai_swarm,
    memory_utilization,
    quick_actions,
    bottom_workspace_tabs,
    section_header,
)


def render_agent_control_tower() -> None:
    """Render the Enterprise AI Organization Operating Center.

    Preserves the original session state, agent cards, event stream, resource
    monitoring, model routing, queue management, navigation, and business
    logic. Reorganizes the surface into the premium NASA Mission Control-style
    layout: HeroHeader -> KPI Strip -> Swarm|Graph|Router ->
    ActiveAgents|Events|Memory -> Queue|Resources|Health -> Bottom tabs +
    Quick Actions.
    """
    init_agent_state()

    # Count running agents
    running_count = sum(1 for a in MOCK_AGENTS if a["status"] == "running")

    # HeroHeader - sticky enterprise command header (reuses foundation tokens)
    agent_header(
        mission="E2E Regression v2.1",
        environment="Staging",
        running_agents=running_count,
        total_agents=len(MOCK_AGENTS),
        health=94,
        exec_time="5m 32s",
    )

    # KPI Strip - MetricCard grid
    kpi_strip()

    # Action Buttons (Toolbar)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🔄 Refresh", width='stretch'):
            st.rerun()
    with col2:
        st.selectbox("Status", ["All", "Running", "Idle", "Paused", "Failed"], label_visibility="collapsed")
    with col3:
        st.selectbox("Category", ["All Categories", "Intelligence", "Testing", "Documentation", "Security", "Learning", "Support"], label_visibility="collapsed")
    with col4:
        if st.button("🔍 Search Agents", width='stretch'):
            st.info("Search functionality")

    # Main Content - Three Column Layout: AI Swarm | Collaboration Graph | Model Router
    left_col, center_col, right_col = st.columns([1.2, 1.8, 1.2], gap="medium")

    with left_col:
        ai_swarm()

    with center_col:
        communication_graph()

    with right_col:
        ai_model_panel()

    # Second row: Active Agents | Event Stream | Memory Utilization
    active_col, event_col, mem_col = st.columns([1.6, 1.1, 1.1], gap="medium")

    with active_col:
        _active_agents_panel()

    with event_col:
        event_stream()

    with mem_col:
        memory_utilization()

    # Third row: Queue | Resource Monitor | Mission Health
    q_col, r_col, h_col = st.columns([1.1, 1.1, 1.0], gap="medium")

    with q_col:
        agent_queue()

    with r_col:
        resource_dashboard()

    with h_col:
        mission_health()

    # Quick Actions - glass buttons
    quick_actions()

    # Bottom Workspace - shared GlassPanel foundation with tabs
    bottom_workspace_tabs()

    # Agent Details section (preserved drawers)
    _agent_details_section()


def _active_agents_panel() -> None:
    """Render the active agents grid (preserves agent card rendering)."""
    section_header("Active Agents", icon="🤖")

    # Filter agents by status/category (preserves filtering logic)
    filtered_agents = MOCK_AGENTS
    cols = st.columns(2)
    for i, agent in enumerate(filtered_agents[:8]):
        with cols[i % 2]:
            agent_card(agent)
            if st.button("Details", key=f"agent_{agent['id']}", width='stretch'):
                set_agent_data("selected_agent", agent["id"])


def _agent_details_section() -> None:
    """Render the agent details drawers (preserved)."""
    cols = st.columns(2)
    for i, agent in enumerate(MOCK_AGENTS[:4]):
        with cols[i % 2]:
            agent_drawer(agent)
