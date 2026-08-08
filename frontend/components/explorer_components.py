"""Application Explorer Components for AI-QOS - Digital Twin Visualization."""

from datetime import datetime, timedelta
from typing import Any, Callable, Optional
import streamlit as st
import plotly.graph_objects as go

from themes.tokens import (
    COLORS, SPACING, TYPOGRAPHY, BORDERS, SHADOWS, ANIMATIONS,
    get_health_color, get_confidence_color, get_status_color, get_priority_color,
)


# ============================================================================
# Layout / styling helpers (token-driven, no hardcoded colors)
# ============================================================================

def _hex_to_rgb(hex_color: str) -> str:
    """Convert a hex color to an 'r, g, b' string for rgba() usage."""
    h = hex_color.lstrip('#')
    return f"{int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}"


def _coverage_color(coverage: float) -> str:
    """Semantic coverage color from a 0-100 value."""
    if coverage >= 80:
        return COLORS.SUCCESS
    if coverage >= 50:
        return COLORS.WARNING
    return COLORS.ERROR


def _risk_color(risk: str) -> str:
    return {"Low": COLORS.SUCCESS, "Medium": COLORS.WARNING,
            "High": COLORS.ERROR, "Critical": COLORS.ERROR}.get(risk, COLORS.TEXT_MUTED)


def _severity_color(severity: str) -> str:
    return {"critical": COLORS.ERROR, "high": COLORS.WARNING,
            "medium": COLORS.INFO, "low": COLORS.TEXT_MUTED,
            "info": COLORS.INFO}.get(severity, COLORS.TEXT_MUTED)


def _escape(text: Any) -> str:
    """Escape text for safe HTML rendering."""
    if text is None:
        return ""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ============================================================================
# Session State Management
# ============================================================================

