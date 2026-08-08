"""AI Release Advisor Components — Autonomous Release Decision Center.

Premium, token-driven components built exclusively on the AI-QOS UI Foundation
(themes/tokens.py + components/shared.py). All styling derives from design
tokens; no hardcoded colors, no duplicate CSS, no duplicate components.
Mock-data driven, frontend-only, backend-ready.
"""

from typing import Any, Optional
import streamlit as st
import plotly.graph_objects as go

try:
    from frontend.themes.tokens import (
        COLORS, SPACING, TYPOGRAPHY, BORDERS, SHADOWS, ANIMATIONS,
        get_status_color, get_confidence_color, get_health_color, get_priority_color,
    )
    from frontend.components.shared import (
        section_header, glass_panel, glass_card, metric_card as _shared_metric_card,
        status_badge, priority_badge, progress_bar, health_bar, confidence_bar,
        empty_state, spacer, divider, pulse_dot, timeline_item, notification,
    )
    from frontend.mock.release_advisor import (
        RA_HERO_KPIS, RA_SCORE_METRICS, RA_DECISION, RA_DECISION_SIGNALS,
        RA_DECISION_PATH, RA_QUALITY_GATES, RA_BLOCKERS, RA_APPROVALS,
        RA_RISKS, RA_RISK_PREDICTIONS, RA_COVERAGE, RA_BUSINESS_IMPACT,
        RA_RELEASE_COMPARISON, RA_RELEASE_HISTORY, RA_ROLLBACK,
        RA_SIMULATIONS, RA_RECOMMENDATIONS, RA_QUICK_ACTIONS,
        RA_BOTTOM_TABS, RA_HEATMAP_IMPACTS, RA_HEATMAP_PROBABILITIES,
    )
except ImportError:  # pragma: no cover - fallback for direct execution
    from themes.tokens import (
        COLORS, SPACING, TYPOGRAPHY, BORDERS, SHADOWS, ANIMATIONS,
        get_status_color, get_confidence_color, get_health_color, get_priority_color,
    )
    from shared import (
        section_header, glass_panel, glass_card, metric_card as _shared_metric_card,
        status_badge, priority_badge, progress_bar, health_bar, confidence_bar,
        empty_state, spacer, divider, pulse_dot, timeline_item, notification,
    )
    from mock.release_advisor import (
        RA_HERO_KPIS, RA_SCORE_METRICS, RA_DECISION, RA_DECISION_SIGNALS,
        RA_DECISION_PATH, RA_QUALITY_GATES, RA_BLOCKERS, RA_APPROVALS,
        RA_RISKS, RA_RISK_PREDICTIONS, RA_COVERAGE, RA_BUSINESS_IMPACT,
        RA_RELEASE_COMPARISON, RA_RELEASE_HISTORY, RA_ROLLBACK,
        RA_SIMULATIONS, RA_RECOMMENDATIONS, RA_QUICK_ACTIONS,
        RA_BOTTOM_TABS, RA_HEATMAP_IMPACTS, RA_HEATMAP_PROBABILITIES,
    )


# ============================================================================
# Token shortcuts
# ============================================================================

_SEMANTIC_COLORS = {
    "primary": COLORS.PRIMARY, "secondary": COLORS.SECONDARY, "accent": COLORS.ACCENT,
    "info": COLORS.INFO, "success": COLORS.SUCCESS, "warning": COLORS.WARNING,
    "error": COLORS.ERROR, "muted": COLORS.TEXT_MUTED,
}


def _hex_to_rgb(hex_color: str) -> str:
    h = hex_color.lstrip('#')
    return f"{int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}"


_SEMANTIC_RGB = {
    "primary": COLORS.PRIMARY_RGB, "secondary": COLORS.SECONDARY_RGB,
    "accent": COLORS.ACCENT_RGB, "info": COLORS.INFO_RGB, "success": COLORS.SUCCESS_RGB,
    "warning": COLORS.WARNING_RGB, "error": COLORS.ERROR_RGB,
    "muted": _hex_to_rgb(COLORS.TEXT_MUTED),
}

_GLASS_BG = f"linear-gradient(135deg, {COLORS.SURFACE} 0%, rgba({COLORS.PRIMARY_RGB}, 0.12) 100%)"
_GLASS_BORDER = f"rgba({COLORS.PRIMARY_RGB}, 0.25)"
_CHART_PAPER_BG = "rgba(0,0,0,0)"
_CHART_GRID = f"rgba({COLORS.BORDER_RGB}, 0.2)"


def _semantic(name: str) -> str:
    return _SEMANTIC_COLORS.get(name, COLORS.PRIMARY)


def _semantic_rgb(name: str) -> str:
    return _SEMANTIC_RGB.get(name, COLORS.PRIMARY_RGB)


def _risk_color(risk: str) -> str:
    return {"low": COLORS.SUCCESS, "medium": COLORS.WARNING,
            "high": COLORS.ERROR, "critical": COLORS.ERROR}.get(risk, COLORS.TEXT_MUTED)


def _gate_color(status: str) -> str:
    return {"pass": COLORS.SUCCESS, "warning": COLORS.WARNING,
            "fail": COLORS.ERROR, "not_run": COLORS.TEXT_MUTED}.get(status, COLORS.TEXT_MUTED)


