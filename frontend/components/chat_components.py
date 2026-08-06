"""AI Chat Workspace components for AI-QOS."""
import streamlit as st
from datetime import datetime
from typing import Optional, List, Dict, Any


# ============================================================================
# Session State Management
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
# Mock Data
# ============================================================================

MOCK_CONVERSATIONS = [
    {"id": 1, "title": "Login Flow Analysis", "preview": "Analyzing the login authentication...", "time": "2 min ago", "pinned": True},
    {"id": 2, "title": "Dashboard Bug Discussion", "preview": "The sidebar visibility issue...", "time": "15 min ago", "pinned": False},
    {"id": 3, "title": "Test Optimization", "preview": "How can I speed up my tests...", "time": "1 hour ago", "pinned": False},
    {"id": 4, "title": "API Testing Strategy", "preview": "Best practices for API validation...", "time": "2 hours ago", "pinned": False},
    {"id": 5, "title": "Locator Generation", "preview": "Generate stable locators for...", "time": "3 hours ago", "pinned": True},
]

MOCK_MESSAGES = [
    {
        "role": "user",
        "content": "Why is the sidebar test failing?",
        "timestamp": datetime.now(),
    },
    {
        "role": "assistant",
        "content": """Based on my analysis of the execution logs, the sidebar test is failing because:

**Root Cause:**
The sidebar element has `class="hidden"` applied dynamically via JavaScript after page load.

**Evidence:**
1. DOM shows: `<nav id="sidebar" class="hidden">`
2. CSS rule: `.hidden { display: none; }`
3. The sidebar is only shown after clicking the hamburger menu

**Recommended Fix:**
```python
def test_sidebar_visible(self):
    # Click hamburger menu first
    self.click("#hamburger-menu")
    # Wait for sidebar
    self.wait_for_selector("#sidebar:not(.hidden)", timeout=5000)
    # Verify visibility
    assert self.is_visible("#sidebar")
```

Would you like me to generate the updated test case?""",
        "timestamp": datetime.now(),
    },
    {
        "role": "user",
        "content": "Yes, please generate the updated test case",
        "timestamp": datetime.now(),
    },
    {
        "role": "assistant",
        "content": """Here's the updated test case:

```python
class TestDashboard:
    """Dashboard page test suite."""
    
    def setup_method(self):
        self.page = Page()
        self.page.goto("https://demo.app/dashboard")
        self.authenticate()
    
    def test_sidebar_navigation_visible(self):
        \"\"\"Test sidebar navigation is visible after clicking hamburger menu.\"\"\"
        # Click hamburger to open sidebar
        self.page.click("#hamburger-menu")
        
        # Wait for sidebar animation to complete
        self.page.wait_for_timeout(500)
        
        # Verify sidebar is visible
        sidebar = self.page.locator("#sidebar")
        assert sidebar.is_visible(), "Sidebar should be visible"
        assert not sidebar.evaluate("el => el.classList.contains('hidden')")
        
        # Verify navigation links
        links = sidebar.locator("nav a")
        expected_links = ["Dashboard", "Profile", "Settings", "Logout"]
        for link in expected_links:
            assert links.filter(has_text=link).is_visible()
    
    def test_sidebar_navigation_functionality(self):
        \"\"\"Test sidebar navigation links work correctly.\"\"\"
        self.page.click("#hamburger-menu")
        self.page.click("#sidebar a:has-text('Profile')")
        self.page.wait_for_url("**/profile")
        assert "profile" in self.page.url
```

**Key Changes:**
1. Added hamburger menu click before checking sidebar
2. Added timeout wait for animation
3. Used more specific locator strategy
4. Added functionality test for navigation links

Should I add this to your test suite?""",
        "timestamp": datetime.now(),
    },
]

MOCK_MISSION_CONTEXT = {
    "mission_name": "E2E Regression Suite v2.1",
    "application": "AIQOS Demo",
    "environment": "Staging",
    "current_test": "Login Flow - Dashboard Access",
    "current_step": "Verify Sidebar Navigation",
    "current_agent": "Frontend Agent",
    "current_browser": "Chrome",
    "execution_status": "Paused at Review",
    "coverage": "94%",
    "pass_rate": "92.3%",
    "current_url": "https://demo.app/dashboard",
}

