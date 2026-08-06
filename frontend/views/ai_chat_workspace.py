"""AI Chat Workspace - AI-QOS."""
import streamlit as st
from components.chat_components import (
    init_chat_state,
    get_chat_data,
    set_chat_data,
    MOCK_MESSAGES,
    MOCK_MISSION_CONTEXT,
    chat_header,
    chat_action_buttons,
    conversation_sidebar,
    chat_message,
    typing_indicator,
    prompt_editor,
    context_panel,
    ai_knowledge_panel,
    quick_actions_grid,
    prompt_library,
    ai_thinking_panel,
)


def render_ai_chat_workspace() -> None:
    """Render the AI Chat Workspace page."""
    init_chat_state()
    
    # Page Header
    chat_header(
        mission_name=MOCK_MISSION_CONTEXT["mission_name"],
        mission_status=MOCK_MISSION_CONTEXT["execution_status"],
        agent=MOCK_MISSION_CONTEXT["current_agent"],
        test=MOCK_MISSION_CONTEXT["current_test"],
    )
    
    # Action Buttons
    chat_action_buttons()
    
    st.markdown("<hr style='margin: 1rem 0; border-color: #334155;'>", unsafe_allow_html=True)
    
    # Main Content - Three Panel Layout
    left_col, center_col, right_col = st.columns([1, 3, 1])
    
    # LEFT SIDEBAR
    with left_col:
        conversation_sidebar()
    
    # CENTER CHAT PANEL
    with center_col:
        render_chat_panel()
    
    # RIGHT CONTEXT PANEL
    with right_col:
        context_panel()
        ai_knowledge_panel()
        ai_thinking_panel()
    
    # Bottom Prompt Bar
    st.markdown("<hr style='margin: 1.5rem 0; border-color: #334155;'>", unsafe_allow_html=True)
    
    # Quick Actions and Prompt Library
    left_panel, right_panel = st.columns(2)
    
    with left_panel:
        quick_actions_grid()
    
    with right_panel:
        prompt_library()
    
    # Prompt Editor
    prompt_editor()


def render_chat_panel() -> None:
    """Render the chat message panel."""
    # Conversation Title
    st.markdown(
        """
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
    
    # Render messages
    for message in MOCK_MESSAGES:
        chat_message(
            role=message["role"],
            content=message["content"],
            timestamp=message["timestamp"],
        )
    
    # Show typing indicator occasionally
    # typing_indicator()
    
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
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    for i, card in enumerate(context_cards):
        col = [col1, col2, col3, col4, col5, col6][i]
        with col:
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


# Command Palette Handler
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
