"""DOM Intelligence Explorer - AI-Powered DOM Operating System.

Premium enterprise layout reusing the AI-QOS UI Foundation (design tokens
from themes/tokens.py and shared components from components/shared.py).
Business logic, session state, and all component signatures are preserved.
"""
from typing import Any
import streamlit as st

from utils.dom_data import (
    DOM_PAGE_INFO,
    DOM_TREE,
    get_element_details,
    generate_dom_metrics,
    generate_ai_discoveries,
    generate_discovery_timeline,
)
from components.dom_components import (
    init_dom_state,
    dom_header,
    dom_kpi_strip,
    dom_tree,
    browser_visualizer,
    element_inspector,
    locator_intelligence,
    accessibility_inspector,
    automation_intelligence,
    dom_metrics,
    ai_discoveries,
    quick_actions,
    element_relationship_graph,
    dom_timeline,
    ai_explanation,
    dom_search,
    bottom_workspace_tabs,
)
from components.shared import section_header, spacer


def render_left_panel() -> None:
    """Render the left DOM tree panel."""
    dom_search()
    spacer(1)
    dom_tree(DOM_TREE, "DOM Tree")


def render_center_panel() -> None:
    """Render the center browser digital twin panel."""
    selected_id = st.session_state.dom_selected_node
    element = get_element_details(selected_id)

    view_tab1, view_tab2 = st.tabs(["🌐 Browser Digital Twin", "📊 DOM Metrics"])
    with view_tab1:
        browser_visualizer(element, "Browser Digital Twin")
    with view_tab2:
        metrics = generate_dom_metrics()
        dom_metrics(metrics, "DOM Metrics")

    spacer(1)
    timeline = generate_discovery_timeline()
    dom_timeline(timeline, "Analysis Timeline")


def render_right_panel() -> None:
    """Render the right AI inspector panel."""
    selected_id = st.session_state.dom_selected_node
    element = get_element_details(selected_id)

    tabs = st.tabs([
        "🔍 Inspector",
        "🎯 Locators",
        "♿ Accessibility",
        "🤖 Automation",
    ])
    with tabs[0]:
        element_inspector(element, "Element Inspector")
        spacer(1)
        element_relationship_graph(selected_id, "Relationships")
        spacer(1)
        ai_explanation(element, "AI Explanation")
    with tabs[1]:
        locator_intelligence(element, "AI Locator Intelligence")
    with tabs[2]:
        accessibility_inspector(element, "Accessibility Inspector")
    with tabs[3]:
        automation_intelligence(element, "Automation Intelligence")


def render_middle_panels() -> None:
    """Render the Locator Rank | Relationship Graph | Automation row."""
    selected_id = st.session_state.dom_selected_node
    element = get_element_details(selected_id)

    col_a, col_b, col_c = st.columns(3, gap="medium")
    with col_a:
        locator_intelligence(element, "Locator Rank")
    with col_b:
        element_relationship_graph(selected_id, "Relationship Graph")
    with col_c:
        automation_intelligence(element, "Automation Intelligence")


def render_bottom_panel() -> None:
    """Render the bottom developer workspace (glass tabs) + quick actions."""
    st.markdown("---")
    section_header("Developer Workspace", icon="🛠️")
    bottom_workspace_tabs()
    spacer(2)

    col1, col2 = st.columns([1, 2])
    with col1:
        quick_actions("Quick Actions")
    with col2:
        section_header("Element Path", icon="📖")
        selected_id = st.session_state.dom_selected_node
        element = get_element_details(selected_id)
        path_col1, path_col2 = st.columns(2)
        with path_col1:
            st.markdown("**XPath**")
            st.code(element.get("xpath", "N/A"), language="xml")
        with path_col2:
            st.markdown("**CSS Selector**")
            st.code(element.get("css", "N/A"), language="css")


def render_page() -> None:
    """Main page render function (preserved entry point)."""
    init_dom_state()

    # Hero Header
    dom_header(DOM_PAGE_INFO)

    # DOM KPI Strip
    dom_kpi_strip()
    spacer(1)

    # Main 3-column layout: DOM Tree | Browser Digital Twin | AI Inspector
    left_col, center_col, right_col = st.columns([0.25, 1, 0.4], gap="medium")
    with left_col:
        render_left_panel()
    with center_col:
        render_center_panel()
    with right_col:
        render_right_panel()

    # Middle panels: Locator Rank | Relationship Graph | Automation Intelligence
    st.markdown("---")
    render_middle_panels()

    # AI Discoveries overview
    st.markdown("---")
    discoveries = generate_ai_discoveries()
    ai_discoveries(discoveries, "AI Discoveries")

    # Bottom developer workspace
    render_bottom_panel()


def main() -> None:
    """Entry point."""
    render_page()


if __name__ == "__main__":
    main()
