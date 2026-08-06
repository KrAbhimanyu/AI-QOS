"""LeftSidebar Component - Agent category navigation."""

from typing import Any
import streamlit as st


CATEGORY_CONFIG = {
    "Intelligence": {
        "icon": "🧠",
        "color": "#8b5cf6",
        "description": "Analysis & Processing",
    },
    "Testing": {
        "icon": "🧪",
        "color": "#3b82f6",
        "description": "Validation & Verification",
    },
    "Documentation": {
        "icon": "📝",
        "color": "#10b981",
        "description": "Documentation Generation",
    },
    "Infrastructure": {
        "icon": "🏗️",
        "color": "#f59e0b",
        "description": "System Management",
    },
    "Learning": {
        "icon": "📚",
        "color": "#ec4899",
        "description": "Continuous Improvement",
    },
    "Security": {
        "icon": "🛡️",
        "color": "#ef4444",
        "description": "Security & Compliance",
    },
    "Support": {
        "icon": "🔧",
        "color": "#22d3ee",
        "description": "Help & Maintenance",
    },
}


def render_category_item(
    category: str,
    agent_count: int,
    is_selected: bool,
    key: str
) -> None:
    """Render a single category item."""
    config = CATEGORY_CONFIG.get(category, CATEGORY_CONFIG["Intelligence"])
    color = config["color"]
    
    bg_style = f"background: linear-gradient(135deg, {color}20, {color}10);" if is_selected else ""
    border_style = f"border-color: {color}50;" if is_selected else ""
    
    st.markdown(f"""
    <div style="
        padding: 14px 16px;
        {bg_style}
        border: 1px solid {border_style if is_selected else 'rgba(148, 163, 184, 0.1)'};
        border-radius: 10px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 12px;
    ">
        <span style="font-size: 20px;">{config['icon']}</span>
        <div style="flex: 1;">
            <div style="font-size: 14px; font-weight: 500; color: #f8fafc;">
                {category}
            </div>
            <div style="font-size: 11px; color: #64748b;">
                {config['description']}
            </div>
        </div>
        <div style="
            padding: 4px 10px;
            background: {color}20;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            color: {color};
        ">
            {agent_count}
        </div>
    </div>
    """, unsafe_allow_html=True)


def left_sidebar(
    agents: list[dict[str, Any]],
    selected_category: str,
    on_category_change: callable
) -> str:
    """
    Render the left sidebar with category navigation.
    
    Args:
        agents: List of agent dictionaries
        selected_category: Currently selected category
        on_category_change: Callback when category changes
        
    Returns:
        Selected category name
    """
    st.markdown("""
    <style>
    .sidebar-container {
        padding: 16px;
        background: rgba(30, 41, 59, 0.5);
        border-radius: 12px;
        height: 100%;
    }
    
    .sidebar-header {
        font-size: 12px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .category-list {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-container">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-header">Agent Categories</div>', unsafe_allow_html=True)
    
    # Count agents by category
    category_counts = {}
    for agent in agents:
        cat = agent["category"].value
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    # All category
    all_count = len(agents)
    is_selected = selected_category == "All"
    
    bg_style = "background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(99, 102, 241, 0.1));" if is_selected else ""
    border_style = "border-color: rgba(99, 102, 241, 0.5);" if is_selected else ""
    
    st.markdown(f"""
    <div style="
        padding: 14px 16px;
        {bg_style}
        border: 1px solid {border_style if is_selected else 'rgba(148, 163, 184, 0.1)'};
        border-radius: 10px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 12px;
    ">
        <span style="font-size: 20px;">🎛️</span>
        <div style="flex: 1;">
            <div style="font-size: 14px; font-weight: 500; color: #f8fafc;">
                All Agents
            </div>
            <div style="font-size: 11px; color: #64748b;">
                Complete agent overview
            </div>
        </div>
        <div style="
            padding: 4px 10px;
            background: rgba(99, 102, 241, 0.2);
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            color: #818cf8;
        ">
            {all_count}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Category items
    for category, config in CATEGORY_CONFIG.items():
        count = category_counts.get(category, 0)
        is_selected = selected_category == category
        
        color = config["color"]
        bg_style = f"background: linear-gradient(135deg, {color}20, {color}10);" if is_selected else ""
        border_style = f"border-color: {color}50;" if is_selected else ""
        
        st.markdown(f"""
        <div style="
            padding: 14px 16px;
            {bg_style}
            border: 1px solid {border_style if is_selected else 'rgba(148, 163, 184, 0.1)'};
            border-radius: 10px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 12px;
        ">
            <span style="font-size: 20px;">{config['icon']}</span>
            <div style="flex: 1;">
                <div style="font-size: 14px; font-weight: 500; color: #f8fafc;">
                    {category}
                </div>
                <div style="font-size: 11px; color: #64748b;">
                    {config['description']}
                </div>
            </div>
            <div style="
                padding: 4px 10px;
                background: {color}20;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 600;
                color: {color};
            ">
                {count}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Use buttons for actual interaction
    st.markdown("")  # Spacer
    
    categories = ["All"] + list(CATEGORY_CONFIG.keys())
    
    selected = st.radio(
        "Categories",
        categories,
        index=categories.index(selected_category) if selected_category in categories else 0,
        label_visibility="collapsed",
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return selected


def render_category_stats(agents: list[dict[str, Any]]) -> None:
    """Render category statistics."""
    st.markdown("### 📊 Category Stats")
    
    # Count by category
    category_counts = {}
    for agent in agents:
        cat = agent["category"].value
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    # Render as mini cards
    for category, config in CATEGORY_CONFIG.items():
        count = category_counts.get(category, 0)
        color = config["color"]
        
        st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 14px;
            background: rgba(30, 41, 59, 0.4);
            border-radius: 8px;
            margin-bottom: 6px;
        ">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 16px;">{config['icon']}</span>
                <span style="font-size: 13px; color: #f8fafc;">{category}</span>
            </div>
            <div style="
                font-size: 14px;
                font-weight: 600;
                font-family: 'JetBrains Mono', monospace;
                color: {color};
            ">
                {count}
            </div>
        </div>
        """, unsafe_allow_html=True)
