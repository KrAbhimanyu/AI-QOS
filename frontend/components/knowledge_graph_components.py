"""Knowledge Graph & AI Cognitive Intelligence Center Components for AI-QOS.

Premium cognitive-intelligence components built on the AI-QOS UI Foundation.
All styling derives from design tokens (themes/tokens.py) and shared
foundation components (components/shared.py). Public function names and
signatures are preserved for backward compatibility — no breaking changes.
"""

from datetime import datetime, timedelta
from typing import Any, Optional
import streamlit as st
import plotly.graph_objects as go

try:
    from frontend.themes.tokens import (
        COLORS, SPACING, TYPOGRAPHY, BORDERS, SHADOWS, ANIMATIONS,
        get_status_color, get_confidence_color, get_health_color, get_priority_color,
    )
    from frontend.components.shared import (
        glass_card, glass_panel, section_header, divider, spacer, pulse_dot,
        empty_state, metric_card, status_badge,
    )
    from frontend.mock.knowledge import (
        KG_HERO_KPIS, KG_KPI_METRICS, KG_DEPENDENCY_CHAIN, KG_HEALTH,
        KG_HEALTH_SUGGESTIONS, KG_BOTTOM_TABS, KG_QUICK_ACTIONS,
        KG_REASONING_TRACE, KG_MEMORY, KG_EVIDENCE,
    )
