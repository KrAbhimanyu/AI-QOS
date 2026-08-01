"""Live Execution Center - AI-QOS."""
import streamlit as st
import time
from datetime import datetime, timedelta
from components.execution_components import (
    init_execution_state,
    get_exec_data,
    set_exec_data,
    MOCK_AGENTS,
    MOCK_LOGS,
    MOCK_NETWORK,
    MOCK_EXECUTION_STEPS,
    execution_header,
    browser_viewer,
    ai_thinking_panel,
    agent_status_card,
    execution_timeline,
    console_viewer,
    network_viewer,
    execution_stats,
    mission_info_panel,
    execution_details_card,
    top_metrics_bar,
    notification_toast,
)


def render_execution_center() -> None:
    """Render the Live Execution Center page."""
    init_execution_state()
    
    # Auto-update execution for demo
    if not get_exec_data("exec_paused") and get_exec_data("exec_is_running"):
        auto_update_execution()
    
    # Top Metrics Bar
    top_metrics_bar()
    
    st.markdown("<hr style='margin: 1rem 0; border-color: #334155;'>", unsafe_allow_html=True)
    
    # Page Header
    execution_header(
        mission_name="E2E Regression Suite v2.1",
        status="Running" if not get_exec_data("exec_paused") else "Paused",
        browser="Chrome",
        environment="Staging",
        elapsed=format_elapsed(get_exec_data("exec_elapsed", 125)),
        progress=get_exec_data("exec_progress", 67),
    )
    
    # Action buttons
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
    
    with col1:
        if st.button("⏸️ Pause", use_container_width=True):
            set_exec_data("exec_paused", True)
            st.rerun()
    
    with col2:
        if st.button("▶️ Resume", use_container_width=True):
            set_exec_data("exec_paused", False)
            st.rerun()
    
    with col3:
        if st.button("⏹️ Stop", use_container_width=True):
            set_exec_data("exec_is_running", False)
            st.rerun()
    
    with col4:
        if st.button("🔄 Restart", use_container_width=True):
            reset_execution()
            st.rerun()
    
    with col5:
        if st.button("📊 Generate Report", use_container_width=True):
            st.success("📊 Report generated successfully!")
    
    with col6:
        if st.button("💬 AI Chat", use_container_width=True):
            st.info("💬 AI Chat panel coming soon!")
    
    st.markdown("<hr style='margin: 1rem 0; border-color: #334155;'>", unsafe_allow_html=True)
    
    # Main Content - Three Column Layout
    left_col, center_col, right_col = st.columns([1, 2.5, 1])
    
    # LEFT PANEL
    with left_col:
        render_left_panel()
    
    # CENTER PANEL
    with center_col:
        render_center_panel()
    
    # RIGHT PANEL
    with right_col:
        render_right_panel()
    
    # Bottom Timeline
    st.markdown("<hr style='margin: 1.5rem 0; border-color: #334155;'>", unsafe_allow_html=True)
    render_bottom_section()


def render_left_panel() -> None:
    """Render left panel with mission info and stats."""
    mission_info_panel(
        mission_name="E2E Regression",
        application="AIQOS Demo",
        environment="Staging",
        mode="Autonomous",
        started="10:00:00",
        elapsed=format_elapsed(get_exec_data("exec_elapsed", 125)),
        remaining="1m 15s",
        progress=get_exec_data("exec_progress", 67),
        coverage=94,
        phase="Running Assertions",
        health=98,
    )
    
    st.markdown("<h4 style='color: #F1F5F9; margin: 1.5rem 0 1rem;'>📊 Statistics</h4>", unsafe_allow_html=True)
    
    execution_stats(
        passed=get_exec_data("exec_passed", 24),
        failed=get_exec_data("exec_failed", 2),
        skipped=get_exec_data("exec_skipped", 3),
        running=4,
        coverage=94,
        success_rate=92.3,
    )
    
    # Test Details Drawer
    st.markdown("<h4 style='color: #F1F5F9; margin: 1.5rem 0 1rem;'>📝 Test Details</h4>", unsafe_allow_html=True)
    
    execution_details_card(
        test_name="Login Flow - Dashboard Access",
        expected="User logged in successfully",
        actual="Authentication successful",
        status="running",
        exec_time="12.5s",
        retries=0,
        step="3/5",
        confidence=get_exec_data("exec_confidence", 92),
    )


