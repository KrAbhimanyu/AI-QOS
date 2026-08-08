"""AI Chat Workspace components for AI-QOS.

Enterprise AI Command Center components built on the AI-QOS UI Foundation.
All styling is derived from design tokens (themes/tokens.py) and shared
foundation components (components/shared.py). Public function names and
signatures are preserved for backward compatibility.
"""
import streamlit as st
from datetime import datetime
from typing import Optional, List, Dict, Any

from frontend.mock.chat import (
    MOCK_CONVERSATIONS,
    MOCK_MESSAGES,
    MOCK_MISSION_CONTEXT,
    MOCK_QUICK_ACTIONS,
    MOCK_PROMPT_TEMPLATES,
    MOCK_HERO_STATS,
    MOCK_CONTEXT_STRIP,
    MOCK_AI_THINKING_STAGES,
    MOCK_AI_CONTEXT,
    MOCK_MISSION_PANEL,
    MOCK_KNOWLEDGE_PANEL,
    MOCK_BOTTOM_TABS,
    MOCK_CONSOLE_LOGS,
    MOCK_BROWSER_FRAME,
    MOCK_SLASH_COMMANDS,
    MOCK_PROMPT_VARIABLES,
    MOCK_PROMPT_EDITOR_TOOLS,
    MOCK_MESSAGE_TYPE_EXAMPLES,
    MOCK_QUICK_ACTIONS_PREMIUM,
)

try:
    from frontend.themes.tokens import (
        COLORS, SPACING, TYPOGRAPHY, BORDERS, SHADOWS, ANIMATIONS, STYLES,
        get_status_color, get_confidence_color,
    )
    from frontend.components.shared import (
        glass_card, glass_panel, section_header, divider, spacer, pulse_dot,
        empty_state, notification as shared_notification, metric_card,
        timeline_item,
    )
except ImportError:  # pragma: no cover - fallback for direct execution
    from themes.tokens import (
        COLORS, SPACING, TYPOGRAPHY, BORDERS, SHADOWS, ANIMATIONS, STYLES,
        get_status_color, get_confidence_color,
    )
    from shared import (
        glass_card, glass_panel, section_header, divider, spacer, pulse_dot,
        empty_state, notification as shared_notification, metric_card,
        timeline_item,
    )


# ============================================================================
# Token shortcuts
# ============================================================================

# Map semantic names -> design token hex colors for accent badges
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

# RGB strings for rgba() composition. Where the token system exposes an
# RGB triple constant we use it; otherwise we derive the triple from the hex
# token so no color value is hardcoded here.
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

# Glass panel background used across chat panels
_GLASS_PANEL_BG = f"linear-gradient(135deg, {COLORS.SURFACE} 0%, rgba({COLORS.PRIMARY_RGB}, 0.12) 100%)"
_GLASS_PANEL_BORDER = f"rgba({COLORS.PRIMARY_RGB}, 0.25)"
_PANEL_BORDER = COLORS.BORDER

# Status color map for chat header / message type badges
_STATUS_HEX = {
    "Running": COLORS.SUCCESS,
    "Paused": COLORS.WARNING,
    "Paused at Review": COLORS.WARNING,
    "Completed": COLORS.PRIMARY,
    "Failed": COLORS.ERROR,
    "Reasoning": COLORS.WARNING,
}


def _semantic(name: str) -> str:
    """Resolve a semantic color name to a hex token."""
    return _SEMANTIC_COLORS.get(name, COLORS.PRIMARY)


def _semantic_rgb(name: str) -> str:
    """Resolve a semantic color name to an RGB string."""
    return _SEMANTIC_RGB.get(name, COLORS.PRIMARY_RGB)


def _status_hex(status: str) -> str:
    """Resolve a chat status string to a token hex color."""
    if status in _STATUS_HEX:
        return _STATUS_HEX[status]
    return get_status_color(status)


def _escape(text: str) -> str:
    """Escape user-provided text for safe HTML interpolation."""
    if text is None:
        return ""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ============================================================================
# Session State Management (preserved keys, no breaking changes)
# ============================================================================

