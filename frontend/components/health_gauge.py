"""HealthGauge Component - Health metrics visualization."""

from typing import Any
import streamlit as st
import plotly.graph_objects as go


def get_health_color(health: float) -> str:
    """Get color based on health value."""
    if health >= 0.9:
        return "#10b981"  # Green
    elif health >= 0.75:
        return "#22d3ee"  # Cyan
    elif health >= 0.5:
        return "#f59e0b"  # Yellow
    else:
        return "#ef4444"  # Red


def render_circular_gauge(
    value: float,
    max_value: float,
    label: str,
    size: str = "medium"
) -> None:
    """Render a circular gauge indicator."""
    percentage = min(100, (value / max_value) * 100) if max_value > 0 else 0
    color = get_health_color(percentage / 100)
    
    size_config = {
        "small": {"size": 100, "font_size": 18},
        "medium": {"size": 150, "font_size": 24},
        "large": {"size": 200, "font_size": 32},
    }
    config = size_config.get(size, size_config["medium"])
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={
            'suffix': '%' if isinstance(value, float) else '',
            'font': {'size': config['font_size'], 'color': '#f8fafc'},
        },
        gauge={
            'axis': {
                'range': [0, max_value],
                'tickwidth': 1,
                'tickcolor': '#64748b',
                'showticklabels': False,
                'ticklen': 5,
            },
            'bar': {
                'color': color,
                'thickness': 0.2,
                'line': {'color': '#fff', 'width': 2},
            },
            'bgcolor': 'rgba(51, 65, 85, 0.5)',
            'borderwidth': 0,
            'bordercolor': 'rgba(148, 163, 184, 0.1)',
            'steps': [
                {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.2)'},
                {'range': [50, 75], 'color': 'rgba(245, 158, 11, 0.2)'},
                {'range': [75, 90], 'color': 'rgba(34, 211, 238, 0.2)'},
                {'range': [90, 100], 'color': 'rgba(16, 185, 129, 0.2)'},
            ],
            'threshold': {
                'line': {'color': color, 'width': 4},
                'thickness': 0.85,
                'value': max_value * 0.9,
            },
        },
        domain={'x': [0, 1], 'y': [0, 1]},
    ))
    
    fig.update_layout(
        height=config['size'],
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
    )
    
    st.plotly_chart(fig, use_container_width=True, key="health_gauge")
    
    st.markdown(f"""<div style="text-align: center; margin-top: -15px;"> <span style=" font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; ">{label}</span> </div>""", unsafe_allow_html=True)


def render_health_bar(health: float, label: str = "Health") -> None:
    """Render a horizontal health bar."""
    color = get_health_color(health)
    
    st.markdown(f"""<div style="margin: 12px 0;"> <div style=" display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; "> <span style="font-size: 12px; color: #94a3b8;">{label}</span> <span style=" font-size: 14px; font-weight: 600; font-family: 'JetBrains Mono', monospace; color: {color}; ">{health:.1%}</span> </div> <div style=" width: 100%; height: 10px; background: rgba(51, 65, 85, 0.5); border-radius: 5px; overflow: hidden; position: relative; "> <div style=" width: {health * 100}%; height: 100%; background: linear-gradient(90deg, {color}, {color}cc); border-radius: 5px; transition: width 0.5s ease; "></div> <!-- Threshold markers --> <div style=" position: absolute; left: 50%; top: 0; bottom: 0; width: 1px; background: rgba(148, 163, 184, 0.3); "></div> <div style=" position: absolute; left: 75%; top: 0; bottom: 0; width: 1px; background: rgba(148, 163, 184, 0.3); "></div> <div style=" position: absolute; left: 90%; top: 0; bottom: 0; width: 1px; background: rgba(148, 163, 184, 0.3); "></div> </div> <div style=" display: flex; justify-content: space-between; margin-top: 4px; padding: 0 2px; "> <span style="font-size: 9px; color: #64748b;">0%</span> <span style="font-size: 9px; color: #64748b;">50%</span> <span style="font-size: 9px; color: #64748b;">75%</span> <span style="font-size: 9px; color: #64748b;">90%</span> <span style="font-size: 9px; color: #64748b;">100%</span> </div> </div>""", unsafe_allow_html=True)


