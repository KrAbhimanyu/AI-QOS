"""Human Review Center components for AI-QOS."""
import streamlit as st
from datetime import datetime
from typing import Optional, List, Dict, Any

from frontend.mock.reports import (
    MOCK_ASSERTIONS,
    MOCK_EVIDENCE,
    MOCK_AI_REVIEW,
)


# ============================================================================
# Session State Management
# ============================================================================

def init_review_state() -> None:
    """Initialize review session state."""
    defaults = {
        "review_current_test": "Login Flow - Dashboard Access",
        "review_current_step": "Verify Dashboard Loaded",
        "review_agent": "Frontend Agent",
        "review_confidence": 92,
        "review_status": "waiting",
        "review_evidence": {},
        "review_decision": None,
        "review_comments": [],
        "review_bug_draft": None,
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_review_data(key: str, default: Any = None) -> Any:
    """Get review data from session state."""
    return st.session_state.get(key, default)


def set_review_data(key: str, value: Any) -> None:
    """Set review data in session state."""
    st.session_state[key] = value


# ============================================================================
# Mock Data (imported from frontend.mock.reports)
# ============================================================================

# MOCK_ASSERTIONS, MOCK_EVIDENCE, MOCK_AI_REVIEW 
# are imported from frontend.mock.reports


# ============================================================================
# Review Header
# ============================================================================

def review_header(
    mission_name: str,
    test_name: str,
    step_name: str,
    agent: str,
    confidence: int,
    status: str,
) -> None:
    """Display review header with mission info."""
    status_colors = {
        "waiting": "#F59E0B",
        "approved": "#10B981",
        "failed": "#EF4444",
        "modified": "#6366F1",
    }
    status_color = status_colors.get(status, "#64748B")
    status_labels = {
        "waiting": "⏳ Waiting for Review",
        "approved": "✅ Approved",
        "failed": "❌ Failed",
        "modified": "🔄 Modified",
    }
    
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(30, 30, 63, 0.95) 100%);
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        ">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                        <span style="color: #64748B; font-size: 0.8rem;">🏠 Dashboard</span>
                        <span style="color: #64748B;">›</span>
                        <span style="color: #64748B; font-size: 0.8rem;">Reviews</span>
                        <span style="color: #64748B;">›</span>
                        <span style="color: #F1F5F9; font-size: 0.8rem;">{mission_name}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <h1 style="margin: 0; font-size: 1.5rem; color: #F1F5F9;">🔍 Human Review Center</h1>
                        <span style="
                            display: inline-flex;
                            align-items: center;
                            gap: 0.5rem;
                            padding: 0.35rem 0.75rem;
                            border-radius: 9999px;
                            font-size: 0.75rem;
                            background: {status_color}20;
                            color: {status_color};
                        ">
                            <span style="width: 8px; height: 8px; border-radius: 50%; background: {status_color};"></span>
                            {status_labels.get(status, status)}
                        </span>
                    </div>
                </div>
                
                <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
                    <div style="text-align: center; padding: 0.5rem 1rem; background: rgba(30, 30, 63, 0.8); border-radius: 8px;">
                        <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Test</p>
                        <p style="color: #F1F5F9; margin: 0; font-size: 0.85rem;">{test_name}</p>
                    </div>
                    <div style="text-align: center; padding: 0.5rem 1rem; background: rgba(30, 30, 63, 0.8); border-radius: 8px;">
                        <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Agent</p>
                        <p style="color: #6366F1; margin: 0; font-size: 0.85rem;">{agent}</p>
                    </div>
                    <div style="text-align: center; padding: 0.5rem 1rem; background: rgba(30, 30, 63, 0.8); border-radius: 8px;">
                        <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Confidence</p>
                        <p style="color: #10B981; margin: 0; font-size: 0.85rem;">{confidence}%</p>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def review_action_buttons() -> None:
    """Display review action buttons."""
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 1, 1, 1])
    
    with col1:
        if st.button("✅ Approve", type="primary", use_container_width=True):
            set_review_data("review_decision", "approved")
            st.success("✅ Test approved! Continuing execution...")
            st.rerun()
    
    with col2:
        if st.button("🔄 Retry", use_container_width=True):
            set_review_data("review_decision", "retry")
            st.info("🔄 Retrying test...")
            st.rerun()
    
    with col3:
        if st.button("❌ Fail", use_container_width=True):
            set_review_data("review_decision", "failed")
            st.error("❌ Test marked as failed")
            st.rerun()
    
    with col4:
        if st.button("✏️ Modify", use_container_width=True):
            set_review_data("show_modify_panel", True)
    
    with col5:
        if st.button("🐛 Bug", use_container_width=True):
            set_review_data("show_bug_panel", True)
    
    with col6:
        if st.button("⏭️ Skip", use_container_width=True):
            set_review_data("review_decision", "skipped")
            st.info("⏭️ Test skipped")
            st.rerun()
    
    with col7:
        if st.button("⏸️ Pause", use_container_width=True):
            st.warning("⏸️ Mission paused by user")


