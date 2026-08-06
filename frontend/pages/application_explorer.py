"""Application Explorer - Digital Twin of the Application.

This page provides a comprehensive view of the application structure,
components, and metadata discovered by AI analysis.
"""

from typing import Any
import streamlit as st
from datetime import datetime

from utils.explorer_data import (
    APPLICATION_INFO,
    APPLICATION_TREE,
    generate_page_detail,
    generate_statistics,
    generate_application_map,
    generate_discovery_timeline,
    generate_ai_discoveries,
    generate_quick_actions,
    get_all_pages,
    search_pages,
)
from components.explorer_components import (
    init_explorer_state,
    application_tree,
    page_gallery,
    page_workspace,
    application_map,
    statistics_dashboard,
    ai_discoveries_panel,
    quick_actions_panel,
    discovery_timeline,
    global_search,
    filter_bar,
    select_page,
    clear_selection,
)


def render_header(info: dict[str, Any]) -> None:
    """Render the page header with application info."""
    st.markdown("""
    <style>
    .explorer-header {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95));
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="explorer-header">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 8px;">
                    <span style="font-size: 48px;">🏪</span>
                    <div>
                        <h1 style="margin: 0; font-size: 28px; color: #f8fafc;">
                            Application Explorer
                        </h1>
                        <p style="margin: 4px 0 0; font-size: 14px; color: #64748b;">
                            Digital Twin • AI-Discovered • Real-Time
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
                    v{}
                </span>
                <span style="
                    padding: 6px 14px;
                    background: rgba(16, 185, 129, 0.2);
                    border: 1px solid rgba(16, 185, 129, 0.3);
                    border-radius: 20px;
                    font-size: 12px;
                    color: #10b981;
                ">
                    {}
                </span>
            </div>
        </div>
    </div>
    """.format(info.get("version", "1.0.0"), info.get("environment", "Production")), unsafe_allow_html=True)
    
    # Stats row
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    
    with col1:
        st.metric("Pages", info.get("total_pages", 0))
    with col2:
        st.metric("Components", info.get("total_components", 0))
    with col3:
        st.metric("Forms", info.get("total_forms", 0))
    with col4:
        st.metric("APIs", info.get("total_apis", 0))
    with col5:
        coverage = info.get("coverage", 0)
        st.metric("Coverage", f"{coverage:.1f}%")
    with col6:
        risk = info.get("risk_score", 0)
        st.metric("Risk", risk)
    with col7:
        tech = info.get("technology", "Unknown")
        st.metric("Tech", tech.value if hasattr(tech, 'value') else str(tech))
    with col8:
        last_scan = info.get("last_scan", datetime.now())
        time_diff = datetime.now() - last_scan
        if time_diff < timedelta(hours=1):
            scan_str = f"{int(time_diff.total_seconds() / 60)}m ago"
        else:
            scan_str = f"{int(time_diff.total_seconds() / 3600)}h ago"
        st.metric("Last Scan", scan_str)


def render_left_sidebar() -> None:
    """Render the left sidebar with application tree."""
    with st.container():
        # Search
        search_query = st.text_input(
            "🔍 Search...",
            placeholder="Search tree...",
            label_visibility="collapsed",
            key="tree_search",
        )
        
        # Tree
        application_tree(APPLICATION_TREE, "Application Structure")
        
        st.markdown("---")
        
        # Quick Stats
        stats = generate_statistics()
        st.markdown("### 📊 Quick Stats")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Coverage", f"{stats['coverage']['overall']:.1f}%")
        with col2:
            st.metric("Risk Score", stats['risk_score'])


def render_center_workspace() -> None:
    """Render the center workspace with page gallery or workspace."""
    
    # Check if a page is selected
    if st.session_state.get("show_page_workspace") and st.session_state.get("selected_page"):
        page = st.session_state.selected_page
        page_detail = generate_page_detail(page["id"])
        
        # Back button
        if st.button("← Back to Gallery", use_container_width=True):
            clear_selection()
            st.rerun()
        
        # Page workspace
        page_workspace(page_detail)
    else:
        # View toggle
        view_tab1, view_tab2 = st.tabs(["🖼️ Page Gallery", "🗺️ Application Map"])
        
        with view_tab1:
            # Search and filter
            col1, col2 = st.columns([3, 1])
            with col1:
                search_query = st.text_input(
                    "🔍 Search pages...",
                    placeholder="Search by name or URL...",
                    label_visibility="collapsed",
                    key="gallery_search",
                )
            
            with col2:
                sort_by = st.selectbox(
                    "Sort",
                    ["Name", "Coverage", "Confidence"],
                    label_visibility="collapsed",
                )
            
            # Get pages
            pages = get_all_pages()
            
            # Apply search
            if search_query:
                pages = search_pages(search_query)
            
            # Apply sort
            if sort_by == "Coverage":
                pages = sorted(pages, key=lambda x: x.get("coverage", 0), reverse=True)
            elif sort_by == "Confidence":
                pages = sorted(pages, key=lambda x: x.get("confidence", 0), reverse=True)
            else:
                pages = sorted(pages, key=lambda x: x.get("name", ""))
            
            # Display gallery
            page_gallery(pages, f"Page Gallery ({len(pages)} pages)")
        
        with view_tab2:
            # Application map
            connections = generate_application_map()
            application_map(connections, "Navigation Flow")


