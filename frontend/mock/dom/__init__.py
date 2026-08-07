"""Mock data for DOM exploration.

DOM element/tree data is sourced from utils/dom_data.py generators.
This module provides premium static mock data for the AI DOM Operating
Center surface (hero KPIs, KPI strip, bottom-workspace tabs, relationship
graph, automation ideas, accessibility, network/CSS/JS/events/performance
panels, history).
"""

from datetime import datetime, timedelta


# Organization/hero KPI chips for the sticky DOM hero header
DOM_HERO_KPIS = [
    {"label": "Current Page", "value": "Products Page", "icon": "📄", "color": "primary"},
    {"label": "Current URL", "value": "shop.staging/products", "icon": "🔗", "color": "secondary"},
    {"label": "DOM Version", "value": "3.2.1", "icon": "🏷️", "color": "info"},
    {"label": "DOM Health", "value": "94%", "icon": "💚", "color": "success"},
    {"label": "Coverage", "value": "82.5%", "icon": "🎯", "color": "primary"},
    {"label": "Automation", "value": "88%", "icon": "🤖", "color": "success"},
    {"label": "A11y Score", "value": "91%", "icon": "♿", "color": "warning"},
    {"label": "Elements", "value": "1,247", "icon": "🧱", "color": "accent"},
    {"label": "Forms", "value": "3", "icon": "📝", "color": "info"},
    {"label": "Buttons", "value": "45", "icon": "🔘", "color": "secondary"},
    {"label": "Inputs", "value": "67", "icon": "⌨️", "color": "primary"},
    {"label": "Shadow DOM", "value": "2", "icon": "👻", "color": "muted"},
]

# KPI strip MetricCards
DOM_KPI_METRICS = [
    {"title": "Total Elements", "value": "1,247", "icon": "🧱", "trend": "+12", "subtitle": "scanned"},
    {"title": "Interactive", "value": 234, "icon": "👆", "trend": "+5", "subtitle": "elements"},
    {"title": "Dynamic", "value": 89, "icon": "🔄", "trend": "+3", "subtitle": "elements"},
    {"title": "Forms", "value": 3, "icon": "📝", "trend": "0", "subtitle": "forms"},
    {"title": "Buttons", "value": 45, "icon": "🔘", "trend": "+2", "subtitle": "buttons"},
    {"title": "Inputs", "value": 67, "icon": "⌨️", "trend": "+1", "subtitle": "inputs"},
    {"title": "ARIA", "value": 142, "icon": "♿", "trend": "+8", "subtitle": "elements"},
    {"title": "Shadow DOM", "value": 2, "icon": "👻", "trend": "0", "subtitle": "roots"},
    {"title": "Iframes", "value": 0, "icon": "🖼️", "trend": "0", "subtitle": "frames"},
    {"title": "Coverage", "value": "82.5%", "icon": "🎯", "trend": "+1.2%", "subtitle": "DOM covered"},
    {"title": "Automation", "value": "88%", "icon": "🤖", "trend": "+3%", "subtitle": "score"},
    {"title": "Health", "value": "94%", "icon": "💚", "trend": "+2%", "subtitle": "healthy"},
]

# Bottom workspace tabs
DOM_BOTTOM_TABS = ["Console", "Network", "Accessibility", "CSS", "JavaScript", "Events", "Performance", "History"]

# Relationship graph: Element -> Component -> Business Rule -> API -> Database -> Workflow -> Report
DOM_RELATIONSHIP_GRAPH = [
    {"id": "element", "name": "Element", "icon": "🧩", "level": 0, "detail": "<input data-testid=\"search-input\">", "color": "primary"},
    {"id": "component", "name": "Component", "icon": "🧱", "level": 1, "detail": "SearchBar component", "color": "secondary"},
    {"id": "business_rule", "name": "Business Rule", "icon": "📏", "level": 2, "detail": "Query must be >= 2 chars", "color": "warning"},
    {"id": "api", "name": "API", "icon": "🔗", "level": 3, "detail": "GET /api/v1/products?q=", "color": "info"},
    {"id": "database", "name": "Database", "icon": "🗄️", "level": 4, "detail": "products WHERE name LIKE", "color": "accent"},
    {"id": "workflow", "name": "Workflow", "icon": "🔀", "level": 5, "detail": "Search -> Filter -> Results", "color": "success"},
    {"id": "report", "name": "Report", "icon": "📊", "level": 6, "detail": "Search Coverage Report", "color": "muted"},
]

