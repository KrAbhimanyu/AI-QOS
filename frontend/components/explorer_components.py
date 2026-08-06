"""Application Explorer Components for AI-QOS - Digital Twin Visualization."""

from datetime import datetime, timedelta
from typing import Any, Callable, Optional
import streamlit as st
import plotly.graph_objects as go


# ============================================================================
# Session State Management
# ============================================================================

def init_explorer_state() -> None:
    """Initialize explorer session state."""
    defaults = {
        "selected_page": None,
        "expanded_nodes": set(),
        "search_query": "",
        "filter_category": "all",
        "inspector_tab": "overview",
        "show_page_workspace": False,
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def toggle_node_expansion(node_id: str) -> None:
    """Toggle tree node expansion."""
    if node_id in st.session_state.expanded_nodes:
        st.session_state.expanded_nodes.discard(node_id)
    else:
        st.session_state.expanded_nodes.add(node_id)


def select_page(page: dict[str, Any]) -> None:
    """Select a page for inspection."""
    st.session_state.selected_page = page
    st.session_state.show_page_workspace = True


def clear_selection() -> None:
    """Clear page selection."""
    st.session_state.selected_page = None
    st.session_state.show_page_workspace = False


# ============================================================================
# Application Tree Component
# ============================================================================

def render_tree_node(
    node: dict[str, Any],
    level: int = 0,
    parent_expanded: bool = True
) -> None:
    """Render a single tree node recursively."""
    node_id = node["id"]
    is_expanded = node_id in st.session_state.expanded_nodes
    has_children = bool(node.get("children"))
    
    # Indentation
    indent = "　　" * level
    
    # Status color
    status_colors = {"active": "#10b981", "partial": "#f59e0b", "inactive": "#64748b"}
    status_color = status_colors.get(node.get("status", "active"), "#64748b")
    
    # Coverage color
    coverage = node.get("coverage", 0)
    if coverage >= 80:
        coverage_color = "#10b981"
    elif coverage >= 50:
        coverage_color = "#f59e0b"
    else:
        coverage_color = "#ef4444"
    
    # Node type icons
    type_icons = {
        "application": "🏪",
        "module": "📁",
        "page": "📄",
    }
    icon = type_icons.get(node.get("type", "page"), "📄")
    
    # Build the row HTML
    col1, col2, col3 = st.columns([4, 1, 1])
    
    with col1:
        # Expand/collapse button for nodes with children
        if has_children:
            if st.button(
                f"{'▼' if is_expanded else '▶'} {indent}{icon} {node['name']}",
                key=f"tree_{node_id}",
                use_container_width=True,
            ):
                toggle_node_expansion(node_id)
                st.rerun()
        else:
            # Leaf node - clickable
            if st.button(
                f"　 {indent}{icon} {node['name']}",
                key=f"tree_{node_id}",
                use_container_width=True,
            ):
                select_page(node)
                st.rerun()
    
    with col2:
        # Coverage badge
        st.markdown(f"""
        <div style="
            padding: 4px 8px;
            background: {coverage_color}20;
            border: 1px solid {coverage_color}50;
            border-radius: 4px;
            font-size: 11px;
            text-align: center;
            color: {coverage_color};
        ">
            {coverage:.0f}%
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Confidence badge
        confidence = node.get("confidence", 0)
        st.markdown(f"""
        <div style="
            padding: 4px 8px;
            background: rgba(99, 102, 241, 0.2);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 4px;
            font-size: 11px;
            text-align: center;
            color: #818cf8;
        ">
            {confidence:.0f}%
        </div>
        """, unsafe_allow_html=True)
    
    # Render children if expanded
    if has_children and is_expanded:
        for child in node.get("children", []):
            render_tree_node(child, level + 1, is_expanded)


def application_tree(tree_data: dict[str, Any], title: str = "Application Tree") -> None:
    """Render the full application tree."""
    st.markdown(f"### 📂 {title}")
    
    # Expand root by default
    if "app_root" not in st.session_state.expanded_nodes:
        st.session_state.expanded_nodes.add("app_root")
    
    # Expand all modules by default
    for child in tree_data.get("children", []):
        if child["id"] not in st.session_state.expanded_nodes:
            st.session_state.expanded_nodes.add(child["id"])
    
    # Render tree
    render_tree_node(tree_data)
    
    # Summary stats
    _render_tree_summary(tree_data)


def _render_tree_summary(tree: dict[str, Any]) -> None:
    """Render tree summary statistics."""
    pages = []
    modules = []
    
    def count_nodes(node: dict[str, Any]) -> None:
        if node.get("type") == "page":
            pages.append(node)
        elif node.get("type") == "module":
            modules.append(node)
        for child in node.get("children", []):
            count_nodes(child)
    
    count_nodes(tree)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Modules", len(modules))
    with col2:
        st.metric("Pages", len(pages))
    with col3:
        avg_coverage = sum(p.get("coverage", 0) for p in pages) / max(1, len(pages))
        st.metric("Avg Coverage", f"{avg_coverage:.1f}%")


# ============================================================================
# Page Card Component
# ============================================================================

def page_card(page: dict[str, Any], columns: int = 3) -> None:
    """Render a page as a card."""
    with st.container():
        # Screenshot placeholder
        st.markdown(f"""
        <div style="
            height: 150px;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(34, 211, 238, 0.1));
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-radius: 12px 12px 0 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 48px;
        ">
            {page.get('icon', '📄')}
        </div>
        """, unsafe_allow_html=True)
        
        # Card content
        coverage = page.get("coverage", 0)
        risk = page.get("risk", "Low")
        
        coverage_color = "#10b981" if coverage >= 80 else "#f59e0b" if coverage >= 50 else "#ef4444"
        risk_colors = {"Low": "#10b981", "Medium": "#f59e0b", "High": "#ef4444", "Critical": "#dc2626"}
        risk_color = risk_colors.get(risk, "#64748b")
        
        st.markdown(f"""
        <div style="
            padding: 16px;
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-top: none;
            border-radius: 0 0 12px 12px;
        ">
            <h4 style="margin: 0 0 8px; color: #f8fafc; font-size: 14px;">
                {page['name']}
            </h4>
            <div style="font-size: 11px; color: #64748b; margin-bottom: 12px;">
                {page.get('url', '/')}
            </div>
            
            <div style="display: flex; gap: 8px; margin-bottom: 12px;">
                <span style="
                    padding: 2px 8px;
                    background: {coverage_color}20;
                    border-radius: 4px;
                    font-size: 10px;
                    color: {coverage_color};
                ">
                    {coverage:.0f}% Covered
                </span>
                <span style="
                    padding: 2px 8px;
                    background: {risk_color}20;
                    border-radius: 4px;
                    font-size: 10px;
                    color: {risk_color};
                ">
                    {risk} Risk
                </span>
            </div>
            
            <div style="
                font-size: 11px;
                color: #818cf8;
                font-family: 'JetBrains Mono', monospace;
            ">
                Confidence: {page.get('confidence', 0):.0f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action button
        if st.button(f"Inspect →", key=f"inspect_{page['id']}", use_container_width=True):
            select_page(page)
            st.rerun()


def page_gallery(pages: list[dict[str, Any]], title: str = "Page Gallery") -> None:
    """Render a gallery of page cards."""
    st.markdown(f"### 🖼️ {title}")
    
    if not pages:
        st.info("No pages match your search criteria.")
        return
    
    # Display in grid
    cols = st.columns(3)
    for i, page in enumerate(pages):
        with cols[i % 3]:
            page_card(page)


# ============================================================================
# Page Workspace Component
# ============================================================================

def page_workspace(page: dict[str, Any]) -> None:
    """Render detailed page workspace."""
    st.markdown(f"""
    <div style="
        padding: 20px;
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        margin-bottom: 20px;
    ">
        <div style="display: flex; align-items: center; gap: 16px;">
            <span style="font-size: 48px;">{page.get('icon', '📄')}</span>
            <div>
                <h2 style="margin: 0; color: #f8fafc;">{page['name']}</h2>
                <div style="font-size: 14px; color: #64748b; margin-top: 4px;">
                    {page.get('url', '/')} • {page.get('framework', 'React')}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Component metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Components", page.get("components", 0))
    with col2:
        st.metric("Forms", page.get("forms", 0))
    with col3:
        st.metric("Buttons", page.get("buttons", 0))
    with col4:
        st.metric("Coverage", f"{page.get('coverage', 0):.1f}%")
    
    st.markdown("---")
    
    # Detailed sections
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Components", "Rules", "Issues"])
    
    with tab1:
        _render_page_overview(page)
    
    with tab2:
        _render_page_components(page)
    
    with tab3:
        _render_page_rules(page)
    
    with tab4:
        _render_page_issues(page)


def _render_page_overview(page: dict[str, Any]) -> None:
    """Render page overview."""
    st.markdown("#### 📊 Scores")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        acc_score = page.get("accessibility_score", 0)
        st.markdown(f"""
        <div style="padding: 16px; background: rgba(30, 41, 59, 0.6); border-radius: 12px; text-align: center;">
            <div style="font-size: 32px; font-weight: 700; color: {'#10b981' if acc_score >= 90 else '#f59e0b' if acc_score >= 70 else '#ef4444'};">
                {acc_score:.0f}
            </div>
            <div style="font-size: 12px; color: #64748b; text-transform: uppercase;">Accessibility</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        perf_score = page.get("performance_score", 0)
        st.markdown(f"""
        <div style="padding: 16px; background: rgba(30, 41, 59, 0.6); border-radius: 12px; text-align: center;">
            <div style="font-size: 32px; font-weight: 700; color: {'#10b981' if perf_score >= 80 else '#f59e0b' if perf_score >= 60 else '#ef4444'};">
                {perf_score:.0f}
            </div>
            <div style="font-size: 12px; color: #64748b; text-transform: uppercase;">Performance</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        sec_score = page.get("security_score", 0)
        st.markdown(f"""
        <div style="padding: 16px; background: rgba(30, 41, 59, 0.6); border-radius: 12px; text-align: center;">
            <div style="font-size: 32px; font-weight: 700; color: {'#10b981' if sec_score >= 85 else '#f59e0b' if sec_score >= 70 else '#ef4444'};">
                {sec_score:.0f}
            </div>
            <div style="font-size: 12px; color: #64748b; text-transform: uppercase;">Security</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("#### 💡 AI Summary")
    st.markdown(f"""
    <div style="
        padding: 16px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(34, 211, 238, 0.1));
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
        font-size: 14px;
        line-height: 1.6;
        color: #94a3b8;
    ">
        {page.get('ai_summary', 'No summary available.')}
    </div>
    """, unsafe_allow_html=True)
    
    # AI Explanation
    st.markdown("#### 🎯 AI Explanation")
    explanation = page.get('why_discovered', 'Discovered through automated analysis.')
    evidence = page.get('evidence', [])
    importance = page.get('business_importance', 'Medium')
    complexity = page.get('automation_complexity', 'Moderate')
    
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px;">
            <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Why Discovered</div>
            <div style="font-size: 13px; color: #f8fafc; margin-top: 4px;">{explanation}</div>
        </div>
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px;">
            <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Business Importance</div>
            <div style="font-size: 13px; color: #f8fafc; margin-top: 4px;">{importance}</div>
        </div>
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px;">
            <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Automation Complexity</div>
            <div style="font-size: 13px; color: #f8fafc; margin-top: 4px;">{complexity}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _render_page_components(page: dict[str, Any]) -> None:
    """Render page components list."""
    components = page.get("components_detail", [])
    
    if not components:
        st.info("No component details available.")
        return
    
    for comp in components:
        comp_type = comp.get("type", {}).value if hasattr(comp.get("type", {}), 'value') else str(comp.get("type", "Unknown"))
        
        status_icons = "✅" if comp.get("automation_ready", False) else "⚠️"
        flaky_indicator = " (Flaky!)" if comp.get("is_flaky", False) else ""
        
        st.markdown(f"""
        <div style="
            padding: 12px;
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-radius: 8px;
            margin-bottom: 8px;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-size: 14px; color: #f8fafc;">{comp['name']}</span>
                    <span style="font-size: 11px; color: #64748b; margin-left: 8px;">{comp_type}{flaky_indicator}</span>
                </div>
                <div style="display: flex; gap: 12px;">
                    {status_icons}
                    <span style="font-size: 11px; color: #818cf8;">
                        Test ID: {comp.get('test_id', 'N/A')}
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def _render_page_rules(page: dict[str, Any]) -> None:
    """Render page business rules."""
    rules = page.get("business_rules_detail", [])
    
    if not rules:
        st.info("No business rules available.")
        return
    
    complexity_colors = {"Low": "#10b981", "Medium": "#f59e0b", "High": "#ef4444"}
    
    for rule in rules:
        color = complexity_colors.get(rule.get("complexity", "Low"), "#64748b")
        st.markdown(f"""
        <div style="
            padding: 14px;
            background: rgba(30, 41, 59, 0.6);
            border-left: 3px solid {color};
            border-radius: 0 8px 8px 0;
            margin-bottom: 10px;
        ">
            <div style="display: flex; justify-content: space-between;">
                <span style="font-size: 14px; color: #f8fafc; font-weight: 500;">
                    {rule['name']}
                </span>
                <span style="
                    padding: 2px 8px;
                    background: {color}20;
                    border-radius: 4px;
                    font-size: 10px;
                    color: {color};
                ">
                    {rule.get('complexity', 'Low')}
                </span>
            </div>
            <div style="font-size: 12px; color: #94a3b8; margin-top: 6px;">
                {rule.get('description', '')}
            </div>
        </div>
        """, unsafe_allow_html=True)


def _render_page_issues(page: dict[str, Any]) -> None:
    """Render page issues."""
    # Accessibility
    st.markdown("#### ♿ Accessibility Issues")
    acc_issues = page.get("accessibility_issues", [])
    for issue in acc_issues:
        severity_colors = {"high": "#ef4444", "medium": "#f59e0b", "low": "#64748b"}
        color = severity_colors.get(issue.get("severity", "low"), "#64748b")
        st.markdown(f"""
        <div style="padding: 10px; background: rgba(239, 68, 68, 0.1); border-left: 3px solid {color}; border-radius: 0 6px 6px 0; margin-bottom: 8px;">
            <span style="font-size: 12px; color: #f8fafc;">{issue.get('issue', '')}</span>
            <span style="font-size: 10px; color: #64748b; margin-left: 8px;">{issue.get('element', '')}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance
    st.markdown("#### ⚡ Performance Issues")
    perf_issues = page.get("performance_issues", [])
    for issue in perf_issues:
        color = "#f59e0b" if issue.get("severity") == "medium" else "#ef4444"
        st.markdown(f"""
        <div style="padding: 10px; background: rgba(245, 158, 11, 0.1); border-left: 3px solid {color}; border-radius: 0 6px 6px 0; margin-bottom: 8px;">
            <span style="font-size: 12px; color: #f8fafc;">{issue.get('issue', '')}</span>
            <span style="font-size: 10px; color: #94a3b8; margin-left: 8px;">{issue.get('impact', '')}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Security
    st.markdown("#### 🔒 Security Warnings")
    sec_warnings = page.get("security_warnings", [])
    for warning in sec_warnings:
        color = "#ef4444" if warning.get("severity") == "critical" else "#f59e0b"
        st.markdown(f"""
        <div style="padding: 10px; background: rgba(239, 68, 68, 0.1); border-left: 3px solid {color}; border-radius: 0 6px 6px 0; margin-bottom: 8px;">
            <span style="font-size: 12px; color: #f8fafc;">{warning.get('warning', '')}</span>
            <span style="font-size: 10px; color: #64748b; margin-left: 8px;">{warning.get('location', '')}</span>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# Application Map Component
# ============================================================================

def application_map(connections: list[dict[str, Any]], title: str = "Application Map") -> None:
    """Render application navigation map as a graph."""
    st.markdown(f"### 🗺️ {title}")
    
    # Create nodes
    nodes = list(set([c["from"] for c in connections] + [c["to"] for c in connections]))
    node_positions = {node: (i % 4, i // 4) for i, node in enumerate(nodes)}
    
    # Create figure
    fig = go.Figure()
    
    # Add edges
    for conn in connections:
        x0, y0 = node_positions[conn["from"]]
        x1, y1 = node_positions[conn["to"]]
        
        type_colors = {
            "navigation": "#6366f1",
            "action": "#22d3ee",
            "auth": "#f59e0b",
            "direct": "#10b981",
        }
        color = type_colors.get(conn.get("type", "navigation"), "#6366f1")
        
        fig.add_trace(go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            mode='lines',
            line=dict(color=color, width=2),
            hoverinfo='text',
            text=f"{conn['from']} → {conn['to']}",
            showlegend=False,
        ))
    
    # Add nodes
    for node, (x, y) in node_positions.items():
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode='markers+text',
            marker=dict(size=30, color='#6366f1', line=dict(color='#fff', width=2)),
            text=[node],
            textposition='middle center',
            textfont=dict(size=10, color='#f8fafc'),
            hovertemplate=f"<b>{node}</b><extra></extra>",
            showlegend=False,
        ))
    
    fig.update_layout(
        height=300,
        showlegend=False,
        paper_bgcolor='transparent',
        plot_bgcolor='transparent',
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 3.5]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 3.5]),
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Legend
    st.markdown("""
    <div style="display: flex; gap: 16px; justify-content: center; margin-top: 12px;">
        <span style="display: flex; align-items: center; gap: 6px;">
            <span style="width: 20px; height: 3px; background: #6366f1; border-radius: 2px;"></span>
            <span style="font-size: 11px; color: #94a3b8;">Navigation</span>
        </span>
        <span style="display: flex; align-items: center; gap: 6px;">
            <span style="width: 20px; height: 3px; background: #22d3ee; border-radius: 2px;"></span>
            <span style="font-size: 11px; color: #94a3b8;">Action</span>
        </span>
        <span style="display: flex; align-items: center; gap: 6px;">
            <span style="width: 20px; height: 3px; background: #f59e0b; border-radius: 2px;"></span>
            <span style="font-size: 11px; color: #94a3b8;">Auth</span>
        </span>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# Statistics Dashboard Component
# ============================================================================

def statistics_dashboard(stats: dict[str, Any], title: str = "Statistics") -> None:
    """Render statistics dashboard."""
    st.markdown(f"### 📊 {title}")
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        pages = stats.get("pages", {})
        st.metric("Pages", pages.get("total", 0), f"{pages.get('discovered', 0)} discovered")
    
    with col2:
        components = stats.get("components", {})
        st.metric("Components", components.get("total", 0))
    
    with col3:
        forms = stats.get("forms", {})
        st.metric("Forms", forms.get("total", 0), f"{forms.get('validated', 0)} validated")
    
    with col4:
        apis = stats.get("apis", {})
        st.metric("APIs", apis.get("total", 0), f"{apis.get('documented', 0)} documented")
    
    st.markdown("---")
    
    # Coverage
    coverage = stats.get("coverage", {})
    st.markdown("#### Coverage")
    
    coverage_col1, coverage_col2, coverage_col3 = st.columns(3)
    with coverage_col1:
        ui_cov = coverage.get("ui_coverage", 0)
        st.markdown(f"""
        <div style="padding: 16px; background: rgba(30, 41, 59, 0.6); border-radius: 12px; text-align: center;">
            <div style="font-size: 28px; font-weight: 700; color: #6366f1;">{ui_cov:.1f}%</div>
            <div style="font-size: 11px; color: #64748b; text-transform: uppercase;">UI Coverage</div>
        </div>
        """, unsafe_allow_html=True)
    
    with coverage_col2:
        api_cov = coverage.get("api_coverage", 0)
        st.markdown(f"""
        <div style="padding: 16px; background: rgba(30, 41, 59, 0.6); border-radius: 12px; text-align: center;">
            <div style="font-size: 28px; font-weight: 700; color: #22d3ee;">{api_cov:.1f}%</div>
            <div style="font-size: 11px; color: #64748b; text-transform: uppercase;">API Coverage</div>
        </div>
        """, unsafe_allow_html=True)
    
    with coverage_col3:
        overall = coverage.get("overall", 0)
        st.markdown(f"""
        <div style="padding: 16px; background: rgba(30, 41, 59, 0.6); border-radius: 12px; text-align: center;">
            <div style="font-size: 28px; font-weight: 700; color: #10b981;">{overall:.1f}%</div>
            <div style="font-size: 11px; color: #64748b; text-transform: uppercase;">Overall</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Additional stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Risk Score", stats.get("risk_score", 0))
    with col2:
        st.metric("Automation Ready", f"{stats.get('automation_ready', 0):.1f}%")


# ============================================================================
# AI Discoveries Panel Component
# ============================================================================

def ai_discoveries_panel(discoveries: list[dict[str, Any]], title: str = "AI Discoveries") -> None:
    """Render AI discoveries panel."""
    st.markdown(f"### 🤖 {title}")
    
    # Summary badges
    col1, col2, col3 = st.columns(3)
    
    critical_count = sum(1 for d in discoveries if d.get("severity") == "critical")
    high_count = sum(1 for d in discoveries if d.get("severity") == "high")
    total_issues = sum(d.get("count", 0) for d in discoveries)
    
    with col1:
        st.metric("Critical", critical_count)
    with col2:
        st.metric("High", high_count)
    with col3:
        st.metric("Total Issues", total_issues)
    
    st.markdown("---")
    
    # Discovery cards
    type_icons = {
        "duplicate_ids": "🔄",
        "missing_labels": "🏷️",
        "accessibility": "♿",
        "performance": "⚡",
        "security": "🔒",
        "automation_risk": "⚠️",
        "missing_test_ids": "🔍",
        "dynamic_elements": "🔀",
        "suggestions": "💡",
    }
    
    severity_colors = {
        "critical": "#ef4444",
        "high": "#f59e0b",
        "medium": "#3b82f6",
        "low": "#64748b",
        "info": "#22d3ee",
    }
    
    for discovery in discoveries:
        icon = type_icons.get(discovery.get("type", ""), "📋")
        color = severity_colors.get(discovery.get("severity", "info"), "#64748b")
        
        st.markdown(f"""
        <div style="
            padding: 14px;
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid {color}30;
            border-radius: 10px;
            margin-bottom: 10px;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 24px;">{icon}</span>
                    <div>
                        <div style="font-size: 14px; color: #f8fafc; font-weight: 500;">
                            {discovery.get('type', 'Unknown').replace('_', ' ').title()}
                        </div>
                        <div style="font-size: 12px; color: #94a3b8;">
                            {discovery.get('description', '')}
                        </div>
                    </div>
                </div>
                <div style="
                    padding: 6px 12px;
                    background: {color}20;
                    border-radius: 6px;
                    font-size: 18px;
                    font-weight: 700;
                    color: {color};
                ">
                    {discovery.get('count', 0)}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# Quick Actions Panel Component
# ============================================================================

def quick_actions_panel(actions: list[dict[str, Any]], title: str = "Quick Actions") -> None:
    """Render quick actions panel."""
    st.markdown(f"### ⚡ {title}")
    
    # Group by category
    categories = {}
    for action in actions:
        cat = action.get("category", "other")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(action)
    
    category_names = {
        "explorer": "🔍 Explorer",
        "generation": "📝 Generation",
        "ai": "🤖 AI",
        "browser": "🌐 Browser",
        "analysis": "📊 Analysis",
    }
    
    for cat_name, cat_actions in categories.items():
        st.markdown(f"**{category_names.get(cat_name, cat_name)}**")
        
        cols = st.columns(3)
        for i, action in enumerate(cat_actions):
            with cols[i % 3]:
                if st.button(
                    f"{action['icon']} {action['name']}",
                    key=f"action_{action['id']}",
                    use_container_width=True,
                ):
                    st.info(f"Action: {action['name']}")
                    st.rerun()
        
        st.markdown("")


# ============================================================================
# Discovery Timeline Component
# ============================================================================

def discovery_timeline(timeline: list[dict[str, Any]], title: str = "Discovery Timeline") -> None:
    """Render discovery timeline."""
    st.markdown(f"### 📅 {title}")
    
    status_colors = {
        "completed": "#10b981",
        "in_progress": "#f59e0b",
        "pending": "#64748b",
    }
    
    for i, item in enumerate(timeline):
        color = status_colors.get(item.get("status", "pending"), "#64748b")
        is_last = i == len(timeline) - 1
        
        # Time formatting
        time_diff = datetime.now() - item.get("time", datetime.now())
        if time_diff < timedelta(hours=1):
            time_str = f"{int(time_diff.total_seconds() / 60)}m ago"
        elif time_diff < timedelta(days=1):
            time_str = f"{int(time_diff.total_seconds() / 3600)}h ago"
        else:
            time_str = f"{int(time_diff.days)}d ago"
        
        st.markdown(f"""
        <div style="display: flex; gap: 16px; margin-bottom: {0 if is_last else 16}px;">
            <div style="display: flex; flex-direction: column; align-items: center;">
                <div style="
                    width: 16px;
                    height: 16px;
                    border-radius: 50%;
                    background: {color};
                    box-shadow: 0 0 10px {color}50;
                "></div>
                {"<div style='width: 2px; flex: 1; background: linear-gradient(180deg, " + color + ", transparent);'></div>" if not is_last else ""}
            </div>
            <div style="flex: 1; padding-bottom: {16 if not is_last else 0}px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 14px; color: #f8fafc; font-weight: 500;">
                        Step {item['step']}: {item['name']}
                    </span>
                    <span style="font-size: 11px; color: #64748b;">{time_str}</span>
                </div>
                <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">
                    {item.get('details', '')}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# Inspector Tabs Component
# ============================================================================

def inspector_tabs(
    page: dict[str, Any],
    active_tab: str = "overview"
) -> str:
    """Render inspector tabs and return selected tab."""
    
    tabs = [
        ("overview", "📋 Overview"),
        ("forms", "📝 Forms"),
        ("buttons", "🔘 Buttons"),
        ("inputs", "📝 Inputs"),
        ("tables", "📊 Tables"),
        ("rules", "📜 Rules"),
        ("accessibility", "♿ Accessibility"),
        ("notes", "📝 Notes"),
    ]
    
    tab_labels = [t[1] for t in tabs]
    tab_keys = [t[0] for t in tabs]
    
    if active_tab not in tab_keys:
        active_tab = "overview"
    
    selected = st.radio(
        "Inspector",
        tab_labels,
        index=tab_keys.index(active_tab),
        horizontal=True,
        label_visibility="collapsed",
    )
    
    return tab_keys[tab_labels.index(selected)]


# ============================================================================
# Search Component
# ============================================================================

def global_search(
    pages: list[dict[str, Any]],
    on_search: Callable[[str], None]
) -> str:
    """Render global search input."""
    query = st.text_input(
        "🔍 Search pages, forms, components...",
        value=st.session_state.get("search_query", ""),
        placeholder="Search by name, URL, or component...",
        label_visibility="collapsed",
        key="explorer_search",
    )
    
    if query != st.session_state.get("search_query", ""):
        st.session_state.search_query = query
        on_search(query)
    
    return query


def filter_bar(
    categories: list[str],
    selected: str,
    on_change: Callable[[str], None]
) -> str:
    """Render filter bar."""
    
    cols = st.columns([1] + [1] * (len(categories) - 1) + [1])
    
    with cols[0]:
        selected = st.selectbox(
            "Filter",
            categories,
            index=categories.index(selected) if selected in categories else 0,
            label_visibility="collapsed",
        )
    
    with cols[-1]:
        if st.button("🔄 Reset"):
            selected = categories[0]
            on_change(selected)
    
    return selected