# ============================================================================
# Evidence Panel
# ============================================================================

def evidence_panel(
    expected: str,
    actual: str,
    assertions: List[Dict],
    exec_time: str,
    confidence: int,
) -> None:
    """Display evidence panel with expected/actual results."""
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(30, 30, 63, 0.95) 0%, rgba(99, 102, 241, 0.1) 100%);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 16px;
            padding: 1.5rem;
        ">
            <h4 style="color: #F1F5F9; margin: 0 0 1.25rem; font-size: 1rem;">📋 Evidence Summary</h4>
        """,
        unsafe_allow_html=True,
    )
    
    # Expected vs Actual
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            <div style="
                padding: 1rem;
                background: rgba(16, 185, 129, 0.1);
                border: 1px solid rgba(16, 185, 129, 0.3);
                border-radius: 12px;
            ">
                <p style="color: #10B981; margin: 0 0 0.5rem; font-size: 0.75rem; font-weight: 500;">✓ Expected Result</p>
                <p style="color: #F1F5F9; margin: 0; font-size: 0.9rem;">""" + expected + """</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col2:
        st.markdown(
            """
            <div style="
                padding: 1rem;
                background: rgba(99, 102, 241, 0.1);
                border: 1px solid rgba(99, 102, 241, 0.3);
                border-radius: 12px;
            ">
                <p style="color: #6366F1; margin: 0 0 0.5rem; font-size: 0.75rem; font-weight: 500;">📝 Actual Result</p>
                <p style="color: #F1F5F9; margin: 0; font-size: 0.9rem;">""" + actual + """</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Assertions
    st.markdown("<h4 style='color: #F1F5F9; margin: 1.5rem 0 1rem;'>✅ Assertions</h4>", unsafe_allow_html=True)
    
    for assertion in assertions:
        status_color = "#10B981" if assertion["status"] == "passed" else "#EF4444"
        status_icon = "✅" if assertion["status"] == "passed" else "❌"
        
        st.markdown(
            f"""
            <div style="
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 0.75rem 1rem;
                background: rgba(30, 30, 63, 0.8);
                border: 1px solid rgba(99, 102, 241, 0.2);
                border-radius: 8px;
                margin-bottom: 0.5rem;
            ">
                <div style="flex: 1;">
                    <p style="color: #F1F5F9; margin: 0 0 0.25rem; font-size: 0.85rem;">{assertion['name']}</p>
                    <p style="color: #64748B; margin: 0; font-size: 0.75rem;">
                        Expected: <span style="color: #10B981;">{assertion['expected']}</span> | 
                        Actual: <span style="color: #22D3EE;">{assertion['actual']}</span>
                    </p>
                </div>
                <span style="font-size: 1.25rem;">{status_icon}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    # Execution Info
    st.markdown("<h4 style='color: #F1F5F9; margin: 1.5rem 0 1rem;'>⏱️ Execution Details</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Execution Time", exec_time)
    with col2:
        passed = sum(1 for a in assertions if a["status"] == "passed")
        st.metric("Passed", f"{passed}/{len(assertions)}")
    with col3:
        st.metric("Confidence", f"{confidence}%")


# ============================================================================
# Browser Comparison View
# ============================================================================

def browser_comparison() -> None:
    """Display browser screenshot with full interactions."""
    # Browser Controls
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 2, 1, 1, 1])
    
    with col1:
        st.button("⬅️ Back", use_container_width=True)
    with col2:
        st.button("➡️ Forward", use_container_width=True)
    with col3:
        st.button("🔄 Refresh", use_container_width=True)
    with col4:
        st.selectbox("Zoom", ["50%", "75%", "100%", "125%", "150%"], label_visibility="collapsed")
    with col5:
        st.selectbox("Device", ["Desktop", "Tablet", "Mobile"], label_visibility="collapsed")
    with col6:
        st.button("⛶ Fullscreen", use_container_width=True)
    with col7:
        st.button("📐 Annotate", use_container_width=True)
    
    # Current URL Display
    st.markdown(
        """
        <div style="
            background: rgba(30, 30, 63, 0.8);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 8px;
            padding: 0.75rem 1rem;
            margin: 1rem 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        ">
            <span style="color: #64748B;">🔒</span>
            <span style="color: #F1F5F9; font-family: monospace;">https://demo.app/dashboard</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Browser Frame
    st.markdown(
        """
        <div style="
            background: #1a1a2e;
            border: 1px solid #334155;
            border-radius: 12px;
            overflow: hidden;
        ">
            <!-- Browser Chrome -->
            <div style="background: #2d2d44; padding: 0.75rem 1rem; display: flex; align-items: center; gap: 1rem;">
                <div style="display: flex; gap: 0.5rem;">
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: #EF4444;"></div>
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: #F59E0B;"></div>
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: #10B981;"></div>
                </div>
                <div style="flex: 1; background: #1a1a2e; border-radius: 6px; padding: 0.5rem 1rem;">
                    <span style="color: #94A3B8; font-size: 0.85rem;">https://demo.app/dashboard</span>
                </div>
            </div>
            
            <!-- Page Content with Annotations -->
            <div style="padding: 1.5rem; background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1a 100%); min-height: 350px; position: relative;">
                <!-- Dashboard Mock -->
                <div style="background: #1e1e3f; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <span style="color: #F1F5F9; font-size: 1.25rem; font-weight: 600;">📊 Dashboard</span>
                        <span style="background: rgba(99, 102, 241, 0.2); padding: 0.25rem 0.75rem; border-radius: 4px; color: #818CF8; font-size: 0.75rem;">Welcome, John</span>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 1rem; text-align: center;">
                            <p style="color: #10B981; margin: 0; font-size: 1.5rem; font-weight: 600;">247</p>
                            <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Active Users</p>
                        </div>
                        <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 8px; padding: 1rem; text-align: center;">
                            <p style="color: #6366F1; margin: 0; font-size: 1.5rem; font-weight: 600;">1.2K</p>
                            <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Revenue</p>
                        </div>
                        <div style="background: rgba(34, 211, 238, 0.1); border: 1px solid rgba(34, 211, 238, 0.3); border-radius: 8px; padding: 1rem; text-align: center;">
                            <p style="color: #22D3EE; margin: 0; font-size: 1.5rem; font-weight: 600;">89%</p>
                            <p style="color: #64748B; margin: 0; font-size: 0.7rem;">Growth</p>
                        </div>
                    </div>
                </div>
                
                <!-- Highlighted Element Annotation -->
                <div style="
                    position: absolute;
                    top: 180px;
                    left: 50%;
                    transform: translateX(-50%);
                    background: rgba(99, 102, 241, 0.2);
                    border: 2px solid #6366F1;
                    border-radius: 8px;
                    padding: 1rem 2rem;
                    box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
                    animation: pulse 2s infinite;
                ">
                    <span style="color: white; font-weight: 600;">Sidebar Menu</span>
                </div>
                
                <!-- AI Bounding Box -->
                <div style="
                    position: absolute;
                    top: 100px;
                    right: 30px;
                    background: rgba(16, 185, 129, 0.2);
                    border: 2px dashed #10B981;
                    border-radius: 4px;
                    padding: 0.5rem 1rem;
                    font-size: 0.7rem;
                    color: #10B981;
                ">
                    ✓ User Avatar
                </div>
            </div>
        </div>
        
        <style>
            @keyframes pulse {
                0%, 100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); }
                50% { box-shadow: 0 0 0 15px rgba(99, 102, 241, 0); }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # Interaction Timeline
    st.markdown("<h4 style='color: #F1F5F9; margin: 1.5rem 0 1rem;'>🔄 AI Actions</h4>", unsafe_allow_html=True)
    
    actions = [
        {"icon": "📍", "name": "Highlight Element", "detail": "Locating sidebar navigation", "status": "completed", "color": "#6366F1"},
        {"icon": "🖱️", "name": "AI Click", "detail": "Clicking sidebar toggle", "status": "completed", "color": "#10B981"},
        {"icon": "⌨️", "name": "Typing", "detail": "Entering search query", "status": "running", "color": "#22D3EE"},
        {"icon": "📜", "name": "Scroll", "detail": "Scrolling to bottom", "status": "pending", "color": "#64748B"},
        {"icon": "✅", "name": "Assertion", "detail": "Verifying element visible", "status": "pending", "color": "#64748B"},
    ]
    
    for action in actions:
        is_running = action["status"] == "running"
        st.markdown(
            f"""
            <div style="
                display: flex;
                align-items: center;
                gap: 1rem;
                padding: 0.75rem 1rem;
                background: rgba(30, 30, 63, 0.8);
                border: 1px solid rgba(99, 102, 241, 0.2);
                border-radius: 8px;
                margin-bottom: 0.5rem;
                {'animation: glow 2s infinite;' if is_running else ''}
            ">
                <div style="
                    width: 36px;
                    height: 36px;
                    border-radius: 8px;
                    background: {action['color']}20;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.25rem;
                ">{action['icon']}</div>
                <div style="flex: 1;">
                    <p style="color: #F1F5F9; margin: 0; font-size: 0.9rem; font-weight: 500;">{action['name']}</p>
                    <p style="color: #64748B; margin: 0.25rem 0 0; font-size: 0.75rem;">{action['detail']}</p>
                </div>
                <span style="
                    padding: 0.25rem 0.75rem;
                    border-radius: 4px;
                    font-size: 0.75rem;
                    background: {action['color']}20;
                    color: {action['color']};
                ">
                    {'⟳ Running' if is_running else '✓' if action['status'] == 'completed' else '○'}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown("<style>@keyframes glow { 0%, 100% { box-shadow: 0 0 5px rgba(34, 211, 238, 0.3); } 50% { box-shadow: 0 0 15px rgba(34, 211, 238, 0.6); } }</style>", unsafe_allow_html=True)
    
    # Annotation Legend
    st.markdown(
        """
        <div style="display: flex; gap: 1rem; margin-top: 1rem; padding: 0.75rem; background: rgba(51, 65, 85, 0.5); border-radius: 8px;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <div style="width: 12px; height: 12px; border: 2px solid #6366F1; border-radius: 2px;"></div>
                <span style="color: #94A3B8; font-size: 0.75rem;">AI Focus</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <div style="width: 12px; height: 12px; border: 2px dashed #10B981; border-radius: 2px;"></div>
                <span style="color: #94A3B8; font-size: 0.75rem;">Validated</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <div style="width: 12px; height: 12px; border: 2px solid #EF4444; border-radius: 2px;"></div>
                <span style="color: #94A3B8; font-size: 0.75rem;">Failed</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# AI Review Panel
# ============================================================================

def ai_review_panel(ai_review: Dict) -> None:
    """Display AI review findings."""
    conf_color = "#10B981" if ai_review["confidence"] >= 80 else "#F59E0B"
    
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(30, 30, 63, 0.95) 100%);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 16px;
            padding: 1.5rem;
            height: 100%;
        ">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.25rem;">
                <div style="
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #6366F1, #8B5CF6);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.25rem;
                ">🤖</div>
                <div>
                    <h4 style="color: #F1F5F9; margin: 0; font-size: 1rem;">AI Review</h4>
                    <p style="color: #64748B; margin: 0.25rem 0 0; font-size: 0.75rem;">Automated analysis</p>
                </div>
            </div>
            
            <!-- Current Observation -->
            <div style="margin-bottom: 1rem;">
                <p style="color: #64748B; margin: 0 0 0.5rem; font-size: 0.75rem;">💭 Current Observation</p>
                <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 8px; padding: 0.75rem;">
                    <p style="color: #F1F5F9; margin: 0; font-size: 0.85rem;">{ai_review['observation']}</p>
                </div>
            </div>
            
            <!-- Reasoning -->
            <div style="margin-bottom: 1rem;">
                <p style="color: #64748B; margin: 0 0 0.5rem; font-size: 0.75rem;">🧠 Reasoning</p>
                <p style="color: #94A3B8; margin: 0; font-size: 0.8rem;">{ai_review['reasoning']}</p>
            </div>
            
            <!-- Evidence -->
            <div style="margin-bottom: 1rem;">
                <p style="color: #64748B; margin: 0 0 0.5rem; font-size: 0.75rem;">📋 Evidence</p>
                {''.join([f'<p style="color: #10B981; margin: 0.25rem 0; font-size: 0.8rem;">▸ {e}</p>' for e in ai_review['evidence']])}
            </div>
            
            <!-- Confidence -->
            <div style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="color: #64748B; font-size: 0.75rem;">Confidence</span>
                    <span style="color: {conf_color}; font-weight: 600;">{ai_review['confidence']}%</span>
                </div>
                <div style="height: 6px; background: #334155; border-radius: 3px; overflow: hidden;">
                    <div style="width: {ai_review['confidence']}%; height: 100%; background: {conf_color}; border-radius: 3px;"></div>
                </div>
            </div>
            
            <!-- Suggested Action -->
            <div style="
                background: rgba(16, 185, 129, 0.1);
                border: 1px solid rgba(16, 185, 129, 0.3);
                border-radius: 8px;
                padding: 0.75rem;
                margin-bottom: 1rem;
            ">
                <p style="color: #10B981; margin: 0 0 0.5rem; font-size: 0.75rem; font-weight: 500;">→ Suggested Action</p>
                <p style="color: #94A3B8; margin: 0; font-size: 0.8rem;">{ai_review['suggested_action']}</p>
            </div>
            
            <!-- Potential Risks -->
            <div style="margin-bottom: 1rem;">
                <p style="color: #F59E0B; margin: 0 0 0.5rem; font-size: 0.75rem; font-weight: 500;">⚠️ Potential Risks</p>
                {''.join([f'<p style="color: #94A3B8; margin: 0.25rem 0; font-size: 0.8rem;">▸ {r}</p>' for r in ai_review['potential_risks']])}
            </div>
            
            <!-- Best Practices -->
            <div>
                <p style="color: #22D3EE; margin: 0 0 0.5rem; font-size: 0.75rem; font-weight: 500;">💡 Best Practices</p>
                {''.join([f'<p style="color: #94A3B8; margin: 0.25rem 0; font-size: 0.8rem;">▸ {b}</p>' for b in ai_review['best_practices']])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# Review Timeline
# ============================================================================

def review_timeline() -> None:
    """Display review timeline."""
    steps = [
        {"name": "Test Started", "status": "completed", "time": "10:00:25"},
        {"name": "Action Performed", "status": "completed", "time": "10:00:28"},
        {"name": "Validation", "status": "completed", "time": "10:00:32"},
        {"name": "Screenshot Captured", "status": "completed", "time": "10:00:35"},
        {"name": "Review Ready", "status": "completed", "time": "10:00:36"},
        {"name": "Waiting For User", "status": "active", "time": "Now"},
    ]
    
    st.markdown(
        """
        <div style="
            background: rgba(30, 30, 63, 0.8);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
        ">
            <h4 style="color: #F1F5F9; margin: 0 0 1.5rem; font-size: 1rem;">📅 Review Timeline</h4>
        """,
        unsafe_allow_html=True,
    )
    
    for i, step in enumerate(steps):
        is_last = i == len(steps) - 1
        status_colors = {"completed": "#10B981", "active": "#F59E0B", "pending": "#64748B"}
        color = status_colors.get(step["status"], "#64748B")
        icon = "✓" if step["status"] == "completed" else "●" if step["status"] == "active" else "○"
        
        st.markdown(
            f"""
            <div style="display: flex; gap: 1rem; margin-bottom: {0 if is_last else 1}rem;">
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <div style="
                        width: 28px;
                        height: 28px;
                        border-radius: 50%;
                        background: {color};
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: white;
                        font-size: 0.8rem;
                    ">{icon}</div>
                    {'' if is_last else f'<div style="width: 2px; flex: 1; min-height: 30px; background: {color}; margin-top: 0.5rem;"></div>'}
                </div>
                <div style="flex: 1; padding-bottom: {0 if is_last else 0.75}rem;">
                    <p style="color: {'#F1F5F9' if step['status'] != 'pending' else '#64748B'}; margin: 0 0 0.25rem; font-size: 0.85rem;">{step['name']}</p>
                    <p style="color: #64748B; margin: 0; font-size: 0.7rem;">{step['time']}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# Bug Preview Panel
# ============================================================================

def bug_preview_panel() -> None:
    """Display bug generation preview."""
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(30, 30, 63, 0.95) 100%);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 16px;
            padding: 1.5rem;
        ">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.25rem;">
                <div style="
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #EF4444, #F59E0B);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.25rem;
                ">🐛</div>
                <div>
                    <h4 style="color: #F1F5F9; margin: 0; font-size: 1rem;">Bug Report Preview</h4>
                    <p style="color: #64748B; margin: 0.25rem 0 0; font-size: 0.75rem;">Generated from failed assertion</p>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Bug fields
    bug_data = {
        "title": "Sidebar Navigation Not Visible After Login",
        "severity": "Medium",
        "priority": "P2",
        "labels": ["UI", "Navigation", "Regression"],
    }
    
    st.markdown(f"**Summary:** {bug_data['title']}", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Severity:** <span style='color: #F59E0B;'>{bug_data['severity']}</span>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"**Priority:** <span style='color: #F59E0B;'>{bug_data['priority']}</span>", unsafe_allow_html=True)
    
    st.markdown("**Labels:**", unsafe_allow_html=True)
    for label in bug_data["labels"]:
        st.markdown(
            f"<span style='display: inline-block; background: rgba(99, 102, 241, 0.2); color: #818CF8; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.75rem; margin-right: 0.5rem;'>{label}</span>",
            unsafe_allow_html=True,
        )
    
    st.markdown("---")
    st.markdown("**Description:**")
    st.text_area(
        "Bug Description",
        value="The sidebar navigation menu is not visible after successful login. Expected: Sidebar should be visible with all navigation items. Actual: Sidebar is hidden/not rendered.",
        height=100,
        label_visibility="collapsed",
    )
    
    st.markdown("**Steps to Reproduce:**")
    st.text_area(
        "Steps",
        value="1. Navigate to login page\n2. Enter valid credentials\n3. Click login button\n4. Observe dashboard",
        height=80,
        label_visibility="collapsed",
    )
    
    st.markdown("**Attachments:** 📷 Screenshot | 🎥 Video | 📄 Logs")
    
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# Modification Panel
# ============================================================================

def modification_panel() -> None:
    """Display modification options panel."""
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(30, 30, 63, 0.95) 100%);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 16px;
            padding: 1.5rem;
        ">
            <h4 style="color: #F1F5F9; margin: 0 0 1.25rem; font-size: 1rem;">✏️ Modify Test</h4>
        """,
        unsafe_allow_html=True,
    )
    
    # Edit Locator
    st.markdown("**🎯 Edit Locator:**")
    st.text_input("New XPath", value="//button[@id='sidebar-toggle']", label_visibility="collapsed")
    
    # Add Assertion
    st.markdown("**➕ Add Assertion:**")
    st.text_input("Assertion Name", placeholder="e.g., Verify sidebar visible", label_visibility="collapsed")
    
    # Remove Assertion
    st.markdown("**➖ Remove Assertion:**")
    assertions_list = ["Page Title Contains 'Dashboard'", "User Name Displayed", "Logout Button Visible", "Sidebar Navigation Present"]
    selected_assertion = st.selectbox("Select to remove", ["(Select assertion)"] + assertions_list, label_visibility="collapsed")
    if selected_assertion != "(Select assertion)":
        st.warning(f"❌ Will remove: {selected_assertion}")
    
    # Change Validation
    st.markdown("**🔄 Change Validation:**")
    st.selectbox("Validation Type", ["Equals", "Contains", "Exists", "Matches Regex"], label_visibility="collapsed")
    
    # Add Note
    st.markdown("**📝 Add Note:**")
    st.text_area("Note", placeholder="Add a note for the team...", height=60, label_visibility="collapsed")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("💾 Apply Changes", type="primary", use_container_width=True)
    with col2:
        st.button("↩️ Reset", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# Review Tabs
# ============================================================================

def review_tabs() -> None:
    """Display review tabs."""
    tabs = st.tabs(["📋 Overview", "🖥️ Browser", "📐 DOM", "🌐 Network", "💻 Console", "📝 Logs", "📷 Screenshots", "🎥 Video", "♿ Accessibility", "⚡ Performance"])
    
    with tabs[0]:
        st.markdown("### Test Overview")
        st.json({
            "test_name": "Login Flow - Dashboard Access",
            "status": "failed",
            "duration": "12.5s",
            "assertions": {"passed": 3, "failed": 1},
            "screenshots": 2,
        })
    
    with tabs[1]:
        st.markdown("### Browser View")
        browser_comparison()
    
    with tabs[2]:
        st.markdown("### DOM Structure")
        st.code("""
<div id="dashboard">
  <header>
    <h1>Dashboard</h1>
    <nav id="sidebar" class="hidden">
      <!-- Sidebar content -->
    </nav>
  </header>
  <main>
    <div class="metrics">
      <!-- Metrics cards -->
    </div>
  </main>
</div>
        """, language="html")
    
    with tabs[3]:
        st.markdown("### Network Requests")
        st.table({
            "Method": ["GET", "POST", "GET"],
            "URL": ["/api/user", "/api/auth", "/api/dashboard"],
            "Status": [200, 200, 200],
            "Duration": ["45ms", "234ms", "156ms"],
        })
    
    with tabs[4]:
        st.markdown("### Console Output")
        st.code("""
[INFO] Page loaded: /dashboard
[INFO] User authenticated: john@example.com
[INFO] Dashboard rendered
[INFO] Sidebar element found but hidden
[WARN] Assertion failed: sidebar.visible
        """, language="bash")
    
    with tabs[5]:
        st.markdown("### Execution Logs")
        st.markdown(
            """
            <div style="background: #0a0a0f; border-radius: 8px; padding: 1rem; font-family: monospace; font-size: 0.8rem;">
                <p style="color: #64748B; margin: 0;">[10:00:25] Test started</p>
                <p style="color: #64748B; margin: 0;">[10:00:26] Navigating to /login</p>
                <p style="color: #10B981; margin: 0;">[10:00:27] Login page loaded</p>
                <p style="color: #64748B; margin: 0;">[10:00:28] Entering credentials</p>
                <p style="color: #10B981; margin: 0;">[10:00:29] Authentication successful</p>
                <p style="color: #64748B; margin: 0;">[10:00:30] Navigating to /dashboard</p>
                <p style="color: #10B981; margin: 0;">[10:00:32] Dashboard loaded</p>
                <p style="color: #F59E0B; margin: 0;">[10:00:33] WARNING: Sidebar not visible</p>
                <p style="color: #EF4444; margin: 0;">[10:00:34] ASSERTION FAILED: sidebar.visible</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns(2)
        with col1:
            st.button("📥 Download Logs", use_container_width=True)
        with col2:
            st.button("🗑️ Clear Logs", use_container_width=True)
    
    with tabs[6]:
        st.markdown("### Screenshots")
        col1, col2, col3 = st.columns(3)
        screenshots = [
            ("Before Login", "10:00:27"),
            ("After Login", "10:00:30"),
            ("Dashboard", "10:00:35"),
        ]
        for col, (name, time) in zip([col1, col2, col3], screenshots):
            with col:
                st.image(f"https://via.placeholder.com/200x150/1E1E3F/6366F1?text={name.replace(' ', '+')}")
                st.caption(f"{name} - {time}")
        st.markdown("**Screenshot Comparison:**")
        st.checkbox("Show side-by-side comparison")
        st.checkbox("Highlight differences")
    
    with tabs[7]:
        st.markdown("### Video Recording")
        st.markdown(
            """
            <div style="background: rgba(30, 30, 63, 0.8); border-radius: 12px; padding: 2rem; text-align: center;">
                <span style="font-size: 4rem;">🎥</span>
                <p style="color: #F1F5F9; margin: 1rem 0;">Video Recording Available</p>
                <p style="color: #64748B; margin: 0;">Duration: 00:34 seconds</p>
                <p style="color: #64748B; margin: 0;">Size: 2.4 MB</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("▶️ Play", use_container_width=True)
        with col2:
            st.button("📥 Download", use_container_width=True)
        with col3:
            st.button("🔗 Share", use_container_width=True)
    
    with tabs[8]:
        st.markdown("### Accessibility")
        st.table({
            "Check": ["Contrast Ratio", "ARIA Labels", "Keyboard Nav", "Focus Order", "Screen Reader"],
            "Status": ["✅ Pass", "⚠️ Warning", "✅ Pass", "✅ Pass", "⚠️ Warning"],
            "Details": ["4.5:1", "Missing on 2 elements", "Fully supported", "Correct order", "Partial support"],
        })
        st.markdown("**Missing ARIA Labels:**")
        st.markdown("- `#sidebar-toggle` button")
        st.markdown("- `.metrics-card` container")
    
    with tabs[9]:
        st.markdown("### Performance Metrics")
        col1, col2, col3, col4 = st.columns(4)
        metrics = [
            ("⏱️ Load Time", "1.2s", "#10B981"),
            ("📊 Page Size", "2.4 MB", "#6366F1"),
            ("🖼️ Requests", "24", "#22D3EE"),
            ("⚡ Score", "94", "#10B981"),
        ]
        for col, (label, value, color) in zip([col1, col2, col3, col4], metrics):
            with col:
                st.markdown(
                    f"""
                    <div style="text-align: center; padding: 1rem; background: rgba(30, 30, 63, 0.8); border-radius: 8px;">
                        <p style="color: #64748B; margin: 0; font-size: 0.75rem;">{label}</p>
                        <p style="color: {color}; margin: 0.5rem 0 0; font-size: 1.5rem; font-weight: 600;">{value}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.markdown("**Resource Breakdown:**")
        st.progress(0.45, text="JavaScript: 45%")
        st.progress(0.30, text="Images: 30%")
        st.progress(0.15, text="CSS: 15%")
        st.progress(0.10, text="HTML: 10%")
