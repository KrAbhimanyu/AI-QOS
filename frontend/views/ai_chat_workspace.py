"""AI Chat Workspace - AI-QOS Enterprise AI Command Center."""
import streamlit as st
from components.chat_components import (
    init_chat_state,
    get_chat_data,
    set_chat_data,
    MOCK_MESSAGES,
    MOCK_MISSION_CONTEXT,
    chat_header,
    chat_action_buttons,
    chat_context_strip,
    conversation_sidebar,
    chat_message,
    typing_indicator,
    prompt_editor,
    context_panel,
    ai_knowledge_panel,
    ai_context_panel,
    mission_context_panel,
    quick_actions_grid,
    quick_actions_premium,
    prompt_library,
    ai_thinking_panel,
    bottom_workspace_tabs,
    console_viewer,
    browser_frame,
    loading_skeleton,
    message_types_legend,
    notification_toast,
)


def render_ai_chat_workspace() -> None:
    """Render the Enterprise AI Command Center chat workspace.

    Preserves the original session state, conversation history, prompt editor,
    AI reasoning, mission context, quick actions, tabs, and business logic.
    Reorganizes the surface into the premium Command Center layout:
    HeroHeader → Context Strip → Conversations | Chat | AI Context →
    Prompt Tools | Prompt Editor | AI Thinking → Bottom Workspace tabs.
    """
    init_chat_state()

    # HeroHeader - sticky enterprise command header (reuses foundation tokens)
    chat_header(
        mission_name=MOCK_MISSION_CONTEXT["mission_name"],
        mission_status=MOCK_MISSION_CONTEXT["execution_status"],
        agent=MOCK_MISSION_CONTEXT["current_agent"],
        test=MOCK_MISSION_CONTEXT["current_test"],
    )

    # Context Strip - premium horizontal live context bar
    chat_context_strip()

    # Action Buttons (Toolbar)
    chat_action_buttons()

    st.markdown("<hr style='margin: 1rem 0; border-color: #334155;'>", unsafe_allow_html=True)

    # Main Content - Three Panel Layout: Conversations | Chat | AI Context
    left_col, center_col, right_col = st.columns([1, 3, 1])

    # LEFT SIDEBAR - Conversation Workspace
    with left_col:
        conversation_sidebar()

    # CENTER CHAT PANEL
    with center_col:
        render_chat_panel()

    # RIGHT PANEL - AI Intelligence + Knowledge
    with right_col:
        ai_context_panel()
        ai_knowledge_panel()

    st.markdown("<hr style='margin: 1.5rem 0; border-color: #334155;'>", unsafe_allow_html=True)

    # Prompt Tools | Prompt Editor | AI Thinking row
    left_panel, center_panel, right_panel = st.columns([1, 2, 1])

    with left_panel:
        quick_actions_premium()

    with center_panel:
        prompt_editor()

    with right_panel:
        ai_thinking_panel()

    # Bottom Workspace - shared GlassPanel foundation with tabs
    st.markdown("<hr style='margin: 1.5rem 0; border-color: #334155;'>", unsafe_allow_html=True)
    bottom_workspace_tabs()

    # Message types legend (different badges)
    st.markdown("<hr style='margin: 1.5rem 0; border-color: #334155;'>", unsafe_allow_html=True)
    message_types_legend()


def render_chat_panel() -> None:
    """Render the chat message panel with markdown/code support."""
    # Conversation Title (token-styled)
    st.markdown(
        f"""
        <div style="
            background: rgba(30, 30, 63, 0.8);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        ">
            <div>
                <h3 style="color: #F1F5F9; margin: 0; font-size: 1rem;">💬 Login Flow Analysis</h3>
                <p style="color: #64748B; margin: 0.25rem 0 0; font-size: 0.8rem;">3 messages • Active now</p>
            </div>
            <div style="display: flex; gap: 0.5rem;">
                <span style="color: #64748B; cursor: pointer;">📌</span>
                <span style="color: #64748B; cursor: pointer;">⋮</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Scrollable chat area
    st.markdown(
        """
        <div style="
            height: 400px;
            overflow-y: auto;
            padding: 1rem;
            background: rgba(15, 15, 26, 0.5);
            border-radius: 12px;
            margin-bottom: 1rem;
        ">
        """,
        unsafe_allow_html=True,
    )

    # Render messages (preserves conversation history)
    for message in MOCK_MESSAGES:
        chat_message(
            role=message["role"],
            content=message["content"],
            timestamp=message["timestamp"],
        )

    # Show typing indicator when AI reasoning is active
    if get_chat_data("chat_ai_thinking_active", True):
        typing_indicator()

    st.markdown("</div>", unsafe_allow_html=True)

    # Context Cards
    st.markdown("<h4 style='color: #F1F5F9; margin: 1rem 0 0.75rem;'>📎 Context Cards</h4>", unsafe_allow_html=True)

    context_cards = [
        {"icon": "🎯", "name": "Mission", "desc": "E2E Regression v2.1"},
        {"icon": "⚡", "name": "Execution", "desc": "Running at 67%"},
        {"icon": "🐛", "name": "Bug", "desc": "Sidebar Hidden"},
        {"icon": "📷", "name": "Screenshot", "desc": "Dashboard"},
        {"icon": "📐", "name": "DOM", "desc": "nav#sidebar"},
        {"icon": "🔗", "name": "API", "desc": "/api/dashboard"},
    ]

    cols = st.columns(6)
    for i, card in enumerate(context_cards):
        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    text-align: center;
                    padding: 0.75rem 0.5rem;
                    background: rgba(30, 30, 63, 0.8);
                    border: 1px solid rgba(99, 102, 241, 0.2);
                    border-radius: 8px;
                    cursor: pointer;
                ">
                    <span style="font-size: 1.25rem;">{card['icon']}</span>
                    <p style="color: #F1F5F9; margin: 0.25rem 0 0; font-size: 0.7rem;">{card['name']}</p>
                    <p style="color: #64748B; margin: 0; font-size: 0.65rem;">{card['desc']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


# Command Palette Handler (preserved)
def handle_command(command: str) -> None:
    """Handle slash commands."""
    commands = {
        "/new": "Starting new conversation...",
        "/help": "Available commands: /new, /tests, /bugs, /dom, /network, /report",
        "/tests": "Here are your test cases...",
        "/bugs": "Open bugs in this mission...",
        "/dom": "Current DOM structure...",
        "/network": "Network activity...",
        "/report": "Generating report...",
        "/screenshot": "Latest screenshot analysis...",
        "/locator": "Current locator strategy...",
        "/execution": "Execution status...",
        "/history": "Conversation history...",
    }

    if command in commands:
        st.info(commands[command])
    elif command.startswith("/"):
        st.warning(f"Unknown command: {command}")
