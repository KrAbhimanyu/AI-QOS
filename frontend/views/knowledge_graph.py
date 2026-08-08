"""Knowledge Graph — AI Cognitive Intelligence Center.

Premium enterprise cognitive workspace reusing the AI-QOS UI Foundation
(design tokens from themes/tokens.py and shared components from
components/shared.py). Business logic, session state, data imports and
all component signatures are preserved — no breaking changes.
"""
from typing import Any
import streamlit as st

from utils.knowledge_graph_data import (
    GRAPH_INFO,
    NAVIGATOR_TREE,
    COVERAGE_MAP,
    BUG_HEATMAP,
    GRAPH_TIMELINE,
    GRAPH_ANALYTICS,
    NODE_EXECUTION_HISTORY,
    LATEST_CHANGES,
    KNOWLEDGE_NODES,
    KNOWLEDGE_RELATIONSHIPS,
    BUSINESS_FLOWS,
    AI_DISCOVERIES,
    GRAPH_STATISTICS,
    AI_RECOMMENDATIONS,
    get_node_by_id,
    get_connected_nodes,
    get_relationships_for_node,
    get_graph_data_for_visualization,
    search_nodes,
)
from components.knowledge_graph_components import (
    init_knowledge_state,
    knowledge_navigator,
    knowledge_graph_canvas,
    node_inspector,
    ai_reasoning_panel,
    impact_analysis_panel,
    business_flow_explorer,
    graph_statistics,
    ai_discoveries_panel,
    ai_recommendations_panel,
    kg_quick_actions,
    kg_search,
    mini_map,
    select_kg_node,
    coverage_map_panel,
    bug_heatmap_panel,
    graph_timeline_panel,
    graph_analytics_panel,
    dependency_explorer_panel,
    recommendation_panel,
    execution_history_panel,
    latest_changes_panel,
    kg_header,
    kg_kpi_strip,
    knowledge_health_panel,
    dependency_chain_panel,
    bottom_workspace_tabs,
)
from components.shared import section_header, spacer


def render_left_panel() -> None:
    """Render the left knowledge explorer panel (Graph Explorer)."""
    query = kg_search()

    display_nodes = KNOWLEDGE_NODES
    if query:
        display_nodes = search_nodes(query)
        st.markdown(f"**Found {len(display_nodes)} matching nodes**")

    knowledge_navigator(display_nodes, "Knowledge Navigator")
    spacer(1)
    coverage_map_panel(COVERAGE_MAP, "Coverage Map")
    spacer(1)
    bug_heatmap_panel(BUG_HEATMAP, "Bug Heatmap")


def render_center_panel() -> None:
    """Render the center AI Cognitive Graph panel."""
    selected_node_id = st.session_state.kg_selected_node
    graph_data = get_graph_data_for_visualization()

    view_tab1, view_tab2, view_tab3 = st.tabs(["🕸️ Graph", "🔀 Flows", "📈 Stats"])
    with view_tab1:
        knowledge_graph_canvas(graph_data, selected_node_id, "AI Cognitive Graph")
    with view_tab2:
        business_flow_explorer(BUSINESS_FLOWS, "Business Flows")
    with view_tab3:
        graph_statistics(GRAPH_STATISTICS, "Graph Statistics")

    spacer(1)

    col1, col2 = st.columns(2)
    with col1:
        mini_map(graph_data, selected_node_id, "Mini Map")
    with col2:
        graph_timeline_panel(GRAPH_TIMELINE, "Timeline")


def render_right_panel() -> None:
    """Render the right Knowledge Inspector panel."""
    selected_node_id = st.session_state.kg_selected_node
    node = get_node_by_id(selected_node_id)

    tabs = st.tabs([
        "🔍 Node",
        "💡 Reasoning",
        "📊 Impact",
        "🔗 Deps",
    ])

    with tabs[0]:
        node_inspector(node, "Node Inspector")
        spacer(1)
        execution_history_panel(NODE_EXECUTION_HISTORY[:5], "Recent Runs")
    with tabs[1]:
        ai_reasoning_panel(node, "AI Reasoning")
    with tabs[2]:
        impact_analysis_panel(selected_node_id, "Impact Analysis")
    with tabs[3]:
        dependencies = {
            "required_by": ["Dashboard Page", "Reports Page"],
            "affected": ["Test Cases", "Feature Files"],
        }
        dependency_explorer_panel(node, dependencies, "Dependencies")

    spacer(1)
    kg_quick_actions("Quick Actions")


def render_middle_panels() -> None:
    """Render the AI Reasoning | Dependency Explorer | Knowledge Health row."""
    selected_node_id = st.session_state.kg_selected_node
    node = get_node_by_id(selected_node_id)

    col_a, col_b, col_c = st.columns(3, gap="medium")
    with col_a:
        ai_reasoning_panel(node, "AI Reasoning")
    with col_b:
        dependency_chain_panel("Dependency Explorer")
    with col_c:
        knowledge_health_panel("Knowledge Health")


def render_bottom_panel() -> None:
    """Render the bottom cognitive workspace (glass tabs)."""
    st.markdown("---")
    section_header("Cognitive Workspace", icon="🧠")
    bottom_workspace_tabs()
    spacer(2)

    # AI Discoveries + Recommendations summary across the bottom
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        ai_discoveries_panel(AI_DISCOVERIES, "AI Discoveries")
    with col2:
        ai_recommendations_panel(AI_RECOMMENDATIONS, "AI Recommendations")


def render_page() -> None:
    """Main page render function (preserved entry point)."""
    init_knowledge_state()

    # Sticky glass Hero Header
    kg_header(GRAPH_INFO)

    # KPI Strip (MetricCard grid)
    kg_kpi_strip()
    spacer(1)

    # Main 3-column layout: Graph Explorer | AI Cognitive Graph | Knowledge Inspector
    left_col, center_col, right_col = st.columns([1, 2, 1], gap="medium")
    with left_col:
        render_left_panel()
    with center_col:
        render_center_panel()
    with right_col:
        render_right_panel()

    # Middle row: AI Reasoning | Dependency Explorer | Knowledge Health
    st.markdown("---")
    render_middle_panels()

    # Bottom cognitive workspace
    render_bottom_panel()


def main() -> None:
    """Entry point."""
    render_page()


if __name__ == "__main__":
    main()
