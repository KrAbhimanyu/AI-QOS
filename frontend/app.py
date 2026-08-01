"""AI-QOS - AI Quality Operating System Main Application."""
import streamlit as st
from pathlib import Path
from themes.theme_config import THEME_CONFIG
from config.app_config import APP_NAME, APP_VERSION, APP_DESCRIPTION

# Page configuration
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom theme
st.markdown(THEME_CONFIG["custom_css"], unsafe_allow_html=True)


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
            "🎯 Mission Planner": "mission_planner",
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
    if current_page == "dashboard":
        from pages.dashboard import render_dashboard
        render_dashboard()
    elif current_page == "mission_planner":
        from pages.mission_planner import render_mission_planner
        render_mission_planner()
    elif current_page == "missions":
        from pages.missions import render_missions
        render_missions()
    elif current_page == "agents":
        from pages.agents import render_agents
        render_agents()
    elif current_page == "executions":
        from pages.executions import render_executions
        render_executions()
    elif current_page == "monitoring":
        from pages.monitoring import render_monitoring
        render_monitoring()
    elif current_page == "quality":
        from pages.quality import render_quality
        render_quality()
    elif current_page == "reports":
        from pages.reports import render_reports
        render_reports()


if __name__ == "__main__":
    main()