def render_right_inspector() -> None:
    """Render the right inspector panel."""
    
    # Statistics
    stats = generate_statistics()
    statistics_dashboard(stats, "Statistics")
    
    st.markdown("")
    
    # AI Discoveries
    discoveries = generate_ai_discoveries()
    
    # Filter for high severity
    with st.expander("🤖 AI Discoveries", expanded=True):
        critical = [d for d in discoveries if d.get("severity") == "critical"]
        high = [d for d in discoveries if d.get("severity") == "high"]
        
        if critical:
            st.markdown("#### 🔴 Critical")
            for d in critical:
                st.markdown(f"- **{d['count']}x** {d['description']}")
        
        if high:
            st.markdown("#### 🟠 High")
            for d in high:
                st.markdown(f"- **{d['count']}x** {d['description']}")
    
    st.markdown("")
    
    # Quick Actions
    actions = generate_quick_actions()
    quick_actions_panel(actions[:6], "Quick Actions")


def render_bottom_panel() -> None:
    """Render the bottom panel with timeline and details."""
    
    st.markdown("---")
    st.markdown("### 📋 Discovery & Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Timeline
        timeline = generate_discovery_timeline()
        discovery_timeline(timeline, "Discovery Progress")
    
    with col2:
        # All AI Discoveries
        discoveries = generate_ai_discoveries()
        ai_discoveries_panel(discoveries[:5], "AI Insights")
    
    st.markdown("")
    
    # Quick Actions Grid
    actions = generate_quick_actions()
    
    st.markdown("### ⚡ All Quick Actions")
    
    # Group actions
    gen_actions = [a for a in actions if a.get("category") == "generation"]
    ai_actions = [a for a in actions if a.get("category") == "ai"]
    other_actions = [a for a in actions if a.get("category") not in ["generation", "ai"]]
    
    action_cols = st.columns(4)
    
    # Generation actions
    with action_cols[0]:
        st.markdown("**📝 Generation**")
        for action in gen_actions[:4]:
            if st.button(f"{action['icon']} {action['name']}", key=f"gen_{action['id']}", use_container_width=True):
                st.session_state[f"action_{action['id']}"] = True
    
    # AI actions
    with action_cols[1]:
        st.markdown("**🤖 AI**")
        for action in ai_actions[:4]:
            if st.button(f"{action['icon']} {action['name']}", key=f"ai_{action['id']}", use_container_width=True):
                st.session_state[f"action_{action['id']}"] = True
    
    # Explorer actions
    with action_cols[2]:
        explorer_actions = [a for a in other_actions if a.get("category") == "explorer"]
        st.markdown("**🔍 Explorer**")
        for action in explorer_actions[:4]:
            if st.button(f"{action['icon']} {action['name']}", key=f"exp_{action['id']}", use_container_width=True):
                st.session_state[f"action_{action['id']}"] = True
    
    # Other actions
    with action_cols[3]:
        other = [a for a in other_actions if a.get("category") not in ["explorer"]]
        st.markdown("**🛠️ Other**")
        for action in other[:4]:
            if st.button(f"{action['icon']} {action['name']}", key=f"oth_{action['id']}", use_container_width=True):
                st.session_state[f"action_{action['id']}"] = True


def render_page() -> None:
    """Main page render function."""
    
    # Initialize state
    init_explorer_state()
    
    # Header
    render_header(APPLICATION_INFO)
    
    # Main layout: 3 columns
    left_col, center_col, right_col = st.columns([0.25, 1, 0.35], gap="medium")
    
    # Left Sidebar
    with left_col:
        st.markdown("### 📂 Explorer")
        with st.container():
            render_left_sidebar()
    
    # Center Workspace
    with center_col:
        render_center_workspace()
    
    # Right Inspector
    with right_col:
        render_right_inspector()
    
    # Bottom Panel
    with st.container():
        render_bottom_panel()


def main() -> None:
    """Entry point."""
    render_page()


if __name__ == "__main__":
    main()