def init_chat_state() -> None:
    """Initialize chat session state."""
    defaults = {
        "chat_conversations": [],
        "chat_current_conversation": None,
        "chat_messages": [],
        "chat_prompt_history": [],
        "chat_pinned": [],
        "chat_selected_context": None,
        # New, non-breaking additions for the Command Center surface
        "chat_bottom_tab": "attachments",
        "chat_prompt_text": "",
        "chat_token_count": 0,
        "chat_ai_thinking_active": True,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_chat_data(key: str, default: Any = None) -> Any:
    """Get chat data from session state."""
    return st.session_state.get(key, default)


def set_chat_data(key: str, value: Any) -> None:
    """Set chat data in session state."""
    st.session_state[key] = value


# ============================================================================
# Chat Header (HeroHeader) - sticky enterprise command header
# ============================================================================

def chat_header(
    mission_name: str,
    mission_status: str,
    agent: str,
    test: str,
) -> None:
    """Display the premium chat hero header with mission info.

    Backward-compatible signature. Uses design tokens for all styling.
    Renders a sticky hero header with breadcrumb, title, status badge,
    and live stat chips (mission / agent / model / tokens / memory /
    knowledge / confidence / status).
    """
    status_color = _status_hex(mission_status)
    status_rgb = _status_hex_rgb(mission_status)

    # Stat chips row (hero stats) - token-backed
    stat_chips = "".join(
        f"""
        <div style="display:flex;flex-direction:column;align-items:center;gap:2px;
                    padding:{SPACING.SPACE_2} {SPACING.SPACE_4};
                    background:rgba({COLORS.SURFACE_RGB},0.7);
                    border:1px solid {_GLASS_PANEL_BORDER};
                    border-radius:{BORDERS.RADIUS_MD};min-width:0;">
            <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};
                         text-transform:uppercase;letter-spacing:1px;">{s['label']}</span>
            <span style="color:{_semantic(s['color'])};font-size:{TYPOGRAPHY.FONT_SIZE_SM};
                         font-weight:600;display:flex;align-items:center;gap:4px;">
                <span style="font-size:0.9rem;">{s['icon']}</span>{_escape(s['value'])}
            </span>
        </div>
        """
        for s in MOCK_HERO_STATS
    )

    st.markdown(f"""<div style=" background:{_GLASS_PANEL_BG}; border:1px solid {_GLASS_PANEL_BORDER}; border-radius:{BORDERS.RADIUS_XL}; padding:{SPACING.SPACE_6}; margin-bottom:{SPACING.SPACE_4}; box-shadow:{SHADOWS.CARD}; position:sticky;top:0;z-index:10; backdrop-filter:blur(12px); "> <div style="display:flex;align-items:center;justify-content:space-between; flex-wrap:wrap;gap:{SPACING.SPACE_4};margin-bottom:{SPACING.SPACE_4};"> <div> <div style="display:flex;align-items:center;gap:{SPACING.SPACE_2}; margin-bottom:{SPACING.SPACE_2};"> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">🏠 Dashboard</span> <span style="color:{COLORS.TEXT_MUTED};">›</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">AI Chat</span> <span style="color:{COLORS.TEXT_MUTED};">›</span> <span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{_escape(mission_name)}</span> </div> <div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};flex-wrap:wrap;"> <h1 style="margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_2XL}; color:{COLORS.TEXT_PRIMARY};font-weight:600;"> 💬 AI Chat Workspace </h1> <span style="display:inline-flex;align-items:center;gap:{SPACING.SPACE_2}; padding:{SPACING.SPACE_1} {SPACING.SPACE_3}; background:rgba({status_rgb},0.2); color:{status_color}; border:1px solid rgba({status_rgb},0.4); border-radius:{BORDERS.RADIUS_FULL}; font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;"> <span style="width:8px;height:8px;border-radius:50%; background:{status_color}; animation:{ANIMATIONS.PULSE};"></span> {_escape(mission_status)} </span> </div> </div> <div style="display:flex;align-items:center;gap:{SPACING.SPACE_2};flex-wrap:wrap;"> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM}; border:1px solid {_PANEL_BORDER};border-radius:{BORDERS.RADIUS_MD}; padding:{SPACING.SPACE_1} {SPACING.SPACE_3};" title="Search conversations">🔍 Search…</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM}; border:1px solid {_PANEL_BORDER};border-radius:{BORDERS.RADIUS_MD}; padding:{SPACING.SPACE_1} {SPACING.SPACE_3};" title="Command palette">⌘K Command</span> <span style="color:{COLORS.TEXT_MUTED};font-size:1rem;cursor:pointer;" title="Notifications">🔔</span> <span style="color:{COLORS.TEXT_MUTED};font-size:1rem;cursor:pointer;" title="Fullscreen">⛶</span> </div> </div> <div style="display:flex;gap:{SPACING.SPACE_2};flex-wrap:wrap;">{stat_chips}</div> </div>""", unsafe_allow_html=True)


def _status_hex_rgb(status: str) -> str:
    """RGB string for a chat status for rgba composition."""
    hex_color = _status_hex(status)
    h = hex_color.lstrip('#')
    return f"{int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}"


def chat_action_buttons() -> None:
    """Display chat action buttons (Toolbar)."""
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

    with col1:
        if st.button("➕ New Chat", width='stretch', key="chat_new"):
            st.info("Starting new conversation...")
    with col2:
        if st.button("📥 Export", width='stretch', key="chat_export"):
            st.success("Chat exported successfully!")
    with col3:
        if st.button("🗑️ Clear", width='stretch', key="chat_clear"):
            st.warning("Chat cleared")
    with col4:
        st.button("🔍 Search", width='stretch', key="chat_search")
    with col5:
        st.button("⚙️ Settings", width='stretch', key="chat_settings")


# ============================================================================
# Context Strip - premium horizontal live context bar
# ============================================================================

def chat_context_strip() -> None:
    """Display the premium horizontal context strip with live badges.

    Reuses design tokens; badges composed from tokens (no duplicate styled
    components). Shows Mission / Page / DOM / URL / Step / Agent / Element /
    Coverage with live pulse indicators.
    """
    badges = "".join(
        f"""
        <span style="display:inline-flex;align-items:center;gap:{SPACING.SPACE_2};
                     padding:{SPACING.SPACE_1} {SPACING.SPACE_3};
                     background:rgba({_semantic_rgb(c['color'])},0.15);
                     border:1px solid rgba({_semantic_rgb(c['color'])},0.35);
                     border-radius:{BORDERS.RADIUS_FULL};
                     font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{_semantic(c['color'])};
                     white-space:nowrap;">
            {f'<span style="width:6px;height:6px;border-radius:50%;background:{_semantic(c["color"])};animation:{ANIMATIONS.PULSE};"></span>' if c.get('live') else ''}
            <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{_escape(c['label'])}:</span>
            <span style="font-weight:500;">{_escape(c['value'])}</span>
        </span>
        """
        for c in MOCK_CONTEXT_STRIP
    )
    st.markdown(f"""<div style="display:flex;align-items:center;gap:{SPACING.SPACE_2};flex-wrap:wrap; padding:{SPACING.SPACE_2} {SPACING.SPACE_4}; background:{COLORS.GLASS_LIGHT}; border:1px solid {_GLASS_PANEL_BORDER}; border-radius:{BORDERS.RADIUS_LG}; margin-bottom:{SPACING.SPACE_4}; backdrop-filter:blur(10px); overflow-x:auto;"> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM}; font-weight:600;letter-spacing:1px;text-transform:uppercase;"> 📍 Context </span> <span style="color:{COLORS.BORDER_LIGHT};">|</span> {badges} </div>""", unsafe_allow_html=True)


# ============================================================================
# Conversation Sidebar
# ============================================================================

def _conversation_card(conv: Dict[str, Any], pinned: bool = False, active: bool = False) -> str:
    """Build a single conversation card HTML from a conversation dict.

    The returned HTML is a single block with no internal blank lines, so
    Streamlit's markdown parser keeps it as one HTML block (blank lines
    would split it and render trailing lines as indented code blocks).
    """
    border_color = COLORS.PRIMARY if pinned or active else _PANEL_BORDER
    bg = f"rgba({COLORS.PRIMARY_RGB},0.10)" if pinned or active else f"rgba({COLORS.SURFACE_RGB},0.4)"
    pin_badge = (
        f'<span style="color:{COLORS.WARNING};font-size:0.7rem;">📌</span>' if pinned else ''
    )
    return (
        f'<div style="padding:{SPACING.SPACE_3} {SPACING.SPACE_4};background:{bg};'
        f'border:1px solid {border_color};border-left:3px solid {border_color};'
        f'border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};'
        f'cursor:pointer;transition:all {ANIMATIONS.DURATION_NORMAL} {ANIMATIONS.EASE_OUT};">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;">'
        f'<p style="color:{COLORS.TEXT_PRIMARY};margin:0 0 {SPACING.SPACE_1};'
        f'font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;">{_escape(conv["title"])}</p>'
        f'{pin_badge}'
        f'</div>'
        f'<p style="color:{COLORS.TEXT_SECONDARY};margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_XS};'
        f'overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{_escape(conv["preview"])}</p>'
        f'<p style="color:{COLORS.TEXT_MUTED};margin:{SPACING.SPACE_2} 0 0;'
        f'font-size:{TYPOGRAPHY.FONT_SIZE_XS};">🕘 {_escape(conv["time"])}</p>'
        f'</div>'
    )


def conversation_sidebar() -> None:
    """Display conversation history sidebar with glass styling and hover animations."""
    st.text_input(
        "Search conversations",
        placeholder="🔍 Search conversations…",
        key="chat_conv_search",
        label_visibility="collapsed",
    )
    spacer(SPACING.SPACE_3)

    # New chat action
    if st.button("➕ New Chat", width='stretch', key="conv_new_chat", type="primary"):
        st.info("Starting new conversation…")
    spacer(SPACING.SPACE_3)

    # Pinned
    section_header("Pinned", icon="📌")
    pinned = [c for c in MOCK_CONVERSATIONS if c.get("pinned")]
    if not pinned:
        empty_state(icon="📌", title="No pinned chats", description="Pin important conversations.")
    else:
        for conv in pinned:
            st.markdown(_conversation_card(conv, pinned=True), unsafe_allow_html=True)

    # Recent
    section_header("Recent", icon="🕐")
    recent = [c for c in MOCK_CONVERSATIONS if not c.get("pinned")]
    if not recent:
        empty_state(icon="📭", title="No recent chats")
    else:
        for conv in recent:
            st.markdown(_conversation_card(conv, pinned=False), unsafe_allow_html=True)

    # Mission chats
    section_header("Mission Chats", icon="🎯")
    for conv in MOCK_CONVERSATIONS[:3]:
        st.markdown(_conversation_card(conv, pinned=False), unsafe_allow_html=True)

    # Templates
    section_header("Templates", icon="📋")
    for tmpl in MOCK_PROMPT_TEMPLATES[:4]:
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};'
            f'padding:{SPACING.SPACE_2} {SPACING.SPACE_3};'
            f'background:rgba({COLORS.SURFACE_RGB},0.5);'
            f'border:1px solid {_PANEL_BORDER};'
            f'border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_1};'
            f'cursor:pointer;">'
            f'<span>{tmpl["icon"]}</span>'
            f'<span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">'
            f'{_escape(tmpl["name"])}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ============================================================================