except ImportError:  # pragma: no cover - fallback for direct execution
    from themes.tokens import (
        COLORS, SPACING, TYPOGRAPHY, BORDERS, SHADOWS, ANIMATIONS,
        get_status_color, get_confidence_color, get_health_color, get_priority_color,
    )
    from shared import (
        glass_card, glass_panel, section_header, divider, spacer, pulse_dot,
        empty_state, metric_card, status_badge,
    )
    from mock.knowledge import (
        KG_HERO_KPIS, KG_KPI_METRICS, KG_DEPENDENCY_CHAIN, KG_HEALTH,
        KG_HEALTH_SUGGESTIONS, KG_BOTTOM_TABS, KG_QUICK_ACTIONS,
        KG_REASONING_TRACE, KG_MEMORY, KG_EVIDENCE,
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
_GRAPH_PAPER_BG = f"rgba({COLORS.SURFACE_RGB}, 0.9)"

# Relationship type -> semantic color (for legend + edges)
_REL_COLORS = {
    "contains": COLORS.PRIMARY,
    "has": COLORS.SECONDARY,
    "uses": COLORS.WARNING,
    "calls": COLORS.SUCCESS,
    "validates": COLORS.ACCENT,
    "covers": COLORS.INFO,
    "affects": COLORS.ERROR,
    "depends_on": COLORS.WARNING,
    "generates": COLORS.SUCCESS,
    "related_to": COLORS.TEXT_MUTED,
    "parent_of": COLORS.PRIMARY,
    "implements": COLORS.SECONDARY,
    "tests": COLORS.INFO,
    "bugs": COLORS.ERROR,
    "releases": COLORS.SECONDARY,
}

# Node type -> icon + semantic color name
_TYPE_CONFIG = {
    "mission": {"icon": "🎯", "color": "accent"},
    "application": {"icon": "🏢", "color": "primary"},
    "business_domain": {"icon": "🏛️", "color": "primary"},
    "business_flow": {"icon": "🔄", "color": "secondary"},
    "page": {"icon": "📄", "color": "secondary"},
    "component": {"icon": "🧩", "color": "success"},
    "dom_element": {"icon": "🏗️", "color": "info"},
    "form": {"icon": "📝", "color": "warning"},
    "button": {"icon": "🔘", "color": "warning"},
    "input": {"icon": "⌨️", "color": "primary"},
    "table": {"icon": "📊", "color": "info"},
    "dialog": {"icon": "💬", "color": "secondary"},
    "locator": {"icon": "🎯", "color": "info"},
    "assertion": {"icon": "✅", "color": "success"},
    "api": {"icon": "🔗", "color": "warning"},
    "database_table": {"icon": "🗄️", "color": "primary"},
    "business_rule": {"icon": "⚖️", "color": "accent"},
    "feature_file": {"icon": "📦", "color": "warning"},
    "scenario": {"icon": "🎬", "color": "secondary"},
    "test_case": {"icon": "🧪", "color": "success"},
    "execution": {"icon": "⚡", "color": "info"},
    "evidence": {"icon": "📸", "color": "info"},
    "bug": {"icon": "🐛", "color": "error"},
    "report": {"icon": "📈", "color": "success"},
    "release": {"icon": "🚀", "color": "secondary"},
    "user": {"icon": "👤", "color": "primary"},
    "role": {"icon": "🎭", "color": "accent"},
}


def _semantic(name: str) -> str:
    return _SEMANTIC_COLORS.get(name, COLORS.PRIMARY)


def _semantic_rgb(name: str) -> str:
    return _SEMANTIC_RGB.get(name, COLORS.PRIMARY_RGB)


def _type_color(node_type: str) -> str:
    cfg = _TYPE_CONFIG.get(node_type, {"color": "muted"})
    return _semantic(cfg["color"])


def _type_icon(node_type: str) -> str:
    return _TYPE_CONFIG.get(node_type, {"icon": "📋"})["icon"]


def _rel_color(rel_type: str) -> str:
    return _REL_COLORS.get(rel_type, COLORS.TEXT_MUTED)


def _status_hex(status: str) -> str:
    return get_status_color(status)


def _risk_color(risk: str) -> str:
    return {
        "low": COLORS.SUCCESS,
        "medium": COLORS.WARNING,
        "high": COLORS.ERROR,
        "critical": COLORS.ERROR,
    }.get(risk, COLORS.TEXT_MUTED)


def _coverage_color(coverage: float) -> str:
    if coverage >= 80:
        return COLORS.SUCCESS
    if coverage >= 60:
        return COLORS.WARNING
    return COLORS.ERROR


def _priority_color(priority: str) -> str:
    return get_priority_color(priority)


def _severity_color(severity: str) -> str:
    return {
        "critical": COLORS.ERROR,
        "high": COLORS.WARNING,
        "medium": COLORS.INFO,
        "low": COLORS.TEXT_MUTED,
        "info": COLORS.INFO,
    }.get(severity, COLORS.TEXT_MUTED)


def _escape(text: Any) -> str:
    if text is None:
        return ""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _conf_color(value: int) -> str:
    return get_confidence_color(value)


# ============================================================================
# Session State Management (preserved keys + one additive key)
# ============================================================================

def init_knowledge_state() -> None:
    """Initialize knowledge graph session state (preserved keys)."""
    defaults = {
        "kg_selected_node": "node_app",
        "kg_expanded_tree": {"root"},
        "kg_search_query": "",
        "kg_filters": set(),
        "kg_view_mode": "graph",
        "kg_selected_flow": None,
        "kg_expanded_categories": set(),
        "kg_bottom_tab": "Timeline",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def select_kg_node(node_id: str) -> None:
    """Select a node for inspection."""
    st.session_state.kg_selected_node = node_id


def toggle_category(category: str) -> None:
    """Toggle category expansion."""
    if category in st.session_state.kg_expanded_categories:
        st.session_state.kg_expanded_categories.discard(category)
    else:
        st.session_state.kg_expanded_categories.add(category)


# ============================================================================
# Hero Header — sticky enterprise cognitive command header
# ============================================================================

def kg_header(info: dict) -> None:
    """Display the premium cognitive hero header with KPI chips."""
    health = info.get("graph_health", 0)
    health_color = get_health_color(health)
    health_rgb = _hex_to_rgb(health_color)
    confidence = info.get("confidence", 0)
    conf_color = _conf_color(confidence)

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
        for k in KG_HERO_KPIS
    )

    st.markdown(
        f"""<div style=" background:{_GLASS_PANEL_BG}; border:1px solid {_GLASS_PANEL_BORDER}; border-radius:{BORDERS.RADIUS_XL}; padding:{SPACING.SPACE_6}; margin-bottom:{SPACING.SPACE_4}; box-shadow:{SHADOWS.CARD}; position:sticky;top:0;z-index:10; backdrop-filter:blur(12px); "> <div style="display:flex;align-items:center;justify-content:space-between; flex-wrap:wrap;gap:{SPACING.SPACE_4};margin-bottom:{SPACING.SPACE_4};"> <div> <div style="display:flex;align-items:center;gap:{SPACING.SPACE_2}; margin-bottom:{SPACING.SPACE_2};"> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">🏠 Dashboard</span> <span style="color:{COLORS.TEXT_MUTED};">›</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">Knowledge Graph</span> <span style="color:{COLORS.TEXT_MUTED};">›</span> <span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{_escape(info.get("application", "E-Commerce Platform"))}</span> </div> <div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};flex-wrap:wrap;"> <h1 style="margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_2XL}; color:{COLORS.TEXT_PRIMARY};font-weight:600;"> 🧠 AI Cognitive Intelligence Center </h1> <span style="display:inline-flex;align-items:center;gap:{SPACING.SPACE_2}; padding:{SPACING.SPACE_1} {SPACING.SPACE_3}; background:rgba({health_rgb},0.2); color:{health_color}; border:1px solid rgba({health_rgb},0.4); border-radius:{BORDERS.RADIUS_FULL}; font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;"> <span style="width:8px;height:8px;border-radius:50%; background:{health_color}; animation:{ANIMATIONS.PULSE};"></span> Graph Health {health}% </span> <span style="display:inline-flex;align-items:center;gap:{SPACING.SPACE_2}; padding:{SPACING.SPACE_1} {SPACING.SPACE_3}; background:rgba({_hex_to_rgb(conf_color)},0.2); color:{conf_color}; border:1px solid rgba({_hex_to_rgb(conf_color)},0.4); border-radius:{BORDERS.RADIUS_FULL}; font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;"> 🧠 Confidence {confidence}% </span> </div> <p style="margin:{SPACING.SPACE_2} 0 0;color:{COLORS.TEXT_MUTED}; font-size:{TYPOGRAPHY.FONT_SIZE_SM};"> Explore the living AI-QOS brain • Knowledge Version {_escape(str(info.get("knowledge_version", "2.0")))} • {_escape(info.get("mission", ""))} </p> </div> <div style="display:flex;align-items:center;gap:{SPACING.SPACE_2};flex-wrap:wrap;"> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM}; border:1px solid {_PANEL_BORDER};border-radius:{BORDERS.RADIUS_MD}; padding:{SPACING.SPACE_1} {SPACING.SPACE_3};" title="Search knowledge graph">🔍 Search…</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM}; border:1px solid {_PANEL_BORDER};border-radius:{BORDERS.RADIUS_MD}; padding:{SPACING.SPACE_1} {SPACING.SPACE_3};" title="Command palette">⌘K Command</span> <span style="color:{COLORS.TEXT_MUTED};font-size:1rem;cursor:pointer;" title="Notifications">🔔</span> <span style="color:{COLORS.TEXT_MUTED};font-size:1rem;cursor:pointer;" title="Fullscreen">⛶</span> </div> </div> <div style="display:flex;gap:{SPACING.SPACE_2};flex-wrap:wrap;">{stat_chips}</div> </div>""",
        unsafe_allow_html=True,
    )


# ============================================================================
# KPI Strip — MetricCard grid
# ============================================================================

def kg_kpi_strip() -> None:
    """Display the knowledge KPI strip as a MetricCard grid."""
    for i in range(0, len(KG_KPI_METRICS), 4):
        row = KG_KPI_METRICS[i:i + 4]
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
# Knowledge Navigator (preserved signature) — token-styled expandable tree
# ============================================================================

def knowledge_navigator(nodes: list[dict[str, Any]], title: str = "Knowledge Navigator") -> None:
    """Render the enhanced knowledge tree navigator (preserved signature)."""
    section_header(title, icon="📚")

    node_groups: dict[str, list[dict[str, Any]]] = {}
    for node in nodes:
        node_type = node.get("type", "unknown")
        node_groups.setdefault(node_type, []).append(node)

    for node_type, type_nodes in sorted(node_groups.items()):
        cfg = _TYPE_CONFIG.get(node_type, {"icon": "📋", "color": "muted"})
        icon = cfg["icon"]
        color = _semantic(cfg["color"])
        color_rgb = _hex_to_rgb(color)
        type_name = node_type.replace("_", " ").title()

        is_expanded = node_type in st.session_state.kg_expanded_categories

        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button(
                f"{'▼' if is_expanded else '▶'} {icon} {type_name}",
                key=f"kg_cat_{node_type}",
                use_container_width=True,
            ):
                toggle_category(node_type)
                st.rerun()
        with col2:
            st.markdown(
                f'<span style="color:{color};font-size:{TYPOGRAPHY.FONT_SIZE_SM};'
                f'font-weight:600;background:rgba({color_rgb},0.15);'
                f'padding:2px 8px;border-radius:{BORDERS.RADIUS_FULL};">'
                f'{len(type_nodes)}</span>',
                unsafe_allow_html=True,
            )

        if is_expanded:
            for node in type_nodes[:10]:
                _render_node_card(node, color)
            if len(type_nodes) > 10:
                st.markdown(
                    f'<span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">'
                    f'... and {len(type_nodes) - 10} more</span>',
                    unsafe_allow_html=True,
                )


def _render_node_card(node: dict[str, Any], accent_color: str) -> None:
    """Render a single node card in the navigator."""
    risk_color = _risk_color(node.get("risk", "low"))
    coverage = node.get("automation_coverage", 0)
    coverage_color = _coverage_color(coverage)

    is_selected = st.session_state.kg_selected_node == node["id"]
    bg = f"rgba({COLORS.PRIMARY_RGB},0.22)" if is_selected else f"rgba({COLORS.SURFACE_RGB},0.5)"
    border_w = "2px" if is_selected else "1px"

    st.markdown(f"""<div style=" padding:{SPACING.SPACE_2} {SPACING.SPACE_3}; background:{bg}; border-left:{border_w} solid {accent_color}; border-radius:0 {BORDERS.RADIUS_MD} {BORDERS.RADIUS_MD} 0; margin:{SPACING.SPACE_1} 0 {SPACING.SPACE_1} {SPACING.SPACE_4}; {'animation:' + ANIMATIONS.FADE_IN + ';' if is_selected else ''} "> <div style="display:flex;justify-content:space-between;align-items:center;"> <span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;">{_escape(node["name"])}</span> <div style="display:flex;gap:{SPACING.SPACE_2};"> <span style="color:{coverage_color};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{coverage:.0f}%</span> <span style="color:{risk_color};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{_escape(str(node.get("risk", "low"))).upper()}</span> </div> </div> </div>""", unsafe_allow_html=True)

    if st.button(
        "Inspect",
        key=f"kg_select_{node['id']}",
        use_container_width=True,
        help=f"Inspect {_escape(node['name'])}",
    ):
        select_kg_node(node["id"])
        st.rerun()


# ============================================================================
# Knowledge Graph Canvas (preserved signature) — premium animated graph
# ============================================================================

def knowledge_graph_canvas(
    graph_data: dict[str, Any],
    selected_node: Optional[str] = None,
    title: str = "Knowledge Graph"
) -> None:
    """Render the interactive knowledge graph (preserved signature)."""
    section_header(title, icon="🕸️")

    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])

    if not nodes:
        empty_state(icon="🕸️", title="No Graph Data", description="No graph data available.")
        return

    positions = _calculate_node_positions(nodes, edges)

    fig = go.Figure()

    for edge in edges:
        source_pos = positions.get(edge["source"], (0, 0))
        target_pos = positions.get(edge["target"], (1, 1))
        color = _rel_color(edge.get("type", "default"))

        fig.add_trace(go.Scatter(
            x=[source_pos[0], target_pos[0]],
            y=[source_pos[1], target_pos[1]],
            mode='lines',
            line=dict(color=color, width=1.5),
            hoverinfo='text',
            text=edge.get("label", ""),
            showlegend=False,
        ))

    for node in nodes:
        pos = positions.get(node["id"], (0, 0))
        is_selected = node["id"] == selected_node
        size = 30 if is_selected else 20
        color = node.get("color", COLORS.PRIMARY)
        if is_selected:
            color = COLORS.TEXT_PRIMARY

        if is_selected:
            fig.add_trace(go.Scatter(
                x=[pos[0]],
                y=[pos[1]],
                mode='markers',
                marker=dict(size=size + 14, color=color, opacity=0.25),
                showlegend=False,
                hoverinfo='skip',
            ))

        fig.add_trace(go.Scatter(
            x=[pos[0]],
            y=[pos[1]],
            mode='markers+text',
            marker=dict(
                size=size,
                color=color,
                line=dict(color=COLORS.TEXT_PRIMARY, width=2 if is_selected else 1),
            ),
            text=[node["label"]],
            textposition="middle center",
            textfont=dict(size=8, color=COLORS.TEXT_PRIMARY),
            hovertemplate=f"<b>{_escape(node['label'])}</b><br>Type: {_escape(node.get('type', 'unknown'))}<extra></extra>",
            showlegend=False,
        ))

    fig.update_layout(
        height=500,
        showlegend=False,
        paper_bgcolor=_GRAPH_PAPER_BG,
        plot_bgcolor=_GRAPH_PAPER_BG,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-2, 2]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-2, 2]),
    )

    st.plotly_chart(fig, use_container_width=True, key=f"kg_canvas_{title}")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🔍 Zoom In", key="kg_zoom_in", use_container_width=True):
            st.toast("Zoom in", icon="🔍")
    with col2:
        if st.button("🔍 Zoom Out", key="kg_zoom_out", use_container_width=True):
            st.toast("Zoom out", icon="🔍")
    with col3:
        if st.button("📐 Fit View", key="kg_fit_view", use_container_width=True):
            st.toast("Fit to view", icon="📐")
    with col4:
        if st.button("🎯 Focus Selected", key="kg_focus", use_container_width=True):
            st.toast("Focusing selected node", icon="🎯")

    legend_items = [
        ("Application", COLORS.PRIMARY),
        ("Page", COLORS.SECONDARY),
        ("Component", COLORS.SUCCESS),
        ("API", COLORS.WARNING),
        ("Database", COLORS.PRIMARY),
        ("Rule", COLORS.ACCENT),
        ("Test", COLORS.INFO),
        ("Bug", COLORS.ERROR),
    ]
    legend_html = "".join(
        f'<span style="display:flex;align-items:center;gap:6px;">'
        f'<span style="width:12px;height:12px;background:{c};border-radius:50%;'
        f'{"animation:" + ANIMATIONS.PULSE + ";" if i == 0 else ""}"></span>'
        f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_SECONDARY};">{name}</span>'
        f'</span>'
        for i, (name, c) in enumerate(legend_items)
    )
    st.markdown(
        f'<div style="display:flex;flex-wrap:wrap;gap:{SPACING.SPACE_4};'
        f'justify-content:center;margin-top:{SPACING.SPACE_3};">{legend_html}</div>',
        unsafe_allow_html=True,
    )


