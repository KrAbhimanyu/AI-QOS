"""EventStream Component - Real-time event feed visualization."""

from datetime import datetime
from typing import Any
import streamlit as st


EVENT_COLORS = {
    "info": ("#3b82f6", "rgba(59, 130, 246, 0.15)"),
    "success": ("#10b981", "rgba(16, 185, 129, 0.15)"),
    "warning": ("#f59e0b", "rgba(245, 158, 11, 0.15)"),
    "error": ("#ef4444", "rgba(239, 68, 68, 0.15)"),
}

EVENT_ICONS = {
    "info": "ℹ️",
    "success": "✅",
    "warning": "⚠️",
    "error": "❌",
}


def format_time(ts: datetime) -> str:
    """Format timestamp for display."""
    now = datetime.now()
    diff = (now - ts).total_seconds()
    
    if diff < 60:
        return "Just now"
    elif diff < 3600:
        return f"{int(diff / 60)}m ago"
    elif diff < 86400:
        return f"{int(diff / 3600)}h ago"
    else:
        return ts.strftime("%H:%M:%S")


def render_event_item(event: dict[str, Any], compact: bool = False) -> None:
    """Render a single event item."""
    color, bg_color = EVENT_COLORS.get(event.get('severity', 'info'), EVENT_COLORS['info'])
    icon = EVENT_ICONS.get(event.get('severity', 'info'), EVENT_ICONS['info'])
    
    if compact:
        st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 12px;
            background: {bg_color};
            border-left: 3px solid {color};
            border-radius: 0 6px 6px 0;
            margin-bottom: 6px;
            transition: all 0.2s ease;
        ">
            <span style="font-size: 14px;">{icon}</span>
            <div style="flex: 1; min-width: 0;">
                <div style="
                    font-size: 12px;
                    color: #f8fafc;
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                ">
                    {event['message']}
                </div>
            </div>
            <span style="
                font-size: 10px;
                color: #64748b;
                font-family: 'JetBrains Mono', monospace;
            ">
                {format_time(event['timestamp'])}
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="
            padding: 12px;
            background: {bg_color};
            border-left: 4px solid {color};
            border-radius: 0 8px 8px 0;
            margin-bottom: 10px;
            transition: all 0.2s ease;
        ">
            <div style="display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 8px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 18px;">{icon}</span>
                    <span style="
                        font-size: 12px;
                        font-weight: 600;
                        color: #f8fafc;
                    ">
                        {event.get('type', 'Event').replace('_', ' ').title()}
                    </span>
                </div>
                <span style="
                    font-size: 10px;
                    color: #64748b;
                    font-family: 'JetBrains Mono', monospace;
                ">
                    {format_time(event['timestamp'])}
                </span>
            </div>
            <div style="
                font-size: 13px;
                color: #94a3b8;
                line-height: 1.4;
            ">
                {event['message']}
            </div>
            <div style="
                display: inline-flex;
                align-items: center;
                gap: 4px;
                margin-top: 8px;
                padding: 2px 8px;
                background: {color}20;
                border-radius: 4px;
                font-size: 10px;
                text-transform: uppercase;
                color: {color};
            ">
                {event.get('severity', 'info')}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_event_timeline(events: list[dict[str, Any]]) -> None:
    """Render events as a vertical timeline."""
    st.markdown("""
    <style>
    .timeline {
        position: relative;
        padding-left: 30px;
    }
    
    .timeline::before {
        content: '';
        position: absolute;
        left: 10px;
        top: 0;
        bottom: 0;
        width: 2px;
        background: linear-gradient(180deg, #6366f1, #22d3ee);
        opacity: 0.3;
    }
    
    .timeline-item {
        position: relative;
        padding-bottom: 20px;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -24px;
        top: 4px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #6366f1;
        border: 2px solid #1e293b;
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.5);
    }
    
    .timeline-item.success::before {
        background: #10b981;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
    }
    
    .timeline-item.error::before {
        background: #ef4444;
        box-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
    }
    
    .timeline-item.warning::before {
        background: #f59e0b;
        box-shadow: 0 0 10px rgba(245, 158, 11, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="timeline">', unsafe_allow_html=True)
    
    for event in events[:10]:
        severity_class = event.get('severity', 'info')
        st.markdown(f'<div class="timeline-item {severity_class}">', unsafe_allow_html=True)
        render_event_item(event, compact=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_event_stats(events: list[dict[str, Any]]) -> dict[str, int]:
    """Calculate and render event statistics."""
    stats = {
        "total": len(events),
        "info": 0,
        "success": 0,
        "warning": 0,
        "error": 0,
    }
    
    for event in events:
        severity = event.get('severity', 'info')
        if severity in stats:
            stats[severity] += 1
    
    cols = st.columns(4)
    
    with cols[0]:
        st.markdown(f"""
        <div style="
            padding: 10px;
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 8px;
            text-align: center;
        ">
            <div style="font-size: 20px; font-weight: 700; color: #3b82f6;">
                {stats['info']}
            </div>
            <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">
                Info
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown(f"""
        <div style="
            padding: 10px;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.2);
            border-radius: 8px;
            text-align: center;
        ">
            <div style="font-size: 20px; font-weight: 700; color: #10b981;">
                {stats['success']}
            </div>
            <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">
                Success
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown(f"""
        <div style="
            padding: 10px;
            background: rgba(245, 158, 11, 0.1);
            border: 1px solid rgba(245, 158, 11, 0.2);
            border-radius: 8px;
            text-align: center;
        ">
            <div style="font-size: 20px; font-weight: 700; color: #f59e0b;">
                {stats['warning']}
            </div>
            <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">
                Warning
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[3]:
        st.markdown(f"""
        <div style="
            padding: 10px;
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            border-radius: 8px;
            text-align: center;
        ">
            <div style="font-size: 20px; font-weight: 700; color: #ef4444;">
                {stats['error']}
            </div>
            <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">
                Error
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    return stats


def event_stream(events: list[dict[str, Any]], max_display: int = 15) -> None:
    """
    Render the event stream component.
    
    Args:
        events: List of event dictionaries
        max_display: Maximum number of events to display
    """
    st.markdown("### 🔔 Event Stream")
    
    # Stats row
    render_event_stats(events[:50])
    
    st.markdown("")  # Spacer
    
    # Live indicator
    st.markdown("""
    <div style="
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 16px;
    ">
        <div style="
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #10b981;
            animation: pulse 2s infinite;
        "></div>
        <span style="font-size: 12px; color: #10b981; font-weight: 500;">
            Live Feed
        </span>
        <span style="font-size: 12px; color: #64748b;">
            • {} events
        </span>
    </div>
    <style>
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
    }
    </style>
    """.format(len(events)), unsafe_allow_html=True)
    
    # Display events
    display_events = events[:max_display]
    
    for event in display_events:
        render_event_item(event, compact=False)
    
    if len(events) > max_display:
        with st.expander(f"View all {len(events)} events..."):
            for event in events[max_display:]:
                render_event_item(event, compact=True)
