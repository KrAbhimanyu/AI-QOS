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
    """,
}
