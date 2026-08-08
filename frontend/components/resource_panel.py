"""ResourcePanel Component - System resource monitoring dashboard."""

from typing import Any
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def render_metric_gauge(
    value: float,
    max_value: float,
    label: str,
    color: str,
    unit: str = "%"
) -> None:
    """Render a circular gauge metric."""
    percentage = min(100, (value / max_value) * 100) if max_value > 0 else 0
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={
            'suffix': unit,
            'font': {'size': 24, 'color': '#f8fafc'},
        },
        gauge={
            'axis': {
                'range': [0, max_value],
                'tickwidth': 0,
                'tickcolor': 'transparent',
                'showticklabels': False,
            },
            'bar': {'color': color, 'thickness': 0.15},
            'bgcolor': 'rgba(51, 65, 85, 0.5)',
            'borderwidth': 0,
            'bordercolor': 'rgba(148, 163, 184, 0.1)',
            'threshold': {
                'line': {'color': '#ef4444', 'width': 2},
                'thickness': 0.75,
                'value': max_value * 0.9,
            },
        },
        domain={'x': [0, 1], 'y': [0, 1]},
    ))
    
    fig.update_layout(
        height=140,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
    )
    
    st.plotly_chart(fig, width='stretch', key="resource_cpu_chart")
    st.markdown(f"""<div style="text-align: center; margin-top: -10px;"> <span style=" font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; ">{label}</span> </div>""", unsafe_allow_html=True)


def render_linear_progress(
    value: float,
    max_value: float,
    label: str,
    color: str,
    show_value: bool = True
) -> None:
    """Render a linear progress bar with label."""
    percentage = min(100, (value / max_value) * 100) if max_value > 0 else 0
    
    st.markdown(f"""<div style="margin-bottom: 16px;"> <div style=" display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; "> <span style="font-size: 12px; color: #94a3b8;">{label}</span> <span style=" font-size: 14px; font-weight: 600; font-family: 'JetBrains Mono', monospace; color: {color}; ">{value:.1f}{'%' if isinstance(value, float) else ''}</span> </div> <div style=" width: 100%; height: 8px; background: rgba(51, 65, 85, 0.5); border-radius: 4px; overflow: hidden; "> <div style=" width: {percentage}%; height: 100%; background: linear-gradient(90deg, {color}, {color}cc); border-radius: 4px; transition: width 0.5s ease; position: relative; "> <div style=" position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent); animation: shimmer 2s infinite; "></div> </div> </div> </div>""", unsafe_allow_html=True)


def render_token_usage_chart(token_data: dict[str, int]) -> None:
    """Render token usage as a bar chart."""
    df = pd.DataFrame({
        'Type': list(token_data.keys()),
        'Tokens': list(token_data.values()),
    })
    
    fig = px.bar(
        df,
        x='Type',
        y='Tokens',
        color='Tokens',
        color_continuous_scale='Viridis',
        text_auto='~s',
    )
    
    fig.update_layout(
        height=180,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        xaxis=dict(
            showgrid=False,
            color='#64748b',
            title=None,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.1)',
            color='#64748b',
            title=None,
        ),
        coloraxis_showscale=False,
    )
    
    fig.update_traces(
        textposition='outside',
        textfont=dict(color='#94a3b8'),
        marker=dict(line=dict(color='transparent')),
    )
    
    st.plotly_chart(fig, width='stretch', key="resource_memory_chart")


def render_latency_chart(latency_data: dict[str, float]) -> None:
    """Render latency metrics as a bar chart."""
    df = pd.DataFrame({
        'Metric': list(latency_data.keys()),
        'Latency (ms)': list(latency_data.values()),
    })
    
    colors = ['#10b981', '#f59e0b', '#ef4444']
    
    fig = go.Figure(go.Bar(
        x=df['Metric'],
        y=df['Latency (ms)'],
        marker_color=colors,
        text=df['Latency (ms)'],
        textposition='outside',
        textfont=dict(color='#94a3b8'),
    ))
    
    fig.update_layout(
        height=180,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        xaxis=dict(
            showgrid=False,
            color='#64748b',
            title=None,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.1)',
            color='#64748b',
            title=None,
        ),
    )
    
    st.plotly_chart(fig, width='stretch', key="resource_disk_chart")


