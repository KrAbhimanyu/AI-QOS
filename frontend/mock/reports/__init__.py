"""Mock data for test reviews, reports, and the Executive Quality Intelligence Center.

Report/analytics business data is sourced from utils/reports_data.py. This
module preserves the existing review mock data and adds the premium
executive surface mock data (hero chips, KPI metrics, quality scores,
business flow quality, bug intel, release readiness, quality gates, AI
recommendations, timeline, release comparison) — mirroring the DOM
Intelligence Explorer / Knowledge Graph mock pattern.
"""

from datetime import datetime, timedelta


# ---------------------------------------------------------------------------
# Existing review mock data (preserved)
# ---------------------------------------------------------------------------
MOCK_ASSERTIONS = [
    {"name": "Page Title Contains 'Dashboard'", "expected": "Dashboard", "actual": "Dashboard", "status": "passed"},
    {"name": "User Name Displayed", "expected": "John Doe", "actual": "John Doe", "status": "passed"},
    {"name": "Logout Button Visible", "expected": "true", "actual": "true", "status": "passed"},
    {"name": "Sidebar Navigation Present", "expected": "true", "actual": "false", "status": "failed"},
]

MOCK_EVIDENCE = {
    "screenshot": "dashboard_loaded.png",
    "timestamp": "10:00:35",
    "url": "https://demo.app/dashboard",
    "network_calls": 12,
    "console_errors": 0,
    "performance_score": 94,
}

MOCK_AI_REVIEW = {
    "observation": "Dashboard page loaded successfully with all expected elements",
    "reasoning": "The page contains user profile, metrics cards, and navigation elements as expected",
    "evidence": [
        "User avatar displayed correctly",
        "Metrics cards showing real data",
        "Navigation menu visible",
    ],
    "confidence": 92,
    "suggested_action": "Approve - All validations pass except sidebar which may be collapsed",
    "potential_risks": [
        "Sidebar state may vary between sessions",
        "Dynamic content may cause timing issues",
    ],
    "best_practices": [
        "Add explicit wait for sidebar to load",
        "Consider mobile viewport testing",
    ],
}


# ---------------------------------------------------------------------------
# Executive hero header KPI chips
# ---------------------------------------------------------------------------
REPORTS_HERO_KPIS = [
    {"label": "Mission", "value": "E2E Regression v2.1", "icon": "🎯", "color": "primary"},
    {"label": "Application", "value": "E-Commerce", "icon": "🏢", "color": "accent"},
    {"label": "Release", "value": "v3.2.1", "icon": "🏷️", "color": "info"},
    {"label": "Build", "value": "#1247", "icon": "🔨", "color": "secondary"},
    {"label": "Environment", "value": "Production", "icon": "🌐", "color": "success"},
    {"label": "Branch", "value": "main", "icon": "🌿", "color": "primary"},
    {"label": "Quality", "value": "87%", "icon": "✅", "color": "success"},
    {"label": "Release Ready", "value": "93%", "icon": "🚀", "color": "success"},
    {"label": "AI Confidence", "value": "92%", "icon": "🧠", "color": "success"},
    {"label": "Last Updated", "value": "5m ago", "icon": "🕐", "color": "muted"},
]