# Chat Messages
# ============================================================================

# ============================================================================
# Chat Messages - professional conversation with markdown / code / types
# ============================================================================

# Message type metadata: badge icon, label, accent color name
_MESSAGE_TYPE_META = {
    "user": ("👤", "User", "primary"),
    "assistant": ("🤖", "Assistant", "accent"),
    "system": ("⚙️", "System", "muted"),
    "mission": ("🎯", "Mission", "primary"),
    "warning": ("⚠️", "Warning", "warning"),
    "tool": ("🔧", "Tool Output", "secondary"),
    "execution": ("⚡", "Execution", "info"),
    "knowledge": ("🧠", "Knowledge", "success"),
    "error": ("❌", "Error", "error"),
}


def _render_content(content: str) -> str:
    """Lightweight markdown-ish renderer for chat content.

    Handles fenced code blocks (```), inline `code`, bold **text**, and
    preserves newlines. User text is escaped first to prevent HTML injection.
    Newlines inside fenced code blocks are preserved as real newlines (not
    converted to <br>) so <pre> renders correctly.
    """
    import re

    escaped = _escape(content)

    # Placeholder stash for fenced code blocks so they are unaffected by
    # subsequent inline transformations and the final newline replacement.
    code_blocks: list[str] = []

    def _stash_code_block(match: "re.Match[str]") -> str:
        lang = match.group(1) or ""
        code = match.group(2)
        lang_badge = (
            f'<span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};'
            f'text-transform:uppercase;letter-spacing:1px;">{_escape(lang)}</span>'
            if lang else ''
        )
        html = (
            f'<div style="margin:{SPACING.SPACE_2} 0;border:1px solid {_PANEL_BORDER};'
            f'border-radius:{BORDERS.RADIUS_MD};overflow:hidden;">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;'
            f'padding:{SPACING.SPACE_1} {SPACING.SPACE_3};'
            f'background:rgba({COLORS.SURFACE_RGB},0.7);">{lang_badge}'
            f'<span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">📋 Copy</span></div>'
            f'<pre style="margin:0;padding:{SPACING.SPACE_3};background:{COLORS.BACKGROUND_ALT};'
            f'overflow-x:auto;font-family:{TYPOGRAPHY.FONT_MONO};font-size:{TYPOGRAPHY.FONT_SIZE_SM};'
            f'color:{COLORS.TEXT_PRIMARY};line-height:1.5;"><code>{code}</code></pre></div>'
        )
        code_blocks.append(html)
        return f"\x00CODEBLOCK{len(code_blocks) - 1}\x00"

    escaped = re.sub(
        r"```(\w*)\n?(.*?)```",
        _stash_code_block,
        escaped,
        flags=re.DOTALL,
    )

    # Inline code: `code` (avoid touching stashed blocks)
    escaped = re.sub(
        r"`([^`]+)`",
        rf'<code style="background:rgba({COLORS.SURFACE_RGB},0.7);'
        rf'padding:1px 5px;border-radius:{BORDERS.RADIUS_SM};'
        rf'font-family:{TYPOGRAPHY.FONT_MONO};font-size:0.85em;'
        rf'color:{COLORS.SECONDARY};">\1</code>',
        escaped,
    )

    # Bold: **text**
    escaped = re.sub(
        r"\*\*([^*]+)\*\*",
        rf'<strong style="color:{COLORS.TEXT_PRIMARY};font-weight:600;">\1</strong>',
        escaped,
    )

    # Newlines -> <br> (stashed code blocks are protected by placeholders)
    escaped = escaped.replace("\n", "<br>")

    # Restore stashed code blocks
    def _restore(match: "re.Match[str]") -> str:
        return code_blocks[int(match.group(1))]

    escaped = re.sub(r"\x00CODEBLOCK(\d+)\x00", _restore, escaped)
    return escaped


