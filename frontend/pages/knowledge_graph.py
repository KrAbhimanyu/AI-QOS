"""Knowledge Graph & AI Reasoning Center.

This page provides an interactive knowledge graph visualization
with AI-powered reasoning and impact analysis.
"""

from typing import Any
import streamlit as st

from utils.knowledge_graph_data import (
    GRAPH_INFO,
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
)


def render_header(info: dict[str, Any]) -> None:
    """Render the page header."""
    st.markdown("""
    <style>
    .kg-header {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95));
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="kg-header">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 8px;">
                    <span style="font-size: 48px;">🕸️</span>
                    <div>
                        <h1 style="margin: 0; font-size: 28px; color: #f8fafc;">
                            Knowledge Graph & AI Reasoning
                        </h1>
                        <p style="margin: 4px 0 0; font-size: 14px; color: #64748b;">
                            AI-Powered Knowledge Operating System • Enterprise Intelligence
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
                    v{info.get('knowledge_version', '1.0')}
                </span>
                <span style="
                    padding: 6px 14px;
                    background: rgba(16, 185, 129, 0.2);
                    border: 1px solid rgba(16, 185, 129, 0.3);
                    border-radius: 20px;
                    font-size: 12px;
                    color: #10b981;
                ">
                    Graph Health: {info.get('graph_health', 0)}%
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats row
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    
    with col1:
        st.metric("Nodes", f"{info.get('total_nodes', 0):,}")
    with col2:
        st.metric("Relationships", f"{info.get('relationships', 0):,}")
    with col3:
        st.metric("Pages", info.get('pages', 0))
    with col4:
        st.metric("Components", info.get('components', 0))
    with col5:
        st.metric("APIs", info.get('apis', 0))
    with col6:
        st.metric("Rules", info.get('business_rules', 0))
    with col7:
        st.metric("Coverage", f"{info.get('coverage', 0):.1f}%")
    with col8:
        st.metric("Flows", info.get('business_flows', 0))


def render_left_panel() -> None:
    """Render the left knowledge navigator panel."""
    
    # Search
    query = kg_search()
    
    # Filter nodes if search query exists
    display_nodes = KNOWLEDGE_NODES
    if query:
        display_nodes = search_nodes(query)
        st.markdown(f"**Found {len(display_nodes)} matching nodes**")
    
    # Navigator
    knowledge_navigator(display_nodes, "Knowledge Navigator")


def render_center_panel() -> None:
    """Render the center graph canvas panel."""
    
    selected_node_id = st.session_state.kg_selected_node
    graph_data = get_graph_data_for_visualization()
    
    # View mode toggle
    view_tab1, view_tab2, view_tab3 = st.tabs(["🕸️ Graph View", "🔀 Business Flows", "📈 Statistics"])
    
    with view_tab1:
        knowledge_graph_canvas(graph_data, selected_node_id, "Knowledge Graph")
    
    with view_tab2:
        business_flow_explorer(BUSINESS_FLOWS, "Business Flows")
    
    with view_tab3:
        graph_statistics(GRAPH_STATISTICS, "Graph Statistics")
    
    st.markdown("")
    
    # Mini Map
    mini_map(graph_data, selected_node_id, "Mini Map")


def render_right_panel() -> None:
    """Render the right inspector panel."""
    
    selected_node_id = st.session_state.kg_selected_node
    node = get_node_by_id(selected_node_id)
    
    # Tabs for different inspector views
    tabs = st.tabs([
        "🔍 Node Details",
        "💡 AI Reasoning",
        "📊 Impact Analysis",
    ])
    
    with tabs[0]:
        node_inspector(node, "Node Inspector")
    
    with tabs[1]:
        ai_reasoning_panel(node, "AI Reasoning")
    
    with tabs[2]:
        impact_analysis_panel(selected_node_id, "Impact Analysis")
    
    st.markdown("")
    
    # Quick Actions
    kg_quick_actions("Quick Actions")


def render_bottom_panel() -> None:
    """Render the bottom intelligence panel."""
    
    st.markdown("---")
    st.markdown("### 🧠 Intelligence Center")
    
    # Tabs
    intel_tab1, intel_tab2, intel_tab3 = st.tabs([
        "🤖 AI Discoveries",
        "🎯 AI Recommendations",
        "🔗 Relationships",
    ])
    
    with intel_tab1:
        ai_discoveries_panel(AI_DISCOVERIES, "AI Discoveries")
    
    with intel_tab2:
        ai_recommendations_panel(AI_RECOMMENDATIONS, "AI Recommendations")
    
    with intel_tab3:
        # Show relationships for selected node
        selected_node_id = st.session_state.kg_selected_node
        relationships = get_relationships_for_node(selected_node_id)
        
        st.markdown(f"### 🔗 Relationships ({len(relationships)})")
        
        if not relationships:
            st.info("No relationships found for this node.")
        else:
            for rel in relationships:
                source_node = get_node_by_id(rel["source"])
                target_node = get_node_by_id(rel["target"])
                
                if source_node and target_node:
                    type_colors = {
                        "contains": "#6366f1",
                        "has": "#22d3ee",
                        "uses": "#f59e0b",
                        "calls": "#10b981",
                        "validates": "#ec4899",
                        "covers": "#14b8a6",
                        "affects": "#ef4444",
                    }
                    color = type_colors.get(rel.get("type", "default"), "#64748b")
                    
                    direction = "→" if rel["source"] == selected_node_id else "←"
                    
                    st.markdown(f"""
                    <div style="
                        display: flex;
                        align-items: center;
                        gap: 12px;
                        padding: 12px;
                        background: rgba(30, 41, 59, 0.6);
                        border-radius: 8px;
                        margin-bottom: 8px;
                    ">
                        <div style="flex: 1;">
                            <span style="color: #f8fafc;">{source_node['name']}</span>
                        </div>
                        <div style="
                            padding: 4px 8px;
                            background: {color}20;
                            border-radius: 4px;
                            font-size: 11px;
                            color: {color};
                        ">
                            {rel.get('label', rel.get('type', ''))}
                        </div>
                        <div style="flex: 1; text-align: right;">
                            <span style="color: #f8fafc;">{target_node['name']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)


def render_page() -> None:
    """Main page render function."""
    
    # Initialize state
    init_knowledge_state()
    
    # Header
    render_header(GRAPH_INFO)
    
    # Main layout: 3 columns
    left_col, center_col, right_col = st.columns([0.25, 1, 0.4], gap="medium")
    
    # Left Panel - Knowledge Navigator
    with left_col:
        st.markdown("### 📚 Navigator")
        render_left_panel()
    
    # Center Panel - Graph Canvas
    with center_col:
        st.markdown("### 🕸️ Knowledge Graph")
        render_center_panel()
    
    # Right Panel - Inspector
    with right_col:
        st.markdown("### 🔍 Inspector")
        render_right_panel()
    
    # Bottom Panel - Intelligence
    with st.container():
        render_bottom_panel()


def main() -> None:
    """Entry point."""
    render_page()


if __name__ == "__main__":
    main()
