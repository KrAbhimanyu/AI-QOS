"""Mock data for the Knowledge Graph / AI Cognitive Intelligence Center.

Knowledge node/relationship/flow data is sourced from
utils/knowledge_graph_data.py generators. This module provides the premium
surface mock data for the cognitive workspace (hero KPI chips, KPI strip
MetricCards, dependency chain, knowledge health, quick actions, bottom
workspace tabs, reasoning trace) — mirroring the DOM Intelligence Explorer
mock pattern.
"""

from datetime import datetime, timedelta


# Organization/hero KPI chips for the sticky cognitive hero header
KG_HERO_KPIS = [
    {"label": "Knowledge Version", "value": "2.0", "icon": "🏷️", "color": "info"},
    {"label": "Graph Health", "value": "94%", "icon": "💚", "color": "success"},
    {"label": "Nodes", "value": "487", "icon": "🔵", "color": "primary"},
    {"label": "Relationships", "value": "1,234", "icon": "🔗", "color": "secondary"},
    {"label": "Business Rules", "value": "89", "icon": "⚖️", "color": "warning"},
    {"label": "Applications", "value": "1", "icon": "🏢", "color": "accent"},
    {"label": "Requirements", "value": "245", "icon": "📋", "color": "primary"},
    {"label": "Pages", "value": "45", "icon": "📄", "color": "secondary"},
    {"label": "DOM Elements", "value": "1,247", "icon": "🏗️", "color": "info"},
    {"label": "APIs", "value": "67", "icon": "🔌", "color": "accent"},
    {"label": "Databases", "value": "34", "icon": "🗄️", "color": "primary"},
    {"label": "Bugs", "value": "12", "icon": "🐛", "color": "error"},
    {"label": "Reports", "value": "45", "icon": "📈", "color": "success"},
    {"label": "AI Confidence", "value": "92%", "icon": "🧠", "color": "success"},
]

# KPI strip MetricCards
KG_KPI_METRICS = [
    {"title": "Total Nodes", "value": "487", "icon": "🔵", "trend": "+12", "subtitle": "knowledge nodes"},
    {"title": "Relationships", "value": "1,234", "icon": "🔗", "trend": "+34", "subtitle": "graph edges"},
    {"title": "Connected Components", "value": 6, "icon": "🕸️", "trend": "0", "subtitle": "clusters"},
    {"title": "Business Rules", "value": "89", "icon": "⚖️", "trend": "+4", "subtitle": "rules mapped"},
    {"title": "Applications", "value": 1, "icon": "🏢", "trend": "0", "subtitle": "application"},
    {"title": "Pages", "value": "45", "icon": "📄", "trend": "+2", "subtitle": "pages"},
    {"title": "APIs", "value": "67", "icon": "🔌", "trend": "+3", "subtitle": "endpoints"},
    {"title": "Databases", "value": "34", "icon": "🗄️", "trend": "+1", "subtitle": "tables"},
    {"title": "DOM Elements", "value": "1,247", "icon": "🏗️", "trend": "+18", "subtitle": "elements"},
    {"title": "Requirements", "value": "245", "icon": "📋", "trend": "+6", "subtitle": "test cases"},
    {"title": "Coverage", "value": "78.5%", "icon": "🎯", "trend": "+1.4%", "subtitle": "automated"},
    {"title": "Health", "value": "94%", "icon": "💚", "trend": "+2%", "subtitle": "graph health"},
]

# Dependency chain: Requirement -> Business Rule -> Application -> Page ->
# DOM -> API -> Database -> Report -> Bug -> Release
KG_DEPENDENCY_CHAIN = [
    {"id": "requirement", "name": "Requirement", "icon": "📋", "level": 0, "detail": "REQ-Checkout: secure payment capture", "color": "primary"},
    {"id": "business_rule", "name": "Business Rule", "icon": "⚖️", "level": 1, "detail": "price_calc: order total = sum(items) + tax", "color": "warning"},
    {"id": "application", "name": "Application", "icon": "🏢", "level": 2, "detail": "E-Commerce Platform", "color": "accent"},
    {"id": "page", "name": "Page", "icon": "📄", "level": 3, "detail": "Checkout page (multi-step)", "color": "secondary"},
    {"id": "dom", "name": "DOM", "icon": "🏗️", "level": 4, "detail": "form#checkout-form > input.card", "color": "info"},
    {"id": "api", "name": "API", "icon": "🔌", "level": 5, "detail": "POST /api/v1/checkout", "color": "primary"},
    {"id": "database", "name": "Database", "icon": "🗄️", "level": 6, "detail": "orders INSERT, inventory UPDATE", "color": "accent"},
    {"id": "report", "name": "Report", "icon": "📈", "level": 7, "detail": "Checkout Coverage Report", "color": "success"},
    {"id": "bug", "name": "Bug", "icon": "🐛", "level": 8, "detail": "BUG-Price: rounding edge case", "color": "error"},
    {"id": "release", "name": "Release", "icon": "🚀", "level": 9, "detail": "Release v3.2.1 (pending)", "color": "muted"},
]

# Knowledge health diagnostics
KG_HEALTH = [
    {"label": "Graph Health", "value": "94%", "score": 94, "color": "success", "detail": "stable, no schema drift"},
    {"label": "Coverage", "value": "78.5%", "score": 78, "color": "warning", "detail": "automation coverage"},
    {"label": "Missing Nodes", "value": "5", "score": 12, "color": "warning", "detail": "unmapped endpoints"},
    {"label": "Orphan Nodes", "value": "4", "score": 9, "color": "warning", "detail": "no inbound relationships"},
    {"label": "Broken Relationships", "value": "4", "score": 15, "color": "error", "detail": "dangling references"},
    {"label": "Duplicate Entities", "value": "3", "score": 8, "color": "info", "detail": "similar components"},
    {"label": "AI Confidence", "value": "92%", "score": 92, "color": "success", "detail": "high certainty graph"},
    {"label": "Knowledge Freshness", "value": "5m ago", "score": 96, "color": "success", "detail": "last update recent"},
]