def render_center_panel() -> None:
    """Render center panel with browser viewer and live execution."""
    # Browser Viewer
    st.markdown("<h3 style='color: #F1F5F9; margin: 0 0 1rem;'>🌐 Live Browser View</h3>", unsafe_allow_html=True)
    
    browser_viewer(
        current_url=get_exec_data("exec_current_url", "https://demo.app/dashboard"),
        highlighted_element="Sign In Button",
        element_locator="#login-btn",
        element_role="button",
        element_text="Sign In",
        element_confidence=get_exec_data("exec_confidence", 92),
        action="clicking",
        animation="pulse",
    )
    
    st.markdown("<h4 style='color: #F1F5F9; margin: 1.5rem 0 1rem;'>🔄 Execution Steps</h4>", unsafe_allow_html=True)
    
    # Execution Steps
    steps = [
        {"name": "Browser Opened", "status": "completed", "icon": "✅"},
        {"name": "Navigating", "status": "completed", "icon": "✅"},
        {"name": "Finding Elements", "status": "completed", "icon": "✅"},
        {"name": "Executing Action", "status": "active", "icon": "🔄"},
        {"name": "Verifying Result", "status": "pending", "icon": "⏳"},
    ]
    
    for i, step in enumerate(steps):
        is_last = i == len(steps) - 1
        status_colors = {"completed": "#10B981", "active": "#6366F1", "pending": "#64748B"}
        color = status_colors.get(step["status"], "#64748B")
        
        st.markdown(
            f"""
            <div style="display: flex; gap: 1rem; margin-bottom: {0 if is_last else 0.75}rem;">
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <div style="
                        width: 28px;
                        height: 28px;
                        border-radius: 50%;
                        background: {color};
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 0.8rem;
                    ">{step['icon']}</div>
                    {'' if is_last else f'<div style="width: 2px; flex: 1; min-height: 20px; background: {color};"></div>'}
                </div>
                <div style="flex: 1;">
                    <p style="color: {'#F1F5F9' if step['status'] != 'pending' else '#64748B'}; margin: 0; font-size: 0.85rem;">{step['name']}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_right_panel() -> None:
    """Render right panel with AI thinking and agents."""
    # AI Thinking Panel
    ai_thinking_panel(
        current_thought="Login button located at position (450, 320)",
        reasoning="Scanned DOM for button elements with text 'Sign In'. Found 3 candidates with confidence scores.",
        decision="Using primary button with highest confidence score",
        confidence=get_exec_data("exec_confidence", 92),
        next_action="Click the button and verify authentication",
        potential_risk="Button may be covered by overlay",
        recommendation="Added fallback locator for reliability",
    )
    
    # Active Agents
    st.markdown("<h4 style='color: #F1F5F9; margin: 1.5rem 0 1rem;'>🤖 Active Agents</h4>", unsafe_allow_html=True)
    
    for agent in MOCK_AGENTS:
        agent_status_card(
            name=agent["name"],
            icon=agent["icon"],
            status=agent["status"],
            health=agent["health"],
            cpu=agent["cpu"],
            memory=agent["memory"],
            task=agent["task"],
            progress=agent["progress"],
        )
    
    # Notifications
    st.markdown("<h4 style='color: #F1F5F9; margin: 1.5rem 0 1rem;'>🔔 Recent</h4>", unsafe_allow_html=True)
    
    notifications = [
        {"type": "success", "message": "Test passed: Login successful", "icon": "✅"},
        {"type": "info", "message": "Screenshot captured", "icon": "📷"},
        {"type": "warning", "message": "Slow API response detected", "icon": "⚠️"},
        {"type": "success", "message": "Assertion passed", "icon": "✅"},
    ]
    
    for notif in notifications:
        notification_toast(notif["message"], notif["type"], notif["icon"])


def render_bottom_section() -> None:
    """Render bottom section with timeline and logs."""
    left_col, right_col = st.columns(2)
    
    with left_col:
        # Execution Timeline
        execution_timeline(MOCK_EXECUTION_STEPS)
    
    with right_col:
        # Console Viewer
        st.markdown(
            """
            <div style="
                background: rgba(30, 30, 63, 0.8);
                border: 1px solid rgba(99, 102, 241, 0.2);
                border-radius: 12px;
                padding: 1rem;
                margin-bottom: 1rem;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h4 style="color: #F1F5F9; margin: 0; font-size: 0.95rem;">💻 Log Console</h4>
                    <div style="display: flex; gap: 0.5rem;">
                        <span style="color: #64748B; font-size: 0.75rem; cursor: pointer;">Clear</span>
                        <span style="color: #64748B; font-size: 0.75rem; cursor: pointer;">Download</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        console_viewer(MOCK_LOGS)
    
    # Network Panel
    st.markdown("<h4 style='color: #F1F5F9; margin: 1.5rem 0 1rem;'>🌐 Network Activity</h4>", unsafe_allow_html=True)
    network_viewer(MOCK_NETWORK)
    
    # Screenshot Panel
    st.markdown("<h4 style='color: #F1F5F9; margin: 1.5rem 0 1rem;'>📷 Latest Screenshots</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    screenshots = [
        {"name": "Login Page", "time": "10:00:15"},
        {"name": "Dashboard", "time": "10:00:35"},
        {"name": "Profile Page", "time": "10:00:52"},
    ]
    
    for i, (col, screenshot) in enumerate(zip([col1, col2, col3], screenshots)):
        with col:
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, rgba(30, 30, 63, 0.9) 0%, rgba(99, 102, 241, 0.1) 100%);
                    border: 1px solid rgba(99, 102, 241, 0.2);
                    border-radius: 12px;
                    padding: 1rem;
                    text-align: center;
                    cursor: pointer;
                    transition: all 0.3s;
                ">
                    <div style="
                        height: 100px;
                        background: linear-gradient(135deg, #1E1E3F, #2A2A4A);
                        border-radius: 8px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin-bottom: 0.75rem;
                    ">
                        <span style="font-size: 2rem;">📷</span>
                    </div>
                    <p style="color: #F1F5F9; margin: 0; font-size: 0.85rem;">{screenshot['name']}</p>
                    <p style="color: #64748B; margin: 0.25rem 0 0; font-size: 0.7rem;">{screenshot['time']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def auto_update_execution() -> None:
    """Auto-update execution for demo purposes."""
    elapsed = get_exec_data("exec_elapsed", 0)
    set_exec_data("exec_elapsed", elapsed + 1)
    
    # Update progress periodically
    if elapsed % 5 == 0:
        progress = get_exec_data("exec_progress", 0)
        set_exec_data("exec_progress", min(100, progress + 1))
        
        # Update passed tests
        passed = get_exec_data("exec_passed", 0)
        if elapsed % 10 == 0:
            set_exec_data("exec_passed", passed + 1)
    
    time.sleep(0.5)


def reset_execution() -> None:
    """Reset execution state."""
    set_exec_data("exec_is_running", True)
    set_exec_data("exec_paused", False)
    set_exec_data("exec_progress", 0)
    set_exec_data("exec_passed", 0)
    set_exec_data("exec_failed", 0)
    set_exec_data("exec_skipped", 0)
    set_exec_data("exec_elapsed", 0)
    set_exec_data("exec_start_time", datetime.now())
    set_exec_data("exec_confidence", 0)


def format_elapsed(seconds: int) -> str:
    """Format elapsed seconds to MM:SS."""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"