def _escape(text: Any) -> str:
    if text is None:
        return ""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _apply_chart_theme(fig: go.Figure, height: int = 300, show_legend: bool = False) -> go.Figure:
    fig.update_layout(
        height=height, paper_bgcolor=_CHART_PAPER_BG, plot_bgcolor=_CHART_PAPER_BG,
        font=dict(color=COLORS.TEXT_PRIMARY, size=12), showlegend=show_legend,
        legend=dict(font=dict(color=COLORS.TEXT_PRIMARY), bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(showgrid=False, linecolor=_CHART_GRID),
        yaxis=dict(showgrid=True, gridcolor=f"rgba({COLORS.BORDER_RGB}, 0.1)", linecolor=_CHART_GRID),
        margin=dict(l=40, r=20, t=40, b=40),
    )
    return fig


# ============================================================================
# Session State
# ============================================================================

def init_release_advisor_state() -> None:
    """Initialize Release Advisor session state (additive keys only)."""
    defaults = {
        "ra_decision_view": "decision",
        "ra_selected_risk": 0,
        "ra_selected_flow": "Checkout",
        "ra_simulation": "Release",
        "ra_bottom_tab": "Overview",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ============================================================================
# Hero header
# ============================================================================

def release_hero_header() -> None:
    """Render the premium sticky glass hero header with KPI chips."""
    decision = RA_DECISION["decision"]
    dec_color = (COLORS.SUCCESS if decision == "GO"
                 else COLORS.WARNING if "RISKS" in decision else COLORS.ERROR)
    dec_rgb = _hex_to_rgb(dec_color)
    conf = RA_DECISION["confidence"]
    conf_color = get_confidence_color(conf)
    conf_rgb = _hex_to_rgb(conf_color)

    chips = "".join(
        f'<div style="display:flex;flex-direction:column;align-items:center;gap:2px;'
        f'padding:{SPACING.SPACE_2} {SPACING.SPACE_4};background:rgba({COLORS.SURFACE_RGB},0.7);'
        f'border:1px solid {_GLASS_BORDER};border-radius:{BORDERS.RADIUS_MD};min-width:96px;">'
        f'<span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};'
        f'text-transform:uppercase;letter-spacing:1px;">{_escape(k["label"])}</span>'
        f'<span style="color:{_semantic(k["color"])};font-size:{TYPOGRAPHY.FONT_SIZE_SM};'
        f'font-weight:600;display:flex;align-items:center;gap:4px;">'
        f'<span style="font-size:0.9rem;">{k["icon"]}</span>{_escape(str(k["value"]))}'
        f'</span></div>'
        for k in RA_HERO_KPIS
    )

    st.markdown(
        f"""
        <div style="
            background:{_GLASS_BG};border:1px solid {_GLASS_BORDER};
            border-radius:{BORDERS.RADIUS_XL};padding:{SPACING.SPACE_6};
            margin-bottom:{SPACING.SPACE_4};box-shadow:{SHADOWS.CARD};
            position:sticky;top:0;z-index:10;backdrop-filter:blur(12px);">
            <div style="display:flex;align-items:center;justify-content:space-between;
                        flex-wrap:wrap;gap:{SPACING.SPACE_4};margin-bottom:{SPACING.SPACE_4};">
                <div>
                    <div style="display:flex;align-items:center;gap:{SPACING.SPACE_2};margin-bottom:{SPACING.SPACE_2};">
                        <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">🏠 Dashboard</span>
                        <span style="color:{COLORS.TEXT_MUTED};">›</span>
                        <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">Release</span>
                        <span style="color:{COLORS.TEXT_MUTED};">›</span>
                        <span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">AI Decision Center</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:{SPACING.SPACE_3};flex-wrap:wrap;">
                        <h1 style="margin:0;font-size:{TYPOGRAPHY.FONT_SIZE_2XL};color:{COLORS.TEXT_PRIMARY};font-weight:600;">
                            🚀 AI Autonomous Release Decision Center
                        </h1>
                        <span style="display:inline-flex;align-items:center;gap:{SPACING.SPACE_2};
                                     padding:{SPACING.SPACE_1} {SPACING.SPACE_3};
                                     background:rgba({dec_rgb},0.2);color:{dec_color};
                                     border:1px solid rgba({dec_rgb},0.4);
                                     border-radius:{BORDERS.RADIUS_FULL};
                                     font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:600;">
                            <span style="width:8px;height:8px;border-radius:50%;background:{dec_color};animation:{ANIMATIONS.PULSE};"></span>
                            {_escape(decision)}
                        </span>
                        <span style="display:inline-flex;align-items:center;gap:{SPACING.SPACE_2};
                                     padding:{SPACING.SPACE_1} {SPACING.SPACE_3};
                                     background:rgba({conf_rgb},0.2);color:{conf_color};
                                     border:1px solid rgba({conf_rgb},0.4);
                                     border-radius:{BORDERS.RADIUS_FULL};
                                     font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;">
                            🧠 AI {conf}%
                        </span>
                    </div>
                    <p style="margin:{SPACING.SPACE_2} 0 0;color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">
                        Autonomous Release Control Center • v3.2.1 • Build #1247 • RC-3 • Last analysis 3m ago
                    </p>
                </div>
                <div style="display:flex;align-items:center;gap:{SPACING.SPACE_2};flex-wrap:wrap;">
                    <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};border:1px solid {COLORS.BORDER};border-radius:{BORDERS.RADIUS_MD};padding:{SPACING.SPACE_1} {SPACING.SPACE_3};" title="Search">🔍 Search…</span>
                    <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};border:1px solid {COLORS.BORDER};border-radius:{BORDERS.RADIUS_MD};padding:{SPACING.SPACE_1} {SPACING.SPACE_3};" title="Command palette">⌘K Command</span>
                    <span style="color:{COLORS.TEXT_MUTED};font-size:1rem;cursor:pointer;" title="Notifications">🔔</span>
                    <span style="color:{COLORS.TEXT_MUTED};font-size:1rem;cursor:pointer;" title="Fullscreen">⛶</span>
                </div>
            </div>
            <div style="display:flex;gap:{SPACING.SPACE_2};flex-wrap:wrap;">{chips}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# Release score strip
# ============================================================================

def _metric_card(title: str, value: str, subtitle: str = "", trend: str = "", icon: str = "📊") -> None:
    """Token-driven metric card (module-local, signature-compatible)."""
    if trend.startswith("+"):
        trend_color = COLORS.SUCCESS
    elif trend.startswith("-"):
        trend_color = COLORS.ERROR
    else:
        trend_color = COLORS.TEXT_MUTED
    st.markdown(f"""
    <div style="padding:{SPACING.SPACE_6};background:{_GLASS_BG};border:{BORDERS.WIDTH_THIN} solid {_GLASS_BORDER};
                border-radius:{BORDERS.RADIUS_LG};margin-bottom:{SPACING.SPACE_4};box-shadow:{SHADOWS.CARD};">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div>
                <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;letter-spacing:1px;margin-bottom:{SPACING.SPACE_2};">{_escape(title)}</div>
                <div style="font-size:{TYPOGRAPHY.FONT_SIZE_3XL};font-weight:700;color:{COLORS.TEXT_PRIMARY};font-family:{TYPOGRAPHY.FONT_MONO};">{_escape(str(value))}</div>
                {f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_SECONDARY};margin-top:{SPACING.SPACE_1};">{_escape(subtitle)}</div>' if subtitle else ''}
            </div>
            <div style="text-align:right;">
                <div style="font-size:{TYPOGRAPHY.FONT_SIZE_2XL};margin-bottom:{SPACING.SPACE_2};">{icon}</div>
                {f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_BASE};font-weight:600;color:{trend_color};">{trend}</div>' if trend else ''}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def release_score_strip() -> None:
    """Render the release score strip as a MetricCard grid."""
    for i in range(0, len(RA_SCORE_METRICS), 4):
        row = RA_SCORE_METRICS[i:i + 4]
        cols = st.columns(len(row))
        for col, m in zip(cols, row):
            with col:
                _metric_card(title=m["title"], value=m["value"],
                             subtitle=m.get("subtitle", ""), trend=m.get("trend", ""),
                             icon=m.get("icon", ""))


# ============================================================================
# AI Release Decision Center (the visual focus)
# ============================================================================

def ai_decision_center() -> None:
    """Render the large premium AI release decision card."""
    section_header("AI Release Decision Center", icon="🤖")
    d = RA_DECISION
    decision = d["decision"]
    dec_color = (COLORS.SUCCESS if decision == "GO"
                 else COLORS.WARNING if "RISKS" in decision else COLORS.ERROR)
    dec_rgb = _hex_to_rgb(dec_color)
    conf = d["confidence"]
    conf_color = get_confidence_color(conf)
    conf_rgb = _hex_to_rgb(conf_color)
    pct = conf

    blocking_count = len(d["blocking_issues"])
    nonblocking_count = len(d["non_blocking_issues"])
    evidence_count = len(d["evidence"])
    gate_count = sum(1 for g in RA_QUALITY_GATES if g["blocking"])
    approval_count = sum(1 for a in RA_APPROVALS if a["status"] != "approved")
    risk_count = len([r for r in RA_RISKS if r["status"] == "open"])

    col_decision, col_counters = st.columns([1, 2])
    with col_decision:
        st.markdown(f"""
        <div style="padding:{SPACING.SPACE_6};background:linear-gradient(135deg, rgba({dec_rgb},0.18), rgba({COLORS.SURFACE_RGB},0.6));
                    border:1px solid rgba({dec_rgb},0.4);border-radius:{BORDERS.RADIUS_XL};text-align:center;box-shadow:0 0 30px rgba({dec_rgb},0.15);">
            <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;margin-bottom:{SPACING.SPACE_2};">AI Verdict</div>
            <div style="font-size:{TYPOGRAPHY.FONT_SIZE_4XL};font-weight:800;color:{dec_color};margin-bottom:{SPACING.SPACE_2};">{_escape(decision)}</div>
            <div style="margin:0 auto;width:120px;height:120px;border-radius:50%;
                        background:conic-gradient({conf_color} {pct}%, rgba({COLORS.SURFACE_RGB},0.8) 0%);
                        display:flex;align-items:center;justify-content:center;
                        box-shadow:0 0 24px rgba({conf_rgb},0.3);">
                <div style="width:92px;height:92px;border-radius:50%;background:{COLORS.SURFACE};display:flex;align-items:center;justify-content:center;">
                    <span style="font-size:{TYPOGRAPHY.FONT_SIZE_XL};font-weight:700;color:{conf_color};">{conf}%</span>
                </div>
            </div>
            <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};margin-top:{SPACING.SPACE_2};text-transform:uppercase;">Confidence</div>
        </div>
        """, unsafe_allow_html=True)
    with col_counters:
        counters = [
            ("Evidence", evidence_count, COLORS.PRIMARY, "📊"),
            ("Blocking", blocking_count, COLORS.ERROR, "🚫"),
            ("Non-Blocking", nonblocking_count, COLORS.WARNING, "⚠️"),
            ("Failed Gates", gate_count, COLORS.ERROR, "🚦"),
            ("Pending Approvals", approval_count, COLORS.WARNING, "✍️"),
            ("Open Risks", risk_count, COLORS.WARNING, "⚠️"),
        ]
        cols = st.columns(3)
        for i, (label, count, color, icon) in enumerate(counters):
            with cols[i % 3]:
                c_rgb = _hex_to_rgb(color)
                st.markdown(f"""
                <div style="padding:{SPACING.SPACE_4};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};border-left:3px solid {color};margin-bottom:{SPACING.SPACE_2};">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};text-transform:uppercase;">{icon} {label}</span>
                        <span style="color:{color};font-size:{TYPOGRAPHY.FONT_SIZE_2XL};font-weight:700;">{count}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Reason + recommended action
    st.markdown(f"""
    <div style="padding:{SPACING.SPACE_4};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_LG};margin-top:{SPACING.SPACE_3};border-left:3px solid {dec_color};">
        <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;margin-bottom:{SPACING.SPACE_2};">Reason</div>
        <div style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_BASE};line-height:1.5;">{_escape(d["reason"])}</div>
        <div style="display:flex;gap:{SPACING.SPACE_4};margin-top:{SPACING.SPACE_3};flex-wrap:wrap;">
            <span style="color:{COLORS.TEXT_SECONDARY};">Business Impact: <span style="color:{COLORS.SUCCESS};font-weight:600;">{_escape(d["business_impact"])}</span></span>
            <span style="color:{COLORS.TEXT_SECONDARY};">Technical Impact: <span style="color:{COLORS.WARNING};font-weight:600;">{_escape(d["technical_impact"])}</span></span>
        </div>
    </div>
    <div style="padding:{SPACING.SPACE_4};background:rgba({_hex_to_rgb(COLORS.SUCCESS)},0.1);border:1px solid rgba({_hex_to_rgb(COLORS.SUCCESS)},0.3);border-radius:{BORDERS.RADIUS_MD};margin-top:{SPACING.SPACE_3};">
        <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">🧠 AI Recommendation</div>
        <div style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_BASE};margin-top:4px;">{_escape(d["recommended_action"])}</div>
    </div>
    """, unsafe_allow_html=True)

    # Evidence / blocking / non-blocking
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### Evidence")
        for ev in d["evidence"]:
            st.markdown(f'<div style="padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {COLORS.PRIMARY};"><span style="color:{COLORS.TEXT_PRIMARY};">📊 {_escape(ev)}</span></div>', unsafe_allow_html=True)
    with col2:
        st.markdown("#### Blocking Issues")
        for iss in d["blocking_issues"]:
            st.markdown(f'<div style="padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({COLORS.ERROR_RGB},0.1);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {COLORS.ERROR};"><span style="color:{COLORS.ERROR};">🚫 {_escape(iss)}</span></div>', unsafe_allow_html=True)
    with col3:
        st.markdown("#### Non-Blocking Issues")
        for iss in d["non_blocking_issues"]:
            st.markdown(f'<div style="padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({COLORS.WARNING_RGB},0.1);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {COLORS.WARNING};"><span style="color:{COLORS.WARNING};">⚠️ {_escape(iss)}</span></div>', unsafe_allow_html=True)


# ============================================================================
# Decision explanation
# ============================================================================

def decision_explanation() -> None:
    """Render AI reasoning / decision explanation."""
    section_header("Decision Explanation", icon="🧠")
    st.markdown("#### Quality & Risk Signals")
    cols = st.columns(4)
    for i, (key, sig) in enumerate(RA_DECISION_SIGNALS.items()):
        with cols[i % 4]:
            c = _semantic(sig["color"])
            icon = "✓" if sig["status"] == "pass" else "⚠" if sig["status"] == "warn" else "✗"
            st.markdown(f"""
            <div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {c};">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;">{_escape(sig["label"])}</span>
                    <span style="color:{c};font-size:{TYPOGRAPHY.FONT_SIZE_LG};">{icon}</span>
                </div>
                <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_SECONDARY};margin-top:4px;">{_escape(sig["detail"])}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("#### Decision Path")
    for i, step in enumerate(RA_DECISION_PATH):
        c = _semantic(step["color"])
        is_last = i == len(RA_DECISION_PATH) - 1
        st.markdown(
            f'<div style="display:flex;gap:{SPACING.SPACE_3};margin-bottom:{0 if is_last else SPACING.SPACE_3};">'
            f'<div style="display:flex;flex-direction:column;align-items:center;">'
            f'<div style="width:28px;height:28px;border-radius:50%;background:rgba({_hex_to_rgb(c)},0.2);'
            f'display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;color:{c};'
            f'border:1px solid rgba({_hex_to_rgb(c)},0.4);{"animation:" + ANIMATIONS.PULSE + ";" if i == len(RA_DECISION_PATH)-1 else ""}">{i+1}</div>'
            + ("" if is_last else f'<div style="width:2px;flex:1;background:linear-gradient(180deg,{c},{COLORS.BORDER});min-height:18px;"></div>')
            + f'</div>'
            f'<div><div style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_PRIMARY};font-weight:500;">{_escape(step["step"])}</div>'
            f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_SECONDARY};">{_escape(step["detail"])}</div></div></div>',
            unsafe_allow_html=True,
        )


