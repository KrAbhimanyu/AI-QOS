"""AI Release Advisor — Autonomous Release Decision Center.

Premium enterprise workspace reusing the AI-QOS UI Foundation (design tokens
from themes/tokens.py and shared components from components/shared.py).
Mock-data driven, frontend-only, backend-ready. Entry points: render_page(),
main().
"""

import streamlit as st

from components.release_advisor_components import (
    init_release_advisor_state,
    release_hero_header,
    release_score_strip,
    ai_decision_center,
    decision_explanation,
    quality_gates_panel,
    blocking_gates_panel,
    approval_matrix_panel,
    risk_intelligence_panel,
    risk_heatmap_panel,
    ai_risk_prediction_panel,
    coverage_intelligence_panel,
    business_impact_panel,
    release_comparison_panel,
    release_history_panel,
    rollback_readiness_panel,
    release_impact_simulation,
    ai_recommendations_panel,
    release_quick_actions,
    bottom_workspace_tabs,
)
from components.shared import section_header, spacer


def render_page() -> None:
    """Main page render function — entry point."""
    init_release_advisor_state()

    # Sticky glass Hero Header
    release_hero_header()

    # Release Score Strip (MetricCard grid)
    release_score_strip()
    spacer(1)

    # AI Release Decision Center (the visual focus)
    ai_decision_center()
    spacer(2)

    # Decision Explanation
    decision_explanation()
    spacer(2)

    # 3-column: Quality Gates | Risk Intelligence | AI Recommendation
    section_header("Release Intelligence", icon="🧩")
    col_a, col_b, col_c = st.columns(3, gap="medium")
    with col_a:
        quality_gates_panel(key_prefix="ra_exec_gates")
        spacer(1)
        blocking_gates_panel()
    with col_b:
        risk_intelligence_panel(key_prefix="ra_exec_risk")
        spacer(1)
        ai_risk_prediction_panel()
    with col_c:
        ai_recommendations_panel()

    st.markdown("---")

    # 3-column: Approval Matrix | Coverage | Release Impact
    section_header("Release Readiness", icon="🚀")
    col_a, col_b, col_c = st.columns(3, gap="medium")
    with col_a:
        approval_matrix_panel(key_prefix="ra_exec_approvals")
    with col_b:
        coverage_intelligence_panel(key_prefix="ra_exec_cov")
    with col_c:
        release_impact_simulation(key_prefix="ra_exec_sim")

    st.markdown("---")

    # Business impact + risk heatmap + release comparison
    section_header("Risk & Business Analysis", icon="📊")
    business_impact_panel(key_prefix="ra_exec_biz")
    spacer(1)
    risk_heatmap_panel(key_prefix="ra_exec_heatmap")
    spacer(1)
    release_comparison_panel()

    st.markdown("---")

    # Release history timeline
    release_history_panel()
    spacer(2)

    # Rollback readiness
    rollback_readiness_panel()
    spacer(2)

    # Bottom executive workspace (glass tabs)
    st.markdown("---")
    section_header("Decision Workspace", icon="🏢")
    bottom_workspace_tabs()
    spacer(2)

    # Quick Actions
    release_quick_actions(key_prefix="ra_exec_qa")


def main() -> None:
    """Entry point."""
    render_page()


if __name__ == "__main__":
    main()