# Executive KPI strip MetricCards
REPORTS_KPI_METRICS = [
    {"title": "Quality Score", "value": "87%", "icon": "✅", "trend": "+4.2%", "subtitle": "Excellent", "status": "success"},
    {"title": "Release Readiness", "value": "93%", "icon": "🚀", "trend": "+2.1%", "subtitle": "GO with risks", "status": "success"},
    {"title": "Automation Coverage", "value": "78.5%", "icon": "📊", "trend": "+5.2%", "subtitle": "Target 85%", "status": "warning"},
    {"title": "Pass Rate", "value": "94.2%", "icon": "🎯", "trend": "+1.3%", "subtitle": "Last 30 days", "status": "success"},
    {"title": "AI Confidence", "value": "92%", "icon": "🧠", "trend": "+3%", "subtitle": "High certainty", "status": "success"},
    {"title": "Business Coverage", "value": "85%", "icon": "💼", "trend": "+2%", "subtitle": "Flows covered", "status": "success"},
    {"title": "API Coverage", "value": "65%", "icon": "🔌", "trend": "+1%", "subtitle": "Below target", "status": "warning"},
    {"title": "Accessibility", "value": "91%", "icon": "♿", "trend": "+2%", "subtitle": "WCAG AA", "status": "success"},
    {"title": "Security", "value": "94%", "icon": "🔒", "trend": "+1%", "subtitle": "No criticals", "status": "success"},
    {"title": "Flaky Tests", "value": "2.3%", "icon": "📳", "trend": "-0.5%", "subtitle": "Target <2%", "status": "warning"},
    {"title": "Risk Score", "value": "23", "icon": "⚠️", "trend": "-4", "subtitle": "Medium", "status": "warning"},
    {"title": "Execution Health", "value": "96%", "icon": "💚", "trend": "+1.5%", "subtitle": "Healthy", "status": "success"},
]

# AI executive summary
AI_EXECUTIVE_SUMMARY = {
    "overall_assessment": "Quality improved 6.4% compared with the previous build. Release is on track with controlled risks.",
    "key_findings": [
        "Coverage up 5.2% — on track to reach 85% target by Q4",
        "Flaky rate dropped to 2.3% — best in 6 months",
        "AI agent efficiency improved 18% with new model routing",
    ],
    "top_risks": [
        "Checkout payment flow contains 3 high-risk flaky tests",
        "API endpoint coverage at 45% — critical business logic exposed",
    ],
    "positive_trends": [
        "Pass rate climbed to 94.2% (+1.3%)",
        "Zero critical defects escaped to production",
        "Execution time improved 15% (45m avg)",
    ],
    "critical_issues": [
        "test_checkout_payment_validation flaky at 15%",
        "API Endpoints coverage gap of 55%",
    ],
    "recommended_actions": [
        "Resolve payment regression before production deployment",
        "Increase API test coverage to 80%",
        "Fix flaky checkout tests",
    ],
    "release_recommendation": "GO WITH RISKS",
    "confidence": 94,
}

# Quality score center — dimension scores with trend + target + status
QUALITY_SCORES = [
    {"dimension": "Overall Quality", "score": 87, "trend": "+4.2%", "target": 90, "status": "good", "color": "success"},
    {"dimension": "Automation", "score": 78, "trend": "+5.2%", "target": 85, "status": "medium", "color": "warning"},
    {"dimension": "Functional", "score": 94, "trend": "+2%", "target": 90, "status": "good", "color": "success"},
    {"dimension": "API", "score": 65, "trend": "+1%", "target": 80, "status": "low", "color": "error"},
    {"dimension": "Performance", "score": 79, "trend": "+8%", "target": 85, "status": "medium", "color": "warning"},
    {"dimension": "Accessibility", "score": 91, "trend": "+2%", "target": 90, "status": "good", "color": "success"},
    {"dimension": "Security", "score": 94, "trend": "+3%", "target": 95, "status": "good", "color": "success"},
    {"dimension": "Business", "score": 85, "trend": "+2%", "target": 88, "status": "good", "color": "success"},
    {"dimension": "Visual", "score": 82, "trend": "+1%", "target": 85, "status": "medium", "color": "warning"},
    {"dimension": "Database", "score": 88, "trend": "+2%", "target": 85, "status": "good", "color": "success"},
]

