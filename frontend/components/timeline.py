"""Timeline Component - Bottom timeline for agent events."""

from typing import Any
from datetime import datetime, timedelta
import streamlit as st


def render_timeline_marker(
    timestamp: datetime,
    label: str,
    status: str,
    is_active: bool = False
) -> None:
    """Render a single timeline marker."""
    colors = {
        "success": "#10b981",
        "info": "#3b82f6",
        "warning": "#f59e0b",
        "error": "#ef4444",
    }
    color = colors.get(status, "#3b82f6")
    
    time_str = timestamp.strftime("%H:%M:%S")
    
    pulse_class = "animation: pulse 2s infinite;" if is_active else ""
    
    st.markdown(f"""<div style=" display: flex; flex-direction: column; align-items: center; gap: 8px; "> <div style=" width: 12px; height: 12px; border-radius: 50%; background: {color}; box-shadow: 0 0 10px {color}50; {pulse_class} "></div> <div style=" font-size: 10px; color: #64748b; font-family: 'JetBrains Mono', monospace; "> {time_str} </div> <div style=" padding: 4px 8px; background: {color}20; border-radius: 4px; font-size: 10px; color: #f8fafc; text-align: center; max-width: 80px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; "> {label} </div> </div>""", unsafe_allow_html=True)


def render_horizontal_timeline(events: list[dict[str, Any]]) -> None:
    """Render horizontal timeline of events."""
    if not events:
        return
    
    # Group events by time bucket
    time_buckets = []
    current_bucket = []
    bucket_size = 5
    
    for i, event in enumerate(events):
        current_bucket.append(event)
        if len(current_bucket) >= bucket_size:
            time_buckets.append(current_bucket)
            current_bucket = []
    
    if current_bucket:
        time_buckets.append(current_bucket)
    
    # Render timeline
    st.markdown("""<style> .timeline-container { overflow-x: auto; padding: 20px 0; margin: 0 -20px; } .timeline-wrapper { display: flex; gap: 40px; padding: 0 20px; min-width: max-content; position: relative; } .timeline-wrapper::before { content: ''; position: absolute; top: 35px; left: 20px; right: 20px; height: 3px; background: linear-gradient(90deg, #6366f1, #22d3ee); border-radius: 2px; opacity: 0.5; } .timeline-bucket { display: flex; flex-direction: column; align-items: center; gap: 12px; min-width: 80px; } .timeline-dot { width: 16px; height: 16px; border-radius: 50%; background: #6366f1; border: 3px solid #1e293b; box-shadow: 0 0 15px rgba(99, 102, 241, 0.5); z-index: 1; } .timeline-time { font-size: 11px; color: #64748b; font-family: 'JetBrains Mono', monospace; margin-top: 8px; } .timeline-events { display: flex; flex-direction: column; gap: 6px; margin-top: 8px; } .timeline-event { padding: 6px 10px; background: rgba(30, 41, 59, 0.6); border-radius: 6px; font-size: 10px; color: #94a3b8; white-space: nowrap; max-width: 100px; overflow: hidden; text-overflow: ellipsis; } .timeline-event.info { border-left: 2px solid #3b82f6; } .timeline-event.success { border-left: 2px solid #10b981; } .timeline-event.warning { border-left: 2px solid #f59e0b; } .timeline-event.error { border-left: 2px solid #ef4444; } </style>""", unsafe_allow_html=True)
    
    st.markdown('<div class="timeline-container"><div class="timeline-wrapper">', unsafe_allow_html=True)
    
    for bucket in time_buckets:
        timestamp = bucket[0]['timestamp']
        time_str = timestamp.strftime("%H:%M")
        
        # Determine dominant status
        statuses = [e.get('severity', 'info') for e in bucket]
        dominant_status = max(set(statuses), key=statuses.count) if statuses else 'info'
        
        colors = {"success": "#10b981", "info": "#3b82f6", "warning": "#f59e0b", "error": "#ef4444"}
        color = colors.get(dominant_status, "#3b82f6")
        
        st.markdown(f"""<div class="timeline-bucket"> <div class="timeline-dot" style="background: {color}; box-shadow: 0 0 15px {color}50;"></div> <div class="timeline-time">{time_str}</div> <div class="timeline-events">""", unsafe_allow_html=True)
        
        for event in bucket[:3]:
            status = event.get('severity', 'info')
            message = event.get('message', 'Event')[:20]
            st.markdown(f'<div class="timeline-event {status}">{message}</div>', unsafe_allow_html=True)
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)