# AI suggestions for knowledge health
KG_HEALTH_SUGGESTIONS = [
    {"label": "Link 4 orphan nodes", "value": "Reconnect orphaned components to their parent pages", "icon": "🔗", "color": "primary"},
    {"label": "Fix 4 broken relationships", "value": "Resolve dangling references in the checkout subgraph", "icon": "🩹", "color": "error"},
    {"label": "Map 5 missing APIs", "value": "Discover unmapped endpoints via traffic analysis", "icon": "🔌", "color": "warning"},
    {"label": "Merge 3 duplicates", "value": "Consolidate similar product-card components", "icon": "🔁", "color": "info"},
    {"label": "Close 15 automation gaps", "value": "Add tests for uncovered business flows", "icon": "🎯", "color": "success"},
]

# Bottom workspace tabs
KG_BOTTOM_TABS = ["Timeline", "Relationships", "Evidence", "Memory", "Analytics", "History"]

# Quick actions (glass buttons)
KG_QUICK_ACTIONS = [
    {"name": "Expand Graph", "icon": "📐", "description": "Expand all navigator categories", "color": "primary"},
    {"name": "Collapse Graph", "icon": "🗂️", "description": "Collapse all navigator categories", "color": "secondary"},
    {"name": "Focus Node", "icon": "🎯", "description": "Focus the graph on the selected node", "color": "info"},
    {"name": "Find Dependencies", "icon": "🔗", "description": "Trace dependencies for selected node", "color": "accent"},
    {"name": "Analyze Impact", "icon": "📊", "description": "Analyze change impact radius", "color": "success"},
    {"name": "Generate Report", "icon": "📈", "description": "Generate coverage report", "color": "warning"},
    {"name": "DOM Explorer", "icon": "🌐", "description": "Open DOM Intelligence Explorer", "color": "primary"},
    {"name": "Open Mission", "icon": "🎯", "description": "Open Mission Planner", "color": "secondary"},
    {"name": "Open Chat", "icon": "💬", "description": "Open AI Chat Workspace", "color": "info"},
    {"name": "Open Reports", "icon": "📑", "description": "Open Reports & Analytics", "color": "accent"},
    {"name": "Release Advisor", "icon": "🚀", "description": "Open Release Advisor", "color": "success"},
    {"name": "Health Scan", "icon": "🩺", "description": "Run a knowledge health scan", "color": "warning"},
]

# AI reasoning trace (decision trace timeline for the selected node)
KG_REASONING_TRACE = [
    {"step": "Knowledge Source", "icon": "📚", "detail": "Discovered during application analysis scan", "color": "primary", "time": "T+0s"},
    {"step": "Business Context", "icon": "🏢", "detail": "Belongs to E-Commerce checkout domain", "color": "accent", "time": "T+1s"},
    {"step": "Connected Nodes", "icon": "🔗", "detail": "Linked to 4 pages, 2 APIs, 1 database table", "color": "secondary", "time": "T+2s"},
    {"step": "Evidence Gathered", "icon": "📸", "detail": "DOM snapshot + network trace captured", "color": "info", "time": "T+3s"},
    {"step": "Reasoning Path", "icon": "🧠", "detail": "Page -> Component -> API -> DB -> Rule chain traced", "color": "warning", "time": "T+4s"},
    {"step": "Risk Assessment", "icon": "⚠️", "detail": "Risk + confidence scored from relationship density", "color": "error", "time": "T+5s"},
    {"step": "Recommendation", "icon": "✅", "detail": "Increase automation coverage for stable quality", "color": "success", "time": "T+6s"},
]

# Knowledge memory entries (semantic memory of past reasoning)
KG_MEMORY = [
    {"title": "Checkout subgraph stabilized", "desc": "Payment gateway component linked; confidence 85%", "time": "2h ago", "icon": "🧠", "color": "success"},
    {"title": "Price calc rule modified", "desc": "Discount edge case captured; new relationship added", "time": "5h ago", "icon": "⚙️", "color": "warning"},
    {"title": "Orphan node detected", "desc": "Legacy report has no inbound relationships", "time": "1d ago", "icon": "🪪", "color": "info"},
    {"title": "Security risk flagged", "desc": "Authentication flow reviewed for vulnerabilities", "time": "1d ago", "icon": "🔒", "color": "error"},
    {"title": "Duplicate merged", "desc": "Two search-bar components consolidated", "time": "2d ago", "icon": "🔁", "color": "primary"},
]

# Evidence artifacts linked to the knowledge graph
KG_EVIDENCE = [
    {"title": "Checkout DOM Snapshot", "type": "📸 Snapshot", "size": "248KB", "color": "primary"},
    {"title": "Payment Network Trace", "type": "🌐 HAR", "size": "1.2MB", "color": "secondary"},
    {"title": "Price Calc Rule Spec", "type": "📄 Spec", "size": "12KB", "color": "warning"},
    {"title": "Auth Flow Test Evidence", "type": "🎥 Video", "size": "8.4MB", "color": "info"},
    {"title": "Cart Bug Reproduction", "type": "🧪 Repro", "size": "96KB", "color": "error"},
    {"title": "Coverage Report Export", "type": "📊 PDF", "size": "320KB", "color": "success"},
]
