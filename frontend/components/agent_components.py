"""Agent Control Tower components for AI-QOS."""
import streamlit as st
from datetime import datetime
from typing import Optional, List, Dict, Any

from frontend.mock.agents import MOCK_AGENTS, MOCK_EVENTS, MOCK_QUEUE, MOCK_MODELS


# ============================================================================
# Session State Management
# ============================================================================

def init_agent_state() -> None:
    """Initialize agent session state."""
    defaults = {
        "agent_selected": None,
        "agent_filters": {"status": "all", "category": "all"},
        "agent_search": "",
        "agent_events": [],
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_agent_data(key: str, default: Any = None) -> Any:
    """Get agent data from session state."""
    return st.session_state.get(key, default)


def set_agent_data(key: str, value: Any) -> None:
    """Set agent data in session state."""
    st.session_state[key] = value


# ============================================================================
# Mock Data (imported from frontend.mock.agents)
# ============================================================================

# Mock data is imported from frontend.mock.agents

# ============================================================================
# Agent Header
# ============================================================================

def agent_header(
    mission: str,
    environment: str,
    running_agents: int,
    total_agents: int,
    health: int,
    exec_time: str,
) -> None:
    """Display agent control tower header."""
    health_color = "#10B981" if health >= 80 else "#F59E0B" if health >= 50 else "#EF4444"
    
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, rgba(30, 30, 63, 0.95) 0%, rgba(99, 102, 241, 0.15) 100%);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        ">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                        <span style="color: #64748B; font-size: 0.8rem;">🏠 Dashboard</span>
                        <span style="color: #64748B;">›</span>
                        <span style="color: #64748B; font-size: 0.8rem;">Agents</span>
                        <span style="color: #64748B;">›</span>
                        <span style="color: #F1F5F9; font-size: 0.8rem;">{mission}</span>
                    </div>
                    <h1 style="margin: 0; font-size: 1.5rem; color: #F1F5F9;">🤖 Agent Control Tower</h1>
                </div>
                
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    <div style="text-align: center; padding: 0.5rem 1rem; background: rgba(30, 30, 63, 0.8); border-radius: 8px;">
                        <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Mission</p>
                        <p style="color: #F1F5F9; margin: 0; font-size: 0.85rem;">{mission}</p>
                    </div>
                    <div style="text-align: center; padding: 0.5rem 1rem; background: rgba(30, 30, 63, 0.8); border-radius: 8px;">
                        <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Environment</p>
                        <p style="color: #F59E0B; margin: 0; font-size: 0.85rem;">{environment}</p>
                    </div>
                    <div style="text-align: center; padding: 0.5rem 1rem; background: rgba(30, 30, 63, 0.8); border-radius: 8px;">
                        <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Running</p>
                        <p style="color: #10B981; margin: 0; font-size: 0.85rem;">{running_agents}/{total_agents}</p>
                    </div>
                    <div style="text-align: center; padding: 0.5rem 1rem; background: rgba(30, 30, 63, 0.8); border-radius: 8px;">
                        <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Health</p>
                        <p style="color: {health_color}; margin: 0; font-size: 0.85rem;">{health}%</p>
                    </div>
                    <div style="text-align: center; padding: 0.5rem 1rem; background: rgba(30, 30, 63, 0.8); border-radius: 8px;">
                        <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Time</p>
                        <p style="color: #6366F1; margin: 0; font-size: 0.85rem;">{exec_time}</p>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# Agent Card
# ============================================================================

