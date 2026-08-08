"""Application Explorer - Digital Twin of the Application.

This page provides a comprehensive view of the application structure,
components, and metadata discovered by AI analysis.
"""

from typing import Any
import streamlit as st
from datetime import datetime, timedelta

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
from themes.tokens import (
    COLORS, SPACING, TYPOGRAPHY, BORDERS, SHADOWS, ANIMATIONS,
    get_health_color, get_confidence_color,
)


def render_header(info: dict[str, Any]) -> None:
    """Render the page header with application info."""
    last_scan = info.get("last_scan", datetime.now())
    time_diff = datetime.now() - last_scan
    if time_diff < timedelta(hours=1):
        scan_str = f"{int(time_diff.total_seconds() / 60)}m ago"
    else:
        scan_str = f"{int(time_diff.total_seconds() / 3600)}h ago"

    tech = info.get("technology", "Unknown")
    tech_str = tech.value if hasattr(tech, 'value') else str(tech)

    st.markdown(f"""<div style=" background: linear-gradient(135deg, rgba({COLORS.SURFACE_RGB}, 0.95), rgba({COLORS.PRIMARY_RGB}, 0.12)); border: {BORDERS.WIDTH_THIN} solid {COLORS.GLASS_BORDER}; border-radius: {BORDERS.RADIUS_XL}; padding: {SPACING.SPACE_6}; margin-bottom: {SPACING.SPACE_4}; box-sizing: border-box; max-width: 100%; "> <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:{SPACING.SPACE_4}; box-sizing:border-box; min-width:0;"> <div style="display:flex; align-items:center; gap:{SPACING.SPACE_4}; min-width:0; flex:1; flex-wrap:wrap;"> <span style="font-size:{TYPOGRAPHY.FONT_SIZE_3XL}; flex-shrink:0;">🏪</span> <div style="min-width:0;"> <h1 style="margin:0; font-size:{TYPOGRAPHY.FONT_SIZE_2XL}; color:{COLORS.TEXT_PRIMARY}; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;"> Application Explorer </h1> <p style="margin:{SPACING.SPACE_1} 0 0; font-size:{TYPOGRAPHY.FONT_SIZE_SM}; color:{COLORS.TEXT_MUTED};"> Digital Twin • AI-Discovered • Real-Time </p> </div> </div> <div style="display:flex; gap:{SPACING.SPACE_3}; flex-shrink:0; flex-wrap:wrap;"> <span style=" padding:{SPACING.SPACE_1} {SPACING.SPACE_3}; background: rgba({COLORS.PRIMARY_RGB}, 0.2); border: {BORDERS.WIDTH_THIN} solid rgba({COLORS.PRIMARY_RGB}, 0.3); border-radius: {BORDERS.RADIUS_FULL}; font-size: {TYPOGRAPHY.FONT_SIZE_XS}; color: {COLORS.PRIMARY}; white-space:nowrap; "> v{info.get("version", "1.0.0")} </span> <span style=" padding:{SPACING.SPACE_1} {SPACING.SPACE_3}; background: rgba({COLORS.SUCCESS_RGB}, 0.2); border: {BORDERS.WIDTH_THIN} solid rgba({COLORS.SUCCESS_RGB}, 0.3); border-radius: {BORDERS.RADIUS_FULL}; font-size: {TYPOGRAPHY.FONT_SIZE_XS}; color: {COLORS.SUCCESS}; white-space:nowrap; "> {info.get("environment", "Production")} </span> </div> </div> </div>""", unsafe_allow_html=True)

    # Stats row — 4 columns x 2 rows to avoid label truncation
    coverage = info.get("coverage", 0)
    risk = info.get("risk_score", 0)
    r1c1, r1c2, r1c3, r1c4 = st.columns(4)
    with r1c1:
        st.metric("Pages", info.get("total_pages", 0))
    with r1c2:
        st.metric("Components", info.get("total_components", 0))
    with r1c3:
        st.metric("Forms", info.get("total_forms", 0))
    with r1c4:
        st.metric("APIs", info.get("total_apis", 0))

    r2c1, r2c2, r2c3, r2c4 = st.columns(4)
    with r2c1:
        st.metric("Coverage", f"{coverage:.1f}%")
    with r2c2:
        st.metric("Risk", risk)
    with r2c3:
        st.metric("Tech", tech_str)
    with r2c4:
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
        if st.button("← Back to Gallery", width='stretch'):
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
            if st.button(f"{action['icon']} {action['name']}", key=f"gen_{action['id']}", width='stretch'):
                st.session_state[f"action_{action['id']}"] = True
    
    # AI actions
    with action_cols[1]:
        st.markdown("**🤖 AI**")
        for action in ai_actions[:4]:
            if st.button(f"{action['icon']} {action['name']}", key=f"ai_{action['id']}", width='stretch'):
                st.session_state[f"action_{action['id']}"] = True
    
    # Explorer actions
    with action_cols[2]:
        explorer_actions = [a for a in other_actions if a.get("category") == "explorer"]
        st.markdown("**🔍 Explorer**")
        for action in explorer_actions[:4]:
            if st.button(f"{action['icon']} {action['name']}", key=f"exp_{action['id']}", width='stretch'):
                st.session_state[f"action_{action['id']}"] = True
    
    # Other actions
    with action_cols[3]:
        other = [a for a in other_actions if a.get("category") not in ["explorer"]]
        st.markdown("**🛠️ Other**")
        for action in other[:4]:
            if st.button(f"{action['icon']} {action['name']}", key=f"oth_{action['id']}", width='stretch'):
                st.session_state[f"action_{action['id']}"] = True


def render_page() -> None:
    """Main page render function."""

    # Initialize state
    init_explorer_state()

    # Global layout-stabilization CSS for the explorer page
    st.markdown("""<style> /* Prevent horizontal page overflow; make all flex/grid children respect parent width */ [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"], .stMainBlockContainer { max-width: 100%; overflow-x: hidden; } .stColumn { min-width: 0; } .stMetric { min-width: 0; } .stMetric label { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; } [data-testid="stMetricValue"] { white-space: nowrap; } /* Ensure all explorer markdown containers don't overflow */ .stMarkdown div, .stMarkdown span { max-width: 100%; } </style>""", unsafe_allow_html=True)

    # Header
    render_header(APPLICATION_INFO)
    
    # Main layout: 3 columns — balanced ratios for tree / gallery / inspector
    left_col, center_col, right_col = st.columns([2.6, 6.2, 3.2], gap="medium")
    
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