def chat_message(
    role: str,
    content: str,
    timestamp: datetime,
    message_type: Optional[str] = None,
) -> None:
    """Display a chat message bubble with markdown/code support.

    Backward-compatible signature (role, content, timestamp). The optional
    ``message_type`` enriches rendering for non-user/assistant types
    (system, mission, warning, tool, execution, knowledge, error) without
    changing existing call sites.
    """
    mtype = message_type or role
    icon, label, color_name = _MESSAGE_TYPE_META.get(mtype, ("🤖", mtype, "accent"))
    accent = _semantic(color_name)
    accent_rgb = _semantic_rgb(color_name)
    ts = timestamp.strftime("%H:%M") if isinstance(timestamp, datetime) else str(timestamp)
    rendered = _render_content(content)

    is_user = (mtype == "user")
    alignment = "flex-end" if is_user else "flex-start"
    avatar_bg = (
        f"linear-gradient(135deg,{COLORS.PRIMARY},{COLORS.ACCENT})"
        if is_user else f"linear-gradient(135deg,{COLORS.PRIMARY},{COLORS.ACCENT})"
    )
    bubble_radius = "16px 16px 4px 16px" if is_user else "4px 16px 16px 16px"
    bubble_bg = (
        f"linear-gradient(135deg,{COLORS.PRIMARY},{COLORS.ACCENT})"
        if is_user else f"rgba({COLORS.SURFACE_RGB},0.85)"
    )
    bubble_text = "white" if is_user else COLORS.TEXT_PRIMARY

    type_badge = "" if is_user else (
        f'<span style="display:inline-flex;align-items:center;gap:4px;'
        f'background:rgba({accent_rgb},0.18);color:{accent};'
        f'border:1px solid rgba({accent_rgb},0.35);'
        f'border-radius:{BORDERS.RADIUS_FULL};padding:1px 8px;'
        f'font-size:{TYPOGRAPHY.FONT_SIZE_XS};font-weight:500;">'
        f'{icon} {label}</span>'
    )

    if is_user:
        st.markdown(f"""<div style="display:flex;justify-content:flex-end;margin-bottom:{SPACING.SPACE_4}; animation:fadeIn {ANIMATIONS.DURATION_NORMAL} {ANIMATIONS.EASE_OUT};"> <div style="max-width:80%;"> <div style="background:{bubble_bg};border-radius:{bubble_radius}; padding:{SPACING.SPACE_4} {SPACING.SPACE_5};box-shadow:{SHADOWS.CARD};"> <p style="color:{bubble_text};margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_BASE}; line-height:1.6;">{rendered}</p> </div> <div style="display:flex;justify-content:flex-end;gap:{SPACING.SPACE_3}; margin-top:{SPACING.SPACE_1};padding-right:{SPACING.SPACE_1};"> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS}; cursor:pointer;">📋 Copy</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS}; cursor:pointer;">✏️ Edit</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS}; cursor:pointer;">🔄 Retry</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS}; cursor:pointer;">🔖 Bookmark</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{ts}</span> </div> </div> </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div style="display:flex;gap:{SPACING.SPACE_3};margin-bottom:{SPACING.SPACE_4}; animation:fadeIn {ANIMATIONS.DURATION_NORMAL} {ANIMATIONS.EASE_OUT};"> <div style="width:36px;height:36px;border-radius:50%;background:{avatar_bg}; display:flex;align-items:center;justify-content:center;flex-shrink:0; box-shadow:{SHADOWS.GLOW_PRIMARY};">{icon}</div> <div style="flex:1;max-width:80%;"> <div style="display:flex;align-items:center;gap:{SPACING.SPACE_2}; margin-bottom:{SPACING.SPACE_1};">{type_badge}</div> <div style="background:{bubble_bg};border:1px solid {_GLASS_PANEL_BORDER}; border-radius:{bubble_radius};padding:{SPACING.SPACE_4} {SPACING.SPACE_5};"> <div style="color:{bubble_text};font-size:{TYPOGRAPHY.FONT_SIZE_BASE}; line-height:1.65;">{rendered}</div> </div> <div style="display:flex;gap:{SPACING.SPACE_3};margin-top:{SPACING.SPACE_1}; padding-left:{SPACING.SPACE_1};"> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS}; cursor:pointer;">📋 Copy</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS}; cursor:pointer;">🔄 Regenerate</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS}; cursor:pointer;">↩️ Continue</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS}; cursor:pointer;">🔖 Bookmark</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS}; cursor:pointer;">🧵 Thread</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{ts}</span> </div> </div> </div>""", unsafe_allow_html=True)


def typing_indicator() -> None:
    """Display AI typing indicator with animated dots."""
    st.markdown(f"""<div style="display:flex;gap:{SPACING.SPACE_3};margin-bottom:{SPACING.SPACE_4}; animation:fadeIn {ANIMATIONS.DURATION_NORMAL} {ANIMATIONS.EASE_OUT};"> <div style="width:36px;height:36px;border-radius:50%; background:linear-gradient(135deg,{COLORS.PRIMARY},{COLORS.ACCENT}); display:flex;align-items:center;justify-content:center;flex-shrink:0; animation:{ANIMATIONS.GLOW};">🤖</div> <div style="background:rgba({COLORS.SURFACE_RGB},0.85); border:1px solid {_GLASS_PANEL_BORDER}; border-radius:4px 16px 16px 16px; padding:{SPACING.SPACE_4} {SPACING.SPACE_6};"> <div style="display:flex;gap:{SPACING.SPACE_2};align-items:center;"> <div style="width:8px;height:8px;border-radius:50%;background:{COLORS.PRIMARY}; animation:typingBounce 1.4s infinite ease-in-out both;"></div> <div style="width:8px;height:8px;border-radius:50%;background:{COLORS.PRIMARY}; animation:typingBounce 1.4s infinite ease-in-out both;animation-delay:0.16s;"></div> <div style="width:8px;height:8px;border-radius:50%;background:{COLORS.PRIMARY}; animation:typingBounce 1.4s infinite ease-in-out both;animation-delay:0.32s;"></div> </div> </div> </div> <style> @keyframes typingBounce {{ 0%,80%,100% {{ transform: scale(0); opacity: 0.4; }} 40% {{ transform: scale(1); opacity: 1; }} }} </style>""", unsafe_allow_html=True)


# ============================================================================
# Prompt Editor - premium editor with toolbar, variables, token counter
# ============================================================================