MOCK_QUICK_ACTIONS = [
    {"icon": "🧪", "name": "Generate Test Case", "description": "Create new test case"},
    {"icon": "📄", "name": "Generate Feature File", "description": "Create Gherkin feature"},
    {"icon": "📦", "name": "Generate Page Object", "description": "Create POM class"},
    {"icon": "❌", "name": "Explain Failure", "description": "Analyze test failure"},
    {"icon": "🎯", "name": "Explain Locator", "description": "Show locator strategy"},
    {"icon": "📐", "name": "Analyze DOM", "description": "Examine DOM structure"},
    {"icon": "🐛", "name": "Generate Bug", "description": "Create bug report"},
    {"icon": "⚡", "name": "Optimize Test", "description": "Improve test performance"},
    {"icon": "🔗", "name": "Create API Test", "description": "Generate API validation"},
    {"icon": "🗄️", "name": "SQL Validation", "description": "Create DB check"},
    {"icon": "📚", "name": "Documentation", "description": "Generate docs"},
    {"icon": "♿", "name": "Accessibility", "description": "A11y analysis"},
]

MOCK_PROMPT_TEMPLATES = [
    {"icon": "🔐", "name": "Generate Login Test", "prompt": "Generate a comprehensive login test case including..."},
    {"icon": "🔁", "name": "Generate Regression", "prompt": "Create a regression test suite for..."},
    {"icon": "💨", "name": "Generate Smoke Test", "prompt": "Create a smoke test covering critical paths..."},
    {"icon": "🐛", "name": "Explain Bug", "prompt": "Explain this bug and suggest fixes..."},
    {"icon": "⚡", "name": "Analyze Performance", "prompt": "Analyze the performance metrics and suggest..."},
    {"icon": "♿", "name": "Accessibility Review", "prompt": "Review for accessibility issues..."},
    {"icon": "🔗", "name": "API Test", "prompt": "Create API test cases for..."},
    {"icon": "📸", "name": "Screenshot Analysis", "prompt": "Analyze this screenshot and suggest..."},
]


# ============================================================================
# Chat Header
# ============================================================================

def chat_header(
    mission_name: str,
    mission_status: str,
    agent: str,
    test: str,
) -> None:
    """Display chat header with mission info."""
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, rgba(30, 30, 63, 0.95) 0%, rgba(99, 102, 241, 0.15) 100%);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 16px;
            padding: 1.25rem;
            margin-bottom: 1rem;
        ">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                        <span style="color: #64748B; font-size: 0.8rem;">🏠 Dashboard</span>
                        <span style="color: #64748B;">›</span>
                        <span style="color: #64748B; font-size: 0.8rem;">AI Chat</span>
                        <span style="color: #64748B;">›</span>
                        <span style="color: #F1F5F9; font-size: 0.8rem;">{mission_name}</span>
                    </div>
                    <h1 style="margin: 0; font-size: 1.5rem; color: #F1F5F9;">💬 AI Chat Workspace</h1>
                </div>
                
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    <div style="text-align: center; padding: 0.5rem 1rem; background: rgba(30, 30, 63, 0.8); border-radius: 8px;">
                        <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Agent</p>
                        <p style="color: #6366F1; margin: 0; font-size: 0.85rem;">{agent}</p>
                    </div>
                    <div style="text-align: center; padding: 0.5rem 1rem; background: rgba(30, 30, 63, 0.8); border-radius: 8px;">
                        <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Status</p>
                        <p style="color: #F59E0B; margin: 0; font-size: 0.85rem;">{mission_status}</p>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chat_action_buttons() -> None:
    """Display chat action buttons."""
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    
    with col1:
        if st.button("➕ New Chat", use_container_width=True):
            st.info("Starting new conversation...")
    
    with col2:
        if st.button("📥 Export", use_container_width=True):
            st.success("Chat exported successfully!")
    
    with col3:
        if st.button("🗑️ Clear", use_container_width=True):
            st.warning("Chat cleared")
    
    with col4:
        st.button("🔍 Search", use_container_width=True)
    
    with col5:
        st.button("⚙️ Settings", use_container_width=True)


