"""AI-QOS - AI Quality Operating System Main Application."""
import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_ROOT = Path(__file__).resolve().parent
for path in (str(PROJECT_ROOT), str(FRONTEND_ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)

try:
    from .themes import THEME_CONFIG
    from .config.app_config import APP_NAME, APP_VERSION, APP_DESCRIPTION
except ImportError:
    from themes import THEME_CONFIG
    from config.app_config import APP_NAME, APP_VERSION, APP_DESCRIPTION

# Page configuration
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom theme CSS
st.markdown(f"<style>{THEME_CONFIG['custom_css']}</style>", unsafe_allow_html=True)


def local_css(file_name: str) -> None:
    """Load custom CSS from file."""
    css_path = Path(__file__).parent / "styles" / file_name
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def init_session_state() -> None:
    """Initialize session state variables."""
    if "user" not in st.session_state:
        st.session_state.user = "Demo User"
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"
    if "current_view" not in st.session_state:
        st.session_state.current_view = "dashboard"


def sidebar_navigation() -> str:
    """Render sidebar navigation and return selected page."""
    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding: 1rem 0; text-align: center;">
                <h2 style="color: #6366F1; margin: 0;">{APP_NAME}</h2>
                <p style="color: #64748B; font-size: 0.75rem; margin: 0.25rem 0 0;">v{APP_VERSION}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.divider()
        
        menu_items = {
            "📊 Dashboard": "dashboard",
            "🔍 Application Explorer": "application_explorer",
            "🌐 DOM Explorer": "dom_explorer",
            "🕸️ Knowledge Graph": "knowledge_graph",
            "📊 Reports & Analytics": "reports_center",
            "🚀 Release Advisor": "release_advisor",
            "🎯 Mission Planner": "mission_planner",
            "🔬 Intelligence Center": "intelligence_center",
            "🚀 Live Execution": "execution_center",
            "🔍 Human Review": "human_review_center",
            "💬 AI Chat": "ai_chat_workspace",
            "🤖 Agent Control": "agent_control_tower",
            "📋 Missions": "missions",
            "🤖 Agents": "agents",
            "⚡ Executions": "executions",
            "📡 Monitoring": "monitoring",
            "✅ Quality": "quality",
            "📈 Reports": "reports",
        }
        
        selected = st.radio(
            "Navigation",
            list(menu_items.keys()),
            index=0,
            label_visibility="collapsed",
        )
        
        st.divider()
        
        # User info
        st.markdown(
            f"""
            <div style="
                background: rgba(99, 102, 241, 0.1);
                border-radius: 12px;
                padding: 1rem;
                text-align: center;
            ">
                <div style="font-size: 2rem;">👤</div>
                <p style="color: #F1F5F9; margin: 0.5rem 0 0; font-weight: 500;">{st.session_state.user}</p>
                <p style="color: #64748B; margin: 0; font-size: 0.75rem;">Administrator</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Settings at bottom
        with st.expander("⚙️ Settings"):
            st.selectbox("Theme", ["Dark", "Light"], disabled=True)
            st.selectbox("Language", ["English"])
    
    return menu_items.get(selected, "dashboard")


def main() -> None:
    """Main application entry point."""
    init_session_state()
    
    # Sidebar navigation
    current_page = sidebar_navigation()
    
    # Route to appropriate page
    try:
        from .views.dashboard import render_dashboard
        from .views.application_explorer import render_page as render_application_explorer
        from .views.dom_explorer import render_page as render_dom_explorer
        from .views.knowledge_graph import render_page as render_knowledge_graph
        from .views.reports_center import render_reports_center
        from .views.release_advisor import render_page as render_release_advisor
        from .views.mission_planner import render_mission_planner
        from .views.intelligence_center import render_intelligence_center
        from .views.execution_center import render_execution_center
        from .views.human_review_center import render_human_review_center
        from .views.ai_chat_workspace import render_ai_chat_workspace
        from .views.agent_control_tower import render_agent_control_tower
        from .views.missions import render_missions
        from .views.agents import render_agents
        from .views.executions import render_executions
        from .views.monitoring import render_monitoring
        from .views.quality import render_quality
        from .views.reports import render_reports
    except ImportError:
        from views.dashboard import render_dashboard
        from views.application_explorer import render_page as render_application_explorer
        from views.dom_explorer import render_page as render_dom_explorer
        from views.knowledge_graph import render_page as render_knowledge_graph
        from views.reports_center import render_reports_center
        from views.release_advisor import render_page as render_release_advisor
        from views.mission_planner import render_mission_planner
        from views.intelligence_center import render_intelligence_center
        from views.execution_center import render_execution_center
        from views.human_review_center import render_human_review_center
        from views.ai_chat_workspace import render_ai_chat_workspace
        from views.agent_control_tower import render_agent_control_tower
        from views.missions import render_missions
        from views.agents import render_agents
        from views.executions import render_executions
        from views.monitoring import render_monitoring
        from views.quality import render_quality
        from views.reports import render_reports
    
    if current_page == "dashboard":
        render_dashboard()
    elif current_page == "application_explorer":
        render_application_explorer()
    elif current_page == "dom_explorer":
        render_dom_explorer()
    elif current_page == "knowledge_graph":
        render_knowledge_graph()
    elif current_page == "reports_center":
        render_reports_center()
    elif current_page == "release_advisor":
        render_release_advisor()
    elif current_page == "mission_planner":
        render_mission_planner()
    elif current_page == "intelligence_center":
        render_intelligence_center()
    elif current_page == "execution_center":
        render_execution_center()
    elif current_page == "human_review_center":
        render_human_review_center()
    elif current_page == "ai_chat_workspace":
        render_ai_chat_workspace()
    elif current_page == "agent_control_tower":
        render_agent_control_tower()
    elif current_page == "missions":
        render_missions()
    elif current_page == "agents":
        render_agents()
    elif current_page == "executions":
        render_executions()
    elif current_page == "monitoring":
        render_monitoring()
    elif current_page == "quality":
        render_quality()
    elif current_page == "reports":
        render_reports()


if __name__ == "__main__":
    main()