def _calculate_node_positions(nodes: list[dict], edges: list[dict]) -> dict[str, tuple[float, float]]:
    """Calculate node positions using a simple force-directed algorithm."""
    positions = {}
    type_clusters = {
        "application": (0, 0),
        "page": (-1.5, 0),
        "component": (-1, -1),
        "api": (1, -0.5),
        "database_table": (1.5, 0),
        "business_rule": (0.5, 1),
        "test_case": (-0.5, 1),
        "bug": (1, 1),
    }

    type_indices: dict[str, int] = {}
    for node in nodes:
        node_type = node.get("type", "unknown")
        if node_type not in type_indices:
            type_indices[node_type] = 0
        index = type_indices[node_type]
        type_indices[node_type] += 1

        base_pos = type_clusters.get(node_type, (0, 0))
        x = base_pos[0] + 0.3 * (index % 3) * (1 if index % 2 else -1)
        y = base_pos[1] + 0.3 * (index // 3) * (1 if index % 2 else -1)
        positions[node["id"]] = (x, y)

    return positions


# ============================================================================
# Node Inspector (preserved signature) — premium sticky inspector
# ============================================================================

def node_inspector(node: dict[str, Any], title: str = "Node Inspector") -> None:
    """Render detailed node inspector (preserved signature) with token styling."""
    section_header(title, icon="🔍")

    if not node:
        empty_state(icon="🔍", title="No Node Selected", description="Select a node to view details.")
        return

    icon = _type_icon(node.get("type", ""))
    type_color = _type_color(node.get("type", ""))
    type_rgb = _hex_to_rgb(type_color)

    st.markdown(f"""<div style=" padding:{SPACING.SPACE_6}; background:linear-gradient(135deg, rgba({COLORS.PRIMARY_RGB},0.12), rgba({COLORS.SECONDARY_RGB},0.12)); border:1px solid rgba({type_rgb},0.35); border-radius:{BORDERS.RADIUS_LG}; margin-bottom:{SPACING.SPACE_4}; "> <div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};"> <span style="font-size:32px;">{icon}</span> <div> <h3 style="margin:0;color:{COLORS.TEXT_PRIMARY};">{_escape(node['name'])}</h3> <span style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_MUTED};">{_escape(node.get('type', 'unknown').replace('_', ' ').title())}</span> </div> </div> </div>""", unsafe_allow_html=True)

    risk_color = _risk_color(node.get("risk", "low"))
    coverage = node.get("automation_coverage", 0)
    coverage_color = _coverage_color(coverage)
    confidence = node.get("confidence", 0)
    priority = node.get("priority", "medium")
    priority_color = _priority_color(priority)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(_metric_tile(f"{coverage:.0f}%", "Coverage", coverage_color), unsafe_allow_html=True)
    with col2:
        st.markdown(_metric_tile(f"{confidence:.0f}%", "Confidence", COLORS.PRIMARY), unsafe_allow_html=True)
    with col3:
        st.markdown(_metric_tile(str(node.get('risk', 'low')).upper(), "Risk", risk_color), unsafe_allow_html=True)
    with col4:
        st.markdown(_metric_tile(str(priority).upper(), "Priority", priority_color), unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("#### 📝 Description")
    st.markdown(
        f'<div style="color:{COLORS.TEXT_SECONDARY};font-size:{TYPOGRAPHY.FONT_SIZE_BASE};">'
        f'{_escape(node.get("description", "No description available."))}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("#### 🎯 Business Purpose")
    st.markdown(
        f'<div style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_BASE};">'
        f'{_escape(node.get("business_purpose", "Not specified."))}</div>',
        unsafe_allow_html=True,
    )

    deps = node.get("dependencies", [])
    if deps:
        st.markdown("#### 🔗 Dependencies")
        for dep_id in deps:
            st.markdown(
                f'<div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.6);'
                f'border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};">'
                f'<span style="color:{COLORS.WARNING};">←</span>'
                f'<span style="color:{COLORS.TEXT_PRIMARY};margin-left:{SPACING.SPACE_2};">'
                f'{_escape(dep_id.replace("node_", "").replace("_", " ").title())}</span></div>',
                unsafe_allow_html=True,
            )


def _metric_tile(value: str, label: str, color: str) -> str:
    """Return HTML for a small centered metric tile."""
    return (
        f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);'
        f'border-radius:{BORDERS.RADIUS_MD};text-align:center;">'
        f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XL};font-weight:700;color:{color};">{value}</div>'
        f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">{label}</div>'
        f'</div>'
    )


# ============================================================================
# AI Reasoning Panel (preserved signature) — cognitive reasoning + trace
# ============================================================================

def ai_reasoning_panel(node: dict[str, Any], title: str = "AI Reasoning") -> None:
    """Render AI-powered reasoning panel (preserved signature) with token styling."""
    section_header(title, icon="💡")

    if not node:
        empty_state(icon="💡", title="No Node Selected", description="Select a node to view AI reasoning.")
        return

    from utils.knowledge_graph_data import generate_ai_reasoning
    reasoning = generate_ai_reasoning(node)

    st.markdown(f"""<div style=" padding:{SPACING.SPACE_4}; background:linear-gradient(135deg, rgba({COLORS.PRIMARY_RGB},0.15), rgba({COLORS.SECONDARY_RGB},0.15)); border:1px solid rgba({COLORS.PRIMARY_RGB},0.3); border-radius:{BORDERS.RADIUS_LG}; margin-bottom:{SPACING.SPACE_4}; "> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;margin-bottom:{SPACING.SPACE_2};">Why Exists</div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_BASE};color:{COLORS.TEXT_PRIMARY};line-height:1.5;">{_escape(reasoning['why_exists'])}</div> </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(_info_tile("Business Importance", reasoning['business_importance'], COLORS.PRIMARY), unsafe_allow_html=True)
        spacer(1)
        st.markdown(_info_tile("Dependencies", reasoning['dependencies'], COLORS.WARNING), unsafe_allow_html=True)
    with col2:
        st.markdown(_info_tile("Risk Assessment", reasoning['risk_assessment'], COLORS.ERROR), unsafe_allow_html=True)
        spacer(1)
        st.markdown(_info_tile("Automation", reasoning['automation_importance'], COLORS.SUCCESS), unsafe_allow_html=True)

    st.markdown("#### 🚀 AI Recommendation")
    st.markdown(f"""<div style=" padding:{SPACING.SPACE_4}; background:rgba({COLORS.SUCCESS_RGB},0.1); border:1px solid rgba({COLORS.SUCCESS_RGB},0.25); border-radius:{BORDERS.RADIUS_MD}; "> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_BASE};color:{COLORS.TEXT_PRIMARY};">{_escape(reasoning['recommendation'])}</div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_SECONDARY};margin-top:{SPACING.SPACE_2};">{_escape(reasoning['future_impact'])}</div> </div>""", unsafe_allow_html=True)

    st.markdown("#### 🧭 Reasoning Trace")
    for i, step in enumerate(KG_REASONING_TRACE):
        c = _semantic(step["color"])
        is_last = i == len(KG_REASONING_TRACE) - 1
        st.markdown(
            f'<div style="display:flex;gap:{SPACING.SPACE_3};margin-bottom:{0 if is_last else SPACING.SPACE_3};">'
            f'<div style="display:flex;flex-direction:column;align-items:center;">'
            f'<div style="width:32px;height:32px;border-radius:50%;background:rgba({_hex_to_rgb(c)},0.2);'
            f'display:flex;align-items:center;justify-content:center;font-size:16px;border:1px solid rgba({_hex_to_rgb(c)},0.4);'
            f'{"animation:" + ANIMATIONS.PULSE + ";" if i == 0 else ""}">{step["icon"]}</div>'
            + ("" if is_last else f'<div style="width:2px;flex:1;background:linear-gradient(180deg,{c},{COLORS.BORDER});min-height:20px;"></div>')
            + f'</div>'
            f'<div><div style="display:flex;gap:{SPACING.SPACE_3};">'
            f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_PRIMARY};font-weight:500;">{_escape(step["step"])}</span>'
            f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">{_escape(step["time"])}</span></div>'
            f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_SECONDARY};">{_escape(step["detail"])}</div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )


def _info_tile(label: str, value: str, color: str) -> str:
    return (
        f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);'
        f'border-radius:{BORDERS.RADIUS_MD};border-left:3px solid {color};">'
        f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">{label}</div>'
        f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_BASE};color:{COLORS.TEXT_PRIMARY};margin-top:4px;">{_escape(value)}</div>'
        f'</div>'
    )


# ============================================================================
# Impact Analysis Panel (preserved signature)
# ============================================================================

def impact_analysis_panel(node_id: str, title: str = "Impact Analysis") -> None:
    """Render impact analysis panel (preserved signature) with token styling."""
    section_header(title, icon="📊")

    from utils.knowledge_graph_data import get_impact_analysis
    analysis = get_impact_analysis(node_id)

    if not analysis:
        empty_state(icon="📊", title="No Impact Analysis", description="No impact analysis available.")
        return

    node = analysis["node"]
    affected = analysis["affected"]
    total = analysis["total_affected"]

    st.markdown(f"""<div style="text-align:center;padding:{SPACING.SPACE_6};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_LG};margin-bottom:{SPACING.SPACE_4};border:1px solid rgba({COLORS.PRIMARY_RGB},0.25);"> <div style="font-size:48px;font-weight:700;color:{COLORS.PRIMARY};">{total}</div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">Nodes Affected by {_escape(node['name'])}</div> </div>""", unsafe_allow_html=True)

    cat_icons = {
        "pages": "📄", "components": "🧩", "apis": "🔌",
        "business_rules": "⚖️", "test_cases": "🧪", "bugs": "🐛",
    }
    for category, cat_nodes in affected.items():
        if cat_nodes:
            category_name = category.replace("_", " ").title()
            icon = cat_icons.get(category, "📋")
            with st.expander(f"{icon} {category_name} ({len(cat_nodes)})"):
                for n in cat_nodes:
                    risk_color = _risk_color(n.get("risk", "low"))
                    st.markdown(
                        f'- **{_escape(n["name"])}** <span style="color:{risk_color};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{_escape(str(n.get("risk", "low"))).upper()}</span>',
                        unsafe_allow_html=True,
                    )


