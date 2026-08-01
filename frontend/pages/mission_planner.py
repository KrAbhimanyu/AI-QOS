"""Mission Planner Wizard - AI-QOS."""
import streamlit as st
from datetime import datetime
from components.wizard_components import (
    init_wizard_state,
    get_wizard_data,
    set_wizard_data,
    validate_step,
    wizard_stepper,
    step_section,
    ai_assistant_panel,
    progress_sidebar,
    wizard_actions,
    testing_type_card,
    summary_item,
)


def render_mission_planner() -> None:
    """Render the Mission Planner Wizard."""
    init_wizard_state()
    
    # Page configuration
    st.markdown(
        """
        <style>
        .mission-planner-header {
            padding: 1rem 0;
            border-bottom: 1px solid #334155;
            margin-bottom: 1.5rem;
        }
        .stColumn > div:first-child {
            padding-top: 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # Header
    st.markdown(
        """
        <div class="mission-planner-header">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="font-size: 2rem;">🎯</span>
                <div>
                    <h1 style="margin: 0; font-size: 1.75rem; color: #F1F5F9;">Mission Planner</h1>
                    <p style="margin: 0.25rem 0 0; color: #94A3B8; font-size: 0.875rem;">
                        Create and configure your AI-powered testing mission
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Progress stepper
    wizard_stepper(st.session_state.wizard_step)
    st.markdown("<hr style='margin: 1.5rem 0; border-color: #334155;'>", unsafe_allow_html=True)
    
    # Main content area with sidebars
    left_col, main_col, right_col = st.columns([1, 3, 1])
    
    # Left sidebar - Progress
    with left_col:
        progress_sidebar(st.session_state.wizard_step)
        
        # Quick stats
        st.markdown(
            """
            <div style="
                background: rgba(30, 30, 63, 0.5);
                border-radius: 12px;
                padding: 1rem;
            ">
                <h4 style="color: #F1F5F9; margin: 0 0 0.75rem; font-size: 0.9rem;">📊 Quick Stats</h4>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #334155;">
                    <span style="color: #94A3B8; font-size: 0.8rem;">Testing Types</span>
                    <span style="color: #6366F1; font-size: 0.8rem;">""" + str(len(get_wizard_data("testing_types", []))) + """</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #334155;">
                    <span style="color: #94A3B8; font-size: 0.8rem;">Files</span>
                    <span style="color: #22D3EE; font-size: 0.8rem;">""" + str(len(get_wizard_data("uploaded_files", []))) + """</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                    <span style="color: #94A3B8; font-size: 0.8rem;">Est. Coverage</span>
                    <span style="color: #10B981; font-size: 0.8rem;">""" + str(min(95, 30 + len(get_wizard_data("testing_types", [])) * 12)) + """%</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    # Main content area
    with main_col:
        # Route to current step
        if st.session_state.wizard_step == 1:
            render_step_1()
        elif st.session_state.wizard_step == 2:
            render_step_2()
        elif st.session_state.wizard_step == 3:
            render_step_3()
        elif st.session_state.wizard_step == 4:
            render_step_4()
        elif st.session_state.wizard_step == 5:
            render_step_5()
        
        st.markdown("<hr style='margin: 1.5rem 0; border-color: #334155;'>", unsafe_allow_html=True)
        
        # Action buttons
        action = wizard_actions(
            current_step=st.session_state.wizard_step,
            show_launch=(st.session_state.wizard_step == 5),
        )
        
        # Handle actions
        if action == "prev":
            st.session_state.wizard_step = max(1, st.session_state.wizard_step - 1)
            st.rerun()
        elif action == "next":
            validation = validate_step(st.session_state.wizard_step)
            if validation["valid"]:
                st.session_state.wizard_step = min(5, st.session_state.wizard_step + 1)
                st.rerun()
            else:
                for error in validation["errors"]:
                    st.error(f"⚠️ {error}")
        elif action == "save":
            st.success("💾 Draft saved successfully!")
        elif action == "cancel":
            st.session_state.wizard_step = 1
            st.session_state.wizard_data = {}
            st.success("Mission cancelled. Ready to start fresh!")
            st.rerun()
        elif action == "launch":
            # Initialize intelligence center state with mission data
            st.session_state.current_view = "intelligence_center"
            st.session_state.mission_launched = True
            st.success("🚀 Mission launched! Navigating to Intelligence Center...")
            st.info("🔬 AI is now studying your application...")
            time.sleep(2)
            st.rerun()
    
    # Right sidebar - AI Assistant
    with right_col:
        ai_assistant_panel(st.session_state.wizard_step)


# =============================================================================
# STEP 1: Mission Information
# =============================================================================

def render_step_1() -> None:
    """Render Step 1: Mission Information."""
    step_section("Mission Information", "📋")
    
    # Mission Name
    st.markdown(
        '<label style="color: #94A3B8; font-size: 0.875rem; margin-bottom: 0.25rem; display: block;">Mission Name *</label>',
        unsafe_allow_html=True,
    )
    mission_name = st.text_input(
        "Mission Name",
        value=get_wizard_data("mission_name", ""),
        placeholder="e.g., E2E Regression Suite v2.1",
        label_visibility="collapsed",
        key="mission_name_input",
        on_change=lambda: set_wizard_data("mission_name", st.session_state.get("mission_name_input", "")),
    )
    if mission_name:
        set_wizard_data("mission_name", mission_name)
    
    # Mission Description
    st.markdown(
        '<label style="color: #94A3B8; font-size: 0.875rem; margin-bottom: 0.25rem; display: block;">Mission Description</label>',
        unsafe_allow_html=True,
    )
    mission_desc = st.text_area(
        "Description",
        value=get_wizard_data("mission_description", ""),
        placeholder="Describe the purpose and scope of this mission...",
        label_visibility="collapsed",
        key="mission_desc_input",
        on_change=lambda: set_wizard_data("mission_description", st.session_state.get("mission_desc_input", "")),
        height=80,
    )
    if mission_desc:
        set_wizard_data("mission_description", mission_desc)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Two column layout for project and app info
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            '<label style="color: #94A3B8; font-size: 0.875rem; margin-bottom: 0.25rem; display: block;">Project</label>',
            unsafe_allow_html=True,
        )
        project = st.selectbox(
            "Project",
            ["", "AI-QOS Platform", "E-Commerce App", "Mobile Backend", "Data Pipeline", "Custom"],
            index=0,
            label_visibility="collapsed",
            key="project_select",
        )
        if project:
            set_wizard_data("project", project)
    
    with col2:
        st.markdown(
            '<label style="color: #94A3B8; font-size: 0.875rem; margin-bottom: 0.25rem; display: block;">Application Name</label>',
            unsafe_allow_html=True,
        )
        app_name = st.text_input(
            "App Name",
            value=get_wizard_data("app_name", ""),
            placeholder="My Application",
            label_visibility="collapsed",
            key="app_name_input",
        )
        if app_name:
            set_wizard_data("app_name", app_name)
    
    # Application URL
    st.markdown(
        '<label style="color: #94A3B8; font-size: 0.875rem; margin-bottom: 0.25rem; display: block;">Application URL *</label>',
        unsafe_allow_html=True,
    )
    app_url = st.text_input(
        "Application URL",
        value=get_wizard_data("app_url", ""),
        placeholder="https://app.example.com",
        label_visibility="collapsed",
        key="app_url_input",
    )
    if app_url:
        set_wizard_data("app_url", app_url)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Environment and Priority
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown(
            '<label style="color: #94A3B8; font-size: 0.875rem; margin-bottom: 0.25rem; display: block;">Environment *</label>',
            unsafe_allow_html=True,
        )
        env_options = ["Development", "QA", "UAT", "Staging", "Production"]
        env = st.selectbox(
            "Environment",
            env_options,
            index=env_options.index(get_wizard_data("environment")) if get_wizard_data("environment") in env_options else 0,
            label_visibility="collapsed",
            key="env_select",
        )
        if env:
            set_wizard_data("environment", env)
    
    with col2:
        st.markdown(
            '<label style="color: #94A3B8; font-size: 0.875rem; margin-bottom: 0.25rem; display: block;">Priority *</label>',
            unsafe_allow_html=True,
        )
        priority_options = ["High", "Medium", "Low"]
        priority = st.selectbox(
            "Priority",
            priority_options,
            index=priority_options.index(get_wizard_data("priority")) if get_wizard_data("priority") in priority_options else 0,
            label_visibility="collapsed",
            key="priority_select",
        )
        if priority:
            set_wizard_data("priority", priority)
    
    with col3:
        st.markdown(
            '<label style="color: #94A3B8; font-size: 0.875rem; margin-bottom: 0.25rem; display: block;">Estimated Time</label>',
            unsafe_allow_html=True,
        )
        time_options = ["5 min", "15 min", "30 min", "1 hour", "2 hours", "4+ hours"]
        est_time = st.selectbox(
            "Est. Time",
            time_options,
            index=time_options.index(get_wizard_data("estimated_time")) if get_wizard_data("estimated_time") in time_options else 0,
            label_visibility="collapsed",
            key="time_select",
        )
        if est_time:
            set_wizard_data("estimated_time", est_time)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Authentication section
    st.markdown(
        """
        <div style="
            background: rgba(30, 30, 63, 0.8);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 12px;
            padding: 1.25rem;
            margin-top: 1rem;
        ">
            <h4 style="color: #F1F5F9; margin: 0 0 1rem; font-size: 0.95rem;">🔐 Authentication (Optional)</h4>
        """,
        unsafe_allow_html=True,
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        auth_options = ["No", "Yes"]
        auth_required = st.radio(
            "Authentication Required",
            auth_options,
            index=auth_options.index(get_wizard_data("auth_required")) if get_wizard_data("auth_required") in auth_options else 0,
            horizontal=True,
        )
        set_wizard_data("auth_required", auth_required)
    
    with col2:
        if auth_required == "Yes":
            st.info("💡 Username and password will be securely stored")
    
    if auth_required == "Yes":
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input(
                "Username",
                value=get_wizard_data("credentials", {}).get("username", ""),
                placeholder="Enter username",
            )
            creds = get_wizard_data("credentials", {})
            creds["username"] = username
            set_wizard_data("credentials", creds)
        
        with col2:
            password = st.text_input(
                "Password",
                value=get_wizard_data("credentials", {}).get("password", ""),
                placeholder="Enter password",
                type="password",
            )
            creds = get_wizard_data("credentials", {})
            creds["password"] = password
            set_wizard_data("credentials", creds)
    
    st.markdown("</div>", unsafe_allow_html=True)


# =============================================================================
# STEP 2: Upload Documents
# =============================================================================

def render_step_2() -> None:
    """Render Step 2: Upload Documents."""
    step_section("Upload Documents", "📄")
    
    st.markdown(
        '<p style="color: #94A3B8; font-size: 0.875rem; margin-bottom: 1.5rem;">Upload supporting documents to help AI understand your testing requirements</p>',
        unsafe_allow_html=True,
    )
    
    # File type configurations
    file_types = [
        {
            "name": "Excel Test Cases",
            "icon": "📊",
            "description": "Test case specifications",
            "extensions": ["xlsx", "xls"],
        },
        {
            "name": "BRD Document",
            "icon": "📝",
            "description": "Business Requirements Document",
            "extensions": ["pdf", "docx", "doc"],
        },
        {
            "name": "PRD Document",
            "icon": "📋",
            "description": "Product Requirements Document",
            "extensions": ["pdf", "docx", "doc"],
        },
        {
            "name": "Swagger/OpenAPI",
            "icon": "🔄",
            "description": "API specifications",
            "extensions": ["json", "yaml", "yml"],
        },
        {
            "name": "Postman Collection",
            "icon": "🚀",
            "description": "API requests collection",
            "extensions": ["json"],
        },
        {
            "name": "Feature Files",
            "icon": "🥒",
            "description": "BDD/Gherkin specifications",
            "extensions": ["feature"],
        },
    ]
    
    # Create 3x2 grid
    for i in range(0, len(file_types), 3):
        cols = st.columns(3)
        for j, file_type in enumerate(file_types[i:i+3]):
            with cols[j]:
                # Card header
                st.markdown(
                    f"""
                    <div style="
                        background: linear-gradient(135deg, rgba(30, 30, 63, 0.9) 0%, rgba(99, 102, 241, 0.1) 100%);
                        border: 1px solid rgba(99, 102, 241, 0.2);
                        border-radius: 12px;
                        padding: 1rem;
                        text-align: center;
                        margin-bottom: 0.5rem;
                    ">
                        <div style="font-size: 1.75rem; margin-bottom: 0.25rem;">{file_type['icon']}</div>
                        <h4 style="color: #F1F5F9; margin: 0 0 0.25rem; font-size: 0.9rem;">{file_type['name']}</h4>
                        <p style="color: #94A3B8; margin: 0 0 0.5rem; font-size: 0.7rem;">{file_type['description']}</p>
                        <p style="color: #64748B; margin: 0; font-size: 0.65rem;">.{', .'.join(file_type['extensions'])}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
                # File uploader
                uploaded_file = st.file_uploader(
                    f"Upload {file_type['name']}",
                    type=file_type["extensions"],
                    key=f"upload_{file_type['name'].replace(' ', '_').lower()}",
                    label_visibility="collapsed",
                )
                
                if uploaded_file:
                    # Add to uploaded files
                    files = get_wizard_data("uploaded_files", [])
                    file_info = {
                        "name": uploaded_file.name,
                        "type": file_type["name"],
                        "size": len(uploaded_file.getvalue()),
                        "uploaded_at": datetime.now().isoformat(),
                    }
                    if file_info not in files:
                        files.append(file_info)
                        set_wizard_data("uploaded_files", files)
                    
                    # Show success state
                    st.success(f"✅ {uploaded_file.name} uploaded")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display uploaded files
    uploaded_files = get_wizard_data("uploaded_files", [])
    if uploaded_files:
        st.markdown(
            """
            <div style="
                background: rgba(30, 30, 63, 0.8);
                border: 1px solid rgba(99, 102, 241, 0.2);
                border-radius: 12px;
                padding: 1.25rem;
                margin-top: 1rem;
            ">
                <h4 style="color: #F1F5F9; margin: 0 0 1rem; font-size: 0.95rem;">📁 Uploaded Files</h4>
            """,
            unsafe_allow_html=True,
        )
        
        for i, file in enumerate(uploaded_files):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <span style="font-size: 1.25rem;">📄</span>
                        <div>
                            <p style="margin: 0; color: #F1F5F9; font-size: 0.85rem;">{file['name']}</p>
                            <p style="margin: 0; color: #64748B; font-size: 0.7rem;">{file['type']} • {file['size']} bytes</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            
            with col3:
                if st.button("🗑️", key=f"remove_file_{i}"):
                    files = get_wizard_data("uploaded_files", [])
                    files.pop(i)
                    set_wizard_data("uploaded_files", files)
                    st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<p style='color: #64748B; font-size: 0.75rem; margin-top: 1rem;'>💡 All uploads are optional. You can proceed with mission creation without documents.</p>", unsafe_allow_html=True)


# =============================================================================
# STEP 3: Testing Types
# =============================================================================

def render_step_3() -> None:
    """Render Step 3: Testing Types."""
    step_section("Select Testing Types", "🧪")
    
    st.markdown(
        '<p style="color: #94A3B8; font-size: 0.875rem; margin-bottom: 1.5rem;">Choose the types of testing to include in your mission</p>',
        unsafe_allow_html=True,
    )
    
    # Testing types configuration
    testing_types = [
        {
            "name": "Frontend",
            "icon": "🖥️",
            "description": "UI/UX testing, form validation, navigation",
            "estimated_time": "15 min",
        },
        {
            "name": "Backend",
            "icon": "⚙️",
            "description": "Business logic, data processing, integrations",
            "estimated_time": "20 min",
        },
        {
            "name": "API",
            "icon": "🔗",
            "description": "REST/GraphQL endpoint testing",
            "estimated_time": "25 min",
        },
        {
            "name": "Smoke",
            "icon": "💨",
            "description": "Quick validation of critical features",
            "estimated_time": "5 min",
        },
        {
            "name": "Sanity",
            "icon": "🧘",
            "description": "Basic functionality check",
            "estimated_time": "10 min",
        },
        {
            "name": "Regression",
            "icon": "🔄",
            "description": "Full regression test suite",
            "estimated_time": "45 min",
        },
        {
            "name": "End to End",
            "icon": "🎭",
            "description": "Complete user journey testing",
            "estimated_time": "30 min",
        },
        {
            "name": "Accessibility",
            "icon": "♿",
            "description": "WCAG compliance verification",
            "estimated_time": "15 min",
        },
        {
            "name": "Visual",
            "icon": "👁️",
            "description": "Visual regression testing",
            "estimated_time": "20 min",
        },
        {
            "name": "Cross Browser",
            "icon": "🌐",
            "description": "Multi-browser compatibility",
            "estimated_time": "25 min",
        },
        {
            "name": "Performance",
            "icon": "⚡",
            "description": "Load and stress testing",
            "estimated_time": "30 min",
        },
        {
            "name": "Security",
            "icon": "🔒",
            "description": "Vulnerability and penetration testing",
            "estimated_time": "35 min",
        },
        {
            "name": "Database",
            "icon": "🗄️",
            "description": "Data integrity and query validation",
            "estimated_time": "15 min",
        },
        {
            "name": "Mobile",
            "icon": "📱",
            "description": "Mobile responsive testing",
            "estimated_time": "20 min",
        },
    ]
    
    # Display in 2 columns
    selected_types = get_wizard_data("testing_types", [])
    
    for i in range(0, len(testing_types), 2):
        cols = st.columns(2)
        
        for j, test_type in enumerate(testing_types[i:i+2]):
            with cols[j]:
                is_selected = test_type["name"] in selected_types
                
                # Card
                border_color = "#6366F1" if is_selected else "#334155"
                bg_color = "rgba(99, 102, 241, 0.15)" if is_selected else "rgba(30, 30, 63, 0.8)"
                
                # Checkbox
                checked = st.checkbox(
                    f"Select {test_type['name']}",
                    value=is_selected,
                    key=f"test_type_{test_type['name']}",
                    label_visibility="collapsed",
                )
                
                # Update selection
                if checked and test_type["name"] not in selected_types:
                    selected_types.append(test_type["name"])
                    set_wizard_data("testing_types", selected_types)
                elif not checked and test_type["name"] in selected_types:
                    selected_types.remove(test_type["name"])
                    set_wizard_data("testing_types", selected_types)
                
                # Card display
                st.markdown(
                    f"""
                    <div style="
                        background: {bg_color};
                        border: 2px solid {border_color};
                        border-radius: 12px;
                        padding: 1rem;
                        margin-top: -45px;
                        transition: all 0.2s ease;
                    ">
                        <div style="display: flex; align-items: start; gap: 1rem;">
                            <div style="
                                width: 40px;
                                height: 40px;
                                border-radius: 10px;
                                background: rgba(99, 102, 241, 0.2);
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                font-size: 1.25rem;
                                flex-shrink: 0;
                            ">{test_type['icon']}</div>
                            <div style="flex: 1;">
                                <h4 style="color: #F1F5F9; margin: 0 0 0.25rem; font-size: 0.95rem;">{test_type['name']}</h4>
                                <p style="color: #94A3B8; margin: 0 0 0.5rem; font-size: 0.8rem;">{test_type['description']}</p>
                                <span style="
                                    display: inline-flex;
                                    align-items: center;
                                    gap: 0.25rem;
                                    padding: 0.2rem 0.5rem;
                                    background: rgba(99, 102, 241, 0.2);
                                    border-radius: 4px;
                                    font-size: 0.7rem;
                                    color: #6366F1;
                                ">⏱️ {test_type['estimated_time']}</span>
                            </div>
                            <div style="
                                width: 24px;
                                height: 24px;
                                border-radius: 50%;
                                border: 2px solid {border_color};
                                background: {'#6366F1' if is_selected else 'transparent'};
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                color: white;
                                font-size: 0.8rem;
                                flex-shrink: 0;
                            ">{'✓' if is_selected else ''}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick selection buttons
    st.markdown(
        """
        <div style="
            background: rgba(30, 30, 63, 0.5);
            border-radius: 12px;
            padding: 1rem;
            margin-top: 1rem;
        ">
            <h4 style="color: #F1F5F9; margin: 0 0 0.75rem; font-size: 0.9rem;">⚡ Quick Select</h4>
        """,
        unsafe_allow_html=True,
    )
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔥 Critical\n(Smoke + API)", use_container_width=True):
            set_wizard_data("testing_types", ["Smoke", "API"])
            st.rerun()
    
    with col2:
        if st.button("📋 Standard\n(Smoke + Sanity + Regression)", use_container_width=True):
            set_wizard_data("testing_types", ["Smoke", "Sanity", "Regression"])
            st.rerun()
    
    with col3:
        if st.button("🎯 Full\n(All Types)", use_container_width=True):
            set_wizard_data("testing_types", [t["name"] for t in testing_types])
            st.rerun()
    
    with col4:
        if st.button("🔒 Security\n(Security + API)", use_container_width=True):
            set_wizard_data("testing_types", ["Security", "API"])
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)


# =============================================================================
# STEP 4: Execution Configuration
# =============================================================================

def render_step_4() -> None:
    """Render Step 4: Execution Configuration."""
    step_section("Execution Configuration", "⚙️")
    
    st.markdown(
        '<p style="color: #94A3B8; font-size: 0.875rem; margin-bottom: 1.5rem;">Configure how and where your mission will be executed</p>',
        unsafe_allow_html=True,
    )
    
    # Execution Mode
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <h4 style="color: #F1F5F9; margin: 0 0 0.75rem; font-size: 0.95rem;">🎛️ Execution Mode</h4>
            <p style="color: #64748B; font-size: 0.8rem; margin: 0 0 1rem;">Select how AI should handle test execution and reporting</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    execution_modes = [
        {"label": "Autonomous", "icon": "🤖", "description": "AI runs tests independently", "color": "#10B981"},
        {"label": "Review", "icon": "👁️", "description": "AI reviews, you approve", "color": "#F59E0B"},
        {"label": "Hybrid", "icon": "🔀", "description": "AI + Human collaboration", "color": "#6366F1"},
        {"label": "Manual", "icon": "👤", "description": "Guided manual execution", "color": "#64748B"},
    ]
    
    cols = st.columns(4)
    current_mode = get_wizard_data("execution_mode")
    
    for i, mode in enumerate(execution_modes):
        with cols[i]:
            is_selected = current_mode == mode["label"]
            
            if st.button(
                f"{mode['icon']}\n{mode['label']}",
                key=f"exec_mode_{mode['label']}",
                use_container_width=True,
            ):
                set_wizard_data("execution_mode", mode["label"])
                st.rerun()
            
            st.markdown(
                f"""
                <p style="
                    text-align: center;
                    margin: -0.5rem 0 0;
                    color: {'#6366F1' if is_selected else '#64748B'};
                    font-size: 0.7rem;
                ">{mode['description']}</p>
                """,
                unsafe_allow_html=True,
            )
    
    st.markdown("<hr style='margin: 1.5rem 0; border-color: #334155;'>", unsafe_allow_html=True)
    
    # Parallel Execution & Browser
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            <div style="
                background: rgba(30, 30, 63, 0.8);
                border: 1px solid rgba(99, 102, 241, 0.2);
                border-radius: 12px;
                padding: 1.25rem;
            ">
                <h4 style="color: #F1F5F9; margin: 0 0 0.75rem; font-size: 0.95rem;">🔀 Parallel Execution</h4>
            """,
            unsafe_allow_html=True,
        )
        
        workers = st.slider(
            "Number of Workers",
            min_value=1,
            max_value=10,
            value=get_wizard_data("parallel_workers", 1),
            step=1,
        )
        set_wizard_data("parallel_workers", workers)
        
        st.markdown(
            f"<p style='color: #94A3B8; font-size: 0.8rem;'>Run {workers} test suite(s) in parallel for faster execution</p>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(
            """
            <div style="
                background: rgba(30, 30, 63, 0.8);
                border: 1px solid rgba(99, 102, 241, 0.2);
                border-radius: 12px;
                padding: 1.25rem;
            ">
                <h4 style="color: #F1F5F9; margin: 0 0 0.75rem; font-size: 0.95rem;">🌐 Browser Selection</h4>
            """,
            unsafe_allow_html=True,
        )
        
        browsers = ["Chrome", "Firefox", "Edge", "Safari"]
        current_browser = get_wizard_data("browser")
        
        browser = st.selectbox(
            "Select Browser",
            browsers,
            index=browsers.index(current_browser) if current_browser in browsers else 0,
        )
        set_wizard_data("browser", browser)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 1.5rem 0; border-color: #334155;'>", unsafe_allow_html=True)
    
    # Advanced Configuration
    st.markdown(
        """
        <div style="
            background: rgba(30, 30, 63, 0.8);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 12px;
            padding: 1.25rem;
        ">
            <h4 style="color: #F1F5F9; margin: 0 0 1rem; font-size: 0.95rem;">⚡ Advanced Settings</h4>
        """,
        unsafe_allow_html=True,
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<label style='color: #94A3B8; font-size: 0.8rem;'>Retry Count</label>", unsafe_allow_html=True)
        retry = st.number_input(
            "Retry Count",
            min_value=0,
            max_value=5,
            value=get_wizard_data("retry_count", 1),
            step=1,
            label_visibility="collapsed",
        )
        set_wizard_data("retry_count", retry)
        
        st.markdown("<label style='color: #94A3B8; font-size: 0.8rem; margin-top: 1rem; display: block;'>Timeout (seconds)</label>", unsafe_allow_html=True)
        timeout = st.number_input(
            "Timeout",
            min_value=10,
            max_value=300,
            value=get_wizard_data("timeout", 30),
            step=10,
            label_visibility="collapsed",
        )
        set_wizard_data("timeout", timeout)
    
    with col2:
        st.markdown("<label style='color: #94A3B8; font-size: 0.8rem;'>Capture Options</label>", unsafe_allow_html=True)
        
        screenshots = st.checkbox(
            "📷 Screenshots",
            value=get_wizard_data("screenshots", True),
        )
        set_wizard_data("screenshots", screenshots)
        
        video = st.checkbox(
            "🎥 Video Recording",
            value=get_wizard_data("video_recording", False),
        )
        set_wizard_data("video_recording", video)
        
        logs = st.checkbox(
            "📝 Detailed Logs",
            value=get_wizard_data("logs_enabled", True),
        )
        set_wizard_data("logs_enabled", logs)
    
    with col3:
        st.markdown("<label style='color: #94A3B8; font-size: 0.8rem;'>Report Options</label>", unsafe_allow_html=True)
        
        gen_docs = st.checkbox(
            "📄 Generate Documentation",
            value=get_wizard_data("generate_docs", True),
        )
        set_wizard_data("generate_docs", gen_docs)
        
        gen_bugs = st.checkbox(
            "🐛 Generate Bug Reports",
            value=get_wizard_data("generate_bug_report", True),
        )
        set_wizard_data("generate_bug_report", gen_bugs)
    
    st.markdown("</div>", unsafe_allow_html=True)


# =============================================================================
# STEP 5: Mission Summary
# =============================================================================

def render_step_5() -> None:
    """Render Step 5: Mission Summary."""
    step_section("Mission Summary", "📊")
    
    st.markdown(
        '<p style="color: #94A3B8; font-size: 0.875rem; margin-bottom: 1.5rem;">Review your mission configuration before launching</p>',
        unsafe_allow_html=True,
    )
    
    data = st.session_state.wizard_data
    
    # Summary Card
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(30, 30, 63, 0.95) 0%, rgba(99, 102, 241, 0.15) 100%);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 1.5rem;
        ">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
                <div style="
                    width: 56px;
                    height: 56px;
                    border-radius: 12px;
                    background: linear-gradient(135deg, #6366F1, #8B5CF6);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.75rem;
                ">🎯</div>
                <div>
                    <h2 style="color: #F1F5F9; margin: 0; font-size: 1.5rem;">""" + data.get("mission_name", "Unnamed Mission") + """</h2>
                    <p style="color: #94A3B8; margin: 0.25rem 0 0; font-size: 0.9rem;">""" + (data.get("mission_description", "No description") if data.get("mission_description") else "No description provided") + """</p>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Details grid
    col1, col2 = st.columns(2)
    
    with col1:
        summary_item("📦 Project", data.get("project", "Not specified"), "📦")
        summary_item("🖥️ Application", data.get("app_name", "Not specified"), "🖥️")
        summary_item("🔗 URL", data.get("app_url", "Not specified"), "🔗")
        summary_item("🌍 Environment", data.get("environment", "Not specified"), "🌍")
    
    with col2:
        priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(data.get("priority", ""), "⚪")
        summary_item(f"{priority_color} Priority", data.get("priority", "Not specified"), "⚡")
        summary_item("⏱️ Est. Time", data.get("estimated_time", "Not specified"), "⏱️")
        summary_item("🔐 Auth", data.get("auth_required", "No"), "🔐")
        summary_item("🎛️ Mode", data.get("execution_mode", "Not specified"), "🎛️")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Testing Types
    testing_types = data.get("testing_types", [])
    if testing_types:
        st.markdown(
            """
            <div style="
                background: rgba(30, 30, 63, 0.8);
                border: 1px solid rgba(99, 102, 241, 0.2);
                border-radius: 12px;
                padding: 1.25rem;
                margin-bottom: 1.5rem;
            ">
                <h4 style="color: #F1F5F9; margin: 0 0 1rem; font-size: 0.95rem;">🧪 Selected Testing Types</h4>
                <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
            """,
            unsafe_allow_html=True,
        )
        
        for test_type in testing_types:
            st.markdown(
                f"""
                <span style="
                    display: inline-flex;
                    align-items: center;
                    gap: 0.25rem;
                    padding: 0.4rem 0.75rem;
                    background: rgba(99, 102, 241, 0.2);
                    border: 1px solid rgba(99, 102, 241, 0.3);
                    border-radius: 20px;
                    font-size: 0.8rem;
                    color: #818CF8;
                ">{test_type}</span>
                """,
                unsafe_allow_html=True,
            )
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Uploaded Files
    uploaded_files = data.get("uploaded_files", [])
    if uploaded_files:
        st.markdown(
            """
            <div style="
                background: rgba(30, 30, 63, 0.8);
                border: 1px solid rgba(99, 102, 241, 0.2);
                border-radius: 12px;
                padding: 1.25rem;
                margin-bottom: 1.5rem;
            ">
                <h4 style="color: #F1F5F9; margin: 0 0 1rem; font-size: 0.95rem;">📄 Uploaded Documents</h4>
            """,
            unsafe_allow_html=True,
        )
        
        for file in uploaded_files:
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0; border-bottom: 1px solid #334155;">
                    <span>📄</span>
                    <span style="color: #F1F5F9;">{file['name']}</span>
                    <span style="color: #64748B; font-size: 0.8rem;">({file['type']})</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Execution Configuration
    st.markdown(
        """
        <div style="
            background: rgba(30, 30, 63, 0.8);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1.5rem;
        ">
            <h4 style="color: #F1F5F9; margin: 0 0 1rem; font-size: 0.95rem;">⚙️ Execution Configuration</h4>
        """,
        unsafe_allow_html=True,
    )
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        summary_item("🔀 Workers", str(data.get("parallel_workers", 1)), "🔀")
    
    with col2:
        summary_item("🌐 Browser", data.get("browser", "Chrome"), "🌐")
    
    with col3:
        summary_item("🔄 Retries", str(data.get("retry_count", 1)), "🔄")
    
    with col4:
        summary_item("⏱️ Timeout", f"{data.get('timeout', 30)}s", "⏱️")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Capture Options
    capture_opts = []
    if data.get("screenshots"):
        capture_opts.append("📷 Screenshots")
    if data.get("video_recording"):
        capture_opts.append("🎥 Video")
    if data.get("logs_enabled"):
        capture_opts.append("📝 Logs")
    
    report_opts = []
    if data.get("generate_docs"):
        report_opts.append("📄 Docs")
    if data.get("generate_bug_report"):
        report_opts.append("🐛 Bugs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            <div style="
                background: rgba(30, 30, 63, 0.8);
                border: 1px solid rgba(99, 102, 241, 0.2);
                border-radius: 12px;
                padding: 1.25rem;
            ">
                <h4 style="color: #F1F5F9; margin: 0 0 0.75rem; font-size: 0.9rem;">📸 Capture</h4>
            """,
            unsafe_allow_html=True,
        )
        if capture_opts:
            for opt in capture_opts:
                st.markdown(f"<span style='color: #94A3B8; font-size: 0.85rem;'>{opt}</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span style='color: #64748B; font-size: 0.85rem;'>None selected</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(
            """
            <div style="
                background: rgba(30, 30, 63, 0.8);
                border: 1px solid rgba(99, 102, 241, 0.2);
                border-radius: 12px;
                padding: 1.25rem;
            ">
                <h4 style="color: #F1F5F9; margin: 0 0 0.75rem; font-size: 0.9rem;">📊 Reports</h4>
            """,
            unsafe_allow_html=True,
        )
        if report_opts:
            for opt in report_opts:
                st.markdown(f"<span style='color: #94A3B8; font-size: 0.85rem;'>{opt}</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span style='color: #64748B; font-size: 0.85rem;'>None selected</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Estimated Coverage & Cost
    coverage = min(95, 30 + len(testing_types) * 12)
    estimated_cost = f"${5 + len(testing_types) * 2}.00"
    
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(30, 30, 63, 0.9) 100%);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 12px;
            padding: 1.5rem;
            margin-top: 1rem;
        ">
            <h4 style="color: #10B981; margin: 0 0 1rem; font-size: 0.95rem;">📊 Mission Estimates</h4>
            <div style="display: flex; gap: 2rem;">
                <div>
                    <p style="color: #94A3B8; margin: 0; font-size: 0.8rem;">Estimated Coverage</p>
                    <p style="color: #10B981; margin: 0.25rem 0 0; font-size: 1.5rem; font-weight: 600;">{coverage}%</p>
                </div>
                <div>
                    <p style="color: #94A3B8; margin: 0; font-size: 0.8rem;">Estimated Cost</p>
                    <p style="color: #F1F5F9; margin: 0.25rem 0 0; font-size: 1.5rem; font-weight: 600;">{estimated_cost}</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
