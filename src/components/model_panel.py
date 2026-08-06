"""ModelPanel Component - AI Model routing and usage visualization."""

from typing import Any
import streamlit as st
import plotly.graph_objects as go


MODEL_COLORS = {
    "GPT-4": "#10a37f",
    "GPT-3.5": "#10a37f",
    "Claude": "#d4a373",
    "Gemini": "#4285f4",
    "DeepSeek": "#0066cc",
    "Qwen": "#ff6b6b",
}

MODEL_ICONS = {
    "GPT-4": "🤖",
    "GPT-3.5": "🔧",
    "Claude": "🧠",
    "Gemini": "✨",
    "DeepSeek": "🔮",
    "Qwen": "🌟",
}


def render_model_card(model: str, requests: int, total_requests: int) -> None:
    """Render individual model card."""
    percentage = (requests / total_requests * 100) if total_requests > 0 else 0
    color = MODEL_COLORS.get(model, "#6366f1")
    icon = MODEL_ICONS.get(model, "🤖")
    
    st.markdown(f"""
    <div style="
        padding: 14px;
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid {color}30;
        border-radius: 10px;
        margin-bottom: 10px;
        transition: all 0.3s ease;
    ">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 24px;">{icon}</span>
                <span style="font-size: 14px; font-weight: 600; color: #f8fafc;">{model}</span>
            </div>
            <div style="
                padding: 4px 10px;
                background: {color}20;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                font-family: 'JetBrains Mono', monospace;
                color: {color};
            ">
                {requests:,}
            </div>
        </div>
        <div style="
            width: 100%;
            height: 6px;
            background: rgba(51, 65, 85, 0.5);
            border-radius: 3px;
            overflow: hidden;
        ">
            <div style="
                width: {percentage}%;
                height: 100%;
                background: linear-gradient(90deg, {color}, {color}cc);
                border-radius: 3px;
                transition: width 0.5s ease;
            "></div>
        </div>
        <div style="
            display: flex;
            justify-content: space-between;
            margin-top: 6px;
        ">
            <span style="font-size: 10px; color: #64748b;">{percentage:.1f}% of requests</span>
            <span style="font-size: 10px; color: {color};">Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_model_pie_chart(model_usage: dict[str, int]) -> None:
    """Render model usage as pie chart."""
    models = list(model_usage.keys())
    values = list(model_usage.values())
    colors = [MODEL_COLORS.get(m, "#6366f1") for m in models]
    
    fig = go.Figure(go.Pie(
        labels=models,
        values=values,
        hole=0.6,
        marker=dict(colors=colors),
        textinfo='percent',
        textposition='outside',
        textfont=dict(color='#94a3b8', size=11),
        hovertemplate='<b>%{label}</b><br>%{percent}<extra></extra>',
    ))
    
    fig.update_layout(
        height=200,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='transparent',
        showlegend=False,
        annotations=[
            dict(
                text='<b>Models</b>',
                x=0.5,
                y=0.5,
                font_size=14,
                font_color='#f8fafc',
                showarrow=False,
            )
        ],
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_routing_visualization(model_usage: dict[str, int]) -> None:
    """Render model routing as a visual flow."""
    total = sum(model_usage.values())
    
    # Create a horizontal flow showing model distribution
    st.markdown("""
    <div style="
        display: flex;
        align-items: center;
        justify-content: space-around;
        padding: 20px 0;
    ">
    """, unsafe_allow_html=True)
    
    # Central hub
    st.markdown("""
    <div style="
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 30px rgba(99, 102, 241, 0.4);
    ">
        <span style="font-size: 24px;">🎛️</span>
        <span style="font-size: 10px; color: #fff; font-weight: 600;">ROUTER</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Arrow
    st.markdown("""
    <div style="
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #6366f1, #22d3ee);
        position: relative;
    ">
        <div style="
            position: absolute;
            right: -8px;
            top: -4px;
            border-left: 10px solid #22d3ee;
            border-top: 6px solid transparent;
            border-bottom: 6px solid transparent;
        "></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Model badges
    cols = st.columns(len(model_usage))
    for i, (model, count) in enumerate(sorted(model_usage.items(), key=lambda x: -x[1])):
        with cols[i]:
            percentage = (count / total * 100) if total > 0 else 0
            color = MODEL_COLORS.get(model, "#6366f1")
            
            st.markdown(f"""
            <div style="
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 6px;
            ">
                <div style="
                    width: 50px;
                    height: 50px;
                    border-radius: 12px;
                    background: {color}20;
                    border: 2px solid {color}50;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 20px;
                ">
                    {MODEL_ICONS.get(model, "🤖")}
                </div>
                <span style="
                    font-size: 11px;
                    font-weight: 600;
                    color: #f8fafc;
                ">{model}</span>
                <span style="
                    font-size: 10px;
                    color: {color};
                    font-family: 'JetBrains Mono', monospace;
                ">{percentage:.0f}%</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def model_panel(model_usage: dict[str, int]) -> None:
    """
    Render the AI Model Panel.
    
    Args:
        model_usage: Dictionary mapping model names to request counts
    """
    total_requests = sum(model_usage.values())
    
    st.markdown("### 🤖 AI Model Panel")
    
    # Summary cards
    cols = st.columns(3)
    
    # Primary model (highest usage)
    primary_model = max(model_usage.items(), key=lambda x: x[1])
    primary_color = MODEL_COLORS.get(primary_model[0], "#6366f1")
    
    with cols[0]:
        st.markdown(f"""
        <div style="
            padding: 14px;
            background: linear-gradient(135deg, {primary_color}20, {primary_color}10);
            border: 1px solid {primary_color}40;
            border-radius: 12px;
            text-align: center;
        ">
            <div style="font-size: 11px; color: #64748b; text-transform: uppercase; margin-bottom: 8px;">
                Primary Model
            </div>
            <div style="font-size: 20px; font-weight: 700; color: {primary_color}; margin-bottom: 4px;">
                {MODEL_ICONS.get(primary_model[0], "🤖")} {primary_model[0]}
            </div>
            <div style="font-size: 12px; color: #94a3b8;">
                {primary_model[1]:,} requests
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown(f"""
        <div style="
            padding: 14px;
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-radius: 12px;
            text-align: center;
        ">
            <div style="font-size: 11px; color: #64748b; text-transform: uppercase; margin-bottom: 8px;">
                Total Requests
            </div>
            <div style="font-size: 20px; font-weight: 700; color: #f8fafc; margin-bottom: 4px;">
                {total_requests:,}
            </div>
            <div style="font-size: 12px; color: #94a3b8;">
                Across {len(model_usage)} models
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        avg_requests = total_requests // len(model_usage) if model_usage else 0
        st.markdown(f"""
        <div style="
            padding: 14px;
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-radius: 12px;
            text-align: center;
        ">
            <div style="font-size: 11px; color: #64748b; text-transform: uppercase; margin-bottom: 8px;">
                Avg per Model
            </div>
            <div style="font-size: 20px; font-weight: 700; color: #22d3ee; margin-bottom: 4px;">
                {avg_requests:,}
            </div>
            <div style="font-size: 12px; color: #94a3b8;">
                requests
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")  # Spacer
    
    # Routing visualization
    with st.expander("🔀 Model Routing Flow", expanded=False):
        render_routing_visualization(model_usage)
    
    # Model cards
    st.markdown("#### Model Distribution")
    sorted_models = sorted(model_usage.items(), key=lambda x: -x[1])
    
    for model, count in sorted_models:
        render_model_card(model, count, total_requests)
    
    # Pie chart
    with st.expander("📊 Usage Distribution", expanded=False):
        render_model_pie_chart(model_usage)
