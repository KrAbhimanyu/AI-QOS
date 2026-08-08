"""Agent Control Tower components for AI-QOS.

Enterprise AI Organization Operating Center components built on the AI-QOS
UI Foundation. All styling is derived from design tokens (themes/tokens.py)
and shared foundation components (components/shared.py). Public function names
and signatures are preserved for backward compatibility.
"""
import streamlit as st
from datetime import datetime
from typing import Optional, List, Dict, Any

from frontend.mock.agents import (
    MOCK_AGENTS,
    MOCK_EVENTS,
    MOCK_QUEUE,
    MOCK_MODELS,
    MOCK_ORG_KPIS,
    MOCK_KPI_METRICS,
    MOCK_SWARM_HIERARCHY,
    MOCK_COLLAB_EDGES,
    MOCK_MODEL_ROUTER,
    MOCK_MEMORY_UTILIZATION,
    MOCK_RESOURCE_MONITOR,
    MOCK_MISSION_HEALTH,
    MOCK_BOTTOM_TABS,
    MOCK_TIMELINE_EVENTS,
    MOCK_TASKS,
    MOCK_QUICK_ACTIONS,
)

try:
    from frontend.themes.tokens import (
        COLORS, SPACING, TYPOGRAPHY, BORDERS, SHADOWS, ANIMATIONS,
        get_status_color, get_confidence_color, get_health_color,
    )
    from frontend.components.shared import (
        glass_card, glass_panel, section_header, divider, spacer, pulse_dot,
        empty_state, metric_card, timeline_item, status_badge,
    )
    from frontend.utils.responsive import metrics_row
except ImportError:  # pragma: no cover - fallback for direct execution
    from themes.tokens import (
        COLORS, SPACING, TYPOGRAPHY, BORDERS, SHADOWS, ANIMATIONS,
        get_status_color, get_confidence_color, get_health_color,
    )
    from shared import (
        glass_card, glass_panel, section_header, divider, spacer, pulse_dot,
        empty_state, metric_card, timeline_item, status_badge,
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
}

_PRIORITY_HEX = {
    "critical": COLORS.ERROR,
    "high": COLORS.WARNING,
    "medium": COLORS.PRIMARY,
    "low": COLORS.SUCCESS,
}

_EVENT_HEX = {
    "started": COLORS.SUCCESS,
    "task": COLORS.PRIMARY,
    "completed": COLORS.SECONDARY,
    "message": COLORS.TEXT_SECONDARY,
    "retry": COLORS.WARNING,
    "learning": COLORS.ACCENT,
}

_EVENT_ICON = {
    "started": "🚀",
    "task": "📋",
    "completed": "✅",
    "message": "💬",
    "retry": "🔄",
    "learning": "🧠",
}


def _semantic(name: str) -> str:
    return _SEMANTIC_COLORS.get(name, COLORS.PRIMARY)


def _semantic_rgb(name: str) -> str:
    return _SEMANTIC_RGB.get(name, COLORS.PRIMARY_RGB)


def _status_hex(status: str) -> str:
    if status in _STATUS_HEX:
        return _STATUS_HEX[status]
    return get_status_color(status)


def _priority_hex(priority: str) -> str:
    return _PRIORITY_HEX.get(priority, COLORS.TEXT_MUTED)


def _escape(text: str) -> str:
    if text is None:
        return ""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ============================================================================
# Session State Management (preserved keys, no breaking changes)
# ============================================================================