def render_multi_metric_gauges(metrics: dict[str, float], title: str) -> None:
    """Render multiple metrics as small gauges in a row."""
    st.markdown(f"#### {title}")
    
    cols = st.columns(len(metrics))
    
    for i, (metric, value) in enumerate(metrics.items()):
        with cols[i]:
            color = get_health_color(value)
            
            st.markdown(f"""<div style=" padding: 16px; background: rgba(30, 41, 59, 0.6); border: 1px solid {color}30; border-radius: 12px; text-align: center; "> <div style=" font-size: 28px; font-weight: 700; font-family: 'JetBrains Mono', monospace; color: {color}; margin-bottom: 6px; "> {value:.1f}{'%' if isinstance(value, float) else ''} </div> <div style=" font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; "> {metric} </div> </div>""", unsafe_allow_html=True)


def render_health_dashboard(health_data: dict[str, Any]) -> None:
    """Render comprehensive health dashboard."""
    st.markdown("### 💚 Mission Health")
    
    # Main health indicator
    overall = health_data.get("overall", 0.95)
    color = get_health_color(overall)
    
    st.markdown(f"""<div style=" padding: 24px; background: linear-gradient(135deg, {color}15, {color}05); border: 1px solid {color}40; border-radius: 16px; text-align: center; margin-bottom: 20px; "> <div style=" font-size: 64px; font-weight: 700; font-family: 'JetBrains Mono', monospace; color: {color}; margin-bottom: 8px; "> {overall:.1%} </div> <div style=" font-size: 14px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; "> Overall Health Score </div> <div style=" display: flex; justify-content: center; gap: 20px; margin-top: 16px; "> <div> <div style="font-size: 11px; color: #64748b;">Status</div> <div style="font-size: 14px; font-weight: 600; color: {color};"> {'Healthy' if overall >= 0.9 else 'Good' if overall >= 0.75 else 'Warning'} </div> </div> <div> <div style="font-size: 11px; color: #64748b;">Uptime</div> <div style="font-size: 14px; font-weight: 600; color: #f8fafc;"> {health_data.get('uptime', 99.9):.1f}% </div> </div> </div> </div>""", unsafe_allow_html=True)
    
    # Health metrics grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Resource Health")
        
        cpu_health = health_data.get("cpu_health", 0.9)
        memory_health = health_data.get("memory_health", 0.9)
        
        render_health_bar(cpu_health, "CPU Health")
        render_health_bar(memory_health, "Memory Health")
    
    with col2:
        st.markdown("#### Reliability")
        
        failure_rate = health_data.get("failure_rate", 0.02)
        retry_rate = health_data.get("retry_rate", 0.05)
        confidence = health_data.get("confidence_avg", 0.9)
        
        st.markdown(f"""<div style="margin-bottom: 12px;"> <div style=" display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; "> <span style="font-size: 12px; color: #94a3b8;">Failure Rate</span> <span style=" font-size: 14px; font-weight: 600; font-family: 'JetBrains Mono', monospace; color: {'#ef4444' if failure_rate > 0.05 else '#10b981'}; ">{(failure_rate * 100):.2f}%</span> </div> </div>""", unsafe_allow_html=True)
        
        st.markdown(f"""<div style="margin-bottom: 12px;"> <div style=" display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; "> <span style="font-size: 12px; color: #94a3b8;">Retry Rate</span> <span style=" font-size: 14px; font-weight: 600; font-family: 'JetBrains Mono', monospace; color: {'#f59e0b' if retry_rate > 0.05 else '#10b981'}; ">{(retry_rate * 100):.2f}%</span> </div> </div>""", unsafe_allow_html=True)
        
        st.markdown(f"""<div style="margin-bottom: 12px;"> <div style=" display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; "> <span style="font-size: 12px; color: #94a3b8;">Avg Confidence</span> <span style=" font-size: 14px; font-weight: 600; font-family: 'JetBrains Mono', monospace; color: #6366f1; ">{confidence:.1%}</span> </div> </div>""", unsafe_allow_html=True)
    
    # Warnings section
    warnings = health_data.get("warning_count", 0)
    if warnings > 0:
        st.markdown(f"""<div style=" padding: 12px; background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 8px; display: flex; align-items: center; gap: 12px; "> <span style="font-size: 20px;">⚠️</span> <div> <div style="font-size: 14px; color: #f59e0b; font-weight: 600;"> {warnings} Active Warning{'s' if warnings > 1 else ''} </div> <div style="font-size: 12px; color: #64748b;"> Review system logs for details </div> </div> </div>""", unsafe_allow_html=True)