# ============================================================================
# Conversation Sidebar
# ============================================================================

def conversation_sidebar() -> None:
    """Display conversation history sidebar."""
    # Pinned Section
    st.markdown("<h4 style='color: #F1F5F9; margin: 1rem 0 0.75rem;'>📌 Pinned</h4>", unsafe_allow_html=True)
    
    for conv in MOCK_CONVERSATIONS[:2]:
        if conv["pinned"]:
            st.markdown(
                f"""
                <div style="
                    padding: 0.75rem 1rem;
                    background: rgba(99, 102, 241, 0.1);
                    border: 1px solid rgba(99, 102, 241, 0.2);
                    border-radius: 8px;
                    margin-bottom: 0.5rem;
                    cursor: pointer;
                    transition: all 0.2s;
                ">
                    <p style="color: #F1F5F9; margin: 0 0 0.25rem; font-size: 0.85rem; font-weight: 500;">{conv['title']}</p>
                    <p style="color: #64748B; margin: 0; font-size: 0.75rem;">{conv['preview']}</p>
                    <p style="color: #64748B; margin: 0.5rem 0 0; font-size: 0.65rem;">{conv['time']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    
    # Recent Section
    st.markdown("<h4 style='color: #F1F5F9; margin: 1.5rem 0 0.75rem;'>🕐 Recent</h4>", unsafe_allow_html=True)
    
    for conv in MOCK_CONVERSATIONS:
        if not conv["pinned"]:
            st.markdown(
                f"""
                <div style="
                    padding: 0.75rem 1rem;
                    background: rgba(30, 30, 63, 0.5);
                    border-radius: 8px;
                    margin-bottom: 0.5rem;
                    cursor: pointer;
                    transition: all 0.2s;
                ">
                    <p style="color: #F1F5F9; margin: 0 0 0.25rem; font-size: 0.85rem;">{conv['title']}</p>
                    <p style="color: #64748B; margin: 0; font-size: 0.75rem;">{conv['preview']}</p>
                    <p style="color: #64748B; margin: 0.5rem 0 0; font-size: 0.65rem;">{conv['time']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    
    # Quick Actions
    st.markdown("<h4 style='color: #F1F5F9; margin: 1.5rem 0 0.75rem;'>⚡ Quick Actions</h4>", unsafe_allow_html=True)
    
    st.button("➕ New Chat", use_container_width=True)
    st.button("📁 Create Folder", use_container_width=True)


# ============================================================================
# Chat Messages
# ============================================================================

def chat_message(role: str, content: str, timestamp: datetime) -> None:
    """Display a chat message bubble."""
    if role == "user":
        # User message
        st.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: flex-end;
                margin-bottom: 1rem;
            ">
                <div style="
                    max-width: 80%;
                    background: linear-gradient(135deg, #6366F1, #8B5CF6);
                    border-radius: 16px 16px 4px 16px;
                    padding: 1rem 1.25rem;
                ">
                    <p style="color: white; margin: 0; font-size: 0.9rem; line-height: 1.5;">{content}</p>
                    <p style="color: rgba(255,255,255,0.7); margin: 0.5rem 0 0; font-size: 0.7rem; text-align: right;">{timestamp.strftime('%H:%M')}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Assistant message
        st.markdown(
            f"""
            <div style="
                display: flex;
                gap: 1rem;
                margin-bottom: 1rem;
            ">
                <div style="
                    width: 36px;
                    height: 36px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #6366F1, #8B5CF6);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    flex-shrink: 0;
                ">
                    <span style="font-size: 1.25rem;">🤖</span>
                </div>
                <div style="flex: 1;">
                    <div style="
                        background: rgba(30, 30, 63, 0.8);
                        border: 1px solid rgba(99, 102, 241, 0.2);
                        border-radius: 4px 16px 16px 16px;
                        padding: 1rem 1.25rem;
                    ">
                        <p style="color: #F1F5F9; margin: 0; font-size: 0.9rem; line-height: 1.6; white-space: pre-wrap;">{content}</p>
                    </div>
                    <div style="display: flex; gap: 1rem; margin-top: 0.5rem; padding-left: 0.5rem;">
                        <span style="color: #64748B; font-size: 0.7rem; cursor: pointer;">📋 Copy</span>
                        <span style="color: #64748B; font-size: 0.7rem; cursor: pointer;">✏️ Edit</span>
                        <span style="color: #64748B; font-size: 0.7rem; cursor: pointer;">🔄 Retry</span>
                        <span style="color: #64748B; font-size: 0.7rem; cursor: pointer;">🔖 Bookmark</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def typing_indicator() -> None:
    """Display AI typing indicator."""
    st.markdown(
        """
        <div style="
            display: flex;
            gap: 1rem;
            margin-bottom: 1rem;
        ">
            <div style="
                width: 36px;
                height: 36px;
                border-radius: 50%;
                background: linear-gradient(135deg, #6366F1, #8B5CF6);
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
            ">
                <span style="font-size: 1.25rem;">🤖</span>
            </div>
            <div style="
                background: rgba(30, 30, 63, 0.8);
                border: 1px solid rgba(99, 102, 241, 0.2);
                border-radius: 4px 16px 16px 16px;
                padding: 1rem 1.5rem;
            ">
                <div style="display: flex; gap: 0.5rem; align-items: center;">
                    <div style="
                        width: 8px;
                        height: 8px;
                        border-radius: 50%;
                        background: #6366F1;
                        animation: bounce 1.4s infinite ease-in-out both;
                    "></div>
                    <div style="
                        width: 8px;
                        height: 8px;
                        border-radius: 50%;
                        background: #6366F1;
                        animation: bounce 1.4s infinite ease-in-out both;
                        animation-delay: 0.16s;
                    "></div>
                    <div style="
                        width: 8px;
                        height: 8px;
                        border-radius: 50%;
                        background: #6366F1;
                        animation: bounce 1.4s infinite ease-in-out both;
                        animation-delay: 0.32s;
                    "></div>
                </div>
            </div>
        </div>
        <style>
            @keyframes bounce {
                0%, 80%, 100% { transform: scale(0); }
                40% { transform: scale(1); }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# Prompt Editor
# ============================================================================

def prompt_editor() -> None:
    """Display prompt input editor."""
    st.markdown(
        """
        <div style="
            background: rgba(30, 30, 63, 0.9);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 16px;
            padding: 1rem;
            margin-top: 1rem;
        ">
            <div style="display: flex; gap: 0.5rem; margin-bottom: 0.75rem;">
                <span style="color: #64748B; font-size: 0.75rem;">💡 Tip: Use / for slash commands</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    col1, col2 = st.columns([6, 1])
    
    with col1:
        prompt = st.text_area(
            "Ask AI about your automation mission...",
            height=100,
            placeholder="Ask AI about your automation mission...\n\nExamples:\n- /new - Start new chat\n- /help - Get help\n- /tests - View test cases",
            label_visibility="collapsed",
            key="prompt_input",
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀", use_container_width=True, help="Send message"):
            if prompt:
                st.info("Sending message to AI...")
                st.rerun()
    
    # Prompt Suggestions
    st.markdown("<h4 style='color: #F1F5F9; margin: 1rem 0 0.75rem;'>💡 Suggested Prompts</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    suggestions = [
        "Generate a login test case",
        "Explain the sidebar failure",
        "Optimize test performance",
    ]
    
    for col, suggestion in zip([col1, col2, col3], suggestions):
        with col:
            if st.button(f"💬 {suggestion}", use_container_width=True):
                st.info(f"Selected: {suggestion}")


# ============================================================================
# Context Panel
# ============================================================================

def context_panel() -> None:
    """Display mission context panel."""
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(30, 30, 63, 0.95) 0%, rgba(99, 102, 241, 0.1) 100%);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 16px;
            padding: 1.25rem;
            margin-bottom: 1rem;
        ">
            <h4 style="color: #F1F5F9; margin: 0 0 1rem; font-size: 1rem;">🎯 Mission Context</h4>
        """,
        unsafe_allow_html=True,
    )
    
    context_items = [
        ("Mission", MOCK_MISSION_CONTEXT["mission_name"], "#6366F1"),
        ("Application", MOCK_MISSION_CONTEXT["application"], "#10B981"),
        ("Environment", MOCK_MISSION_CONTEXT["environment"], "#F59E0B"),
        ("Current Test", MOCK_MISSION_CONTEXT["current_test"], "#22D3EE"),
        ("Current Step", MOCK_MISSION_CONTEXT["current_step"], "#8B5CF6"),
        ("Agent", MOCK_MISSION_CONTEXT["current_agent"], "#6366F1"),
        ("Browser", MOCK_MISSION_CONTEXT["current_browser"], "#10B981"),
        ("Status", MOCK_MISSION_CONTEXT["execution_status"], "#F59E0B"),
        ("Coverage", MOCK_MISSION_CONTEXT["coverage"], "#10B981"),
        ("Pass Rate", MOCK_MISSION_CONTEXT["pass_rate"], "#22D3EE"),
        ("URL", MOCK_MISSION_CONTEXT["current_url"], "#94A3B8"),
    ]
    
    for label, value, color in context_items:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(51, 65, 85, 0.5);">
                <span style="color: #64748B; font-size: 0.8rem;">{label}</span>
                <span style="color: {color}; font-size: 0.8rem; font-weight: 500;">{value}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown("</div>", unsafe_allow_html=True)


def ai_knowledge_panel() -> None:
    """Display AI knowledge panel."""
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(30, 30, 63, 0.95) 0%, rgba(99, 102, 241, 0.1) 100%);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 16px;
            padding: 1.25rem;
            margin-bottom: 1rem;
        ">
            <h4 style="color: #F1F5F9; margin: 0 0 1rem; font-size: 1rem;">🧠 AI Knowledge</h4>
        """,
        unsafe_allow_html=True,
    )
    
    knowledge_items = [
        ("📄", "Detected Pages", "8 pages"),
        ("🔗", "Detected APIs", "83 endpoints"),
        ("🎯", "Current Locator", "#sidebar-menu"),
        ("📐", "DOM Element", "nav#sidebar"),
        ("📷", "Latest Screenshot", "Dashboard"),
        ("🐛", "Latest Bug", "Sidebar Hidden"),
        ("📊", "Latest Report", "v2.1.45"),
    ]
    
    for icon, label, value in knowledge_items:
        st.markdown(
            f"""
            <div style="
                display: flex;
                align-items: center;
                gap: 0.75rem;
                padding: 0.75rem;
                background: rgba(51, 65, 85, 0.5);
                border-radius: 8px;
                margin-bottom: 0.5rem;
                cursor: pointer;
            ">
                <span style="font-size: 1.25rem;">{icon}</span>
                <div style="flex: 1;">
                    <p style="color: #64748B; margin: 0; font-size: 0.7rem;">{label}</p>
                    <p style="color: #F1F5F9; margin: 0.25rem 0 0; font-size: 0.85rem;">{value}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# Quick Actions
# ============================================================================

def quick_actions_grid() -> None:
    """Display quick actions grid."""
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(30, 30, 63, 0.95) 0%, rgba(99, 102, 241, 0.1) 100%);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 16px;
            padding: 1.25rem;
        ">
            <h4 style="color: #F1F5F9; margin: 0 0 1rem; font-size: 1rem;">⚡ Quick Actions</h4>
        """,
        unsafe_allow_html=True,
    )
    
    col1, col2, col3, col4 = st.columns(4)
    
    for i, action in enumerate(MOCK_QUICK_ACTIONS):
        col = [col1, col2, col3, col4][i % 4]
        with col:
            st.markdown(
                f"""
                <div style="
                    text-align: center;
                    padding: 1rem 0.5rem;
                    background: rgba(51, 65, 85, 0.5);
                    border-radius: 8px;
                    margin-bottom: 0.5rem;
                    cursor: pointer;
                    transition: all 0.2s;
                ">
                    <span style="font-size: 1.5rem;">{action['icon']}</span>
                    <p style="color: #F1F5F9; margin: 0.5rem 0 0.25rem; font-size: 0.75rem;">{action['name']}</p>
                    <p style="color: #64748B; margin: 0; font-size: 0.65rem;">{action['description']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# Prompt Library
# ============================================================================

def prompt_library() -> None:
    """Display prompt template library."""
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(30, 30, 63, 0.95) 0%, rgba(99, 102, 241, 0.1) 100%);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 16px;
            padding: 1.25rem;
        ">
            <h4 style="color: #F1F5F9; margin: 0 0 1rem; font-size: 1rem;">📚 Prompt Library</h4>
        """,
        unsafe_allow_html=True,
    )
    
    for template in MOCK_PROMPT_TEMPLATES:
        st.markdown(
            f"""
            <div style="
                display: flex;
                align-items: center;
                gap: 1rem;
                padding: 0.75rem;
                background: rgba(51, 65, 85, 0.5);
                border-radius: 8px;
                margin-bottom: 0.5rem;
                cursor: pointer;
            ">
                <span style="font-size: 1.5rem;">{template['icon']}</span>
                <div style="flex: 1;">
                    <p style="color: #F1F5F9; margin: 0; font-size: 0.85rem;">{template['name']}</p>
                    <p style="color: #64748B; margin: 0.25rem 0 0; font-size: 0.75rem;">{template['prompt'][:50]}...</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# AI Thinking Panel
# ============================================================================

def ai_thinking_panel() -> None:
    """Display AI thinking panel."""
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(30, 30, 63, 0.95) 100%);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 16px;
            padding: 1.25rem;
        ">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                <div style="
                    width: 32px;
                    height: 32px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #6366F1, #8B5CF6);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    animation: glow 2s infinite;
                ">🧠</div>
                <h4 style="color: #F1F5F9; margin: 0;">AI Thinking</h4>
            </div>
        """,
        unsafe_allow_html=True,
    )
    
    thinking_items = [
        ("Current Thought", "Analyzing sidebar visibility issue...", "#6366F1"),
        ("Confidence", "94%", "#10B981"),
        ("Reasoning", "Element has dynamic class toggle", "#22D3EE"),
        ("Evidence", "3 DOM observations matched", "#F59E0B"),
        ("Recommendation", "Add wait for class removal", "#8B5CF6"),
        ("Next Step", "Generate updated test case", "#6366F1"),
    ]
    
    for label, value, color in thinking_items:
        st.markdown(
            f"""
            <div style="padding: 0.75rem; background: rgba(51, 65, 85, 0.5); border-radius: 8px; margin-bottom: 0.5rem;">
                <p style="color: {color}; margin: 0 0 0.25rem; font-size: 0.7rem; font-weight: 500;">{label}</p>
                <p style="color: #F1F5F9; margin: 0; font-size: 0.8rem;">{value}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown("</div><style>@keyframes glow { 0%, 100% { box-shadow: 0 0 10px rgba(99, 102, 241, 0.5); } 50% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.8); } }</style>", unsafe_allow_html=True)


# ============================================================================
# Notifications
# ============================================================================

def notification_toast(message: str, type: str = "info") -> None:
    """Display notification toast."""
    icons = {"success": "✅", "info": "ℹ️", "warning": "⚠️", "error": "❌"}
    colors = {"success": "#10B981", "info": "#6366F1", "warning": "#F59E0B", "error": "#EF4444"}
    
    st.markdown(
        f"""
        <div style="
            background: {colors.get(type, '#6366F1')}20;
            border: 1px solid {colors.get(type, '#6366F1')};
            border-radius: 8px;
            padding: 0.75rem 1rem;
            margin-bottom: 0.5rem;
            animation: slideIn 0.3s ease;
        ">
            <span>{icons.get(type, 'ℹ️')}</span>
            <span style="color: #F1F5F9; margin-left: 0.5rem;">{message}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