def agent_card(agent: Dict) -> None:
    """Display an agent card with all fields."""
    status_colors = {
        "running": "#10B981",
        "idle": "#64748B",
        "paused": "#F59E0B",
        "failed": "#EF4444",
    }
    status_color = status_colors.get(agent["status"], "#64748B")
    health_color = "#10B981" if agent["health"] >= 80 else "#F59E0B" if agent["health"] >= 50 else "#EF4444"
    
    st.markdown(
        f"""
        <div style="
            background: rgba(30, 30, 63, 0.8);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 0.75rem;
            transition: all 0.3s;
            {'animation: pulse 2s infinite;' if agent['status'] == 'running' else ''}
            {'opacity: 0.7;' if agent['status'] == 'idle' else ''}
        ">
            <!-- Header -->
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;">
                <div style="
                    width: 44px;
                    height: 44px;
                    border-radius: 10px;
                    background: linear-gradient(135deg, {status_color}, {status_color}80);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.5rem;
                    {'animation: glow 2s infinite;' if agent['status'] == 'running' else ''}
                ">{agent['icon']}</div>
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="color: #F1F5F9; font-weight: 600; font-size: 0.9rem;">{agent['name']}</span>
                        <span style="
                            width: 8px;
                            height: 8px;
                            border-radius: 50%;
                            background: {status_color};
                        "></span>
                    </div>
                    <p style="color: #64748B; margin: 0.25rem 0 0; font-size: 0.75rem;">v{agent.get('version', '1.0.0')} • {agent.get('role', 'Agent')}</p>
                </div>
            </div>
            
            <!-- Current Task -->
            <div style="margin-bottom: 0.75rem; padding: 0.5rem; background: rgba(51, 65, 85, 0.5); border-radius: 6px;">
                <p style="color: #64748B; margin: 0 0 0.25rem; font-size: 0.65rem;">Current Task</p>
                <p style="color: #F1F5F9; margin: 0; font-size: 0.8rem;">{agent['task']}</p>
            </div>
            
            <!-- Current Prompt -->
            <div style="margin-bottom: 0.75rem;">
                <p style="color: #64748B; margin: 0 0 0.25rem; font-size: 0.65rem;">Current Prompt</p>
                <p style="color: #22D3EE; margin: 0; font-size: 0.75rem; font-style: italic;">"{agent.get('current_prompt', 'N/A')[:40]}..."</p>
            </div>
            
            <!-- Progress -->
            <div style="margin-bottom: 0.75rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                    <span style="color: #64748B; font-size: 0.7rem;">Progress</span>
                    <span style="color: #6366F1; font-size: 0.7rem; font-weight: 600;">{agent['progress']}%</span>
                </div>
                <div style="height: 4px; background: #334155; border-radius: 2px; overflow: hidden;">
                    <div style="width: {agent['progress']}%; height: 100%; background: linear-gradient(90deg, #6366F1, #8B5CF6); border-radius: 2px;"></div>
                </div>
            </div>
            
            <!-- Metrics Grid -->
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; margin-bottom: 0.75rem;">
                <div style="text-align: center; padding: 0.4rem; background: rgba(51, 65, 85, 0.5); border-radius: 6px;">
                    <p style="color: #64748B; margin: 0; font-size: 0.6rem;">CPU</p>
                    <p style="color: #F59E0B; margin: 0.25rem 0 0; font-size: 0.8rem; font-weight: 600;">{agent['cpu']}%</p>
                </div>
                <div style="text-align: center; padding: 0.4rem; background: rgba(51, 65, 85, 0.5); border-radius: 6px;">
                    <p style="color: #64748B; margin: 0; font-size: 0.6rem;">Memory</p>
                    <p style="color: #22D3EE; margin: 0.25rem 0 0; font-size: 0.8rem; font-weight: 600;">{agent['memory']}%</p>
                </div>
                <div style="text-align: center; padding: 0.4rem; background: rgba(51, 65, 85, 0.5); border-radius: 6px;">
                    <p style="color: #64748B; margin: 0; font-size: 0.6rem;">Health</p>
                    <p style="color: {health_color}; margin: 0.25rem 0 0; font-size: 0.8rem; font-weight: 600;">{agent['health']}%</p>
                </div>
                <div style="text-align: center; padding: 0.4rem; background: rgba(51, 65, 85, 0.5); border-radius: 6px;">
                    <p style="color: #64748B; margin: 0; font-size: 0.6rem;">Confidence</p>
                    <p style="color: #10B981; margin: 0.25rem 0 0; font-size: 0.8rem; font-weight: 600;">{agent['confidence']}%</p>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="display: flex; justify-content: space-between; padding-top: 0.5rem; border-top: 1px solid #334155;">
                <span style="color: #64748B; font-size: 0.65rem;">Model: {agent['model']}</span>
                <span style="color: #64748B; font-size: 0.65rem;">{agent['exec_time']}</span>
            </div>
        </div>
        <style>
            @keyframes pulse {{
                0%, 100% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }}
                50% {{ box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }}
            }}
            @keyframes glow {{
                0%, 100% {{ box-shadow: 0 0 10px rgba(16, 185, 129, 0.5); }}
                50% {{ box-shadow: 0 0 20px rgba(16, 185, 129, 0.8); }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# Agent Category Sidebar
# ============================================================================

def agent_categories() -> None:
    """Display agent category sidebar."""
    categories = [
        {"icon": "🧠", "name": "Intelligence", "count": 5, "color": "#6366F1"},
        {"icon": "🧪", "name": "Testing", "count": 6, "color": "#10B981"},
        {"icon": "📝", "name": "Documentation", "count": 1, "color": "#22D3EE"},
        {"icon": "🔐", "name": "Security", "count": 1, "color": "#EF4444"},
        {"icon": "⚡", "name": "Performance", "count": 1, "color": "#F59E0B"},
        {"icon": "🧠", "name": "Learning", "count": 1, "color": "#8B5CF6"},
        {"icon": "🚀", "name": "Support", "count": 1, "color": "#F472B6"},
    ]
    
    st.markdown("<h4 style='color: #F1F5F9; margin: 1rem 0 0.75rem;'>📂 Categories</h4>", unsafe_allow_html=True)
    
    for cat in categories:
        st.markdown(
            f"""
            <div style="
                display: flex;
                align-items: center;
                gap: 0.75rem;
                padding: 0.75rem;
                background: rgba(30, 30, 63, 0.5);
                border-radius: 8px;
                margin-bottom: 0.5rem;
                cursor: pointer;
                transition: all 0.2s;
            ">
                <span style="font-size: 1.25rem;">{cat['icon']}</span>
                <div style="flex: 1;">
                    <p style="color: #F1F5F9; margin: 0; font-size: 0.85rem;">{cat['name']}</p>
                </div>
                <span style="
                    background: {cat['color']}20;
                    color: {cat['color']};
                    padding: 0.2rem 0.5rem;
                    border-radius: 4px;
                    font-size: 0.75rem;
                    font-weight: 600;
                ">{cat['count']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================================
# Communication Graph
# ============================================================================

def communication_graph() -> None:
    """Display agent communication graph."""
    st.markdown(
        """
        <div style="
            background: rgba(30, 30, 63, 0.8);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        ">
            <h4 style="color: #F1F5F9; margin: 0 0 1rem; font-size: 1rem;">🔗 Agent Communication</h4>
        """,
        unsafe_allow_html=True,
    )
    
    # Animated nodes
    nodes = [
        {"name": "Requirement", "icon": "📋", "x": 50, "y": 10},
        {"name": "Application", "icon": "🔍", "x": 20, "y": 30},
        {"name": "DOM", "icon": "📐", "x": 50, "y": 30},
        {"name": "Locator", "icon": "🎯", "x": 80, "y": 30},
        {"name": "Frontend", "icon": "🖥️", "x": 35, "y": 55},
        {"name": "API", "icon": "🔗", "x": 65, "y": 55},
        {"name": "Docs", "icon": "📝", "x": 50, "y": 80},
    ]
    
    # Draw SVG-like connections
    connections = [
        ("Requirement", "Application"),
        ("Requirement", "DOM"),
        ("Requirement", "Locator"),
        ("Application", "Frontend"),
        ("DOM", "Frontend"),
        ("Locator", "Frontend"),
        ("Frontend", "API"),
        ("Frontend", "Docs"),
        ("API", "Docs"),
    ]
    
    # Create connection lines
    for conn in connections:
        st.markdown(
            f"""
            <div style="
                position: absolute;
                width: 2px;
                height: 40px;
                background: linear-gradient(180deg, #6366F1, #10B981);
                opacity: 0.5;
                animation: flow 2s infinite;
            "></div>
            """,
            unsafe_allow_html=True,
        )
    
    # Draw nodes
    cols = st.columns(7)
    icons = ["📋", "🔍", "📐", "🎯", "🖥️", "🔗", "📝"]
    names = ["Requirement", "Application", "DOM", "Locator", "Frontend", "API", "Docs"]
    
    for i, (col, icon, name) in enumerate(zip(cols, icons, names)):
        with col:
            st.markdown(
                f"""
                <div style="
                    text-align: center;
                    padding: 0.75rem;
                    background: rgba(99, 102, 241, 0.2);
                    border: 1px solid rgba(99, 102, 241, 0.3);
                    border-radius: 12px;
                    {'animation: pulse 2s infinite;' if i in [0, 4] else ''}
                ">
                    <span style="font-size: 1.5rem; display: block; margin-bottom: 0.5rem;">{icon}</span>
                    <span style="color: #F1F5F9; font-size: 0.7rem;">{name}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    
    st.markdown(
        """
        <style>
            @keyframes flow {
                0% { opacity: 0.2; }
                50% { opacity: 0.8; }
                100% { opacity: 0.2; }
            }
            @keyframes pulse {
                0%, 100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); }
                50% { box-shadow: 0 0 0 8px rgba(99, 102, 241, 0); }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# Agent Queue
# ============================================================================

def agent_queue() -> None:
    """Display agent queue status."""
    st.markdown(
        """
        <div style="
            background: rgba(30, 30, 63, 0.8);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        ">
            <h4 style="color: #F1F5F9; margin: 0 0 1rem; font-size: 1rem;">📊 Agent Queue</h4>
        """,
        unsafe_allow_html=True,
    )
    
    queue_items = [
        {"status": "Running", "agents": MOCK_QUEUE["running"], "color": "#10B981", "icon": "▶️"},
        {"status": "Waiting", "agents": MOCK_QUEUE["waiting"], "color": "#64748B", "icon": "⏸️"},
        {"status": "Paused", "agents": MOCK_QUEUE["paused"], "color": "#F59E0B", "icon": "⏸️"},
        {"status": "Failed", "agents": MOCK_QUEUE["failed"], "color": "#EF4444", "icon": "❌"},
    ]
    
    for item in queue_items:
        with st.expander(f"{item['icon']} {item['status']} ({len(item['agents'])})", expanded=item["status"] == "Running"):
            if item["agents"]:
                for agent in item["agents"]:
                    st.markdown(
                        f"""
                        <div style="
                            padding: 0.5rem 0.75rem;
                            background: rgba(51, 65, 85, 0.5);
                            border-radius: 6px;
                            margin-bottom: 0.5rem;
                        ">
                            <span style="color: #F1F5F9; font-size: 0.85rem;">{agent}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown("<p style='color: #64748B; font-size: 0.8rem;'>None</p>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# Resource Dashboard
# ============================================================================

def resource_dashboard() -> None:
    """Display resource usage dashboard."""
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(30, 30, 63, 0.95) 0%, rgba(99, 102, 241, 0.1) 100%);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        ">
            <h4 style="color: #F1F5F9; margin: 0 0 1rem; font-size: 1rem;">📈 Resource Dashboard</h4>
        """,
        unsafe_allow_html=True,
    )
    
    resources = [
        {"name": "CPU", "value": 45, "max": 100, "color": "#F59E0B"},
        {"name": "Memory", "value": 62, "max": 100, "color": "#22D3EE"},
        {"name": "GPU", "value": 28, "max": 100, "color": "#6366F1"},
        {"name": "Token Usage", "value": 156000, "max": 500000, "color": "#10B981", "suffix": " tokens"},
        {"name": "Requests", "value": 1247, "max": 5000, "color": "#8B5CF6", "suffix": ""},
        {"name": "Queue", "value": 8, "max": 50, "color": "#F472B6", "suffix": ""},
        {"name": "Latency", "value": 45, "max": 200, "color": "#EF4444", "suffix": "ms"},
    ]
    
    for res in resources:
        value = res.get("value", 0)
        max_val = res.get("max", 100)
        percentage = int((value / max_val) * 100)
        suffix = res.get("suffix", "%")
        
        st.markdown(
            f"""
            <div style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                    <span style="color: #94A3B8; font-size: 0.8rem;">{res['name']}</span>
                    <span style="color: {res['color']}; font-size: 0.8rem; font-weight: 600;">{value}{suffix}</span>
                </div>
                <div style="height: 6px; background: #334155; border-radius: 3px; overflow: hidden;">
                    <div style="width: {percentage}%; height: 100%; background: {res['color']}; border-radius: 3px;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# AI Model Panel
# ============================================================================

def ai_model_panel() -> None:
    """Display AI model usage panel."""
    st.markdown(
        """
        <div style="
            background: rgba(30, 30, 63, 0.8);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        ">
            <h4 style="color: #F1F5F9; margin: 0 0 1rem; font-size: 1rem;">🧠 AI Models</h4>
        """,
        unsafe_allow_html=True,
    )
    
    for model in MOCK_MODELS:
        st.markdown(
            f"""
            <div style="
                display: flex;
                align-items: center;
                gap: 1rem;
                padding: 0.75rem;
                background: rgba(51, 65, 85, 0.5);
                border-radius: 8px;
                margin-bottom: 0.5rem;
            ">
                <div style="
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    background: {model['color']};
                "></div>
                <div style="flex: 1;">
                    <p style="color: #F1F5F9; margin: 0; font-size: 0.85rem;">{model['name']}</p>
                </div>
                <div style="width: 60px; height: 6px; background: #334155; border-radius: 3px; overflow: hidden;">
                    <div style="width: {model['usage']}%; height: 100%; background: {model['color']}; border-radius: 3px;"></div>
                </div>
                <span style="color: {model['color']}; font-size: 0.8rem; font-weight: 600; min-width: 40px; text-align: right;">{model['usage']}%</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# Event Stream
# ============================================================================

def event_stream() -> None:
    """Display live event stream."""
    st.markdown(
        """
        <div style="
            background: rgba(30, 30, 63, 0.8);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h4 style="color: #F1F5F9; margin: 0; font-size: 1rem;">⚡ Event Stream</h4>
                <span style="
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    background: #10B981;
                    animation: blink 1s infinite;
                "></span>
            </div>
        """,
        unsafe_allow_html=True,
    )
    
    event_types = {
        "started": ("#10B981", "🚀"),
        "task": ("#6366F1", "📋"),
        "completed": ("#22D3EE", "✅"),
        "message": ("#94A3B8", "💬"),
        "retry": ("#F59E0B", "🔄"),
        "learning": ("#8B5CF6", "🧠"),
    }
    
    for event in MOCK_EVENTS:
        color, icon = event_types.get(event["type"], ("#64748B", "ℹ️"))
        st.markdown(
            f"""
            <div style="
                display: flex;
                align-items: flex-start;
                gap: 0.75rem;
                padding: 0.5rem 0;
                border-bottom: 1px solid rgba(51, 65, 85, 0.5);
            ">
                <span style="font-size: 1rem;">{icon}</span>
                <div style="flex: 1;">
                    <p style="color: #F1F5F9; margin: 0; font-size: 0.8rem;">{event['message']}</p>
                    <p style="color: {color}; margin: 0.25rem 0 0; font-size: 0.7rem;">{event['agent']}</p>
                </div>
                <span style="color: #64748B; font-size: 0.7rem;">{event['time'].strftime('%H:%M:%S')}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown(
        """
        <style>
            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.3; }
            }
        </style>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# Mission Health
# ============================================================================

def mission_health() -> None:
    """Display mission health metrics."""
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(30, 30, 63, 0.95) 100%);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        ">
            <h4 style="color: #F1F5F9; margin: 0 0 1rem; font-size: 1rem;">🏥 Mission Health</h4>
        """,
        unsafe_allow_html=True,
    )
    
    health_items = [
        {"label": "Overall Health", "value": 94, "color": "#10B981"},
        {"label": "CPU Usage", "value": 45, "color": "#F59E0B"},
        {"label": "Memory Usage", "value": 62, "color": "#22D3EE"},
        {"label": "Failures", "value": 2, "color": "#EF4444"},
        {"label": "Retries", "value": 5, "color": "#F59E0B"},
        {"label": "Warnings", "value": 3, "color": "#F59E0B"},
        {"label": "Confidence", "value": 89, "color": "#10B981"},
    ]
    
    col1, col2 = st.columns(2)
    
    for i, item in enumerate(health_items):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(
                f"""
                <div style="
                    padding: 0.75rem;
                    background: rgba(51, 65, 85, 0.5);
                    border-radius: 8px;
                    margin-bottom: 0.5rem;
                ">
                    <p style="color: #64748B; margin: 0; font-size: 0.7rem;">{item['label']}</p>
                    <p style="color: {item['color']}; margin: 0.25rem 0 0; font-size: 1.25rem; font-weight: 600;">{item['value']}{'%' if isinstance(item['value'], int) and item['value'] < 100 else ''}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# Agent Drawer
