"""Application Intelligence Center - AI-QOS."""
import streamlit as st
import time
from datetime import datetime, timedelta
from components.intelligence_components import (
    init_intelligence_state,
    get_intel_data,
    set_intel_data,
    DISCOVERY_PHASES,
    MOCK_DISCOVERED_PAGES,
    MOCK_TECH_STACK,
    MOCK_AI_THOUGHTS,
    mission_info_card,
    tech_card,
    ai_thinking_panel,
    timeline_step,
    application_overview_card,
    dom_summary_card,
    discovery_progress_bar,
    phase_completed_badge,
    glass_loading_panel,
    skeleton_card,
    confidence_indicator,
    notification_toast,
)


def render_intelligence_center() -> None:
    """Render the Application Intelligence Center page."""
    init_intelligence_state()
    
    # Auto-advance phases for demo
    if not get_intel_data("intel_discovery_complete") and not get_intel_data("intel_paused"):
        auto_advance_phases()
    
    # Page header
    render_page_header()
    
    st.markdown("<hr style='margin: 1rem 0; border-color: #334155;'>", unsafe_allow_html=True)
    
    # Main content area
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
    
    # Bottom timeline
    st.markdown("<hr style='margin: 1.5rem 0; border-color: #334155;'>", unsafe_allow_html=True)
    render_bottom_timeline()
    
    # Discovered pages table
    st.markdown("<hr style='margin: 1.5rem 0; border-color: #334155;'>", unsafe_allow_html=True)
    render_discovered_pages()
    
    # Side Drawer for Page Details
    render_page_drawer()


def render_page_header() -> None:
    """Render page header with mission info and actions."""
    mission_name = get_intel_data("wizard_data", {}).get("mission_name", "E2E Regression Suite v2.1")
    app_url = get_intel_data("wizard_data", {}).get("app_url", "https://demo-aiqos.app")
    environment = get_intel_data("wizard_data", {}).get("environment", "Staging")
    current_phase_idx = get_intel_data("intel_current_phase", 0)
    current_phase = DISCOVERY_PHASES[current_phase_idx]["name"] if current_phase_idx < len(DISCOVERY_PHASES) else "Completed"
    status = "Paused" if get_intel_data("intel_paused") else "Running"
    confidence = get_intel_data("intel_confidence", 0)
    
    # Notification button
    notification_count = len(get_intel_data("intel_notifications", []))
    
    st.markdown("""<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;"> <div> <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;"> <span style="color: #64748B; font-size: 0.8rem;">🏠 Dashboard</span> <span style="color: #64748B;">›</span> <span style="color: #64748B; font-size: 0.8rem;">Missions</span> <span style="color: #64748B;">›</span> <span style="color: #F1F5F9; font-size: 0.8rem;">""" + mission_name + """</span> </div> <div style="display: flex; align-items: center; gap: 1rem;"> <h1 style="margin: 0; font-size: 1.5rem; color: #F1F5F9;">🎯 Application Intelligence Center</h1> <span style=" display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; background: rgba(99, 102, 241, 0.2); color: #6366F1; "> <span style="width: 8px; height: 8px; border-radius: 50%; background: #6366F1;"></span> """ + status + """ </span> </div> </div> <div style="display: flex; align-items: center; gap: 0.75rem;"> <div style="text-align: center; padding: 0.5rem 1rem; background: rgba(30, 30, 63, 0.8); border-radius: 8px;"> <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Confidence</p> <p style="color: #10B981; margin: 0; font-size: 1.25rem; font-weight: 600;">""" + str(confidence) + """%</p> </div> </div> </div>""", unsafe_allow_html=True)
    
    # Action buttons row
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 1, 1, 1])
    
    with col1:
        if st.button("⏸️ Pause", width='stretch'):
            set_intel_data("intel_paused", True)
            st.rerun()
    
    with col2:
        if st.button("▶️ Resume", width='stretch'):
            set_intel_data("intel_paused", False)
            st.rerun()
    
    with col3:
        if st.button("🔄 Restart", width='stretch'):
            reset_intelligence()
            st.rerun()
    
    with col4:
        if st.button("📥 Export Blueprint", width='stretch'):
            st.success("📥 Blueprint exported successfully!")
    
    with col5:
        st.button("📊 Generate Report", width='stretch')
    
    with col6:
        if st.button("❓ Help", width='stretch'):
            set_intel_data("show_help", not get_intel_data("show_help", False))
    
    with col7:
        if st.button("🤖 Continue to Automation →", type="primary", width='stretch'):
            st.info("🚀 Moving to Automation Phase...")


