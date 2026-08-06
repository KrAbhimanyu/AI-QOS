"""AgentCard Component - Displays individual agent information."""

from typing import Any
import streamlit as st
from datetime import datetime, timedelta


def render_status_badge(status: str) -> str:
    """Get HTML for status badge."""
    colors = {
        "running": ("#10b981", "Running"),
        "waiting": ("#f59e0b", "Waiting"),
        "paused": ("#64748b", "Paused"),
        "failed": ("#ef4444", "Failed"),
        "completed": ("#3b82f6", "Completed"),
        "idle": ("#94a3b8", "Idle"),
    }
    color, label = colors.get(status.lower(), ("#94a3b8", status))
    
    pulse_class = "animation: pulse 2s infinite;" if status == "running" else ""
    
    return f"""
    <div style="
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        background: {color}20;
        border: 1px solid {color}50;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
    ">
        <span style="
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: {color};
            {pulse_class}
        "></span>
        <span style="color: {color};">{label}</span>
    </div>
    """


def render_health_bar(health: float) -> str:
    """Get HTML for health progress bar."""
    if health >= 0.9:
        color = "#10b981"
    elif health >= 0.75:
        color = "#22d3ee"
    elif health >= 0.5:
        color = "#f59e0b"
    else:
        color = "#ef4444"
    
    return f"""
    <div style="
        width: 100%;
        height: 6px;
        background: #334155;
        border-radius: 3px;
        overflow: hidden;
    ">
        <div style="
            width: {health * 100}%;
            height: 100%;
            background: linear-gradient(90deg, {color}, {color}cc);
            border-radius: 3px;
            transition: width 0.5s ease;
        "></div>
    </div>
    """


def render_progress_bar(progress: float, status: str) -> str:
    """Get HTML for task progress bar."""
    if status != "running":
        return f"""
        <div style="
            width: 100%;
            height: 6px;
            background: #334155;
            border-radius: 3px;
        ">
            <div style="
                width: {progress}%;
                height: 100%;
                background: linear-gradient(90deg, #6366f1, #22d3ee);
                border-radius: 3px;
            "></div>
        </div>
        """
    
    return f"""
    <div style="
        width: 100%;
        height: 6px;
        background: #334155;
        border-radius: 3px;
        overflow: hidden;
    ">
        <div style="
            width: {progress}%;
            height: 100%;
            background: linear-gradient(90deg, #6366f1, #22d3ee);
            border-radius: 3px;
            position: relative;
            overflow: hidden;
        ">
            <div style="
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
                animation: shimmer 1.5s infinite;
            "></div>
        </div>
    </div>
    """


def render_metric_mini(value: float, label: str, suffix: str = "%") -> str:
    """Get HTML for mini metric display."""
    return f"""
    <div style="text-align: center;">
        <div style="
            font-size: 16px;
            font-weight: 600;
            font-family: 'JetBrains Mono', monospace;
            color: #f8fafc;
        ">{value}{suffix}</div>
        <div style="
            font-size: 10px;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        ">{label}</div>
    </div>
    """


def format_duration(seconds: int) -> str:
    """Format duration in human-readable format."""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    else:
        return f"{seconds // 3600}h {(seconds % 3600) // 60}m"