def init_explorer_state() -> None:
    """Initialize explorer session state."""
    defaults = {
        "selected_page": None,
        "expanded_nodes": set(),
        "search_query": "",
        "filter_category": "all",
        "inspector_tab": "overview",
        "show_page_workspace": False,
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def toggle_node_expansion(node_id: str) -> None:
    """Toggle tree node expansion."""
    if node_id in st.session_state.expanded_nodes:
        st.session_state.expanded_nodes.discard(node_id)
    else:
        st.session_state.expanded_nodes.add(node_id)


def select_page(page: dict[str, Any]) -> None:
    """Select a page for inspection."""
    st.session_state.selected_page = page
    st.session_state.show_page_workspace = True


def clear_selection() -> None:
    """Clear page selection."""
    st.session_state.selected_page = None
    st.session_state.show_page_workspace = False


# ============================================================================
# Application Tree Component
# ============================================================================

def render_tree_node(
    node: dict[str, Any],
    level: int = 0,
    parent_expanded: bool = True
) -> None:
    """Render a single tree node recursively."""
    node_id = node["id"]
    is_expanded = node_id in st.session_state.expanded_nodes
    has_children = bool(node.get("children"))

    # Coverage / confidence colors (token-driven)
    coverage = node.get("coverage", 0)
    cov_color = _coverage_color(coverage)
    confidence = node.get("confidence", 0)

    # Node type icons
    type_icons = {"application": "🏪", "module": "📁", "page": "📄"}
    icon = type_icons.get(node.get("type", "page"), "📄")

    # Indentation via CSS padding-left (no Unicode full-width spaces)
    indent_px = level * 16

    # Expand/collapse glyph
    expand_glyph = "▼" if (has_children and is_expanded) else "▶" if has_children else "•"

    # Single stable HTML flex row: [glyph][icon][name flex:1 truncate][coverage badge][confidence badge]
    st.markdown(f"""<div style=" display:flex; align-items:center; gap:{SPACING.SPACE_2}; padding:{SPACING.SPACE_1} {SPACING.SPACE_2}; padding-left:{indent_px}px; background:rgba({COLORS.SURFACE_RGB}, 0.4); border-radius:{BORDERS.RADIUS_SM}; margin-bottom:{SPACING.SPACE_1}; box-sizing:border-box; min-width:0; max-width:100%; "> <span style="flex-shrink:0; font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_MUTED}; width:14px; text-align:center;">{expand_glyph}</span> <span style="flex-shrink:0; font-size:{TYPOGRAPHY.FONT_SIZE_BASE};">{icon}</span> <span style=" flex:1; min-width:0; color:{COLORS.TEXT_PRIMARY}; font-size:{TYPOGRAPHY.FONT_SIZE_SM}; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; ">{_escape(node['name'])}</span> <span style=" flex-shrink:0; padding:2px {SPACING.SPACE_2}; background:rgba({_hex_to_rgb(cov_color)}, 0.15); border:{BORDERS.WIDTH_THIN} solid rgba({_hex_to_rgb(cov_color)}, 0.4); border-radius:{BORDERS.RADIUS_SM}; font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{cov_color}; white-space:nowrap; ">{coverage:.0f}%</span> <span style=" flex-shrink:0; padding:2px {SPACING.SPACE_2}; background:rgba({COLORS.PRIMARY_RGB}, 0.15); border:{BORDERS.WIDTH_THIN} solid rgba({COLORS.PRIMARY_RGB}, 0.3); border-radius:{BORDERS.RADIUS_SM}; font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.PRIMARY}; white-space:nowrap; ">{confidence:.0f}%</span> </div>""", unsafe_allow_html=True)

    # Interaction button (full-width, stable height) — separate from the visual row
    button_label = f"{expand_glyph} {icon} {node['name']}"
    if st.button(button_label, key=f"tree_{node_id}", width='stretch'):
        if has_children:
            toggle_node_expansion(node_id)
        else:
            select_page(node)
        st.rerun()

    # Render children if expanded
    if has_children and is_expanded:
        for child in node.get("children", []):
            render_tree_node(child, level + 1, is_expanded)


def application_tree(tree_data: dict[str, Any], title: str = "Application Tree") -> None:
    """Render the full application tree."""
    st.markdown(f"### 📂 {title}")
    
    # Expand root by default
    if "app_root" not in st.session_state.expanded_nodes:
        st.session_state.expanded_nodes.add("app_root")
    
    # Expand all modules by default
    for child in tree_data.get("children", []):
        if child["id"] not in st.session_state.expanded_nodes:
            st.session_state.expanded_nodes.add(child["id"])
    
    # Render tree
    render_tree_node(tree_data)
    
    # Summary stats
    _render_tree_summary(tree_data)


def _render_tree_summary(tree: dict[str, Any]) -> None:
    """Render tree summary statistics."""
    pages = []
    modules = []
    
    def count_nodes(node: dict[str, Any]) -> None:
        if node.get("type") == "page":
            pages.append(node)
        elif node.get("type") == "module":
            modules.append(node)
        for child in node.get("children", []):
            count_nodes(child)
    
    count_nodes(tree)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Modules", len(modules))
    with col2:
        st.metric("Pages", len(pages))
    with col3:
        avg_coverage = sum(p.get("coverage", 0) for p in pages) / max(1, len(pages))
        st.metric("Avg Coverage", f"{avg_coverage:.1f}%")


# ============================================================================
# Page Card Component
# ============================================================================

def page_card(page: dict[str, Any], columns: int = 3) -> None:
    """Render a page as a card."""
    with st.container():
        coverage = page.get("coverage", 0)
        risk = page.get("risk", "Low")
        cov_color = _coverage_color(coverage)
        risk_color = _risk_color(risk)
        cov_rgb = _hex_to_rgb(cov_color)
        risk_rgb = _hex_to_rgb(risk_color)
        icon = page.get('icon', '📄')
        name = _escape(page['name'])
        url = _escape(page.get('url', '/'))
        conf = page.get('confidence', 0)

        # Single-line HTML to prevent Streamlit code-block rendering of indented markup
        st.markdown(
            f'<div style="height:120px;background:linear-gradient(135deg,rgba({COLORS.PRIMARY_RGB},0.1),rgba({COLORS.SECONDARY_RGB},0.1));border:{BORDERS.WIDTH_THIN} solid rgba({COLORS.BORDER_RGB},0.2);border-radius:{BORDERS.RADIUS_LG} {BORDERS.RADIUS_LG} 0 0;display:flex;align-items:center;justify-content:center;font-size:{TYPOGRAPHY.FONT_SIZE_3XL};box-sizing:border-box;overflow:hidden;">{icon}</div>'
            f'<div style="padding:{SPACING.SPACE_4};background:{COLORS.GLASS_LIGHT};border:{BORDERS.WIDTH_THIN} solid rgba({COLORS.BORDER_RGB},0.15);border-top:none;border-radius:0 0 {BORDERS.RADIUS_LG} {BORDERS.RADIUS_LG};box-sizing:border-box;min-width:0;max-width:100%;overflow:hidden;">'
            f'<h4 style="margin:0 0 {SPACING.SPACE_2};color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_BASE};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{name}</h4>'
            f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};margin-bottom:{SPACING.SPACE_3};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-family:{TYPOGRAPHY.FONT_MONO};">{url}</div>'
            f'<div style="display:flex;gap:{SPACING.SPACE_2};margin-bottom:{SPACING.SPACE_3};flex-wrap:wrap;min-width:0;">'
            f'<span style="padding:2px {SPACING.SPACE_2};background:rgba({cov_rgb},0.15);border-radius:{BORDERS.RADIUS_SM};font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{cov_color};white-space:nowrap;">{coverage:.0f}% Covered</span>'
            f'<span style="padding:2px {SPACING.SPACE_2};background:rgba({risk_rgb},0.15);border-radius:{BORDERS.RADIUS_SM};font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{risk_color};white-space:nowrap;">{risk} Risk</span>'
            f'</div>'
            f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.PRIMARY};font-family:{TYPOGRAPHY.FONT_MONO};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">Confidence: {conf:.0f}%</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Action button — stable full width
        if st.button("Inspect →", key=f"inspect_{page['id']}", width='stretch'):
            select_page(page)
            st.rerun()