def init_agent_state() -> None:
    """Initialize agent session state (preserved keys)."""
    defaults = {
        "agent_selected": None,
        "agent_filters": {"status": "all", "category": "all"},
        "agent_search": "",
        "agent_events": [],
        "agent_bottom_tab": "Timeline",
        "agent_swarm_heartbeat": True,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_agent_data(key: str, default: Any = None) -> Any:
    """Get agent data from session state."""
    return st.session_state.get(key, default)


def set_agent_data(key: str, value: Any) -> None:
    """Set agent data in session state."""
    st.session_state[key] = value


# ============================================================================
# Hero Header (Agent Control Tower) - sticky enterprise command header
# ============================================================================

def agent_header(
    mission: str,
    environment: str,
    running_agents: int,
    total_agents: int,
    health: int,
    exec_time: str,
) -> None:
    """Display the premium agent control tower hero header.

    Backward-compatible signature. Uses design tokens for all styling.
    Renders a sticky glass header with breadcrumb, title, status badge,
    and organization KPI chips.
    """
    health_color = get_health_color(health)
    health_rgb = _hex_to_rgb(health_color)
    stat_chips = "".join(
        f'<div style="display:flex;flex-direction:column;align-items:center;gap:2px;'
        f'padding:{SPACING.SPACE_2} {SPACING.SPACE_4};'
        f'background:rgba({COLORS.SURFACE_RGB},0.7);'
        f'border:1px solid {_GLASS_PANEL_BORDER};'
        f'border-radius:{BORDERS.RADIUS_MD};min-width:0;>'
        f'<span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};'
        f'text-transform:uppercase;letter-spacing:1px;">{_escape(k["label"])}</span>'
        f'<span style="color:{_semantic(k["color"])};font-size:{TYPOGRAPHY.FONT_SIZE_SM};'
        f'font-weight:600;display:flex;align-items:center;gap:4px;">'
        f'<span style="font-size:0.9rem;">{k["icon"]}</span>{_escape(str(k["value"]))}'
        f'</span></div>'
        for k in MOCK_ORG_KPIS
    )

    st.markdown(f"""<div style=" background:{_GLASS_PANEL_BG}; border:1px solid {_GLASS_PANEL_BORDER}; border-radius:{BORDERS.RADIUS_XL}; padding:{SPACING.SPACE_6}; margin-bottom:{SPACING.SPACE_4}; box-shadow:{SHADOWS.CARD}; position:sticky;top:0;z-index:10; backdrop-filter:blur(12px); "> <div style="display:flex;align-items:center;justify-content:space-between; flex-wrap:wrap;gap:{SPACING.SPACE_4};margin-bottom:{SPACING.SPACE_4};"> <div> <div style="display:flex;align-items:center;gap:{SPACING.SPACE_2}; margin-bottom:{SPACING.SPACE_2};"> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">🏠 Dashboard</span> <span style="color:{COLORS.TEXT_MUTED};">›</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">Agents</span> <span style="color:{COLORS.TEXT_MUTED};">›</span> <span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{_escape(mission)}</span> </div> <div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};flex-wrap:wrap;"> <h1 style="margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_2XL}; color:{COLORS.TEXT_PRIMARY};font-weight:600;"> 🤖 Agent Control Tower </h1> <span style="display:inline-flex;align-items:center;gap:{SPACING.SPACE_2}; padding:{SPACING.SPACE_1} {SPACING.SPACE_3}; background:rgba({health_rgb},0.2); color:{health_color}; border:1px solid rgba({health_rgb},0.4); border-radius:{BORDERS.RADIUS_FULL}; font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;"> <span style="width:8px;height:8px;border-radius:50%; background:{health_color}; animation:{ANIMATIONS.PULSE};"></span> Health {health}% </span> </div> </div> <div style="display:flex;align-items:center;gap:{SPACING.SPACE_2};flex-wrap:wrap;"> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM}; border:1px solid {_PANEL_BORDER};border-radius:{BORDERS.RADIUS_MD}; padding:{SPACING.SPACE_1} {SPACING.SPACE_3};" title="Search agents">🔍 Search…</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM}; border:1px solid {_PANEL_BORDER};border-radius:{BORDERS.RADIUS_MD}; padding:{SPACING.SPACE_1} {SPACING.SPACE_3};" title="Command palette">⌘K Command</span> <span style="color:{COLORS.TEXT_MUTED};font-size:1rem;cursor:pointer;" title="Notifications">🔔</span> <span style="color:{COLORS.TEXT_MUTED};font-size:1rem;cursor:pointer;" title="Fullscreen">⛶</span> </div> </div> <div style="display:flex;gap:{SPACING.SPACE_2};flex-wrap:wrap;">{stat_chips}</div> </div>""", unsafe_allow_html=True)


# ============================================================================
# KPI Strip - MetricCard grid
# ============================================================================

def kpi_strip() -> None:
    """Display the organization KPI strip as a MetricCard grid."""
    for i in range(0, len(MOCK_KPI_METRICS), 4):
        row = MOCK_KPI_METRICS[i:i + 4]
        cols = metrics_row(len(row))
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
# AI Swarm - visual organization hierarchy with heartbeat
# ============================================================================

def ai_swarm() -> None:
    """Display the AI swarm hierarchy with animated heartbeat and agent glow."""
    section_header("AI Swarm", icon="🏢")

    levels: Dict[int, list] = {}
    for agent in MOCK_SWARM_HIERARCHY:
        levels.setdefault(agent["level"], []).append(agent)

    glass_panel(title="", icon="")

    for level in sorted(levels.keys()):
        agents = levels[level]
        try:
            from frontend.utils.responsive import metrics_row
            cols = metrics_row(len(agents))
        except Exception:
            cols = st.columns(len(agents))
        for col, agent in zip(cols, agents):
            with col:
                color = _semantic(agent["color"])
                color_rgb = _semantic_rgb(agent["color"])
                running = agent["status"] == "running"
                heartbeat = f"animation:{ANIMATIONS.PULSE};" if running else ""
                glow = f"box-shadow:0 0 12px rgba({color_rgb},0.5);" if running else ""
                st.markdown(
                    f'<div style="text-align:center;padding:{SPACING.SPACE_3} {SPACING.SPACE_2};'
                    f'background:rgba({color_rgb},0.12);'
                    f'border:1px solid rgba({color_rgb},0.35);'
                    f'border-radius:{BORDERS.RADIUS_LG};{glow}{heartbeat}">'
                    f'<div style="font-size:1.5rem;margin-bottom:{SPACING.SPACE_1};">{agent["icon"]}</div>'
                    f'<div style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};'
                    f'font-weight:600;">{_escape(agent["name"])}</div>'
                    f'<div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};'
                    f'margin-top:2px;">{_escape(agent["task"])}</div>'
                    f'<div style="margin-top:{SPACING.SPACE_1};">'
                    f'<span style="width:6px;height:6px;border-radius:50%;'
                    f'background:{color};display:inline-block;"></span>'
                    f'<span style="color:{color};font-size:{TYPOGRAPHY.FONT_SIZE_XS};'
                    f'margin-left:4px;">{agent["status"]}</span>'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )
        if level < max(levels.keys()):
            st.markdown(
                f'<div style="text-align:center;color:{COLORS.TEXT_MUTED};'
                f'font-size:0.9rem;margin:{SPACING.SPACE_1} 0;">↓</div>',
                unsafe_allow_html=True,
            )


# ============================================================================
# Agent Card (preserved) - token-styled
# ============================================================================

def agent_card(agent: Dict) -> None:
    """Display an agent card (preserved signature) with token styling."""
    status_color = _status_hex(agent["status"])
    status_rgb = _hex_to_rgb(status_color)
    health_color = get_health_color(agent["health"])
    running = agent["status"] == "running"
    glow = f"box-shadow:0 0 12px rgba({status_rgb},0.4);" if running else "box-shadow:none;"
    heartbeat = f"animation:{ANIMATIONS.PULSE};" if running else ""
    opacity = "opacity:0.75;" if agent["status"] == "idle" else ""

    st.markdown(
        f'<div style="background:rgba({COLORS.SURFACE_RGB},0.8);'
        f'border:1px solid {_GLASS_PANEL_BORDER};'
        f'border-radius:{BORDERS.RADIUS_LG};padding:{SPACING.SPACE_4};'
        f'margin-bottom:{SPACING.SPACE_3};{glow}{heartbeat}{opacity}">'
        f'<div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};margin-bottom:{SPACING.SPACE_3};">'
        f'<div style="width:44px;height:44px;border-radius:{BORDERS.RADIUS_MD};'
        f'background:linear-gradient(135deg,{status_color},rgba({status_rgb},0.5));'
        f'display:flex;align-items:center;justify-content:center;font-size:1.5rem;">{agent["icon"]}</div>'
        f'<div style="flex:1;">'
        f'<div style="display:flex;align-items:center;gap:{SPACING.SPACE_2};">'
        f'<span style="color:{COLORS.TEXT_PRIMARY};font-weight:600;font-size:{TYPOGRAPHY.FONT_SIZE_BASE};">{_escape(agent["name"])}</span>'
        f'<span style="width:8px;height:8px;border-radius:50%;background:{status_color};"></span>'
        f'</div>'
        f'<p style="color:{COLORS.TEXT_MUTED};margin:0.25rem 0 0;font-size:{TYPOGRAPHY.FONT_SIZE_SM};">v{_escape(agent.get("version", "1.0.0"))} • {_escape(agent.get("role", "Agent"))}</p>'
        f'</div></div>'
        f'<div style="margin-bottom:{SPACING.SPACE_3};padding:{SPACING.SPACE_2};'
        f'background:rgba({COLORS.BORDER_RGB},0.5);border-radius:{BORDERS.RADIUS_MD};">'
        f'<p style="color:{COLORS.TEXT_MUTED};margin:0 0 {SPACING.SPACE_1};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">Current Task</p>'
        f'<p style="color:{COLORS.TEXT_PRIMARY};margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{_escape(agent["task"])}</p>'
        f'</div>'
        f'<div style="margin-bottom:{SPACING.SPACE_3};">'
        f'<p style="color:{COLORS.TEXT_MUTED};margin:0 0 {SPACING.SPACE_1};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">Current Prompt</p>'
        f'<p style="color:{COLORS.SECONDARY};margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-style:italic;">"{_escape(str(agent.get("current_prompt", "N/A"))[:40])}..."</p>'
        f'</div>'
        f'<div style="margin-bottom:{SPACING.SPACE_3};">'
        f'<div style="display:flex;justify-content:space-between;margin-bottom:{SPACING.SPACE_1};">'
        f'<span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">Progress</span>'
        f'<span style="color:{COLORS.PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_XS};font-weight:600;">{agent["progress"]}%</span>'
        f'</div>'
        f'<div style="height:4px;background:{COLORS.BORDER};border-radius:{BORDERS.RADIUS_FULL};overflow:hidden;">'
        f'<div style="width:{agent["progress"]}%;height:100%;background:linear-gradient(90deg,{COLORS.PRIMARY},{COLORS.ACCENT});border-radius:{BORDERS.RADIUS_FULL};"></div>'
        f'</div></div>'
        f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:{SPACING.SPACE_2};margin-bottom:{SPACING.SPACE_3};">'
        f'<div style="text-align:center;padding:{SPACING.SPACE_1};background:rgba({COLORS.BORDER_RGB},0.5);border-radius:{BORDERS.RADIUS_MD};">'
        f'<p style="color:{COLORS.TEXT_MUTED};margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_XS};">CPU</p>'
        f'<p style="color:{COLORS.WARNING};margin:{SPACING.SPACE_1} 0 0;font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;">{agent["cpu"]}%</p></div>'
        f'<div style="text-align:center;padding:{SPACING.SPACE_1};background:rgba({COLORS.BORDER_RGB},0.5);border-radius:{BORDERS.RADIUS_MD};">'
        f'<p style="color:{COLORS.TEXT_MUTED};margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_XS};">Memory</p>'
        f'<p style="color:{COLORS.SECONDARY};margin:{SPACING.SPACE_1} 0 0;font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;">{agent["memory"]}%</p></div>'
        f'<div style="text-align:center;padding:{SPACING.SPACE_1};background:rgba({COLORS.BORDER_RGB},0.5);border-radius:{BORDERS.RADIUS_MD};">'
        f'<p style="color:{COLORS.TEXT_MUTED};margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_XS};">Health</p>'
        f'<p style="color:{health_color};margin:{SPACING.SPACE_1} 0 0;font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;">{agent["health"]}%</p></div>'
        f'<div style="text-align:center;padding:{SPACING.SPACE_1};background:rgba({COLORS.BORDER_RGB},0.5);border-radius:{BORDERS.RADIUS_MD};">'
        f'<p style="color:{COLORS.TEXT_MUTED};margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_XS};">Confidence</p>'
        f'<p style="color:{COLORS.SUCCESS};margin:{SPACING.SPACE_1} 0 0;font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;">{agent["confidence"]}%</p></div>'
        f'</div>'
        f'<div style="display:flex;justify-content:space-between;padding-top:{SPACING.SPACE_2};border-top:1px solid {COLORS.BORDER};">'
        f'<span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">Model: {_escape(agent["model"])}</span>'
        f'<span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{_escape(agent["exec_time"])}</span>'
        f'</div></div>',
        unsafe_allow_html=True,
    )


# ============================================================================
# Agent Categories Sidebar (preserved)
# ============================================================================

def agent_categories() -> None:
    """Display agent category sidebar (preserved signature) with token styling."""
    section_header("Categories", icon="📂")
    categories = [
        {"icon": "🧠", "name": "Intelligence", "count": 5, "color": "primary"},
        {"icon": "🧪", "name": "Testing", "count": 6, "color": "success"},
        {"icon": "📝", "name": "Documentation", "count": 1, "color": "secondary"},
        {"icon": "🔐", "name": "Security", "count": 1, "color": "error"},
        {"icon": "⚡", "name": "Performance", "count": 1, "color": "warning"},
        {"icon": "🧠", "name": "Learning", "count": 1, "color": "accent"},
        {"icon": "🚀", "name": "Support", "count": 1, "color": "info"},
    ]
    for cat in categories:
        color = _semantic(cat["color"])
        color_rgb = _semantic_rgb(cat["color"])
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};'
            f'padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.5);'
            f'border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};cursor:pointer;">'
            f'<span style="font-size:1.25rem;">{cat["icon"]}</span>'
            f'<div style="flex:1;"><p style="color:{COLORS.TEXT_PRIMARY};margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_BASE};">{_escape(cat["name"])}</p></div>'
            f'<span style="background:rgba({color_rgb},0.2);color:{color};'
            f'padding:{SPACING.SPACE_1} {SPACING.SPACE_2};border-radius:{BORDERS.RADIUS_SM};'
            f'font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;">{cat["count"]}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ============================================================================
