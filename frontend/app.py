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
    initial_sidebar_state="collapsed",
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


def header_navigation() -> str:
    """Render a global header navigation and return the selected page."""
    menu_items = [
        ("Dashboard", "dashboard"),
        ("Application Explorer", "application_explorer"),
        ("DOM Explorer", "dom_explorer"),
        ("Knowledge Graph", "knowledge_graph"),
        ("Reports", "reports_center"),
        ("Release Advisor", "release_advisor"),
        ("Mission Planner", "mission_planner"),
        ("Intelligence", "intelligence_center"),
        ("Execution", "execution_center"),
        ("Review", "human_review_center"),
        ("AI Chat", "ai_chat_workspace"),
        ("Agents", "agent_control_tower"),
    ]

    primary_items = menu_items[:7]
    secondary_items = menu_items[7:]

    # Render full header inside one HTML container so Streamlit doesn't create
    # implicit extra rows. All navigation and utilities are rendered while the
    # header HTML is open to guarantee a single-line layout.
    st.markdown(
        f"""
        <div class="aiqos-top-header">
            <div class="aiqos-top-header__brand">
                <div style="font-weight: 700; color: #F8FAFC; font-size:1.05rem;">{APP_NAME}</div>
                <div style="font-size: 0.68rem; color: #94A3B8; margin-left:6px;">v{APP_VERSION}</div>
            </div>
            <div class="aiqos-top-header__nav">
        """,
        unsafe_allow_html=True,
    )

    # Primary navigation (text-first, non-wrapping). Render as inline buttons.
    try:
        from frontend.utils.responsive import metrics_row
        nav_cols = metrics_row(len(primary_items))
    except Exception:
        nav_cols = st.columns(len(primary_items))
    for col, (label, view_name) in zip(nav_cols, primary_items):
        with col:
            if st.button(
                label,
                key=f"nav_{view_name}",
                width='content',
                type=("primary" if st.session_state.current_view == view_name else "secondary"),
            ):
                st.session_state.current_view = view_name
                st.rerun()

    # Utility area: render inline within the same header container so nothing
    # drops to a second row. Utilities include Search, AI Chat, Agents, Deploy, More.
    util_cols = st.columns([0.02, 0.02, 0.02, 0.02, 0.01, 0.01])
    # Map utilities to actions (keep behavior unchanged)
    with util_cols[0]:
        if st.button("Search", key="util_search", width='content'):
            # existing search behavior (noop here — pages may implement search hooks)
            pass
    with util_cols[1]:
        if st.button("AI Chat", key="util_ai_chat", width='content'):
            st.session_state.current_view = "ai_chat_workspace"
            st.rerun()
    with util_cols[2]:
        if st.button("Agents", key="util_agents", width='content'):
            st.session_state.current_view = "agent_control_tower"
            st.rerun()
    with util_cols[3]:
        if st.button("Deploy", key="util_deploy", width='content'):
            # Deploy action retained as a header action — pages handle the event
            pass
    # More menu placeholder (will open an expander when clicked)
    with util_cols[4]:
        if "header_more_open" not in st.session_state:
            st.session_state.header_more_open = False
        if st.button("More ▾", key="util_more", width='content'):
            st.session_state.header_more_open = not st.session_state.header_more_open
            st.rerun()
    # Close the nav wrapper after utilities
    st.markdown("</div>", unsafe_allow_html=True)

    # If More expanded, render options inline but as a compact expander below header
    if st.session_state.get("header_more_open"):
        with st.expander("More navigation", expanded=True):
            for label, view_name in secondary_items:
                if st.button(label, key=f"more_{view_name}", width='stretch'):
                    st.session_state.current_view = view_name
                    st.session_state.header_more_open = False
                    st.rerun()
        # Icon map for secondary items (compact representation)
        ICON_MAP = {
            "Intelligence": "🧠",
            "Execution": "⚡",
            "Review": "🔎",
            "AI Chat": "💬",
            "Agents": "🤖",
        }

        # Render secondary items as compact icon-only buttons
        if secondary_items:
            try:
                from frontend.utils.responsive import metrics_row
                sec_cols = metrics_row(len(secondary_items) + 1)
            except Exception:
                sec_cols = st.columns(len(secondary_items) + 1)
            for col, (label, view_name) in zip(sec_cols, secondary_items):
                with col:
                    icon_label = ICON_MAP.get(label, "•")
                    if st.button(
                        icon_label,
                        key=f"nav_{view_name}",
                        width='content',
                        type=("primary" if st.session_state.current_view == view_name else "secondary"),
                        help=label,
                    ):
                        st.session_state.current_view = view_name
                        st.rerun()

            # Overflow control (three-dot) shown as the last small column
            with sec_cols[-1]:
                if "header_overflow_open" not in st.session_state:
                    st.session_state.header_overflow_open = False
                if st.button("⋯", key="nav_overflow_toggle", width='content', help="More navigation"):
                    st.session_state.header_overflow_open = not st.session_state.header_overflow_open
                    st.rerun()

        # If overflow toggled, render an accessible expander with full-label buttons
        if st.session_state.get("header_overflow_open"):
            with st.expander("More navigation", expanded=True):
                for label, view_name in secondary_items:
                    if st.button(label, key=f"overflow_{view_name}", width='stretch', help=f"Go to {label}"):
                        st.session_state.current_view = view_name
                        st.session_state.header_overflow_open = False
                        st.rerun()

    # Utility badges (user + environment) — remain inside header but visually
    # separated and non-wrapping.
    st.markdown(
        f"""
            <div style="display:inline-flex;gap:8px;align-items:center;margin-left:12px;">
                <span style="padding: 0.28rem 0.55rem; border-radius: 999px; background: rgba(99, 102, 241, 0.12); color: #C7D2FE; font-size: 0.78rem; white-space: nowrap;">{st.session_state.user}</span>
                <span style="padding: 0.28rem 0.55rem; border-radius: 999px; background: rgba(16, 185, 129, 0.12); color: #A7F3D0; font-size: 0.78rem; white-space: nowrap;">Environment: Staging</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return st.session_state.current_view


def main() -> None:
    """Main application entry point."""
    init_session_state()
    
    current_page = header_navigation()
    
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