def render_agent_timeline(agents: list[dict[str, Any]]) -> None:
    """Render timeline showing agent activity."""
    st.markdown("""<style> .agent-timeline { display: flex; flex-direction: column; gap: 12px; padding: 16px 0; } .agent-timeline-item { display: flex; align-items: center; gap: 16px; padding: 12px 16px; background: rgba(30, 41, 59, 0.4); border-radius: 10px; transition: all 0.2s ease; } .agent-timeline-item:hover { background: rgba(30, 41, 59, 0.6); transform: translateX(4px); } .agent-timeline-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; } .agent-timeline-content { flex: 1; } .agent-timeline-name { font-size: 14px; font-weight: 500; color: #f8fafc; margin-bottom: 2px; } .agent-timeline-mission { font-size: 12px; color: #64748b; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 300px; } .agent-timeline-progress { width: 100px; height: 6px; background: rgba(51, 65, 85, 0.5); border-radius: 3px; overflow: hidden; } .agent-timeline-progress-fill { height: 100%; border-radius: 3px; transition: width 0.5s ease; } .agent-timeline-time { font-size: 11px; color: #64748b; font-family: 'JetBrains Mono', monospace; min-width: 60px; text-align: right; } </style>""", unsafe_allow_html=True)
    
    # Sort agents by status priority and recency
    status_priority = {"running": 0, "waiting": 1, "paused": 2, "failed": 3, "completed": 4, "idle": 5}
    sorted_agents = sorted(
        agents,
        key=lambda a: (status_priority.get(a["status"].value, 6), -a.get("execution_time", 0))
    )
    
    st.markdown('<div class="agent-timeline">', unsafe_allow_html=True)
    
    for agent in sorted_agents[:10]:
        status = agent["status"].value
        icon = agent["icon"]
        
        status_colors = {
            "running": "#10b981",
            "waiting": "#f59e0b",
            "paused": "#64748b",
            "failed": "#ef4444",
            "completed": "#3b82f6",
            "idle": "#94a3b8",
        }
        color = status_colors.get(status, "#94a3b8")
        
        mission = agent.get("mission", "")[:40]
        progress = agent.get("progress", 0)
        exec_time = agent.get("execution_time", 0)
        
        # Format execution time
        if exec_time < 60:
            time_str = f"{exec_time}s"
        elif exec_time < 3600:
            time_str = f"{exec_time // 60}m"
        else:
            time_str = f"{exec_time // 3600}h"
        
        st.markdown(f"""<div class="agent-timeline-item"> <div class="agent-timeline-icon" style="background: {color}20; border: 1px solid {color}40;"> {icon} </div> <div class="agent-timeline-content"> <div class="agent-timeline-name">{agent["name"]}</div> <div class="agent-timeline-mission">{mission}...</div> </div> <div class="agent-timeline-progress"> <div class="agent-timeline-progress-fill" style="width: {progress}%; background: linear-gradient(90deg, {color}, {color}cc);"></div> </div> <div class="agent-timeline-time">{time_str}</div> </div>""", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def timeline(agents: list[dict[str, Any]], events: list[dict[str, Any]]) -> None:
    """
    Render the bottom timeline component.
    
    Args:
        agents: List of agent dictionaries
        events: List of event dictionaries
    """
    st.markdown("---")
    st.markdown("### 📅 Agent Activity Timeline")
    
    tab1, tab2 = st.tabs(["Agent Progress", "Event Stream"])
    
    with tab1:
        render_agent_timeline(agents)
    
    with tab2:
        render_horizontal_timeline(events)