# ============================================================================
# Quality gates
# ============================================================================

def quality_gates_panel(key_prefix: str = "ra") -> None:
    """Render the 11 quality gates matrix."""
    section_header("Quality Gates", icon="🚦")
    cols = st.columns(4)
    for i, gate in enumerate(RA_QUALITY_GATES):
        with cols[i % 4]:
            c = _gate_color(gate["status"])
            icon = "✅" if gate["status"] == "pass" else "⚠️" if gate["status"] == "warning" else "❌"
            block_badge = f'<span style="color:{COLORS.ERROR};font-size:{TYPOGRAPHY.FONT_SIZE_XS};font-weight:600;">BLOCKING</span>' if gate["blocking"] else ""
            st.markdown(f"""
            <div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {c};">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;">{icon} {_escape(gate["gate"])}</span>
                    {block_badge}
                </div>
                <div style="display:flex;justify-content:space-between;margin-top:{SPACING.SPACE_1};">
                    <span style="color:{c};font-weight:700;">{gate["score"]}</span>
                    <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">≥ {gate["threshold"]}</span>
                </div>
                <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};margin-top:4px;">👤 {_escape(gate["owner"])} • {_escape(gate["last_run"])}</div>
                <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_SECONDARY};margin-top:2px;">🧠 {_escape(gate["recommendation"])}</div>
            </div>
            """, unsafe_allow_html=True)


