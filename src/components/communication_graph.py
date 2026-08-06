"""CommunicationGraph Component - Animated agent communication visualization."""

from typing import Any
import streamlit as st
import plotly.graph_objects as go
import random


def get_agent_icon(agent_id: str, agents: list[dict[str, Any]]) -> str:
    """Get agent icon by ID."""
    for agent in agents:
        if agent['id'] == agent_id:
            return agent['icon']
    return "🤖"


def get_agent_name(agent_id: str, agents: list[dict[str, Any]]) -> str:
    """Get agent name by ID."""
    for agent in agents:
        if agent['id'] == agent_id:
            return agent['name']
    return agent_id


def render_communication_graph(
    pipeline: list[tuple[str, str]],
    agents: list[dict[str, Any]],
    animating: bool = True
) -> None:
    """
    Render the agent communication pipeline graph.
    
    Args:
        pipeline: List of (source_id, target_id) tuples
        agents: List of agent dictionaries
    """
    if not pipeline:
        st.info("No active communication pipeline")
        return
    
    # Calculate positions for nodes in vertical flow
    n_nodes = len(set([p[0] for p in pipeline] + [p[1] for p in pipeline]))
    
    # Create node positions
    nodes = list(dict.fromkeys([p[0] for p in pipeline] + [p[1] for p in pipeline]))
    
    # Position nodes vertically
    node_positions = {}
    y_start = 0.9
    y_step = 0.8 / (len(nodes) - 1) if len(nodes) > 1 else 0
    
    for i, node_id in enumerate(nodes):
        node_positions[node_id] = (0.5, y_start - i * y_step)
    
    # Create figure
    fig = go.Figure()
    
    # Add edges (connections)
    edge_animation_frames = []
    
    for i, (source, target) in enumerate(pipeline):
        x0, y0 = node_positions[source]
        x1, y1 = node_positions[target]
        
        # Calculate control points for curved line
        mid_y = (y0 + y1) / 2
        
        # Add the edge line
        fig.add_trace(go.Scatter(
            x=[x0, x0, x1, x1],
            y=[y0, mid_y, mid_y, y1],
            mode='lines',
            line=dict(
                color='rgba(99, 102, 241, 0.3)',
                width=3,
            ),
            hoverinfo='skip',
            showlegend=False,
        ))
        
        # Add animated particle along the edge
        for step in range(20):
            t = step / 19
            px = x0 * (1-t)**3 + x0 * 3*(1-t)**2*t + x1 * 3*(1-t)*t**2 + x1 * t**3
            py = y0 * (1-t)**3 + mid_y * 3*(1-t)**2*t + mid_y * 3*(1-t)*t**2 + y1 * t**3
            
            visible = [False] * len(pipeline)
            visible[i] = True
            
            frame_data = go.Scatter(
                x=[px],
                y=[py],
                mode='markers',
                marker=dict(
                    size=12,
                    color='#22d3ee',
                    symbol='circle',
                    line=dict(color='#0ea5e9', width=2),
                ),
                showlegend=False,
                hovertemplate=f"{source} → {target}<extra></extra>",
            )
            
            edge_animation_frames.append(
                go.Frame(
                    data=[frame_data],
                    name=f"step_{step}",
                    traces=[len(pipeline) + i],
                )
            )
    
    # Add message particles
    for i, (source, target) in enumerate(pipeline):
        fig.add_trace(go.Scatter(
            x=[0],
            y=[0],
            mode='markers',
            marker=dict(
                size=12,
                color='#22d3ee',
                symbol='circle',
            ),
            showlegend=False,
            visible=False,
            name=f"particle_{i}",
        ))
    
    # Add node markers with labels
    for node_id in nodes:
        x, y = node_positions[node_id]
        icon = get_agent_icon(node_id, agents)
        name = get_agent_name(node_id, agents)
        
        # Node background
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode='markers+text',
            marker=dict(
                size=60,
                color='rgba(30, 41, 59, 0.9)',
                line=dict(color='#6366f1', width=2),
                symbol='circle',
            ),
            text=[icon],
            textposition='middle center',
            textfont=dict(size=24),
            hovertemplate=f"<b>{name}</b><extra></extra>",
            showlegend=False,
        ))
        
        # Node label
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y - 0.08],
            mode='text',
            text=[name.replace(' Agent', '')],
            textposition='top center',
            textfont=dict(
                size=10,
                color='#94a3b8',
            ),
            hovertemplate=f"<b>{name}</b><extra></extra>",
            showlegend=False,
        ))
    
    # Add animated message indicators between nodes
    if animating:
        for i, (source, target) in enumerate(pipeline):
            x0, y0 = node_positions[source]
            x1, y1 = node_positions[target]
            
            # Add pulsing message indicator
            for step in range(10):
                t = step / 9
                msg_x = x0 + (x1 - x0) * t
                msg_y = y0 + (y1 - y0) * t
                
                fig.add_trace(go.Scatter(
                    x=[msg_x],
                    y=[msg_y],
                    mode='markers',
                    marker=dict(
                        size=8 + step * 0.5,
                        color=f'rgba(34, 211, 238, {1 - step/15})',
                        symbol='circle',
                    ),
                    showlegend=False,
                    visible=False,
                    name=f"msg_{i}_{step}",
                ))
    
    # Add legend for message flow
    fig.add_trace(go.Scatter(
        x=[0.85],
        y=[0.95],
        mode='markers',
        marker=dict(size=10, color='#22d3ee'),
        showlegend=True,
        name='Message Flow',
    ))
    
    # Update layout
    fig.update_layout(
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='#94a3b8'),
            bgcolor='rgba(0,0,0,0)',
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[0, 1],
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[0, 1],
            scaleanchor='x',
            scaleratio=1,
        ),
        hoverlabel=dict(
            bgcolor='#1e293b',
            bordercolor='#6366f1',
            font=dict(color='#f8fafc'),
        ),
    )
    
    # Add animation
    if animating:
        steps = []
        for i in range(20):
            step = dict(
                method='update',
                args=[{'visible': [False] * len(fig.data)}],
                label=str(i),
            )
            
            # Show all edges
            for j in range(len(pipeline)):
                step['args'][0]['visible'][j] = True
            
            # Show current particle position for all edges
            for j in range(len(pipeline)):
                particle_idx = len(pipeline) + j
                if particle_idx < len(fig.data):
                    step['args'][0]['visible'][particle_idx] = True
            
            # Show nodes
            for j in range(len(nodes) * 2):
                node_start = len(pipeline) * 2
                if node_start + j < len(fig.data):
                    step['args'][0]['visible'][node_start + j] = True
            
            steps.append(step)
        
        sliders = [dict(
            active=0,
            currentvalue=dict(
                prefix="Flow: ",
                visible=True,
                font=dict(color='#94a3b8'),
            ),
            pad=dict(t=20),
            steps=steps,
            x=0.1,
            len=0.8,
            xanchor='left',
            y=0,
            yanchor='top',
            bgcolor='#1e293b',
            bordercolor='#6366f1',
            tickcolor='#6366f1',
            font=dict(color='#94a3b8'),
        )]
        
        fig.update_layout(
            sliders=sliders,
            updatemenus=[
                dict(
                    type='buttons',
                    showactive=False,
                    y=1.1,
                    x=0.1,
                    xanchor='right',
                    bgcolor='#1e293b',
                    bordercolor='#6366f1',
                    font=dict(color='#94a3b8'),
                    buttons=[
                        dict(
                            label='▶ Play',
                            method='animate',
                            args=[
                                None,
                                dict(
                                    frame=dict(duration=100, redraw=True),
                                    fromcurrent=True,
                                    transition=dict(duration=50),
                                )
                            ],
                        ),
                        dict(
                            label='⏸ Pause',
                            method='animate',
                            args=[
                                [None],
                                dict(
                                    frame=dict(duration=0, redraw=False),
                                    mode='immediate',
                                    transition=dict(duration=0),
                                )
                            ],
                        ),
                    ],
                ),
            ],
        )
    
    st.plotly_chart(fig, use_container_width=True)


