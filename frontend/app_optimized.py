"""AI-QOS - AI Quality Operating System Main Application (Optimized).

This is the optimized version of the main application with:
- Lazy imports
- Session state optimization
- Theme CSS caching
- Performance utilities
"""
import streamlit as st
from pathlib import Path

# Lazy import for theme config (only loaded once)
_theme_config = None

def get_theme_config():
    """Lazy load theme configuration."""
    global _theme_config
    if _theme_config is None:
        from themes.theme_config import THEME_CONFIG
        _theme_config = THEME_CONFIG
    return _theme_config


def get_app_config():
    """Lazy load app configuration."""
    from config.app_config import APP_NAME, APP_VERSION, APP_DESCRIPTION
    return APP_NAME, APP_VERSION, APP_DESCRIPTION


# Page configuration
APP_NAME, APP_VERSION, _ = get_app_config()

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


def apply_theme_once() -> None:
    """Apply theme CSS only once per session."""
    theme_key = "theme_applied"
    
    if not st.session_state.get(theme_key, False):
        theme_config = get_theme_config()
        st.markdown(
            f"<style>{theme_config['custom_css']}</style>",
            unsafe_allow_html=True
        )
        st.session_state[theme_key] = True


def init_session_state() -> None:
    """Initialize session state variables efficiently."""
    defaults = {
        "user": "Demo User",
        "theme": "dark",
        "current_view": "dashboard",
        # Add other persistent state here
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_navigation_items() -> dict:
    """Get navigation items (cached in session state)."""
    cache_key = "navigation_items"
    
    if cache_key not in st.session_state:
        st.session_state[cache_key] = {
            "📊 Dashboard": "dashboard",
            "🔍 Application Explorer": "application_explorer",
            "🌐 DOM Explorer": "dom_explorer",
            "🕸️ Knowledge Graph": "knowledge_graph",
            "📊 Reports & Analytics": "reports_center",
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
    
    return st.session_state[cache_key]


def sidebar_navigation() -> str:
    """Render sidebar navigation and return selected page."""
    with st.sidebar:
        # Use cached navigation items
        menu_items = get_navigation_items()
        
        # Header with app name (optimized - single markdown call)
        st.markdown(f"""
        <div style="padding: 1rem 0; text-align: center;">
            <h2 style="color: #6366F1; margin: 0;">{APP_NAME}</h2>
            <p style="color: #64748B; font-size: 0.75rem; margin: 0.25rem 0 0;">v{APP_VERSION}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Navigation radio (optimized - no re-render on expand/collapse)
        selected = st.radio(
            "Navigation",
            list(menu_items.keys()),
            index=0,
            label_visibility="collapsed",
            key="nav_radio"
        )
        
        st.divider()
        
        # User info (optimized - single markdown)
        st.markdown(f"""
        <div style="
            background: rgba(99, 102, 241, 0.1);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
        ">
            <div style="font-size: 2rem;">👤</div>
            <p style="color: #F1F5F9; margin: 0.5rem 0 0; font-weight: 500;">
                {st.session_state.user}
            </p>
            <p style="color: #64748B; margin: 0; font-size: 0.75rem;">
                Administrator
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Settings (collapsed by default for performance)
        with st.expander("⚙️ Settings"):
            st.selectbox("Theme", ["Dark", "Light"], disabled=True)
            st.selectbox("Language", ["English"])
    
    return menu_items.get(selected, "dashboard")


# View registry for lazy loading
_VIEW_REGISTRY = {
    "dashboard": ("views.dashboard", "render_dashboard"),
    "application_explorer": ("views.application_explorer", "render_page"),
    "dom_explorer": ("views.dom_explorer", "render_page"),
    "knowledge_graph": ("views.knowledge_graph", "render_page"),
    "reports_center": ("views.reports_center", "render_reports_center"),
    "mission_planner": ("views.mission_planner", "render_mission_planner"),
    "intelligence_center": ("views.intelligence_center", "render_intelligence_center"),
    "execution_center": ("views.execution_center", "render_execution_center"),
    "human_review_center": ("views.human_review_center", "render_human_review_center"),
    "ai_chat_workspace": ("views.ai_chat_workspace", "render_ai_chat_workspace"),
    "agent_control_tower": ("views.agent_control_tower", "render_agent_control_tower"),
    "missions": ("views.missions", "render_missions"),
    "agents": ("views.agents", "render_agents"),
    "executions": ("views.executions", "render_executions"),
    "monitoring": ("views.monitoring", "render_monitoring"),
    "quality": ("views.quality", "render_quality"),
    "reports": ("views.reports", "render_reports"),
}


def load_view(view_name: str) -> None:
    """Lazy load and render a view."""
    if view_name not in _VIEW_REGISTRY:
        st.error(f"Unknown view: {view_name}")
        return
    
    module_name, func_name = _VIEW_REGISTRY[view_name]
    
    # Import and call the render function
    import importlib
    module = importlib.import_module(module_name)
    render_func = getattr(module, func_name)
    render_func()


def main() -> None:
    """Main application entry point."""
    # Initialize session state once
    init_session_state()
    
    # Apply theme CSS once
    apply_theme_once()
    
    # Sidebar navigation
    current_page = sidebar_navigation()
    
    # Route to appropriate page (lazy loaded)
    load_view(current_page)


if __name__ == "__main__":
    main()