def blocking_gates_panel() -> None:
    """Render the dedicated blocker panel."""
    section_header(f"Blocking Gates ({len(RA_BLOCKERS)})", icon="🚫")
    for b in RA_BLOCKERS:
        c = _semantic(b["color"])
        st.markdown(f"""
        <div style="padding:{SPACING.SPACE_4};background:rgba({_hex_to_rgb(c)},0.1);border:1px solid rgba({_hex_to_rgb(c)},0.3);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_3};display:flex;justify-content:space-between;align-items:center;">
            <div>
                <div style="color:{COLORS.TEXT_PRIMARY};font-weight:600;font-size:{TYPOGRAPHY.FONT_SIZE_BASE};">🚫 {_escape(b["name"])}</div>
                <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};margin-top:4px;">{_escape(b["type"].upper())} • {_escape(b["detail"])}</div>
            </div>
            <div style="text-align:right;">
                <div style="color:{c};font-size:{TYPOGRAPHY.FONT_SIZE_XS};font-weight:600;text-transform:uppercase;">{_escape(b["severity"])}</div>
                <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">👤 {_escape(b["owner"])}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# Approval matrix
# ============================================================================

def approval_matrix_panel(key_prefix: str = "ra") -> None:
    """Render the approval matrix."""
    section_header("Approval Matrix", icon="✍️")
    approved = sum(1 for a in RA_APPROVALS if a["status"] == "approved")
    st.markdown(f'<div style="margin-bottom:{SPACING.SPACE_3};color:{COLORS.TEXT_SECONDARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">Approved <span style="color:{COLORS.SUCCESS};font-weight:600;">{approved}</span> / {len(RA_APPROVALS)}</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, a in enumerate(RA_APPROVALS):
        with cols[i % 4]:
            c = _semantic(a["color"])
            icon = "✅" if a["status"] == "approved" else "⏳" if a["status"] == "pending" else "⚠️"
            st.markdown(f"""
            <div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {c};">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;">{icon} {_escape(a["role"])}</span>
                </div>
                <div style="color:{COLORS.TEXT_SECONDARY};font-size:{TYPOGRAPHY.FONT_SIZE_XS};margin-top:2px;">👤 {_escape(a["name"])}</div>
                <div style="color:{c};font-size:{TYPOGRAPHY.FONT_SIZE_XS};font-weight:600;text-transform:uppercase;margin-top:2px;">{_escape(a["status"])}</div>
                <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};margin-top:4px;">🕐 {_escape(a["timestamp"])}</div>
                <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_SECONDARY};margin-top:2px;font-style:italic;">"{_escape(a["comment"])}"</div>
            </div>
            """, unsafe_allow_html=True)


# ============================================================================
# Risk intelligence + heatmap
# ============================================================================

def risk_intelligence_panel(key_prefix: str = "ra") -> None:
    """Render risk intelligence with selectable inspector."""
    section_header("Risk Intelligence", icon="⚠️")
    selected_idx = st.session_state.get("ra_selected_risk", 0)
    selected = RA_RISKS[selected_idx] if selected_idx < len(RA_RISKS) else RA_RISKS[0]

    col_list, col_detail = st.columns([2, 1])
    with col_list:
        for i, risk in enumerate(RA_RISKS):
            c = _semantic(risk["color"])
            is_sel = i == selected_idx
            bg = f"rgba({COLORS.PRIMARY_RGB},0.22)" if is_sel else f"rgba({COLORS.SURFACE_RGB},0.5)"
            border_w = "2px" if is_sel else "1px"
            st.markdown(f"""
            <div style="padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:{bg};border-left:{border_w} solid {c};border-radius:0 {BORDERS.RADIUS_MD} {BORDERS.RADIUS_MD} 0;margin-bottom:{SPACING.SPACE_1};">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;">{_escape(risk["risk"])}</span>
                    <div style="display:flex;gap:{SPACING.SPACE_2};">
                        <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">P:{risk["probability"]}%</span>
                        <span style="color:{c};font-size:{TYPOGRAPHY.FONT_SIZE_XS};font-weight:600;text-transform:uppercase;">{_escape(risk["severity"])}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Select", key=f"{key_prefix}_risk_sel_{i}", use_container_width=True, help=f"Inspect {risk['risk']}"):
                st.session_state.ra_selected_risk = i
                st.rerun()
    with col_detail:
        c = _semantic(selected["color"])
        st.markdown(f"""
        <div style="padding:{SPACING.SPACE_4};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_LG};border:1px solid rgba({_hex_to_rgb(c)},0.3);">
            <div style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_LG};font-weight:600;margin-bottom:{SPACING.SPACE_2};">{_escape(selected["risk"])}</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:{SPACING.SPACE_2};">
                <div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_MD};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Category</div><div style="color:{COLORS.TEXT_PRIMARY};font-weight:600;">{_escape(selected["category"])}</div></div>
                <div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_MD};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Probability</div><div style="color:{c};font-weight:700;">{selected["probability"]}%</div></div>
                <div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_MD};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Impact</div><div style="color:{COLORS.TEXT_PRIMARY};font-weight:600;">{_escape(selected["impact"])}</div></div>
                <div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_MD};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Severity</div><div style="color:{c};font-weight:700;text-transform:uppercase;">{_escape(selected["severity"])}</div></div>
                <div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_MD};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Owner</div><div style="color:{COLORS.TEXT_PRIMARY};font-weight:600;">{_escape(selected["owner"])}</div></div>
                <div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_MD};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Status</div><div style="color:{COLORS.TEXT_PRIMARY};font-weight:600;">{_escape(selected["status"])}</div></div>
            </div>
            <div style="margin-top:{SPACING.SPACE_2};font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_SECONDARY};"><strong>Mitigation:</strong> {_escape(selected["mitigation"])}</div>
            <div style="margin-top:{SPACING.SPACE_1};font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_SECONDARY};"><strong>🧠 AI:</strong> {_escape(selected["recommendation"])}</div>
        </div>
        """, unsafe_allow_html=True)