# ============================================================================
# Business Flow Explorer (preserved signature)
# ============================================================================

def business_flow_explorer(flows: list[dict[str, Any]], title: str = "Business Flows") -> None:
    """Render business flow explorer (preserved signature) with token styling."""
    section_header(title, icon="🔀")

    from utils.knowledge_graph_data import get_node_by_id

    for flow in flows:
        risk_color = _risk_color(flow.get("risk", "low"))
        coverage = flow.get("automation_coverage", 0)
        coverage_color = _coverage_color(coverage)

        with st.expander(f"🔀 {_escape(flow['name'])} ({_escape(str(flow.get('risk', 'low'))).upper()})"):
            st.markdown(f"**Description:** {_escape(flow.get('description', ''))}")
            st.markdown(f"**Coverage:** <span style='color:{coverage_color};font-weight:600;'>{coverage:.0f}%</span> <span style='color:{risk_color};'>• {_escape(str(flow.get('risk','low'))).upper()} risk</span>", unsafe_allow_html=True)

            st.markdown("**Flow Steps:**")
            steps = flow.get("steps", [])
            for i, step_id in enumerate(steps):
                snode = get_node_by_id(step_id)
                arrow = " → " if i < len(steps) - 1 else ""
                name = snode["name"] if snode else step_id
                icon = _type_icon(snode["type"]) if snode else "•"
                st.markdown(f"{icon} {_escape(name)}{arrow}", unsafe_allow_html=True)