# Agent Collaboration Graph (preserved name) - animated message flow
# ============================================================================

def communication_graph() -> None:
    """Display agent collaboration graph with animated message flow (preserved signature)."""
    section_header("Agent Collaboration Graph", icon="🔗")

    total_msgs = sum(e["messages"] for e in MOCK_COLLAB_EDGES)
    active_edges = sum(1 for e in MOCK_COLLAB_EDGES if e["status"] == "active")
    st.markdown(
        f'<div style="display:flex;gap:{SPACING.SPACE_3};flex-wrap:wrap;margin-bottom:{SPACING.SPACE_3};">'
        f'<span style="display:inline-flex;align-items:center;gap:{SPACING.SPACE_1};'
        f'padding:{SPACING.SPACE_1} {SPACING.SPACE_3};background:rgba({COLORS.PRIMARY_RGB},0.15);'
        f'border:1px solid {_GLASS_PANEL_BORDER};border-radius:{BORDERS.RADIUS_FULL};'
        f'color:{COLORS.TEXT_SECONDARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">📨 {total_msgs} messages</span>'
        f'<span style="display:inline-flex;align-items:center;gap:{SPACING.SPACE_1};'
        f'padding:{SPACING.SPACE_1} {SPACING.SPACE_3};background:rgba({COLORS.SUCCESS_RGB},0.15);'
        f'border:1px solid rgba({COLORS.SUCCESS_RGB},0.4);border-radius:{BORDERS.RADIUS_FULL};'
        f'color:{COLORS.SUCCESS};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">⚡ {active_edges} active flows</span>'
        f'<span style="display:inline-flex;align-items:center;gap:{SPACING.SPACE_1};'
        f'padding:{SPACING.SPACE_1} {SPACING.SPACE_3};background:rgba({COLORS.WARNING_RGB},0.15);'
        f'border:1px solid rgba({COLORS.WARNING_RGB},0.4);border-radius:{BORDERS.RADIUS_FULL};'
        f'color:{COLORS.WARNING};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">🎯 High priority routing</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    glass_panel(title="", icon="")
    for edge in MOCK_COLLAB_EDGES:
        prio_color = _priority_hex(edge["priority"])
        active = edge["status"] == "active"
        status_dot_color = _status_hex(edge["status"])
        flow_anim = f"animation:{ANIMATIONS.PULSE};" if active else ""
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:{SPACING.SPACE_2};'
            f'padding:{SPACING.SPACE_2} {SPACING.SPACE_3};'
            f'background:rgba({COLORS.SURFACE_RGB},0.6);'
            f'border:1px solid {_PANEL_BORDER};border-left:3px solid {prio_color};'
            f'border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};">'
            f'<span style="width:8px;height:8px;border-radius:50%;background:{status_dot_color};'
            f'{flow_anim}"></span>'
            f'<div style="flex:1;">'
            f'<div style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;">'
            f'{_escape(edge["from"])} → {_escape(edge["to"])}</div>'
            f'<div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">'
            f'{edge["messages"]} msgs · {_escape(edge["priority"])} priority · {_escape(edge["status"])}</div>'
            f'</div>'
            f'<span style="color:{prio_color};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;">{edge["messages"]}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div style="margin-top:{SPACING.SPACE_3};color:{COLORS.TEXT_MUTED};'
        f'font-size:{TYPOGRAPHY.FONT_SIZE_SM};margin-bottom:{SPACING.SPACE_2};">Agent Clusters</div>',
        unsafe_allow_html=True,
    )
    clusters = ["📋 Requirement", "🔍 Application", "📐 DOM", "🎯 Locator",
                "🖥️ Frontend", "🔗 API", "📝 Docs", "🧠 Learning"]
    try:
        from frontend.utils.responsive import metrics_row
        cols = metrics_row(len(clusters))
    except Exception:
        cols = st.columns(len(clusters))
    for i, (col, name) in enumerate(zip(cols, clusters)):
        with col:
            pulse = f"animation:{ANIMATIONS.PULSE};" if i in [0, 4, 7] else ""
            st.markdown(
                f'<div style="text-align:center;padding:{SPACING.SPACE_2};'
                f'background:rgba({COLORS.PRIMARY_RGB},0.15);'
                f'border:1px solid {_GLASS_PANEL_BORDER};'
                f'border-radius:{BORDERS.RADIUS_MD};{pulse}">'
                f'<span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">'
                f'{_escape(name)}</span></div>',
                unsafe_allow_html=True,
            )