def risk_heatmap_panel(key_prefix: str = "ra") -> None:
    """Render the risk heatmap (probability vs impact)."""
    section_header("Risk Heatmap", icon="🔥")
    # Build matrix: rows = probability (low->critical bottom->top), cols = impact (low->critical)
    impact_levels = RA_HEATMAP_IMPACTS  # Low, Medium, High, Critical
    prob_levels = RA_HEATMAP_PROBABILITIES  # Low, Medium, High, Critical
    # color intensity by combined level
    def cell_color(prob, impact):
        idx = prob_levels.index(prob) + impact_levels.index(impact)
        if idx <= 1:
            return COLORS.SUCCESS
        if idx <= 3:
            return COLORS.WARNING
        return COLORS.ERROR
    # header row
    header = "".join(f'<th style="padding:{SPACING.SPACE_2};color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};text-transform:uppercase;">{imp}</th>' for imp in impact_levels)
    rows = ""
    for prob in reversed(prob_levels):  # Critical on top
        cells = ""
        for imp in impact_levels:
            cc = cell_color(prob, imp)
            risks_here = [r for r in RA_RISKS
                          if str(r["prob_level"]).lower() == prob.lower()
                          and str(r["impact_level"]).lower() == imp.lower()]
            count = len(risks_here)
            label = ", ".join(r["risk"].replace(" Risk", "") for r in risks_here) if risks_here else "—"
            cells += f'<td style="padding:{SPACING.SPACE_2};background:rgba({_hex_to_rgb(cc)},0.12);border:1px solid rgba({_hex_to_rgb(cc)},0.3);border-radius:{BORDERS.RADIUS_SM};text-align:center;min-width:90px;"><div style="color:{cc};font-weight:700;font-size:{TYPOGRAPHY.FONT_SIZE_LG};">{count}</div><div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">{_escape(label)}</div></td>'
        rows += f'<tr><td style="padding:{SPACING.SPACE_2};color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};text-transform:uppercase;font-weight:600;">{prob}</td>{cells}</tr>'
    st.markdown(f"""
    <div style="overflow-x:auto;">
        <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;margin-bottom:{SPACING.SPACE_2};text-align:center;">Impact →</div>
        <table style="width:100%;border-collapse:separate;border-spacing:4px;">
            <thead><tr><th></th>{header}</tr></thead>
            <tbody>{rows}</tbody>
        </table>
        <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;margin-top:{SPACING.SPACE_2};">↑ Probability</div>
    </div>
    """, unsafe_allow_html=True)