# Business flow quality
BUSINESS_FLOW_QUALITY = [
    {"id": "flow_login", "name": "Login", "coverage": 100, "pass_rate": 98, "failures": 1, "risk": "low", "last_execution": "2h ago", "impact": "Critical", "automation": 100, "confidence": 99, "icon": "🔐"},
    {"id": "flow_search", "name": "Search", "coverage": 82, "pass_rate": 88, "failures": 4, "risk": "medium", "last_execution": "3h ago", "impact": "High", "automation": 82, "confidence": 90, "icon": "🔍"},
    {"id": "flow_product", "name": "Product Discovery", "coverage": 88, "pass_rate": 92, "failures": 2, "risk": "low", "last_execution": "1h ago", "impact": "High", "automation": 88, "confidence": 94, "icon": "📦"},
    {"id": "flow_cart", "name": "Cart", "coverage": 90, "pass_rate": 95, "failures": 3, "risk": "low", "last_execution": "4h ago", "impact": "Critical", "automation": 90, "confidence": 96, "icon": "🛒"},
    {"id": "flow_checkout", "name": "Checkout", "coverage": 75, "pass_rate": 82, "failures": 8, "risk": "high", "last_execution": "1h ago", "impact": "Critical", "automation": 75, "confidence": 85, "icon": "💳"},
    {"id": "flow_payment", "name": "Payment", "coverage": 71, "pass_rate": 78, "failures": 12, "risk": "critical", "last_execution": "30m ago", "impact": "Critical", "automation": 71, "confidence": 80, "icon": "💰"},
    {"id": "flow_order", "name": "Order", "coverage": 84, "pass_rate": 90, "failures": 2, "risk": "low", "last_execution": "5h ago", "impact": "High", "automation": 84, "confidence": 92, "icon": "📝"},
    {"id": "flow_cancel", "name": "Cancellation", "coverage": 68, "pass_rate": 85, "failures": 3, "risk": "medium", "last_execution": "6h ago", "impact": "Medium", "automation": 68, "confidence": 86, "icon": "❌"},
    {"id": "flow_refund", "name": "Refund", "coverage": 62, "pass_rate": 80, "failures": 4, "risk": "medium", "last_execution": "8h ago", "impact": "Medium", "automation": 62, "confidence": 82, "icon": "💸"},
    {"id": "flow_account", "name": "Account", "coverage": 70, "pass_rate": 88, "failures": 2, "risk": "low", "last_execution": "7h ago", "impact": "Medium", "automation": 70, "confidence": 88, "icon": "👤"},
]

# Bug intelligence
BUG_INTELLIGENCE = {
    "summary": {
        "total": 43, "critical": 0, "high": 3, "medium": 12, "low": 28,
        "new": 7, "resolved": 15, "reopened": 2, "regression": 4, "flaky_related": 8,
    },
    "severity_distribution": [
        {"severity": "Critical", "count": 0, "color": "error"},
        {"severity": "High", "count": 3, "color": "warning"},
        {"severity": "Medium", "count": 12, "color": "info"},
        {"severity": "Low", "count": 28, "color": "muted"},
    ],
    "trend": [
        {"date": "W1", "bugs": 58}, {"date": "W2", "bugs": 52}, {"date": "W3", "bugs": 48},
        {"date": "W4", "bugs": 45}, {"date": "W5", "bugs": 43},
    ],
    "by_module": [
        {"module": "Checkout", "count": 12, "color": "error"},
        {"module": "Payment", "count": 9, "color": "warning"},
        {"module": "Search", "count": 7, "color": "info"},
        {"module": "Cart", "count": 6, "color": "info"},
        {"module": "Profile", "count": 5, "color": "muted"},
        {"module": "Catalog", "count": 4, "color": "muted"},
    ],
    "root_causes": [
        {"cause": "Logic Error", "count": 14, "color": "error"},
        {"cause": "Timing/Race", "count": 9, "color": "warning"},
        {"cause": "Data Issue", "count": 8, "color": "info"},
        {"cause": "UI/Visual", "count": 7, "color": "muted"},
        {"cause": "Environment", "count": 5, "color": "muted"},
    ],
    "top_recurring": [
        {"name": "BUG-Price: rounding edge case", "occurrences": 5, "severity": "high", "color": "warning"},
        {"name": "BUG-Cart: persistence race", "occurrences": 4, "severity": "medium", "color": "info"},
        {"name": "BUG-Search: result ordering", "occurrences": 3, "severity": "medium", "color": "info"},
    ],
    "ai_summary": "Most defects cluster around the checkout/payment subgraph (49% of total). Recommend contract testing + locator healing for dynamic payment elements.",
}

