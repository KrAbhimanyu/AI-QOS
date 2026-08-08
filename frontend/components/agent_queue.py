"""AgentQueue Component - Agent queue status visualization."""

from typing import Any
import streamlit as st


QUEUE_STATUS_CONFIG = {
    "running": {
        "color": "#10b981",
        "bg_color": "rgba(16, 185, 129, 0.15)",
        "icon": "▶️",
        "label": "Running",
    },
    "waiting": {
        "color": "#f59e0b",
        "bg_color": "rgba(245, 158, 11, 0.15)",
        "icon": "⏳",
        "label": "Waiting",
    },
    "paused": {
        "color": "#64748b",
        "bg_color": "rgba(100, 116, 139, 0.15)",
        "icon": "⏸️",
        "label": "Paused",
    },
    "failed": {
        "color": "#ef4444",
        "bg_color": "rgba(239, 68, 68, 0.15)",
        "icon": "❌",
        "label": "Failed",
    },
    "completed": {
        "color": "#3b82f6",
        "bg_color": "rgba(59, 130, 246, 0.15)",
        "icon": "✅",
        "label": "Completed",
    },
    "idle": {
        "color": "#94a3b8",
        "bg_color": "rgba(148, 163, 184, 0.15)",
        "icon": "💤",
        "label": "Idle",
    },
}


def get_queue_counts(agents: list[dict[str, Any]]) -> dict[str, int]:
    """Calculate queue counts by status."""
    counts = {
        "running": 0,
        "waiting": 0,
        "paused": 0,
        "failed": 0,
        "completed": 0,
        "idle": 0,
    }
    
    for agent in agents:
        status = agent["status"].value.lower()
        if status in counts:
            counts[status] += 1
    
    return counts


def render_queue_bar(counts: dict[str, int], total: int) -> None:
    """Render queue as horizontal stacked bar."""
    if total == 0:
        return
    
    segments = []
    for status, config in QUEUE_STATUS_CONFIG.items():
        count = counts.get(status, 0)
        if count > 0:
            width = (count / total) * 100
            segments.append(f"""
                <div style="
                    width: {width}%;
                    height: 100%;
                    background: {config['color']};
                    position: relative;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">
                    <span style="
                        font-size: 11px;
                        font-weight: 600;
                        color: #fff;
                        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
                    ">
                        {count}
                    </span>
                </div>
            """)
    
    st.markdown(f"""<div style=" display: flex; height: 36px; border-radius: 8px; overflow: hidden; margin: 16px 0; border: 1px solid rgba(148, 163, 184, 0.1); "> {''.join(segments)} </div>""", unsafe_allow_html=True)


def render_queue_item(status: str, count: int, config: dict[str, Any]) -> None:
    """Render individual queue status item."""
    st.markdown(f"""<div style=" display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; background: {config['bg_color']}; border: 1px solid {config['color']}30; border-radius: 10px; margin-bottom: 8px; transition: all 0.2s ease; "> <div style="display: flex; align-items: center; gap: 12px;"> <span style="font-size: 20px;">{config['icon']}</span> <span style="font-size: 14px; color: #f8fafc; font-weight: 500;"> {config['label']} </span> </div> <div style=" font-size: 20px; font-weight: 700; font-family: 'JetBrains Mono', monospace; color: {config['color']}; "> {count} </div> </div>""", unsafe_allow_html=True)


def render_queue_visual(agents: list[dict[str, Any]]) -> None:
    """Render visual queue representation."""
    counts = get_queue_counts(agents)
    total = len(agents)
    
    if total == 0:
        return
    
    # Grid visualization
    st.markdown("""<style> .queue-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(50px, 1fr)); gap: 8px; padding: 16px; background: rgba(30, 41, 59, 0.4); border-radius: 12px; margin-top: 12px; } .queue-dot { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px; transition: all 0.2s ease; cursor: pointer; } .queue-dot:hover { transform: scale(1.15); z-index: 1; } </style>""", unsafe_allow_html=True)
    
    st.markdown('<div class="queue-grid">', unsafe_allow_html=True)
    
    for agent in agents:
        status = agent["status"].value.lower()
        config = QUEUE_STATUS_CONFIG.get(status, QUEUE_STATUS_CONFIG["idle"])
        
        st.markdown(f"""<div class="queue-dot" style="background: {config['bg_color']}; border: 2px solid {config['color']}50;" title="{agent['name']}: {agent['status'].value}"> {agent['icon']} </div>""", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def agent_queue(agents: list[dict[str, Any]]) -> None:
    """
    Render the Agent Queue component.
    
    Args:
        agents: List of agent dictionaries
    """
    st.markdown("### 📋 Agent Queue")
    
    counts = get_queue_counts(agents)
    total = len(agents)
    
    # Summary header
    col1, col2 = st.columns(2)
    
    with col1:
        running = counts.get("running", 0)
        st.markdown(f"""<div style=" padding: 16px; background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.1)); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; text-align: center; "> <div style="font-size: 36px; font-weight: 700; color: #10b981;"> {running} </div> <div style="font-size: 12px; color: #64748b; text-transform: uppercase;"> Active Agents </div> </div>""", unsafe_allow_html=True)
    
    with col2:
        failed = counts.get("failed", 0)
        failed_color = "#ef4444" if failed > 0 else "#10b981"
        st.markdown(f"""<div style=" padding: 16px; background: linear-gradient(135deg, {failed_color}20, {failed_color}10); border: 1px solid {failed_color}30; border-radius: 12px; text-align: center; "> <div style="font-size: 36px; font-weight: 700; color: {failed_color};"> {failed} </div> <div style="font-size: 12px; color: #64748b; text-transform: uppercase;"> Failed Agents </div> </div>""", unsafe_allow_html=True)
    
    # Queue bar
    st.markdown("#### Queue Distribution")
    render_queue_bar(counts, total)
    
    # Queue items
    st.markdown("""<div style=" display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; ">""", unsafe_allow_html=True)
    
    for status, config in QUEUE_STATUS_CONFIG.items():
        count = counts.get(status, 0)
        render_queue_item(status, count, config)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Visual grid
    with st.expander("🔲 Visual Grid", expanded=False):
        render_queue_visual(agents)
