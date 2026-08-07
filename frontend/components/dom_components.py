"""DOM Intelligence Explorer Components for AI-QOS.

AI DOM Operating System components built on the AI-QOS UI Foundation.
All styling is derived from design tokens (themes/tokens.py) and shared
foundation components (components/shared.py). Public function names and
signatures are preserved for backward compatibility.
"""
import streamlit as st
from datetime import datetime, timedelta
from typing import Any, Optional

from frontend.mock.dom import (
    DOM_HERO_KPIS,
    DOM_KPI_METRICS,
    DOM_BOTTOM_TABS,
    DOM_RELATIONSHIP_GRAPH,
    DOM_AUTOMATION_IDEAS,
    DOM_ACCESSIBILITY_PANEL,
    DOM_NETWORK_LOGS,
    DOM_CSS_RULES,
    DOM_JS_LOGS,
    DOM_EVENTS_LOG,
    DOM_PERF_METRICS,
    DOM_HISTORY,
    DOM_QUICK_ACTIONS,
)

try:
    from frontend.themes.tokens import (
        COLORS, SPACING, TYPOGRAPHY, BORDERS, SHADOWS, ANIMATIONS,
        get_status_color, get_confidence_color, get_health_color,
    )
    from frontend.components.shared import (
        glass_card, glass_panel, section_header, divider, spacer, pulse_dot,
        empty_state, metric_card, status_badge,
    )
except ImportError:  # pragma: no cover - fallback for direct execution
    from themes.tokens import (
        COLORS, SPACING, TYPOGRAPHY, BORDERS, SHADOWS, ANIMATIONS,
        get_status_color, get_confidence_color, get_health_color,
    )
    from shared import (
        glass_card, glass_panel, section_header, divider, spacer, pulse_dot,
        empty_state, metric_card, status_badge,
    )


# ============================================================================
# Token shortcuts
# ============================================================================

_SEMANTIC_COLORS = {
    "primary": COLORS.PRIMARY,
    "secondary": COLORS.SECONDARY,
    "accent": COLORS.ACCENT,
    "info": COLORS.INFO,
    "success": COLORS.SUCCESS,
    "warning": COLORS.WARNING,
    "error": COLORS.ERROR,
    "muted": COLORS.TEXT_MUTED,
}


def _hex_to_rgb(hex_color: str) -> str:
    h = hex_color.lstrip('#')
    return f"{int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}"


_SEMANTIC_RGB = {
    "primary": COLORS.PRIMARY_RGB,
    "secondary": COLORS.SECONDARY_RGB,
    "accent": COLORS.ACCENT_RGB,
    "info": COLORS.INFO_RGB,
    "success": COLORS.SUCCESS_RGB,
    "warning": COLORS.WARNING_RGB,
    "error": COLORS.ERROR_RGB,
    "muted": _hex_to_rgb(COLORS.TEXT_MUTED),
}

_GLASS_PANEL_BG = f"linear-gradient(135deg, {COLORS.SURFACE} 0%, rgba({COLORS.PRIMARY_RGB}, 0.12) 100%)"
_GLASS_PANEL_BORDER = f"rgba({COLORS.PRIMARY_RGB}, 0.25)"
_PANEL_BORDER = COLORS.BORDER

_STATUS_HEX = {
    "running": COLORS.SUCCESS,
    "active": COLORS.SUCCESS,
    "idle": COLORS.TEXT_MUTED,
    "paused": COLORS.WARNING,
    "failed": COLORS.ERROR,
    "pending": COLORS.TEXT_MUTED,
    "waiting": COLORS.TEXT_MUTED,
    "completed": COLORS.PRIMARY,
    "easy": COLORS.SUCCESS,
    "moderate": COLORS.WARNING,
    "complex": COLORS.ERROR,
    "very_complex": COLORS.ERROR,
    "low": COLORS.SUCCESS,
    "medium": COLORS.WARNING,
    "high": COLORS.ERROR,
    "critical": COLORS.ERROR,
}

_LEVEL_HEX = {
    "info": COLORS.TEXT_MUTED,
    "warn": COLORS.WARNING,
    "warning": COLORS.WARNING,
    "error": COLORS.ERROR,
    "success": COLORS.SUCCESS,
}


def _semantic(name: str) -> str:
    return _SEMANTIC_COLORS.get(name, COLORS.PRIMARY)


def _semantic_rgb(name: str) -> str:
    return _SEMANTIC_RGB.get(name, COLORS.PRIMARY_RGB)


def _status_hex(status: str) -> str:
    if status in _STATUS_HEX:
        return _STATUS_HEX[status]
    return get_status_color(status)


def _level_hex(level: str) -> str:
    return _LEVEL_HEX.get(level, COLORS.TEXT_MUTED)


def _escape(text: Any) -> str:
    if text is None:
        return ""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _conf_color(value: int) -> str:
    return get_confidence_color(value)


# ============================================================================
# Session State Management (preserved keys, no breaking changes)
# ============================================================================