# Execution intelligence
EXECUTION_INTELLIGENCE = {
    "summary": {
        "total": 1234, "passed": 1162, "failed": 47, "skipped": 25, "retries": 38,
        "avg_duration": "45m", "p95_duration": "78m", "parallelization": "8x",
    },
    "browser_distribution": [
        {"browser": "Chromium", "count": 612, "color": "primary"},
        {"browser": "Firefox", "count": 312, "color": "secondary"},
        {"browser": "WebKit", "count": 198, "color": "info"},
        {"browser": "Edge", "count": 112, "color": "accent"},
    ],
    "env_distribution": [
        {"env": "Staging", "count": 689, "color": "success"},
        {"env": "Production", "count": 312, "color": "warning"},
        {"env": "Dev", "count": 233, "color": "info"},
    ],
    "trend": [
        {"date": "D1", "executions": 38, "passed": 36}, {"date": "D2", "executions": 42, "passed": 40},
        {"date": "D3", "executions": 45, "passed": 43}, {"date": "D4", "executions": 39, "passed": 37},
        {"date": "D5", "executions": 48, "passed": 45}, {"date": "D6", "executions": 44, "passed": 42},
        {"date": "D7", "executions": 41, "passed": 39},
    ],
}

# AI performance intelligence
AI_PERFORMANCE_INTEL = {
    "summary": {
        "agents": 16, "executions": 4587, "success_rate": 96.5, "confidence": 92,
        "tokens": "2.5M", "avg_latency": "1.2s", "efficiency": 94,
    },
    "top_performers": [
        {"agent": "Intelligence Agent", "tasks": 1234, "success": 98, "color": "success"},
        {"agent": "Testing Agent", "tasks": 1567, "success": 95, "color": "success"},
        {"agent": "Documentation Agent", "tasks": 456, "success": 99, "color": "success"},
    ],
    "underperformers": [
        {"agent": "Infrastructure Agent", "tasks": 1096, "success": 94, "color": "warning"},
    ],
    "model_usage": [
        {"model": "GPT-4", "requests": 3456, "percentage": 45, "color": "primary"},
        {"model": "Claude", "requests": 2345, "percentage": 30, "color": "secondary"},
        {"model": "Gemini", "requests": 1234, "percentage": 16, "color": "info"},
        {"model": "DeepSeek", "requests": 678, "percentage": 9, "color": "accent"},
    ],
    "tool_usage": [
        {"tool": "bash", "count": 2340, "color": "primary"},
        {"tool": "file_edit", "count": 1567, "color": "secondary"},
        {"tool": "browser", "count": 890, "color": "info"},
        {"tool": "search", "count": 678, "color": "accent"},
    ],
}

# Release readiness
RELEASE_READINESS = {
    "score": 93,
    "status": "GO WITH RISKS",
    "risk_level": "Medium",
    "gates": [
        {"name": "Functional", "status": "pass", "score": 94, "threshold": 90, "color": "success"},
        {"name": "API", "status": "pass", "score": 92, "threshold": 85, "color": "success"},
        {"name": "Security", "status": "pass", "score": 94, "threshold": 90, "color": "success"},
        {"name": "Accessibility", "status": "pass", "score": 91, "threshold": 90, "color": "success"},
        {"name": "Performance", "status": "warn", "score": 79, "threshold": 85, "color": "warning"},
        {"name": "Flaky Tests", "status": "warn", "score": 97.7, "threshold": 98, "color": "warning"},
        {"name": "Coverage", "status": "pass", "score": 78.5, "threshold": 75, "color": "success"},
        {"name": "Regression", "status": "pass", "score": 95, "threshold": 90, "color": "success"},
    ],
    "readiness_breakdown": [
        {"label": "Business Readiness", "score": 90, "color": "success"},
        {"label": "Security Readiness", "score": 94, "color": "success"},
        {"label": "Performance Readiness", "score": 79, "color": "warning"},
        {"label": "Accessibility Readiness", "score": 91, "color": "success"},
        {"label": "Automation Readiness", "score": 82, "color": "warning"},
    ],
    "ai_confidence": 92,
}