def prompt_editor() -> None:
    """Display the premium prompt input editor.

    Backward-compatible (no args). Enriched with a toolbar (prompt library,
    variables, slash commands, attachment placeholders, voice/image/code
    placeholders), an auto-expanding area, and a token counter.
    """
    glass_panel(
        title="Prompt Editor",
        icon="✍️",
    )

    # Toolbar (prompt tools) - placeholder buttons composed from tokens
    tool_chips = "".join(
        f"""
        <span style="display:inline-flex;align-items:center;gap:4px;
                     padding:{SPACING.SPACE_1} {SPACING.SPACE_3};
                     background:rgba({COLORS.SURFACE_RGB},0.6);
                     border:1px solid {_PANEL_BORDER};
                     border-radius:{BORDERS.RADIUS_FULL};
                     font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_SECONDARY};
                     cursor:pointer;" title="{t['label']} (placeholder)">
            {t['icon']} <span style="color:{COLORS.TEXT_MUTED};">{t['label']}</span>
        </span>
        """
        for t in MOCK_PROMPT_EDITOR_TOOLS
    )
    st.markdown(f"""<div style="display:flex;gap:{SPACING.SPACE_2};flex-wrap:wrap;margin-bottom:{SPACING.SPACE_2};"> {tool_chips} </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([6, 1])

    with col1:
        prompt = st.text_area(
            "Ask AI about your automation mission...",
            height=120,
            placeholder="Ask AI about your automation mission…\n\nExamples:\n- /new - Start new chat\n- /help - Get help\n- /tests - View test cases",
            label_visibility="collapsed",
            key="prompt_input",
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀", width='stretch', help="Send message", key="prompt_send"):
            if prompt:
                st.info("Sending message to AI...")
                st.rerun()

    # Token counter + slash commands hint
    token_count = len(prompt.split()) if prompt else 0
    set_chat_data("chat_token_count", token_count)
    set_chat_data("chat_prompt_text", prompt or "")
    st.markdown(f"""<div style="display:flex;justify-content:space-between;align-items:center; margin-top:{SPACING.SPACE_2};flex-wrap:wrap;gap:{SPACING.SPACE_2};"> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};"> 💡 Tip: Use <code style="color:{COLORS.SECONDARY};">/</code> for slash commands </span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};"> 🔢 Tokens: <strong style="color:{COLORS.PRIMARY};">{token_count}</strong> / 16K </span> </div>""", unsafe_allow_html=True)

    # Suggested prompts
    section_header("Suggested Prompts", icon="💡")
    col1, col2, col3 = st.columns(3)
    suggestions = [
        "Generate a login test case",
        "Explain the sidebar failure",
        "Optimize test performance",
    ]
    for col, suggestion in zip([col1, col2, col3], suggestions):
        with col:
            if st.button(f"💬 {suggestion}", width='stretch', key=f"suggestion_{suggestion[:6]}"):
                st.info(f"Selected: {suggestion}")

    # Variables panel (composed from tokens)
    var_chips = "".join(
        f"""
        <span style="display:inline-flex;align-items:center;gap:4px;
                     padding:{SPACING.SPACE_1} {SPACING.SPACE_3};
                     background:rgba({COLORS.SECONDARY_RGB},0.15);
                     border:1px solid rgba({COLORS.SECONDARY_RGB},0.35);
                     border-radius:{BORDERS.RADIUS_FULL};
                     font-size:{TYPOGRAPHY.FONT_SIZE_XS};">
            <span style="color:{COLORS.TEXT_MUTED};">${{v['name']}}</span>
            <span style="color:{COLORS.SECONDARY};">{_escape(v['value'])}</span>
        </span>
        """
        for v in MOCK_PROMPT_VARIABLES
    )
    st.markdown(f"""<div style="margin-top:{SPACING.SPACE_3};"> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM}; font-weight:600;">🔧 Variables:</span> <div style="display:flex;gap:{SPACING.SPACE_2};flex-wrap:wrap;margin-top:{SPACING.SPACE_2};"> {var_chips} </div> </div>""", unsafe_allow_html=True)


# ============================================================================
# Mission Context Panel
# ============================================================================

def context_panel() -> None:
    """Display mission context panel (back-compatible, token-styled)."""
    glass_panel(title="Mission Context", icon="🎯")
    items = [
        ("Mission", MOCK_MISSION_CONTEXT["mission_name"], COLORS.PRIMARY),
        ("Application", MOCK_MISSION_CONTEXT["application"], COLORS.SUCCESS),
        ("Environment", MOCK_MISSION_CONTEXT["environment"], COLORS.WARNING),
        ("Current Test", MOCK_MISSION_CONTEXT["current_test"], COLORS.SECONDARY),
        ("Current Step", MOCK_MISSION_CONTEXT["current_step"], COLORS.ACCENT),
        ("Agent", MOCK_MISSION_CONTEXT["current_agent"], COLORS.PRIMARY),
        ("Browser", MOCK_MISSION_CONTEXT["current_browser"], COLORS.SUCCESS),
        ("Status", MOCK_MISSION_CONTEXT["execution_status"], COLORS.WARNING),
        ("Coverage", MOCK_MISSION_CONTEXT["coverage"], COLORS.SUCCESS),
        ("Pass Rate", MOCK_MISSION_CONTEXT["pass_rate"], COLORS.SECONDARY),
        ("URL", MOCK_MISSION_CONTEXT["current_url"], COLORS.TEXT_SECONDARY),
    ]
    rows = "".join(
        f"""
        <div style="display:flex;justify-content:space-between;padding:{SPACING.SPACE_2} 0;
                    border-bottom:1px solid {COLORS.BORDER};">
            <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{_escape(label)}</span>
            <span style="color:{color};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;">
                {_escape(value)}
            </span>
        </div>
        """
        for label, value, color in items
    )
    st.markdown(rows, unsafe_allow_html=True)


def mission_context_panel() -> None:
    """Display the enriched mission context panel for the Command Center.

    Adds execution/browser/environment/coverage/risk/connected APIs/database/
    knowledge graph/business flow on top of the existing context_panel data.
    """
    glass_panel(title="Mission Context", icon="🎯")
    m = MOCK_MISSION_PANEL
    risk_color = COLORS.WARNING if m["risk"] == "Medium" else COLORS.SUCCESS
    rows = [
        ("Mission", m["mission"], COLORS.PRIMARY),
        ("Application", m["application"], COLORS.SUCCESS),
        ("Execution", m["execution"], COLORS.WARNING),
        ("Browser", m["browser"], COLORS.SECONDARY),
        ("Environment", m["environment"], COLORS.WARNING),
        ("Coverage", m["coverage"], COLORS.SUCCESS),
        ("Execution Status", m["execution_status"], get_status_color(m["execution_status"])),
        ("Risk", m["risk"], risk_color),
        ("Connected APIs", f"{len(m['connected_apis'])} endpoints", COLORS.SECONDARY),
        ("Database", m["database"], COLORS.TEXT_SECONDARY),
        ("Knowledge Graph", m["knowledge_graph"], COLORS.PRIMARY),
        ("Business Flow", m["business_flow"], COLORS.ACCENT),
    ]
    rows_html = "".join(
        f"""
        <div style="display:flex;justify-content:space-between;padding:{SPACING.SPACE_2} 0;
                    border-bottom:1px solid {COLORS.BORDER};">
            <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{_escape(label)}</span>
            <span style="color:{color};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;">
                {_escape(value)}
            </span>
        </div>
        """
        for label, value, color in rows
    )
    st.markdown(rows_html, unsafe_allow_html=True)


# ============================================================================
# AI Knowledge Panel
# ============================================================================