def ai_risk_prediction_panel() -> None:
    """Render AI risk prediction (mock predictive)."""
    section_header("AI Risk Prediction", icon="🔮")
    for pred in RA_RISK_PREDICTIONS:
        c = _semantic(pred["color"])
        st.markdown(f"""
        <div style="padding:{SPACING.SPACE_4};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_3};border-left:3px solid {c};">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:{SPACING.SPACE_2};">
                <span style="color:{COLORS.TEXT_PRIMARY};font-weight:600;font-size:{TYPOGRAPHY.FONT_SIZE_BASE};">🔮 {_escape(pred["failure"])}</span>
                <span style="color:{c};font-weight:700;font-size:{TYPOGRAPHY.FONT_SIZE_LG};">{pred["probability"]}%</span>
            </div>
            <div style="display:flex;gap:{SPACING.SPACE_4};flex-wrap:wrap;font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_SECONDARY};">
                <span>Impact: <span style="color:{COLORS.TEXT_PRIMARY};font-weight:600;">{_escape(pred["impact"])}</span></span>
                <span>Confidence: <span style="color:{COLORS.TEXT_PRIMARY};font-weight:600;">{pred["confidence"]}%</span></span>
                <span>Flow: <span style="color:{COLORS.TEXT_PRIMARY};font-weight:600;">{_escape(pred["affected_flow"])}</span></span>
                <span>Component: <span style="color:{COLORS.TEXT_PRIMARY};font-weight:600;">{_escape(pred["affected_component"])}</span></span>
            </div>
            <div style="margin-top:{SPACING.SPACE_2};font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_SECONDARY};">🧠 {_escape(pred["recommendation"])}</div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# Coverage intelligence
# ============================================================================

def coverage_intelligence_panel(key_prefix: str = "ra") -> None:
    """Render coverage intelligence (current vs previous vs target)."""
    section_header("Coverage Intelligence", icon="🧪")
    areas = [c["area"] for c in RA_COVERAGE]
    current = [c["current"] for c in RA_COVERAGE]
    previous = [c["previous"] for c in RA_COVERAGE]
    target = [c["target"] for c in RA_COVERAGE]
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Current", x=areas, y=current, marker_color=COLORS.PRIMARY))
    fig.add_trace(go.Bar(name="Previous", x=areas, y=previous, marker_color=COLORS.TEXT_MUTED))
    fig.add_trace(go.Scatter(name="Target", x=areas, y=target, mode="markers+lines",
                            marker=dict(color=COLORS.WARNING, size=10, symbol="line-ns-open"),
                            line=dict(color=COLORS.WARNING, dash="dash", width=2)))
    fig.update_layout(barmode="group")
    _apply_chart_theme(fig, height=320, show_legend=True)
    st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_coverage_chart")

    for c in RA_COVERAGE:
        col = _semantic(c["color"])
        gap = c["target"] - c["current"]
        gap_str = f'<span style="color:{COLORS.ERROR};">gap {gap}</span>' if gap > 0 else f'<span style="color:{COLORS.SUCCESS};">on target</span>'
        st.markdown(f"""
        <div style="padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {col};">
            <div style="display:flex;justify-content:space-between;">
                <span style="color:{COLORS.TEXT_PRIMARY};font-weight:500;">{_escape(c["area"])}</span>
                <div style="display:flex;gap:{SPACING.SPACE_3};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">
                    <span style="color:{COLORS.TEXT_MUTED};">prev {c["previous"]}</span>
                    <span style="color:{col};font-weight:600;">{c["current"]}</span>
                    <span style="color:{COLORS.TEXT_MUTED};">target {c["target"]}</span>
                    <span style="color:{COLORS.SUCCESS};">{_escape(c["trend"])}</span>
                    {gap_str}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# Business impact
# ============================================================================

def business_impact_panel(key_prefix: str = "ra") -> None:
    """Render business flow impact with selectable inspector."""
    section_header("Business Impact", icon="💼")
    flow_names = [f["flow"] for f in RA_BUSINESS_IMPACT]
    selected_name = st.session_state.get("ra_selected_flow", "Checkout")
    selected = next((f for f in RA_BUSINESS_IMPACT if f["flow"] == selected_name), RA_BUSINESS_IMPACT[0])

    col_list, col_detail = st.columns([2, 1])
    with col_list:
        for flow in RA_BUSINESS_IMPACT:
            c = _risk_color(flow["risk"])
            is_sel = flow["flow"] == selected_name
            bg = f"rgba({COLORS.PRIMARY_RGB},0.22)" if is_sel else f"rgba({COLORS.SURFACE_RGB},0.5)"
            border_w = "2px" if is_sel else "1px"
            block_badge = f'<span style="color:{COLORS.ERROR};font-size:{TYPOGRAPHY.FONT_SIZE_XS};font-weight:600;">BLOCKING</span>' if flow["blocking"] else ""
            st.markdown(f"""
            <div style="padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:{bg};border-left:{border_w} solid {c};border-radius:0 {BORDERS.RADIUS_MD} {BORDERS.RADIUS_MD} 0;margin-bottom:{SPACING.SPACE_1};">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};font-weight:500;">{flow["icon"]} {_escape(flow["flow"])}</span>
                    <div style="display:flex;gap:{SPACING.SPACE_2};align-items:center;">
                        {block_badge}
                        <span style="color:{c};font-size:{TYPOGRAPHY.FONT_SIZE_XS};font-weight:600;text-transform:uppercase;">{_escape(flow["risk"])}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Select", key=f"{key_prefix}_flow_sel_{flow['flow']}", use_container_width=True, help=f"Inspect {flow['flow']}"):
                st.session_state.ra_selected_flow = flow["flow"]
                st.rerun()
    with col_detail:
        c = _risk_color(selected["risk"])
        st.markdown(f"""
        <div style="padding:{SPACING.SPACE_4};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_LG};border:1px solid rgba({_hex_to_rgb(c)},0.3);">
            <div style="display:flex;align-items:center;gap:{SPACING.SPACE_2};margin-bottom:{SPACING.SPACE_3};">
                <span style="font-size:24px;">{selected["icon"]}</span>
                <span style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_LG};font-weight:600;">{_escape(selected["flow"])}</span>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:{SPACING.SPACE_2};">
                <div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_MD};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Coverage</div><div style="color:{COLORS.TEXT_PRIMARY};font-weight:700;">{selected["coverage"]}%</div></div>
                <div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_MD};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Pass Rate</div><div style="color:{COLORS.SUCCESS};font-weight:700;">{selected["pass_rate"]}%</div></div>
                <div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_MD};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Revenue Impact</div><div style="color:{COLORS.TEXT_PRIMARY};font-weight:600;">{_escape(selected["revenue_impact"])}</div></div>
                <div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_MD};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Customer Impact</div><div style="color:{COLORS.TEXT_PRIMARY};font-weight:600;">{_escape(selected["customer_impact"])}</div></div>
                <div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_MD};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Risk</div><div style="color:{c};font-weight:700;text-transform:uppercase;">{_escape(selected["risk"])}</div></div>
                <div style="padding:{SPACING.SPACE_2};background:rgba({COLORS.SURFACE_RGB},0.4);border-radius:{BORDERS.RADIUS_MD};"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">AI Confidence</div><div style="color:{COLORS.PRIMARY};font-weight:700;">{selected["confidence"]}%</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# Release comparison
# ============================================================================

