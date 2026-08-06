"""Knowledge Graph & AI Reasoning Center Components for AI-QOS."""

from datetime import datetime, timedelta
from typing import Any, Optional
import streamlit as st
import plotly.graph_objects as go


# ============================================================================
# Session State Management
# ============================================================================

def init_knowledge_state() -> None:
    """Initialize knowledge graph session state."""
    defaults = {
        "kg_selected_node": "node_app",
        "kg_expanded_tree": {"root"},
        "kg_search_query": "",
        "kg_filters": set(),
        "kg_view_mode": "graph",
        "kg_selected_flow": None,
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def select_kg_node(node_id: str) -> None:
    """Select a node for inspection."""
    st.session_state.kg_selected_node = node_id


# ============================================================================
# Knowledge Navigator Component
# ============================================================================

def knowledge_navigator(nodes: list[dict[str, Any]], title: str = "Knowledge Navigator") -> None:
    """Render the knowledge tree navigator."""
    st.markdown(f"### 📚 {title}")
    
    # Group nodes by type
    node_groups = {}
    for node in nodes:
        node_type = node.get("type", "unknown")
        if node_type not in node_groups:
            node_groups[node_type] = []
        node_groups[node_type].append(node)
    
    # Type icons
    type_icons = {
        "application": "🏪",
        "page": "📄",
        "component": "🧩",
        "api": "🔗",
        "database_table": "🗄️",
        "business_rule": "📜",
        "test_case": "🧪",
        "bug": "🐛",
    }
    
    # Render expandable groups
    for node_type, type_nodes in node_groups.items():
        icon = type_icons.get(node_type, "📋")
        type_name = node_type.replace("_", " ").title()
        
        with st.expander(f"{icon} {type_name} ({len(type_nodes)})", expanded=False):
            for node in type_nodes:
                # Node card
                risk_colors = {"low": "#10b981", "medium": "#f59e0b", "high": "#ef4444", "critical": "#dc2626"}
                risk_color = risk_colors.get(node.get("risk", "low"), "#64748b")
                
                coverage = node.get("automation_coverage", 0)
                coverage_color = "#10b981" if coverage >= 80 else "#f59e0b" if coverage >= 60 else "#ef4444"
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    if st.button(
                        f"**{node['name']}**",
                        key=f"kg_nav_{node['id']}",
                        use_container_width=True,
                    ):
                        select_kg_node(node["id"])
                        st.rerun()
                    
                    if st.session_state.kg_selected_node == node["id"]:
                        st.markdown(f"<div style='color: #6366f1; font-size: 11px;'>{node.get('description', '')[:60]}</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"<div style='color: {risk_color}; font-size: 10px; text-align: right;'>{node.get('risk', 'low').upper()}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: {coverage_color}; font-size: 10px; text-align: right;'>{coverage:.0f}%</div>", unsafe_allow_html=True)


# ============================================================================
# Knowledge Graph Canvas Component
# ============================================================================

def knowledge_graph_canvas(
    graph_data: dict[str, Any],
    selected_node: Optional[str] = None,
    title: str = "Knowledge Graph"
) -> None:
    """Render the interactive knowledge graph."""
    st.markdown(f"### 🕸️ {title}")
    
    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])
    
    if not nodes:
        st.info("No graph data available.")
        return
    
    # Create positions for nodes
    positions = _calculate_node_positions(nodes, edges)
    
    # Create figure
    fig = go.Figure()
    
    # Add edges
    for edge in edges:
        source_pos = positions.get(edge["source"], (0, 0))
        target_pos = positions.get(edge["target"], (1, 1))
        
        # Edge colors based on relationship type
        edge_colors = {
            "contains": "#6366f1",
            "has": "#22d3ee",
            "uses": "#f59e0b",
            "calls": "#10b981",
            "validates": "#ec4899",
            "covers": "#14b8a6",
            "affects": "#ef4444",
            "default": "#64748b",
        }
        
        fig.add_trace(go.Scatter(
            x=[source_pos[0], target_pos[0]],
            y=[source_pos[1], target_pos[1]],
            mode='lines',
            line=dict(
                color=edge_colors.get(edge.get("type", "default"), "#64748b"),
                width=1.5
            ),
            hoverinfo='text',
            text=edge.get("label", ""),
            showlegend=False,
        ))
    
    # Add nodes
    for node in nodes:
        pos = positions.get(node["id"], (0, 0))
        is_selected = node["id"] == selected_node
        
        # Node size based on selection
        size = 30 if is_selected else 20
        
        # Node color
        color = node.get("color", "#6366f1")
        if is_selected:
            color = "#fff"
        
        # Add glow effect for selected
        if is_selected:
            fig.add_trace(go.Scatter(
                x=[pos[0]],
                y=[pos[1]],
                mode='markers',
                marker=dict(size=size + 10, color=color, opacity=0.3),
                showlegend=False,
                hoverinfo='skip',
            ))
        
        fig.add_trace(go.Scatter(
            x=[pos[0]],
            y=[pos[1]],
            mode='markers+text',
            marker=dict(
                size=size,
                color=color,
                line=dict(color="#fff", width=2 if is_selected else 1)
            ),
            text=[node["label"]],
            textposition="middle center",
            textfont=dict(size=8, color="#f8fafc"),
            hovertemplate=f"<b>{node['label']}</b><br>Type: {node.get('type', 'unknown')}<extra></extra>",
            showlegend=False,
        ))
    
    # Update layout
    fig.update_layout(
        height=500,
        showlegend=False,
        paper_bgcolor='rgba(15, 23, 42, 0.9)',
        plot_bgcolor='rgba(15, 23, 42, 0.9)',
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-2, 2]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-2, 2]),
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Controls
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🔍 Zoom In", use_container_width=True):
            st.info("Zoom in")
    with col2:
        if st.button("🔍 Zoom Out", use_container_width=True):
            st.info("Zoom out")
    with col3:
        if st.button("📐 Fit View", use_container_width=True):
            st.info("Fit view")
    with col4:
        if st.button("🎯 Focus Selected", use_container_width=True):
            st.info("Focus on selected node")
    
    # Legend
    st.markdown("""
    <div style="display: flex; flex-wrap: wrap; gap: 16px; justify-content: center; margin-top: 12px;">
        <span style="display: flex; align-items: center; gap: 6px;">
            <span style="width: 12px; height: 12px; background: #6366f1; border-radius: 50%;"></span>
            <span style="font-size: 11px; color: #94a3b8;">Application</span>
        </span>
        <span style="display: flex; align-items: center; gap: 6px;">
            <span style="width: 12px; height: 12px; background: #22d3ee; border-radius: 50%;"></span>
            <span style="font-size: 11px; color: #94a3b8;">Page</span>
        </span>
        <span style="display: flex; align-items: center; gap: 6px;">
            <span style="width: 12px; height: 12px; background: #10b981; border-radius: 50%;"></span>
            <span style="font-size: 11px; color: #94a3b8;">Component</span>
        </span>
        <span style="display: flex; align-items: center; gap: 6px;">
            <span style="width: 12px; height: 12px; background: #f59e0b; border-radius: 50%;"></span>
            <span style="font-size: 11px; color: #94a3b8;">API</span>
        </span>
        <span style="display: flex; align-items: center; gap: 6px;">
            <span style="width: 12px; height: 12px; background: #8b5cf6; border-radius: 50%;"></span>
            <span style="font-size: 11px; color: #94a3b8;">Database</span>
        </span>
        <span style="display: flex; align-items: center; gap: 6px;">
            <span style="width: 12px; height: 12px; background: #ec4899; border-radius: 50%;"></span>
            <span style="font-size: 11px; color: #94a3b8;">Rule</span>
        </span>
    </div>
    """, unsafe_allow_html=True)