def page_gallery(pages: list[dict[str, Any]], title: str = "Page Gallery") -> None:
    """Render a gallery of page cards."""
    st.markdown(f"### 🖼️ {title}")
    
    if not pages:
        st.info("No pages match your search criteria.")
        return
    
    # Display in grid
    cols = st.columns(3)
    for i, page in enumerate(pages):
        with cols[i % 3]:
            page_card(page)


# ============================================================================
# Page Workspace Component
# ============================================================================

def page_workspace(page: dict[str, Any]) -> None:
    """Render detailed page workspace."""
    st.markdown(f"""<div style=" padding: {SPACING.SPACE_6}; background: {COLORS.GLASS_LIGHT}; border: {BORDERS.WIDTH_THIN} solid rgba({COLORS.BORDER_RGB}, 0.15); border-radius: {BORDERS.RADIUS_LG}; margin-bottom: {SPACING.SPACE_6}; box-sizing: border-box; min-width:0; max-width:100%; "> <div style="display: flex; align-items: center; gap: {SPACING.SPACE_4}; min-width:0; flex-wrap:wrap;"> <span style="font-size:{TYPOGRAPHY.FONT_SIZE_3XL}; flex-shrink:0;">{page.get('icon', '📄')}</span> <div style="min-width:0; flex:1;"> <h2 style="margin: 0; color: {COLORS.TEXT_PRIMARY}; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{_escape(page['name'])}</h2> <div style="font-size: {TYPOGRAPHY.FONT_SIZE_SM}; color: {COLORS.TEXT_MUTED}; margin-top: {SPACING.SPACE_1}; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;"> {_escape(page.get('url', '/'))} • {_escape(page.get('framework', 'React'))} </div> </div> </div> </div>""", unsafe_allow_html=True)

    # Component metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Components", page.get("components", 0))
    with col2:
        st.metric("Forms", page.get("forms", 0))
    with col3:
        st.metric("Buttons", page.get("buttons", 0))
    with col4:
        st.metric("Coverage", f"{page.get('coverage', 0):.1f}%")

    st.markdown("---")

    # Detailed sections
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Components", "Rules", "Issues"])

    with tab1:
        _render_page_overview(page)

    with tab2:
        _render_page_components(page)

    with tab3:
        _render_page_rules(page)

    with tab4:
        _render_page_issues(page)