# Quality gates matrix
QUALITY_GATES = [
    {"gate": "Frontend", "status": "pass", "score": 92, "threshold": 85, "owner": "Frontend Team", "last_run": "1h ago", "recommendation": "Maintain", "color": "success"},
    {"gate": "Backend", "status": "pass", "score": 90, "threshold": 85, "owner": "Backend Team", "last_run": "2h ago", "recommendation": "Maintain", "color": "success"},
    {"gate": "API", "status": "warn", "score": 65, "threshold": 80, "owner": "API Team", "last_run": "3h ago", "recommendation": "Increase coverage", "color": "warning"},
    {"gate": "Database", "status": "pass", "score": 88, "threshold": 85, "owner": "Data Team", "last_run": "4h ago", "recommendation": "Maintain", "color": "success"},
    {"gate": "Security", "status": "pass", "score": 94, "threshold": 90, "owner": "Security Team", "last_run": "1h ago", "recommendation": "Maintain", "color": "success"},
    {"gate": "Performance", "status": "warn", "score": 79, "threshold": 85, "owner": "Perf Team", "last_run": "2h ago", "recommendation": "Optimize checkout", "color": "warning"},
    {"gate": "Accessibility", "status": "pass", "score": 91, "threshold": 90, "owner": "A11y Team", "last_run": "5h ago", "recommendation": "Maintain", "color": "success"},
    {"gate": "Visual", "status": "pass", "score": 82, "threshold": 80, "owner": "QA Team", "last_run": "3h ago", "recommendation": "Maintain", "color": "success"},
    {"gate": "Regression", "status": "pass", "score": 95, "threshold": 90, "owner": "QA Team", "last_run": "1h ago", "recommendation": "Maintain", "color": "success"},
    {"gate": "Business", "status": "pass", "score": 85, "threshold": 80, "owner": "Product Team", "last_run": "6h ago", "recommendation": "Maintain", "color": "success"},
    {"gate": "Documentation", "status": "pass", "score": 88, "threshold": 80, "owner": "Docs Team", "last_run": "8h ago", "recommendation": "Maintain", "color": "success"},
]

# Coverage intelligence (by area)
COVERAGE_INTELLIGENCE = [
    {"area": "Application", "covered": 82, "partial": 12, "missing": 6, "risk": "low", "trend": "+3%", "recommendation": "Maintain", "color": "success"},
    {"area": "Module", "covered": 78, "partial": 15, "missing": 7, "risk": "medium", "trend": "+2%", "recommendation": "Close gaps", "color": "warning"},
    {"area": "Business Flow", "covered": 85, "partial": 10, "missing": 5, "risk": "low", "trend": "+2%", "recommendation": "Maintain", "color": "success"},
    {"area": "Frontend", "covered": 88, "partial": 8, "missing": 4, "risk": "low", "trend": "+4%", "recommendation": "Maintain", "color": "success"},
    {"area": "Backend", "covered": 80, "partial": 12, "missing": 8, "risk": "medium", "trend": "+2%", "recommendation": "Increase", "color": "warning"},
    {"area": "API", "covered": 65, "partial": 20, "missing": 15, "risk": "high", "trend": "+1%", "recommendation": "Priority focus", "color": "error"},
    {"area": "Database", "covered": 88, "partial": 8, "missing": 4, "risk": "low", "trend": "+2%", "recommendation": "Maintain", "color": "success"},
    {"area": "Accessibility", "covered": 91, "partial": 6, "missing": 3, "risk": "low", "trend": "+2%", "recommendation": "Maintain", "color": "success"},
    {"area": "Security", "covered": 94, "partial": 4, "missing": 2, "risk": "low", "trend": "+1%", "recommendation": "Maintain", "color": "success"},
    {"area": "Performance", "covered": 79, "partial": 14, "missing": 7, "risk": "medium", "trend": "+8%", "recommendation": "Add benchmarks", "color": "warning"},
    {"area": "Visual", "covered": 82, "partial": 12, "missing": 6, "risk": "medium", "trend": "+1%", "recommendation": "Increase", "color": "warning"},
]