# ============================================================================
# Agent Queue (preserved)
# ============================================================================

def agent_queue() -> None:
    """Display agent queue status (preserved signature) with token styling."""
    section_header("Agent Queue", icon="📊")
    queue_items = [
        {"status": "Running", "agents": MOCK_QUEUE["running"], "color": "success", "icon": "▶️"},
        {"status": "Waiting", "agents": MOCK_QUEUE["waiting"], "color": "muted", "icon": "⏸️"},
        {"status": "Paused", "agents": MOCK_QUEUE["paused"], "color": "warning", "icon": "⏸️"},
        {"status": "Failed", "agents": MOCK_QUEUE["failed"], "color": "error", "icon": "❌"},
    ]
    for item in queue_items:
        color = _semantic(item["color"])
        with st.expander(f"{item['icon']} {item['status']} ({len(item['agents'])})", expanded=item["status"] == "Running"):
            if item["agents"]:
                for agent in item["agents"]:
                    st.markdown(
                        f'<div style="padding:{SPACING.SPACE_2} {SPACING.SPACE_3};'
                        f'background:rgba({COLORS.BORDER_RGB},0.5);'
                        f'border-left:3px solid {color};'
                        f'border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};">'
                        f'<span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{_escape(agent)}</span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    f'<p style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">None</p>',
                    unsafe_allow_html=True,
                )