def _render_page_overview(page: dict[str, Any]) -> None:
    """Render page overview."""
    st.markdown("#### 📊 Scores")

    col1, col2, col3 = st.columns(3)
    with col1:
        acc_score = page.get("accessibility_score", 0)
        acc_color = COLORS.SUCCESS if acc_score >= 90 else COLORS.WARNING if acc_score >= 70 else COLORS.ERROR
        st.markdown(f"""<div style="padding:{SPACING.SPACE_4}; background:{COLORS.GLASS_LIGHT}; border-radius:{BORDERS.RADIUS_LG}; text-align:center; box-sizing:border-box; min-width:0;"> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_3XL}; font-weight:700; color:{acc_color};">{acc_score:.0f}</div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_MUTED}; text-transform:uppercase;">Accessibility</div> </div>""", unsafe_allow_html=True)

    with col2:
        perf_score = page.get("performance_score", 0)
        perf_color = COLORS.SUCCESS if perf_score >= 80 else COLORS.WARNING if perf_score >= 60 else COLORS.ERROR
        st.markdown(f"""<div style="padding:{SPACING.SPACE_4}; background:{COLORS.GLASS_LIGHT}; border-radius:{BORDERS.RADIUS_LG}; text-align:center; box-sizing:border-box; min-width:0;"> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_3XL}; font-weight:700; color:{perf_color};">{perf_score:.0f}</div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_MUTED}; text-transform:uppercase;">Performance</div> </div>""", unsafe_allow_html=True)

    with col3:
        sec_score = page.get("security_score", 0)
        sec_color = COLORS.SUCCESS if sec_score >= 85 else COLORS.WARNING if sec_score >= 70 else COLORS.ERROR
        st.markdown(f"""<div style="padding:{SPACING.SPACE_4}; background:{COLORS.GLASS_LIGHT}; border-radius:{BORDERS.RADIUS_LG}; text-align:center; box-sizing:border-box; min-width:0;"> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_3XL}; font-weight:700; color:{sec_color};">{sec_score:.0f}</div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_MUTED}; text-transform:uppercase;">Security</div> </div>""", unsafe_allow_html=True)

    st.markdown("#### 💡 AI Summary")
    st.markdown(f"""<div style=" padding:{SPACING.SPACE_4}; background: linear-gradient(135deg, rgba({COLORS.PRIMARY_RGB}, 0.1), rgba({COLORS.SECONDARY_RGB}, 0.1)); border: {BORDERS.WIDTH_THIN} solid rgba({COLORS.PRIMARY_RGB}, 0.2); border-radius: {BORDERS.RADIUS_LG}; font-size: {TYPOGRAPHY.FONT_SIZE_SM}; line-height: 1.6; color: {COLORS.TEXT_SECONDARY}; box-sizing:border-box; min-width:0; max-width:100%; overflow-wrap:anywhere; word-break:normal; "> {_escape(page.get('ai_summary', 'No summary available.'))} </div>""", unsafe_allow_html=True)

    # AI Explanation
    st.markdown("#### 🎯 AI Explanation")
    explanation = page.get('why_discovered', 'Discovered through automated analysis.')
    importance = page.get('business_importance', 'Medium')
    complexity = page.get('automation_complexity', 'Moderate')

    st.markdown(f"""<div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:{SPACING.SPACE_3}; box-sizing:border-box; min-width:0; max-width:100%;"> <div style="padding:{SPACING.SPACE_3}; background:{COLORS.GLASS_LIGHT}; border-radius:{BORDERS.RADIUS_MD}; min-width:0; overflow:hidden;"> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_MUTED}; text-transform:uppercase;">Why Discovered</div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM}; color:{COLORS.TEXT_PRIMARY}; margin-top:{SPACING.SPACE_1}; overflow-wrap:anywhere;">{_escape(explanation)}</div> </div> <div style="padding:{SPACING.SPACE_3}; background:{COLORS.GLASS_LIGHT}; border-radius:{BORDERS.RADIUS_MD}; min-width:0; overflow:hidden;"> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_MUTED}; text-transform:uppercase;">Business Importance</div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM}; color:{COLORS.TEXT_PRIMARY}; margin-top:{SPACING.SPACE_1}; overflow-wrap:anywhere;">{_escape(importance)}</div> </div> <div style="padding:{SPACING.SPACE_3}; background:{COLORS.GLASS_LIGHT}; border-radius:{BORDERS.RADIUS_MD}; min-width:0; overflow:hidden;"> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_MUTED}; text-transform:uppercase;">Automation Complexity</div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM}; color:{COLORS.TEXT_PRIMARY}; margin-top:{SPACING.SPACE_1}; overflow-wrap:anywhere;">{_escape(complexity)}</div> </div> </div>""", unsafe_allow_html=True)


def _render_page_components(page: dict[str, Any]) -> None:
    """Render page components list."""
    components = page.get("components_detail", [])

    if not components:
        st.info("No component details available.")
        return

    for comp in components:
        comp_type = comp.get("type", {}).value if hasattr(comp.get("type", {}), 'value') else str(comp.get("type", "Unknown"))

        status_icons = "✅" if comp.get("automation_ready", False) else "⚠️"
        flaky_indicator = " (Flaky!)" if comp.get("is_flaky", False) else ""

        st.markdown(f"""<div style=" padding:{SPACING.SPACE_3}; background:{COLORS.GLASS_LIGHT}; border:{BORDERS.WIDTH_THIN} solid rgba({COLORS.BORDER_RGB}, 0.15); border-radius:{BORDERS.RADIUS_MD}; margin-bottom:{SPACING.SPACE_2}; box-sizing:border-box; min-width:0; max-width:100%; "> <div style="display:flex; justify-content:space-between; align-items:center; gap:{SPACING.SPACE_2}; min-width:0;"> <div style="min-width:0; overflow:hidden;"> <span style="font-size:{TYPOGRAPHY.FONT_SIZE_SM}; color:{COLORS.TEXT_PRIMARY}; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{_escape(comp['name'])}</span> <span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_MUTED}; margin-left:{SPACING.SPACE_2};">{_escape(comp_type)}{_escape(flaky_indicator)}</span> </div> <div style="display:flex; gap:{SPACING.SPACE_3}; flex-shrink:0; align-items:center;"> {status_icons} <span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.PRIMARY}; white-space:nowrap;"> Test ID: {_escape(str(comp.get('test_id', 'N/A')))} </span> </div> </div> </div>""", unsafe_allow_html=True)