# ============================================================================
# Graph Statistics (preserved signature)
# ============================================================================

def graph_statistics(stats: dict[str, Any], title: str = "Graph Statistics") -> None:
    """Render graph statistics dashboard (preserved signature) with token styling."""
    section_header(title, icon="📈")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Nodes", stats.get("total_nodes", 0))
    with col2:
        st.metric("Relationships", stats.get("total_relationships", 0))
    with col3:
        st.metric("Coverage", f"{stats.get('coverage', 0):.1f}%")
    with col4:
        st.metric("Confidence", f"{stats.get('confidence_score', 0):.0f}%")

    st.markdown("---")

    st.markdown("#### Nodes by Type")
    by_type = stats.get("by_type", {})
    for node_type, data in by_type.items():
        type_name = node_type.replace("_", " ").title()
        count = data.get("count", 0)
        cov = data.get("coverage", 0)
        cov_color = _coverage_color(cov)

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"**{type_name}**")
        with col2:
            st.markdown(f"Count: {count}")
        with col3:
            st.markdown(f"<span style='color:{cov_color};font-weight:600;'>Coverage: {cov}%</span>", unsafe_allow_html=True)


# ============================================================================
# AI Discoveries (preserved signature)
# ============================================================================

def ai_discoveries_panel(discoveries: list[dict[str, Any]], title: str = "AI Discoveries") -> None:
    """Render AI discoveries panel (preserved signature) with token styling."""
    section_header(title, icon="🤖")

    critical = sum(1 for d in discoveries if d.get("severity") == "critical")
    high = sum(1 for d in discoveries if d.get("severity") == "high")
    total = sum(d.get("count", 0) for d in discoveries)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Critical", critical)
    with col2:
        st.metric("High", high)
    with col3:
        st.metric("Total Issues", total)

    st.markdown("---")

    type_icons = {
        "duplicate_components": "🔄", "dead_pages": "💀", "unused_apis": "🔗",
        "broken_relationships": "⛓️", "missing_business_rules": "📜",
        "automation_gaps": "🕳️", "accessibility_issues": "♿",
        "security_risks": "🔒", "flaky_components": "📳",
    }

    for discovery in discoveries:
        icon = type_icons.get(discovery.get("type", ""), "📋")
        color = _severity_color(discovery.get("severity", "info"))
        with st.expander(
            f"{icon} {_escape(discovery['type'].replace('_', ' ').title())} ({discovery['count']})",
            expanded=discovery.get("severity") in ["critical", "high"],
        ):
            st.markdown(f"**{_escape(discovery['description'])}**")
            st.markdown(
                f'<span style="color:{color};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;">'
                f'{_escape(str(discovery.get("severity", "info"))).upper()} severity</span>',
                unsafe_allow_html=True,
            )


# ============================================================================
# AI Recommendations (preserved signature)
# ============================================================================

def ai_recommendations_panel(recommendations: list[dict[str, Any]], title: str = "AI Recommendations") -> None:
    """Render AI recommendations panel (preserved signature) with token styling."""
    section_header(title, icon="🎯")

    category_icons = {
        "tests": "🧪", "automation": "🤖", "coverage": "📊",
        "accessibility": "♿", "security": "🔒",
    }

    for rec in recommendations:
        icon = category_icons.get(rec.get("category", ""), "💡")
        priority_color = _priority_color(rec.get("priority", "medium"))

        st.markdown(f"""<div style=" padding:{SPACING.SPACE_4}; background:rgba({COLORS.SURFACE_RGB},0.6); border-left:3px solid {priority_color}; border-radius:0 {BORDERS.RADIUS_MD} {BORDERS.RADIUS_MD} 0; margin-bottom:{SPACING.SPACE_3}; "> <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:{SPACING.SPACE_2};"> <span style="font-size:16px;">{icon}</span> <span style="padding:2px 8px;background:rgba({_hex_to_rgb(priority_color)},0.2);border-radius:{BORDERS.RADIUS_SM};font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{priority_color};text-transform:uppercase;font-weight:600;">{_escape(str(rec.get('priority', 'medium')))}</span> </div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_BASE};color:{COLORS.TEXT_PRIMARY};margin-bottom:{SPACING.SPACE_2};">{_escape(rec.get('recommendation', ''))}</div> <div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_SECONDARY};">{_escape(rec.get('reason', ''))}</div> </div>""", unsafe_allow_html=True)


# ============================================================================
# Quick Actions (preserved signature) — glass buttons
# ============================================================================

def kg_quick_actions(title: str = "Quick Actions") -> None:
    """Render quick actions panel (preserved signature) with glass buttons."""
    section_header(title, icon="⚡")

    for i in range(0, len(KG_QUICK_ACTIONS), 4):
        row = KG_QUICK_ACTIONS[i:i + 4]
        cols = st.columns(len(row))
        for col, action in zip(cols, row):
            with col:
                if st.button(
                    f"{action['icon']} {action['name']}",
                    key=f"kg_action_{i}_{action['name']}",
                    use_container_width=True,
                    help=action["description"],
                ):
                    st.toast(action["description"], icon=action["icon"])


# ============================================================================
# Search (preserved signature)
# ============================================================================

def kg_search(on_search: callable = None) -> str:
    """Render knowledge graph search input (preserved signature)."""
    query = st.text_input(
        "🔍 Search knowledge graph...",
        placeholder="Search nodes, relationships, business rules...",
        label_visibility="collapsed",
        key="kg_search_input",
    )
    return query


# ============================================================================
# Mini Map (preserved signature) — fixed plotly transparent-color crash
# ============================================================================

def mini_map(graph_data: dict[str, Any], selected_node: Optional[str] = None, title: str = "Mini Map") -> None:
    """Render a mini map of the knowledge graph (preserved signature)."""
    section_header(title, icon="🗺️")

    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])
    positions = _calculate_node_positions(nodes, edges)

    fig = go.Figure()

    for edge in edges[:20]:
        source_pos = positions.get(edge["source"], (0, 0))
        target_pos = positions.get(edge["target"], (1, 1))
        fig.add_trace(go.Scatter(
            x=[source_pos[0], target_pos[0]],
            y=[source_pos[1], target_pos[1]],
            mode='lines',
            line=dict(color=COLORS.BORDER, width=1),
            showlegend=False,
            hoverinfo='skip',
        ))

    for node in nodes:
        pos = positions.get(node["id"], (0, 0))
        is_selected = node["id"] == selected_node
        fig.add_trace(go.Scatter(
            x=[pos[0]],
            y=[pos[1]],
            mode='markers',
            marker=dict(
                size=8 if is_selected else 5,
                color=node.get("color", COLORS.PRIMARY),
                opacity=1.0 if is_selected else 0.6,
            ),
            showlegend=False,
            hoverinfo='text',
            text=node["label"],
        ))

    # rgba(0,0,0,0) instead of 'transparent' for Plotly 6.x compatibility
    fig.update_layout(
        height=120,
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=5, r=5, t=5, b=5),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-2, 2]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-2, 2]),
    )

    st.plotly_chart(fig, use_container_width=True, key=f"kg_minimap_{title}")