# Automation intelligence ideas for the selected element
DOM_AUTOMATION_IDEAS = [
    {"label": "AI Test Idea", "value": "Verify search returns relevant products for 'headphones'", "icon": "💡", "color": "primary"},
    {"label": "Generated Feature", "value": "Feature: Product search returns matching results", "icon": "📝", "color": "secondary"},
    {"label": "Generated Test Case", "value": "test_search_returns_results_for_valid_query()", "icon": "🧪", "color": "success"},
    {"label": "Generated Page Object", "value": "class SearchPage: def search(self, q): ...", "icon": "🏗️", "color": "info"},
    {"label": "Business Importance", "value": "Critical — drives product discovery", "icon": "⭐", "color": "warning"},
]

# Accessibility panel (WCAG breakdown)
DOM_ACCESSIBILITY_PANEL = [
    {"label": "ARIA Labels", "value": "Present", "score": 95, "color": "success", "detail": "aria-label defined"},
    {"label": "Keyboard", "value": "Full support", "score": 92, "color": "success", "detail": "focusable + reachable"},
    {"label": "Contrast", "value": "AA (4.8:1)", "score": 88, "color": "warning", "detail": "meets WCAG AA"},
    {"label": "Focus", "value": "Visible", "score": 90, "color": "success", "detail": "focus ring present"},
    {"label": "Screen Reader", "value": "Compatible", "score": 91, "color": "success", "detail": "announced correctly"},
    {"label": "WCAG Status", "value": "AA Compliant", "score": 91, "color": "success", "detail": "WCAG 2.1 AA"},
    {"label": "AI Suggestion", "value": "Add aria-live for dynamic results", "score": 0, "color": "info", "detail": "improve SR feedback"},
]

# Network requests for the Network tab
DOM_NETWORK_LOGS = [
    {"method": "GET", "url": "/api/v1/products?page=1", "status": 200, "time": "142ms", "size": "24KB", "color": "success"},
    {"method": "GET", "url": "/api/v1/categories", "status": 200, "time": "38ms", "size": "2KB", "color": "success"},
    {"method": "POST", "url": "/api/v1/search", "status": 201, "time": "210ms", "size": "48KB", "color": "success"},
    {"method": "GET", "url": "/api/v1/products/123", "status": 200, "time": "95ms", "size": "8KB", "color": "success"},
    {"method": "GET", "url": "/assets/main.css", "status": 200, "time": "22ms", "size": "120KB", "color": "success"},
    {"method": "GET", "url": "/assets/app.js", "status": 200, "time": "64ms", "size": "340KB", "color": "success"},
    {"method": "GET", "url": "/img/product1.jpg", "status": 404, "time": "12ms", "size": "0KB", "color": "error"},
    {"method": "PUT", "url": "/api/v1/cart", "status": 401, "time": "58ms", "size": "1KB", "color": "warning"},
]

# CSS rules for the CSS tab
DOM_CSS_RULES = [
    {"selector": ".product-card", "props": "display:flex; flex-direction:column; padding:16px;", "source": "products.css:42", "color": "primary"},
    {"selector": ".btn-primary", "props": "background:#6366f1; color:#fff; border-radius:6px;", "source": "buttons.css:18", "color": "info"},
    {"selector": "#search-input", "props": "width:200px; padding:8px 12px; border-radius:6px;", "source": "header.css:7", "color": "secondary"},
    {"selector": ".products-grid", "props": "display:grid; grid-template-columns:repeat(2,1fr);", "source": "products.css:12", "color": "accent"},
    {"selector": "nav[aria-label]", "props": "display:flex; gap:12px;", "source": "nav.css:3", "color": "success"},
]

# JavaScript console for the JavaScript tab
DOM_JS_LOGS = [
    {"level": "info", "message": "App initialized in 1.2s", "time": "10:00:01", "color": "muted"},
    {"level": "info", "message": "ProductGrid mounted (2 items)", "time": "10:00:02", "color": "muted"},
    {"level": "warn", "message": "Image /img/product1.jpg failed (404)", "time": "10:00:03", "color": "warning"},
    {"level": "error", "message": "Uncaught TypeError: cart.addItem is not a function", "time": "10:00:05", "color": "error"},
    {"level": "info", "message": "Analytics: search_event tracked", "time": "10:00:08", "color": "success"},
]