def _render_page_rules(page: dict[str, Any]) -> None:
    """Render page business rules."""
    rules = page.get("business_rules_detail", [])

    if not rules:
        st.info("No business rules available.")
        return

    complexity_colors = {"Low": COLORS.SUCCESS, "Medium": COLORS.WARNING, "High": COLORS.ERROR}

    for rule in rules:
        color = complexity_colors.get(rule.get("complexity", "Low"), COLORS.TEXT_MUTED)
        st.markdown(f"""<div style=" padding:{SPACING.SPACE_4}; background:{COLORS.GLASS_LIGHT}; border-left:3px solid {color}; border-radius:0 {BORDERS.RADIUS_MD} {BORDERS.RADIUS_MD} 0; margin-bottom:{SPACING.SPACE_3}; box-sizing:border-box; min-width:0; max-width:100%; "> <div style="display:flex; justify-content:space-between; gap:{SPACING.SPACE_2}; min-width:0;"> <span style="font-size:{TYPOGRAPHY.FONT_SIZE_SM}; color:{COLORS.TEXT_PRIMARY}; font-weight:500; overflow-wrap:anywhere; min-width:0;"> {_escape(rule['name'])} </span> <span style=" flex-shrink:0; padding:2px {SPACING.SPACE_2}; background:rgba({_hex_to_rgb(color)}, 0.15); border-radius:{BORDERS.RADIUS_SM}; font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{color}; white-space:nowrap; "> {_escape(rule.get('complexity', 'Low'))} </span> </div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_SECONDARY}; margin-top:{SPACING.SPACE_2}; overflow-wrap:anywhere; word-break:normal;"> {_escape(rule.get('description', ''))} </div> </div>""", unsafe_allow_html=True)


def _render_page_issues(page: dict[str, Any]) -> None:
    """Render page issues."""
    # Accessibility
    st.markdown("#### ♿ Accessibility Issues")
    acc_issues = page.get("accessibility_issues", [])
    for issue in acc_issues:
        color = _severity_color(issue.get("severity", "low"))
        st.markdown(f"""<div style="padding:{SPACING.SPACE_3}; background:rgba({COLORS.ERROR_RGB}, 0.1); border-left:3px solid {color}; border-radius:0 {BORDERS.RADIUS_SM} {BORDERS.RADIUS_SM} 0; margin-bottom:{SPACING.SPACE_2}; box-sizing:border-box; min-width:0; overflow-wrap:anywhere; word-break:normal;"> <span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_PRIMARY};">{_escape(issue.get('issue', ''))}</span> <span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_MUTED}; margin-left:{SPACING.SPACE_2};">{_escape(issue.get('element', ''))}</span> </div>""", unsafe_allow_html=True)

    # Performance
    st.markdown("#### ⚡ Performance Issues")
    perf_issues = page.get("performance_issues", [])
    for issue in perf_issues:
        color = COLORS.WARNING if issue.get("severity") == "medium" else COLORS.ERROR
        st.markdown(f"""<div style="padding:{SPACING.SPACE_3}; background:rgba({COLORS.WARNING_RGB}, 0.1); border-left:3px solid {color}; border-radius:0 {BORDERS.RADIUS_SM} {BORDERS.RADIUS_SM} 0; margin-bottom:{SPACING.SPACE_2}; box-sizing:border-box; min-width:0; overflow-wrap:anywhere; word-break:normal;"> <span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_PRIMARY};">{_escape(issue.get('issue', ''))}</span> <span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_SECONDARY}; margin-left:{SPACING.SPACE_2};">{_escape(issue.get('impact', ''))}</span> </div>""", unsafe_allow_html=True)

    # Security
    st.markdown("#### 🔒 Security Warnings")
    sec_warnings = page.get("security_warnings", [])
    for warning in sec_warnings:
        color = COLORS.ERROR if warning.get("severity") == "critical" else COLORS.WARNING
        st.markdown(f"""<div style="padding:{SPACING.SPACE_3}; background:rgba({COLORS.ERROR_RGB}, 0.1); border-left:3px solid {color}; border-radius:0 {BORDERS.RADIUS_SM} {BORDERS.RADIUS_SM} 0; margin-bottom:{SPACING.SPACE_2}; box-sizing:border-box; min-width:0; overflow-wrap:anywhere; word-break:normal;"> <span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_PRIMARY};">{_escape(warning.get('warning', ''))}</span> <span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_MUTED}; margin-left:{SPACING.SPACE_2};">{_escape(warning.get('location', ''))}</span> </div>""", unsafe_allow_html=True)


# ============================================================================
# Application Map Component
# ============================================================================

