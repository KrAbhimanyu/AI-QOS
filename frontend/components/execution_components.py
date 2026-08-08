"""Execution Center components for AI-QOS."""
import streamlit as st
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import time

from frontend.mock.missions import (
    MOCK_AGENTS,
    MOCK_LOGS,
    MOCK_NETWORK,
    MOCK_EXECUTION_STEPS,
)


# ============================================================================
# Session State Management
# ============================================================================

def init_execution_state() -> None:
    """Initialize execution session state."""
    defaults = {
        "exec_is_running": True,
        "exec_paused": False,
        "exec_current_test": "test_login_flow",
        "exec_current_step": 3,
        "exec_progress": 67,
        "exec_passed": 24,
        "exec_failed": 2,
        "exec_skipped": 3,
        "exec_elapsed": 125,
        "exec_confidence": 92,
        "exec_start_time": datetime.now() - timedelta(seconds=125),
        "exec_current_url": "https://demo.app/dashboard",
        "exec_browser_screenshot": "dashboard",
        "exec_logs": [],
        "exec_network_requests": [],
        "exec_agents": [],
        "exec_notifications": [],
        "exec_timeline": [],
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_exec_data(key: str, default: Any = None) -> Any:
    """Get execution data from session state."""
    return st.session_state.get(key, default)


def set_exec_data(key: str, value: Any) -> None:
    """Set execution data in session state."""
    st.session_state[key] = value


# ============================================================================
# Mock Data (imported from frontend.mock.missions)
# ============================================================================

# MOCK_AGENTS, MOCK_LOGS, MOCK_NETWORK, MOCK_EXECUTION_STEPS 
# are imported from frontend.mock.missions


# ============================================================================
# Execution Components
# ============================================================================

def execution_header(
    mission_name: str,
    status: str,
    browser: str,
    environment: str,
    elapsed: str,
    progress: int,
) -> None:
    """Display execution header with mission info and actions."""
    status_colors = {
        "Running": "#10B981",
        "Paused": "#F59E0B",
        "Stopped": "#EF4444",
        "Completed": "#6366F1",
    }
    status_color = status_colors.get(status, "#64748B")
    
    st.markdown(f"""<div style=" background: linear-gradient(135deg, rgba(30, 30, 63, 0.95) 0%, rgba(99, 102, 241, 0.15) 100%); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem; "> <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;"> <div> <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;"> <span style="color: #64748B; font-size: 0.8rem;">🏠 Dashboard</span> <span style="color: #64748B;">›</span> <span style="color: #64748B; font-size: 0.8rem;">Executions</span> <span style="color: #64748B;">›</span> <span style="color: #F1F5F9; font-size: 0.8rem;">{mission_name}</span> </div> <div style="display: flex; align-items: center; gap: 1rem;"> <h1 style="margin: 0; font-size: 1.5rem; color: #F1F5F9;">🚀 Live Execution Center</h1> <span style=" display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.35rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; background: {status_color}20; color: {status_color}; "> <span style="width: 8px; height: 8px; border-radius: 50%; background: {status_color};"></span> {status} </span> </div> </div> <div style="display: flex; gap: 1rem; align-items: center;"> <div style="text-align: center; padding: 0.5rem 1rem; background: rgba(30, 30, 63, 0.8); border-radius: 8px;"> <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Browser</p> <p style="color: #22D3EE; margin: 0; font-size: 0.9rem; font-weight: 500;">{browser}</p> </div> <div style="text-align: center; padding: 0.5rem 1rem; background: rgba(30, 30, 63, 0.8); border-radius: 8px;"> <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Environment</p> <p style="color: #F59E0B; margin: 0; font-size: 0.9rem; font-weight: 500;">{environment}</p> </div> <div style="text-align: center; padding: 0.5rem 1rem; background: rgba(30, 30, 63, 0.8); border-radius: 8px;"> <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Elapsed</p> <p style="color: #6366F1; margin: 0; font-size: 0.9rem; font-weight: 500;">{elapsed}</p> </div> <div style="text-align: center; padding: 0.5rem 1rem; background: rgba(30, 30, 63, 0.8); border-radius: 8px;"> <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Progress</p> <p style="color: #10B981; margin: 0; font-size: 0.9rem; font-weight: 500;">{progress}%</p> </div> </div> </div> </div>""", unsafe_allow_html=True)


def browser_viewer(
    current_url: str,
    highlighted_element: str = "Login Button",
    element_locator: str = "#login-btn",
    element_role: str = "button",
    element_text: str = "Sign In",
    element_confidence: int = 98,
    action: str = "clicking",
    animation: str = "pulse",
) -> None:
    """Display animated browser mockup."""
    animation_style = {
        "pulse": "animation: pulse 2s infinite;",
        "click": "animation: click 0.3s ease;",
        "type": "animation: typing 0.5s steps(10);",
        "scroll": "animation: scroll 1s ease;",
    }.get(animation, "")
    
    st.markdown(f"""<div style=" background: #1a1a2e; border: 1px solid #334155; border-radius: 12px; overflow: hidden; "> <!-- Browser Chrome --> <div style="background: #2d2d44; padding: 0.75rem 1rem; display: flex; align-items: center; gap: 1rem;"> <div style="display: flex; gap: 0.5rem;"> <div style="width: 12px; height: 12px; border-radius: 50%; background: #EF4444;"></div> <div style="width: 12px; height: 12px; border-radius: 50%; background: #F59E0B;"></div> <div style="width: 12px; height: 12px; border-radius: 50%; background: #10B981;"></div> </div> <div style="flex: 1; background: #1a1a2e; border-radius: 6px; padding: 0.5rem 1rem; display: flex; align-items: center; gap: 0.5rem;"> <span style="color: #64748B;">🔒</span> <span style="color: #94A3B8; font-size: 0.85rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{current_url}</span> </div> <div style="display: flex; gap: 0.5rem;"> <span style="color: #64748B; font-size: 1.25rem;">⟲</span> <span style="color: #64748B; font-size: 1.25rem;">↗</span> <span style="color: #64748B; font-size: 1.25rem;">⋮</span> </div> </div> <!-- Page Content --> <div style="padding: 1.5rem; background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1a 100%); min-height: 350px; position: relative;"> <!-- Simulated Dashboard --> <div style="background: #1e1e3f; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;"> <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;"> <div style="display: flex; align-items: center; gap: 0.5rem;"> <span style="color: #F1F5F9; font-size: 1.25rem; font-weight: 600;">📊 Dashboard</span> </div> <div style="display: flex; gap: 0.5rem;"> <div style="background: rgba(99, 102, 241, 0.2); padding: 0.25rem 0.75rem; border-radius: 4px; color: #818CF8; font-size: 0.75rem;">Welcome, User</div> </div> </div> <!-- Metrics Cards --> <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1rem;"> <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 1rem; text-align: center;"> <p style="color: #10B981; margin: 0; font-size: 1.5rem; font-weight: 600;">247</p> <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Active Users</p> </div> <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 8px; padding: 1rem; text-align: center;"> <p style="color: #6366F1; margin: 0; font-size: 1.5rem; font-weight: 600;">1.2K</p> <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Revenue</p> </div> <div style="background: rgba(34, 211, 238, 0.1); border: 1px solid rgba(34, 211, 238, 0.3); border-radius: 8px; padding: 1rem; text-align: center;"> <p style="color: #22D3EE; margin: 0; font-size: 1.5rem; font-weight: 600;">89%</p> <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Growth</p> </div> </div> </div> <!-- Highlighted Element --> <div style=" background: rgba(99, 102, 241, 0.15); border: 2px solid #6366F1; border-radius: 8px; padding: 1rem; text-align: center; position: relative; {animation_style} "> <div style=" position: absolute; top: -8px; left: 50%; transform: translateX(-50%); background: #6366F1; color: white; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.7rem; white-space: nowrap; "> {action.upper()} </div> <div style=" background: #6366F1; border-radius: 6px; padding: 0.75rem 2rem; display: inline-block; margin-top: 0.5rem; "> <span style="color: white; font-weight: 600;">{element_text}</span> </div> </div> <!-- Element Info Tooltip --> <div style=" position: absolute; bottom: 1rem; left: 1rem; background: rgba(30, 30, 63, 0.95); border: 1px solid #6366F1; border-radius: 8px; padding: 0.75rem; font-size: 0.75rem; max-width: 300px; "> <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;"> <span style="color: #64748B;">Element:</span> <span style="color: #F1F5F9;">{highlighted_element}</span> </div> <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;"> <span style="color: #64748B;">Locator:</span> <span style="color: #22D3EE; font-family: monospace;">{element_locator}</span> </div> <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;"> <span style="color: #64748B;">Role:</span> <span style="color: #F1F5F9;">{element_role}</span> </div> <div style="display: flex; justify-content: space-between;"> <span style="color: #64748B;">Confidence:</span> <span style="color: #10B981; font-weight: 600;">{element_confidence}%</span> </div> </div> </div> </div> <style> @keyframes pulse {{ 0%, 100% {{ box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); }} 50% {{ box-shadow: 0 0 0 10px rgba(99, 102, 241, 0); }} }} @keyframes click {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(0.95); }} 100% {{ transform: scale(1); }} }} </style>""", unsafe_allow_html=True)


def ai_thinking_panel(
    current_thought: str,
    reasoning: str,
    decision: str,
    confidence: int,
    next_action: str,
    potential_risk: str = None,
    recommendation: str = None,
) -> None:
    """Display AI thinking panel."""
    conf_color = "#10B981" if confidence >= 80 else "#F59E0B" if confidence >= 60 else "#EF4444"
    
    st.markdown(f"""<div style=" background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(30, 30, 63, 0.95) 100%); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 16px; padding: 1.25rem; height: 100%; "> <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;"> <div style=" width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #6366F1, #8B5CF6); display: flex; align-items: center; justify-content: center; font-size: 1.25rem; animation: glow 2s infinite; ">🤖</div> <div> <h4 style="color: #F1F5F9; margin: 0; font-size: 1rem;">AI Thinking</h4> <p style="color: #64748B; margin: 0.25rem 0 0; font-size: 0.75rem;">Real-time analysis</p> </div> </div> <div style="margin-bottom: 1rem;"> <p style="color: #64748B; margin: 0 0 0.5rem; font-size: 0.75rem;">💭 Current Thought</p> <div style=" background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 8px; padding: 0.75rem; "> <p style="color: #F1F5F9; margin: 0; font-size: 0.85rem;">{current_thought}</p> </div> </div> <div style="margin-bottom: 1rem;"> <p style="color: #64748B; margin: 0 0 0.5rem; font-size: 0.75rem;">🧠 Reasoning</p> <p style="color: #94A3B8; margin: 0; font-size: 0.8rem;">{reasoning}</p> </div> <div style="margin-bottom: 1rem;"> <p style="color: #64748B; margin: 0 0 0.5rem; font-size: 0.75rem;">⚡ Decision</p> <p style="color: #22D3EE; margin: 0; font-size: 0.85rem; font-weight: 500;">{decision}</p> </div> <div style="margin-bottom: 1rem;"> <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;"> <p style="color: #64748B; margin: 0; font-size: 0.75rem;">Confidence</p> <span style="color: {conf_color}; font-weight: 600;">{confidence}%</span> </div> <div style="height: 6px; background: #334155; border-radius: 3px; overflow: hidden;"> <div style="width: {confidence}%; height: 100%; background: {conf_color}; border-radius: 3px;"></div> </div> </div> <div style=" background: rgba(34, 211, 238, 0.1); border: 1px solid rgba(34, 211, 238, 0.3); border-radius: 8px; padding: 0.75rem; margin-bottom: 1rem; "> <p style="color: #22D3EE; margin: 0 0 0.5rem; font-size: 0.75rem; font-weight: 500;">→ Next Action</p> <p style="color: #94A3B8; margin: 0; font-size: 0.8rem;">{next_action}</p> </div> """ + (f""" <div style=" background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 8px; padding: 0.75rem; margin-bottom: 1rem; "> <p style="color: #F59E0B; margin: 0 0 0.5rem; font-size: 0.75rem; font-weight: 500;">⚠️ Potential Risk</p> <p style="color: #94A3B8; margin: 0; font-size: 0.8rem;">{potential_risk}</p> </div> """ if potential_risk else "") + (f""" <div style=" background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 0.75rem; "> <p style="color: #10B981; margin: 0 0 0.5rem; font-size: 0.75rem; font-weight: 500;">💡 Recommendation</p> <p style="color: #94A3B8; margin: 0; font-size: 0.8rem;">{recommendation}</p> </div> """ if recommendation else "") + """ </div> <style> @keyframes glow { 0%, 100% { box-shadow: 0 0 10px rgba(99, 102, 241, 0.5); } 50% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.8); } } </style>""", unsafe_allow_html=True)


def agent_status_card(
    name: str,
    icon: str,
    status: str,
    health: int,
    cpu: int,
    memory: int,
    task: str,
    progress: int,
) -> None:
    """Display agent status card."""
    status_colors = {"running": "#10B981", "idle": "#64748B", "error": "#EF4444"}
    status_color = status_colors.get(status, "#64748B")
    health_color = "#10B981" if health >= 80 else "#F59E0B" if health >= 50 else "#EF4444"
    
    st.markdown(f"""<div style=" background: rgba(30, 30, 63, 0.8); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem; transition: all 0.3s ease; "> <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;"> <div style=" width: 36px; height: 36px; border-radius: 8px; background: linear-gradient(135deg, #6366F1, #8B5CF6); display: flex; align-items: center; justify-content: center; font-size: 1.25rem; ">{icon}</div> <div style="flex: 1;"> <div style="display: flex; align-items: center; gap: 0.5rem;"> <span style="color: #F1F5F9; font-weight: 500;">{name}</span> <span style=" width: 8px; height: 8px; border-radius: 50%; background: {status_color}; "></span> </div> <p style="color: #64748B; margin: 0.25rem 0 0; font-size: 0.75rem;">{task}</p> </div> </div> <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; margin-bottom: 0.75rem;"> <div style="text-align: center;"> <p style="color: #64748B; margin: 0; font-size: 0.65rem;">Health</p> <p style="color: {health_color}; margin: 0; font-size: 0.85rem; font-weight: 600;">{health}%</p> </div> <div style="text-align: center;"> <p style="color: #64748B; margin: 0; font-size: 0.65rem;">CPU</p> <p style="color: #F59E0B; margin: 0; font-size: 0.85rem; font-weight: 600;">{cpu}%</p> </div> <div style="text-align: center;"> <p style="color: #64748B; margin: 0; font-size: 0.65rem;">Memory</p> <p style="color: #22D3EE; margin: 0; font-size: 0.85rem; font-weight: 600;">{memory}%</p> </div> </div> <div> <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;"> <span style="color: #64748B; font-size: 0.7rem;">Progress</span> <span style="color: #6366F1; font-size: 0.7rem;">{progress}%</span> </div> <div style="height: 4px; background: #334155; border-radius: 2px; overflow: hidden;"> <div style="width: {progress}%; height: 100%; background: linear-gradient(90deg, #6366F1, #8B5CF6); border-radius: 2px;"></div> </div> </div> </div>""", unsafe_allow_html=True)


def execution_timeline(steps: List[Dict]) -> None:
    """Display animated execution timeline."""
    st.markdown("""<div style=" background: rgba(30, 30, 63, 0.8); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 16px; padding: 1.5rem; "> <h4 style="color: #F1F5F9; margin: 0 0 1.5rem; font-size: 1rem;">📅 Execution Timeline</h4> </div>""", unsafe_allow_html=True)
    
    # Display timeline steps
    for i, step in enumerate(steps):
        is_last = i == len(steps) - 1
        is_active = step["status"] == "active"
        
        status_colors = {"completed": "#10B981", "active": "#6366F1", "pending": "#64748B"}
        color = status_colors.get(step["status"], "#64748B")
        icon = "✓" if step["status"] == "completed" else "●" if step["status"] == "active" else "○"
        
        st.markdown(f"""<div style="display: flex; gap: 1rem; margin-bottom: {0 if is_last else 1}rem;"> <div style="display: flex; flex-direction: column; align-items: center;"> <div style=" width: 28px; height: 28px; border-radius: 50%; background: {color}; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.8rem; flex-shrink: 0; {'animation: pulse 2s infinite;' if is_active else ''} ">{icon}</div> {'' if is_last else f'<div style="width: 2px; flex: 1; min-height: 30px; background: {color}; margin-top: 0.5rem;"></div>'} </div> <div style="flex: 1; padding-bottom: {0 if is_last else 0.75}rem;"> <p style="color: {'#F1F5F9' if step['status'] != 'pending' else '#64748B'}; margin: 0 0 0.25rem; font-weight: 500; font-size: 0.85rem;">{step['name']}</p> <p style="color: #64748B; margin: 0; font-size: 0.7rem;">{step['time']} {f"• {step['duration']}" if step['duration'] != '-' else ''}</p> </div> </div>""", unsafe_allow_html=True)
    
    st.markdown("<style>@keyframes pulse { 0%, 100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); } 50% { box-shadow: 0 0 0 8px rgba(99, 102, 241, 0); } }</style>", unsafe_allow_html=True)


def console_viewer(logs: List[Dict]) -> None:
    """Display log console."""
    st.markdown("""<div style=" background: #0a0a0f; border: 1px solid #334155; border-radius: 12px; overflow: hidden; font-family: 'Monaco', 'Menlo', monospace; "> <div style="background: #1a1a2e; padding: 0.75rem 1rem; display: flex; justify-content: space-between; align-items: center;"> <span style="color: #F1F5F9; font-size: 0.85rem;">Terminal</span> <div style="display: flex; gap: 0.5rem;"> <span style="color: #64748B; font-size: 0.75rem;">Auto-scroll</span> <div style="width: 32px; height: 16px; background: #10B981; border-radius: 8px; position: relative;"> <div style="width: 12px; height: 12px; background: white; border-radius: 50%; position: absolute; right: 2px; top: 2px;"></div> </div> </div> </div> <div style="padding: 1rem; max-height: 250px; overflow-y: auto;">""", unsafe_allow_html=True)
    
    for log in logs:
        time_str = log["time"].strftime("%H:%M:%S")
        status_colors = {
            "info": "#64748B",
            "success": "#10B981",
            "error": "#EF4444",
            "warning": "#F59E0B",
        }
        color = status_colors.get(log["status"], "#64748B")
        
        st.markdown(f"""<div style="margin-bottom: 0.5rem; font-size: 0.8rem;"> <span style="color: #64748B;">[{time_str}]</span> <span style="color: #6366F1; margin-left: 0.5rem;">[{log['agent']}]</span> <span style="color: {color}; margin-left: 0.5rem;">{log['message']}</span> </div>""", unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)


def network_viewer(requests: List[Dict]) -> None:
    """Display network request table."""
    st.markdown("""<div style=" background: rgba(30, 30, 63, 0.8); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 12px; padding: 1rem; "> <h4 style="color: #F1F5F9; margin: 0 0 1rem; font-size: 0.95rem;">🌐 Network Requests</h4>""", unsafe_allow_html=True)
    
    for req in requests:
        method_colors = {
            "GET": "#10B981",
            "POST": "#6366F1",
            "PUT": "#F59E0B",
            "DELETE": "#EF4444",
        }
        method_color = method_colors.get(req["method"], "#64748B")
        status_color = "#10B981" if req["status"] == 200 else "#F59E0B"
        
        st.markdown(f"""<div style=" display: flex; align-items: center; gap: 1rem; padding: 0.5rem 0; border-bottom: 1px solid rgba(51, 65, 85, 0.5); "> <span style=" background: {method_color}20; color: {method_color}; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.7rem; font-weight: 600; ">{req['method']}</span> <span style="color: #94A3B8; font-size: 0.8rem; flex: 1; font-family: monospace;">{req['url']}</span> <span style="color: {status_color}; font-size: 0.8rem;">{req['status']}</span> <span style="color: #64748B; font-size: 0.75rem;">{req['duration']}ms</span> <span style="color: #64748B; font-size: 0.75rem;">{req['size']}</span> </div>""", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def execution_stats(passed: int, failed: int, skipped: int, running: int, coverage: int, success_rate: float) -> None:
    """Display execution statistics."""
    st.markdown(f"""<div style=" background: linear-gradient(135deg, rgba(30, 30, 63, 0.95) 0%, rgba(99, 102, 241, 0.1) 100%); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 16px; padding: 1.5rem; "> <h4 style="color: #F1F5F9; margin: 0 0 1.25rem; font-size: 1rem;">📊 Execution Statistics</h4> <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.25rem;"> <div style="text-align: center; padding: 1rem; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px;"> <p style="color: #10B981; margin: 0; font-size: 2rem; font-weight: 700;">{passed}</p> <p style="color: #64748B; margin: 0.25rem 0 0; font-size: 0.75rem;">Passed</p> </div> <div style="text-align: center; padding: 1rem; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 12px;"> <p style="color: #EF4444; margin: 0; font-size: 2rem; font-weight: 700;">{failed}</p> <p style="color: #64748B; margin: 0.25rem 0 0; font-size: 0.75rem;">Failed</p> </div> <div style="text-align: center; padding: 1rem; background: rgba(100, 116, 139, 0.1); border: 1px solid rgba(100, 116, 139, 0.3); border-radius: 12px;"> <p style="color: #64748B; margin: 0; font-size: 2rem; font-weight: 700;">{skipped}</p> <p style="color: #64748B; margin: 0.25rem 0 0; font-size: 0.75rem;">Skipped</p> </div> </div> <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;"> <div style="padding: 0.75rem; background: rgba(51, 65, 85, 0.5); border-radius: 8px;"> <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Running</p> <p style="color: #6366F1; margin: 0.25rem 0 0; font-size: 1.25rem; font-weight: 600;">{running}</p> </div> <div style="padding: 0.75rem; background: rgba(51, 65, 85, 0.5); border-radius: 8px;"> <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Coverage</p> <p style="color: #10B981; margin: 0.25rem 0 0; font-size: 1.25rem; font-weight: 600;">{coverage}%</p> </div> </div> <div style="margin-top: 1rem; padding: 1rem; background: rgba(51, 65, 85, 0.5); border-radius: 8px;"> <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;"> <span style="color: #64748B; font-size: 0.8rem;">Success Rate</span> <span style="color: #10B981; font-size: 1rem; font-weight: 600;">{success_rate}%</span> </div> <div style="height: 8px; background: #334155; border-radius: 4px; overflow: hidden;"> <div style="width: {success_rate}%; height: 100%; background: linear-gradient(90deg, #10B981, #22D3EE); border-radius: 4px;"></div> </div> </div> </div>""", unsafe_allow_html=True)


def mission_info_panel(
    mission_name: str,
    application: str,
    environment: str,
    mode: str,
    started: str,
    elapsed: str,
    remaining: str,
    progress: int,
    coverage: int,
    phase: str,
    health: int,
) -> None:
    """Display mission information panel."""
    health_color = "#10B981" if health >= 80 else "#F59E0B" if health >= 50 else "#EF4444"
    
    st.markdown(f"""<div style=" background: linear-gradient(135deg, rgba(30, 30, 63, 0.95) 0%, rgba(99, 102, 241, 0.1) 100%); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 16px; padding: 1.5rem; "> <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.25rem;"> <div style=" width: 40px; height: 40px; border-radius: 10px; background: linear-gradient(135deg, #6366F1, #8B5CF6); display: flex; align-items: center; justify-content: center; font-size: 1.25rem; ">🎯</div> <div> <h4 style="color: #F1F5F9; margin: 0; font-size: 1rem;">Mission Info</h4> <p style="color: #64748B; margin: 0.25rem 0 0; font-size: 0.75rem;">{mission_name}</p> </div> </div> <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-bottom: 1rem;"> <div style="padding: 0.5rem; background: rgba(51, 65, 85, 0.5); border-radius: 6px;"> <p style="color: #64748B; margin: 0; font-size: 0.65rem;">Application</p> <p style="color: #F1F5F9; margin: 0.25rem 0 0; font-size: 0.8rem;">{application}</p> </div> <div style="padding: 0.5rem; background: rgba(51, 65, 85, 0.5); border-radius: 6px;"> <p style="color: #64748B; margin: 0; font-size: 0.65rem;">Environment</p> <p style="color: #F59E0B; margin: 0.25rem 0 0; font-size: 0.8rem;">{environment}</p> </div> <div style="padding: 0.5rem; background: rgba(51, 65, 85, 0.5); border-radius: 6px;"> <p style="color: #64748B; margin: 0; font-size: 0.65rem;">Mode</p> <p style="color: #22D3EE; margin: 0.25rem 0 0; font-size: 0.8rem;">{mode}</p> </div> <div style="padding: 0.5rem; background: rgba(51, 65, 85, 0.5); border-radius: 6px;"> <p style="color: #64748B; margin: 0; font-size: 0.65rem;">Started</p> <p style="color: #F1F5F9; margin: 0.25rem 0 0; font-size: 0.8rem;">{started}</p> </div> </div> <div style="margin-bottom: 1rem;"> <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;"> <span style="color: #64748B; font-size: 0.75rem;">Progress</span> <span style="color: #6366F1; font-size: 0.75rem; font-weight: 600;">{progress}%</span> </div> <div style="height: 6px; background: #334155; border-radius: 3px; overflow: hidden;"> <div style="width: {progress}%; height: 100%; background: linear-gradient(90deg, #6366F1, #8B5CF6); border-radius: 3px;"></div> </div> </div> <div style="display: flex; justify-content: space-between; padding: 0.75rem; background: rgba(51, 65, 85, 0.5); border-radius: 8px; margin-bottom: 0.75rem;"> <div> <p style="color: #64748B; margin: 0; font-size: 0.65rem;">Elapsed</p> <p style="color: #22D3EE; margin: 0.25rem 0 0; font-size: 0.9rem; font-weight: 600;">{elapsed}</p> </div> <div> <p style="color: #64748B; margin: 0; font-size: 0.65rem;">Remaining</p> <p style="color: #F59E0B; margin: 0.25rem 0 0; font-size: 0.9rem; font-weight: 600;">{remaining}</p> </div> </div> <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem;"> <div style="padding: 0.5rem; background: rgba(51, 65, 85, 0.5); border-radius: 6px;"> <p style="color: #64748B; margin: 0; font-size: 0.65rem;">Coverage</p> <p style="color: #10B981; margin: 0.25rem 0 0; font-size: 0.85rem; font-weight: 600;">{coverage}%</p> </div> <div style="padding: 0.5rem; background: rgba(51, 65, 85, 0.5); border-radius: 6px;"> <p style="color: #64748B; margin: 0; font-size: 0.65rem;">Health</p> <p style="color: {health_color}; margin: 0.25rem 0 0; font-size: 0.85rem; font-weight: 600;">{health}%</p> </div> </div> <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 8px;"> <p style="color: #64748B; margin: 0; font-size: 0.65rem;">Current Phase</p> <p style="color: #F1F5F9; margin: 0.25rem 0 0; font-size: 0.85rem;">{phase}</p> </div> </div>""", unsafe_allow_html=True)


def execution_details_card(
    test_name: str,
    expected: str,
    actual: str,
    status: str,
    exec_time: str,
    retries: int,
    step: str,
    confidence: int,
) -> None:
    """Display current execution details card."""
    status_colors = {"passed": "#10B981", "failed": "#EF4444", "running": "#6366F1", "skipped": "#64748B"}
    status_color = status_colors.get(status.lower(), "#64748B")
    
    st.markdown(f"""<div style=" background: rgba(30, 30, 63, 0.8); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 12px; padding: 1.25rem; "> <h4 style="color: #F1F5F9; margin: 0 0 1rem; font-size: 0.95rem;">📝 Current Test</h4> <div style="margin-bottom: 1rem;"> <p style="color: #64748B; margin: 0 0 0.25rem; font-size: 0.7rem;">Test Name</p> <p style="color: #F1F5F9; margin: 0; font-size: 0.9rem; font-weight: 500;">{test_name}</p> </div> <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-bottom: 1rem;"> <div> <p style="color: #64748B; margin: 0 0 0.25rem; font-size: 0.7rem;">Expected</p> <p style="color: #10B981; margin: 0; font-size: 0.8rem;">{expected}</p> </div> <div> <p style="color: #64748B; margin: 0 0 0.25rem; font-size: 0.7rem;">Actual</p> <p style="color: #22D3EE; margin: 0; font-size: 0.8rem;">{actual}</p> </div> </div> <div style="display: flex; justify-content: space-between; padding: 0.75rem; background: rgba(51, 65, 85, 0.5); border-radius: 8px; margin-bottom: 0.75rem;"> <span style="color: #64748B; font-size: 0.75rem;">Status</span> <span style="color: {status_color}; font-weight: 600;">{status.upper()}</span> </div> <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem;"> <div style="text-align: center; padding: 0.5rem; background: rgba(51, 65, 85, 0.5); border-radius: 6px;"> <p style="color: #64748B; margin: 0; font-size: 0.65rem;">Time</p> <p style="color: #F1F5F9; margin: 0.25rem 0 0; font-size: 0.8rem;">{exec_time}</p> </div> <div style="text-align: center; padding: 0.5rem; background: rgba(51, 65, 85, 0.5); border-radius: 6px;"> <p style="color: #64748B; margin: 0; font-size: 0.65rem;">Retries</p> <p style="color: #F59E0B; margin: 0.25rem 0 0; font-size: 0.8rem;">{retries}</p> </div> <div style="text-align: center; padding: 0.5rem; background: rgba(51, 65, 85, 0.5); border-radius: 6px;"> <p style="color: #64748B; margin: 0; font-size: 0.65rem;">Step</p> <p style="color: #6366F1; margin: 0.25rem 0 0; font-size: 0.8rem;">{step}</p> </div> </div> <div style="margin-top: 1rem;"> <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;"> <span style="color: #64748B; font-size: 0.75rem;">Confidence</span> <span style="color: #10B981; font-weight: 600;">{confidence}%</span> </div> <div style="height: 6px; background: #334155; border-radius: 3px; overflow: hidden;"> <div style="width: {confidence}%; height: 100%; background: #10B981; border-radius: 3px;"></div> </div> </div> </div>""", unsafe_allow_html=True)


def top_metrics_bar() -> None:
    """Display top metrics bar."""
    metrics = [
        ("⏱️", "Running", "2:05", "#6366F1"),
        ("💻", "CPU", "45%", "#F59E0B"),
        ("💾", "Memory", "62%", "#22D3EE"),
        ("🤖", "Agents", "5", "#10B981"),
        ("🌐", "Browsers", "2", "#8B5CF6"),
        ("🔗", "API Calls", "127", "#6366F1"),
        ("📷", "Screenshots", "24", "#22D3EE"),
        ("🎥", "Videos", "2", "#F472B6"),
        ("✅", "Assertions", "156", "#10B981"),
    ]
    
    st.markdown("""<div style=" display: flex; gap: 1rem; overflow-x: auto; padding: 0.5rem 0; ">""", unsafe_allow_html=True)
    
    for icon, label, value, color in metrics:
        st.markdown(f"""<div style=" display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; background: rgba(30, 30, 63, 0.8); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 8px; white-space: nowrap; "> <span style="font-size: 1rem;">{icon}</span> <div> <p style="color: #64748B; margin: 0; font-size: 0.65rem;">{label}</p> <p style="color: {color}; margin: 0; font-size: 0.9rem; font-weight: 600;">{value}</p> </div> </div>""", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def notification_toast(message: str, type: str = "info", icon: str = "ℹ️") -> None:
    """Display notification toast."""
    colors = {
        "success": ("#10B981", "rgba(16, 185, 129, 0.2)"),
        "info": ("#6366F1", "rgba(99, 102, 241, 0.2)"),
        "warning": ("#F59E0B", "rgba(245, 158, 11, 0.2)"),
        "error": ("#EF4444", "rgba(239, 68, 68, 0.2)"),
    }
    color, bg = colors.get(type, colors["info"])
    
    st.markdown(f"""<div style=" background: {bg}; border: 1px solid {color}; border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.75rem; animation: slideIn 0.3s ease; "> <span>{icon}</span> <span style="color: #F1F5F9; font-size: 0.85rem;">{message}</span> </div>""", unsafe_allow_html=True)