def render_left_panel() -> None:
    """Render left panel with mission info."""
    # Mission Info Card
    mission_name = get_intel_data("wizard_data", {}).get("mission_name", "E2E Regression Suite v2.1")
    project = get_intel_data("wizard_data", {}).get("project", "AI-QOS Platform")
    environment = get_intel_data("wizard_data", {}).get("environment", "Staging")
    priority = get_intel_data("wizard_data", {}).get("priority", "High")
    mode = get_intel_data("wizard_data", {}).get("execution_mode", "Autonomous")
    current_phase_idx = get_intel_data("intel_current_phase", 0)
    current_phase = DISCOVERY_PHASES[current_phase_idx]["name"] if current_phase_idx < len(DISCOVERY_PHASES) else "Completed"
    start_time = get_intel_data("intel_start_time", datetime.now())
    elapsed = (datetime.now() - start_time).total_seconds()
    elapsed_str = f"{int(elapsed // 60)}m {int(elapsed % 60)}s"
    
    # Calculate remaining time
    total_duration = sum(p["duration"] for p in DISCOVERY_PHASES)
    remaining = max(0, total_duration - current_phase_idx - (elapsed / 10))
    remaining_str = f"{int(remaining // 60)}m {int(remaining % 60)}s"
    
    progress = int((current_phase_idx / len(DISCOVERY_PHASES)) * 100)
    status = "Paused" if get_intel_data("intel_paused") else "Running"
    
    mission_info_card(
        mission_name=mission_name,
        project=project,
        environment=environment,
        priority=priority,
        mode=mode,
        started_at=start_time,
        elapsed=elapsed_str,
        remaining=remaining_str,
        progress=progress,
        phase=current_phase,
        status=status,
    )
    
    # DOM Summary
    stats = get_intel_data("intel_stats", {
        "Total Elements": 2847,
        "Interactive": 423,
        "Forms": 27,
        "Inputs": 156,
        "Buttons": 89,
        "Tables": 12,
        "Dropdowns": 34,
        "Links": 567,
        "Images": 123,
        "Hidden": 45,
    })
    
    st.markdown("<h4 style='color: #F1F5F9; margin: 1rem 0 0.75rem;'>📐 DOM Summary</h4>", unsafe_allow_html=True)
    
    dom_summary_card(stats)