def agent_card(agent: dict[str, Any], key: str | None = None) -> None:
    """
    Render an agent card with full details.
    
    Args:
        agent: Agent data dictionary
        key: Optional unique key for the card
    """
    status_color = {
        "running": "#10b981",
        "waiting": "#f59e0b",
        "paused": "#64748b",
        "failed": "#ef4444",
        "completed": "#3b82f6",
        "idle": "#94a3b8",
    }.get(agent["status"].value, "#94a3b8")
    
    category_colors = {
        "Intelligence": "#8b5cf6",
        "Testing": "#3b82f6",
        "Documentation": "#10b981",
        "Infrastructure": "#f59e0b",
        "Learning": "#ec4899",
        "Security": "#ef4444",
        "Support": "#22d3ee",
    }
    category_color = category_colors.get(agent["category"].value, "#6366f1")
    
    with st.container():
        # Main card with glassmorphism
        st.markdown(f"""
        <div class="agent-card" id="agent-{agent['id']}" style="margin-bottom: 16px;">
            <!-- Header -->
            <div style="display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 16px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="
                        width: 48px;
                        height: 48px;
                        border-radius: 12px;
                        background: linear-gradient(135deg, {status_color}30, {status_color}10);
                        border: 1px solid {status_color}30;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 24px;
                    ">
                        {agent['icon']}
                    </div>
                    <div>
                        <h3 style="
                            margin: 0;
                            font-size: 16px;
                            font-weight: 600;
                            color: #f8fafc;
                        ">{agent['name']}</h3>
                        <div style="
                            display: inline-flex;
                            align-items: center;
                            gap: 6px;
                            padding: 2px 8px;
                            background: {category_color}20;
                            border: 1px solid {category_color}40;
                            border-radius: 4px;
                            font-size: 11px;
                            color: {category_color};
                            margin-top: 4px;
                        ">
                            {agent['category'].value}
                        </div>
                    </div>
                </div>
                {render_status_badge(agent['status'].value)}
            </div>
            
            <!-- Mission -->
            <div style="
                padding: 12px;
                background: rgba(30, 41, 59, 0.6);
                border-radius: 8px;
                margin-bottom: 16px;
            ">
                <div style="
                    font-size: 11px;
                    color: #64748b;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    margin-bottom: 4px;
                ">Current Mission</div>
                <div style="
                    font-size: 14px;
                    color: #f8fafc;
                    line-height: 1.4;
                ">{agent['mission']}</div>
            </div>
            
            <!-- Task & Progress -->
            <div style="margin-bottom: 16px;">
                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 6px;
                ">
                    <span style="font-size: 12px; color: #94a3b8;">
                        {agent['current_task']}
                    </span>
                    <span style="
                        font-size: 12px;
                        font-weight: 600;
                        font-family: 'JetBrains Mono', monospace;
                        color: #6366f1;
                    ">{agent['progress']:.0f}%</span>
                </div>
                {render_progress_bar(agent['progress'], agent['status'].value)}
            </div>
            
            <!-- Metrics Grid -->
            <div style="
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 12px;
                margin-bottom: 16px;
                padding: 12px;
                background: rgba(30, 41, 59, 0.4);
                border-radius: 8px;
            ">
                {render_metric_mini(agent['cpu'], 'CPU')}
                {render_metric_mini(agent['memory'], 'MEM')}
                {render_metric_mini(agent['confidence'] * 100, 'CONF', '%')}
                {render_metric_mini(agent['health'] * 100, 'HLTH', '%')}
            </div>
            
            <!-- Additional Info -->
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding-top: 12px;
                border-top: 1px solid rgba(148, 163, 184, 0.1);
            ">
                <div style="display: flex; align-items: center; gap: 16px;">
                    <div>
                        <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Tool</div>
                        <div style="font-size: 12px; color: #94a3b8;">
                            {agent['current_tool'].value if agent['current_tool'] else 'N/A'}
                        </div>
                    </div>
                    <div>
                        <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Model</div>
                        <div style="font-size: 12px; color: #94a3b8;">{agent['current_model'].value}</div>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Exec Time</div>
                    <div style="
                        font-size: 12px;
                        font-family: 'JetBrains Mono', monospace;
                        color: #94a3b8;
                    ">{format_duration(agent['execution_time'])}</div>
                </div>
            </div>
            
            <!-- Messages Processed & Health -->
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 12px;
                padding-top: 12px;
                border-top: 1px solid rgba(148, 163, 184, 0.1);
            ">
                <div>
                    <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Messages</div>
                    <div style="
                        font-size: 14px;
                        font-weight: 600;
                        font-family: 'JetBrains Mono', monospace;
                        color: #f8fafc;
                    ">{agent['messages_processed']:,}</div>
                </div>
                <div style="flex: 1; max-width: 120px; margin: 0 16px;">
                    {render_health_bar(agent['health'])}
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Health</div>
                    <div style="
                        font-size: 14px;
                        font-weight: 600;
                        color: {'#10b981' if agent['health'] >= 0.9 else '#f59e0b' if agent['health'] >= 0.7 else '#ef4444'};
                    ">{agent['health']:.0%}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Click handler
        if st.button(
            f"View Details: {agent['name']}",
            key=f"btn_{key or agent['id']}",
            use_container_width=True,
            type="secondary"
        ):
            from src.utils.session import SessionState
            SessionState.select_agent(agent)
            st.rerun()