def application_map(connections: list[dict[str, Any]], title: str = "Application Map") -> None:
    """Render application navigation map as a graph."""
    st.markdown(f"### 🗺️ {title}")
    
    # Create nodes
    nodes = list(set([c["from"] for c in connections] + [c["to"] for c in connections]))
    node_positions = {node: (i % 4, i // 4) for i, node in enumerate(nodes)}
    
    # Create figure
    fig = go.Figure()
    
    # Add edges
    for conn in connections:
        x0, y0 = node_positions[conn["from"]]
        x1, y1 = node_positions[conn["to"]]
        
        type_colors = {
            "navigation": COLORS.PRIMARY,
            "action": COLORS.SECONDARY,
            "auth": COLORS.WARNING,
            "direct": COLORS.SUCCESS,
        }
        color = type_colors.get(conn.get("type", "navigation"), COLORS.PRIMARY)
        
        fig.add_trace(go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            mode='lines',
            line=dict(color=color, width=2),
            hoverinfo='text',
            text=f"{conn['from']} → {conn['to']}",
            showlegend=False,
        ))
    
    # Add nodes
    for node, (x, y) in node_positions.items():
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode='markers+text',
            marker=dict(size=30, color=COLORS.PRIMARY, line=dict(color=COLORS.TEXT_PRIMARY, width=2)),
            text=[node],
            textposition='middle center',
            textfont=dict(size=10, color=COLORS.TEXT_PRIMARY),
            hovertemplate=f"<b>{node}</b><extra></extra>",
            showlegend=False,
        ))
    
    fig.update_layout(
        height=300,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 3.5]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 3.5]),
    )
    
    st.plotly_chart(fig, width='stretch', key="app_map_chart")
    
    # Legend
    st.markdown(f"""<div style="display:flex; gap:{SPACING.SPACE_4}; justify-content:center; margin-top:{SPACING.SPACE_3}; flex-wrap:wrap; box-sizing:border-box; min-width:0;"> <span style="display:flex; align-items:center; gap:{SPACING.SPACE_2};"> <span style="width:20px; height:3px; background:{COLORS.PRIMARY}; border-radius:2px; flex-shrink:0;"></span> <span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_SECONDARY}; white-space:nowrap;">Navigation</span> </span> <span style="display:flex; align-items:center; gap:{SPACING.SPACE_2};"> <span style="width:20px; height:3px; background:{COLORS.SECONDARY}; border-radius:2px; flex-shrink:0;"></span> <span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_SECONDARY}; white-space:nowrap;">Action</span> </span> <span style="display:flex; align-items:center; gap:{SPACING.SPACE_2};"> <span style="width:20px; height:3px; background:{COLORS.WARNING}; border-radius:2px; flex-shrink:0;"></span> <span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_SECONDARY}; white-space:nowrap;">Auth</span> </span> </div>""", unsafe_allow_html=True)


# ============================================================================
# Statistics Dashboard Component
# ============================================================================