def render_center_panel() -> None:
    """Render center panel with discovery phases and overview."""
    current_phase_idx = get_intel_data("intel_current_phase", 0)
    phase_progress = get_intel_data("intel_phase_progress", {})
    is_complete = get_intel_data("intel_discovery_complete", False)
    
    # Discovery Progress Section
    st.markdown("""<div style=" background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(30, 30, 63, 0.95) 100%); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem; "> <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.25rem;"> <h2 style="color: #F1F5F9; margin: 0; font-size: 1.25rem;">🔬 Application Intelligence</h2> <span style=" display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.35rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; background: rgba(99, 102, 241, 0.2); color: #6366F1; "> <span style="width: 8px; height: 8px; border-radius: 50%; background: #6366F1; animation: pulse 2s infinite;"></span> AI Studying Application </span> </div> </div>""", unsafe_allow_html=True)
    
    # Phase list with progress
    for i, phase in enumerate(DISCOVERY_PHASES):
        phase_id = phase["id"]
        is_completed = i < current_phase_idx
        is_current = i == current_phase_idx and not is_complete
        prog = phase_progress.get(phase_id, 100 if is_completed else (50 if is_current else 0))
        
        if is_completed:
            phase_completed_badge(phase["name"], phase["icon"])
        elif is_current:
            discovery_progress_bar(
                phase_name=phase["name"],
                progress=prog,
                icon=phase["icon"],
                color="#6366F1",
            )
        else:
            st.markdown(f"""<div style=" display: flex; align-items: center; gap: 1rem; padding: 0.75rem; background: rgba(30, 30, 63, 0.5); border-radius: 8px; margin-bottom: 0.5rem; opacity: 0.5; "> <span style="font-size: 1.25rem;">{phase['icon']}</span> <span style="color: #64748B;">{phase['name']}</span> <span style="color: #64748B; margin-left: auto; font-size: 0.75rem;">Pending</span> </div>""", unsafe_allow_html=True)
    
    if is_complete:
        st.markdown("""<div style=" background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 1.5rem; text-align: center; margin-top: 1rem; "> <span style="font-size: 3rem;">🎉</span> <h3 style="color: #10B981; margin: 1rem 0 0.5rem;">Discovery Complete!</h3> <p style="color: #94A3B8; margin: 0;">Application blueprint generated successfully</p> </div>""", unsafe_allow_html=True)
    
    # Application Overview
    st.markdown("<h3 style='color: #F1F5F9; margin: 1.5rem 0 1rem;'>🌐 Application Overview</h3>", unsafe_allow_html=True)
    
    application_overview_card(
        website_name="AIQOS Demo",
        technology="React + Node.js",
        authentication="Yes",
        total_pages=get_intel_data("intel_stats", {}).get("total_pages", 8),
        forms=get_intel_data("intel_stats", {}).get("forms", 27),
        buttons=get_intel_data("intel_stats", {}).get("buttons", 89),
        tables=get_intel_data("intel_stats", {}).get("tables", 12),
        dropdowns=get_intel_data("intel_stats", {}).get("dropdowns", 34),
        dialogs=12,
        nav_menu=8,
        api_count=get_intel_data("intel_stats", {}).get("api_endpoints", 83),
    )
    
    # Tech Stack
    st.markdown("<h3 style='color: #F1F5F9; margin: 1.5rem 0 1rem;'>⚙️ Technology Stack</h3>", unsafe_allow_html=True)
    
    tech_cards = [
        ("Frontend", MOCK_TECH_STACK["frontend"]["name"], MOCK_TECH_STACK["frontend"]["version"], MOCK_TECH_STACK["frontend"]["confidence"], "🖥️"),
        ("Backend", MOCK_TECH_STACK["backend"]["name"], MOCK_TECH_STACK["backend"]["version"], MOCK_TECH_STACK["backend"]["confidence"], "⚙️"),
        ("Database", MOCK_TECH_STACK["database"]["name"], MOCK_TECH_STACK["database"]["version"], MOCK_TECH_STACK["database"]["confidence"], "🗄️"),
        ("Auth", MOCK_TECH_STACK["auth"]["name"], "", MOCK_TECH_STACK["auth"]["confidence"], "🔐"),
    ]
    
    for title, value, version, confidence, icon in tech_cards:
        tech_card(title, value, version, confidence, icon)