# Flaky test categories
FLAKY_CATEGORIES = [
    {"category": "Locator Instability", "count": 8, "color": "error", "recommendation": "Adopt locator healing + stable data-testid"},
    {"category": "Timing", "count": 10, "color": "warning", "recommendation": "Add explicit waits + retry policies"},
    {"category": "Network", "count": 7, "color": "info", "recommendation": "Mock flaky endpoints + retry on 5xx"},
    {"category": "Environment", "count": 1, "color": "muted", "recommendation": "Stabilize test env config"},
    {"category": "Data", "count": 4, "color": "info", "recommendation": "Use deterministic test data fixtures"},
    {"category": "Animation", "count": 3, "color": "muted", "recommendation": "Wait for animation completion"},
    {"category": "Application Defect", "count": 5, "color": "error", "recommendation": "File bug — real defect, not test issue"},
]

# Quality risk matrix
QUALITY_RISK_MATRIX = [
    {"risk": "Business Risk", "severity": "medium", "probability": 30, "impact": "High", "owner": "Product Team", "status": "mitigated", "recommendation": "Monitor checkout conversions", "color": "warning"},
    {"risk": "Technical Risk", "severity": "high", "probability": 55, "impact": "High", "owner": "Eng Team", "status": "open", "recommendation": "Refactor payment service", "color": "error"},
    {"risk": "Security Risk", "severity": "low", "probability": 15, "impact": "Critical", "owner": "Security Team", "status": "mitigated", "recommendation": "Maintain SAST + pentest cadence", "color": "success"},
    {"risk": "Performance Risk", "severity": "medium", "probability": 40, "impact": "Medium", "owner": "Perf Team", "status": "open", "recommendation": "Optimize checkout critical path", "color": "warning"},
    {"risk": "Automation Risk", "severity": "medium", "probability": 35, "impact": "Medium", "owner": "QA Team", "status": "open", "recommendation": "Close API coverage gaps", "color": "warning"},
    {"risk": "Accessibility Risk", "severity": "low", "probability": 12, "impact": "Medium", "owner": "A11y Team", "status": "mitigated", "recommendation": "Maintain WCAG AA", "color": "success"},
]

# AI recommendations
AI_RECOMMENDATIONS = [
    {"priority": "high", "finding": "Checkout flaky tests", "impact": "Release confidence", "recommendation": "Reduce checkout flaky tests", "expected": "+5% release confidence", "confidence": 94, "color": "warning"},
    {"priority": "critical", "finding": "API coverage gap", "impact": "Critical logic exposed", "recommendation": "Increase API coverage to 80%", "expected": "+15% API coverage", "confidence": 96, "color": "error"},
    {"priority": "medium", "finding": "Performance regression", "impact": "User experience", "recommendation": "Optimize checkout critical path", "expected": "-12% P95 latency", "confidence": 88, "color": "warning"},
    {"priority": "medium", "finding": "Flaky locator instability", "impact": "Test reliability", "recommendation": "Adopt locator healing", "expected": "-40% flaky rate", "confidence": 92, "color": "info"},
    {"priority": "low", "finding": "Visual coverage", "impact": "UI consistency", "recommendation": "Add visual regression tests", "expected": "+3% visual coverage", "confidence": 85, "color": "success"},
]

# Quality timeline
QUALITY_TIMELINE = [
    {"step": "Build Started", "icon": "🔨", "detail": "Build #1247 triggered on main", "color": "primary", "time": "T+0m"},
    {"step": "Tests Executed", "icon": "🧪", "detail": "1,247 tests across 3 browsers", "color": "secondary", "time": "T+8m"},
    {"step": "Failures Detected", "icon": "❌", "detail": "47 failures, 38 retries", "color": "error", "time": "T+45m"},
    {"step": "AI Analysis", "icon": "🧠", "detail": "AI analyzed failures, 92% confidence", "color": "info", "time": "T+47m"},
    {"step": "Bug Generation", "icon": "🐛", "detail": "7 new bugs, 4 regressions filed", "color": "warning", "time": "T+52m"},
    {"step": "Human Review", "icon": "👀", "detail": "3 high-severity reviewed", "color": "accent", "time": "T+60m"},
    {"step": "Quality Gates", "icon": "🚦", "detail": "6/8 gates passed, 2 warnings", "color": "success", "time": "T+62m"},
    {"step": "Release Assessment", "icon": "🚀", "detail": "GO WITH RISKS — 93% ready", "color": "success", "time": "T+65m"},
    {"step": "Report Generated", "icon": "📄", "detail": "Executive report exported", "color": "muted", "time": "T+67m"},
]

