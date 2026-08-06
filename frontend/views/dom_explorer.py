"""DOM Intelligence Explorer - AI-Powered DOM Operating System.

This page provides comprehensive DOM analysis with AI-powered intelligence
for automation, accessibility, and quality assurance.
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
    generate_console_logs,
    find_node_by_id,
)
from components.dom_components import (
    init_dom_state,
    dom_tree,
    browser_visualizer,
    element_inspector,
    locator_intelligence,
    accessibility_inspector,
    automation_intelligence,
    dom_metrics,
    ai_discoveries,
    console_panel,
    quick_actions,
    element_relationship_graph,
    dom_timeline,
    ai_explanation,
    dom_search,
)


def render_header(info: dict[str, Any]) -> None:
    """Render the page header."""
    st.markdown("""
    <style>
    .dom-header {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95));
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="dom-header">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 8px;">
                    <span style="font-size: 48px;">🔍</span>
                    <div>
                        <h1 style="margin: 0; font-size: 28px; color: #f8fafc;">
                            DOM Intelligence Explorer
                        </h1>
                        <p style="margin: 4px 0 0; font-size: 14px; color: #64748b;">
                            AI-Powered DOM Operating System • Real-Time Analysis
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
                    v{info.get('dom_version', '1.0.0')}
                </span>
                <span style="
                    padding: 6px 14px;
                    background: rgba(16, 185, 129, 0.2);
                    border: 1px solid rgba(16, 185, 129, 0.3);
                    border-radius: 20px;
                    font-size: 12px;
                    color: #10b981;
                ">
                    DOM Health: {info.get('dom_health', 0)}%
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats row
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    
    with col1:
        st.metric("Total Elements", f"{info.get('total_elements', 0):,}")
    with col2:
        st.metric("Interactive", info.get('interactive_elements', 0))
    with col3:
        st.metric("Forms", info.get('forms', 0))
    with col4:
        st.metric("Buttons", info.get('buttons', 0))
    with col5:
        st.metric("Inputs", info.get('inputs', 0))
    with col6:
        st.metric("Tables", info.get('tables', 0))
    with col7:
        st.metric("Coverage", f"{info.get('coverage', 0):.1f}%")
    with col8:
        st.metric("Shadow DOM", info.get('shadow_dom', 0))


def render_left_panel() -> None:
    """Render the left DOM tree panel."""
    with st.container():
        # Search
        dom_search()
        
        st.markdown("")
        
        # DOM Tree
        dom_tree(DOM_TREE, "DOM Tree")


def render_center_panel() -> None:
    """Render the center browser visualizer panel."""
    
    # Get selected element details
    selected_id = st.session_state.dom_selected_node
    element = get_element_details(selected_id)
    
    # View mode toggle
    view_tab1, view_tab2 = st.tabs(["🌐 Browser Preview", "📊 DOM Metrics"])
    
    with view_tab1:
        browser_visualizer(element, f"Live DOM - {selected_id}")
    
    with view_tab2:
        metrics = generate_dom_metrics()
        dom_metrics(metrics, "DOM Metrics")
    
    st.markdown("")
    
    # Timeline
    timeline = generate_discovery_timeline()
    dom_timeline(timeline, "Analysis Timeline")


def render_right_panel() -> None:
    """Render the right inspector panel."""
    
    selected_id = st.session_state.dom_selected_node
    element = get_element_details(selected_id)
    
    # Tabs for different inspector views
    tabs = st.tabs([
        "🔍 Inspector",
        "🎯 Locators",
        "♿ Accessibility",
        "🤖 Automation",
    ])
    
    with tabs[0]:
        element_inspector(element, f"Element: <{element.get('tag', 'unknown')}>")
        
        st.markdown("")
        
        # Element relationships
        element_relationship_graph(selected_id, "Relationships")
        
        st.markdown("")
        
        # AI Explanation
        ai_explanation(element, "AI Explanation")
    
    with tabs[1]:
        locator_intelligence(element, "AI Locator Intelligence")
    
    with tabs[2]:
        accessibility_inspector(element, "Accessibility Inspector")
    
    with tabs[3]:
        automation_intelligence(element, "Automation Intelligence")


def render_bottom_panel() -> None:
    """Render the bottom developer console panel."""
    
    st.markdown("---")
    st.markdown("### 💻 Developer Console")
    
    # Console tabs
    console_tab1, console_tab2, console_tab3 = st.tabs(["📋 Overview", "💻 Console", "🤖 AI Discoveries"])
    
    with console_tab1:
        # Overview of all findings
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### DOM Summary")
            info = DOM_PAGE_INFO
            st.markdown(f"""
            - **URL:** `{info['url']}`
            - **Page:** {info['page']}
            - **Total Elements:** {info['total_elements']:,}
            - **Interactive Elements:** {info['interactive_elements']}
            - **Coverage:** {info['coverage']}%
            - **DOM Health:** {info['dom_health']}%
            """)
        
        with col2:
            st.markdown("#### Quick Stats")
            metrics = generate_dom_metrics()
            st.markdown(f"""
            - **Forms:** {metrics['forms']}
            - **Buttons:** {metrics['buttons']}
            - **Inputs:** {metrics['inputs']}
            - **Tables:** {metrics['tables']}
            - **Links:** {metrics['links']}
            - **ARIA Elements:** {metrics['aria_elements']}
            """)
    
    with console_tab2:
        logs = generate_console_logs()
        console_panel(logs, "Console")
    
    with console_tab3:
        discoveries = generate_ai_discoveries()
        ai_discoveries(discoveries, "AI Discoveries")
    
    st.markdown("")
    
    # Quick Actions
    col1, col2 = st.columns([1, 3])
    
    with col1:
        quick_actions("Quick Actions")
    
    with col2:
        # Additional info
        st.markdown("### 📖 Element Path")
        
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
    """Main page render function."""
    
    # Initialize state
    init_dom_state()
    
    # Header
    render_header(DOM_PAGE_INFO)
    
    # Main layout: 3 columns
    left_col, center_col, right_col = st.columns([0.25, 1, 0.4], gap="medium")
    
    # Left Panel - DOM Tree
    with left_col:
        st.markdown("### 🌳 DOM Explorer")
        render_left_panel()
    
    # Center Panel - Browser Visualizer
    with center_col:
        st.markdown("### 🌐 Browser Workspace")
        render_center_panel()
    
    # Right Panel - Inspector
    with right_col:
        st.markdown("### 🔍 Inspector")
        render_right_panel()
    
    # Bottom Panel - Console
    with st.container():
        render_bottom_panel()


def main() -> None:
    """Entry point."""
    render_page()


if __name__ == "__main__":
    main()
