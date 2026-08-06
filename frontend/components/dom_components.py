"""DOM Intelligence Explorer Components for AI-QOS."""

from datetime import datetime
from typing import Any, Optional
import streamlit as st


# ============================================================================
# Session State Management
# ============================================================================

def init_dom_state() -> None:
    """Initialize DOM explorer session state."""
    defaults = {
        "dom_selected_node": "node_search_input",
        "dom_expanded_nodes": {"node_html", "node_body", "node_header", "node_main"},
        "dom_search_query": "",
        "dom_inspector_tab": "overview",
        "dom_hovered_node": None,
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def toggle_dom_node(node_id: str) -> None:
    """Toggle DOM tree node expansion."""
    if node_id in st.session_state.dom_expanded_nodes:
        st.session_state.dom_expanded_nodes.discard(node_id)
    else:
        st.session_state.dom_expanded_nodes.add(node_id)


def select_dom_node(node_id: str) -> None:
    """Select a DOM node for inspection."""
    st.session_state.dom_selected_node = node_id


# ============================================================================
# DOM Tree Component
# ============================================================================

def render_dom_node(node: dict[str, Any], level: int = 0) -> None:
    """Render a single DOM tree node."""
    node_id = node["id"]
    is_expanded = node_id in st.session_state.dom_expanded_nodes
    has_children = bool(node.get("children"))
    is_selected = st.session_state.dom_selected_node == node_id
    
    # Tag icons
    tag_icons = {
        "html": "🌐", "head": "📋", "body": "📦",
        "header": "🔝", "main": "⬜", "nav": "🧭",
        "section": "📐", "div": "▢", "form": "📝",
        "input": "⌨️", "button": "🔘", "table": "📊",
        "a": "🔗", "img": "🖼️", "span": "▭", "p": "¶",
        "h1": "H1", "h2": "H2", "h3": "H3",
        "label": "🏷️", "select": "▼", "option": "•",
        "dialog": "📫", "ul": "≡", "li": "•",
    }
    
    icon = tag_icons.get(node["tag"], "⬜")
    
    # Build attributes summary
    attrs = node.get("attributes", {})
    attr_parts = []
    if "id" in attrs:
        attr_parts.append(f'#{attrs["id"]}')
    if "data-testid" in attrs:
        attr_parts.append(f'[testid={attrs["data-testid"]}]')
    if "class" in attrs:
        classes = attrs["class"][:30] + "..." if len(attrs.get("class", "")) > 30 else attrs.get("class", "")
        attr_parts.append(f'.{classes}')
    
    attr_str = " ".join(attr_parts[:2])  # Limit display
    
    # Text preview
    text = node.get("text", "")
    if text and len(text) > 30:
        text = text[:30] + "..."
    text_display = f'"{text}"' if text else ""
    
    # Selection styling
    bg_color = "rgba(99, 102, 241, 0.2)" if is_selected else "transparent"
    border_left = "3px solid #6366f1" if is_selected else "3px solid transparent"
    
    # Node row
    col1, col2 = st.columns([1, 4])
    
    with col1:
        indent = "　　" * level
        # Expand/collapse or bullet
        prefix = "▼ " if (has_children and is_expanded) else "▶ " if has_children else "• "
        
        button_label = f"{indent}{prefix}{icon} {node['tag']}"
        if attr_str:
            button_label += f" {attr_str}"
        if text_display:
            button_label += f" {text_display}"
        
        # Truncate long labels
        if len(button_label) > 60:
            button_label = button_label[:57] + "..."
        
        if st.button(
            button_label,
            key=f"dom_{node_id}",
            use_container_width=True,
        ):
            if has_children:
                toggle_dom_node(node_id)
            select_dom_node(node_id)
            st.rerun()
    
    # Status badges
    with col2:
        badges = []
        
        # Has children indicator
        if has_children:
            child_count = len(node.get("children", []))
            badges.append(f'<span style="background:rgba(99,102,241,0.2);padding:2px 6px;border-radius:4px;font-size:10px;color:#818cf8;">{child_count}</span>')
        
        # Interactive indicator
        if node["tag"] in ["button", "a", "input", "select", "textarea"]:
            badges.append('<span style="background:rgba(34,211,238,0.2);padding:2px 6px;border-radius:4px;font-size:10px;color:#22d3ee;">interactive</span>')
        
        # Has testid
        if "data-testid" in attrs:
            badges.append('<span style="background:rgba(16,185,129,0.2);padding:2px 6px;border-radius:4px;font-size:10px;color:#10b981;">testid</span>')
        
        st.markdown(" " + " ".join(badges), unsafe_allow_html=True)
    
    # Render children
    if has_children and is_expanded:
        for child in node.get("children", []):
            render_dom_node(child, level + 1)


def dom_tree(tree_data: dict[str, Any], title: str = "DOM Tree") -> None:
    """Render the full DOM tree."""
    st.markdown(f"### 🌳 {title}")
    
    # Search
    search_query = st.text_input(
        "🔍 Search elements...",
        placeholder="Search by tag, ID, class, text...",
        label_visibility="collapsed",
        key="dom_tree_search",
    )
    
    if search_query:
        from utils.dom_data import search_elements
        results = search_elements(search_query)
        st.markdown(f"**Found {len(results)} matching elements**")
        
        for node in results[:10]:  # Show top 10
            render_dom_node({
                "id": node["id"],
                "tag": node["tag"],
                "attributes": node.get("attributes", {}),
                "text": node.get("text", ""),
                "children": [],
            })
    else:
        # Render full tree
        render_dom_node(tree_data)


# ============================================================================
# Browser Visualizer Component
# ============================================================================

def browser_visualizer(node: Optional[dict[str, Any]], title: str = "Live DOM") -> None:
    """Render the browser preview with element highlighting."""
    st.markdown(f"### 🌐 {title}")
    
    # Browser chrome
    st.markdown("""
    <style>
    .browser-chrome {
        background: linear-gradient(180deg, #2a2a2a 0%, #1a1a1a 100%);
        border-radius: 12px 12px 0 0;
        padding: 12px 16px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .browser-controls {
        display: flex;
        gap: 6px;
    }
    .browser-control {
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }
    .browser-url {
        flex: 1;
        background: #3a3a3a;
        border-radius: 6px;
        padding: 6px 12px;
        color: #888;
        font-size: 12px;
        font-family: monospace;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="browser-chrome">
        <div class="browser-controls">
            <div class="browser-control" style="background: #ff5f57;"></div>
            <div class="browser-control" style="background: #febc2e;"></div>
            <div class="browser-control" style="background: #28c840;"></div>
        </div>
        <div class="browser-url">https://shop.staging.example.com/products</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Preview area
    with st.container():
        # Mock page content
        st.markdown("""
        <div style="
            min-height: 400px;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-top: none;
            border-radius: 0 0 12px 12px;
            padding: 20px;
            position: relative;
        ">
            <!-- Header -->
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 16px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; margin-bottom: 16px;">
                <div style="display: flex; align-items: center; gap: 16px;">
                    <span style="font-size: 24px;">🏪</span>
                    <div style="display: flex; gap: 12px; font-size: 14px; color: #94a3b8;">
                        <span>Home</span>
                        <span style="color: #6366f1; font-weight: 600;">Products</span>
                        <span>Cart</span>
                    </div>
                </div>
                <div style="display: flex; gap: 8px; align-items: center;">
                    <input type="text" placeholder="Search products..." style="padding: 8px 12px; border-radius: 6px; border: 1px solid #334155; background: rgba(15, 23, 42, 0.8); color: #f8fafc; width: 200px;">
                    <button style="padding: 8px 16px; background: #6366f1; border: none; border-radius: 6px; color: white; cursor: pointer;">Search</button>
                </div>
            </div>
            
            <!-- Products Section -->
            <div style="margin-bottom: 16px;">
                <h2 style="color: #f8fafc; margin: 0 0 16px;">Our Products</h2>
                
                <div style="display: flex; gap: 8px; margin-bottom: 16px; padding: 12px; background: rgba(30, 41, 59, 0.4); border-radius: 8px;">
                    <select style="padding: 8px; border-radius: 6px; background: #1e293b; border: 1px solid #334155; color: #f8fafc;">
                        <option>All Categories</option>
                        <option>Electronics</option>
                    </select>
                    <input type="number" placeholder="Min" style="padding: 8px; width: 80px; border-radius: 6px; background: #1e293b; border: 1px solid #334155; color: #f8fafc;">
                    <input type="number" placeholder="Max" style="padding: 8px; width: 80px; border-radius: 6px; background: #1e293b; border: 1px solid #334155; color: #f8fafc;">
                    <button style="padding: 8px 16px; background: #6366f1; border: none; border-radius: 6px; color: white;">Apply</button>
                </div>
            </div>
            
            <!-- Product Grid -->
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px;">
                <div style="background: rgba(30, 41, 59, 0.6); border-radius: 12px; padding: 16px; border: 2px solid #6366f1; box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);">
                    <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(34, 211, 238, 0.2)); height: 120px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 48px; margin-bottom: 12px;">🎧</div>
                    <h3 style="color: #f8fafc; margin: 0 0 8px;">Wireless Headphones</h3>
                    <div style="color: #10b981; font-size: 18px; font-weight: 700; margin-bottom: 12px;">$99.99</div>
                    <div style="display: flex; gap: 8px;">
                        <button style="flex: 1; padding: 10px; background: #22d3ee; border: none; border-radius: 6px; color: #0f172a; font-weight: 600; cursor: pointer;">Add to Cart</button>
                        <button style="padding: 10px 12px; background: transparent; border: 1px solid #334155; border-radius: 6px; color: #94a3b8; cursor: pointer;">View</button>
                    </div>
                </div>
                <div style="background: rgba(30, 41, 59, 0.6); border-radius: 12px; padding: 16px;">
                    <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(34, 211, 238, 0.2)); height: 120px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 48px; margin-bottom: 12px;">⌚</div>
                    <h3 style="color: #f8fafc; margin: 0 0 8px;">Smart Watch</h3>
                    <div style="color: #10b981; font-size: 18px; font-weight: 700; margin-bottom: 12px;">$199.99</div>
                    <div style="display: flex; gap: 8px;">
                        <button style="flex: 1; padding: 10px; background: #22d3ee; border: none; border-radius: 6px; color: #0f172a; font-weight: 600; cursor: pointer;">Add to Cart</button>
                        <button style="padding: 10px 12px; background: transparent; border: 1px solid #334155; border-radius: 6px; color: #94a3b8; cursor: pointer;">View</button>
                    </div>
                </div>
            </div>
            
            <!-- Pagination -->
            <div style="display: flex; justify-content: center; gap: 8px; margin-top: 20px;">
                <button style="padding: 8px 16px; background: rgba(99, 102, 241, 0.3); border: none; border-radius: 6px; color: #94a3b8;">Previous</button>
                <button style="padding: 8px 16px; background: #6366f1; border: none; border-radius: 6px; color: white;">1</button>
                <button style="padding: 8px 16px; background: transparent; border: 1px solid #334155; border-radius: 6px; color: #94a3b8;">2</button>
                <button style="padding: 8px 16px; background: transparent; border: 1px solid #334155; border-radius: 6px; color: #94a3b8;">3</button>
                <button style="padding: 8px 16px; background: transparent; border: 1px solid #334155; border-radius: 6px; color: #94a3b8;">Next</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Element info overlay
    if node:
        st.markdown(f"""
        <div style="
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: rgba(15, 23, 42, 0.95);
            border: 1px solid #6366f1;
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 12px;
            color: #f8fafc;
        ">
            <div style="display: flex; gap: 16px;">
                <span><strong>Tag:</strong> {node.get('tag', 'unknown')}</span>
                <span><strong>Path:</strong> <code style="color: #22d3ee;">{node.get('xpath', 'N/A')[:50]}...</code></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Controls
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🔍 Zoom In", use_container_width=True):
            st.info("Zoom in")
    with col2:
        if st.button("🔍 Zoom Out", use_container_width=True):
            st.info("Zoom out")
    with col3:
        if st.button("📱 Fullscreen", use_container_width=True):
            st.info("Fullscreen mode")
    with col4:
        if st.button("📍 Toggle Grid", use_container_width=True):
            st.info("Toggle grid overlay")


# ============================================================================
# Element Inspector Component
# ============================================================================

def element_inspector(element: dict[str, Any], title: str = "Element Inspector") -> None:
    """Render detailed element inspector."""
    st.markdown(f"### 🔍 {title}")
    
    # Element basics
    st.markdown("#### Element")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; margin-bottom: 8px;">
            <div style="font-size: 11px; color: #64748b; text-transform: uppercase;">Tag</div>
            <div style="font-size: 16px; color: #22d3ee; font-family: monospace;">&lt;{element.get('tag', 'unknown')}&gt;</div>
        </div>
        """, unsafe_allow_html=True)
        
        if element.get("id"):
            st.markdown(f"""
            <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; margin-bottom: 8px;">
                <div style="font-size: 11px; color: #64748b; text-transform: uppercase;">ID</div>
                <div style="font-size: 14px; color: #10b981; font-family: monospace;">#{element.get('id', '')}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if element.get("role"):
            st.markdown(f"""
            <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; margin-bottom: 8px;">
                <div style="font-size: 11px; color: #64748b; text-transform: uppercase;">ARIA Role</div>
                <div style="font-size: 14px; color: #f59e0b; font-family: monospace;">[role={element.get('role', '')}]</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Classes
    if element.get("classes"):
        st.markdown("""
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; margin-bottom: 8px;">
            <div style="font-size: 11px; color: #64748b; text-transform: uppercase; margin-bottom: 4px;">Classes</div>
            <div style="font-family: monospace; font-size: 12px; color: #a78bfa; word-break: break-all;">
                {' '.join(f'.{c}' for c in element.get('classes', []))}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Text/Value
    if element.get("text"):
        st.markdown(f"""
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; margin-bottom: 8px;">
            <div style="font-size: 11px; color: #64748b; text-transform: uppercase;">Text</div>
            <div style="font-size: 14px; color: #f8fafc;">{element.get('text', '')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    if element.get("value"):
        st.markdown(f"""
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; margin-bottom: 8px;">
            <div style="font-size: 11px; color: #64748b; text-transform: uppercase;">Value</div>
            <div style="font-size: 14px; color: #f8fafc; font-family: monospace;">{element.get('value', '')}</div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# Locator Intelligence Component
# ============================================================================

def locator_intelligence(element: dict[str, Any], title: str = "AI Locator Intelligence") -> None:
    """Render locator intelligence panel."""
    st.markdown(f"### 🎯 {title}")
    
    from utils.dom_data import generate_locators
    
    locators = generate_locators(element)
    
    for i, loc in enumerate(locators):
        confidence_color = "#10b981" if loc["confidence"] >= 95 else "#f59e0b" if loc["confidence"] >= 80 else "#ef4444"
        reliability_color = "#10b981" if loc["reliability"] >= 90 else "#f59e0b" if loc["reliability"] >= 70 else "#ef4444"
        
        priority_badge = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"
        
        with st.expander(f"{priority_badge} {loc['type'].upper()} - {loc['confidence']}% confidence", expanded=i==0):
            st.markdown(f"""
            <div style="margin-bottom: 12px;">
                <div style="font-size: 11px; color: #64748b; text-transform: uppercase; margin-bottom: 4px;">CSS Locator</div>
                <code style="display: block; padding: 8px; background: rgba(15, 23, 42, 0.8); border-radius: 6px; font-size: 12px; color: #22d3ee; word-break: break-all;">
                    {loc['locator']}
                </code>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div style="padding: 8px; background: rgba(30, 41, 59, 0.6); border-radius: 6px; margin-bottom: 8px;">
                    <div style="font-size: 10px; color: #64748b;">Confidence</div>
                    <div style="font-size: 16px; font-weight: 700; color: {confidence_color};">{loc['confidence']}%</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div style="padding: 8px; background: rgba(30, 41, 59, 0.6); border-radius: 6px; margin-bottom: 8px;">
                    <div style="font-size: 10px; color: #64748b;">Dynamic Risk</div>
                    <div style="font-size: 14px; color: {'#10b981' if loc['dynamic_risk'] == 'Low' else '#f59e0b' if loc['dynamic_risk'] == 'Medium' else '#ef4444'};">{loc['dynamic_risk']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="padding: 8px; background: rgba(30, 41, 59, 0.6); border-radius: 6px; margin-bottom: 8px;">
                    <div style="font-size: 10px; color: #64748b;">Reliability</div>
                    <div style="font-size: 16px; font-weight: 700; color: {reliability_color};">{loc['reliability']}%</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div style="padding: 8px; background: rgba(30, 41, 59, 0.6); border-radius: 6px; margin-bottom: 8px;">
                    <div style="font-size: 10px; color: #64748b;">Healing Strategy</div>
                    <div style="font-size: 12px; color: #94a3b8;">{loc['healing_strategy']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Code snippets
            st.markdown("**Code Snippets**")
            code_col1, code_col2 = st.columns(2)
            with code_col1:
                st.code(loc.get("playwright", ""), language="python")
            with code_col2:
                st.code(loc.get("selenium", ""), language="python")
            
            # Copy buttons
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("📋 Copy CSS", key=f"copy_css_{i}"):
                    st.session_state[f"copied_{i}"] = "css"
            with c2:
                if st.button("📋 Copy Playwright", key=f"copy_pw_{i}"):
                    st.session_state[f"copied_{i}"] = "playwright"
            with c3:
                if st.button("📋 Copy Selenium", key=f"copy_se_{i}"):
                    st.session_state[f"copied_{i}"] = "selenium"


# ============================================================================
# Accessibility Inspector Component
# ============================================================================

def accessibility_inspector(element: dict[str, Any], title: str = "Accessibility") -> None:
    """Render accessibility inspector."""
    st.markdown(f"### ♿ {title}")
    
    from utils.dom_data import generate_accessibility_info
    
    a11y = generate_accessibility_info(element)
    
    # Score gauge
    score = a11y["score"]
    score_color = "#10b981" if score >= 90 else "#f59e0b" if score >= 70 else "#ef4444"
    
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; background: rgba(30, 41, 59, 0.6); border-radius: 12px; margin-bottom: 16px;">
        <div style="font-size: 48px; font-weight: 700; color: {score_color};">{score}</div>
        <div style="font-size: 14px; color: #64748b; text-transform: uppercase;">Accessibility Score</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Details
    col1, col2 = st.columns(2)
    with col1:
        st.metric("ARIA Label", a11y["aria_label"][:30] + "..." if len(a11y["aria_label"]) > 30 else a11y["aria_label"])
        st.metric("Keyboard Support", a11y["keyboard_support"])
    with col2:
        st.metric("ARIA Role", a11y["aria_role"])
        st.metric("Focus Manageable", "Yes" if a11y["focus_manageable"] else "No")
    
    # Issues
    if a11y["issues"]:
        st.markdown("#### ⚠️ Issues")
        for issue in a11y["issues"]:
            severity_colors = {"high": "#ef4444", "medium": "#f59e0b", "low": "#64748b"}
            color = severity_colors.get(issue["severity"], "#64748b")
            st.markdown(f"""
            <div style="padding: 10px; background: rgba(239, 68, 68, 0.1); border-left: 3px solid {color}; border-radius: 0 6px 6px 0; margin-bottom: 8px;">
                <span style="font-size: 12px; color: {color}; text-transform: uppercase;">{issue['severity']}</span>
                <span style="font-size: 13px; color: #f8fafc; margin-left: 8px;">{issue['issue']}</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Suggestions
    st.markdown("#### 💡 Suggestions")
    for suggestion in a11y["suggestions"]:
        icon = "✅" if suggestion.startswith("Good") else "💡"
        st.markdown(f"- {icon} {suggestion}")


# ============================================================================
# Automation Intelligence Component
# ============================================================================

def automation_intelligence(element: dict[str, Any], title: str = "Automation") -> None:
    """Render automation intelligence panel."""
    st.markdown(f"### 🤖 {title}")
    
    from utils.dom_data import generate_automation_info
    
    auto = generate_automation_info(element)
    
    # Difficulty badge
    difficulty_colors = {"Easy": "#10b981", "Moderate": "#f59e0b", "Complex": "#ef4444", "Very Complex": "#dc2626"}
    diff_color = difficulty_colors.get(auto["difficulty"], "#64748b")
    
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 16px; background: rgba(30, 41, 59, 0.6); border-radius: 12px; margin-bottom: 16px;">
        <div>
            <div style="font-size: 11px; color: #64748b; text-transform: uppercase;">Automation Difficulty</div>
            <div style="font-size: 24px; font-weight: 700; color: {diff_color};">{auto['difficulty']}</div>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 11px; color: #64748b; text-transform: uppercase;">Difficulty Score</div>
            <div style="font-size: 24px; font-weight: 700; color: {diff_color};">{auto['difficulty_score']}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        risk_color = "#10b981" if auto["flaky_risk"] == "Low" else "#f59e0b" if auto["flaky_risk"] == "Medium" else "#ef4444"
        st.markdown(f"""
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; text-align: center;">
            <div style="font-size: 10px; color: #64748b;">Flaky Risk</div>
            <div style="font-size: 16px; font-weight: 700; color: {risk_color};">{auto['flaky_risk']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        stability_color = "#10b981" if auto["locator_stability"] == "High" else "#f59e0b"
        st.markdown(f"""
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; text-align: center;">
            <div style="font-size: 10px; color: #64748b;">Locator Stability</div>
            <div style="font-size: 16px; font-weight: 700; color: {stability_color};">{auto['locator_stability']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; text-align: center;">
            <div style="font-size: 10px; color: #64748b;">Dynamic Content</div>
            <div style="font-size: 16px; font-weight: 700; color: {'#ef4444' if auto['dynamic_content'] else '#10b981'};">{'Yes' if auto['dynamic_content'] else 'No'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Wait Strategy
    st.markdown("#### ⏱️ Wait Strategy")
    st.markdown(f"- **{auto['wait_strategy']}**")
    st.markdown(f"- **Retry:** {auto['retry_strategy']}")
    
    # Expected Assertions
    st.markdown("#### ✅ Expected Assertions")
    for assertion in auto["expected_assertions"]:
        st.markdown(f"- {assertion}")


# ============================================================================
# DOM Metrics Component
# ============================================================================

def dom_metrics(metrics: dict[str, Any], title: str = "DOM Metrics") -> None:
    """Render DOM metrics dashboard."""
    st.markdown(f"### 📊 {title}")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Nodes", metrics["total_nodes"])
        st.metric("Forms", metrics["forms"])
    with col2:
        st.metric("Interactive", metrics["interactive_nodes"])
        st.metric("Buttons", metrics["buttons"])
    with col3:
        st.metric("Hidden", metrics["hidden_nodes"])
        st.metric("Inputs", metrics["inputs"])
    with col4:
        st.metric("Dynamic", metrics["dynamic_nodes"])
        st.metric("Tables", metrics["tables"])
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Links", metrics["links"])
        st.metric("ARIA Elements", metrics["aria_elements"])
    with col2:
        st.metric("Images", metrics["images"])
        st.metric("Shadow DOM", metrics["shadow_dom"])
    with col3:
        st.metric("Iframes", metrics["iframes"])


# ============================================================================
# AI Discoveries Component
# ============================================================================

def ai_discoveries(discoveries: list[dict[str, Any]], title: str = "AI Discoveries") -> None:
    """Render AI discoveries panel."""
    st.markdown(f"### 🤖 {title}")
    
    # Summary
    critical = sum(1 for d in discoveries if d["severity"] == "critical")
    high = sum(1 for d in discoveries if d["severity"] == "high")
    total = sum(d["count"] for d in discoveries)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Critical", critical)
    with col2:
        st.metric("High Priority", high)
    with col3:
        st.metric("Total Issues", total)
    
    st.markdown("---")
    
    type_icons = {
        "missing_ids": "🏷️",
        "missing_labels": "📝",
        "dynamic_elements": "🔄",
        "poor_locators": "⚠️",
        "accessibility_issues": "♿",
        "shadow_dom": "👻",
        "flaky_components": "📳",
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
        icon = type_icons.get(discovery["type"], "📋")
        color = severity_colors.get(discovery["severity"], "#64748b")
        
        with st.expander(f"{icon} {discovery['type'].replace('_', ' ').title()} ({discovery['count']})", expanded=discovery["severity"] in ["critical", "high"]):
            st.markdown(f"**Description:** {discovery['description']}")
            if discovery["elements"]:
                st.markdown(f"**Elements:** {', '.join(discovery['elements'][:5])}")


# ============================================================================
# Console Panel Component
# ============================================================================

def console_panel(logs: list[dict[str, Any]], title: str = "Console") -> None:
    """Render developer console panel."""
    st.markdown(f"### 💻 {title}")
    
    level_colors = {
        "info": "#64748b",
        "warn": "#f59e0b",
        "error": "#ef4444",
        "success": "#10b981",
    }
    
    level_icons = {
        "info": "ℹ️",
        "warn": "⚠️",
        "error": "❌",
        "success": "✅",
    }
    
    for log in logs:
        color = level_colors.get(log["level"], "#64748b")
        icon = level_icons.get(log["level"], "•")
        
        st.markdown(f"""
        <div style="
            display: flex;
            gap: 8px;
            padding: 8px;
            border-bottom: 1px solid rgba(148, 163, 184, 0.1);
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
        ">
            <span style="color: #64748b;">{log['time']}</span>
            <span style="color: {color};">{icon}</span>
            <span style="color: #f8fafc;">{log['message']}</span>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# Quick Actions Component
# ============================================================================

def quick_actions(title: str = "Quick Actions") -> None:
    """Render quick actions panel."""
    st.markdown(f"### ⚡ {title}")
    
    actions = [
        ("📋 Copy XPath", "Copy XPath to clipboard"),
        ("📋 Copy CSS", "Copy CSS selector"),
        ("📋 Copy Playwright", "Copy Playwright locator"),
        ("📋 Copy Selenium", "Copy Selenium locator"),
        ("🧪 Generate Test", "Generate test case"),
        ("📝 Generate Page Object", "Generate page object"),
        ("♿ Accessibility Test", "Generate accessibility test"),
        ("📊 Generate Report", "Generate analysis report"),
    ]
    
    cols = st.columns(2)
    for i, (label, tooltip) in enumerate(actions):
        with cols[i % 2]:
            if st.button(label, key=f"dom_action_{i}", use_container_width=True):
                st.info(tooltip)
                st.rerun()


# ============================================================================
# Element Relationship Graph Component
# ============================================================================

def element_relationship_graph(element_id: str, title: str = "Element Relationships") -> None:
    """Render element relationship graph."""
    st.markdown(f"### 🔗 {title}")
    
    from utils.dom_data import generate_relationship_graph
    
    relationships = generate_relationship_graph(element_id)
    
    if not relationships:
        st.info("No relationships found for this element.")
        return
    
    type_icons = {
        "form": "📝",
        "api": "🔗",
        "ui": "🖥️",
        "state": "📊",
        "validation": "✅",
        "service": "⚙️",
    }
    
    for rel in relationships:
        icon = type_icons.get(rel["type"], "•")
        st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            background: rgba(30, 41, 59, 0.6);
            border-radius: 8px;
            margin-bottom: 8px;
        ">
            <span style="font-size: 20px;">{icon}</span>
            <div style="flex: 1;">
                <div style="font-size: 14px; color: #f8fafc;">{rel['target']}</div>
                <div style="font-size: 12px; color: #94a3b8;">{rel['relationship']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# DOM Timeline Component
# ============================================================================

def dom_timeline(timeline: list[dict[str, Any]], title: str = "DOM Analysis Timeline") -> None:
    """Render DOM analysis timeline."""
    st.markdown(f"### 📅 {title}")
    
    status_colors = {
        "completed": "#10b981",
        "in_progress": "#f59e0b",
        "pending": "#64748b",
    }
    
    for i, item in enumerate(timeline):
        color = status_colors.get(item["status"], "#64748b")
        is_last = i == len(timeline) - 1
        
        # Time display
        time_diff = datetime.now() - item.get("time", datetime.now())
        if time_diff < timedelta(minutes=1):
            time_str = f"{int(time_diff.total_seconds())}s ago"
        elif time_diff < timedelta(hours=1):
            time_str = f"{int(time_diff.total_seconds() / 60)}m ago"
        else:
            time_str = f"{int(time_diff.total_seconds() / 3600)}h ago"
        
        st.markdown(f"""
        <div style="display: flex; gap: 12px; margin-bottom: {0 if is_last else 12}px;">
            <div style="display: flex; flex-direction: column; align-items: center;">
                <div style="
                    width: 12px;
                    height: 12px;
                    border-radius: 50%;
                    background: {color};
                "></div>
                {"<div style='width: 2px; flex: 1; background: linear-gradient(180deg, " + color + ", #334155);'></div>" if not is_last else ""}
            </div>
            <div style="flex: 1;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-size: 13px; color: #f8fafc; font-weight: 500;">
                        {item['name']}
                    </span>
                    <span style="font-size: 11px; color: #64748b;">{time_str}</span>
                </div>
                <div style="font-size: 11px; color: #94a3b8;">{item['details']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# AI Explanation Component
# ============================================================================

def ai_explanation(element: dict[str, Any], title: str = "AI Explanation") -> None:
    """Render AI-powered element explanation."""
    st.markdown(f"### 💡 {title}")
    
    tag = element.get("tag", "unknown")
    
    explanations = {
        "input": {
            "why": "Collects user input for forms and search functionality",
            "purpose": "User interaction and data collection",
            "priority": "High",
            "complexity": "Low",
            "impact": "Critical for user workflows",
        },
        "button": {
            "why": "Triggers actions and form submissions",
            "purpose": "User action initiation",
            "priority": "Critical",
            "complexity": "Low",
            "impact": "Core user interaction",
        },
        "form": {
            "why": "Groups related inputs and manages submission",
            "purpose": "Data collection and validation",
            "priority": "Critical",
            "complexity": "Medium",
            "impact": "Essential business logic",
        },
    }
    
    exp = explanations.get(tag, {
        "why": "Provides structure and content",
        "purpose": "UI composition",
        "priority": "Medium",
        "complexity": "Low",
        "impact": "Visual rendering",
    })
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px;">
            <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Why Important</div>
            <div style="font-size: 13px; color: #f8fafc; margin-top: 4px;">{}</div>
        </div>
        """.format(exp["why"]), unsafe_allow_html=True)
        
        st.markdown("""
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; margin-top: 8px;">
            <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Business Purpose</div>
            <div style="font-size: 13px; color: #f8fafc; margin-top: 4px;">{}</div>
        </div>
        """.format(exp["purpose"]), unsafe_allow_html=True)
    
    with col2:
        priority_colors = {"Critical": "#ef4444", "High": "#f59e0b", "Medium": "#3b82f6", "Low": "#64748b"}
        priority_color = priority_colors.get(exp["priority"], "#64748b")
        
        st.markdown(f"""
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px;">
            <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Testing Priority</div>
            <div style="font-size: 16px; font-weight: 700; color: {priority_color}; margin-top: 4px;">{exp['priority']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; margin-top: 8px;">
            <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Automation Complexity</div>
            <div style="font-size: 14px; color: #f8fafc; margin-top: 4px;">{exp['complexity']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommendation
    st.markdown("""
    <div style="padding: 14px; background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(34, 211, 238, 0.1)); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 10px; margin-top: 12px;">
        <div style="font-size: 11px; color: #64748b; text-transform: uppercase; margin-bottom: 6px;">AI Recommendation</div>
        <div style="font-size: 13px; color: #f8fafc;">
            This <code style="color: #22d3ee;">&lt;{}&gt;</code> element is critical for user interaction. 
            Ensure proper test coverage with both positive and negative test cases.
        </div>
    </div>
    """.format(tag), unsafe_allow_html=True)


# ============================================================================
# Search Component
# ============================================================================

def dom_search(on_search: callable = None) -> str:
    """Render DOM search input."""
    query = st.text_input(
        "🔍 Search DOM...",
        placeholder="Search by tag, ID, class, text, role...",
        label_visibility="collapsed",
        key="dom_search_input",
    )
    
    return query


from datetime import timedelta
