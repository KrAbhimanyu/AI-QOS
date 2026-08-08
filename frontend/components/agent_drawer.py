"""AgentDrawer Component - Detailed agent information panel."""

from datetime import datetime
from typing import Any
import streamlit as st
import pandas as pd


def format_timestamp(ts: datetime) -> str:
    """Format timestamp for display."""
    return ts.strftime("%H:%M:%S")


def format_full_timestamp(ts: datetime) -> str:
    """Format full timestamp with date."""
    return ts.strftime("%Y-%m-%d %H:%M:%S")


def render_dna_section(agent: dict[str, Any]) -> None:
    """Render the Agent DNA section."""
    st.markdown("### 🧬 Agent DNA")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div style="padding: 12px; background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 8px; margin-bottom: 12px;"> <div style="font-size: 11px; color: #64748b; text-transform: uppercase; margin-bottom: 6px;">Agent ID</div> <div style="font-size: 14px; font-family: 'JetBrains Mono', monospace; color: #f8fafc;">{agent['id']}</div> </div>""", unsafe_allow_html=True)
        
        st.markdown(f"""<div style="padding: 12px; background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 8px; margin-bottom: 12px;"> <div style="font-size: 11px; color: #64748b; text-transform: uppercase; margin-bottom: 6px;">Category</div> <div style="font-size: 14px; color: #f8fafc;">{agent['category'].value}</div> </div>""", unsafe_allow_html=True)
        
        st.markdown(f"""<div style="padding: 12px; background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 8px;"> <div style="font-size: 11px; color: #64748b; text-transform: uppercase; margin-bottom: 6px;">Status</div> <div style="font-size: 14px; color: #f8fafc;">{agent['status'].value.title()}</div> </div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""<div style="padding: 12px; background: rgba(34, 211, 238, 0.1); border: 1px solid rgba(34, 211, 238, 0.2); border-radius: 8px; margin-bottom: 12px;"> <div style="font-size: 11px; color: #64748b; text-transform: uppercase; margin-bottom: 6px;">Current Model</div> <div style="font-size: 14px; color: #f8fafc;">{agent['current_model'].value}</div> </div>""", unsafe_allow_html=True)
        
        tool_name = agent['current_tool'].value if agent['current_tool'] else "None"
        st.markdown(f"""<div style="padding: 12px; background: rgba(34, 211, 238, 0.1); border: 1px solid rgba(34, 211, 238, 0.2); border-radius: 8px; margin-bottom: 12px;"> <div style="font-size: 11px; color: #64748b; text-transform: uppercase; margin-bottom: 6px;">Current Tool</div> <div style="font-size: 14px; color: #f8fafc;">{tool_name}</div> </div>""", unsafe_allow_html=True)
        
        st.markdown(f"""<div style="padding: 12px; background: rgba(34, 211, 238, 0.1); border: 1px solid rgba(34, 211, 238, 0.2); border-radius: 8px;"> <div style="font-size: 11px; color: #64748b; text-transform: uppercase; margin-bottom: 6px;">Confidence</div> <div style="font-size: 14px; color: #f8fafc;">{agent['confidence']:.1%}</div> </div>""", unsafe_allow_html=True)


def render_capabilities_section(capabilities: list[str]) -> None:
    """Render capabilities list."""
    st.markdown("### ⚡ Capabilities")
    caps_html = ""
    for cap in capabilities:
        caps_html += f"""
        <div style="display: inline-flex; align-items: center; gap: 8px; padding: 8px 14px; background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.2); border-radius: 6px; margin: 4px 8px 4px 0; font-size: 13px; color: #c4b5fd;">
            <span style="color: #8b5cf6;">▸</span>{cap}
        </div>
        """
    st.markdown(caps_html, unsafe_allow_html=True)


def render_tools_section(tools: list[Any]) -> None:
    """Render tools list."""
    st.markdown("### 🛠️ Tools")
    cols = st.columns(2)
    for i, tool in enumerate(tools):
        with cols[i % 2]:
            st.markdown(f"""<div style="padding: 10px 14px; background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 6px; font-size: 13px; color: #93c5fd; margin-bottom: 8px;"> {tool.value} </div>""", unsafe_allow_html=True)


def render_current_context_section(context: dict[str, Any]) -> None:
    """Render current execution context."""
    st.markdown("### 📍 Current Context")
    
    project = context.get('project', 'N/A')
    module = context.get('module', 'N/A')
    branch = context.get('branch', 'N/A')
    env = context.get('environment', 'N/A')
    
    st.markdown(f"""<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;"> <div style="padding: 10px; background: rgba(30, 41, 59, 0.6); border-radius: 6px;"> <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Project</div> <div style="font-size: 12px; color: #f8fafc; font-family: 'JetBrains Mono', monospace;">{project}</div> </div> <div style="padding: 10px; background: rgba(30, 41, 59, 0.6); border-radius: 6px;"> <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Module</div> <div style="font-size: 12px; color: #f8fafc; font-family: 'JetBrains Mono', monospace;">{module}</div> </div> <div style="padding: 10px; background: rgba(30, 41, 59, 0.6); border-radius: 6px;"> <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Branch</div> <div style="font-size: 12px; color: #f8fafc; font-family: 'JetBrains Mono', monospace;">{branch}</div> </div> <div style="padding: 10px; background: rgba(30, 41, 59, 0.6); border-radius: 6px;"> <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Environment</div> <div style="font-size: 12px; color: #f8fafc;">{env}</div> </div> </div>""", unsafe_allow_html=True)