# ============================================================================
# Coverage Map (preserved signature)
# ============================================================================

def coverage_map_panel(coverage_data: dict[str, Any], title: str = "Automation Coverage") -> None:
    """Render the automation coverage map (preserved signature) with token styling."""
    section_header(title, icon="📊")

    for category, data in coverage_data.items():
        coverage = data.get("coverage", 0)
        status = data.get("status", "unknown")
        color = {"good": COLORS.SUCCESS, "medium": COLORS.WARNING, "low": COLORS.ERROR}.get(status, COLORS.TEXT_MUTED)
        category_name = category.replace("_", " ").title()

        st.markdown(f"""<div style="margin-bottom:{SPACING.SPACE_3};"> <div style="display:flex;justify-content:space-between;margin-bottom:4px;"> <span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{category_name}</span> <span style="color:{color};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;">{coverage}%</span> </div> <div style="width:100%;height:6px;background:rgba({COLORS.SURFACE_RGB},0.8);border-radius:3px;overflow:hidden;"> <div style="width:{coverage}%;height:100%;background:{color};border-radius:3px;"></div> </div> </div>""", unsafe_allow_html=True)


# ============================================================================
# Bug Heatmap (preserved signature)
# ============================================================================

def bug_heatmap_panel(heatmap_data: dict[str, Any], title: str = "Bug Heatmap") -> None:
    """Render the bug heatmap (preserved signature) with token styling."""
    section_header(title, icon="🔥")

    tab1, tab2, tab3 = st.tabs(["Components", "APIs", "Pages"])

    def _heat_row(name: str, item: dict) -> str:
        color = _severity_color(item.get("risk", "low"))
        failures = item.get("failures", 0)
        flaky = item.get("flaky", 0)
        flaky_html = f'<span style="color:{COLORS.WARNING};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">📳 {flaky}</span>' if flaky else ""
        return (
            f'<div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.6);'
            f'border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {color};">'
            f'<div style="display:flex;justify-content:space-between;">'
            f'<span style="color:{COLORS.TEXT_PRIMARY};">{_escape(name)}</span>'
            f'<span style="color:{color};font-size:{TYPOGRAPHY.FONT_SIZE_XS};font-weight:600;">{_escape(str(item.get("risk","low"))).upper()}</span>'
            f'</div>'
            f'<div style="display:flex;gap:{SPACING.SPACE_4};margin-top:6px;">'
            f'<span style="color:{COLORS.ERROR};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">❌ {failures}</span>'
            f'{flaky_html}</div></div>'
        )

    with tab1:
        for item in heatmap_data.get("by_component", []):
            st.markdown(_heat_row(item["name"], item), unsafe_allow_html=True)
    with tab2:
        for item in heatmap_data.get("by_api", []):
            st.markdown(
                f'<div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.6);'
                f'border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {_severity_color(item.get("risk","low"))};">'
                f'<div style="display:flex;justify-content:space-between;">'
                f'<span style="color:{COLORS.SECONDARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-family:{TYPOGRAPHY.FONT_MONO};">{_escape(item["name"])}</span>'
                f'<span style="color:{_severity_color(item.get("risk","low"))};font-size:{TYPOGRAPHY.FONT_SIZE_XS};font-weight:600;">{_escape(str(item.get("risk","low"))).upper()}</span>'
                f'</div><div style="margin-top:4px;"><span style="color:{COLORS.ERROR};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">❌ {item.get("failures",0)} failures</span></div></div>',
                unsafe_allow_html=True,
            )
    with tab3:
        for item in heatmap_data.get("by_page", []):
            st.markdown(_heat_row(item["name"], item), unsafe_allow_html=True)


# ============================================================================
# Graph Timeline (preserved signature) — fixed plotly transparent-color crash
# ============================================================================