# ============================================================================
# AI Model Router (preserved name: ai_model_panel) - routing table
# ============================================================================

def ai_model_panel() -> None:
    """Display AI model router panel (preserved signature) with token styling."""
    section_header("AI Model Router", icon="🧠")

    for model in MOCK_MODEL_ROUTER:
        color = _semantic(model["color"])
        conf_color = get_confidence_color(model["confidence"])
        st.markdown(
            f'<div style="background:rgba({COLORS.SURFACE_RGB},0.8);'
            f'border:1px solid {_GLASS_PANEL_BORDER};'
            f'border-left:3px solid {color};'
            f'border-radius:{BORDERS.RADIUS_MD};padding:{SPACING.SPACE_3};margin-bottom:{SPACING.SPACE_2};">'
            f'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:{SPACING.SPACE_2};">'
            f'<div style="display:flex;align-items:center;gap:{SPACING.SPACE_2};">'
            f'<span style="width:8px;height:8px;border-radius:50%;background:{color};'
            f'animation:{ANIMATIONS.PULSE};"></span>'
            f'<span style="color:{COLORS.TEXT_PRIMARY};font-weight:600;font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{_escape(model["name"])}</span>'
            f'</div>'
            f'<span style="color:{conf_color};font-size:{TYPOGRAPHY.FONT_SIZE_XS};font-weight:600;">{model["confidence"]}% conf</span>'
            f'</div>'
            f'<div style="height:5px;background:{COLORS.BORDER};border-radius:{BORDERS.RADIUS_FULL};overflow:hidden;margin-bottom:{SPACING.SPACE_2};">'
            f'<div style="width:{model["usage"]}%;height:100%;background:{color};border-radius:{BORDERS.RADIUS_FULL};"></div>'
            f'</div>'
            f'<div style="display:flex;justify-content:space-between;color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">'
            f'<span>📊 {model["requests"]} req</span>'
            f'<span>⏱️ {_escape(model["latency"])}</span>'
            f'<span>💰 {_escape(model["cost"])}</span>'
            f'</div>'
            f'<div style="color:{COLORS.TEXT_SECONDARY};font-size:{TYPOGRAPHY.FONT_SIZE_XS};margin-top:{SPACING.SPACE_1};">'
            f'→ {_escape(model["agent"])}'
            f'</div></div>',
            unsafe_allow_html=True,
        )


# ============================================================================
# Memory Utilization - animated bars
# ============================================================================