def render_right_panel() -> None:
    """Render right panel with AI assistant."""
    current_phase_idx = get_intel_data("intel_current_phase", 0)
    current_phase = DISCOVERY_PHASES[current_phase_idx] if current_phase_idx < len(DISCOVERY_PHASES) else DISCOVERY_PHASES[-1]
    
    # AI Thinking Panel
    ai_thinking_panel(
        current_thought=MOCK_AI_THOUGHTS[current_phase_idx % len(MOCK_AI_THOUGHTS)],
        current_activity=f"Analyzing: {current_phase['name']}",
        confidence=get_intel_data("intel_confidence", 75),
        findings=[
            "Detected React 18 framework",
            "Found 27 forms across pages",
            "Identified JWT authentication",
            "Discovered 83 API endpoints",
        ],
        warnings=[
            "Some pages use dynamic content loading",
            "API rate limiting detected",
        ],
    )
    
    # Progress Stats
    st.markdown("""<div style=" background: rgba(30, 30, 63, 0.8); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 12px; padding: 1.25rem; margin-top: 1rem; "> <h4 style="color: #F1F5F9; margin: 0 0 1rem; font-size: 0.95rem;">📊 Progress Stats</h4>""", unsafe_allow_html=True)
    
    progress_items = [
        ("Pages Scanned", "8/8", "#10B981"),
        ("APIs Found", "83", "#6366F1"),
        ("Forms Mapped", "27", "#22D3EE"),
        ("Coverage", "94%", "#10B981"),
    ]
    
    for label, value, color in progress_items:
        st.markdown(f"""<div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(51, 65, 85, 0.5);"> <span style="color: #94A3B8; font-size: 0.8rem;">{label}</span> <span style="color: {color}; font-weight: 600;">{value}</span> </div>""", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Recent Notifications
    notifications = get_intel_data("intel_notifications", [
        {"type": "success", "message": "Discovery completed for Dashboard page", "time": "Just now"},
        {"type": "info", "message": "Technology stack identified", "time": "2 min ago"},
        {"type": "success", "message": "Authentication flow detected", "time": "3 min ago"},
    ])
    
    st.markdown("""<div style=" background: rgba(30, 30, 63, 0.8); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 12px; padding: 1.25rem; margin-top: 1rem; "> <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;"> <h4 style="color: #F1F5F9; margin: 0; font-size: 0.95rem;">🔔 Notifications</h4> <span style="color: #64748B; font-size: 0.75rem;">3 new</span> </div>""", unsafe_allow_html=True)
    
    for notif in notifications:
        notification_toast(notif["message"], notif["type"], "✅" if notif["type"] == "success" else "ℹ️")
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_bottom_timeline() -> None:
    """Render bottom timeline."""
    current_phase_idx = get_intel_data("intel_current_phase", 0)
    start_time = get_intel_data("intel_start_time", datetime.now())
    
    st.markdown("""<div style=" background: rgba(30, 30, 63, 0.8); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 16px; padding: 1.5rem; "> <h3 style="color: #F1F5F9; margin: 0 0 1.5rem; font-size: 1.1rem;">📅 Mission Timeline</h3> </div>""", unsafe_allow_html=True)
    
    # Timeline steps
    timeline_items = [
        ("Mission Created", "completed", start_time.strftime("%H:%M:%S"), "0s"),
        ("Application Opened", "completed", (start_time + timedelta(seconds=5)).strftime("%H:%M:%S"), "5s"),
        ("Technology Identified", "completed", (start_time + timedelta(seconds=15)).strftime("%H:%M:%S"), "10s"),
        ("DOM Studied", "completed", (start_time + timedelta(seconds=25)).strftime("%H:%M:%S"), "10s"),
        ("Pages Mapped", "completed", (start_time + timedelta(seconds=35)).strftime("%H:%M:%S"), "10s"),
        ("Forms Mapped", "active", datetime.now().strftime("%H:%M:%S"), "In progress"),
        ("API Discovery", "pending", "-", "-"),
        ("Blueprint Generated", "pending", "-", "-"),
        ("Ready for Automation", "pending", "-", "-"),
    ]
    
    # Display in two columns
    col1, col2 = st.columns(2)
    
    for idx, (step, status, time_str, duration) in enumerate(timeline_items):
        is_last = idx == len(timeline_items) - 1
        with col1 if idx < 5 else col2:
            timeline_step(step, status, time_str, duration, is_last=(idx % 5) == 4)


def render_discovered_pages() -> None:
    """Render discovered pages table."""
    pages = MOCK_DISCOVERED_PAGES
    
    st.markdown("""<div style=" background: rgba(30, 30, 63, 0.8); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 16px; padding: 1.5rem; "> <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;"> <div> <h3 style="color: #F1F5F9; margin: 0; font-size: 1.1rem;">📄 Discovered Pages</h3> <p style="color: #64748B; margin: 0.25rem 0 0; font-size: 0.8rem;">8 pages analyzed</p> </div> <div style="display: flex; gap: 0.5rem;"> <input type="text" placeholder="Search pages..." style=" background: rgba(51, 65, 85, 0.5); border: 1px solid #334155; border-radius: 8px; padding: 0.5rem 1rem; color: #F1F5F9; font-size: 0.85rem; "> </div> </div> </div>""", unsafe_allow_html=True)
    
    # Display pages as cards
    for i, page in enumerate(pages):
        status_color = "#10B981" if page["status"] == "Analyzed" else "#64748B"
        
        st.markdown(f"""<div style=" background: rgba(30, 30, 63, 0.6); border: 1px solid rgba(51, 65, 85, 0.5); border-radius: 12px; padding: 1rem 1.5rem; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 1.5rem; "> <div style=" width: 40px; height: 40px; border-radius: 8px; background: linear-gradient(135deg, #6366F1, #8B5CF6); display: flex; align-items: center; justify-content: center; font-size: 1.25rem; ">📄</div> <div style="flex: 1;"> <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.25rem;"> <span style="color: #F1F5F9; font-weight: 500;">{page['name']}</span> <span style="color: #64748B; font-size: 0.8rem;">{page['url']}</span> </div> <div style="display: flex; gap: 1rem;"> <span style="color: #64748B; font-size: 0.75rem;">📝 {page['forms']} forms</span> <span style="color: #64748B; font-size: 0.75rem;">🔘 {page['buttons']} buttons</span> <span style="color: #64748B; font-size: 0.75rem;">📊 {page['tables']} tables</span> </div> </div> <div style="text-align: center; padding: 0.5rem 1rem; background: rgba(51, 65, 85, 0.5); border-radius: 8px;"> <p style="color: #64748B; margin: 0; font-size: 0.65rem;">Coverage</p> <p style="color: #10B981; margin: 0; font-size: 0.95rem; font-weight: 600;">{page['coverage']}</p> </div> <span style=" display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.35rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; background: {status_color}20; color: {status_color}; "> <span style="width: 6px; height: 6px; border-radius: 50%; background: {status_color};"></span> {page['status']} </span> </div>""", unsafe_allow_html=True)


def auto_advance_phases() -> None:
    """Auto-advance through phases for demo."""
    current = get_intel_data("intel_current_phase", 0)
    
    if current >= len(DISCOVERY_PHASES):
        set_intel_data("intel_discovery_complete", True)
        return
    
    # Simulate progress
    phase_data = get_intel_data("intel_phase_progress", {})
    phase_id = DISCOVERY_PHASES[current]["id"]
    current_progress = phase_data.get(phase_id, 0)
    
    if current_progress < 100:
        phase_data[phase_id] = min(100, current_progress + 15)
        set_intel_data("intel_phase_progress", phase_data)
    else:
        # Move to next phase
        set_intel_data("intel_current_phase", current + 1)
        set_intel_data("intel_confidence", min(98, 60 + current * 3))
        
        # Add notification
        notifications = get_intel_data("intel_notifications", [])
        notifications.insert(0, {
            "type": "success",
            "message": f"Completed: {DISCOVERY_PHASES[current]['name']}",
            "time": "Just now",
        })
        set_intel_data("intel_notifications", notifications[:5])
        
        # Update stats
        stats = get_intel_data("intel_stats", {})
        if current == 4:  # Forms phase
            stats["forms"] = 27
        elif current == 5:  # Buttons phase
            stats["buttons"] = 89
        elif current == 6:  # Tables phase
            stats["tables"] = 12
        elif current == 9:  # APIs phase
            stats["api_endpoints"] = 83
        set_intel_data("intel_stats", stats)
    
    time.sleep(0.5)


def reset_intelligence() -> None:
    """Reset intelligence state."""
    set_intel_data("intel_current_phase", 0)
    set_intel_data("intel_phase_progress", {})
    set_intel_data("intel_discovery_complete", False)
    set_intel_data("intel_paused", False)
    set_intel_data("intel_start_time", datetime.now())
    set_intel_data("intel_confidence", 0)
    set_intel_data("intel_notifications", [])
    set_intel_data("intel_stats", {
        "total_pages": 0,
        "forms": 0,
        "buttons": 0,
        "tables": 0,
        "dropdowns": 0,
        "api_endpoints": 0,
    })


def render_page_drawer() -> None:
    """Render side drawer for page details."""
    # Initialize selected page state
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = None
    
    # Page selector in sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown("""<div style=" background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(30, 30, 63, 0.9) 100%); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 12px; padding: 1rem; "> <h4 style="color: #F1F5F9; margin: 0 0 0.75rem; font-size: 0.95rem;">📄 Page Explorer</h4> <p style="color: #94A3B8; margin: 0 0 1rem; font-size: 0.75rem;">Click a page to view details</p> </div>""", unsafe_allow_html=True)
        
        # Page selection
        page_names = [p["name"] for p in MOCK_DISCOVERED_PAGES]
        selected = st.selectbox("Select Page", ["(Select a page)"] + page_names, key="page_selector")
        
        if selected != "(Select a page)":
            st.session_state.selected_page = selected
    
    # Show drawer if page selected
    if st.session_state.selected_page:
        selected_page_data = next((p for p in MOCK_DISCOVERED_PAGES if p["name"] == st.session_state.selected_page), None)
        
        if selected_page_data:
            with st.expander("📋 Page Details: " + st.session_state.selected_page, expanded=True):
                # Page Header
                st.markdown(f"""<div style=" background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(30, 30, 63, 0.95) 100%); border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; "> <div style="display: flex; align-items: center; gap: 1rem;"> <div style=" width: 48px; height: 48px; border-radius: 12px; background: linear-gradient(135deg, #6366F1, #8B5CF6); display: flex; align-items: center; justify-content: center; font-size: 1.5rem; ">📄</div> <div> <h3 style="color: #F1F5F9; margin: 0;">{selected_page_data['name']}</h3> <p style="color: #94A3B8; margin: 0.25rem 0 0; font-size: 0.85rem;">{selected_page_data['url']}</p> </div> </div> </div>""", unsafe_allow_html=True)
                
                # Detected Components
                st.markdown("### 🔍 Detected Components")
                components = {
                    "Forms": selected_page_data["forms"],
                    "Buttons": selected_page_data["buttons"],
                    "Tables": selected_page_data["tables"],
                    "Dropdowns": 3,
                    "Links": 24,
                    "Images": 8,
                }
                
                for comp, count in components.items():
                    st.markdown(f"""<div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #334155;"> <span style="color: #94A3B8;">{comp}</span> <span style="color: #F1F5F9; font-weight: 500;">{count}</span> </div>""", unsafe_allow_html=True)
                
                st.markdown("### 📐 DOM Summary")
                dom_elements = {
                    "Total Elements": 356,
                    "Interactive Elements": 42,
                    "Input Fields": selected_page_data["forms"] * 4,
                    "Hidden Elements": 12,
                }
                
                for elem, count in dom_elements.items():
                    st.markdown(f"""<div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #334155;"> <span style="color: #94A3B8;">{elem}</span> <span style="color: #F1F5F9; font-weight: 500;">{count}</span> </div>""", unsafe_allow_html=True)
                
                st.markdown("### ✅ Suggested Test Cases")
                test_cases = [
                    ("Verify page loads correctly", "High"),
                    ("Test all form validations", "High"),
                    ("Check button click handlers", "Medium"),
                    ("Validate table data rendering", "Medium"),
                    ("Test navigation links", "Low"),
                ]
                
                for case, priority in test_cases:
                    priority_color = {"High": "#EF4444", "Medium": "#F59E0B", "Low": "#10B981"}.get(priority, "#64748B")
                    st.markdown(f"""<div style=" display: flex; justify-content: space-between; align-items: center; padding: 0.5rem; background: rgba(51, 65, 85, 0.3); border-radius: 6px; margin-bottom: 0.5rem; "> <span style="color: #F1F5F9; font-size: 0.85rem;">{case}</span> <span style="color: {priority_color}; font-size: 0.75rem;">{priority}</span> </div>""", unsafe_allow_html=True)
                
                st.markdown("### ⚠️ Potential Risks")
                risks = [
                    "Dynamic content loading may affect test stability",
                    "Third-party scripts could cause flakiness",
                    "Complex nested modals detected",
                ]
                
                for risk in risks:
                    st.markdown(f"""<div style=" padding: 0.5rem 0.75rem; background: rgba(245, 158, 11, 0.1); border-left: 3px solid #F59E0B; margin-bottom: 0.5rem; "> <span style="color: #F59E0B; font-size: 0.8rem;">⚠️ {risk}</span> </div>""", unsafe_allow_html=True)
                
                st.markdown("### ♿ Accessibility Notes")
                a11y_notes = [
                    "Missing ARIA labels on 3 buttons",
                    "Color contrast ratio: 4.2:1 (Good)",
                    "Keyboard navigation: Fully supported",
                    "Screen reader: Partially supported",
                ]
                
                for note in a11y_notes:
                    status_color = "#10B981" if "Good" in note or "Fully" in note else "#F59E0B"
                    st.markdown(f"""<div style=" padding: 0.5rem 0; border-bottom: 1px solid #334155; display: flex; align-items: center; gap: 0.5rem; "> <span style="color: {status_color};">{'✅' if 'Good' in note or 'Fully' in note else '⚠️'}</span> <span style="color: #94A3B8; font-size: 0.8rem;">{note}</span> </div>""", unsafe_allow_html=True)
                
                # Coverage
                st.markdown("---")
                coverage = int(selected_page_data["coverage"].replace("%", ""))
                st.markdown(f"""<div style=" background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(30, 30, 63, 0.9) 100%); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 1rem; text-align: center; "> <p style="color: #94A3B8; margin: 0 0 0.5rem; font-size: 0.8rem;">Estimated Coverage</p> <p style="color: #10B981; margin: 0; font-size: 2rem; font-weight: 700;">{coverage}%</p> <div style="height: 6px; background: #334155; border-radius: 3px; margin-top: 0.5rem;"> <div style="width: {coverage}%; height: 100%; background: #10B981; border-radius: 3px;"></div> </div> </div>""", unsafe_allow_html=True)
    
    # Show help panel if requested
    if get_intel_data("show_help", False):
        with st.expander("❓ Help & Tips", expanded=True):
            st.markdown("""<div style=" background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(30, 30, 63, 0.9) 100%); border-radius: 12px; padding: 1.5rem; "> <h4 style="color: #F1F5F9; margin: 0 0 1rem;">🚀 Getting Started</h4> <ol style="color: #94A3B8; padding-left: 1.25rem; font-size: 0.85rem;"> <li style="margin-bottom: 0.5rem;">The AI is currently studying your application</li> <li style="margin-bottom: 0.5rem;">Each phase analyzes different aspects of your app</li> <li style="margin-bottom: 0.5rem;">Click on any page to see detailed analysis</li> <li style="margin-bottom: 0.5rem;">Review suggested test cases for each page</li> <li>Click "Continue to Automation" when ready</li> </ol> <h4 style="color: #F1F5F9; margin: 1.5rem 0 1rem;">💡 Tips</h4> <ul style="color: #94A3B8; padding-left: 1.25rem; font-size: 0.85rem;"> <li style="margin-bottom: 0.5rem;">Use "Pause" to stop analysis temporarily</li> <li style="margin-bottom: 0.5rem;">"Export Blueprint" saves the app map</li> <li>Higher confidence = better test generation</li> </ul> </div>""", unsafe_allow_html=True)