def graph_timeline_panel(timeline_data: list[dict[str, Any]], title: str = "Graph Timeline") -> None:
    """Render the knowledge graph timeline (preserved signature)."""
    section_header(title, icon="📅")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[t["date"] for t in timeline_data],
        y=[t["nodes_added"] for t in timeline_data],
        mode="lines+markers",
        name="Nodes Added",
        line=dict(color=COLORS.SUCCESS, width=2),
        marker=dict(size=8),
    ))

    fig.add_trace(go.Scatter(
        x=[t["date"] for t in timeline_data],
        y=[t["nodes_removed"] for t in timeline_data],
        mode="lines+markers",
        name="Nodes Removed",
        line=dict(color=COLORS.ERROR, width=2),
        marker=dict(size=8),
    ))

    fig.update_layout(
        height=200,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS.TEXT_PRIMARY, size=11),
        showlegend=True,
        legend=dict(font=dict(color=COLORS.TEXT_PRIMARY)),
        xaxis=dict(showgrid=False, linecolor=f"rgba({COLORS.BORDER_RGB},0.3)"),
        yaxis=dict(showgrid=True, gridcolor=f"rgba({COLORS.BORDER_RGB},0.2)"),
    )

    st.plotly_chart(fig, use_container_width=True, key=f"kg_timeline_{title}")

    st.markdown("**Version History:**")
    for t in timeline_data:
        st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_SM};margin-bottom:4px;"> <span style="color:{COLORS.SECONDARY};">v{_escape(str(t['version']))}</span> <span style="color:{COLORS.TEXT_SECONDARY};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{_escape(str(t['date']))}</span> <span style="color:{COLORS.SUCCESS};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">+{t['nodes_added']}</span> <span style="color:{COLORS.ERROR};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">-{t['nodes_removed']}</span> </div>""", unsafe_allow_html=True)


# ============================================================================
# Graph Analytics (preserved signature)
# ============================================================================

def graph_analytics_panel(analytics: dict[str, Any], title: str = "Graph Analytics") -> None:
    """Render graph analytics (preserved signature) with token styling."""
    section_header(title, icon="📈")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Nodes", f"{analytics.get('total_nodes', 0):,}")
        st.metric("Relationships", f"{analytics.get('total_relationships', 0):,}")
        st.metric("Coverage", f"{analytics.get('coverage', 0):.1f}%")
        st.metric("Automation Ready", f"{analytics.get('automation_readiness', 0):.1f}%")
    with col2:
        st.metric("Confidence", f"{analytics.get('confidence', 0)}%")
        st.metric("Risk Score", analytics.get('risk', 0))
        st.metric("Flaky Components", analytics.get('flaky_components', 0))
        st.metric("Business Flows", analytics.get('business_flows', 0))

    st.markdown("**🔴 Critical Path:**")
    path = analytics.get('critical_path', [])
    path_html = " → ".join([f"<span style='color:{COLORS.SECONDARY};'>{_escape(p)}</span>" for p in path])
    st.markdown(f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};">{path_html}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        most = analytics.get('most_connected', {})
        st.markdown(f"**🔗 Most Connected:** {_escape(str(most.get('node', 'N/A')))} ({most.get('connections', 0)} connections)")
    with col2:
        least = analytics.get('least_connected', {})
        st.markdown(f"**🔗 Least Connected:** {_escape(str(least.get('node', 'N/A')))} ({least.get('connections', 0)} connections)")


# ============================================================================
# Dependency Explorer (preserved signature)
# ============================================================================

def dependency_explorer_panel(node: dict[str, Any], dependencies: dict[str, list], title: str = "Dependencies") -> None:
    """Render dependency explorer for a node (preserved signature)."""
    section_header(title, icon="🔗")

    if not node:
        empty_state(icon="🔗", title="No Node Selected", description="Select a node to see dependencies.")
        return

    st.markdown(f"**{_escape(node.get('name', 'Unknown'))}**")

    tabs = st.tabs(["Depends On", "Required By", "Affected"])

    def _dep_row(arrow: str, color: str, name: str) -> str:
        return (
            f'<div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.6);'
            f'border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {color};">'
            f'<span style="color:{color};">{arrow}</span>'
            f'<span style="color:{COLORS.TEXT_PRIMARY};margin-left:{SPACING.SPACE_2};">{_escape(name)}</span></div>'
        )

    with tabs[0]:
        deps = node.get("dependencies", [])
        if deps:
            for dep in deps:
                st.markdown(_dep_row("←", COLORS.WARNING, dep), unsafe_allow_html=True)
        else:
            st.info("No dependencies")
    with tabs[1]:
        required = dependencies.get("required_by", [])
        if required:
            for req in required:
                st.markdown(_dep_row("→", COLORS.SUCCESS, req), unsafe_allow_html=True)
        else:
            st.info("No dependents")
    with tabs[2]:
        affected = dependencies.get("affected", [])
        if affected:
            for aff in affected:
                st.markdown(_dep_row("⚡", COLORS.ACCENT, aff), unsafe_allow_html=True)
        else:
            st.info("No affected nodes")


# ============================================================================
# Dependency Chain (NEW) — animated cognitive dependency path
# ============================================================================

def dependency_chain_panel(title: str = "Cognitive Dependency Chain") -> None:
    """Render the animated requirement-to-release dependency chain."""
    section_header(title, icon="🕸️")

    selected_id = st.session_state.get("kg_selected_node", "node_app")
    from utils.knowledge_graph_data import get_node_by_id
    selected = get_node_by_id(selected_id)
    selected_name = _escape(selected["name"]) if selected else "Selected Node"

    st.markdown(
        f'<div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};'
        f'margin-bottom:{SPACING.SPACE_3};">Tracing knowledge path from '
        f'<span style="color:{COLORS.PRIMARY};font-weight:600;">{selected_name}</span> '
        f'through the dependency graph:</div>',
        unsafe_allow_html=True,
    )

    for i, node in enumerate(KG_DEPENDENCY_CHAIN):
        c = _semantic(node["color"])
        c_rgb = _hex_to_rgb(c)
        is_last = node["level"] == len(KG_DEPENDENCY_CHAIN) - 1
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};margin-bottom:{SPACING.SPACE_1};">'
            f'<div style="width:44px;height:44px;border-radius:{BORDERS.RADIUS_MD};'
            f'background:rgba({c_rgb},0.2);display:flex;align-items:center;justify-content:center;'
            f'font-size:20px;border:1px solid rgba({c_rgb},0.4);flex-shrink:0;'
            f'{"animation:" + ANIMATIONS.PULSE + ";" if i == 0 else ""}">{node["icon"]}</div>'
            f'<div><div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;color:{c};">{_escape(node["name"])}</div>'
            f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_SECONDARY};'
            f'font-family:{TYPOGRAPHY.FONT_MONO};">{_escape(node["detail"])}</div></div>'
            f'</div>'
            + ("" if is_last else f'<div style="margin-left:22px;width:2px;height:14px;'
                f'background:linear-gradient(180deg,{c},{COLORS.BORDER});"></div>'),
            unsafe_allow_html=True,
        )


# ============================================================================
# Knowledge Health (NEW) — graph diagnostics + AI suggestions
# ============================================================================

def knowledge_health_panel(title: str = "Knowledge Health") -> None:
    """Render the knowledge graph health diagnostics panel."""
    section_header(title, icon="🩺")

    col1, col2 = st.columns(2)
    for i, item in enumerate(KG_HEALTH):
        c = _semantic(item["color"])
        bar = (
            f'<div style="height:6px;background:rgba({COLORS.BORDER_RGB},0.4);border-radius:3px;'
            f'margin-top:4px;overflow:hidden;"><div style="width:{item["score"]}%;height:100%;'
            f'background:{c};border-radius:3px;"></div></div>'
        )
        tile = (
            f'<div style="padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);'
            f'border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {c};">'
            f'<div style="display:flex;justify-content:space-between;">'
            f'<span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;">{_escape(item["label"])}</span>'
            f'<span style="color:{c};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;">{_escape(str(item["value"]))}</span></div>'
            f'<div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{_escape(item["detail"])}</div>'
            f'{bar}</div>'
        )
        with (col1 if i % 2 == 0 else col2):
            st.markdown(tile, unsafe_allow_html=True)

    st.markdown("#### 🧠 AI Suggestions")
    for sug in KG_HEALTH_SUGGESTIONS:
        c = _semantic(sug["color"])
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};'
            f'padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({_hex_to_rgb(c)},0.1);'
            f'border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {c};">'
            f'<span style="font-size:18px;">{sug["icon"]}</span>'
            f'<div><div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;color:{c};">{_escape(sug["label"])}</div>'
            f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_SECONDARY};">{_escape(sug["value"])}</div></div></div>',
            unsafe_allow_html=True,
        )


# ============================================================================
# Recommendation Panel (preserved signature)
# ============================================================================

def recommendation_panel(recommendations: list[dict[str, Any]], title: str = "AI Recommendations") -> None:
    """Render AI recommendations (preserved signature) with token styling."""
    section_header(title, icon="💡")

    for rec in recommendations:
        priority = rec.get("priority", "medium")
        color = _priority_color(priority)
        st.markdown(f"""<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-left:3px solid {color};border-radius:0 {BORDERS.RADIUS_MD} {BORDERS.RADIUS_MD} 0;margin-bottom:{SPACING.SPACE_3};"> <div style="display:flex;justify-content:space-between;margin-bottom:{SPACING.SPACE_2};"> <span style="color:{color};font-size:{TYPOGRAPHY.FONT_SIZE_XS};text-transform:uppercase;font-weight:600;">{_escape(priority)}</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{_escape(rec.get('category', ''))}</span> </div> <div style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_BASE};margin-bottom:{SPACING.SPACE_2};">{_escape(rec.get('recommendation', ''))}</div> <div style="color:{COLORS.TEXT_SECONDARY};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{_escape(rec.get('reason', ''))}</div> </div>""", unsafe_allow_html=True)


# ============================================================================
# Execution History (preserved signature)
# ============================================================================