def render_memory_section(memory: dict[str, Any]) -> None:
    """Render agent memory state."""
    st.markdown("### 🧠 Memory State")
    
    patterns = memory.get('patterns_learned', 0)
    strategies = memory.get('strategies_optimized', 0)
    kb_size = memory.get('knowledge_base_size', 'N/A')
    ctx_usage = memory.get('context_window_usage', 'N/A')
    
    cols = st.columns(2)
    with cols[0]:
        st.metric("Patterns Learned", patterns)
    with cols[1]:
        st.metric("Strategies Optimized", strategies)
    
    col3, col4 = st.columns(2)
    with col3:
        st.metric("Knowledge Base", kb_size)
    with col4:
        st.metric("Context Window", ctx_usage)


def render_execution_history(history: list[dict[str, Any]]) -> None:
    """Render execution history table."""
    st.markdown("### 📜 Execution History")
    
    if history:
        data = []
        for h in history[:10]:
            data.append({
                "Time": format_timestamp(h["timestamp"]),
                "Action": h["action"],
                "Duration": f"{h['duration_ms']}ms",
                "Status": "✓" if h["success"] else "✗",
            })
        df = pd.DataFrame(data)
        st.dataframe(df, width='stretch', hide_index=True)
    else:
        st.info("No execution history available")