def render_queue_chart(queue_data: dict[str, int]) -> None:
    """Render queue status as a visual representation."""
    max_size = queue_data.get('max_size', 100)
    waiting = queue_data.get('waiting', 0)
    processing = queue_data.get('processing', 0)
    
    # Create stacked bar
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=['Queue'],
        y=[waiting],
        name='Waiting',
        marker_color='#f59e0b',
        text=waiting,
        textposition='inside',
        textfont=dict(color='#000'),
    ))
    
    fig.add_trace(go.Bar(
        x=['Queue'],
        y=[processing],
        name='Processing',
        marker_color='#10b981',
        text=processing,
        textposition='inside',
        textfont=dict(color='#000'),
    ))
    
    fig.add_trace(go.Bar(
        x=['Queue'],
        y=[max_size - waiting - processing],
        name='Available',
        marker_color='rgba(51, 65, 85, 0.5)',
    ))
    
    fig.update_layout(
        height=120,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        barmode='stack',
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(
            showgrid=False,
            title=None,
            range=[0, max_size],
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(color='#94a3b8', size=10),
            bgcolor='rgba(0,0,0,0)',
        ),
    )
    
    st.plotly_chart(fig, width='stretch', key="resource_network_chart")


def resource_panel(metrics: dict[str, Any]) -> None:
    """
    Render the resource monitoring panel.
    
    Args:
        metrics: System metrics dictionary
    """
    st.markdown("### 📊 Resource Dashboard")
    
    # Main resource gauges
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""<div style=" padding: 16px; background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 12px; text-align: center; "> <div style="font-size: 32px; font-weight: 700; font-family: 'JetBrains Mono', monospace; color: #6366f1;"> {}% </div> <div style="font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px;"> Total CPU </div> </div>""".format(metrics['total_cpu']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""<div style=" padding: 16px; background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(34, 211, 238, 0.2); border-radius: 12px; text-align: center; "> <div style="font-size: 32px; font-weight: 700; font-family: 'JetBrains Mono', monospace; color: #22d3ee;"> {}% </div> <div style="font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px;"> Total Memory </div> </div>""".format(metrics['total_memory']), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""<div style=" padding: 16px; background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(236, 72, 153, 0.2); border-radius: 12px; text-align: center; "> <div style="font-size: 32px; font-weight: 700; font-family: 'JetBrains Mono', monospace; color: #ec4899;"> {}% </div> <div style="font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px;"> Total GPU </div> </div>""".format(metrics['total_gpu']), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""<div style=" padding: 16px; background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 12px; text-align: center; "> <div style="font-size: 32px; font-weight: 700; font-family: 'JetBrains Mono', monospace; color: #10b981;"> {:,} </div> <div style="font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px;"> Requests </div> </div>""".format(metrics['requests']['total']), unsafe_allow_html=True)
    
    st.markdown("")  # Spacer
    
    # Token Usage Section
    st.markdown("""<div style=" padding: 12px 16px; background: linear-gradient(90deg, rgba(99, 102, 241, 0.1), rgba(34, 211, 238, 0.1)); border-radius: 8px; margin-bottom: 12px; "> <span style="font-size: 13px; font-weight: 600; color: #f8fafc;">💎 Token Usage</span> </div>""", unsafe_allow_html=True)
    render_token_usage_chart(metrics['token_usage'])
    
    # Latency Section
    st.markdown("""<div style=" padding: 12px 16px; background: linear-gradient(90deg, rgba(245, 158, 11, 0.1), rgba(239, 68, 68, 0.1)); border-radius: 8px; margin-bottom: 12px; margin-top: 16px; "> <span style="font-size: 13px; font-weight: 600; color: #f8fafc;">⏱️ Latency</span> </div>""", unsafe_allow_html=True)
    render_latency_chart(metrics['latency'])
    
    # Queue Section
    st.markdown("""<div style=" padding: 12px 16px; background: linear-gradient(90deg, rgba(16, 185, 129, 0.1), rgba(59, 130, 246, 0.1)); border-radius: 8px; margin-bottom: 12px; margin-top: 16px; "> <span style="font-size: 13px; font-weight: 600; color: #f8fafc;">📬 Queue Status</span> </div>""", unsafe_allow_html=True)
    render_queue_chart(metrics['queue'])
    
    # Detailed metrics
    with st.expander("📈 Detailed Metrics"):
        cols = st.columns(3)
        with cols[0]:
            st.metric("Pending Requests", metrics['requests']['pending'])
        with cols[1]:
            st.metric("Completed", metrics['requests']['completed'])
        with cols[2]:
            st.metric("Success Rate", f"{(metrics['requests']['completed']/max(1,metrics['requests']['total'])*100):.1f}%")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            render_linear_progress(
                metrics['total_cpu'], 100,
                "CPU Utilization", "#6366f1"
            )
            render_linear_progress(
                metrics['total_memory'], 100,
                "Memory Utilization", "#22d3ee"
            )
        with col2:
            render_linear_progress(
                metrics['total_gpu'], 100,
                "GPU Utilization", "#ec4899"
            )