def render_simple_communication_flow(
    pipeline: list[tuple[str, str]],
    agents: list[dict[str, Any]]
) -> None:
    """Render a simplified vertical flow diagram."""
    st.markdown("""
    <style>
    .comm-flow {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0;
        padding: 20px 0;
    }
    
    .comm-node {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 2px solid #6366f1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
    }
    
    .comm-node:hover {
        transform: scale(1.1);
        border-color: #22d3ee;
        box-shadow: 0 0 20px rgba(34, 211, 238, 0.4);
    }
    
    .comm-node.active {
        border-color: #10b981;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.5);
    }
    
    .comm-node-label {
        font-size: 9px;
        color: #94a3b8;
        text-align: center;
        margin-top: 2px;
        max-width: 80px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    
    .comm-connector {
        width: 3px;
        height: 30px;
        background: linear-gradient(180deg, #6366f1, #22d3ee);
        position: relative;
        overflow: hidden;
    }
    
    .comm-connector::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 10px;
        background: linear-gradient(180deg, #22d3ee, transparent);
        animation: flowDown 1.5s infinite;
    }
    
    @keyframes flowDown {
        0% { top: -10px; opacity: 1; }
        100% { top: 100%; opacity: 0; }
    }
    
    .comm-message {
        position: absolute;
        left: 80px;
        background: rgba(34, 211, 238, 0.2);
        border: 1px solid rgba(34, 211, 238, 0.4);
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 10px;
        color: #22d3ee;
        white-space: nowrap;
        animation: messageFloat 3s infinite;
    }
    
    @keyframes messageFloat {
        0%, 100% { opacity: 0.7; transform: translateX(0); }
        50% { opacity: 1; transform: translateX(5px); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Build flow HTML
    nodes = list(dict.fromkeys([p[0] for p in pipeline] + [p[1] for p in pipeline]))
    
    flow_html = '<div class="comm-flow">'
    
    for i, node_id in enumerate(nodes):
        agent = next((a for a in agents if a['id'] == node_id), None)
        if not agent:
            continue
            
        icon = agent['icon']
        name = agent['name'].replace(' Agent', '').replace(' Intelligence', '')
        active_class = 'active' if agent['status'].value == 'running' else ''
        
        flow_html += f'''
        <div class="comm-node {active_class}" title="{agent['name']}">
            <span>{icon}</span>
            <span class="comm-node-label">{name}</span>
        </div>
        '''
        
        if i < len(nodes) - 1:
            flow_html += '<div class="comm-connector"></div>'
    
    flow_html += '</div>'
    
    st.markdown(flow_html, unsafe_allow_html=True)
