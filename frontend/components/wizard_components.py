"""Reusable wizard components for AI-QOS Mission Planner."""
import streamlit as st
from typing import Optional, List, Dict, Any, Callable
from datetime import datetime


# ============================================================================
# Wizard State Management
# ============================================================================

def init_wizard_state() -> None:
    """Initialize wizard session state."""
    defaults = {
        "wizard_step": 1,
        "wizard_data": {
            # Step 1: Mission Information
            "mission_name": "",
            "mission_description": "",
            "project": "",
            "app_name": "",
            "app_url": "",
            "environment": None,
            "auth_required": None,
            "credentials": {"username": "", "password": ""},
            "estimated_time": "",
            "priority": None,
            # Step 2: Upload Documents
            "uploaded_files": [],
            # Step 3: Testing Types
            "testing_types": [],
            # Step 4: Execution Configuration
            "execution_mode": None,
            "parallel_workers": 1,
            "browser": None,
            "retry_count": 1,
            "timeout": 30,
            "screenshots": True,
            "video_recording": False,
            "logs_enabled": True,
            "generate_docs": True,
            "generate_bug_report": True,
        },
        "wizard_validated": {},
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_wizard_data(key: str, default: Any = None) -> Any:
    """Get wizard data from session state."""
    return st.session_state.wizard_data.get(key, default)


def set_wizard_data(key: str, value: Any) -> None:
    """Set wizard data in session state."""
    st.session_state.wizard_data[key] = value


def validate_step(step: int) -> Dict[str, Any]:
    """Validate current step and return validation results."""
    data = st.session_state.wizard_data
    
    if step == 1:
        errors = []
        if not data.get("mission_name", "").strip():
            errors.append("Mission name is required")
        if not data.get("app_url", "").strip():
            errors.append("Application URL is required")
        if not data.get("environment"):
            errors.append("Environment is required")
        if not data.get("priority"):
            errors.append("Priority is required")
        if data.get("auth_required") == "Yes":
            if not data.get("credentials", {}).get("username"):
                errors.append("Username is required when authentication is enabled")
        
        st.session_state.wizard_validated[1] = len(errors) == 0
        return {"valid": len(errors) == 0, "errors": errors}
    
    elif step == 2:
        # Upload is optional
        st.session_state.wizard_validated[2] = True
        return {"valid": True, "errors": []}
    
    elif step == 3:
        errors = []
        if not data.get("testing_types"):
            errors.append("At least one testing type is required")
        
        st.session_state.wizard_validated[3] = len(errors) == 0
        return {"valid": len(errors) == 0, "errors": errors}
    
    elif step == 4:
        errors = []
        if not data.get("execution_mode"):
            errors.append("Execution mode is required")
        if not data.get("browser"):
            errors.append("Browser selection is required")
        
        st.session_state.wizard_validated[4] = len(errors) == 0
        return {"valid": len(errors) == 0, "errors": errors}
    
    elif step == 5:
        # Final validation
        return {"valid": True, "errors": []}
    
    return {"valid": True, "errors": []}


# ============================================================================
# Wizard Navigation Components
# ============================================================================

def wizard_stepper(current_step: int, total_steps: int = 5) -> None:
    """Display horizontal stepper for wizard progress."""
    steps = [
        "Mission Info",
        "Documents",
        "Testing Types",
        "Configuration",
        "Summary",
    ]
    
    icons = ["📋", "📄", "🧪", "⚙️", "📊"]
    
    cols = st.columns(total_steps)
    
    for i, (step, icon) in enumerate(zip(steps, icons), 1):
        with cols[i - 1]:
            is_completed = i < current_step
            is_current = i == current_step
            is_validated = st.session_state.wizard_validated.get(i, False)
            
            if is_completed:
                bg_color = "#10B981"
                border_color = "#10B981"
            elif is_current:
                bg_color = "#6366F1"
                border_color = "#6366F1"
            else:
                bg_color = "#334155"
                border_color = "#334155"
            
            st.markdown(
                f"""
                <div style="text-align: center; padding: 0.5rem;">
                    <div style="
                        width: 40px;
                        height: 40px;
                        border-radius: 50%;
                        background: {bg_color};
                        border: 2px solid {border_color};
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 0 auto 0.5rem;
                        font-size: 1.25rem;
                    ">
                        {'✓' if is_completed else icon}
                    </div>
                    <p style="
                        margin: 0;
                        font-size: 0.75rem;
                        color: {'#10B981' if is_completed else '#F1F5F9' if is_current else '#64748B'};
                        font-weight: {600 if is_current else 400};
                    ">{step}</p>
                    <p style="
                        margin: 0.25rem 0 0;
                        font-size: 0.65rem;
                        color: #64748B;
                    ">Step {i}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
            # Connectors
            if i < total_steps:
                connector_color = "#10B981" if i < current_step else "#334155"
                st.markdown(
                    f"""
                    <div style="
                        position: absolute;
                        top: 25px;
                        left: calc({(i) * 20}% + 20px);
                        width: calc(20% - 40px);
                        height: 2px;
                        background: {connector_color};
                    "></div>
                    """,
                    unsafe_allow_html=True,
                )


def validation_badge(is_valid: bool, message: str = "") -> None:
    """Display validation status badge."""
    if is_valid:
        st.markdown(
            f"""
            <span style="
                display: inline-flex;
                align-items: center;
                gap: 0.25rem;
                padding: 0.25rem 0.5rem;
                border-radius: 4px;
                font-size: 0.7rem;
                background: rgba(16, 185, 129, 0.2);
                color: #10B981;
            ">
                ✓ {message or 'Valid'}
            </span>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <span style="
                display: inline-flex;
                align-items: center;
                gap: 0.25rem;
                padding: 0.25rem 0.5rem;
                border-radius: 4px;
                font-size: 0.7rem;
                background: rgba(239, 68, 68, 0.2);
                color: #EF4444;
            ">
                ✗ {message or 'Invalid'}
            </span>
            """,
            unsafe_allow_html=True,
        )


def step_section(title: str, icon: str = "📋") -> None:
    """Display step section header."""
    st.markdown(
        f"""
        <div style="margin-bottom: 1.5rem;">
            <h2 style="
                font-size: 1.5rem;
                font-weight: 600;
                color: #F1F5F9;
                margin: 0 0 0.25rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            ">
                <span>{icon}</span>
                <span>{title}</span>
            </h2>
            <div style="height: 2px; background: linear-gradient(90deg, #6366F1, transparent); margin-top: 0.5rem;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# Form Components
# ============================================================================

def glass_card(content_fn: Callable, **kwargs) -> None:
    """Create a glass morphism card container."""
    st.markdown(
        """
        <div style="
            background: rgba(30, 30, 63, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        ">
        """,
        unsafe_allow_html=True,
    )
    content_fn(**kwargs)
    st.markdown("</div>", unsafe_allow_html=True)


def input_field(
    label: str,
    key: str,
    placeholder: str = "",
    help_text: str = "",
    required: bool = False,
    input_type: str = "text",
) -> str:
    """Render a styled input field."""
    label_html = f'<label style="color: #94A3B8; font-size: 0.875rem; margin-bottom: 0.25rem; display: block;">{label}{" *" if required else ""}</label>'
    st.markdown(label_html, unsafe_allow_html=True)
    
    if help_text:
        st.markdown(
            f'<p style="color: #64748B; font-size: 0.75rem; margin: 0 0 0.5rem;">{help_text}</p>',
            unsafe_allow_html=True,
        )
    
    value = get_wizard_data(key, "")
    return st.text_input(
        label,
        value=value,
        placeholder=placeholder,
        label_visibility="collapsed",
        key=f"input_{key}",
    )


def select_field(
    label: str,
    key: str,
    options: List[str],
    help_text: str = "",
    required: bool = False,
) -> str:
    """Render a styled select field."""
    st.markdown(
        f'<label style="color: #94A3B8; font-size: 0.875rem; margin-bottom: 0.25rem; display: block;">{label}{" *" if required else ""}</label>',
        unsafe_allow_html=True,
    )
    
    if help_text:
        st.markdown(
            f'<p style="color: #64748B; font-size: 0.75rem; margin: 0 0 0.5rem;">{help_text}</p>',
            unsafe_allow_html=True,
        )
    
    value = get_wizard_data(key)
    index = options.index(value) if value in options else 0
    return st.selectbox(
        label,
        options=options,
        index=index,
        label_visibility="collapsed",
        key=f"select_{key}",
    )


def checkbox_field(
    label: str,
    key: str,
    help_text: str = "",
) -> bool:
    """Render a styled checkbox field."""
    checked = get_wizard_data(key, False)
    return st.checkbox(label, value=checked, key=f"checkbox_{key}")


# ============================================================================
# Upload Components
# ============================================================================

def file_upload_card(
    file_type: str,
    icon: str,
    description: str,
    extensions: List[str],
) -> Dict[str, Any]:
    """Render a drag-and-drop file upload card."""
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, rgba(30, 30, 63, 0.9) 0%, rgba(99, 102, 241, 0.1) 100%);
            border: 2px dashed rgba(99, 102, 241, 0.3);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            transition: all 0.3s ease;
        ">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
            <h4 style="color: #F1F5F9; margin: 0 0 0.25rem;">{file_type}</h4>
            <p style="color: #94A3B8; font-size: 0.75rem; margin: 0 0 0.5rem;">{description}</p>
            <p style="color: #64748B; font-size: 0.7rem; margin: 0;">{', '.join(extensions)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    uploaded_file = st.file_uploader(
        f"Upload {file_type}",
        type=extensions,
        key=f"upload_{file_type}",
        label_visibility="collapsed",
    )
    
    return {"file": uploaded_file, "type": file_type}


# ============================================================================
# Testing Type Card
# ============================================================================

def testing_type_card(
    test_type: str,
    icon: str,
    description: str,
    estimated_time: str,
    is_selected: bool = False,
) -> bool:
    """Render a selectable testing type card."""
    border_color = "#6366F1" if is_selected else "#334155"
    bg_color = "rgba(99, 102, 241, 0.15)" if is_selected else "transparent"
    
    st.markdown(
        f"""
        <div style="
            background: {bg_color};
            border: 2px solid {border_color};
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 0.5rem;
            cursor: pointer;
            transition: all 0.2s ease;
        ">
            <div style="display: flex; align-items: start; gap: 1rem;">
                <div style="
                    width: 36px;
                    height: 36px;
                    border-radius: 8px;
                    background: rgba(99, 102, 241, 0.2);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.25rem;
                    flex-shrink: 0;
                ">{icon}</div>
                <div style="flex: 1;">
                    <h4 style="color: #F1F5F9; margin: 0 0 0.25rem; font-size: 0.95rem;">{test_type}</h4>
                    <p style="color: #94A3B8; margin: 0 0 0.5rem; font-size: 0.8rem;">{description}</p>
                    <span style="
                        display: inline-flex;
                        align-items: center;
                        gap: 0.25rem;
                        padding: 0.2rem 0.5rem;
                        background: rgba(99, 102, 241, 0.2);
                        border-radius: 4px;
                        font-size: 0.7rem;
                        color: #6366F1;
                    ">⏱️ {estimated_time}</span>
                </div>
                <div style="
                    width: 24px;
                    height: 24px;
                    border-radius: 50%;
                    border: 2px solid {'#6366F1' if is_selected else '#334155'};
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
    
    return st.checkbox(
        f"Select {test_type}",
        value=is_selected,
        key=f"test_type_{test_type}",
        label_visibility="collapsed",
    )


# ============================================================================
# Configuration Card
# ============================================================================

def config_card(
    title: str,
    icon: str,
    description: str,
    options: List[Dict[str, Any]],
    key: str,
    selected: Optional[str] = None,
) -> str:
    """Render a configuration selection card with options."""
    st.markdown(
        f"""
        <div style="
            background: rgba(30, 30, 63, 0.8);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1rem;
        ">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;">
                <span style="font-size: 1.5rem;">{icon}</span>
                <div>
                    <h4 style="color: #F1F5F9; margin: 0;">{title}</h4>
                    <p style="color: #94A3B8; margin: 0; font-size: 0.8rem;">{description}</p>
                </div>
            </div>
            <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
            """,
        unsafe_allow_html=True,
    )
    
    cols = st.columns(len(options))
    result = selected
    
    for i, opt in enumerate(options):
        with cols[i]:
            opt_key = f"config_{key}_{opt['value']}"
            is_selected = (selected == opt["value"]) if selected else False
            
            bg_color = "#6366F1" if is_selected else "#1E1E3F"
            border_color = "#6366F1" if is_selected else "#334155"
            
            if st.button(
                f"{opt['icon']} {opt['label']}",
                key=opt_key,
            ):
                result = opt["value"]
                set_wizard_data(key, opt["value"])
            
            st.markdown("</button>", unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    return result


# ============================================================================
# Summary Card
# ============================================================================

def summary_item(label: str, value: Any, icon: str = "📋") -> None:
    """Render a summary item."""
    st.markdown(
        f"""
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem 0;
            border-bottom: 1px solid #334155;
        ">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <span style="font-size: 1.25rem;">{icon}</span>
                <span style="color: #94A3B8; font-size: 0.875rem;">{label}</span>
            </div>
            <span style="color: #F1F5F9; font-weight: 500;">{value}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# AI Assistant Panel
# ============================================================================

def ai_assistant_panel(step: int) -> None:
    """Render AI assistant panel with context-aware tips."""
    tips = {
        1: {
            "title": "💡 Mission Setup Tips",
            "items": [
                "Use descriptive mission names like 'API Regression Suite'",
                "Include the full application URL including protocol",
                "Match environment to your testing stage",
            ],
        },
        2: {
            "title": "📄 Document Guidelines",
            "items": [
                "Upload Swagger/OpenAPI specs for API testing",
                "BRD helps AI understand business requirements",
                "Test case spreadsheets speed up test creation",
            ],
        },
        3: {
            "title": "🧪 Testing Strategy",
            "items": [
                "Start with Smoke + Sanity for quick validation",
                "Add Regression for comprehensive coverage",
                "API + Backend testing catches integration issues",
            ],
        },
        4: {
            "title": "⚙️ Performance Tips",
            "items": [
                "Use parallel execution for faster results",
                "Enable screenshots for debugging failed tests",
                "Set appropriate timeouts for slow endpoints",
            ],
        },
        5: {
            "title": "📊 Launch Checklist",
            "items": [
                "Review all selections before launching",
                "Save draft to continue later",
                "Estimated coverage improves with more test types",
            ],
        },
    }
    
    current_tip = tips.get(step, tips[1])
    
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(30, 30, 63, 0.9) 100%);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 12px;
            padding: 1.25rem;
            height: 100%;
        ">
            <h4 style="color: #F1F5F9; margin: 0 0 1rem; display: flex; align-items: center; gap: 0.5rem;">
                🤖 AI Assistant
            </h4>
            <h5 style="color: #6366F1; margin: 0 0 0.75rem; font-size: 0.9rem;">{current_tip['title']}</h5>
        """,
        unsafe_allow_html=True,
    )
    
    for item in current_tip["items"]:
        st.markdown(
            f"""
            <div style="
                display: flex;
                align-items: start;
                gap: 0.5rem;
                padding: 0.5rem 0;
                border-bottom: 1px solid rgba(99, 102, 241, 0.1);
            ">
                <span style="color: #22D3EE; font-size: 0.8rem;">▸</span>
                <span style="color: #94A3B8; font-size: 0.8rem;">{item}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    # Coverage estimate
    if step >= 3:
        testing_types = get_wizard_data("testing_types", [])
        coverage = min(95, 30 + len(testing_types) * 12)
        
        st.markdown(
            f"""
            <div style="
                margin-top: 1rem;
                padding: 1rem;
                background: rgba(16, 185, 129, 0.1);
                border-radius: 8px;
                border: 1px solid rgba(16, 185, 129, 0.3);
            ">
                <p style="color: #10B981; margin: 0 0 0.5rem; font-size: 0.8rem; font-weight: 500;">
                    📊 Estimated Coverage
                </p>
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <div style="flex: 1; height: 8px; background: #334155; border-radius: 4px;">
                        <div style="width: {coverage}%; height: 100%; background: #10B981; border-radius: 4px;"></div>
                    </div>
                    <span style="color: #10B981; font-weight: 600;">{coverage}%</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# Progress Sidebar
# ============================================================================

def progress_sidebar(current_step: int) -> None:
    """Render progress sidebar."""
    steps = [
        ("1", "Mission Info", "📋"),
        ("2", "Documents", "📄"),
        ("3", "Testing Types", "🧪"),
        ("4", "Configuration", "⚙️"),
        ("5", "Summary", "📊"),
    ]
    
    st.markdown(
        """
        <div style="
            background: rgba(30, 30, 63, 0.5);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
        ">
            <h4 style="color: #F1F5F9; margin: 0 0 1rem; font-size: 0.95rem;">📍 Mission Progress</h4>
        """,
        unsafe_allow_html=True,
    )
    
    for step_num, title, icon in steps:
        is_completed = int(step_num) < current_step
        is_current = int(step_num) == current_step
        is_valid = st.session_state.wizard_validated.get(int(step_num), False)
        
        if is_completed:
            color = "#10B981"
            icon_display = "✓"
        elif is_current:
            color = "#6366F1"
            icon_display = icon
        else:
            color = "#64748B"
            icon_display = step_num
        
        st.markdown(
            f"""
            <div style="
                display: flex;
                align-items: center;
                gap: 0.75rem;
                padding: 0.75rem;
                background: {'rgba(99, 102, 241, 0.1)' if is_current else 'transparent'};
                border-radius: 8px;
                margin-bottom: 0.5rem;
                border-left: 3px solid {color};
            ">
                <div style="
                    width: 28px;
                    height: 28px;
                    border-radius: 50%;
                    background: {color};
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 0.8rem;
                    color: white;
                    flex-shrink: 0;
                ">{icon_display}</div>
                <div style="flex: 1;">
                    <p style="margin: 0; color: {'#F1F5F9' if is_current else '#94A3B8'}; font-size: 0.85rem;">{title}</p>
                </div>
                {'✅' if is_completed else '⏳' if is_current else '⭕'}
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# Action Buttons
# ============================================================================

def wizard_actions(
    current_step: int,
    total_steps: int = 5,
    show_launch: bool = False,
) -> Optional[str]:
    """Render wizard action buttons."""
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    
    action = None
    
    with col1:
        if current_step > 1:
            if st.button("← Previous", use_container_width=True, key="btn_prev"):
                action = "prev"
    
    with col2:
        if st.button("💾 Save Draft", use_container_width=True, key="btn_save"):
            action = "save"
    
    with col3:
        if st.button("Cancel", use_container_width=True, key="btn_cancel"):
            action = "cancel"
    
    with col4:
        if current_step < total_steps:
            if st.button("Next →", use_container_width=True, type="primary", key="btn_next"):
                action = "next"
        elif show_launch:
            if st.button("🚀 Launch Mission", use_container_width=True, type="primary", key="btn_launch"):
                action = "launch"
    
    return action