# DOM events for the Events tab
DOM_EVENTS_LOG = [
    {"event": "click", "target": "button[data-testid='add-to-cart-1']", "time": "10:00:12", "color": "primary"},
    {"event": "input", "target": "input[data-testid='search-input']", "time": "10:00:15", "color": "secondary"},
    {"event": "change", "target": "select[data-testid='category-select']", "time": "10:00:18", "color": "info"},
    {"event": "submit", "target": "form[data-testid='search-form']", "time": "10:00:20", "color": "accent"},
    {"event": "focus", "target": "input#login-email", "time": "10:00:22", "color": "warning"},
    {"event": "blur", "target": "input#login-email", "time": "10:00:23", "color": "muted"},
    {"event": "click", "target": "a[href='/products/123']", "time": "10:00:25", "color": "success"},
]

# Performance metrics for the Performance tab
DOM_PERF_METRICS = [
    {"metric": "DOM Content Loaded", "value": "1.2s", "score": 88, "color": "success"},
    {"metric": "Load Complete", "value": "2.4s", "score": 76, "color": "warning"},
    {"metric": "First Contentful Paint", "value": "0.8s", "score": 92, "color": "success"},
    {"metric": "Largest Contentful Paint", "value": "1.9s", "score": 81, "color": "warning"},
    {"metric": "Time to Interactive", "value": "2.1s", "score": 84, "color": "success"},
    {"metric": "Total Blocking Time", "value": "180ms", "score": 79, "color": "warning"},
    {"metric": "Cumulative Layout Shift", "value": "0.05", "score": 95, "color": "success"},
    {"metric": "JS Heap", "value": "24MB", "score": 90, "color": "success"},
]

# DOM analysis history for the History tab
DOM_HISTORY = [
    {"time": "10:00:01", "icon": "🌐", "title": "DOM Scan Started", "desc": "Scanning shop.staging/products", "color": "primary"},
    {"time": "10:00:03", "icon": "🧱", "title": "1,247 Elements Detected", "desc": "234 interactive, 89 dynamic", "color": "secondary"},
    {"time": "10:00:08", "icon": "🎯", "title": "Locators Generated", "desc": "24 stable XPath selectors", "color": "success"},
    {"time": "10:00:12", "icon": "♿", "title": "A11y Audit Complete", "desc": "Score 91 — 2 issues found", "color": "warning"},
    {"time": "10:00:15", "icon": "🤖", "title": "Automation Analysis", "desc": "88% automation score", "color": "info"},
    {"time": "10:00:18", "icon": "🔗", "title": "Relationships Mapped", "desc": "7 business-flow links", "color": "accent"},
    {"time": "10:00:20", "icon": "✅", "title": "Scan Complete", "desc": "DOM Health 94% — Ready", "color": "success"},
]

# Quick actions (glass buttons)
DOM_QUICK_ACTIONS = [
    {"name": "Copy CSS", "icon": "📋", "description": "Copy CSS selector", "color": "primary"},
    {"name": "Copy XPath", "icon": "📋", "description": "Copy XPath selector", "color": "secondary"},
    {"name": "Copy Playwright", "icon": "📋", "description": "Copy Playwright locator", "color": "info"},
    {"name": "Copy Selenium", "icon": "📋", "description": "Copy Selenium locator", "color": "accent"},
    {"name": "Generate Test", "icon": "🧪", "description": "Generate test case", "color": "success"},
    {"name": "Generate Feature", "icon": "📝", "description": "Generate feature spec", "color": "warning"},
    {"name": "Generate Assertion", "icon": "✅", "description": "Generate assertions", "color": "primary"},
    {"name": "Generate Page Object", "icon": "🏗️", "description": "Page object model", "color": "secondary"},
    {"name": "Analyze A11y", "icon": "♿", "description": "Accessibility audit", "color": "info"},
    {"name": "Analyze Perf", "icon": "⚡", "description": "Performance audit", "color": "accent"},
    {"name": "Open Browser", "icon": "🌐", "description": "Open in browser", "color": "success"},
    {"name": "Knowledge Graph", "icon": "🕸️", "description": "Open graph explorer", "color": "primary"},
]

