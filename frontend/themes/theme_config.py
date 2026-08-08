"""Theme configuration for AI-QOS dark theme."""

THEME_CONFIG: dict = {
    "theme": {
        "primaryColor": "#6366F1",
        "backgroundColor": "#0F0F23",
        "secondaryBackgroundColor": "#1E1E3F",
        "textColor": "#E2E8F0",
        "font": "Inter",
    },
    "custom_css": """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary: #6366F1;
        --primary-light: #818CF8;
        --primary-dark: #4F46E5;
        --secondary: #22D3EE;
        --accent: #F472B6;
        --success: #10B981;
        --warning: #F59E0B;
        --error: #EF4444;
        --background: #0F0F23;
        --surface: #1E1E3F;
        --surface-hover: #2A2A4A;
        --border: #334155;
        --text-primary: #F1F5F9;
        --text-secondary: #94A3B8;
        --text-muted: #64748B;
        --radius: 12px;
        --radius-sm: 8px;
        --shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        --glass: rgba(30, 30, 63, 0.8);
        --glass-border: rgba(99, 102, 241, 0.2);
    }
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0F0F23 0%, #1A1A2E 100%);
    }
    
    div[data-testid="stSidebar"] {
        background: rgba(15, 15, 35, 0.95);
        border-right: 1px solid var(--border);
    }
    
    div[data-testid="stToolbar"] {
        background: var(--background);
    }
    
    .aiqos-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.5rem;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }
    
    .aiqos-card:hover {
        border-color: var(--primary);
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.15);
    }
    
    .aiqos-metric-card {
        background: linear-gradient(135deg, var(--surface) 0%, rgba(99, 102, 241, 0.1) 100%);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.5rem;
        text-align: center;
    }
    
    .aiqos-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .aiqos-badge-success {
        background: rgba(16, 185, 129, 0.2);
        color: #10B981;
    }
    
    .aiqos-badge-warning {
        background: rgba(245, 158, 11, 0.2);
        color: #F59E0B;
    }
    
    .aiqos-badge-error {
        background: rgba(239, 68, 68, 0.2);
        color: #EF4444;
    }
    
    .aiqos-badge-info {
        background: rgba(99, 102, 241, 0.2);
        color: #6366F1;
    }
    
    .aiqos-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
    }
    
    .aiqos-subheader {
        font-size: 1rem;
        font-weight: 500;
        color: var(--text-secondary);
    }
    
    div[data-testid="stMetric"] {
        background: var(--surface);
        padding: 1rem;
        border-radius: var(--radius);
        border: 1px solid var(--border);
    }
    
    div[data-testid="stMetricLabel"] {
        color: var(--text-secondary);
    }
    
    div[data-testid="stMetricValue"] {
        color: var(--primary);
        font-weight: 600;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: var(--surface);
        padding: 0.5rem;
        border-radius: var(--radius);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-sm);
        padding: 0.75rem 1.5rem;
    }
    
    .stTabs button[aria-selected="true"] {
        background: var(--primary) !important;
        color: white !important;
    }

    /* Global shell and navigation */
    .aiqos-top-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 2000;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        flex-wrap: nowrap;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        width: 100%;
        height: 68px;
        min-height: 68px;
        padding: 0 16px;
        margin: 0;
        border: none;
        border-bottom: 1px solid rgba(51,65,85,0.55);
        background: rgba(15, 15, 35, 0.98);
        backdrop-filter: blur(6px);
        box-sizing: border-box;
    }

    /* By default hide the selectbox overflow; revealed on small screens */
    .aiqos-top-header .stSelectbox {
        display: none;
    }
    .aiqos-top-header__brand {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        white-space: nowrap;
        flex-shrink: 0;
        margin-right: 20px;
    }
    .aiqos-top-header__nav {
        display: inline-flex;
        align-items: center;
        gap: 10px; /* navigation gap: 8-12px */
        flex: 1 1 auto;
        flex-wrap: nowrap;
        min-width: 0;
        overflow-x: auto;
    }
    /* Primary navigation and utility button sizing */
    .aiqos-top-header .stButton > button {
        height: 40px;
        min-height: 40px;
        padding: 8px 14px;
        border-radius: 10px;
        white-space: nowrap;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.95rem;
        line-height: 1;
    }
    .aiqos-top-header .stButton > button[title] {
        padding-left: 10px;
        padding-right: 10px;
    }
    .aiqos-top-header__utility {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        flex-wrap: nowrap;
        margin-left: auto;
        flex-shrink: 0;
    }

    /* Hide header scrollbar while allowing scroll */
    .aiqos-top-header::-webkit-scrollbar,
    .aiqos-top-header__nav::-webkit-scrollbar {
        height: 8px;
    }
    .aiqos-top-header::-webkit-scrollbar-thumb,
    .aiqos-top-header__nav::-webkit-scrollbar-thumb {
        background: rgba(51,65,85,0.6);
        border-radius: 6px;
    }

    /* Remove stray pseudo-elements (fix stray red dot issue) */
    .aiqos-top-header *::before,
    .aiqos-top-header *::after {
        display: none !important;
        content: none !important;
    }

    /* Responsive behavior: collapse inline secondary buttons into an overflow selectbox */
    @media (max-width: 980px) {
        .aiqos-top-header__nav .stButton {
            display: none !important;
        }
        .aiqos-top-header .stSelectbox {
            display: block !important;
            min-width: 160px;
            margin-left: 0.5rem;
        }
    }

    /* Slightly reduce gaps on medium screens for compactness */
    @media (max-width: 1200px) {
        .aiqos-top-header {
            gap: 0.4rem;
        }
        .aiqos-top-header__nav {
            gap: 0.25rem;
        }
    }
    /* Focus and hover states for keyboard accessibility */
    .aiqos-top-header .stButton > button:focus {
        outline: 2px solid rgba(99,102,241,0.35);
        outline-offset: 2px;
    }
    .aiqos-top-header .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(99,102,241,0.06);
    }
    .aiqos-top-header .stExpander {
        background: rgba(255,255,255,0.02);
        border-radius: 8px;
        padding: 0.25rem;
    }

    .stButton > button,
    .stDownloadButton > button,
    .stFormSubmitButton > button {
        min-height: 40px;
        height: auto;
        padding: 0.6rem 0.9rem;
        border-radius: 10px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        min-width: fit-content;
        box-sizing: border-box;
    }
    .stButton > button:hover {
        border-color: var(--primary);
        transform: translateY(-1px);
    }

    .stMain .block-container {
        max-width: 1600px;
        padding-left: 24px;
        padding-right: 24px;
        padding-top: 92px; /* header (68px) + 24px gap */
        margin: 0 auto;
    }
    .stAppViewContainer {
        overflow-x: hidden;
    }
    .stMarkdown p,
    .stMarkdown li,
    .stMarkdown td,
    .stMarkdown span,
    h1, h2, h3, h4, h5, h6,
    p, li, span {
        overflow-wrap: break-word;
        word-break: normal;
    }
    .element-container,
    .stColumn,
    [data-testid="stColumn"] {
        min-width: 0;
        max-width: 100%;
    }
    
    div[data-testid="stAlert"] {
        border-radius: var(--radius);
        border: none;
    }
    
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--surface);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-muted);
    }

    /* ============================================================
       GLOBAL LAYOUT STABILIZATION
       Prevents horizontal page overflow, squeezed columns,
       broken text wrapping, and content-dependent layout shifts
       across every module. Applied app-wide via app.py.
       ============================================================ */

    /* Universal box model — no content may exceed its parent */
    *, *::before, *::after {
        box-sizing: border-box;
    }

    /* App + main containers never horizontally scroll */
    [data-testid="stAppViewContainer"],
    [data-testid="stMainBlockContainer"],
    .stMainBlockContainer,
    section[data-testid="stMainBlockContainer"],
    div[data-testid="stAppViewBlockContainer"] {
        max-width: 100%;
        overflow-x: hidden;
    }

    /* Every Streamlit column can shrink and never overflows */
    .stColumn,
    [data-testid="stColumn"] {
        min-width: 0;
        max-width: 100%;
    }

    /* Metrics are stable — label/value never wrap to vertical chars */
    .stMetric,
    [data-testid="stMetric"] {
        min-width: 0;
    }
    .stMetric label,
    [data-testid="stMetricLabel"] {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    [data-testid="stMetricValue"] {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* Markdown containers never overflow horizontally */
    .stMarkdown,
    [data-testid="stMarkdownContainer"] {
        max-width: 100%;
        min-width: 0;
        overflow-wrap: anywhere;
        word-break: normal;
    }
    .stMarkdown div,
    .stMarkdown span {
        max-width: 100%;
    }

    /* Dataframes/tables scroll internally, never push the page */
    .stDataFrame,
    [data-testid="stDataFrame"] {
        max-width: 100%;
        overflow-x: auto;
    }

    /* Code blocks scroll horizontally, never wrap vertically */
    .stCodeBlock,
    pre {
        max-width: 100%;
        overflow-x: auto;
        white-space: pre;
        word-break: normal;
        overflow-wrap: normal;
    }

    /* Tabs never overflow horizontally — wrap if needed */
    .stTabs [data-baseweb="tab-list"] {
        max-width: 100%;
        overflow-x: auto;
        flex-wrap: nowrap;
    }

    /* Plotly charts respect parent width */
    .stPlotlyChart,
    [data-testid="stPlotlyChart"] {
        max-width: 100%;
        min-width: 0;
    }

    /* Prevent long unbreakable strings (URLs, IDs, JSON) from breaking layout */
    .stMarkdown p,
    .stMarkdown li,
    .stMarkdown td {
        overflow-wrap: anywhere;
        word-break: normal;
    }

    /* ============================================================
       ADDITIONAL GLOBAL LAYOUT FIXES
       Enforce viewport-aware widths, prevent horizontal overflow,
       and provide responsive helpers for KPI/coverage grids.
       ============================================================ */

    /* Global base containers: never exceed viewport width */
    html,
    body,
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
        overflow-x: hidden !important;
    }

    /* Page content wrapper recommended for pages */
    .page-content,
    .app-content,
    .workspace,
    .main-content {
        width: 100%;
        max-width: 1600px;
        margin: 0 auto;
        padding-left: 24px;
        padding-right: 24px;
        box-sizing: border-box;
        min-width: 0;
    }
    @media (max-width: 1200px) {
        .page-content,
        .app-content,
        .workspace,
        .main-content {
            padding-left: 16px;
            padding-right: 16px;
        }
    }
    @media (max-width: 480px) {
        .page-content,
        .app-content,
        .workspace,
        .main-content {
            padding-left: 12px;
            padding-right: 12px;
        }
    }

    /* Ensure common card/grid components do not force overflow */
    .aiqos-card,
    .aiqos-metric-card,
    .aiqos-kpi-card,
    .aiqos-coverage-card {
        min-width: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }

    /* Generic responsive grid for KPI/coverage sections
       Use class="aiqos-kpi-grid" on containers where applicable */
    .aiqos-kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 16px;
        align-items: start;
        width: 100%;
        box-sizing: border-box;
    }

    /* Flex children must be allowed to shrink to avoid overflow */
    .aiqos-top-header > *,
    .aiqos-kpi-grid > *,
    .aiqos-card > *,
    .aiqos-metric-card > *,
    .stColumn,
    [data-testid="stColumn"],
    .element-container {
        min-width: 0 !important;
    }

    /* Prevent elements using 100vw from exceeding viewport due to scrollbars */
    .aiqos-full-bleed,
    .full-bleed {
        width: 100vw;
        max-width: 100vw;
        box-sizing: border-box;
        margin-left: calc(50% - 50vw);
        margin-right: calc(50% - 50vw);
    }

    /* Images and SVGs must be responsive */
    img, svg {
        max-width: 100%;
        height: auto;
        display: block;
    }

    /* Charts should never exceed their parent width */
    .stPlotlyChart, [data-testid="stPlotlyChart"] {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
    }

    /* Tables and code keep internal horizontal scroll only */
    table, .stDataFrame, .stCodeBlock, pre {
        max-width: 100%;
        box-sizing: border-box;
    }

    /* Small helper for columns created by st.columns() — allow wrapping on very narrow screens */
    .stColumns, .stColumns > div, .stColumnsContainer {
        min-width: 0 !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    """,
}