def statistics_dashboard(stats: dict[str, Any], title: str = "Statistics") -> None:
    """Render statistics dashboard."""
    st.markdown(f"### 📊 {title}")
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        pages = stats.get("pages", {})
        st.metric("Pages", pages.get("total", 0), f"{pages.get('discovered', 0)} discovered")
    
    with col2:
        components = stats.get("components", {})
        st.metric("Components", components.get("total", 0))
    
    with col3:
        forms = stats.get("forms", {})
        st.metric("Forms", forms.get("total", 0), f"{forms.get('validated', 0)} validated")
    
    with col4:
        apis = stats.get("apis", {})
        st.metric("APIs", apis.get("total", 0), f"{apis.get('documented', 0)} documented")
    
    st.markdown("---")
    
    # Coverage
    coverage = stats.get("coverage", {})
    st.markdown("#### Coverage")
    
    coverage_col1, coverage_col2, coverage_col3 = st.columns(3)
    with coverage_col1:
        ui_cov = coverage.get("ui_coverage", 0)
        st.markdown(f"""<div style="padding:{SPACING.SPACE_4}; background:{COLORS.GLASS_LIGHT}; border-radius:{BORDERS.RADIUS_LG}; text-align:center; box-sizing:border-box; min-width:0;"> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_3XL}; font-weight:700; color:{COLORS.PRIMARY};">{ui_cov:.1f}%</div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_MUTED}; text-transform:uppercase;">UI Coverage</div> </div>""", unsafe_allow_html=True)

    with coverage_col2:
        api_cov = coverage.get("api_coverage", 0)
        st.markdown(f"""<div style="padding:{SPACING.SPACE_4}; background:{COLORS.GLASS_LIGHT}; border-radius:{BORDERS.RADIUS_LG}; text-align:center; box-sizing:border-box; min-width:0;"> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_3XL}; font-weight:700; color:{COLORS.SECONDARY};">{api_cov:.1f}%</div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_MUTED}; text-transform:uppercase;">API Coverage</div> </div>""", unsafe_allow_html=True)

    with coverage_col3:
        overall = coverage.get("overall", 0)
        st.markdown(f"""<div style="padding:{SPACING.SPACE_4}; background:{COLORS.GLASS_LIGHT}; border-radius:{BORDERS.RADIUS_LG}; text-align:center; box-sizing:border-box; min-width:0;"> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_3XL}; font-weight:700; color:{COLORS.SUCCESS};">{overall:.1f}%</div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_MUTED}; text-transform:uppercase;">Overall</div> </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Additional stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Risk Score", stats.get("risk_score", 0))
    with col2:
        st.metric("Automation Ready", f"{stats.get('automation_ready', 0):.1f}%")


# ============================================================================
# AI Discoveries Panel Component
# ============================================================================

def ai_discoveries_panel(discoveries: list[dict[str, Any]], title: str = "AI Discoveries") -> None:
    """Render AI discoveries panel."""
    st.markdown(f"### 🤖 {title}")
    
    # Summary badges
    col1, col2, col3 = st.columns(3)
    
    critical_count = sum(1 for d in discoveries if d.get("severity") == "critical")
    high_count = sum(1 for d in discoveries if d.get("severity") == "high")
    total_issues = sum(d.get("count", 0) for d in discoveries)
    
    with col1:
        st.metric("Critical", critical_count)
    with col2:
        st.metric("High", high_count)
    with col3:
        st.metric("Total Issues", total_issues)
    
    st.markdown("---")
    
    # Discovery cards
    type_icons = {
        "duplicate_ids": "🔄",
        "missing_labels": "🏷️",
        "accessibility": "♿",
        "performance": "⚡",
        "security": "🔒",
        "automation_risk": "⚠️",
        "missing_test_ids": "🔍",
        "dynamic_elements": "🔀",
        "suggestions": "💡",
    }
    
    severity_colors = {
        "critical": COLORS.ERROR,
        "high": COLORS.WARNING,
        "medium": COLORS.INFO,
        "low": COLORS.TEXT_MUTED,
        "info": COLORS.SECONDARY,
    }
    
    for discovery in discoveries:
        icon = type_icons.get(discovery.get("type", ""), "📋")
        color = severity_colors.get(discovery.get("severity", "info"), COLORS.TEXT_MUTED)

        st.markdown(f"""<div style=" padding:{SPACING.SPACE_4}; background:{COLORS.GLASS_LIGHT}; border:{BORDERS.WIDTH_THIN} solid {color}30; border-radius:{BORDERS.RADIUS_MD}; margin-bottom:{SPACING.SPACE_3}; box-sizing:border-box; min-width:0; max-width:100%; "> <div style="display:flex; justify-content:space-between; align-items:center; gap:{SPACING.SPACE_3}; min-width:0;"> <div style="display:flex; align-items:center; gap:{SPACING.SPACE_3}; min-width:0;"> <span style="font-size:{TYPOGRAPHY.FONT_SIZE_3XL}; flex-shrink:0;">{icon}</span> <div style="min-width:0; overflow:hidden;"> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM}; color:{COLORS.TEXT_PRIMARY}; font-weight:500; overflow-wrap:anywhere;"> {_escape(discovery.get('type', 'Unknown').replace('_', ' ').title())} </div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_SECONDARY}; overflow-wrap:anywhere; word-break:normal;"> {_escape(discovery.get('description', ''))} </div> </div> </div> <div style=" flex-shrink:0; padding:{SPACING.SPACE_2} {SPACING.SPACE_3}; background:{color}20; border-radius:{BORDERS.RADIUS_SM}; font-size:{TYPOGRAPHY.FONT_SIZE_2XL}; font-weight:700; color:{color}; white-space:nowrap; "> {discovery.get('count', 0)} </div> </div> </div>""", unsafe_allow_html=True)


# ============================================================================
# Quick Actions Panel Component
# ============================================================================

def quick_actions_panel(actions: list[dict[str, Any]], title: str = "Quick Actions") -> None:
    """Render quick actions panel."""
    st.markdown(f"### ⚡ {title}")
    
    # Group by category
    categories = {}
    for action in actions:
        cat = action.get("category", "other")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(action)
    
    category_names = {
        "explorer": "🔍 Explorer",
        "generation": "📝 Generation",
        "ai": "🤖 AI",
        "browser": "🌐 Browser",
        "analysis": "📊 Analysis",
    }
    
    for cat_name, cat_actions in categories.items():
        st.markdown(f"**{category_names.get(cat_name, cat_name)}**")
        
        cols = st.columns(3)
        for i, action in enumerate(cat_actions):
            with cols[i % 3]:
                if st.button(
                    f"{action['icon']} {action['name']}",
                    key=f"action_{action['id']}",
                    width='stretch',
                ):
                    st.info(f"Action: {action['name']}")
                    st.rerun()
        
        st.markdown("")


# ============================================================================
# Discovery Timeline Component
# ============================================================================

def discovery_timeline(timeline: list[dict[str, Any]], title: str = "Discovery Timeline") -> None:
    """Render discovery timeline."""
    st.markdown(f"### 📅 {title}")
    
    status_colors = {
        "completed": COLORS.SUCCESS,
        "in_progress": COLORS.WARNING,
        "pending": COLORS.TEXT_MUTED,
    }
    
    for i, item in enumerate(timeline):
        color = status_colors.get(item.get("status", "pending"), COLORS.TEXT_MUTED)
        is_last = i == len(timeline) - 1
        
        # Time formatting
        time_diff = datetime.now() - item.get("time", datetime.now())
        if time_diff < timedelta(hours=1):
            time_str = f"{int(time_diff.total_seconds() / 60)}m ago"
        elif time_diff < timedelta(days=1):
            time_str = f"{int(time_diff.total_seconds() / 3600)}h ago"
        else:
            time_str = f"{int(time_diff.days)}d ago"
        
        st.markdown(f"""<div style="display:flex; gap:{SPACING.SPACE_4}; margin-bottom:{0 if is_last else 16}px; min-width:0; box-sizing:border-box;"> <div style="display:flex; flex-direction:column; align-items:center; flex-shrink:0;"> <div style=" width:16px; height:16px; border-radius:50%; background:{color}; box-shadow:0 0 10px {color}50; flex-shrink:0; "></div> {"<div style='width:2px; flex:1; background:linear-gradient(180deg, " + color + ", transparent);'></div>" if not is_last else ""} </div> <div style="flex:1; padding-bottom:{16 if not is_last else 0}px; min-width:0; overflow:hidden;"> <div style="display:flex; justify-content:space-between; align-items:center; gap:{SPACING.SPACE_2}; min-width:0;"> <span style="font-size:{TYPOGRAPHY.FONT_SIZE_SM}; color:{COLORS.TEXT_PRIMARY}; font-weight:500; overflow-wrap:anywhere; min-width:0;"> Step {item['step']}: {_escape(item['name'])} </span> <span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_MUTED}; white-space:nowrap; flex-shrink:0;">{time_str}</span> </div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{COLORS.TEXT_SECONDARY}; margin-top:4px; overflow-wrap:anywhere; word-break:normal;"> {_escape(item.get('details', ''))} </div> </div> </div>""", unsafe_allow_html=True)


# ============================================================================
# Inspector Tabs Component
# ============================================================================

def inspector_tabs(
    page: dict[str, Any],
    active_tab: str = "overview"
) -> str:
    """Render inspector tabs and return selected tab."""
    
    tabs = [
        ("overview", "📋 Overview"),
        ("forms", "📝 Forms"),
        ("buttons", "🔘 Buttons"),
        ("inputs", "📝 Inputs"),
        ("tables", "📊 Tables"),
        ("rules", "📜 Rules"),
        ("accessibility", "♿ Accessibility"),
        ("notes", "📝 Notes"),
    ]
    
    tab_labels = [t[1] for t in tabs]
    tab_keys = [t[0] for t in tabs]
    
    if active_tab not in tab_keys:
        active_tab = "overview"
    
    selected = st.radio(
        "Inspector",
        tab_labels,
        index=tab_keys.index(active_tab),
        horizontal=True,
        label_visibility="collapsed",
    )
    
    return tab_keys[tab_labels.index(selected)]


# ============================================================================
# Search Component
# ============================================================================

def global_search(
    pages: list[dict[str, Any]],
    on_search: Callable[[str], None]
) -> str:
    """Render global search input."""
    query = st.text_input(
        "🔍 Search pages, forms, components...",
        value=st.session_state.get("search_query", ""),
        placeholder="Search by name, URL, or component...",
        label_visibility="collapsed",
        key="explorer_search",
    )
    
    if query != st.session_state.get("search_query", ""):
        st.session_state.search_query = query
        on_search(query)
    
    return query


def filter_bar(
    categories: list[str],
    selected: str,
    on_change: Callable[[str], None]
) -> str:
    """Render filter bar."""
    
    cols = st.columns([1] + [1] * (len(categories) - 1) + [1])
    
    with cols[0]:
        selected = st.selectbox(
            "Filter",
            categories,
            index=categories.index(selected) if selected in categories else 0,
            label_visibility="collapsed",
        )
    
    with cols[-1]:
        if st.button("🔄 Reset"):
            selected = categories[0]
            on_change(selected)
    
    return selected