def execution_history_panel(history: list[dict[str, Any]], title: str = "Execution History") -> None:
    """Render execution history for a node (preserved signature)."""
    section_header(title, icon="⚡")

    for item in history:
        status_color = COLORS.SUCCESS if item.get("status") == "passed" else COLORS.ERROR
        status_icon = "✅" if item.get("status") == "passed" else "❌"
        st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {status_color};"> <span style="color:{status_color};">{status_icon} {_escape(str(item.get('status', 'unknown')))}</span> <span style="color:{COLORS.TEXT_SECONDARY};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{item.get('duration', 0)}s</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{_escape(str(item.get('agent', '')))}</span> </div>""", unsafe_allow_html=True)


# ============================================================================
# Latest Changes (preserved signature)
# ============================================================================

def latest_changes_panel(changes: list[dict[str, Any]], title: str = "Latest Changes") -> None:
    """Render latest graph changes (preserved signature) with token styling."""
    section_header(title, icon="🕐")

    type_icons = {
        "node_added": "➕", "relationship_added": "🔗", "coverage_updated": "📊",
        "rule_modified": "⚙️", "test_added": "🧪",
    }

    for change in changes:
        icon = type_icons.get(change.get("type", ""), "📝")
        time_val = change.get("time", datetime.now())
        if isinstance(time_val, datetime):
            diff = datetime.now() - time_val
            if diff < timedelta(minutes=1):
                time_str = f"{int(diff.total_seconds())}s ago"
            elif diff < timedelta(hours=1):
                time_str = f"{int(diff.total_seconds() / 60)}m ago"
            else:
                time_str = f"{int(diff.total_seconds() / 3600)}h ago"
        else:
            time_str = str(time_val)

        st.markdown(f"""<div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};"> <span style="font-size:14px;">{icon}</span> <div style="flex:1;"> <div style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{_escape(change.get('item', ''))}</div> <div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{_escape(change.get('type', '').replace('_', ' '))} • {time_str}</div> </div> </div>""", unsafe_allow_html=True)


# ============================================================================
# Bottom Workspace Tabs (NEW) — lazy cognitive workspace
# ============================================================================

def bottom_workspace_tabs() -> None:
    """Render the bottom cognitive workspace tabs using shared foundation."""
    tabs = st.tabs(KG_BOTTOM_TABS)
    tab_map = dict(zip(KG_BOTTOM_TABS, tabs))

    with tab_map["Timeline"]:
        _render_timeline_tab()
    with tab_map["Relationships"]:
        _render_relationships_tab()
    with tab_map["Evidence"]:
        _render_evidence_tab()
    with tab_map["Memory"]:
        _render_memory_tab()
    with tab_map["Analytics"]:
        _render_analytics_tab()
    with tab_map["History"]:
        _render_history_tab()


def _render_timeline_tab() -> None:
    from utils.knowledge_graph_data import GRAPH_TIMELINE, LATEST_CHANGES
    graph_timeline_panel(GRAPH_TIMELINE, "Graph Timeline")
    spacer(1)
    latest_changes_panel(LATEST_CHANGES, "Latest Changes")


def _render_relationships_tab() -> None:
    from utils.knowledge_graph_data import (
        get_relationships_for_node, get_node_by_id,
        KNOWLEDGE_RELATIONSHIPS,
    )
    selected_node_id = st.session_state.kg_selected_node
    relationships = get_relationships_for_node(selected_node_id)

    st.markdown(f"### 🔗 Relationships ({len(relationships)})")

    if not relationships:
        empty_state(icon="🔗", title="No Relationships", description="No relationships found for this node.")
        return

    for rel in relationships:
        source_node = get_node_by_id(rel["source"])
        target_node = get_node_by_id(rel["target"])
        if source_node and target_node:
            color = _rel_color(rel.get("type", "default"))
            st.markdown(f"""<div style=" display:flex;align-items:center;gap:{SPACING.SPACE_3}; padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6); border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2}; border-left:3px solid {color}; "> <div style="flex:1;"> <span style="color:{COLORS.TEXT_PRIMARY};">{_escape(source_node['name'])}</span> </div> <div style=" padding:4px 8px;background:rgba({_hex_to_rgb(color)},0.2); border-radius:{BORDERS.RADIUS_SM};font-size:{TYPOGRAPHY.FONT_SIZE_XS}; color:{color};font-weight:600; "> {_escape(rel.get('label', rel.get('type', '')))} </div> <div style="flex:1;text-align:right;"> <span style="color:{COLORS.TEXT_PRIMARY};">{_escape(target_node['name'])}</span> </div> </div>""", unsafe_allow_html=True)

    spacer(1)
    st.markdown("#### 📊 Relationship Types")
    type_counts: dict[str, int] = {}
    for rel in KNOWLEDGE_RELATIONSHIPS:
        t = rel.get("type", "related_to")
        type_counts[t] = type_counts.get(t, 0) + 1
    cols = st.columns(min(len(type_counts), 4))
    for col, (t, count) in zip(cols, sorted(type_counts.items(), key=lambda x: -x[1])):
        color = _rel_color(t)
        with col:
            st.markdown(
                f'<div style="padding:{SPACING.SPACE_3};background:rgba({_hex_to_rgb(color)},0.1);'
                f'border-radius:{BORDERS.RADIUS_MD};text-align:center;border:1px solid rgba({_hex_to_rgb(color)},0.3);">'
                f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XL};font-weight:700;color:{color};">{count}</div>'
                f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">{_escape(t.replace("_"," "))}</div></div>',
                unsafe_allow_html=True,
            )


def _render_evidence_tab() -> None:
    st.markdown("### 📸 Knowledge Evidence")
    cols = st.columns(3)
    for i, ev in enumerate(KG_EVIDENCE):
        c = _semantic(ev["color"])
        with cols[i % 3]:
            st.markdown(
                f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);'
                f'border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};'
                f'border-left:3px solid {c};">'
                f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;color:{COLORS.TEXT_PRIMARY};">{_escape(ev["title"])}</div>'
                f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{c};margin-top:4px;">{ev["type"]}</div>'
                f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">{_escape(ev["size"])}</div></div>',
                unsafe_allow_html=True,
            )


def _render_memory_tab() -> None:
    st.markdown("### 🧠 Knowledge Memory")
    for i, mem in enumerate(KG_MEMORY):
        c = _semantic(mem["color"])
        is_last = i == len(KG_MEMORY) - 1
        st.markdown(
            f'<div style="display:flex;gap:{SPACING.SPACE_3};margin-bottom:{0 if is_last else SPACING.SPACE_3};">'
            f'<div style="display:flex;flex-direction:column;align-items:center;">'
            f'<div style="width:32px;height:32px;border-radius:50%;background:rgba({_hex_to_rgb(c)},0.2);'
            f'display:flex;align-items:center;justify-content:center;font-size:16px;border:1px solid rgba({_hex_to_rgb(c)},0.4);'
            f'{"animation:" + ANIMATIONS.PULSE + ";" if i == 0 else ""}">{mem["icon"]}</div>'
            + ("" if is_last else f'<div style="width:2px;flex:1;background:linear-gradient(180deg,{c},{COLORS.BORDER});min-height:20px;"></div>')
            + f'</div>'
            f'<div><div style="display:flex;gap:{SPACING.SPACE_3};">'
            f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_PRIMARY};font-weight:500;">{_escape(mem["title"])}</span>'
            f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">{_escape(mem["time"])}</span></div>'
            f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_SECONDARY};">{_escape(mem["desc"])}</div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )


def _render_analytics_tab() -> None:
    from utils.knowledge_graph_data import GRAPH_ANALYTICS, GRAPH_STATISTICS
    graph_analytics_panel(GRAPH_ANALYTICS, "Graph Analytics")
    spacer(1)
    graph_statistics(GRAPH_STATISTICS, "Graph Statistics")


def _render_history_tab() -> None:
    from utils.knowledge_graph_data import NODE_EXECUTION_HISTORY
    execution_history_panel(NODE_EXECUTION_HISTORY[:8], "Execution History")