# Release comparison (current vs previous)
RELEASE_COMPARISON = {
    "current": "v3.2.1 (Build #1247)",
    "previous": "v3.2.0 (Build #1180)",
    "metrics": [
        {"metric": "Quality", "current": 87, "previous": 81, "color": "success", "unit": "%"},
        {"metric": "Coverage", "current": 78.5, "previous": 73.3, "color": "success", "unit": "%"},
        {"metric": "Pass Rate", "current": 94.2, "previous": 92.9, "color": "success", "unit": "%"},
        {"metric": "Failures", "current": 47, "previous": 62, "color": "success", "unit": ""},
        {"metric": "Bugs", "current": 43, "previous": 58, "color": "success", "unit": ""},
        {"metric": "Flaky Tests", "current": 28, "previous": 41, "color": "success", "unit": ""},
        {"metric": "Performance", "current": 79, "previous": 71, "color": "success", "unit": "%"},
        {"metric": "Security", "current": 94, "previous": 93, "color": "success", "unit": "%"},
        {"metric": "Accessibility", "current": 91, "previous": 89, "color": "success", "unit": "%"},
        {"metric": "AI Confidence", "current": 92, "previous": 88, "color": "success", "unit": "%"},
    ],
}

# Report library categories
REPORT_LIBRARY = [
    {"name": "Q3 Executive Summary", "category": "Executive", "created": "1d ago", "author": "AI Agent", "status": "generated", "coverage": 87, "quality": 87, "color": "primary"},
    {"name": "Weekly QA Summary", "category": "QA", "created": "2h ago", "author": "QA Agent", "status": "generated", "coverage": 78, "quality": 92, "color": "secondary"},
    {"name": "Automation Report", "category": "Automation", "created": "5h ago", "author": "Testing Agent", "status": "generated", "coverage": 78, "quality": 90, "color": "success"},
    {"name": "API Coverage Report", "category": "API", "created": "6h ago", "author": "API Agent", "status": "generated", "coverage": 65, "quality": 80, "color": "warning"},
    {"name": "Performance Benchmark", "category": "Performance", "created": "1d ago", "author": "Perf Agent", "status": "generated", "coverage": 79, "quality": 79, "color": "warning"},
    {"name": "Security Scan Report", "category": "Security", "created": "3d ago", "author": "Security Agent", "status": "generated", "coverage": 94, "quality": 94, "color": "success"},
    {"name": "Accessibility Audit", "category": "Accessibility", "created": "4d ago", "author": "A11y Agent", "status": "generated", "coverage": 91, "quality": 91, "color": "success"},
    {"name": "Release v3.2.1 Report", "category": "Release", "created": "2d ago", "author": "Release Agent", "status": "scheduled", "coverage": 93, "quality": 87, "color": "info"},
]

# Quick actions
REPORTS_QUICK_ACTIONS = [
    {"name": "Executive Report", "icon": "📈", "description": "Generate executive report", "color": "primary"},
    {"name": "Regression Report", "icon": "🔄", "description": "Generate regression report", "color": "secondary"},
    {"name": "Compare Releases", "icon": "⚖️", "description": "Compare current vs previous release", "color": "info"},
    {"name": "Analyze Quality", "icon": "✅", "description": "Analyze overall quality", "color": "success"},
    {"name": "Analyze Flaky", "icon": "📳", "description": "Analyze flaky tests", "color": "warning"},
    {"name": "Analyze Coverage", "icon": "📊", "description": "Analyze coverage gaps", "color": "accent"},
    {"name": "Export Report", "icon": "📤", "description": "Export current report", "color": "primary"},
    {"name": "Release Advisor", "icon": "🚀", "description": "Open Release Advisor", "color": "success"},
    {"name": "Knowledge Graph", "icon": "🕸️", "description": "Open Knowledge Graph", "color": "secondary"},
    {"name": "AI Chat", "icon": "💬", "description": "Open AI Chat Workspace", "color": "info"},
    {"name": "Open Mission", "icon": "🎯", "description": "Open Mission Planner", "color": "accent"},
    {"name": "Health Scan", "icon": "🩺", "description": "Run quality health scan", "color": "warning"},
]

