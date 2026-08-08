Layout Audit — AI-QOS (generated)

Summary:
- Repo-wide grep found 429 layout-related matches across 44 files (fixed widths, min-width, 100vw, translateX, negative margins, `st.columns(...)`, etc.).
- 143 matches of explicit `width: Npx` / `min-width: Npx` across 32 files.

Top files with risky patterns (recommend prioritizing):
- `frontend/components/agent_components.py` — multiple `min-width:96px`, inline `width:NNpx` styles, many `st.columns(len(...))` calls.
- `frontend/components/dom_components.py` — inline widths for inputs and avatar boxes; `min-width` usages; timeline spacing using `margin-left`.
- `frontend/components/knowledge_graph_components.py` — `min-width:96px`, wide icons, fixed-width nodes.
- `frontend/components/reports_components.py` — fixed-size circular charts (`width:110px`), `min-width` in table cells, and wide tables.
- `frontend/components/release_advisor_components.py` — `width:120px` conic charts, `min-width` table cells.
- `frontend/components/execution_components.py` — many inline fixed sizes and container `height:100%` blocks.
- `frontend/views/*` (dashboard, application_explorer, explorer, reports_center, mission_planner, etc.) — frequent `st.columns(4,5,6,...)`, explicit multi-column layouts that may squeeze content.
- `frontend/components/agent_drawer.py` — drawer set to `width:650px` (uses `max-width:95vw` already, but keep an eye).

Immediate recommendations (safe, global):
1. Use the injected global CSS in `theme_config.py` (already applied) — it enforces `box-sizing` and prevents main containers from overflowing.
2. Replace rigid `st.columns(len(...))` or high-count `st.columns(8|10|12)` uses with `utils.responsive.metrics_row()` or `responsive_grid` or manual chunking to multiple rows.
3. Replace fixed `min-width:96px` for cards with `min-width:0` and rely on `.aiqos-kpi-grid` (new helper) for responsive wrapping.
4. Convert circular widgets that are purely decorative (width/height fixed) to use `max-width:110px; width:100%; aspect-ratio:1/1` where appropriate.
5. Ensure tables and code blocks keep `overflow-x:auto` and their containers don't use `width:100vw`.

Planned safe automated fixes (proposed):
- Replace `min-width:96px` in component templates with `min-width:0` (safe, prevents forcing column widths).
- Replace `st.columns(len(row))` patterns where used to render many items with `responsive.metrics_row()` or `responsive_grid(items, columns_desktop=4)`.
- Replace `width: Npx` on text containers (labels, inputs) like `width:200px` for search inputs with `max-width:200px` and `width:100%` inside a constrained parent; or change to `flex: 0 0 200px` for explicit sidebars.

Next actions I can run now (pick one):
- (A) Auto-apply the safe fixes across the top 15 offending files (replace `min-width:96px` -> `min-width:0`, convert `st.columns(len(...))` to `responsive.metrics_row()` where the call is clearly a metrics row). This will be conservative and aim to preserve behavior.
- (B) Produce a per-file patch list (diffs) for your review before applying.
- (C) Run the responsive visual test (snapshots) across the typical viewports and produce a regression report.

I can proceed with (A) and apply conservative automated fixes now. Reply with `A` to proceed, `B` to get diffs first, or `C` to run snapshot tests first.
