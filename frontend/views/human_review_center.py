"""Human Review Center - AI-QOS."""
import streamlit as st
from components.review_components import (
    init_review_state,
    get_review_data,
    set_review_data,
    MOCK_ASSERTIONS,
    MOCK_EVIDENCE,
    MOCK_AI_REVIEW,
    review_header,
    review_action_buttons,
    evidence_panel,
    browser_comparison,
    ai_review_panel,
    review_timeline,
    bug_preview_panel,
    modification_panel,
    review_tabs,
)


def render_human_review_center() -> None:
    """Render the Human Review Center page."""
    init_review_state()
    
    # Page Header
    review_header(
        mission_name="E2E Regression v2.1",
        test_name=get_review_data("review_current_test"),
        step_name=get_review_data("review_current_step"),
        agent=get_review_data("review_agent"),
        confidence=get_review_data("review_confidence"),
        status=get_review_data("review_status"),
    )
    
    # Action Buttons
    review_action_buttons()
    
    st.markdown("<hr style='margin: 1.5rem 0; border-color: #334155;'>", unsafe_allow_html=True)
    
    # Main Content - Three Column Layout
    left_col, center_col, right_col = st.columns([1, 2, 1])
    
    # LEFT PANEL - Evidence
    with left_col:
        evidence_panel(
            expected="Dashboard loads with sidebar navigation visible",
            actual="Dashboard loads but sidebar navigation is hidden",
            assertions=MOCK_ASSERTIONS,
            exec_time="12.5s",
            confidence=get_review_data("review_confidence"),
        )
        
        # Review Timeline
        st.markdown("<br>", unsafe_allow_html=True)
        review_timeline()
    
    # CENTER PANEL - Browser View
    with center_col:
        browser_comparison(key_prefix="review_browser")
        
        # Review Tabs
        st.markdown("<br>", unsafe_allow_html=True)
        review_tabs()
    
    # RIGHT PANEL - AI Review
    with right_col:
        ai_review_panel(MOCK_AI_REVIEW)
    
    # Bottom Section - Panels
    st.markdown("<hr style='margin: 1.5rem 0; border-color: #334155;'>", unsafe_allow_html=True)
    
    # Bug Generation and Modification Panels
    col1, col2 = st.columns(2)
    
    with col1:
        if get_review_data("show_bug_panel", False):
            st.subheader("🐛 Generate Bug Report")
            bug_preview_panel()
        else:
            if st.button("🐛 Generate Bug Report", use_container_width=True):
                set_review_data("show_bug_panel", True)
    
    with col2:
        if get_review_data("show_modify_panel", False):
            st.subheader("✏️ Modify Test")
            modification_panel()
        else:
            if st.button("✏️ Modify Test", use_container_width=True):
                set_review_data("show_modify_panel", True)