def ai_knowledge_panel() -> None:
    """Display AI knowledge panel (back-compatible, token-styled)."""
    glass_panel(title="AI Knowledge", icon="🧠")
    k = MOCK_KNOWLEDGE_PANEL
    items = [
        ("📄", "Detected Pages", f"{k['detected_pages']} pages"),
        ("🔗", "Detected APIs", f"{k['detected_apis']} endpoints"),
        ("🧩", "Detected Components", f"{k['detected_components']} components"),
        ("📐", "DOM Nodes", f"{k['dom_nodes']:,} nodes"),
        ("🎯", "Current Locator", k["current_locator"]),
        ("🐛", "Latest Bug", k["latest_bug"]),
        ("📷", "Latest Screenshot", k["latest_screenshot"]),
        ("📊", "Latest Report", k["latest_report"]),
    ]
    rows = "".join(
        f"""
        <div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};
                    padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.5);
                    border:1px solid {COLORS.BORDER};border-radius:{BORDERS.RADIUS_MD};
                    margin-bottom:{SPACING.SPACE_2};cursor:pointer;">
            <span style="font-size:1.25rem;">{icon}</span>
            <div style="flex:1;">
                <p style="color:{COLORS.TEXT_MUTED};margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{_escape(label)}</p>
                <p style="color:{COLORS.TEXT_PRIMARY};margin:0.15rem 0 0;font-size:{TYPOGRAPHY.FONT_SIZE_SM};">
                    {_escape(value)}
                </p>
            </div>
        </div>
        """
        for icon, label, value in items
    )
    # Knowledge confidence bar
    conf_color = get_confidence_color(k["knowledge_confidence"])
    rows += f"""
        <div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.5);
                    border:1px solid {COLORS.BORDER};border-radius:{BORDERS.RADIUS_MD};">
            <div style="display:flex;justify-content:space-between;margin-bottom:{SPACING.SPACE_1};">
                <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">
                    Knowledge Confidence
                </span>
                <span style="color:{conf_color};font-weight:600;font-size:{TYPOGRAPHY.FONT_SIZE_XS};">
                    {k['knowledge_confidence']}%
                </span>
            </div>
            <div style="height:6px;background:{COLORS.BORDER};border-radius:{BORDERS.RADIUS_FULL};overflow:hidden;">
                <div style="width:{k['knowledge_confidence']}%;height:100%;background:{conf_color};
                            border-radius:{BORDERS.RADIUS_FULL};
                            transition:width {ANIMATIONS.DURATION_SLOWER} {ANIMATIONS.EASE_OUT};"></div>
            </div>
        </div>
    """
    st.markdown(rows, unsafe_allow_html=True)


# ============================================================================
# Quick Actions
# ============================================================================

def quick_actions_grid() -> None:
    """Display quick actions grid (back-compatible, token-styled)."""
    glass_panel(title="Quick Actions", icon="⚡")
    cols = st.columns(4)
    for i, action in enumerate(MOCK_QUICK_ACTIONS):
        with cols[i % 4]:
            st.markdown(f"""<div style="text-align:center;padding:{SPACING.SPACE_3} {SPACING.SPACE_2}; background:rgba({COLORS.SURFACE_RGB},0.5); border:1px solid {COLORS.BORDER}; border-radius:{BORDERS.RADIUS_MD}; margin-bottom:{SPACING.SPACE_2};cursor:pointer; transition:all {ANIMATIONS.DURATION_NORMAL} {ANIMATIONS.EASE_OUT};"> <span style="font-size:1.5rem;">{action['icon']}</span> <p style="color:{COLORS.TEXT_PRIMARY};margin:0.4rem 0 0.2rem; font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{_escape(action['name'])}</p> <p style="color:{COLORS.TEXT_MUTED};margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_XS};"> {_escape(action['description'])} </p> </div>""", unsafe_allow_html=True)


def quick_actions_premium() -> None:
    """Display the premium quick actions grid for the Command Center."""
    glass_panel(title="Quick Actions", icon="⚡")
    cols = st.columns(4)
    for i, action in enumerate(MOCK_QUICK_ACTIONS_PREMIUM):
        with cols[i % 4]:
            st.markdown(f"""<div style="text-align:center;padding:{SPACING.SPACE_4} {SPACING.SPACE_2}; background:linear-gradient(135deg,rgba({COLORS.SURFACE_RGB},0.6) 0%,rgba({COLORS.PRIMARY_RGB},0.08) 100%); border:1px solid {_GLASS_PANEL_BORDER}; border-radius:{BORDERS.RADIUS_MD}; margin-bottom:{SPACING.SPACE_2};cursor:pointer; transition:all {ANIMATIONS.DURATION_NORMAL} {ANIMATIONS.EASE_OUT};"> <span style="font-size:1.6rem;display:inline-block;">{action['icon']}</span> <p style="color:{COLORS.TEXT_PRIMARY};margin:0.5rem 0 0.2rem; font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;"> {_escape(action['name'])} </p> <p style="color:{COLORS.TEXT_MUTED};margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_XS};"> {_escape(action['description'])} </p> </div>""", unsafe_allow_html=True)


# ============================================================================
# Prompt Library
# ============================================================================

def prompt_library() -> None:
    """Display prompt template library (back-compatible, token-styled)."""
    glass_panel(title="Prompt Library", icon="📚")
    rows = "".join(
        f"""
        <div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};
                    padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.5);
                    border:1px solid {COLORS.BORDER};border-radius:{BORDERS.RADIUS_MD};
                    margin-bottom:{SPACING.SPACE_2};cursor:pointer;">
            <span style="font-size:1.5rem;">{template['icon']}</span>
            <div style="flex:1;min-width:0;">
                <p style="color:{COLORS.TEXT_PRIMARY};margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_SM};
                          font-weight:500;">{_escape(template['name'])}</p>
                <p style="color:{COLORS.TEXT_MUTED};margin:0.15rem 0 0;font-size:{TYPOGRAPHY.FONT_SIZE_XS};
                           overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
                    {_escape(template['prompt'][:50])}…
                </p>
            </div>
        </div>
        """
        for template in MOCK_PROMPT_TEMPLATES
    )
    st.markdown(rows, unsafe_allow_html=True)


# ============================================================================
# AI Thinking Panel (back-compatible) + enriched AI Intelligence panel
# ============================================================================