def render_health_history_chart(history: list[dict[str, Any]]) -> None:
    """Render health history as chart."""
    st.markdown("### 📊 Health History")
    
    if history:
        import plotly.express as px
        import plotly.graph_objects as go
        
        df = pd.DataFrame(history)
        df['Time'] = df['timestamp'].apply(lambda x: x.strftime("%H:%M"))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['health'],
            name='Health',
            line=dict(color='#6366f1', width=2),
            fill='tozeroy',
            fillcolor='rgba(99, 102, 241, 0.2)',
        ))
        
        fig.update_layout(
            height=200,
            margin=dict(l=0, r=0, t=20, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8'),
            xaxis=dict(showgrid=False, color='#64748b', title=None),
            yaxis=dict(showgrid=True, gridcolor='rgba(148, 163, 184, 0.1)', color='#64748b', range=[0, 1], title=None),
        )
        
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("No health history available")


def render_recent_events(events: list[dict[str, Any]]) -> None:
    """Render recent events list."""
    st.markdown("### 🔔 Recent Events")
    
    severity_colors = {
        "info": "#3b82f6",
        "success": "#10b981",
        "warning": "#f59e0b",
        "error": "#ef4444",
    }
    
    for event in events[:15]:
        color = severity_colors.get(event.get('severity', 'info'), "#3b82f6")
        message = event.get('message', 'Event')
        time_str = format_timestamp(event['timestamp'])
        severity = event.get('severity', 'info')
        
        st.markdown(f"""<div style="display: flex; align-items: flex-start; gap: 12px; padding: 10px; background: {color}10; border-left: 3px solid {color}; border-radius: 0 6px 6px 0; margin-bottom: 8px;"> <div style="flex: 1;"> <div style="font-size: 13px; color: #f8fafc; margin-bottom: 4px;">{message}</div> <div style="font-size: 11px; color: #64748b;">{time_str}</div> </div> <div style="padding: 2px 8px; background: {color}20; border-radius: 4px; font-size: 10px; text-transform: uppercase; color: {color};">{severity}</div> </div>""", unsafe_allow_html=True)


def agent_drawer(agent: dict[str, Any]) -> None:
    """
    Render the agent detail drawer.
    
    Args:
        agent: Agent data dictionary
    """
    # Drawer styles
    st.markdown("""<style> .drawer-content { position: fixed; top: 0; right: 0; bottom: 0; width: 650px; max-width: 95vw; background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%); border-left: 1px solid rgba(148, 163, 184, 0.1); z-index: 1001; overflow-y: auto; padding: 24px; animation: slideIn 0.3s ease; } @keyframes slideIn { from { transform: translateX(100%); } to { transform: translateX(0); } } .drawer-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid rgba(148, 163, 184, 0.1); } .drawer-title { display: flex; align-items: center; gap: 16px; } .drawer-title h2 { margin: 0; font-size: 24px; font-weight: 600; color: #f8fafc; } .drawer-close { width: 36px; height: 36px; border-radius: 8px; background: rgba(148, 163, 184, 0.1); border: 1px solid rgba(148, 163, 184, 0.2); color: #94a3b8; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s ease; } .drawer-close:hover { background: rgba(239, 68, 68, 0.2); border-color: rgba(239, 68, 68, 0.3); color: #ef4444; } </style>""", unsafe_allow_html=True)
    
    # Header with close button
    col1, col2, col3 = st.columns([1, 8, 1])
    with col1:
        st.markdown(f"<div style='font-size: 48px;'>{agent['icon']}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"## {agent['name']}")
        st.markdown(f"*{agent['description']}*")
    with col3:
        if st.button("✕", key="close_drawer"):
            from src.utils.session import SessionState
            SessionState.close_drawer()
            st.rerun()
    
    st.markdown("---")
    
    # Current Mission Section
    st.markdown("### 🎯 Current Mission")
    mission = agent.get('mission', 'N/A')
    task = agent.get('current_task', 'N/A')
    progress = agent.get('progress', 0)
    decisions = agent.get('decisions', 0)
    
    st.markdown(f"""<div style="padding: 16px; background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(34, 211, 238, 0.1)); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 12px; margin-bottom: 20px;"> <div style="font-size: 16px; color: #f8fafc; margin-bottom: 12px;">{mission}</div> <div style="display: flex; gap: 16px;"> <div><div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Current Task</div><div style="font-size: 13px; color: #94a3b8;">{task}</div></div> <div><div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Progress</div><div style="font-size: 13px; color: #6366f1; font-weight: 600;">{progress:.1f}%</div></div> <div><div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Decisions</div><div style="font-size: 13px; color: #94a3b8;">{decisions}</div></div> </div> </div>""", unsafe_allow_html=True)
    
    # Agent DNA
    render_dna_section(agent)
    st.markdown("")
    
    # Current Prompt
    prompt = agent.get('current_prompt', 'N/A')
    st.markdown("### 💬 Current Prompt")
    st.markdown(f"""<div style="padding: 14px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; font-size: 13px; color: #c4b5fd; font-family: 'JetBrains Mono', monospace; line-height: 1.6; margin-bottom: 20px;">{prompt}</div>""", unsafe_allow_html=True)
    
    # Capabilities
    render_capabilities_section(agent['capabilities'])
    st.markdown("")
    
    # Tools
    render_tools_section(agent['tools'])
    st.markdown("")
    
    # Context
    render_current_context_section(agent['current_context'])
    st.markdown("")
    
    # Memory
    render_memory_section(agent['current_memory'])
    st.markdown("")
    
    # Health History Chart
    render_health_history_chart(agent['health_history'])
    st.markdown("")
    
    # Execution History
    render_execution_history(agent['execution_history'])
    st.markdown("")
    
    # Recent Events
    render_recent_events(agent['recent_events'])
    
    # Stats row at bottom
    st.markdown("---")
    cpu = agent.get('cpu', 0)
    mem = agent.get('memory', 0)
    retries = agent.get('retries', 0)
    failures = agent.get('failures', 0)
    
    cols = st.columns(4)
    with cols[0]:
        st.metric("CPU", f"{cpu:.1f}%")
    with cols[1]:
        st.metric("Memory", f"{mem:.1f}%")
    with cols[2]:
        st.metric("Retries", retries)
    with cols[3]:
        st.metric("Failures", failures)