def memory_utilization() -> None:
    """Display memory utilization with animated bars."""
    section_header("Memory Utilization", icon="💾")
    glass_panel(title="", icon="")
    for mem in MOCK_MEMORY_UTILIZATION:
        color = _semantic(mem["color"])
        color_rgb = _semantic_rgb(mem["color"])
        st.markdown(
            f'<div style="margin-bottom:{SPACING.SPACE_3};">'
            f'<div style="display:flex;justify-content:space-between;margin-bottom:{SPACING.SPACE_1};">'
            f'<span style="color:{COLORS.TEXT_SECONDARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{_escape(mem["name"])}</span>'
            f'<span style="color:{color};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;">{mem["value"]}%</span>'
            f'</div>'
            f'<div style="height:6px;background:{COLORS.BORDER};border-radius:{BORDERS.RADIUS_FULL};overflow:hidden;">'
            f'<div style="width:{mem["value"]}%;height:100%;'
            f'background:linear-gradient(90deg,{color},rgba({color_rgb},0.7));'
            f'border-radius:{BORDERS.RADIUS_FULL};'
            f'transition:width {ANIMATIONS.DURATION_SLOWER} {ANIMATIONS.EASE_OUT};"></div>'
            f'</div>'
            f'<div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};margin-top:2px;">{_escape(mem["detail"])}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ============================================================================
# Resource Dashboard (preserved) - resource monitor with mock values
# ============================================================================

def resource_dashboard() -> None:
    """Display resource monitor (preserved signature) with token styling and mock values."""
    section_header("Resource Monitor", icon="📈")
    glass_panel(title="", icon="")
    for res in MOCK_RESOURCE_MONITOR:
        color = _semantic(res["color"])
        value = res["value"]
        max_val = res["max"]
        percentage = int((value / max_val) * 100)
        unit = res["unit"]
        st.markdown(
            f'<div style="margin-bottom:{SPACING.SPACE_3};">'
            f'<div style="display:flex;justify-content:space-between;margin-bottom:{SPACING.SPACE_1};">'
            f'<span style="color:{COLORS.TEXT_SECONDARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{_escape(res["name"])}</span>'
            f'<span style="color:{color};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;">{value} {unit}</span>'
            f'</div>'
            f'<div style="height:6px;background:{COLORS.BORDER};border-radius:{BORDERS.RADIUS_FULL};overflow:hidden;">'
            f'<div style="width:{percentage}%;height:100%;background:{color};border-radius:{BORDERS.RADIUS_FULL};"></div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )


# ============================================================================
# Event Stream (preserved)
# ============================================================================

def event_stream() -> None:
    """Display live event stream (preserved signature) with token styling."""
    section_header("Event Stream", icon="⚡")

    st.markdown(
        f'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:{SPACING.SPACE_3};">'
        f'<span style="display:inline-flex;align-items:center;gap:{SPACING.SPACE_2};'
        f'color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">'
        f'<span style="width:8px;height:8px;border-radius:50%;background:{COLORS.SUCCESS};'
        f'animation:{ANIMATIONS.PULSE};"></span>Live · auto-scroll</span>'
        f'<span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};'
        f'border:1px solid {_PANEL_BORDER};border-radius:{BORDERS.RADIUS_MD};'
        f'padding:{SPACING.SPACE_1} {SPACING.SPACE_2};">🔎 Filter…</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    for event in MOCK_EVENTS:
        color = _EVENT_HEX.get(event["type"], COLORS.TEXT_MUTED)
        icon = _EVENT_ICON.get(event["type"], "ℹ️")
        st.markdown(
            f'<div style="display:flex;align-items:flex-start;gap:{SPACING.SPACE_3};'
            f'padding:{SPACING.SPACE_2} 0;border-bottom:1px solid {COLORS.BORDER};">'
            f'<span style="font-size:1rem;">{icon}</span>'
            f'<div style="flex:1;">'
            f'<p style="color:{COLORS.TEXT_PRIMARY};margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{_escape(event["message"])}</p>'
            f'<p style="color:{color};margin:0.25rem 0 0;font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{_escape(event["agent"])}</p>'
            f'</div>'
            f'<span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{event["time"].strftime("%H:%M:%S")}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ============================================================================
# Mission Health (preserved)
# ============================================================================

def mission_health() -> None:
    """Display mission health metrics (preserved signature) with token styling."""
    section_header("Mission Health", icon="🏥")
    glass_panel(title="", icon="")
    col1, col2 = st.columns(2)
    for i, item in enumerate(MOCK_MISSION_HEALTH):
        color = _semantic(item["color"])
        col = col1 if i % 2 == 0 else col2
        with col:
            val = item["value"]
            suffix = "%" if isinstance(val, int) and val < 100 else ""
            st.markdown(
                f'<div style="padding:{SPACING.SPACE_3};'
                f'background:rgba({COLORS.BORDER_RGB},0.5);'
                f'border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};'
                f'border-left:3px solid {color};">'
                f'<p style="color:{COLORS.TEXT_MUTED};margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{_escape(item["label"])}</p>'
                f'<p style="color:{color};margin:0.25rem 0 0;font-size:1.25rem;font-weight:600;">{val}{suffix}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ============================================================================
# Quick Actions - glass buttons
# ============================================================================

def quick_actions() -> None:
    """Display quick action glass buttons."""
    section_header("Quick Actions", icon="⚡")
    cols = st.columns(4)
    for i, action in enumerate(MOCK_QUICK_ACTIONS):
        with cols[i % 4]:
            if st.button(
                f"{action['icon']} {action['name']}",
                key=f"qa_{action['name']}",
                width='stretch',
                help=action["description"],
            ):
                st.info(f"{action['name']}: {action['description']}")
    spacer(SPACING.SPACE_2)


# ============================================================================
# Bottom Workspace Tabs - Timeline | Tasks | Logs | Models | Tools | Metrics | Alerts | History
# ============================================================================

def bottom_workspace_tabs() -> None:
    """Display bottom workspace with lazy-rendered tab contents."""
    section_header("Workspace", icon="🧰")
    tab_objs = st.tabs(MOCK_BOTTOM_TABS)
    tab_map = dict(zip(MOCK_BOTTOM_TABS, tab_objs))

    with tab_map["Timeline"]:
        for ev in MOCK_TIMELINE_EVENTS:
            color = _semantic(ev["color"])
            color_rgb = _semantic_rgb(ev["color"])
            st.markdown(
                f'<div style="display:flex;align-items:flex-start;gap:{SPACING.SPACE_3};'
                f'padding:{SPACING.SPACE_2} 0;border-bottom:1px solid {COLORS.BORDER};">'
                f'<div style="width:36px;height:36px;border-radius:{BORDERS.RADIUS_MD};'
                f'background:rgba({color_rgb},0.15);border:1px solid rgba({color_rgb},0.4);'
                f'display:flex;align-items:center;justify-content:center;font-size:1.1rem;'
                f'animation:{ANIMATIONS.PULSE};">{ev["icon"]}</div>'
                f'<div style="flex:1;">'
                f'<div style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;">{_escape(ev["title"])}</div>'
                f'<div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{_escape(ev["desc"])}</div>'
                f'</div>'
                f'<span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{_escape(ev["time"])}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with tab_map["Tasks"]:
        for task in MOCK_TASKS:
            status_color = _status_hex(task["status"])
            prio_color = _priority_hex(task["priority"])
            st.markdown(
                f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.7);'
                f'border:1px solid {_PANEL_BORDER};border-left:3px solid {prio_color};'
                f'border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};">'
                f'<div style="display:flex;justify-content:space-between;margin-bottom:{SPACING.SPACE_1};">'
                f'<span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;">{_escape(task["task"])}</span>'
                f'<span style="color:{status_color};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{_escape(task["status"])}</span>'
                f'</div>'
                f'<div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};margin-bottom:{SPACING.SPACE_1};">'
                f'🤖 {_escape(task["agent"])} · {_escape(task["priority"])} priority</div>'
                f'<div style="height:4px;background:{COLORS.BORDER};border-radius:{BORDERS.RADIUS_FULL};overflow:hidden;">'
                f'<div style="width:{task["progress"]}%;height:100%;background:linear-gradient(90deg,{COLORS.PRIMARY},{COLORS.ACCENT});border-radius:{BORDERS.RADIUS_FULL};"></div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

    with tab_map["Logs"]:
        for ev in MOCK_TIMELINE_EVENTS:
            st.markdown(
                f'<div style="font-family:{TYPOGRAPHY.FONT_MONO};font-size:{TYPOGRAPHY.FONT_SIZE_XS};'
                f'color:{COLORS.TEXT_SECONDARY};padding:2px 0;">'
                f'<span style="color:{COLORS.TEXT_MUTED};">{_escape(ev["time"])}</span> '
                f'{ev["icon"]} {_escape(ev["title"])} — {_escape(ev["desc"])}</div>',
                unsafe_allow_html=True,
            )

    with tab_map["Models"]:
        ai_model_panel()

    with tab_map["Tools"]:
        tools = [
            {"name": "RequirementParser", "status": "active", "uses": 156},
            {"name": "WebScanner", "status": "active", "uses": 89},
            {"name": "DOMInspector", "status": "active", "uses": 234},
            {"name": "LocatorGenerator", "status": "active", "uses": 78},
            {"name": "PlaywrightRunner", "status": "active", "uses": 142},
            {"name": "PatternLearner", "status": "active", "uses": 24},
            {"name": "BugAnalyzer", "status": "active", "uses": 12},
            {"name": "ReportGenerator", "status": "idle", "uses": 0},
        ]
        for tool in tools:
            color = _status_hex(tool["status"])
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};'
                f'padding:{SPACING.SPACE_2} {SPACING.SPACE_3};'
                f'background:rgba({COLORS.SURFACE_RGB},0.7);border:1px solid {_PANEL_BORDER};'
                f'border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_1};">'
                f'<span style="width:8px;height:8px;border-radius:50%;background:{color};"></span>'
                f'<span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};flex:1;">{_escape(tool["name"])}</span>'
                f'<span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{tool["uses"]} uses</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with tab_map["Metrics"]:
        for m in MOCK_KPI_METRICS[:6]:
            color = COLORS.SUCCESS if str(m["trend"]).startswith("+") else COLORS.ERROR if str(m["trend"]).startswith("-") else COLORS.TEXT_MUTED
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;padding:{SPACING.SPACE_2} 0;'
                f'border-bottom:1px solid {COLORS.BORDER};">'
                f'<span style="color:{COLORS.TEXT_SECONDARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{_escape(m["title"])}</span>'
                f'<span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;">{m["value"]}</span>'
                f'<span style="color:{color};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{_escape(m["trend"])}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with tab_map["Alerts"]:
        alerts = [
            {"level": "warning", "msg": "Redis memory at 88%", "time": "10:05:00"},
            {"level": "error", "msg": "Sidebar visibility test failed", "time": "10:03:30"},
            {"level": "info", "msg": "Pattern learned: Login flow", "time": "10:05:00"},
        ]
        for a in alerts:
            color = _semantic(a["level"])
            st.markdown(
                f'<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.7);'
                f'border:1px solid {_PANEL_BORDER};border-left:3px solid {color};'
                f'border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};">'
                f'<div style="color:{color};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;text-transform:uppercase;">{_escape(a["level"])}</div>'
                f'<div style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};margin-top:2px;">{_escape(a["msg"])}</div>'
                f'<div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};margin-top:2px;">{_escape(a["time"])}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with tab_map["History"]:
        for ev in reversed(MOCK_TIMELINE_EVENTS):
            st.markdown(
                f'<div style="display:flex;gap:{SPACING.SPACE_2};padding:{SPACING.SPACE_2} 0;'
                f'border-bottom:1px solid {COLORS.BORDER};">'
                f'<span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};min-width:0;">{_escape(ev["time"])}</span>'
                f'<span style="font-size:1rem;">{ev["icon"]}</span>'
                f'<span style="color:{COLORS.TEXT_SECONDARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{_escape(ev["title"])} — {_escape(ev["desc"])}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ============================================================================
# Agent Drawer (preserved)
# ============================================================================

def agent_drawer(agent: Dict) -> None:
    """Display detailed agent drawer (preserved signature) with token styling."""
    with st.expander(f"🤖 {_escape(agent['name'])} Details", expanded=True):
        status_color = _status_hex(agent["status"])
        status_rgb = _hex_to_rgb(status_color)
        st.markdown(
            f'<div style="background:linear-gradient(135deg,rgba({COLORS.PRIMARY_RGB},0.2) 0%,{COLORS.SURFACE} 100%);'
            f'border:1px solid {_GLASS_PANEL_BORDER};border-radius:{BORDERS.RADIUS_LG};'
            f'padding:{SPACING.SPACE_6};margin-bottom:{SPACING.SPACE_4};text-align:center;">'
            f'<span style="font-size:4rem;display:block;margin-bottom:{SPACING.SPACE_4};">{agent["icon"]}</span>'
            f'<h3 style="color:{COLORS.TEXT_PRIMARY};margin:0;">{_escape(agent["name"])}</h3>'
            f'<p style="color:{COLORS.TEXT_MUTED};margin:0.5rem 0 0;">Agent DNA • v{_escape(agent.get("version", "1.0.0"))}</p>'
            f'<span style="display:inline-flex;align-items:center;gap:{SPACING.SPACE_1};'
            f'margin-top:{SPACING.SPACE_2};padding:{SPACING.SPACE_1} {SPACING.SPACE_3};'
            f'background:rgba({status_rgb},0.2);color:{status_color};'
            f'border-radius:{BORDERS.RADIUS_FULL};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">'
            f'<span style="width:6px;height:6px;border-radius:50%;background:{status_color};"></span>'
            f'{_escape(agent["status"].title())}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Role:** {_escape(agent.get('role', 'Agent'))}")
            st.markdown(f"**Version:** {_escape(agent.get('version', '1.0.0'))}")
            st.markdown(f"**Status:** {_escape(agent['status'].title())}")
        with col2:
            st.markdown(f"**Owner:** {_escape(agent.get('owner', 'AI-QOS Team'))}")
            st.markdown(f"**Last Updated:** {_escape(agent.get('last_updated', 'N/A'))}")
            st.markdown(f"**Health Score:** {agent['health']}%")

        st.markdown("**🎯 Capabilities:**")
        for cap in agent.get('capabilities', ['No capabilities defined']):
            st.markdown(f"- {_escape(cap)}")

        st.markdown("**🔐 Permissions:**")
        for perm in agent.get('permissions', ['Read']):
            st.markdown(f"- {_escape(perm)}")

        st.markdown("**🛠️ Tools:**")
        for tool in agent.get('tools', [agent.get('tool', 'N/A')]):
            st.markdown(f"- {_escape(tool)}")

        st.markdown("**🔗 Dependencies:**")
        deps = agent.get('dependencies', [])
        if deps:
            for dep in deps:
                st.markdown(f"- {_escape(dep)}")
        else:
            st.markdown("- No dependencies")

        st.markdown("**📋 Current Context:**")
        st.markdown(f"- **Mission:** {_escape(agent['mission'])}")
        st.markdown(f"- **Current Task:** {_escape(agent['task'])}")
        st.markdown(f"- **Progress:** {agent['progress']}%")
        st.markdown(f"- **Confidence:** {agent['confidence']}%")
        st.markdown(f"- **Current Tool:** {_escape(agent['tool'])}")
        st.markdown(f"- **Current Model:** {_escape(agent['model'])}")

        st.markdown("**💾 Memory Usage:**")
        st.markdown(f"- {_escape(agent.get('memory_usage', 'N/A'))}")

        st.markdown("**💭 Current Prompt:**")
        st.code(agent.get('current_prompt', 'No current prompt'), language=None)

        st.markdown("**📊 Execution History:**")
        st.json({
            "total_tasks": 24,
            "completed": 18,
            "failed": 1,
            "avg_duration": "45s",
            "success_rate": "94%",
        })

        st.markdown("**🏥 Health History:**")
        st.line_chart({"health": [95, 92, 94, 96, 95, 98, 97]})