def _calculate_node_positions(nodes: list[dict], edges: list[dict]) -> dict[str, tuple[float, float]]:
    """Calculate node positions using a simple force-directed algorithm."""
    positions = {}
    
    # Group by type for clustering
    type_clusters = {
        "application": (0, 0),
        "page": (-1.5, 0),
        "component": (-1, -1),
        "api": (1, -0.5),
        "database_table": (1.5, 0),
        "business_rule": (0.5, 1),
        "test_case": (-0.5, 1),
        "bug": (1, 1),
    }
    
    # Initialize positions based on type
    type_indices = {}
    for node in nodes:
        node_type = node.get("type", "unknown")
        if node_type not in type_indices:
            type_indices[node_type] = 0
        index = type_indices[node_type]
        type_indices[node_type] += 1
        
        base_pos = type_clusters.get(node_type, (0, 0))
        
        # Spread nodes within cluster
        angle = index * 0.5
        x = base_pos[0] + 0.3 * (index % 3) * (1 if index % 2 else -1)
        y = base_pos[1] + 0.3 * (index // 3) * (1 if index % 2 else -1)
        
        positions[node["id"]] = (x, y)
    
    return positions


# ============================================================================
# Node Inspector Component
# ============================================================================

def node_inspector(node: dict[str, Any], title: str = "Node Inspector") -> None:
    """Render detailed node inspector."""
    st.markdown(f"### 🔍 {title}")
    
    if not node:
        st.info("Select a node to view details.")
        return
    
    # Node header
    type_icons = {
        "application": "🏪",
        "page": "📄",
        "component": "🧩",
        "api": "🔗",
        "database_table": "🗄️",
        "business_rule": "📜",
        "test_case": "🧪",
        "bug": "🐛",
    }
    
    icon = type_icons.get(node.get("type", ""), "📋")
    
    st.markdown(f"""
    <div style="
        padding: 20px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(34, 211, 238, 0.1));
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
        margin-bottom: 16px;
    ">
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 32px;">{icon}</span>
            <div>
                <h3 style="margin: 0; color: #f8fafc;">{node['name']}</h3>
                <span style="font-size: 12px; color: #64748b;">{node.get('type', 'unknown').replace('_', ' ').title()}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics
    risk_colors = {"low": "#10b981", "medium": "#f59e0b", "high": "#ef4444", "critical": "#dc2626"}
    risk_color = risk_colors.get(node.get("risk", "low"), "#64748b")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        coverage = node.get("automation_coverage", 0)
        coverage_color = "#10b981" if coverage >= 80 else "#f59e0b" if coverage >= 60 else "#ef4444"
        st.markdown(f"""
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; text-align: center;">
            <div style="font-size: 24px; font-weight: 700; color: {coverage_color};">{coverage:.0f}%</div>
            <div style="font-size: 10px; color: #64748b;">Coverage</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        confidence = node.get("confidence", 0)
        st.markdown(f"""
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; text-align: center;">
            <div style="font-size: 24px; font-weight: 700; color: #818cf8;">{confidence:.0f}%</div>
            <div style="font-size: 10px; color: #64748b;">Confidence</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; text-align: center;">
            <div style="font-size: 18px; font-weight: 700; color: {risk_color};">{node.get('risk', 'low').upper()}</div>
            <div style="font-size: 10px; color: #64748b;">Risk</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        priority = node.get("priority", "medium")
        priority_color = "#ef4444" if priority == "critical" else "#f59e0b" if priority == "high" else "#64748b"
        st.markdown(f"""
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; text-align: center;">
            <div style="font-size: 16px; font-weight: 700; color: {priority_color};">{priority.upper()}</div>
            <div style="font-size: 10px; color: #64748b;">Priority</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Description
    st.markdown("#### 📝 Description")
    st.markdown(f"<div style='color: #94a3b8; font-size: 14px;'>{node.get('description', 'No description available.')}</div>", unsafe_allow_html=True)
    
    # Business Purpose
    st.markdown("#### 🎯 Business Purpose")
    st.markdown(f"<div style='color: #f8fafc; font-size: 14px;'>{node.get('business_purpose', 'Not specified.')}</div>", unsafe_allow_html=True)
    
    # Dependencies
    deps = node.get("dependencies", [])
    if deps:
        st.markdown("#### 🔗 Dependencies")
        dep_names = []
        for dep_id in deps:
            dep_names.append(f"- {dep_id.replace('node_', '').replace('_', ' ').title()}")
        st.markdown("\n".join(dep_names))


# ============================================================================
# AI Reasoning Panel Component
# ============================================================================

def ai_reasoning_panel(node: dict[str, Any], title: str = "AI Reasoning") -> None:
    """Render AI-powered reasoning panel."""
    st.markdown(f"### 💡 {title}")
    
    if not node:
        st.info("Select a node to view AI reasoning.")
        return
    
    from utils.knowledge_graph_data import generate_ai_reasoning
    
    reasoning = generate_ai_reasoning(node)
    
    st.markdown(f"""
    <div style="
        padding: 16px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(34, 211, 238, 0.15));
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        margin-bottom: 16px;
    ">
        <div style="font-size: 11px; color: #64748b; text-transform: uppercase; margin-bottom: 8px;">Why Exists</div>
        <div style="font-size: 14px; color: #f8fafc; line-height: 1.5;">{reasoning['why_exists']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px;">
            <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Business Importance</div>
            <div style="font-size: 16px; color: #f8fafc; margin-top: 4px;">{reasoning['business_importance']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        
        st.markdown(f"""
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px;">
            <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Dependencies</div>
            <div style="font-size: 14px; color: #f8fafc; margin-top: 4px;">{reasoning['dependencies']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px;">
            <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Risk Assessment</div>
            <div style="font-size: 14px; color: #f8fafc; margin-top: 4px;">{reasoning['risk_assessment']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        
        st.markdown(f"""
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px;">
            <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Automation</div>
            <div style="font-size: 14px; color: #f8fafc; margin-top: 4px;">{reasoning['automation_importance']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommendation
    st.markdown("#### 🚀 AI Recommendation")
    st.markdown(f"""
    <div style="
        padding: 14px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 10px;
    ">
        <div style="font-size: 14px; color: #f8fafc;">{reasoning['recommendation']}</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 8px;">{reasoning['future_impact']}</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# Impact Analysis Panel Component
# ============================================================================

def impact_analysis_panel(node_id: str, title: str = "Impact Analysis") -> None:
    """Render impact analysis panel."""
    st.markdown(f"### 📊 {title}")
    
    from utils.knowledge_graph_data import get_impact_analysis
    
    analysis = get_impact_analysis(node_id)
    
    if not analysis:
        st.info("No impact analysis available.")
        return
    
    node = analysis["node"]
    affected = analysis["affected"]
    total = analysis["total_affected"]
    
    # Summary
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; background: rgba(30, 41, 59, 0.6); border-radius: 12px; margin-bottom: 16px;">
        <div style="font-size: 48px; font-weight: 700; color: #6366f1;">{total}</div>
        <div style="font-size: 12px; color: #64748b; text-transform: uppercase;">Nodes Affected by {node['name']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Affected nodes by category
    for category, nodes in affected.items():
        if nodes:
            category_name = category.replace("_", " ").title()
            icon = "📄" if "page" in category else "🧩" if "component" in category else "🔗" if "api" in category else "📜" if "rule" in category else "🧪" if "test" in category else "🐛" if "bug" in category else "📋"
            
            with st.expander(f"{icon} {category_name} ({len(nodes)})"):
                for n in nodes:
                    risk_color = "#ef4444" if n.get("risk") == "high" else "#f59e0b" if n.get("risk") == "medium" else "#10b981"
                    st.markdown(f"- **{n['name']}** <span style='color: {risk_color}; font-size: 11px;'>{n.get('risk', 'low').upper()}</span>", unsafe_allow_html=True)


# ============================================================================
# Business Flow Explorer Component
# ============================================================================

def business_flow_explorer(flows: list[dict[str, Any]], title: str = "Business Flows") -> None:
    """Render business flow explorer."""
    st.markdown(f"### 🔀 {title}")
    
    from utils.knowledge_graph_data import get_node_by_id
    
    for flow in flows:
        risk_colors = {"low": "#10b981", "medium": "#f59e0b", "high": "#ef4444", "critical": "#dc2626"}
        risk_color = risk_colors.get(flow.get("risk", "low"), "#64748b")
        
        coverage = flow.get("automation_coverage", 0)
        coverage_color = "#10b981" if coverage >= 80 else "#f59e0b" if coverage >= 60 else "#ef4444"
        
        with st.expander(f"🔀 {flow['name']} ({flow.get('risk', 'low').upper()})"):
            st.markdown(f"**Description:** {flow.get('description', '')}")
            st.markdown(f"**Coverage:** <span style='color: {coverage_color}'>{coverage:.0f}%</span>", unsafe_allow_html=True)
            
            # Flow steps
            st.markdown("**Flow Steps:**")
            for i, step_id in enumerate(flow.get("steps", [])):
                node = get_node_by_id(step_id)
                if node:
                    arrow = " → " if i < len(flow["steps"]) - 1 else ""
                    st.markdown(f"📄 {node['name']}{arrow}", unsafe_allow_html=True)


# ============================================================================
# Graph Statistics Component
# ============================================================================

def graph_statistics(stats: dict[str, Any], title: str = "Graph Statistics") -> None:
    """Render graph statistics dashboard."""
    st.markdown(f"### 📈 {title}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Nodes", stats.get("total_nodes", 0))
    with col2:
        st.metric("Relationships", stats.get("total_relationships", 0))
    with col3:
        coverage = stats.get("coverage", 0)
        st.metric("Coverage", f"{coverage:.1f}%")
    with col4:
        st.metric("Confidence", f"{stats.get('confidence_score', 0):.0f}%")
    
    st.markdown("---")
    
    # Type breakdown
    st.markdown("#### Nodes by Type")
    by_type = stats.get("by_type", {})
    
    for node_type, data in by_type.items():
        type_name = node_type.replace("_", " ").title()
        count = data.get("count", 0)
        cov = data.get("coverage", 0)
        
        cov_color = "#10b981" if cov >= 80 else "#f59e0b" if cov >= 60 else "#ef4444"
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"**{type_name}**")
        with col2:
            st.markdown(f"Count: {count}")
        with col3:
            st.markdown(f"<span style='color: {cov_color};'>Coverage: {cov}%</span>", unsafe_allow_html=True)


# ============================================================================
# AI Discoveries Component
# ============================================================================

def ai_discoveries_panel(discoveries: list[dict[str, Any]], title: str = "AI Discoveries") -> None:
    """Render AI discoveries panel."""
    st.markdown(f"### 🤖 {title}")
    
    # Summary
    critical = sum(1 for d in discoveries if d.get("severity") == "critical")
    high = sum(1 for d in discoveries if d.get("severity") == "high")
    total = sum(d.get("count", 0) for d in discoveries)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Critical", critical)
    with col2:
        st.metric("High", high)
    with col3:
        st.metric("Total Issues", total)
    
    st.markdown("---")
    
    type_icons = {
        "duplicate_components": "🔄",
        "dead_pages": "💀",
        "unused_apis": "🔗",
        "broken_relationships": "⛓️",
        "missing_business_rules": "📜",
        "automation_gaps": "🕳️",
        "accessibility_issues": "♿",
        "security_risks": "🔒",
        "flaky_components": "📳",
    }
    
    severity_colors = {
        "critical": "#ef4444",
        "high": "#f59e0b",
        "medium": "#3b82f6",
        "low": "#64748b",
    }
    
    for discovery in discoveries:
        icon = type_icons.get(discovery.get("type", ""), "📋")
        color = severity_colors.get(discovery.get("severity", "info"), "#64748b")
        
        with st.expander(f"{icon} {discovery['type'].replace('_', ' ').title()} ({discovery['count']})", expanded=discovery.get("severity") in ["critical", "high"]):
            st.markdown(f"**{discovery['description']}**")
            st.markdown(f"<span style='color: {color}; font-size: 12px;'>{discovery.get('severity', 'info').upper()} severity</span>", unsafe_allow_html=True)


# ============================================================================
# AI Recommendations Component
# ============================================================================

def ai_recommendations_panel(recommendations: list[dict[str, Any]], title: str = "AI Recommendations") -> None:
    """Render AI recommendations panel."""
    st.markdown(f"### 🎯 {title}")
    
    priority_colors = {
        "critical": "#ef4444",
        "high": "#f59e0b",
        "medium": "#3b82f6",
        "low": "#64748b",
    }
    
    category_icons = {
        "tests": "🧪",
        "automation": "🤖",
        "coverage": "📊",
        "accessibility": "♿",
        "security": "🔒",
    }
    
    for rec in recommendations:
        icon = category_icons.get(rec.get("category", ""), "💡")
        priority_color = priority_colors.get(rec.get("priority", "medium"), "#64748b")
        
        st.markdown(f"""
        <div style="
            padding: 14px;
            background: rgba(30, 41, 59, 0.6);
            border-left: 3px solid {priority_color};
            border-radius: 0 8px 8px 0;
            margin-bottom: 12px;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 16px;">{icon}</span>
                <span style="
                    padding: 2px 8px;
                    background: {priority_color}20;
                    border-radius: 4px;
                    font-size: 10px;
                    color: {priority_color};
                    text-transform: uppercase;
                ">
                    {rec.get('priority', 'medium')}
                </span>
            </div>
            <div style="font-size: 14px; color: #f8fafc; margin-bottom: 6px;">
                {rec.get('recommendation', '')}
            </div>
            <div style="font-size: 12px; color: #94a3b8;">
                {rec.get('reason', '')}
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# Quick Actions Component
# ============================================================================

def kg_quick_actions(title: str = "Quick Actions") -> None:
    """Render quick actions panel."""
    st.markdown(f"### ⚡ {title}")
    
    actions = [
        ("🌐 DOM Explorer", "Open DOM Intelligence Explorer"),
        ("📂 Application Explorer", "Open Application Explorer"),
        ("🧪 Generate Tests", "Generate test cases for selected"),
        ("📝 Feature Files", "Generate feature files"),
        ("📦 Page Objects", "Generate page objects"),
        ("📊 Reports", "Generate coverage reports"),
        ("💡 Explain Flow", "Explain business flow"),
        ("📈 Impact Analysis", "Analyze change impact"),
    ]
    
    cols = st.columns(2)
    for i, (label, tooltip) in enumerate(actions):
        with cols[i % 2]:
            if st.button(label, key=f"kg_action_{i}", use_container_width=True):
                st.info(tooltip)
                st.rerun()


# ============================================================================
# Search Component
# ============================================================================

def kg_search(on_search: callable = None) -> str:
    """Render knowledge graph search input."""
    query = st.text_input(
        "🔍 Search knowledge graph...",
        placeholder="Search nodes, relationships, business rules...",
        label_visibility="collapsed",
        key="kg_search_input",
    )
    
    return query


# ============================================================================
# Mini Map Component
# ============================================================================

def mini_map(graph_data: dict[str, Any], selected_node: Optional[str] = None, title: str = "Mini Map") -> None:
    """Render a mini map of the knowledge graph."""
    st.markdown(f"### 🗺️ {title}")
    
    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])
    
    # Create a simplified visualization
    positions = _calculate_node_positions(nodes, edges)
    
    fig = go.Figure()
    
    # Add edges (simplified)
    for edge in edges[:20]:  # Limit edges for performance
        source_pos = positions.get(edge["source"], (0, 0))
        target_pos = positions.get(edge["target"], (1, 1))
        
        fig.add_trace(go.Scatter(
            x=[source_pos[0], target_pos[0]],
            y=[source_pos[1], target_pos[1]],
            mode='lines',
            line=dict(color="#334155", width=1),
            showlegend=False,
            hoverinfo='skip',
        ))
    
    # Add nodes
    for node in nodes:
        pos = positions.get(node["id"], (0, 0))
        is_selected = node["id"] == selected_node
        
        fig.add_trace(go.Scatter(
            x=[pos[0]],
            y=[pos[1]],
            mode='markers',
            marker=dict(
                size=8 if is_selected else 5,
                color=node.get("color", "#6366f1"),
                opacity=1.0 if is_selected else 0.6,
            ),
            showlegend=False,
            hoverinfo='text',
            text=node["label"],
        ))
    
    fig.update_layout(
        height=150,
        showlegend=False,
        paper_bgcolor='transparent',
        plot_bgcolor='transparent',
        margin=dict(l=5, r=5, t=5, b=5),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-2, 2]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-2, 2]),
    )
    
    st.plotly_chart(fig, use_container_width=True)