def ai_thinking_panel() -> None:
    """Display AI thinking panel (back-compatible, token-styled)."""
    st.markdown(f"""<div style=" background:linear-gradient(135deg,rgba({COLORS.PRIMARY_RGB},0.15) 0%,rgba({COLORS.SURFACE_RGB},0.95) 100%); border:1px solid {_GLASS_PANEL_BORDER}; border-radius:{BORDERS.RADIUS_XL}; padding:{SPACING.SPACE_5}; margin-bottom:{SPACING.SPACE_4}; "> <div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};margin-bottom:{SPACING.SPACE_4};"> <div style="width:36px;height:36px;border-radius:50%; background:linear-gradient(135deg,{COLORS.PRIMARY},{COLORS.ACCENT}); display:flex;align-items:center;justify-content:center;font-size:1.25rem; animation:glow 2s infinite;"></div> <h4 style="color:{COLORS.TEXT_PRIMARY};margin:0;">AI Thinking</h4> </div>""", unsafe_allow_html=True)
    thinking_items = [
        ("Current Thought", "Analyzing sidebar visibility issue…", COLORS.PRIMARY),
        ("Confidence", "94%", COLORS.SUCCESS),
        ("Reasoning", "Element has dynamic class toggle", COLORS.SECONDARY),
        ("Evidence", "3 DOM observations matched", COLORS.WARNING),
        ("Recommendation", "Add wait for class removal", COLORS.ACCENT),
        ("Next Step", "Generate updated test case", COLORS.PRIMARY),
    ]
    for label, value, color in thinking_items:
        st.markdown(f"""<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.BORDER_RGB},0.5); border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};"> <p style="color:{color};margin:0 0 {SPACING.SPACE_1};font-size:{TYPOGRAPHY.FONT_SIZE_XS}; font-weight:500;text-transform:uppercase;letter-spacing:1px;">{label}</p> <p style="color:{COLORS.TEXT_PRIMARY};margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_SM};"> {_escape(value)} </p> </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def ai_context_panel() -> None:
    """Display the enriched AI Intelligence panel for the Command Center.

    Shows current thought, reasoning, confidence, evidence, current tool,
    current agent, current model, knowledge used, memory used, business
    context, and recommendation with a live reasoning animation.
    """
    c = MOCK_AI_CONTEXT
    conf_color = get_confidence_color(c["confidence"])
    st.markdown(f"""<div style=" background:linear-gradient(135deg,rgba({COLORS.PRIMARY_RGB},0.18) 0%,rgba({COLORS.SURFACE_RGB},0.95) 100%); border:1px solid {_GLASS_PANEL_BORDER}; border-radius:{BORDERS.RADIUS_XL}; padding:{SPACING.SPACE_5}; margin-bottom:{SPACING.SPACE_4}; "> <div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};margin-bottom:{SPACING.SPACE_4};"> <div style="width:40px;height:40px;border-radius:50%; background:linear-gradient(135deg,{COLORS.PRIMARY},{COLORS.ACCENT}); display:flex;align-items:center;justify-content:center;font-size:1.35rem; box-shadow:{SHADOWS.GLOW_PRIMARY}; animation:glow 2s infinite;">🤖</div> <div> <h4 style="color:{COLORS.TEXT_PRIMARY};margin:0;">AI Intelligence</h4> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};"> Live reasoning · <span style="color:{conf_color};font-weight:600;">{c['confidence']}% confidence</span> </span> </div> </div> <div style="margin-bottom:{SPACING.SPACE_3};"> <p style="color:{COLORS.TEXT_MUTED};margin:0 0 {SPACING.SPACE_1};font-size:{TYPOGRAPHY.FONT_SIZE_XS}; text-transform:uppercase;letter-spacing:1px;">Current Thought</p> <div style="background:rgba({COLORS.PRIMARY_RGB},0.1);border:1px solid rgba({COLORS.PRIMARY_RGB},0.25); border-radius:{BORDERS.RADIUS_MD};padding:{SPACING.SPACE_3};"> <p style="color:{COLORS.TEXT_PRIMARY};margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_SM};"> {_escape(c['current_thought'])} </p> </div> </div> </div>""", unsafe_allow_html=True)
    items = [
        ("Reasoning", c["reasoning"], COLORS.SECONDARY),
        ("Evidence", c["evidence"], COLORS.WARNING),
        ("Current Tool", c["current_tool"], COLORS.PRIMARY),
        ("Current Agent", c["current_agent"], COLORS.PRIMARY),
        ("Current Model", c["current_model"], COLORS.ACCENT),
        ("Knowledge Used", c["knowledge_used"], COLORS.SUCCESS),
        ("Memory Used", c["memory_used"], COLORS.SUCCESS),
        ("Business Context", c["business_context"], COLORS.INFO),
        ("Recommendation", c["recommendation"], COLORS.ACCENT),
    ]
    for label, value, color in items:
        st.markdown(f"""<div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.BORDER_RGB},0.5); border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};"> <p style="color:{color};margin:0 0 {SPACING.SPACE_1};font-size:{TYPOGRAPHY.FONT_SIZE_XS}; font-weight:500;text-transform:uppercase;letter-spacing:1px;">{label}</p> <p style="color:{COLORS.TEXT_PRIMARY};margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_SM};"> {_escape(value)} </p> </div>""", unsafe_allow_html=True)

    # Live reasoning stages (timeline via foundation timeline_item)
    section_header("Reasoning Stages", icon="🔬")
    for stage in MOCK_AI_THINKING_STAGES:
        timeline_item(
            title=stage["stage"],
            description=stage["detail"],
            status=stage["status"],
            time=stage["status"].capitalize(),
            icon="✓" if stage["status"] == "completed" else "●" if stage["status"] == "active" else "○",
        )


# ============================================================================
# Bottom Workspace Tabs (Attachments | Mission | Browser | Console | ...)
# ============================================================================

def console_viewer(logs: Optional[List[Dict[str, Any]]] = None) -> None:
    """Display a console viewer (reuses foundation tokens)."""
    glass_panel(title="Console", icon="🖥️")
    logs = logs if logs is not None else MOCK_CONSOLE_LOGS
    level_color = {
        "info": COLORS.INFO,
        "warning": COLORS.WARNING,
        "error": COLORS.ERROR,
    }
    rows = "".join(
        f"""
        <div style="display:flex;gap:{SPACING.SPACE_2};padding:{SPACING.SPACE_2} {SPACING.SPACE_3};
                    background:rgba({COLORS.BORDER_RGB},0.4);border-radius:{BORDERS.RADIUS_SM};
                    margin-bottom:{SPACING.SPACE_1};font-family:{TYPOGRAPHY.FONT_MONO};
                    font-size:{TYPOGRAPHY.FONT_SIZE_XS};">
            <span style="color:{COLORS.TEXT_MUTED};">{log['time']}</span>
            <span style="color:{level_color.get(log['level'], COLORS.TEXT_MUTED)};
                         font-weight:600;text-transform:uppercase;">{log['level']}</span>
            <span style="color:{COLORS.TEXT_MUTED};">[{log['source']}]</span>
            <span style="color:{COLORS.TEXT_PRIMARY};">{_escape(log['message'])}</span>
        </div>
        """
        for log in logs
    )
    st.markdown(rows, unsafe_allow_html=True)