def release_comparison_panel() -> None:
    """Render release comparison (current vs previous)."""
    section_header("Release Comparison", icon="⚖️")
    rc = RA_RELEASE_COMPARISON
    st.markdown(
        f'<div style="display:flex;justify-content:space-between;padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_4};">'
        f'<div><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Current</div>'
        f'<div style="color:{COLORS.SUCCESS};font-weight:600;">{_escape(rc["current"])}</div></div>'
        f'<div style="text-align:right;"><div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">Previous</div>'
        f'<div style="color:{COLORS.TEXT_SECONDARY};font-weight:600;">{_escape(rc["previous"])}</div></div></div>',
        unsafe_allow_html=True,
    )
    for m in rc["metrics"]:
        diff = m["current"] - m["previous"]
        if m["unit"] == "%":
            status = "improved" if diff > 0 else ("regressed" if diff < 0 else "unchanged")
        else:
            status = "improved" if diff < 0 else ("regressed" if diff > 0 else "unchanged")
        status_color = COLORS.SUCCESS if status == "improved" else COLORS.ERROR if status == "regressed" else COLORS.TEXT_MUTED
        arrow = "↑" if diff > 0 else "↓" if diff < 0 else "→"
        diff_disp = round(abs(diff), 2)
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {status_color};">
            <span style="color:{COLORS.TEXT_PRIMARY};font-weight:500;">{_escape(m["metric"])}</span>
            <div style="display:flex;gap:{SPACING.SPACE_4};align-items:center;">
                <span style="color:{COLORS.TEXT_SECONDARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{m["previous"]}{m["unit"]}</span>
                <span style="color:{COLORS.TEXT_MUTED};">→</span>
                <span style="color:{COLORS.TEXT_PRIMARY};font-weight:700;">{m["current"]}{m["unit"]}</span>
                <span style="color:{status_color};font-weight:600;font-size:{TYPOGRAPHY.FONT_SIZE_SM};">{arrow} {diff_disp}{m["unit"]}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# Release history timeline
# ============================================================================

def release_history_panel() -> None:
    """Render the release history timeline."""
    section_header("Release History", icon="📅")
    for i, step in enumerate(RA_RELEASE_HISTORY):
        c = _semantic(step["color"])
        is_last = i == len(RA_RELEASE_HISTORY) - 1
        st.markdown(
            f'<div style="display:flex;gap:{SPACING.SPACE_3};margin-bottom:{0 if is_last else SPACING.SPACE_3};">'
            f'<div style="display:flex;flex-direction:column;align-items:center;">'
            f'<div style="width:32px;height:32px;border-radius:50%;background:rgba({_hex_to_rgb(c)},0.2);'
            f'display:flex;align-items:center;justify-content:center;font-size:16px;border:1px solid rgba({_hex_to_rgb(c)},0.4);'
            f'{"animation:" + ANIMATIONS.PULSE + ";" if i == len(RA_RELEASE_HISTORY)-1 else ""}">{step["icon"]}</div>'
            + ("" if is_last else f'<div style="width:2px;flex:1;background:linear-gradient(180deg,{c},{COLORS.BORDER});min-height:20px;"></div>')
            + f'</div>'
            f'<div><div style="display:flex;gap:{SPACING.SPACE_3};">'
            f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_SM};color:{COLORS.TEXT_PRIMARY};font-weight:500;">{_escape(step["step"])}</span>'
            f'<span style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};">{_escape(step["time"])}</span></div>'
            f'<div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_SECONDARY};">{_escape(step["detail"])}</div></div></div>',
            unsafe_allow_html=True,
        )


# ============================================================================
# Rollback readiness
# ============================================================================