# ============================================================================

def agent_drawer(agent: Dict) -> None:
    """Display detailed agent drawer with all fields."""
    with st.expander(f"🤖 {agent['name']} Details", expanded=True):
        # Agent Header
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(30, 30, 63, 0.95) 100%);
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                text-align: center;
            ">
                <span style="font-size: 4rem; display: block; margin-bottom: 1rem;">{agent['icon']}</span>
                <h3 style="color: #F1F5F9; margin: 0;">{agent['name']}</h3>
                <p style="color: #64748B; margin: 0.5rem 0 0;">Agent DNA • v{agent.get('version', '1.0.0')}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Basic Info
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Role:** {agent.get('role', 'Agent')}")
            st.markdown(f"**Version:** {agent.get('version', '1.0.0')}")
            st.markdown(f"**Status:** {agent['status'].title()}")
        with col2:
            st.markdown(f"**Owner:** {agent.get('owner', 'AI-QOS Team')}")
            st.markdown(f"**Last Updated:** {agent.get('last_updated', 'N/A')}")
            st.markdown(f"**Health Score:** {agent['health']}%")
        
        # Capabilities
        st.markdown("**🎯 Capabilities:**")
        capabilities = agent.get('capabilities', ['No capabilities defined'])
        for cap in capabilities:
            st.markdown(f"- {cap}")
        
        # Permissions
        st.markdown("**🔐 Permissions:**")
        permissions = agent.get('permissions', ['Read'])
        for perm in permissions:
            st.markdown(f"- {perm}")
        
        # Tools
        st.markdown("**🛠️ Tools:**")
        tools = agent.get('tools', [agent.get('tool', 'N/A')])
        for tool in tools:
            st.markdown(f"- {tool}")
        
        # Dependencies
        st.markdown("**🔗 Dependencies:**")
        deps = agent.get('dependencies', [])
        if deps:
            for dep in deps:
                st.markdown(f"- {dep}")
        else:
            st.markdown("- No dependencies")
        
        # Current Context
        st.markdown("**📋 Current Context:**")
        st.markdown(f"- **Mission:** {agent['mission']}")
        st.markdown(f"- **Current Task:** {agent['task']}")
        st.markdown(f"- **Progress:** {agent['progress']}%")
        st.markdown(f"- **Confidence:** {agent['confidence']}%")
        st.markdown(f"- **Current Tool:** {agent['tool']}")
        st.markdown(f"- **Current Model:** {agent['model']}")
        
        # Memory Usage
        st.markdown("**💾 Memory Usage:**")
        st.markdown(f"- {agent.get('memory_usage', 'N/A')}")
        
        # Current Prompt
        st.markdown("**💭 Current Prompt:**")
        st.code(agent.get('current_prompt', 'No current prompt'), language=None)
        
        # Execution History
        st.markdown("**📊 Execution History:**")
        st.json({
            "total_tasks": 24,
            "completed": 18,
            "failed": 1,
            "avg_duration": "45s",
            "success_rate": "94%",
        })
        
        # Health History
        st.markdown("**🏥 Health History:**")
        st.line_chart({"health": [95, 92, 94, 96, 95, 98, 97]})