def browser_frame(frame: Optional[Dict[str, Any]] = None) -> None:
    """Display a browser frame viewer (reuses foundation tokens)."""
    f = frame if frame is not None else MOCK_BROWSER_FRAME
    glass_panel(title="Browser", icon="🌐")
    conf_color = get_confidence_color(f["confidence"])
    st.markdown(f"""<div style="border:1px solid {COLORS.BORDER};border-radius:{BORDERS.RADIUS_MD};overflow:hidden;"> <div style="display:flex;align-items:center;gap:{SPACING.SPACE_2};padding:{SPACING.SPACE_2} {SPACING.SPACE_3}; background:rgba({COLORS.SURFACE_RGB},0.7);"> <span style="color:{COLORS.ERROR};">●</span> <span style="color:{COLORS.WARNING};">●</span> <span style="color:{COLORS.SUCCESS};">●</span> <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};margin-left:{SPACING.SPACE_2}; font-family:{TYPOGRAPHY.FONT_MONO};">{_escape(f['url'])}</span> </div> <div style="padding:{SPACING.SPACE_6};background:{COLORS.BACKGROUND_ALT};min-height:160px; display:flex;align-items:center;justify-content:center;position:relative;"> <div style="position:absolute;border:2px solid {COLORS.PRIMARY};border-radius:{BORDERS.RADIUS_MD}; padding:{SPACING.SPACE_4} {SPACING.SPACE_6};background:rgba({COLORS.PRIMARY_RGB},0.15); box-shadow:{SHADOWS.GLOW_PRIMARY};"> <span style="font-size:2rem;">{f['text']}</span> </div> <span style="position:absolute;top:{SPACING.SPACE_2};right:{SPACING.SPACE_3}; color:{conf_color};font-size:{TYPOGRAPHY.FONT_SIZE_XS};font-weight:600;"> 🎯 {f['confidence']}% · {f['action']} </span> </div> <div style="padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.7); display:flex;justify-content:space-between;font-size:{TYPOGRAPHY.FONT_SIZE_XS};"> <span style="color:{COLORS.TEXT_MUTED};">Locator: <code style="color:{COLORS.SECONDARY};">{f['locator']}</code></span> <span style="color:{COLORS.TEXT_MUTED};">Role: {f['role']}</span> </div> </div>""", unsafe_allow_html=True)


def _bottom_tab_placeholder(label: str, icon: str) -> None:
    """Render a placeholder body for a bottom workspace tab using the foundation empty_state."""
    empty_state(
        icon=icon,
        title=label,
        description=f"{label} content rendered via the shared Enterprise UI Foundation. "
        f"No duplicate components — reuses GlassPanel and EmptyState.",
    )


def bottom_workspace_tabs() -> None:
    """Display the bottom workspace tab bar and active tab body.

    Uses the shared GlassPanel foundation. Tabs: Attachments | Mission |
    Browser | Console | Knowledge | Reports | History | Bookmarks | Memory.
    The active tab is stored in session state ``chat_bottom_tab``.
    """
    glass_panel(title="Workspace", icon="🧰")
    active = get_chat_data("chat_bottom_tab", "attachments")
    tab_labels = [f"{t['icon']} {t['label']}" for t in MOCK_BOTTOM_TABS]
    active_idx = next(
        (i for i, t in enumerate(MOCK_BOTTOM_TABS) if t["id"] == active), 0
    )
    selected = st.tabs(tab_labels)
    # Persist selected tab
    for i, tab in enumerate(MOCK_BOTTOM_TABS):
        with selected[i]:
            if st.session_state.get("chat_bottom_tab") != tab["id"]:
                set_chat_data("chat_bottom_tab", tab["id"])
            _render_bottom_tab_body(tab["id"], tab["label"], tab["icon"])


def _render_bottom_tab_body(tab_id: str, label: str, icon: str) -> None:
    """Render the body for a given bottom workspace tab."""
    if tab_id == "console":
        console_viewer()
        return
    if tab_id == "browser":
        browser_frame()
        return
    if tab_id == "mission":
        mission_context_panel()
        return
    if tab_id == "knowledge":
        ai_knowledge_panel()
        return
    _bottom_tab_placeholder(label, icon)


# ============================================================================
# Loading skeleton (foundation-backed)
# ============================================================================

def loading_skeleton(rows: int = 3) -> None:
    """Display a loading skeleton placeholder using tokens."""
    bars = "".join(
        f"""
        <div style="height:14px;width:{65 + (i * 10) % 30}%;
                    background:linear-gradient(90deg,rgba({COLORS.BORDER_RGB},0.4) 25%,rgba({COLORS.BORDER_RGB},0.1) 50%,rgba({COLORS.BORDER_RGB},0.4) 75%);
                    background-size:200% 100%;border-radius:{BORDERS.RADIUS_SM};
                    margin-bottom:{SPACING.SPACE_2};animation:shimmer 1.5s infinite;"></div>
        """
        for i in range(rows)
    )
    st.markdown(f"""<div style="padding:{SPACING.SPACE_4};">{bars}</div> <style>@keyframes shimmer {{0%{{background-position:200% 0;}}100%{{background-position:-200% 0;}}}}</style>""", unsafe_allow_html=True)


# ============================================================================
# Notifications (back-compatible) + message types legend
# ============================================================================

def notification_toast(message: str, type: str = "info") -> None:
    """Display notification toast (back-compatible, token-styled)."""
    # Delegate to the shared foundation notification where possible, but keep
    # the chat-specific toast styling for parity with prior call sites.
    shared_notification(message=message, notification_type=type)


def message_types_legend() -> None:
    """Display the message-type legend (different badges)."""
    glass_panel(title="Message Types", icon="🏷️")
    badges = "".join(
        f"""
        <span style="display:inline-flex;align-items:center;gap:4px;
                     padding:{SPACING.SPACE_1} {SPACING.SPACE_3};
                     background:rgba({_semantic_rgb(m['color'])},0.18);
                     color:{_semantic(m['color'])};
                     border:1px solid rgba({_semantic_rgb(m['color'])},0.35);
                     border-radius:{BORDERS.RADIUS_FULL};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">
            {m['icon']} {_escape(m['label'])}
        </span>
        """
        for m in MOCK_MESSAGE_TYPE_EXAMPLES
    )
    st.markdown(f"""<div style="display:flex;flex-wrap:wrap;gap:{SPACING.SPACE_2};">{badges}</div>""", unsafe_allow_html=True)