# Bottom workspace tabs
REPORTS_BOTTOM_TABS = ["Dashboard", "Trends", "Coverage", "Quality", "Bugs", "Executions", "AI Performance", "Flaky Tests", "Release", "Reports"]

# Trend views
TREND_VIEWS = {
    "Daily": [
        {"date": "D1", "quality": 84, "pass_rate": 93, "failure_rate": 7, "coverage": 77, "flaky_rate": 2.8, "defect_rate": 4.5, "ai_confidence": 90},
        {"date": "D2", "quality": 85, "pass_rate": 93.5, "failure_rate": 6.5, "coverage": 77.5, "flaky_rate": 2.6, "defect_rate": 4.2, "ai_confidence": 91},
        {"date": "D3", "quality": 86, "pass_rate": 94, "failure_rate": 6, "coverage": 78, "flaky_rate": 2.4, "defect_rate": 3.9, "ai_confidence": 91},
        {"date": "D4", "quality": 86.5, "pass_rate": 94.1, "failure_rate": 5.9, "coverage": 78.2, "flaky_rate": 2.3, "defect_rate": 3.7, "ai_confidence": 92},
        {"date": "D5", "quality": 87, "pass_rate": 94.2, "failure_rate": 5.8, "coverage": 78.5, "flaky_rate": 2.3, "defect_rate": 3.5, "ai_confidence": 92},
    ],
    "Weekly": [
        {"date": "W1", "quality": 81, "pass_rate": 91, "failure_rate": 9, "coverage": 73, "flaky_rate": 4.2, "defect_rate": 5.8, "ai_confidence": 86},
        {"date": "W2", "quality": 83, "pass_rate": 92, "failure_rate": 8, "coverage": 75, "flaky_rate": 3.5, "defect_rate": 5.2, "ai_confidence": 88},
        {"date": "W3", "quality": 85, "pass_rate": 93, "failure_rate": 7, "coverage": 76.5, "flaky_rate": 2.9, "defect_rate": 4.6, "ai_confidence": 90},
        {"date": "W4", "quality": 87, "pass_rate": 94.2, "failure_rate": 5.8, "coverage": 78.5, "flaky_rate": 2.3, "defect_rate": 3.5, "ai_confidence": 92},
    ],
    "Monthly": [
        {"date": "M1", "quality": 78, "pass_rate": 90, "failure_rate": 10, "coverage": 70, "flaky_rate": 5.0, "defect_rate": 6.5, "ai_confidence": 84},
        {"date": "M2", "quality": 82, "pass_rate": 91.5, "failure_rate": 8.5, "coverage": 74, "flaky_rate": 3.8, "defect_rate": 5.0, "ai_confidence": 88},
        {"date": "M3", "quality": 87, "pass_rate": 94.2, "failure_rate": 5.8, "coverage": 78.5, "flaky_rate": 2.3, "defect_rate": 3.5, "ai_confidence": 92},
    ],
    "Release": [
        {"date": "v3.1", "quality": 75, "pass_rate": 89, "failure_rate": 11, "coverage": 68, "flaky_rate": 5.5, "defect_rate": 7.0, "ai_confidence": 82},
        {"date": "v3.2.0", "quality": 81, "pass_rate": 92.9, "failure_rate": 7.1, "coverage": 73.3, "flaky_rate": 4.0, "defect_rate": 5.5, "ai_confidence": 88},
        {"date": "v3.2.1", "quality": 87, "pass_rate": 94.2, "failure_rate": 5.8, "coverage": 78.5, "flaky_rate": 2.3, "defect_rate": 3.5, "ai_confidence": 92},
    ],
}