def rollback_readiness_panel() -> None:
    """Render the premium rollback readiness panel."""
    section_header("Rollback Readiness", icon="↩️")
    rb = RA_ROLLBACK
    status_color = COLORS.SUCCESS if rb["available"] else COLORS.ERROR
    status_rgb = _hex_to_rgb(status_color)
    conf_color = get_confidence_color(rb["confidence"])

    col_status, col_details = st.columns([1, 2])
    with col_status:
        pct = rb["confidence"]
        st.markdown(f"""
        <div style="padding:{SPACING.SPACE_6};background:linear-gradient(135deg, rgba({status_rgb},0.15), rgba({COLORS.SURFACE_RGB},0.6));border:1px solid rgba({status_rgb},0.3);border-radius:{BORDERS.RADIUS_XL};text-align:center;">
            <div style="font-size:{TYPOGRAPHY.FONT_SIZE_4XL};">↩️</div>
            <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XL};font-weight:700;color:{status_color};margin-top:{SPACING.SPACE_2};">{_escape(rb["status"])}</div>
            <div style="margin:{SPACING.SPACE_3} auto;width:110px;height:110px;border-radius:50%;background:conic-gradient({conf_color} {pct}%, rgba({COLORS.SURFACE_RGB},0.8) 0%);display:flex;align-items:center;justify-content:center;box-shadow:0 0 20px rgba({_hex_to_rgb(conf_color)},0.3);">
                <div style="width:84px;height:84px;border-radius:50%;background:{COLORS.SURFACE};display:flex;align-items:center;justify-content:center;">
                    <span style="font-size:{TYPOGRAPHY.FONT_SIZE_XL};font-weight:700;color:{conf_color};">{pct}%</span>
                </div>
            </div>
            <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">Rollback Confidence</div>
        </div>
        """, unsafe_allow_html=True)
    with col_details:
        checks = [
            ("Rollback Version", rb["version"], COLORS.PRIMARY),
            ("Estimated Recovery", rb["duration"], COLORS.SUCCESS),
            ("Database Compatible", "Yes" if rb["db_compatible"] else "No", COLORS.SUCCESS if rb["db_compatible"] else COLORS.ERROR),
            ("Migration Status", rb["migration_status"], COLORS.SUCCESS),
            ("Backup Status", rb["backup_status"], COLORS.SUCCESS),
            ("Dependency Compatible", "Yes" if rb["dependency_compatible"] else "No", COLORS.SUCCESS if rb["dependency_compatible"] else COLORS.ERROR),
            ("Rollback Risk", rb["risk"].upper(), _risk_color(rb["risk"])),
        ]
        cols = st.columns(4)
        for i, (label, value, color) in enumerate(checks):
            with cols[i % 4]:
                st.markdown(f"""
                <div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};border-left:3px solid {color};">
                    <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">{_escape(label)}</div>
                    <div style="color:{color};font-weight:700;font-size:{TYPOGRAPHY.FONT_SIZE_BASE};">{_escape(str(value))}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("#### Rollback Steps")
        for step in rb["steps"]:
            c = _semantic(step["color"])
            st.markdown(f"""
            <div style="padding:{SPACING.SPACE_2} {SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};margin-bottom:{SPACING.SPACE_2};display:flex;justify-content:space-between;align-items:center;border-left:3px solid {c};">
                <span style="color:{COLORS.TEXT_PRIMARY};">✅ {_escape(step["step"])}</span>
                <div style="display:flex;gap:{SPACING.SPACE_3};">
                    <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">⏱ {_escape(step["duration"])}</span>
                    <span style="color:{c};font-size:{TYPOGRAPHY.FONT_SIZE_XS};font-weight:600;text-transform:uppercase;">{_escape(step["status"])}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ============================================================================
# Release impact simulation
# ============================================================================

def release_impact_simulation(key_prefix: str = "ra") -> None:
    """Render mock release impact simulation."""
    section_header("Release Impact Simulation", icon="🎮")
    st.markdown(f'<div style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_SM};margin-bottom:{SPACING.SPACE_3};">UI simulation only — no real deployment or rollback is performed.</div>', unsafe_allow_html=True)
    options = list(RA_SIMULATIONS.keys())
    selected = st.radio("Choose action", options=options, horizontal=True, key=f"{key_prefix}_sim_radio", label_visibility="collapsed")
    st.session_state.ra_simulation = selected
    sim = RA_SIMULATIONS[selected]
    c = _semantic(sim["color"])
    c_rgb = _hex_to_rgb(c)

    st.markdown(f"""
    <div style="padding:{SPACING.SPACE_6};background:linear-gradient(135deg, rgba({c_rgb},0.15), rgba({COLORS.SURFACE_RGB},0.6));border:1px solid rgba({c_rgb},0.3);border-radius:{BORDERS.RADIUS_LG};margin-bottom:{SPACING.SPACE_3};">
        <div style="font-size:{TYPOGRAPHY.FONT_SIZE_LG};font-weight:700;color:{c};margin-bottom:{SPACING.SPACE_2};"> {_escape(selected)}</div>
        <div style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_BASE};line-height:1.5;">{_escape(sim["summary"])}</div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(5)
    fields = [
        ("Business Impact", sim["business_impact"], COLORS.SUCCESS),
        ("Technical Impact", sim["technical_impact"], COLORS.WARNING),
        ("Customer Impact", sim["customer_impact"], COLORS.SUCCESS),
        ("Risk", sim["risk"], _risk_color(sim["risk"].lower())),
        ("Est. Recovery", sim["estimated_recovery"], COLORS.PRIMARY),
    ]
    for i, (label, value, color) in enumerate(fields):
        with cols[i]:
            st.markdown(f"""
            <div style="padding:{SPACING.SPACE_3};background:rgba({COLORS.SURFACE_RGB},0.6);border-radius:{BORDERS.RADIUS_MD};text-align:center;border-left:3px solid {color};">
                <div style="font-size:{TYPOGRAPHY.FONT_SIZE_XS};color:{COLORS.TEXT_MUTED};text-transform:uppercase;">{_escape(label)}</div>
                <div style="color:{color};font-weight:700;font-size:{TYPOGRAPHY.FONT_SIZE_BASE};">{_escape(str(value))}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown(f'<div style="margin-top:{SPACING.SPACE_3};color:{COLORS.TEXT_SECONDARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};">🧠 Simulation confidence: <span style="color:{get_confidence_color(sim["confidence"])};font-weight:600;">{sim["confidence"]}%</span></div>', unsafe_allow_html=True)


# ============================================================================
# AI recommendations
# ============================================================================

def ai_recommendations_panel() -> None:
    """Render prioritized AI recommendations."""
    section_header("AI Recommendations", icon="💡")
    for rec in RA_RECOMMENDATIONS:
        c = _semantic(rec["color"])
        c_rgb = _hex_to_rgb(c)
        st.markdown(f"""
        <div style="padding:{SPACING.SPACE_4};background:rgba({COLORS.SURFACE_RGB},0.6);border-left:3px solid {c};border-radius:0 {BORDERS.RADIUS_MD} {BORDERS.RADIUS_MD} 0;margin-bottom:{SPACING.SPACE_3};">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:{SPACING.SPACE_2};">
                <span style="padding:2px 8px;background:rgba({c_rgb},0.2);color:{c};border-radius:{BORDERS.RADIUS_SM};font-size:{TYPOGRAPHY.FONT_SIZE_XS};font-weight:600;text-transform:uppercase;">{_escape(rec["priority"])}</span>
                <span style="color:{COLORS.TEXT_MUTED};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">AI confidence: {rec["confidence"]}%</span>
            </div>
            <div style="color:{COLORS.TEXT_PRIMARY};font-size:{TYPOGRAPHY.FONT_SIZE_BASE};margin-bottom:{SPACING.SPACE_1};"><strong>Finding:</strong> {_escape(rec["finding"])}</div>
            <div style="color:{COLORS.TEXT_SECONDARY};font-size:{TYPOGRAPHY.FONT_SIZE_SM};margin-bottom:{SPACING.SPACE_1};"><strong>Recommendation:</strong> {_escape(rec["recommendation"])}</div>
            <div style="color:{COLORS.SUCCESS};font-size:{TYPOGRAPHY.FONT_SIZE_XS};">Expected: {_escape(rec["expected"])}</div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# Quick actions
# ============================================================================

def release_quick_actions(key_prefix: str = "ra") -> None:
    """Render premium quick actions as glass buttons."""
    section_header("Quick Actions", icon="⚡")
    for i in range(0, len(RA_QUICK_ACTIONS), 4):
        row = RA_QUICK_ACTIONS[i:i + 4]
        cols = st.columns(len(row))
        for col, action in zip(cols, row):
            with col:
                if st.button(
                    f"{action['icon']} {action['name']}",
                    key=f"{key_prefix}_qa_{i}_{action['name']}",
                    use_container_width=True, help=action["description"],
                ):
                    st.toast(action["description"], icon=action["icon"])


# ============================================================================
# Bottom workspace tabs (lazy)
# ============================================================================

def bottom_workspace_tabs() -> None:
    """Render the bottom workspace tabs (lazy rendering)."""
    tabs = st.tabs(RA_BOTTOM_TABS)
    tab_map = dict(zip(RA_BOTTOM_TABS, tabs))
    with tab_map["Overview"]:
        ai_decision_center()
        spacer(1)
        decision_explanation()
        spacer(1)
        ai_recommendations_panel()
    with tab_map["Quality Gates"]:
        blocking_gates_panel()
        spacer(1)
        quality_gates_panel(key_prefix="ra_bottom_gates")
    with tab_map["Approvals"]:
        approval_matrix_panel(key_prefix="ra_bottom_approvals")
    with tab_map["Risks"]:
        risk_intelligence_panel(key_prefix="ra_bottom_risk")
        spacer(1)
        risk_heatmap_panel(key_prefix="ra_bottom_heatmap")
        spacer(1)
        ai_risk_prediction_panel()
    with tab_map["Coverage"]:
        coverage_intelligence_panel(key_prefix="ra_bottom_cov")
        spacer(1)
        business_impact_panel(key_prefix="ra_bottom_biz")
    with tab_map["History"]:
        release_history_panel()
        spacer(1)
        release_comparison_panel()
    with tab_map["Rollback"]:
        rollback_readiness_panel()
        spacer(1)
        release_impact_simulation(key_prefix="ra_bottom_sim")