def init_dom_state() -> None:
    """Initialize DOM explorer session state (preserved keys)."""
    defaults = {
        "dom_selected_node": "node_search_input",
        "dom_expanded_nodes": {"node_html", "node_body", "node_header", "node_main"},
        "dom_search_query": "",
        "dom_inspector_tab": "overview",
        "dom_hovered_node": None,
        "dom_bottom_tab": "Console",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def toggle_dom_node(node_id: str) -> None:
    """Toggle DOM tree node expansion."""
    if node_id in st.session_state.dom_expanded_nodes:
        st.session_state.dom_expanded_nodes.discard(node_id)
    else:
        st.session_state.dom_expanded_nodes.add(node_id)


def select_dom_node(node_id: str) -> None:
    """Select a DOM node for inspection."""
    st.session_state.dom_selected_node = node_id


# ============================================================================
# Hero Header (DOM Intelligence Explorer) - sticky enterprise command header
# ============================================================================

def dom_header(info: dict) -> None:
    """Display the premium DOM hero header with KPI chips."""
    health = info.get("dom_health", 0)
    health_color = get_health_color(health)
    health_rgb = _hex_to_rgb(health_color)

    stat_chips = "".join(
        f'<div style="display:flex;flex-direction:column;align-items:center;gap:2px;'
        f'padding:{SPACING.SPACE_2} {SPACING.SPACE_4};'
        f'background:rgba({COLORS.SURFACE_RGB},0.7);'
        f'border:1px solid {_GLASS_PANEL_BORDER};'
        f'border-radius:{BORDERS.RADIUS_MD};min-width:96px;">'
        f'<span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};'
        f'text-transform:uppercase;letter-spacing:1px;">{_escape(k["label"])}</span>'
        f'<span style="color:{_semantic(k["color"])};font-size:{TYPOGRAPHY.FONT_SIZE_SM};'
        f'font-weight:600;display:flex;align-items:center;gap:4px;">'
        f'<span style="font-size:0.9rem;">{k["icon"]}</span>{_escape(str(k["value"]))}'
        f'</span></div>'
        for k in DOM_HERO_KPIS
    )

    st.markdown(
        f"""
        <div style="
            background:{_GLASS_PANEL_BG};
            border:1px solid {_GLASS_PANEL_BORDER};
            border-radius:{BORDERS.RADIUS_XL};
            padding:{SPACING.SPACE_6};
            margin-bottom:{SPACING.SPACE_4};
            box-shadow:{SHADOWS.CARD};
            position:sticky;top:0;z-index:10;
            backdrop-filter:blur(12px);
        ">
            <div style="display:flex;align-items:center;justify-content:space-between;
                        flex-wrap:wrap;gap:{SPACING.SPACE_4};margin-bottom:{SPACING.SPACE_4};">
                <div>
                    <div style="display:flex;align-items:center;gap:{SPACING.SPACE_2};
                                margin-bottom:{SPACING.SPACE_2};">
                        <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">🏠 Dashboard</span>
                        <span style="color:{COLORS.TEXT_MUTED};">›</span>
                        <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">DOM Explorer</span>
                        <span style="color:{COLORS.TEXT_MUTED};">›</span>
                        <span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{_escape(info.get("page", "Products Page"))}</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};flex-wrap:wrap;">
                        <h1 style="margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_2XL};
                                   color:{COLORS.TEXT_PRIMARY};font-weight:600;">
                            🔍 DOM Intelligence Explorer
                        </h1>
                        <span style="display:inline-flex;align-items:center;gap:{SPACING.SPACE_2};
                                     padding:{SPACING.SPACE_1} {SPACING.SPACE_3};
                                     background:rgba({health_rgb},0.2);
                                     color:{health_color};
                                     border:1px solid rgba({health_rgb},0.4);
                                     border-radius:{BORDERS.RADIUS_FULL};
                                     font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;">
                            <span style="width:8px;height:8px;border-radius:50%;
                                        background:{health_color};
                                        animation:{ANIMATIONS.PULSE};"></span>
                            DOM Health {health}%
                        </span>
                    </div>
                </div>
                <div style="display:flex;align-items:center;gap:{SPACING.SPACE_2};flex-wrap:wrap;">
                    <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};
                                 border:1px solid {_PANEL_BORDER};border-radius:{BORDERS.RADIUS_MD};
                                 padding:{SPACING.SPACE_1} {SPACING.SPACE_3};"
                          title="Search DOM">🔍 Search…</span>
                    <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};
                                 border:1px solid {_PANEL_BORDER};border-radius:{BORDERS.RADIUS_MD};
                                 padding:{SPACING.SPACE_1} {SPACING.SPACE_3};"
                          title="Command palette">⌘K Command</span>
                    <span style="color:{COLORS.TEXT_MUTED};font-size:1rem;cursor:pointer;"
                          title="Notifications">🔔</span>
                    <span style="color:{COLORS.TEXT_MUTED};font-size:1rem;cursor:pointer;"
                          title="Fullscreen">⛶</span>
                </div>
            </div>
            <div style="display:flex;gap:{SPACING.SPACE_2};flex-wrap:wrap;">{stat_chips}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# DOM KPI Strip - MetricCard grid
# ============================================================================

def dom_kpi_strip() -> None:
    """Display the DOM KPI strip as a MetricCard grid."""
    for i in range(0, len(DOM_KPI_METRICS), 4):
        row = DOM_KPI_METRICS[i:i + 4]
        cols = st.columns(len(row))
        for col, m in zip(cols, row):
            with col:
                metric_card(
                    title=m["title"],
                    value=m["value"],
                    subtitle=m.get("subtitle", ""),
                    trend=m.get("trend", ""),
                    icon=m.get("icon", ""),
                )



# ============================================================================
# DOM Tree Component (preserved) - token-styled with hover glow
# ============================================================================

def render_dom_node(node: dict[str, Any], level: int = 0) -> None:
    """Render a single DOM tree node (preserved signature) with token styling."""
    node_id = node["id"]
    is_expanded = node_id in st.session_state.dom_expanded_nodes
    has_children = bool(node.get("children"))
    is_selected = st.session_state.dom_selected_node == node_id

    tag_icons = {
        "html": "🌐", "head": "📋", "body": "📦",
        "header": "🔝", "main": "⬜", "nav": "🧭",
        "section": "📐", "div": "▢", "form": "📝",
        "input": "⌨️", "button": "🔘", "table": "📊",
        "a": "🔗", "img": "🖼️", "span": "▭", "p": "¶",
        "h1": "H1", "h2": "H2", "h3": "H3",
        "label": "🏷️", "select": "▼", "option": "•",
        "dialog": "📫", "ul": "≡", "li": "•",
    }
    icon = tag_icons.get(node["tag"], "⬜")

    attrs = node.get("attributes", {})
    attr_parts = []
    if "id" in attrs:
        attr_parts.append(f'#{attrs["id"]}')
    if "data-testid" in attrs:
        attr_parts.append(f'[testid={attrs["data-testid"]}]')
    if "class" in attrs:
        classes = attrs["class"][:30] + "..." if len(attrs.get("class", "")) > 30 else attrs.get("class", "")
        attr_parts.append(f'.{classes}')
    attr_str = " ".join(attr_parts[:2])

    text = node.get("text", "")
    if text and len(text) > 30:
        text = text[:30] + "..."
    text_display = f'"{text}"' if text else ""

    col1, col2 = st.columns([1, 4])
    with col1:
        indent = "　　" * level
        prefix = "▼ " if (has_children and is_expanded) else "▶ " if has_children else "• "
        button_label = f"{indent}{prefix}{icon} {node['tag']}"
        if attr_str:
            button_label += f" {attr_str}"
        if text_display:
            button_label += f" {text_display}"
        if len(button_label) > 60:
            button_label = button_label[:57] + "..."

        if st.button(button_label, key=f"dom_{node_id}", use_container_width=True):
            if has_children:
                toggle_dom_node(node_id)
            select_dom_node(node_id)
            st.rerun()

    with col2:
        badges = []
        if has_children:
            child_count = len(node.get("children", []))
            badges.append(f'<span style="background:rgba({COLORS.PRIMARY_RGB},0.2);padding:2px 6px;border-radius:{BORDERS.RADIUS_SM};font-size:10px;color:{COLORS.PRIMARY_LIGHT};">{child_count}</span>')
        if node["tag"] in ["button", "a", "input", "select", "textarea"]:
            badges.append(f'<span style="background:rgba({COLORS.SECONDARY_RGB},0.2);padding:2px 6px;border-radius:{BORDERS.RADIUS_SM};font-size:10px;color:{COLORS.SECONDARY};">interactive</span>')
        if "data-testid" in attrs:
            badges.append(f'<span style="background:rgba({COLORS.SUCCESS_RGB},0.2);padding:2px 6px;border-radius:{BORDERS.RADIUS_SM};font-size:10px;color:{COLORS.SUCCESS};">testid</span>')
        if "aria-label" in attrs:
            badges.append(f'<span style="background:rgba({COLORS.WARNING_RGB},0.2);padding:2px 6px;border-radius:{BORDERS.RADIUS_SM};font-size:10px;color:{COLORS.WARNING};">aria</span>')
        st.markdown(" " + " ".join(badges), unsafe_allow_html=True)

    if has_children and is_expanded:
        for child in node.get("children", []):
            render_dom_node(child, level + 1)


def dom_tree(tree_data: dict[str, Any], title: str = "DOM Tree") -> None:
    """Render the full DOM tree (preserved signature) with token styling."""
    section_header(title, icon="🌳")

    search_query = st.text_input(
        "Search elements...",
        placeholder="Search by tag, ID, class, text...",
        label_visibility="collapsed",
        key="dom_tree_search",
    )

    if search_query:
        from utils.dom_data import search_elements
        results = search_elements(search_query)
        st.markdown(f'<span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">Found <b style="color:{COLORS.PRIMARY_LIGHT};">{len(results)}</b> matching elements</span>', unsafe_allow_html=True)
        for node in results[:10]:
            render_dom_node({
                "id": node["id"],
                "tag": node["tag"],
                "attributes": node.get("attributes", {}),
                "text": node.get("text", ""),
                "children": [],
            })
    else:
        render_dom_node(tree_data)


# ============================================================================
# Browser Digital Twin (preserved name) - glass chrome + AI highlight
# ============================================================================

def browser_visualizer(node: Optional[dict[str, Any]], title: str = "Live DOM") -> None:
    """Render the browser digital twin (preserved signature) with token styling."""
    section_header(title, icon="🌐")

    # Browser chrome (glass)
    st.markdown(
        f'<div style="background:linear-gradient(180deg,{COLORS.SURFACE_HOVER} 0%,{COLORS.SURFACE} 100%);'
        f'border:1px solid {_PANEL_BORDER};'
        f'border-radius:{BORDERS.RADIUS_LG} {BORDERS.RADIUS_LG} 0 0;'
        f'padding:{SPACING.SPACE_3} {SPACING.SPACE_4};display:flex;align-items:center;gap:{SPACING.SPACE_3};">'
        f'<div style="display:flex;gap:6px;">'
        f'<div style="width:12px;height:12px;border-radius:50%;background:{COLORS.ERROR};"></div>'
        f'<div style="width:12px;height:12px;border-radius:50%;background:{COLORS.WARNING};"></div>'
        f'<div style="width:12px;height:12px;border-radius:50%;background:{COLORS.SUCCESS};"></div>'
        f'</div>'
        f'<div style="flex:1;background:rgba({COLORS.BORDER_RGB},0.5);border-radius:{BORDERS.RADIUS_MD};'
        f'padding:{SPACING.SPACE_2} {SPACING.SPACE_3};color:{COLORS.TEXT_MUTED};'
        f'font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-family:{TYPOGRAPHY.FONT_MONO};">'
        f'🔒 https://shop.staging.example.com/products</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Preview area with AI highlight
    st.markdown(
        f'<div style="min-height:400px;'
        f'background:linear-gradient(135deg,{COLORS.BACKGROUND_ALT} 0%,{COLORS.SURFACE} 100%);'
        f'border:1px solid {_PANEL_BORDER};border-top:none;'
        f'border-radius:0 0 {BORDERS.RADIUS_LG} {BORDERS.RADIUS_LG};'
        f'padding:{SPACING.SPACE_6};position:relative;">'
        # Header
        f'<div style="display:flex;justify-content:space-between;align-items:center;padding:{SPACING.SPACE_4};'
        f'background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_4};">'
        f'<div style="display:flex;align-items:center;gap:{SPACING.SPACE_4};">'
        f'<span style="font-size:24px;">🏪</span>'
        f'<div style="display:flex;gap:{SPACING.SPACE_3};font-size:{TYPOGRAPHY.FONT_SIZE_BASE};color:{COLORS.TEXT_SECONDARY};">'
        f'<span>Home</span><span style="color:{COLORS.PRIMARY};font-weight:600;">Products</span><span>Cart</span>'
        f'</div></div>'
        f'<div style="display:flex;gap:{SPACING.SPACE_2};align-items:center;">'
        f'<input type="text" placeholder="Search products..." style="padding:8px 12px;border-radius:{BORDERS.RADIUS_MD};border:1px solid {COLORS.BORDER};background:rgba({COLORS.SURFACE_RGB},0.8);color:{COLORS.TEXT_PRIMARY};width:200px;">'
        f'<button style="padding:8px 16px;background:{COLORS.PRIMARY};border:none;border-radius:{BORDERS.RADIUS_MD};color:white;cursor:pointer;">Search</button>'
        f'</div></div>'
        # Products
        f'<div style="margin-bottom:{SPACING.SPACE_4};">'
        f'<h2 style="color:{COLORS.TEXT_PRIMARY};margin:0 0 {SPACING.SPACE_4};">Our Products</h2>'
        f'<div style="display:flex;gap:{SPACING.SPACE_2};margin-bottom:{SPACING.SPACE_4};padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_MD};">'
        f'<select style="padding:8px;border-radius:{BORDERS.RADIUS_MD};background:{COLORS.SURFACE};border:1px solid {COLORS.BORDER};color:{COLORS.TEXT_PRIMARY};"><option>All Categories</option><option>Electronics</option></select>'
        f'<input type="number" placeholder="Min" style="padding:8px;width:80px;border-radius:{BORDERS.RADIUS_MD};background:{COLORS.SURFACE};border:1px solid {COLORS.BORDER};color:{COLORS.TEXT_PRIMARY};">'
        f'<input type="number" placeholder="Max" style="padding:8px;width:80px;border-radius:{BORDERS.RADIUS_MD};background:{COLORS.SURFACE};border:1px solid {COLORS.BORDER};color:{COLORS.TEXT_PRIMARY};">'
        f'<button style="padding:8px 16px;background:{COLORS.PRIMARY};border:none;border-radius:{BORDERS.RADIUS_MD};color:white;">Apply</button>'
        f'</div></div>'
        # Product grid - first card highlighted (AI bounding box)
        f'<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:{SPACING.SPACE_4};">'
        f'<div style="background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_LG};padding:{SPACING.SPACE_4};border:2px solid {COLORS.PRIMARY};box-shadow:0 0 20px rgba({COLORS.PRIMARY_RGB},0.3);animation:{ANIMATIONS.PULSE};">'
        f'<div style="background:linear-gradient(135deg,rgba({COLORS.PRIMARY_RGB},0.2),rgba({COLORS.SECONDARY_RGB},0.2));height:120px;border-radius:{BORDERS.RADIUS_MD};display:flex;align-items:center;justify-content:center;font-size:48px;margin-bottom:{SPACING.SPACE_3};">🎧</div>'
        f'<h3 style="color:{COLORS.TEXT_PRIMARY};margin:0 0 {SPACING.SPACE_2};">Wireless Headphones</h3>'
        f'<div style="color:{COLORS.SUCCESS};font-size:18px;font-weight:700;margin-bottom:{SPACING.SPACE_3};">$99.99</div>'
        f'<div style="display:flex;gap:{SPACING.SPACE_2};">'
        f'<button style="flex:1;padding:10px;background:{COLORS.SECONDARY};border:none;border-radius:{BORDERS.RADIUS_MD};color:{COLORS.BACKGROUND};font-weight:600;cursor:pointer;">Add to Cart</button>'
        f'<button style="padding:10px 12px;background:transparent;border:1px solid {COLORS.BORDER};border-radius:{BORDERS.RADIUS_MD};color:{COLORS.TEXT_SECONDARY};cursor:pointer;">View</button>'
        f'</div></div>'
        f'<div style="background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_LG};padding:{SPACING.SPACE_4};">'
        f'<div style="background:linear-gradient(135deg,rgba({COLORS.PRIMARY_RGB},0.2),rgba({COLORS.SECONDARY_RGB},0.2));height:120px;border-radius:{BORDERS.RADIUS_MD};display:flex;align-items:center;justify-content:center;font-size:48px;margin-bottom:{SPACING.SPACE_3};">⌚</div>'
        f'<h3 style="color:{COLORS.TEXT_PRIMARY};margin:0 0 {SPACING.SPACE_2};">Smart Watch</h3>'
        f'<div style="color:{COLORS.SUCCESS};font-size:18px;font-weight:700;margin-bottom:{SPACING.SPACE_3};">$199.99</div>'
        f'<div style="display:flex;gap:{SPACING.SPACE_2};">'
        f'<button style="flex:1;padding:10px;background:{COLORS.SECONDARY};border:none;border-radius:{BORDERS.RADIUS_MD};color:{COLORS.BACKGROUND};font-weight:600;cursor:pointer;">Add to Cart</button>'
        f'<button style="padding:10px 12px;background:transparent;border:1px solid {COLORS.BORDER};border-radius:{BORDERS.RADIUS_MD};color:{COLORS.TEXT_SECONDARY};cursor:pointer;">View</button>'
        f'</div></div>'
        f'</div>'
        # Pagination
        f'<div style="display:flex;justify-content:center;gap:{SPACING.SPACE_2};margin-top:20px;">'
        f'<button style="padding:8px 16px;background:rgba({COLORS.PRIMARY_RGB},0.3);border:none;border-radius:{BORDERS.RADIUS_MD};color:{COLORS.TEXT_SECONDARY};">Previous</button>'
        f'<button style="padding:8px 16px;background:{COLORS.PRIMARY};border:none;border-radius:{BORDERS.RADIUS_MD};color:white;">1</button>'
        f'<button style="padding:8px 16px;background:transparent;border:1px solid {COLORS.BORDER};border-radius:{BORDERS.RADIUS_MD};color:{COLORS.TEXT_SECONDARY};">2</button>'
        f'<button style="padding:8px 16px;background:transparent;border:1px solid {COLORS.BORDER};border-radius:{BORDERS.RADIUS_MD};color:{COLORS.TEXT_SECONDARY};">Next</button>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # AI highlight badge overlay
    if node:
        st.markdown(
            f'<div style="margin-top:{SPACING.SPACE_2};display:inline-flex;align-items:center;gap:{SPACING.SPACE_2};'
            f'padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({COLORS.PRIMARY_RGB},0.15);'
            f'border:1px solid {_GLASS_PANEL_BORDER};border-radius:{BORDERS.RADIUS_FULL};'
            f'color:{COLORS.PRIMARY_LIGHT};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">'
            f'<span style="width:8px;height:8px;border-radius:50%;background:{COLORS.PRIMARY};animation:{ANIMATIONS.PULSE};"></span>'
            f'AI Highlight: &lt;{_escape(node.get("tag", "unknown"))}&gt; · <code style="color:{COLORS.SECONDARY};">{_escape(str(node.get("xpath", "N/A"))[:50])}...</code>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # Controls
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🔍 Zoom In", use_container_width=True):
            st.info("Zoom in")
    with col2:
        if st.button("🔍 Zoom Out", use_container_width=True):
            st.info("Zoom out")
    with col3:
        if st.button("📱 Fullscreen", use_container_width=True):
            st.info("Fullscreen mode")
    with col4:
        if st.button("📍 Toggle Grid", use_container_width=True):
            st.info("Toggle grid overlay")


# ============================================================================
# AI Inspector (preserved name: element_inspector) - token-styled
# ============================================================================

def element_inspector(element: dict[str, Any], title: str = "Element Inspector") -> None:
    """Render detailed element inspector (preserved signature) with token styling."""
    section_header(title, icon="🔍")

    st.markdown(f'<div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};margin-bottom:{SPACING.SPACE_2};">Element</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {COLORS.SECONDARY};">'
            f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">Tag</div>'
            f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_LG};color:{COLORS.SECONDARY};font-family:{TYPOGRAPHY.FONT_MONO};">&lt;{_escape(element.get("tag", "unknown"))}&gt;</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        if element.get("id"):
            st.markdown(
                f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {COLORS.SUCCESS};">'
                f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">ID</div>'
                f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_BASE};color:{COLORS.SUCCESS};font-family:{TYPOGRAPHY.FONT_MONO};">#{_escape(element.get("id", ""))}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with col2:
        if element.get("role"):
            st.markdown(
                f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {COLORS.WARNING};">'
                f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">ARIA Role</div>'
                f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_BASE};color:{COLORS.WARNING};font-family:{TYPOGRAPHY.FONT_MONO};">[role={_escape(element.get("role", ""))}]</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    if element.get("classes"):
        st.markdown(
            f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};">'
            f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;margin-bottom:4px;">Classes</div>'
            f'<div style="font-family:{TYPOGRAPHY.FONT_MONO};font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.ACCENT};word-break:break-all;">'
            f'{" ".join(f".{_escape(c)}" for c in element.get("classes", []))}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    if element.get("text"):
        st.markdown(
            f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};">'
            f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">Text</div>'
            f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_BASE};color:{COLORS.TEXT_PRIMARY};">{_escape(element.get("text", ""))}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    if element.get("value"):
        st.markdown(
            f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};">'
            f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">Value</div>'
            f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_BASE};color:{COLORS.TEXT_PRIMARY};font-family:{TYPOGRAPHY.FONT_MONO};">{_escape(element.get("value", ""))}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )



# ============================================================================
# Locator Intelligence (preserved name) - token-styled ranking
# ============================================================================

def locator_intelligence(element: dict[str, Any], title: str = "AI Locator Intelligence") -> None:
    """Render locator intelligence panel (preserved signature) with token styling."""
    section_header(title, icon="🎯")

    from utils.dom_data import generate_locators
    locators = generate_locators(element)

    # Namespace widget keys by title so the same component can be rendered in
    # multiple panels (Locator Rank + AI Locator Intelligence) without duplicate
    # element-id conflicts. Falls back to "" for the original default title.
    ns = "" if title == "AI Locator Intelligence" else title.lower().replace(" ", "_") + "_"

    for i, loc in enumerate(locators):
        conf_color = _conf_color(loc["confidence"])
        rel_color = _conf_color(loc["reliability"])
        risk_color = _status_hex(loc["dynamic_risk"].lower().replace(" ", "_"))
        priority_badge = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"

        expander_label = f"{priority_badge} {loc['type'].upper()} - {loc['confidence']}% confidence"
        with st.expander(expander_label, expanded=i == 0, key=f"{ns}loc_expander_{i}"):
            st.markdown(
                f'<div style="margin-bottom:{SPACING.SPACE_3};">'
                f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;margin-bottom:4px;">CSS Locator</div>'
                f'<code style="display:block;padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.8);border-radius:{BORDERS.RADIUS_MD};font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.SECONDARY};word-break:break-all;">{_escape(loc["locator"])}</code>'
                f'</div>',
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                    f'<div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};">'
                    f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Confidence</div>'
                    f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_LG};font-weight:700;color:{conf_color};">{loc["confidence"]}%</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};">'
                    f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Dynamic Risk</div>'
                    f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_BASE};color:{risk_color};">{loc["dynamic_risk"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    f'<div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};">'
                    f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Reliability</div>'
                    f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_LG};font-weight:700;color:{rel_color};">{loc["reliability"]}%</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};">'
                    f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Healing Strategy</div>'
                    f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_SECONDARY};">{_escape(loc["healing_strategy"])}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            st.markdown(f'<div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;margin-bottom:{SPACING.SPACE_2};">Code Snippets</div>', unsafe_allow_html=True)
            code_col1, code_col2 = st.columns(2)
            with code_col1:
                st.code(loc.get("playwright", ""), language="python")
            with code_col2:
                st.code(loc.get("selenium", ""), language="python")

            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("📋 Copy CSS", key=f"{ns}copy_css_{i}"):
                    st.session_state[f"copied_{i}"] = "css"
            with c2:
                if st.button("📋 Copy Playwright", key=f"{ns}copy_pw_{i}"):
                    st.session_state[f"copied_{i}"] = "playwright"
            with c3:
                if st.button("📋 Copy Selenium", key=f"{ns}copy_se_{i}"):
                    st.session_state[f"copied_{i}"] = "selenium"


# ============================================================================
# Accessibility Inspector (preserved name) - token-styled + premium panel
# ============================================================================

def accessibility_inspector(element: dict[str, Any], title: str = "Accessibility") -> None:
    """Render accessibility inspector (preserved signature) with token styling."""
    section_header(title, icon="♿")

    from utils.dom_data import generate_accessibility_info
    a11y = generate_accessibility_info(element)

    score = a11y["score"]
    score_color = get_confidence_color(score)

    st.markdown(
        f'<div style="text-align:center;padding:{SPACING.SPACE_5};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_LG};margin-bottom:{SPACING.SPACE_4};border:1px solid {_PANEL_BORDER};">'
        f'<div style="font-size:48px;font-weight:700;color:{score_color};">{score}</div>'
        f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_BASE};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">Accessibility Score</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.metric("ARIA Label", a11y["aria_label"][:30] + "..." if len(a11y["aria_label"]) > 30 else a11y["aria_label"])
        st.metric("Keyboard Support", a11y["keyboard_support"])
    with col2:
        st.metric("ARIA Role", a11y["aria_role"])
        st.metric("Focus Manageable", "Yes" if a11y["focus_manageable"] else "No")

    if a11y["issues"]:
        st.markdown(f'<div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_BASE};font-weight:600;margin:{SPACING.SPACE_3} 0 {SPACING.SPACE_2};">⚠️ Issues</div>', unsafe_allow_html=True)
        for issue in a11y["issues"]:
            color = {"high": COLORS.ERROR, "medium": COLORS.WARNING, "low": COLORS.TEXT_MUTED}.get(issue["severity"], COLORS.TEXT_MUTED)
            color_rgb = _hex_to_rgb(color)
            st.markdown(
                f'<div style="padding:{SPACING.SPACE_3};background:rgba({color_rgb},0.1);border-left:3px solid {color};border-radius:0 {BORDERS.RADIUS_MD} {BORDERS.RADIUS_MD} 0;margin-bottom:{SPACING.SPACE_2};">'
                f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{color};text-transform:uppercase;">{_escape(issue["severity"])}</span>'
                f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_PRIMARY};margin-left:{SPACING.SPACE_2};">{_escape(issue["issue"])}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown(f'<div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_BASE};font-weight:600;margin:{SPACING.SPACE_3} 0 {SPACING.SPACE_2};">💡 Suggestions</div>', unsafe_allow_html=True)
    for suggestion in a11y["suggestions"]:
        icon = "✅" if suggestion.startswith("Good") else "💡"
        st.markdown(f"- {icon} {suggestion}")

    # Premium WCAG breakdown panel
    st.markdown(f'<div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_BASE};font-weight:600;margin:{SPACING.SPACE_4} 0 {SPACING.SPACE_2};">♿ WCAG Breakdown</div>', unsafe_allow_html=True)
    for item in DOM_ACCESSIBILITY_PANEL:
        c = _semantic(item["color"])
        c_rgb = _hex_to_rgb(c)
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;align-items:center;padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_1};border-left:3px solid {c};">'
            f'<div><span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;">{item["label"]}</span><br>'
            f'<span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{item["detail"]}</span></div>'
            f'<div style="text-align:right;"><span style="color:{c};font-size:{TYPOGRAPHY.FONT_SIZE_BASE};font-weight:600;">{item["value"]}</span>'
            + (f'<br><span style="color:{_conf_color(item["score"])};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{item["score"]}/100</span>' if item["score"] else "") +
            f'</div></div>',
            unsafe_allow_html=True,
        )


# ============================================================================
# Automation Intelligence (preserved name) - token-styled + premium ideas
# ============================================================================

def automation_intelligence(element: dict[str, Any], title: str = "Automation") -> None:
    """Render automation intelligence panel (preserved signature) with token styling."""
    section_header(title, icon="🤖")

    from utils.dom_data import generate_automation_info
    auto = generate_automation_info(element)

    diff_color = _status_hex(auto["difficulty"].lower().replace(" ", "_"))

    st.markdown(
        f'<div style="display:flex;justify-content:space-between;align-items:center;padding:{SPACING.SPACE_4};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_LG};margin-bottom:{SPACING.SPACE_4};border-left:4px solid {diff_color};">'
        f'<div><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">Automation Difficulty</div>'
        f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_2XL};font-weight:700;color:{diff_color};">{auto["difficulty"]}</div></div>'
        f'<div style="text-align:right;"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">Difficulty Score</div>'
        f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_2XL};font-weight:700;color:{diff_color};">{auto["difficulty_score"]}%</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        risk_color = _status_hex(auto["flaky_risk"].lower().replace(" ", "_"))
        st.markdown(f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};text-align:center;"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Flaky Risk</div><div style="font-size:{TYPOGRAPHY.FONT_SIZE_LG};font-weight:700;color:{risk_color};">{auto["flaky_risk"]}</div></div>', unsafe_allow_html=True)
    with col2:
        stability_color = COLORS.SUCCESS if auto["locator_stability"] == "High" else COLORS.WARNING
        st.markdown(f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};text-align:center;"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Locator Stability</div><div style="font-size:{TYPOGRAPHY.FONT_SIZE_LG};font-weight:700;color:{stability_color};">{auto["locator_stability"]}</div></div>', unsafe_allow_html=True)
    with col3:
        dyn_color = COLORS.ERROR if auto["dynamic_content"] else COLORS.SUCCESS
        st.markdown(f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};text-align:center;"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Dynamic Content</div><div style="font-size:{TYPOGRAPHY.FONT_SIZE_LG};font-weight:700;color:{dyn_color};">{"Yes" if auto["dynamic_content"] else "No"}</div></div>', unsafe_allow_html=True)

    st.markdown(f'<div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_BASE};font-weight:600;margin:{SPACING.SPACE_4} 0 {SPACING.SPACE_2};">⏱️ Wait Strategy</div>', unsafe_allow_html=True)
    st.markdown(f"- **{auto['wait_strategy']}**")
    st.markdown(f"- **Retry:** {auto['retry_strategy']}")

    st.markdown(f'<div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_BASE};font-weight:600;margin:{SPACING.SPACE_4} 0 {SPACING.SPACE_2};">✅ Expected Assertions</div>', unsafe_allow_html=True)
    for assertion in auto["expected_assertions"]:
        st.markdown(f"- {assertion}")

    # Premium automation ideas panel
    st.markdown(f'<div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_BASE};font-weight:600;margin:{SPACING.SPACE_4} 0 {SPACING.SPACE_2};">💡 AI Automation Ideas</div>', unsafe_allow_html=True)
    for idea in DOM_AUTOMATION_IDEAS:
        c = _semantic(idea["color"])
        c_rgb = _hex_to_rgb(c)
        st.markdown(
            f'<div style="display:flex;gap:{SPACING.SPACE_3};padding:{SPACING.SPACE_3};background:rgba({c_rgb},0.1);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {c};">'
            f'<span style="font-size:20px;">{idea["icon"]}</span>'
            f'<div><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">{idea["label"]}</div>'
            f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_PRIMARY};">{_escape(idea["value"])}</div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ============================================================================
# DOM Metrics (preserved name) - token-styled MetricCard grid
# ============================================================================

def dom_metrics(metrics: dict[str, Any], title: str = "DOM Metrics") -> None:
    """Render DOM metrics dashboard (preserved signature) with token styling."""
    section_header(title, icon="📊")

    grid_data = [
        ("Total Nodes", metrics["total_nodes"], "🧱"),
        ("Interactive", metrics["interactive_nodes"], "👆"),
        ("Hidden", metrics["hidden_nodes"], "👁️"),
        ("Dynamic", metrics["dynamic_nodes"], "🔄"),
        ("Forms", metrics["forms"], "📝"),
        ("Buttons", metrics["buttons"], "🔘"),
        ("Inputs", metrics["inputs"], "⌨️"),
        ("Tables", metrics["tables"], "📊"),
        ("Links", metrics["links"], "🔗"),
        ("ARIA Elements", metrics["aria_elements"], "♿"),
        ("Images", metrics["images"], "🖼️"),
        ("Shadow DOM", metrics["shadow_dom"], "👻"),
        ("Iframes", metrics["iframes"], "🖼️"),
    ]
    for i in range(0, len(grid_data), 4):
        row = grid_data[i:i + 4]
        cols = st.columns(len(row))
        for col, (t, v, icon) in zip(cols, row):
            with col:
                metric_card(title=t, value=v, icon=icon)


# ============================================================================
# AI Discoveries (preserved name) - token-styled
# ============================================================================

def ai_discoveries(discoveries: list[dict[str, Any]], title: str = "AI Discoveries") -> None:
    """Render AI discoveries panel (preserved signature) with token styling."""
    section_header(title, icon="🤖")

    critical = sum(1 for d in discoveries if d["severity"] == "critical")
    high = sum(1 for d in discoveries if d["severity"] == "high")
    total = sum(d["count"] for d in discoveries)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Critical", critical)
    with col2:
        st.metric("High Priority", high)
    with col3:
        st.metric("Total Issues", total)

    divider()

    type_icons = {
        "missing_ids": "🏷️", "missing_labels": "📝", "dynamic_elements": "🔄",
        "poor_locators": "⚠️", "accessibility_issues": "♿", "shadow_dom": "👻",
        "flaky_components": "📳", "suggestions": "💡",
    }
    severity_hex = {
        "critical": COLORS.ERROR, "high": COLORS.WARNING, "medium": COLORS.PRIMARY,
        "low": COLORS.TEXT_MUTED, "info": COLORS.SECONDARY,
    }

    for discovery in discoveries:
        icon = type_icons.get(discovery["type"], "📋")
        color = severity_hex.get(discovery["severity"], COLORS.TEXT_MUTED)
        with st.expander(f"{icon} {discovery['type'].replace('_', ' ').title()} ({discovery['count']})", expanded=discovery["severity"] in ["critical", "high"]):
            st.markdown(f"**Description:** {discovery['description']}")
            if discovery["elements"]:
                st.markdown(f"**Elements:** {', '.join(discovery['elements'][:5])}")


# ============================================================================
# Console Panel (preserved name) - token-styled
# ============================================================================

def console_panel(logs: list[dict[str, Any]], title: str = "Console") -> None:
    """Render developer console panel (preserved signature) with token styling."""
    section_header(title, icon="💻")

    for log in logs:
        color = _level_hex(log["level"])
        icon = {"info": "ℹ️", "warn": "⚠️", "error": "❌", "success": "✅"}.get(log["level"], "•")
        st.markdown(
            f'<div style="display:flex;gap:{SPACING.SPACE_2};padding:{SPACING.SPACE_2};border-bottom:1px solid rgba({COLORS.BORDER_RGB},0.3);font-family:{TYPOGRAPHY.FONT_MONO};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">'
            f'<span style="color:{COLORS.TEXT_MUTED};">{_escape(log["time"])}</span>'
            f'<span style="color:{color};">{icon}</span>'
            f'<span style="color:{COLORS.TEXT_PRIMARY};">{_escape(log["message"])}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ============================================================================
# Quick Actions (preserved name) - token-styled glass buttons
# ============================================================================

def quick_actions(title: str = "Quick Actions") -> None:
    """Render quick actions panel (preserved signature) with token styling."""
    section_header(title, icon="⚡")

    for i in range(0, len(DOM_QUICK_ACTIONS), 4):
        row = DOM_QUICK_ACTIONS[i:i + 4]
        cols = st.columns(len(row))
        for col, action in zip(cols, row):
            with col:
                if st.button(f"{action['icon']} {action['name']}", key=f"dom_action_{i}_{action['name']}", use_container_width=True, help=action["description"]):
                    st.info(action["description"])
                    st.rerun()


# ============================================================================
# Element Relationship Graph (preserved name) - token-styled + premium chain
# ============================================================================

def element_relationship_graph(element_id: str, title: str = "Element Relationships") -> None:
    """Render element relationship graph (preserved signature) + premium chain."""
    section_header(title, icon="🔗")

    from utils.dom_data import generate_relationship_graph
    relationships = generate_relationship_graph(element_id)

    if relationships:
        type_icons = {"form": "📝", "api": "🔗", "ui": "🖥️", "state": "📊", "validation": "✅", "service": "⚙️"}
        for rel in relationships:
            icon = type_icons.get(rel["type"], "•")
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};">'
                f'<span style="font-size:20px;">{icon}</span>'
                f'<div style="flex:1;"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_BASE};color:{COLORS.TEXT_PRIMARY};">{_escape(rel["target"])}</div>'
                f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_SECONDARY};">{_escape(rel["relationship"])}</div></div>'
                f'</div>',
                unsafe_allow_html=True,
            )
    else:
        empty_state(icon="🔗", title="No Relationships", description="No relationships found for this element.")

    # Premium relationship chain: Element -> Component -> Business Rule -> API -> DB -> Workflow -> Report
    st.markdown(f'<div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_BASE};font-weight:600;margin:{SPACING.SPACE_4} 0 {SPACING.SPACE_3};">🕸️ Business Flow Chain</div>', unsafe_allow_html=True)
    for node in DOM_RELATIONSHIP_GRAPH:
        c = _semantic(node["color"])
        c_rgb = _hex_to_rgb(c)
        is_last = node["level"] == len(DOM_RELATIONSHIP_GRAPH) - 1
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};margin-bottom:{SPACING.SPACE_1};">'
            f'<div style="width:44px;height:44px;border-radius:{BORDERS.RADIUS_MD};background:rgba({c_rgb},0.2);display:flex;align-items:center;justify-content:center;font-size:20px;border:1px solid rgba({c_rgb},0.4);flex-shrink:0;">{node["icon"]}</div>'
            f'<div><div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;color:{c};">{node["name"]}</div>'
            f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_SECONDARY};font-family:{TYPOGRAPHY.FONT_MONO};">{_escape(node["detail"])}</div></div>'
            f'</div>'
            + ("" if is_last else f'<div style="margin-left:22px;width:2px;height:14px;background:linear-gradient(180deg,{c},{COLORS.BORDER});"></div>'),
            unsafe_allow_html=True,
        )


# ============================================================================
# DOM Timeline (preserved name) - token-styled
# ============================================================================

def dom_timeline(timeline: list[dict[str, Any]], title: str = "DOM Analysis Timeline") -> None:
    """Render DOM analysis timeline (preserved signature) with token styling."""
    section_header(title, icon="📅")

    status_colors = {"completed": COLORS.SUCCESS, "in_progress": COLORS.WARNING, "pending": COLORS.TEXT_MUTED}

    for i, item in enumerate(timeline):
        color = status_colors.get(item["status"], COLORS.TEXT_MUTED)
        is_last = i == len(timeline) - 1
        time_diff = datetime.now() - item.get("time", datetime.now())
        if time_diff < timedelta(minutes=1):
            time_str = f"{int(time_diff.total_seconds())}s ago"
        elif time_diff < timedelta(hours=1):
            time_str = f"{int(time_diff.total_seconds() / 60)}m ago"
        else:
            time_str = f"{int(time_diff.total_seconds() / 3600)}h ago"

        st.markdown(
            f'<div style="display:flex;gap:{SPACING.SPACE_3};margin-bottom:{0 if is_last else SPACING.SPACE_3};">'
            f'<div style="display:flex;flex-direction:column;align-items:center;">'
            f'<div style="width:12px;height:12px;border-radius:50%;background:{color};"></div>'
            + ("" if is_last else f'<div style="width:2px;flex:1;background:linear-gradient(180deg,{color},{COLORS.BORDER});"></div>') +
            f'</div>'
            f'<div style="flex:1;"><div style="display:flex;justify-content:space-between;">'
            f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_PRIMARY};font-weight:500;">{_escape(item["name"])}</span>'
            f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">{time_str}</span></div>'
            f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_SECONDARY};">{_escape(item["details"])}</div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ============================================================================
# AI Explanation (preserved name) - token-styled
# ============================================================================

def ai_explanation(element: dict[str, Any], title: str = "AI Explanation") -> None:
    """Render AI-powered element explanation (preserved signature) with token styling."""
    section_header(title, icon="💡")

    tag = element.get("tag", "unknown")
    explanations = {
        "input": {"why": "Collects user input for forms and search functionality", "purpose": "User interaction and data collection", "priority": "High", "complexity": "Low", "impact": "Critical for user workflows"},
        "button": {"why": "Triggers actions and form submissions", "purpose": "User action initiation", "priority": "Critical", "complexity": "Low", "impact": "Core user interaction"},
        "form": {"why": "Groups related inputs and manages submission", "purpose": "Data collection and validation", "priority": "Critical", "complexity": "Medium", "impact": "Essential business logic"},
    }
    exp = explanations.get(tag, {"why": "Provides structure and content", "purpose": "UI composition", "priority": "Medium", "complexity": "Low", "impact": "Visual rendering"})

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">Why Important</div><div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_PRIMARY};margin-top:4px;">{_escape(exp["why"])}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-top:{SPACING.SPACE_2};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">Business Purpose</div><div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_PRIMARY};margin-top:4px;">{_escape(exp["purpose"])}</div></div>', unsafe_allow_html=True)
    with col2:
        priority_colors = {"Critical": COLORS.ERROR, "High": COLORS.WARNING, "Medium": COLORS.PRIMARY, "Low": COLORS.TEXT_MUTED}
        priority_color = priority_colors.get(exp["priority"], COLORS.TEXT_MUTED)
        st.markdown(f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">Testing Priority</div><div style="font-size:{TYPOGRAPHY.FONT_SIZE_LG};font-weight:700;color:{priority_color};margin-top:4px;">{exp["priority"]}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-top:{SPACING.SPACE_2};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">Automation Complexity</div><div style="font-size:{TYPOGRAPHY.FONT_SIZE_BASE};color:{COLORS.TEXT_PRIMARY};margin-top:4px;">{exp["complexity"]}</div></div>', unsafe_allow_html=True)

    st.markdown(
        f'<div style="padding:{SPACING.SPACE_4};background:linear-gradient(135deg,rgba({COLORS.PRIMARY_RGB},0.1),rgba({COLORS.SECONDARY_RGB},0.1));border:1px solid {_GLASS_PANEL_BORDER};border-radius:{BORDERS.RADIUS_MD};margin-top:{SPACING.SPACE_3};">'
        f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;margin-bottom:6px;">AI Recommendation</div>'
        f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_PRIMARY};">This <code style="color:{COLORS.SECONDARY};">&lt;{_escape(tag)}&gt;</code> element is critical for user interaction. Ensure proper test coverage with both positive and negative test cases.</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ============================================================================
# Search (preserved name) - token-styled
# ============================================================================

def dom_search(on_search: callable = None) -> str:
    """Render DOM search input (preserved signature) with token styling."""
    query = st.text_input(
        "Search DOM...",
        placeholder="Search by tag, ID, class, text, role...",
        label_visibility="collapsed",
        key="dom_search_input",
    )
    return query


# ============================================================================
# Bottom Workspace Tabs (premium) - Console/Network/A11y/CSS/JS/Events/Perf/History
# ============================================================================

def bottom_workspace_tabs() -> None:
    """Render the bottom developer workspace tabs using shared foundation."""
    selected = st.session_state.get("dom_bottom_tab", "Console")
    tabs = st.tabs(DOM_BOTTOM_TABS)
    tab_map = dict(zip(DOM_BOTTOM_TABS, tabs))

    with tab_map["Console"]:
        _render_console_tab()
    with tab_map["Network"]:
        _render_network_tab()
    with tab_map["Accessibility"]:
        _render_a11y_tab()
    with tab_map["CSS"]:
        _render_css_tab()
    with tab_map["JavaScript"]:
        _render_js_tab()
    with tab_map["Events"]:
        _render_events_tab()
    with tab_map["Performance"]:
        _render_performance_tab()
    with tab_map["History"]:
        _render_history_tab()


def _render_console_tab() -> None:
    from utils.dom_data import generate_console_logs
    logs = generate_console_logs()
    for log in logs:
        color = _level_hex(log["level"])
        icon = {"info": "ℹ️", "warn": "⚠️", "error": "❌", "success": "✅"}.get(log["level"], "•")
        st.markdown(
            f'<div style="display:flex;gap:{SPACING.SPACE_2};padding:{SPACING.SPACE_2};border-bottom:1px solid rgba({COLORS.BORDER_RGB},0.3);font-family:{TYPOGRAPHY.FONT_MONO};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">'
            f'<span style="color:{COLORS.TEXT_MUTED};">{_escape(log["time"])}</span>'
            f'<span style="color:{color};">{icon}</span>'
            f'<span style="color:{COLORS.TEXT_PRIMARY};">{_escape(log["message"])}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


def _render_network_tab() -> None:
    for log in DOM_NETWORK_LOGS:
        c = _semantic(log["color"])
        c_rgb = _hex_to_rgb(c)
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_1};border-left:3px solid {c};">'
            f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};font-weight:700;color:{c};min-width:42px;">{log["method"]}</span>'
            f'<span style="flex:1;font-family:{TYPOGRAPHY.FONT_MONO};font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_PRIMARY};">{_escape(log["url"])}</span>'
            f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">{log["time"]}</span>'
            f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">{log["size"]}</span>'
            f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;color:{c};">{log["status"]}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


def _render_a11y_tab() -> None:
    for item in DOM_ACCESSIBILITY_PANEL:
        c = _semantic(item["color"])
        c_rgb = _hex_to_rgb(c)
        bar = f'<div style="height:6px;background:rgba({COLORS.BORDER_RGB},0.4);border-radius:3px;margin-top:4px;overflow:hidden;"><div style="width:{item["score"]}%;height:100%;background:{c};border-radius:3px;"></div></div>' if item["score"] else ""
        st.markdown(
            f'<div style="padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {c};">'
            f'<div style="display:flex;justify-content:space-between;"><span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;">{item["label"]}</span>'
            f'<span style="color:{c};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;">{item["value"]}</span></div>'
            f'<div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{item["detail"]}</div>'
            f'{bar}</div>',
            unsafe_allow_html=True,
        )


def _render_css_tab() -> None:
    for rule in DOM_CSS_RULES:
        c = _semantic(rule["color"])
        st.markdown(
            f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {c};">'
            f'<div style="font-family:{TYPOGRAPHY.FONT_MONO};font-size:{TYPOGRAPHY.FONT_SIZE_BASE};color:{c};font-weight:600;">{_escape(rule["selector"])}</div>'
            f'<div style="font-family:{TYPOGRAPHY.FONT_MONO};font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_SECONDARY};">{_escape(rule["props"])}</div>'
            f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};margin-top:2px;">{_escape(rule["source"])}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


def _render_js_tab() -> None:
    for log in DOM_JS_LOGS:
        color = _level_hex(log["level"])
        icon = {"info": "ℹ️", "warn": "⚠️", "error": "❌", "success": "✅"}.get(log["level"], "•")
        st.markdown(
            f'<div style="display:flex;gap:{SPACING.SPACE_2};padding:{SPACING.SPACE_2};border-bottom:1px solid rgba({COLORS.BORDER_RGB},0.3);font-family:{TYPOGRAPHY.FONT_MONO};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">'
            f'<span style="color:{COLORS.TEXT_MUTED};">{_escape(log["time"])}</span>'
            f'<span style="color:{color};">{icon}</span>'
            f'<span style="color:{COLORS.TEXT_PRIMARY};">{_escape(log["message"])}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


def _render_events_tab() -> None:
    for ev in DOM_EVENTS_LOG:
        c = _semantic(ev["color"])
        c_rgb = _hex_to_rgb(c)
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({c_rgb},0.1);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_1};border-left:3px solid {c};">'
            f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};font-weight:700;color:{c};min-width:64px;">{ev["event"]}</span>'
            f'<span style="flex:1;font-family:{TYPOGRAPHY.FONT_MONO};font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_PRIMARY};">{_escape(ev["target"])}</span>'
            f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">{_escape(ev["time"])}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


def _render_performance_tab() -> None:
    for m in DOM_PERF_METRICS:
        c = _semantic(m["color"])
        bar = f'<div style="height:6px;background:rgba({COLORS.BORDER_RGB},0.4);border-radius:3px;margin-top:4px;overflow:hidden;"><div style="width:{m["score"]}%;height:100%;background:{c};border-radius:3px;"></div></div>'
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};">'
            f'<div style="flex:1;"><div style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;">{m["metric"]}</div>{bar}</div>'
            f'<span style="color:{c};font-size:{TYPOGRAPHY.FONT_SIZE_LG};font-weight:700;">{m["value"]}</span>'
            f'<span style="color:{_conf_color(m["score"])};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{m["score"]}/100</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


def _render_history_tab() -> None:
    for i, item in enumerate(DOM_HISTORY):
        c = _semantic(item["color"])
        is_last = i == len(DOM_HISTORY) - 1
        st.markdown(
            f'<div style="display:flex;gap:{SPACING.SPACE_3};margin-bottom:{0 if is_last else SPACING.SPACE_2};">'
            f'<div style="display:flex;flex-direction:column;align-items:center;">'
            f'<div style="width:32px;height:32px;border-radius:50%;background:rgba({_hex_to_rgb(c)},0.2);display:flex;align-items:center;justify-content:center;font-size:16px;">{item["icon"]}</div>'
            + ("" if is_last else f'<div style="width:2px;flex:1;background:linear-gradient(180deg,{c},{COLORS.BORDER});min-height:20px;"></div>') +
            f'</div>'
            f'<div><div style="display:flex;gap:{SPACING.SPACE_3};"><span style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_PRIMARY};font-weight:500;">{item["title"]}</span>'
            f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">{item["time"]}</span></div>'
            f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_SECONDARY};">{item["desc"]}</div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

