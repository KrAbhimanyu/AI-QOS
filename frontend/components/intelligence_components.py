"""Intelligence Center components for AI-QOS."""
import streamlit as st
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Callable
import time

from frontend.mock.application import (
    MOCK_DISCOVERED_PAGES,
    MOCK_TECH_STACK,
    MOCK_AI_THOUGHTS,
)


# ============================================================================
# Session State Management
# ============================================================================

def init_intelligence_state() -> None:
    """Initialize intelligence center session state."""
    defaults = {
        "intel_current_phase": 0,
        "intel_phase_progress": {},
        "intel_discovery_complete": False,
        "intel_paused": False,
        "intel_start_time": datetime.now(),
        "intel_discovered_pages": [],
        "intel_technology_stack": {},
        "intel_stats": {
            "total_pages": 0,
            "forms": 0,
            "buttons": 0,
            "tables": 0,
            "dropdowns": 0,
            "dialogs": 0,
            "api_endpoints": 0,
        },
        "intel_timeline": [],
        "intel_notifications": [],
        "intel_confidence": 0,
        "intel_current_thought": "",
        "intel_activity": "",
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_intel_data(key: str, default: Any = None) -> Any:
    """Get intelligence data from session state."""
    return st.session_state.get(key, default)


def set_intel_data(key: str, value: Any) -> None:
    """Set intelligence data in session state."""
    st.session_state[key] = value


# ============================================================================
# Discovery Phases
# ============================================================================

DISCOVERY_PHASES = [
    {"id": "discover", "name": "Discovering Website", "icon": "🌐", "duration": 3},
    {"id": "tech_stack", "name": "Detecting Technology Stack", "icon": "🔍", "duration": 5},
    {"id": "navigation", "name": "Scanning Navigation", "icon": "🧭", "duration": 4},
    {"id": "dom_study", "name": "Studying DOM Structure", "icon": "📐", "duration": 6},
    {"id": "forms", "name": "Finding Forms", "icon": "📝", "duration": 4},
    {"id": "buttons", "name": "Finding Buttons", "icon": "🔘", "duration": 3},
    {"id": "tables", "name": "Finding Tables", "icon": "📊", "duration": 4},
    {"id": "menus", "name": "Finding Menus", "icon": "📋", "duration": 3},
    {"id": "modals", "name": "Finding Modals", "icon": "🪟", "duration": 4},
    {"id": "apis", "name": "Discovering APIs", "icon": "🔗", "duration": 6},
    {"id": "auth", "name": "Reading Authentication Flow", "icon": "🔐", "duration": 5},
    {"id": "workflows", "name": "Learning Business Workflows", "icon": "🔄", "duration": 6},
    {"id": "blueprint", "name": "Generating Application Blueprint", "icon": "🗺️", "duration": 8},
    {"id": "automation", "name": "Preparing Automation Plan", "icon": "🤖", "duration": 5},
]


# ============================================================================
# Mock Data (imported from frontend.mock.application)
# ============================================================================

# MOCK_DISCOVERED_PAGES, MOCK_TECH_STACK, MOCK_AI_THOUGHTS 
# are imported from frontend.mock.application


# ============================================================================
# Progress Components
# ============================================================================

def discovery_progress_bar(
    phase_name: str,
    progress: int,
    icon: str = "⏳",
    color: str = "#6366F1",
) -> None:
    """Display animated discovery progress bar."""
    st.markdown(f"""<div style=" background: rgba(30, 30, 63, 0.8); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem; transition: all 0.3s ease; "> <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.75rem;"> <span style="font-size: 1.5rem;">{icon}</span> <div style="flex: 1;"> <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;"> <span style="color: #F1F5F9; font-weight: 500;">{phase_name}</span> <span style="color: {color}; font-weight: 600;">{progress}%</span> </div> <div style="height: 6px; background: #334155; border-radius: 3px; overflow: hidden;"> <div style=" width: {progress}%; height: 100%; background: linear-gradient(90deg, {color}, {color}aa); border-radius: 3px; transition: width 0.5s ease; "></div> </div> </div> </div> </div>""", unsafe_allow_html=True)


def phase_completed_badge(phase_name: str, icon: str = "✅") -> None:
    """Display completed phase badge."""
    st.markdown(f"""<div style=" display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem 1rem; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; margin-bottom: 0.5rem; "> <span style="color: #10B981; font-size: 1.25rem;">{icon}</span> <span style="color: #94A3B8; font-size: 0.875rem;">{phase_name}</span> <span style="color: #10B981; margin-left: auto; font-size: 0.75rem;">Completed</span> </div>""", unsafe_allow_html=True)


def glass_loading_panel(message: str = "Loading...") -> None:
    """Display glass morphism loading panel."""
    st.markdown(f"""<div style=" background: rgba(30, 30, 63, 0.9); backdrop-filter: blur(10px); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 16px; padding: 2rem; text-align: center; "> <div style=" width: 60px; height: 60px; border: 3px solid rgba(99, 102, 241, 0.2); border-top-color: #6366F1; border-radius: 50%; margin: 0 auto 1rem; animation: spin 1s linear infinite; "></div> <p style="color: #F1F5F9; margin: 0;">{message}</p> <style> @keyframes spin {{ to {{ transform: rotate(360deg); }} }} </style> </div>""", unsafe_allow_html=True)


def skeleton_card(lines: int = 3) -> None:
    """Display skeleton loading card."""
    skeletons = ""
    for i in range(lines):
        width = 100 - (i * 15)
        skeletons += f"""
        <div style="
            height: 12px;
            background: linear-gradient(90deg, #334155 25%, #3D4F6A 50%, #334155 75%);
            background-size: 200% 100%;
            border-radius: 6px;
            margin-bottom: 0.75rem;
            width: {width}%;
            animation: shimmer 1.5s infinite;
        "></div>
        """
    
    st.markdown(f"""<div style=" background: rgba(30, 30, 63, 0.5); border: 1px solid #334155; border-radius: 12px; padding: 1.5rem; "> {skeletons} <style> @keyframes shimmer {{ 0% {{ background-position: 200% 0; }} 100% {{ background-position: -200% 0; }} }} </style> </div>""", unsafe_allow_html=True)


# ============================================================================
# Card Components
# ============================================================================

def mission_info_card(
    mission_name: str,
    project: str,
    environment: str,
    priority: str,
    mode: str,
    started_at: datetime,
    elapsed: str,
    remaining: str,
    progress: int,
    phase: str,
    status: str,
) -> None:
    """Display mission information card."""
    priority_colors = {"High": "#EF4444", "Medium": "#F59E0B", "Low": "#10B981"}
    status_colors = {"Running": "#6366F1", "Paused": "#F59E0B", "Completed": "#10B981", "Failed": "#EF4444"}
    prio_color = priority_colors.get(priority, "#64748B")
    stat_color = status_colors.get(status, "#64748B")
    
    st.markdown(f"""<div style=" background: linear-gradient(135deg, rgba(30, 30, 63, 0.95) 0%, rgba(99, 102, 241, 0.15) 100%); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 16px; padding: 1.5rem; "> <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.25rem;"> <div style=" width: 48px; height: 48px; border-radius: 12px; background: linear-gradient(135deg, #6366F1, #8B5CF6); display: flex; align-items: center; justify-content: center; font-size: 1.5rem; ">🎯</div> <div> <h3 style="color: #F1F5F9; margin: 0; font-size: 1.1rem;">{mission_name}</h3> <p style="color: #94A3B8; margin: 0.25rem 0 0; font-size: 0.8rem;">{project}</p> </div> </div> <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-bottom: 1rem;"> <div style="padding: 0.75rem; background: rgba(51, 65, 85, 0.5); border-radius: 8px;"> <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Environment</p> <p style="color: #F1F5F9; margin: 0.25rem 0 0; font-size: 0.85rem; font-weight: 500;">{environment}</p> </div> <div style="padding: 0.75rem; background: rgba(51, 65, 85, 0.5); border-radius: 8px;"> <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Priority</p> <p style="color: {prio_color}; margin: 0.25rem 0 0; font-size: 0.85rem; font-weight: 500;">{priority}</p> </div> <div style="padding: 0.75rem; background: rgba(51, 65, 85, 0.5); border-radius: 8px;"> <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Execution Mode</p> <p style="color: #F1F5F9; margin: 0.25rem 0 0; font-size: 0.85rem; font-weight: 500;">{mode}</p> </div> <div style="padding: 0.75rem; background: rgba(51, 65, 85, 0.5); border-radius: 8px;"> <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Started</p> <p style="color: #F1F5F9; margin: 0.25rem 0 0; font-size: 0.85rem; font-weight: 500;">{started_at.strftime('%H:%M:%S')}</p> </div> </div> <div style="margin-bottom: 1rem;"> <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;"> <span style="color: #94A3B8; font-size: 0.8rem;">Progress</span> <span style="color: #6366F1; font-size: 0.8rem; font-weight: 600;">{progress}%</span> </div> <div style="height: 8px; background: #334155; border-radius: 4px; overflow: hidden;"> <div style=" width: {progress}%; height: 100%; background: linear-gradient(90deg, #6366F1, #8B5CF6); border-radius: 4px; transition: width 0.5s ease; "></div> </div> </div> <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 1rem; border-top: 1px solid #334155;"> <div> <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Current Phase</p> <p style="color: #F1F5F9; margin: 0.25rem 0 0; font-size: 0.85rem;">{phase}</p> </div> <span style=" display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.35rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; background: {stat_color}20; color: {stat_color}; "> <span style="width: 8px; height: 8px; border-radius: 50%; background: {stat_color};"></span> {status} </span> </div> <div style="display: flex; justify-content: space-between; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #334155;"> <div> <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Elapsed</p> <p style="color: #22D3EE; margin: 0.25rem 0 0; font-size: 1rem; font-weight: 600;">{elapsed}</p> </div> <div style="text-align: right;"> <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Remaining</p> <p style="color: #F59E0B; margin: 0.25rem 0 0; font-size: 1rem; font-weight: 600;">{remaining}</p> </div> </div> </div>""", unsafe_allow_html=True)


def tech_card(title: str, value: str, version: str = "", confidence: int = 0, icon: str = "🔧") -> None:
    """Display technology stack card."""
    conf_color = "#10B981" if confidence >= 80 else "#F59E0B" if confidence >= 60 else "#EF4444"
    
    st.markdown(f"""<div style=" background: rgba(30, 30, 63, 0.8); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem; "> <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;"> <span style="font-size: 1.5rem;">{icon}</span> <div style="flex: 1;"> <p style="color: #64748B; margin: 0; font-size: 0.7rem;">{title}</p> <p style="color: #F1F5F9; margin: 0; font-size: 0.95rem; font-weight: 500;">{value}</p> </div> </div> <div style="display: flex; justify-content: space-between; align-items: center;"> {f'<span style="color: #94A3B8; font-size: 0.75rem;">v{version}</span>' if version else '<span></span>'} <span style=" display: inline-flex; align-items: center; gap: 0.25rem; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.7rem; background: {conf_color}20; color: {conf_color}; "> {confidence}% confident </span> </div> </div>""", unsafe_allow_html=True)


def ai_thinking_panel(
    current_thought: str,
    current_activity: str,
    confidence: int,
    findings: List[str],
    warnings: List[str],
) -> None:
    """Display AI thinking panel."""
    conf_color = "#10B981" if confidence >= 80 else "#F59E0B" if confidence >= 60 else "#EF4444"
    
    st.markdown(f"""<div style=" background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(30, 30, 63, 0.95) 100%); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 16px; padding: 1.25rem; height: 100%; "> <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;"> <div style=" width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #6366F1, #8B5CF6); display: flex; align-items: center; justify-content: center; font-size: 1.25rem; ">🤖</div> <h4 style="color: #F1F5F9; margin: 0;">AI Assistant</h4> </div> <div style="margin-bottom: 1rem;"> <p style="color: #64748B; margin: 0 0 0.5rem; font-size: 0.75rem;">Current Thought</p> <div style=" background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 8px; padding: 0.75rem; "> <p style="color: #F1F5F9; margin: 0; font-size: 0.85rem;">{current_thought}</p> </div> </div> <div style="margin-bottom: 1rem;"> <p style="color: #64748B; margin: 0 0 0.5rem; font-size: 0.75rem;">Current Activity</p> <p style="color: #22D3EE; margin: 0; font-size: 0.85rem;">{current_activity}</p> </div> <div style="margin-bottom: 1rem;"> <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;"> <p style="color: #64748B; margin: 0; font-size: 0.75rem;">Confidence Score</p> <span style="color: {conf_color}; font-weight: 600;">{confidence}%</span> </div> <div style="height: 6px; background: #334155; border-radius: 3px; overflow: hidden;"> <div style=" width: {confidence}%; height: 100%; background: {conf_color}; border-radius: 3px; "></div> </div> </div> <div style="margin-bottom: 1rem;"> <p style="color: #64748B; margin: 0 0 0.75rem; font-size: 0.75rem;">Interesting Findings</p> {''.join([f'<div style="padding: 0.5rem 0; border-bottom: 1px solid rgba(99, 102, 241, 0.1);"><span style="color: #10B981;">▸</span> <span style="color: #94A3B8; font-size: 0.8rem;">{finding}</span></div>' for finding in findings])} </div> {"".join([f''' <div style=" background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 8px; padding: 0.75rem; margin-top: 1rem; "> <p style="color: #F59E0B; margin: 0 0 0.5rem; font-size: 0.75rem; font-weight: 500;">⚠️ Warning</p> <p style="color: #94A3B8; margin: 0; font-size: 0.8rem;">{warning}</p> </div> ''' for warning in warnings])} </div>""", unsafe_allow_html=True)


def timeline_step(
    step_name: str,
    status: str,
    timestamp: str,
    duration: str = "",
    is_active: bool = False,
    is_last: bool = False,
) -> None:
    """Display timeline step."""
    status_colors = {
        "completed": "#10B981",
        "active": "#6366F1",
        "pending": "#64748B",
    }
    color = status_colors.get(status, "#64748B")
    icon = "✓" if status == "completed" else "●" if status == "active" else "○"
    
    st.markdown(f"""<div style="display: flex; gap: 1rem; margin-bottom: {0 if is_last else 1.5}rem;"> <div style="display: flex; flex-direction: column; align-items: center;"> <div style=" width: 32px; height: 32px; border-radius: 50%; background: {color}; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.9rem; flex-shrink: 0; ">{icon}</div> {'' if is_last else f'<div style="width: 2px; flex: 1; min-height: 40px; background: {color}; margin-top: 0.5rem;"></div>'} </div> <div style="flex: 1; padding-bottom: {0 if is_last else 1}rem;"> <p style="color: {'#F1F5F9' if status != 'pending' else '#64748B'}; margin: 0 0 0.25rem; font-weight: 500;">{step_name}</p> <p style="color: #64748B; margin: 0; font-size: 0.75rem;">{timestamp} {f'• {duration}' if duration else ''}</p> </div> </div>""", unsafe_allow_html=True)


def application_overview_card(
    website_name: str,
    technology: str,
    authentication: str,
    total_pages: int,
    forms: int,
    buttons: int,
    tables: int,
    dropdowns: int,
    dialogs: int,
    nav_menu: int,
    api_count: int,
) -> None:
    """Display application overview card."""
    st.markdown(f"""<div style=" background: linear-gradient(135deg, rgba(30, 30, 63, 0.95) 0%, rgba(99, 102, 241, 0.1) 100%); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem; "> <h3 style="color: #F1F5F9; margin: 0 0 1rem; font-size: 1.1rem;">Application Overview</h3> <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;"> <div style="padding: 1rem; background: rgba(51, 65, 85, 0.5); border-radius: 12px; text-align: center;"> <p style="color: #64748B; margin: 0 0 0.25rem; font-size: 0.7rem;">Website</p> <p style="color: #F1F5F9; margin: 0; font-size: 1rem; font-weight: 600;">{website_name}</p> </div> <div style="padding: 1rem; background: rgba(51, 65, 85, 0.5); border-radius: 12px; text-align: center;"> <p style="color: #64748B; margin: 0 0 0.25rem; font-size: 0.7rem;">Technology</p> <p style="color: #6366F1; margin: 0; font-size: 1rem; font-weight: 600;">{technology}</p> </div> </div> <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; background: rgba(51, 65, 85, 0.5); border-radius: 8px; margin-bottom: 1rem;"> <span style="color: #94A3B8;">🔐 Authentication</span> <span style="color: #10B981; font-weight: 500;">{authentication}</span> </div> <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem;"> {''.join([f''' <div style="text-align: center; padding: 0.75rem; background: rgba(51, 65, 85, 0.3); border-radius: 8px;"> <p style="color: #64748B; margin: 0 0 0.25rem; font-size: 0.65rem;">{label}</p> <p style="color: #F1F5F9; margin: 0; font-size: 1.25rem; font-weight: 600;">{value}</p> </div> ''' for label, value in [ ("Pages", total_pages), ("Forms", forms), ("Buttons", buttons), ("Tables", tables), ("Dropdowns", dropdowns), ("Dialogs", dialogs), ("Nav Menu", nav_menu), ("APIs", api_count), ("", ""), ] if label])} </div> </div>""", unsafe_allow_html=True)


def dom_summary_card(stats: Dict[str, int]) -> None:
    """Display DOM summary card."""
    st.markdown("""<div style=" background: rgba(30, 30, 63, 0.8); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 12px; padding: 1.25rem; "> <h4 style="color: #F1F5F9; margin: 0 0 1rem; font-size: 0.95rem;">DOM Summary</h4>""", unsafe_allow_html=True)
    
    for label, value in stats.items():
        st.markdown(f"""<div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(51, 65, 85, 0.5);"> <span style="color: #94A3B8; font-size: 0.85rem;">{label}</span> <span style="color: #F1F5F9; font-weight: 500;">{value}</span> </div>""", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def notification_badge(count: int) -> None:
    """Display notification badge."""
    if count > 0:
        st.markdown(f"""<span style=" position: absolute; top: -5px; right: -5px; width: 18px; height: 18px; border-radius: 50%; background: #EF4444; color: white; font-size: 0.65rem; display: flex; align-items: center; justify-content: center; font-weight: 600; ">{count}</span>""", unsafe_allow_html=True)


def confidence_indicator(value: int, size: str = "large") -> None:
    """Display confidence indicator."""
    conf_color = "#10B981" if value >= 80 else "#F59E0B" if value >= 60 else "#EF4444"
    size_styles = {
        "large": {"width": 80, "height": 80, "font_size": "1.5rem"},
        "medium": {"width": 60, "height": 60, "font_size": "1.25rem"},
        "small": {"width": 40, "height": 40, "font_size": "0.9rem"},
    }
    style = size_styles.get(size, size_styles["large"])
    
    st.markdown(f"""<div style=" width: {style['width']}px; height: {style['height']}px; border-radius: 50%; background: conic-gradient({conf_color} {value}%, rgba(51, 65, 85, 0.3) 0%); display: flex; align-items: center; justify-content: center; position: relative; "> <div style=" width: calc(100% - 8px); height: calc(100% - 8px); border-radius: 50%; background: #1E1E3F; display: flex; align-items: center; justify-content: center; "> <span style="color: {conf_color}; font-size: {style['font_size']}; font-weight: 700;">{value}%</span> </div> </div>""", unsafe_allow_html=True)


def notification_toast(message: str, type: str = "info", icon: str = "ℹ️") -> None:
    """Display notification toast."""
    colors = {
        "success": ("#10B981", "rgba(16, 185, 129, 0.2)"),
        "info": ("#6366F1", "rgba(99, 102, 241, 0.2)"),
        "warning": ("#F59E0B", "rgba(245, 158, 11, 0.2)"),
        "error": ("#EF4444", "rgba(239, 68, 68, 0.2)"),
    }
    color, bg = colors.get(type, colors["info"])
    
    st.markdown(f"""<div style=" background: {bg}; border: 1px solid {color}; border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.75rem; "> <span>{icon}</span> <span style="color: #F1F5F9; font-size: 0.85rem;">{message}</span> </div>""", unsafe_allow_html=True)
