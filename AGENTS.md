# AI-QOS Repository Notes

## Tech Stack
- Streamlit frontend (`frontend/`), run with `python -m streamlit run frontend/app.py --server.port 12000`
- Plotly for graph/chart visualizations
- Python 3.13, deps in root `requirements.txt` (streamlit>=1.35, plotly>=5.22, streamlit-extras, pandas, numpy)

## Architecture
- `frontend/app.py` routes sidebar pages to `frontend/views/*.render_*` / `render_page` functions
- Enterprise UI Foundation = `frontend/components/shared.py` (glass_panel, section_header, metric_card,
  status_badge, empty_state, spacer, etc.) + `frontend/themes/tokens.py` (COLORS, SPACING, TYPOGRAPHY,
  BORDERS, SHADOWS, ANIMATIONS, get_health_color, get_confidence_color, get_status_color, get_priority_color)
- Premium modules (dom_explorer, agent_control_tower, etc.) follow the pattern in
  `frontend/components/dom_components.py`: a `*_header()` sticky glass hero + `*_kpi_strip()` MetricCard grid,
  token-driven styling via `_semantic()`/`_hex_to_rgb()` helpers, all hardcoded colors replaced by tokens.
- Module-specific mock surface data lives in `frontend/mock/<module>/__init__.py`; business data/logic in
  `frontend/utils/<module>_data.py`.

## Component preservation rule
When enhancing an existing module, preserve every public function name and signature verbatim.
Only ADD new functions (e.g. `kg_header`, `kg_kpi_strip`, `knowledge_health_panel`, `dependency_chain_panel`,
`bottom_workspace_tabs`). Session-state keys must stay identical; only ADD keys (e.g. `kg_bottom_tab`).

## Gotchas
- **Plotly 6.x rejects `paper_bgcolor='transparent'`** — crashes the whole page render. Use `rgba(0,0,0,0)`.
- **Streamlit 1.61 duplicate-element IDs**: when the same `plotly_chart` figure is rendered in two places
  (e.g. a chart in the center panel AND in a bottom tab), pass a unique `key=f"..._{title}"` to each
  `st.plotly_chart(...)` call, otherwise `StreamlitDuplicateElementId` is raised.
- **Module caching**: editing a component file while the server runs does NOT take effect until the server
  is restarted (Streamlit caches imported modules in sys.modules). Kill + relaunch to verify edits.
- `st.toast` requires a running ScriptRunContext (warns in bare mode, harmless).
- The app uses `use_container_width=True` widely; Streamlit 1.61 emits a deprecation warning suggesting
  `width='stretch'` — cosmetic, non-breaking, do not mass-refactor unless asked.

## Work host mapping
- Port 12000 -> https://work-1-trrqwxujqtptoqqj.prod-runtime.all-hands.dev/
- Port 12001 -> https://work-2-trrqwxujqtptoqqj.prod-runtime.all-hands.dev/

## Reports & Analytics (Executive Quality Intelligence Center) — Module 10
- Premium page routes via `app.py` -> `views/reports_center.render_reports_center()`.
- Component logic in `components/reports_components.py`; business/mock data in
  `utils/reports_data.py`; premium surface mock data in `mock/reports/__init__.py`.
- NOTE: the legacy `views/reports.py` (`📈 Reports` nav) is a separate page — out of scope.
- **Pre-existing latent bug (now fixed):** the view used `go.Figure()` but never imported
  `plotly.graph_objects as go`, crashing Quality/AI-Performance/Flaky tabs with `NameError: name 'go'`.
  Fix = `import plotly.graph_objects as go` at top of the view.
- **Duplicate-key collisions:** the Executive Workspace tab renders many components at the top
  level AND again inside `bottom_workspace_tabs`. Any component with keyed widgets
  (`st.plotly_chart key=`, `st.button key=`, `st.expander` without key, `st.selectbox key=`)
  MUST accept a `key_prefix` param and be passed distinct prefixes from each call site
  (e.g. `reports_exec_*` for the exec-workspace call, `reports_bottom_*` for the bottom-tab call).
  `quality_trend_center`, `coverage_intelligence`, `bug_intelligence`,
  `execution_intelligence`, `ai_performance_intelligence`, `report_library_panel`,
  `report_generator_panel`, `export_center`, `quality_risk_matrix_panel` all take `key_prefix`.
- Preserved signatures: `metric_card(title,value,subtitle,trend,icon)`,
  `metric_gauge(value,max_value,label,unit,color)`, `report_card(report,compact)`,
  `coverage_chart(data,title)`, `trend_chart(data,title,color)`, `pie_chart(data,title)`,
  `progress_bar_section(data,title)`, `data_table(data,columns,title)`,
  `risk_matrix(risks,title)`, `report_generator(templates)`,
  `scheduled_reports_table(scheduled)`, `export_panel()`, `ai_insights(insights)`,
  `comparison_chart(data,title)`. Module-local `metric_card` shadows shared `metric_card` —
  preserved intentionally to avoid breaking the view's call sites.
- Session-state keys preserved: `reports_selected_report`, `reports_date_range`,
  `reports_view_mode`. Additive: `reports_bottom_tab`, `reports_selected_flow`, `reports_trend_view`.

## AI Release Advisor (Autonomous Release Decision Center) — Module 11
- NEW premium page registered additively in `app.py`: nav `"🚀 Release Advisor" -> "release_advisor"`,
  import `from views.release_advisor import render_page as render_release_advisor`, route
  `elif current_page == "release_advisor": render_release_advisor()`. Purely additive — no existing
  route/menu item altered.
- Architecture: `views/release_advisor.py` (`render_page` + `main`) -> `components/release_advisor_components.py`
  (token-driven) -> `mock/release_advisor/__init__.py` (surface mock data, backend-ready contract).
- Other modules already referenced "Open Release Advisor" as a quick action — the nav item now exists.
- Entry points: `render_page()`, `main()`, `init_release_advisor_state()`.
- Session state (additive only): `ra_decision_view`, `ra_selected_risk`, `ra_selected_flow`,
  `ra_simulation`, `ra_bottom_tab`.
- Components with keyed widgets accept `key_prefix` to avoid collisions between the executive
  workspace call sites and `bottom_workspace_tabs` (same pattern as Reports):
  `quality_gates_panel`, `approval_matrix_panel`, `risk_intelligence_panel`, `risk_heatmap_panel`,
  `coverage_intelligence_panel`, `business_impact_panel`, `release_impact_simulation`,
  `release_quick_actions`. Exec workspace passes `ra_exec_*`; bottom tabs pass `ra_bottom_*`.
- **Risk heatmap gotcha:** mock `RA_RISKS` uses lowercase `prob_level`/`impact_level` (e.g. `"medium"`)
  while heatmap axes (`RA_HEATMAP_IMPACTS`/`RA_HEATMAP_PROBABILITIES`) use Title Case. Matching must
  be case-insensitive (`str(...).lower()`) or every cell shows count 0.
- Zero hardcoded colors — all via `COLORS.*`, `_semantic()`, `_hex_to_rgb()`, `get_*_color()` helpers.
- No new heavy deps; reuses Plotly (`plotly.graph_objects as go`) + shared components.

## Verification workflow for a Streamlit view
1. `python -c "...render_page()"` bare-render smoke test (catches exceptions, ignores ScriptRunContext warnings)
2. Launch `python -m streamlit run frontend/app.py --server.port 12000 --server.headless true`
3. Browser: navigate, click nav item, `browser_get_content` and grep server log for `Traceback`/error class
