"""AI-QOS Design System - Glassmorphism Theme for Agent Control Tower."""

GLASSMORPHISM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --primary-color: #6366f1;
        --primary-light: #818cf8;
        --primary-dark: #4f46e5;
        --secondary-color: #22d3ee;
        --accent-color: #f472b6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --info-color: #3b82f6;
        
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-tertiary: #334155;
        --bg-glass: rgba(30, 41, 59, 0.7);
        
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        
        --border-color: rgba(148, 163, 184, 0.1);
        --border-glow: rgba(99, 102, 241, 0.3);
        
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
        --shadow-glow: 0 0 20px rgba(99, 102, 241, 0.2);
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: var(--bg-primary);
        color: var(--text-primary);
    }
    
    /* Glassmorphism Card */
    .glass-card {
        background: var(--bg-glass);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        box-shadow: var(--shadow-md), var(--shadow-glow);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: var(--border-glow);
        box-shadow: var(--shadow-lg), 0 0 30px rgba(99, 102, 241, 0.3);
        transform: translateY(-2px);
    }
    
    /* Agent Card Styles */
    .agent-card {
        background: var(--bg-glass);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .agent-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .agent-card:hover::before {
        opacity: 1;
    }
    
    .agent-card:hover {
        border-color: var(--border-glow);
        box-shadow: var(--shadow-lg), 0 0 30px rgba(99, 102, 241, 0.2);
        transform: translateY(-4px);
    }
    
    /* Status Indicators */
    .status-running {
        background: linear-gradient(135deg, var(--success-color), #059669);
        animation: pulse-glow 2s infinite;
    }
    
    .status-waiting {
        background: linear-gradient(135deg, var(--warning-color), #d97706);
    }
    
    .status-paused {
        background: linear-gradient(135deg, var(--text-muted), #475569);
    }
    
    .status-failed {
        background: linear-gradient(135deg, var(--error-color), #dc2626);
        animation: error-pulse 1s infinite;
    }
    
    .status-completed {
        background: linear-gradient(135deg, var(--info-color), #2563eb);
    }
    
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 5px currentColor; }
        50% { box-shadow: 0 0 20px currentColor, 0 0 30px currentColor; }
    }
    
    @keyframes error-pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    /* Health Gauge */
    .health-gauge {
        width: 100%;
        height: 8px;
        background: var(--bg-tertiary);
        border-radius: 4px;
        overflow: hidden;
        position: relative;
    }
    
    .health-gauge-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease;
    }
    
    .health-excellent { background: linear-gradient(90deg, #10b981, #059669); }
    .health-good { background: linear-gradient(90deg, #22d3ee, #06b6d4); }
    .health-warning { background: linear-gradient(90deg, #f59e0b, #d97706); }
    .health-critical { background: linear-gradient(90deg, #ef4444, #dc2626); }
    
    /* Progress Bar */
    .progress-bar {
        width: 100%;
        height: 6px;
        background: var(--bg-tertiary);
        border-radius: 3px;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        border-radius: 3px;
        transition: width 0.5s ease;
        position: relative;
    }
    
    .progress-bar-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Resource Metrics */
    .metric-card {
        background: var(--bg-glass);
        backdrop-filter: blur(12px);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        font-size: 12px;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }
    
    /* Event Stream */
    .event-item {
        padding: 10px 12px;
        border-left: 3px solid var(--border-color);
        margin-bottom: 8px;
        background: rgba(30, 41, 59, 0.5);
        border-radius: 0 8px 8px 0;
        transition: all 0.2s ease;
    }
    
    .event-item:hover {
        background: rgba(30, 41, 59, 0.8);
        border-left-color: var(--primary-color);
    }
    
    .event-info { background: rgba(59, 130, 246, 0.2); border-left-color: #3b82f6; }
    .event-success { background: rgba(16, 185, 129, 0.2); border-left-color: #10b981; }
    .event-warning { background: rgba(245, 158, 11, 0.2); border-left-color: #f59e0b; }
    .event-error { background: rgba(239, 68, 68, 0.2); border-left-color: #ef4444; }
    
    /* Communication Graph */
    .comm-node {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        background: var(--bg-glass);
        border: 2px solid var(--border-color);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .comm-node:hover {
        transform: scale(1.15);
        border-color: var(--primary-color);
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.5);
    }
    
    .comm-node.active {
        border-color: var(--success-color);
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.5);
        animation: node-pulse 1.5s infinite;
    }
    
    @keyframes node-pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .comm-connection {
        position: absolute;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        height: 2px;
        transform-origin: left center;
        opacity: 0.6;
    }
    
    .comm-connection.active {
        opacity: 1;
        animation: flow 1s infinite;
    }
    
    @keyframes flow {
        0% { background-position: 0% 0%; }
        100% { background-position: 200% 0%; }
    }
    
    /* Model Panel */
    .model-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        background: var(--bg-glass);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
    }
    
    .model-badge.active {
        border-color: var(--primary-color);
        background: rgba(99, 102, 241, 0.15);
    }
    
    /* Drawer Animation */
    .drawer-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(4px);
        z-index: 1000;
        animation: fade-in 0.3s ease;
    }
    
    .drawer-content {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        width: 600px;
        max-width: 90vw;
        background: var(--bg-secondary);
        border-left: 1px solid var(--border-color);
        box-shadow: -20px 0 60px rgba(0, 0, 0, 0.5);
        z-index: 1001;
        animation: slide-in 0.3s ease;
        overflow-y: auto;
    }
    
    @keyframes fade-in {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slide-in {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
    }
    
    /* Header Stats */
    .header-stat {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 12px 20px;
        background: var(--bg-glass);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        min-width: 120px;
    }
    
    .header-stat-value {
        font-size: 24px;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .header-stat-label {
        font-size: 11px;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--bg-tertiary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-muted);
    }
    
    /* Category Badge */
    .category-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 6px;
        font-size: 12px;
        font-weight: 500;
    }
    
    .category-intelligence { background: rgba(139, 92, 246, 0.15); border-color: rgba(139, 92, 246, 0.3); }
    .category-testing { background: rgba(59, 130, 246, 0.15); border-color: rgba(59, 130, 246, 0.3); }
    .category-documentation { background: rgba(16, 185, 129, 0.15); border-color: rgba(16, 185, 129, 0.3); }
    .category-infrastructure { background: rgba(245, 158, 11, 0.15); border-color: rgba(245, 158, 11, 0.3); }
    .category-learning { background: rgba(236, 72, 153, 0.15); border-color: rgba(236, 72, 153, 0.3); }
    .category-security { background: rgba(239, 68, 68, 0.15); border-color: rgba(239, 68, 68, 0.3); }
    .category-support { background: rgba(34, 211, 238, 0.15); border-color: rgba(34, 211, 238, 0.3); }
    
    /* Search Input */
    .search-input {
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 10px 16px;
        color: var(--text-primary);
        font-size: 14px;
        width: 100%;
        transition: all 0.2s ease;
    }
    
    .search-input:focus {
        outline: none;
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
    }
    
    .search-input::placeholder {
        color: var(--text-muted);
    }
    
    /* Queue Status */
    .queue-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 14px;
        background: var(--bg-glass);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        margin-bottom: 8px;
    }
    
    .queue-count {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        font-size: 18px;
    }
    
    /* Timeline */
    .timeline-container {
        position: relative;
        padding: 20px;
    }
    
    .timeline-line {
        position: absolute;
        top: 0;
        bottom: 0;
        left: 50%;
        width: 4px;
        background: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
        border-radius: 2px;
        opacity: 0.3;
    }
    
    /* Tooltip */
    .tooltip {
        position: relative;
    }
    
    .tooltip::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        padding: 6px 10px;
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: 6px;
        font-size: 12px;
        white-space: nowrap;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.2s ease;
        z-index: 100;
    }
    
    .tooltip:hover::after {
        opacity: 1;
    }
    
    /* Confirmed Messages Animation */
    .message-flow {
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }
    
    .message-particle {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--secondary-color);
        position: absolute;
        animation: message-travel 2s infinite;
        box-shadow: 0 0 10px var(--secondary-color);
    }
    
    @keyframes message-travel {
        0% { left: 0; opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { left: 100%; opacity: 0; }
    }
    
    /* Loading Skeleton */
    .skeleton {
        background: linear-gradient(90deg, var(--bg-tertiary) 25%, var(--bg-secondary) 50%, var(--bg-tertiary) 75%);
        background-size: 200% 100%;
        animation: skeleton-loading 1.5s infinite;
        border-radius: 8px;
    }
    
    @keyframes skeleton-loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    /* Responsive Grid */
    .agent-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 20px;
    }
    
    @media (max-width: 768px) {
        .agent-grid {
            grid-template-columns: 1fr;
        }
        
        .header-stat {
            min-width: 80px;
            padding: 8px 12px;
        }
    }
</style>
"""


def get_status_color(status: str) -> str:
    """Get color for agent status."""
    colors = {
        "running": "#10b981",
        "waiting": "#f59e0b",
        "paused": "#64748b",
        "failed": "#ef4444",
        "completed": "#3b82f6",
        "idle": "#94a3b8",
    }
    return colors.get(status.lower(), "#94a3b8")


def get_health_class(health: float) -> str:
    """Get health class based on health value."""
    if health >= 0.9:
        return "health-excellent"
    elif health >= 0.75:
        return "health-good"
    elif health >= 0.5:
        return "health-warning"
    else:
        return "health-critical"


def get_category_class(category: str) -> str:
    """Get CSS class for category."""
    return f"category-{category.lower()}"
