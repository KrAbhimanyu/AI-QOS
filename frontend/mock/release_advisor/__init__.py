"""Mock data for the AI Release Advisor — Autonomous Release Decision Center.

All data is professional mock content, frontend-only, and structured as a
backend-ready contract (no business logic, no external calls). Future backend
integration can replace these constants with API responses without changing
the view/component signatures.
"""

from datetime import datetime, timedelta


# ---------------------------------------------------------------------------
# Release hero header chips
# ---------------------------------------------------------------------------
RA_HERO_KPIS = [
    {"label": "Mission", "value": "E2E Regression v2.1", "icon": "🎯", "color": "primary"},
    {"label": "Application", "value": "E-Commerce", "icon": "🏢", "color": "accent"},
    {"label": "Release", "value": "v3.2.1", "icon": "🏷️", "color": "info"},
    {"label": "Build", "value": "#1247", "icon": "🔨", "color": "secondary"},
    {"label": "Commit", "value": "a1b2c3d", "icon": "🔗", "color": "primary"},
    {"label": "Branch", "value": "main", "icon": "🌿", "color": "success"},
    {"label": "Environment", "value": "Production", "icon": "🌐", "color": "warning"},
    {"label": "RC Version", "value": "RC-3", "icon": "🚦", "color": "info"},
    {"label": "Status", "value": "GO WITH RISKS", "icon": "🟡", "color": "warning"},
    {"label": "AI Confidence", "value": "94%", "icon": "🧠", "color": "success"},
    {"label": "Last Analysis", "value": "3m ago", "icon": "🕐", "color": "muted"},
]

# Release score strip MetricCards
RA_SCORE_METRICS = [
    {"title": "Overall Score", "value": "87", "icon": "🎯", "trend": "+4.2%", "subtitle": "≥ 80 threshold", "status": "success", "threshold": 80},
    {"title": "Quality", "value": "87%", "icon": "✅", "trend": "+4.2%", "subtitle": "Excellent", "status": "success", "threshold": 85},
    {"title": "Automation", "value": "78.5%", "icon": "🤖", "trend": "+5.2%", "subtitle": "Target 85%", "status": "warning", "threshold": 85},
    {"title": "Coverage", "value": "78.5%", "icon": "📊", "trend": "+5.2%", "subtitle": "Above target", "status": "success", "threshold": 75},
    {"title": "Security", "value": "94%", "icon": "🔒", "trend": "+1%", "subtitle": "No criticals", "status": "success", "threshold": 90},
    {"title": "Performance", "value": "79%", "icon": "⚡", "trend": "+8%", "subtitle": "Below target", "status": "warning", "threshold": 85},
    {"title": "Accessibility", "value": "91%", "icon": "♿", "trend": "+2%", "subtitle": "WCAG AA", "status": "success", "threshold": 90},
    {"title": "Business", "value": "85%", "icon": "💼", "trend": "+2%", "subtitle": "Flows covered", "status": "success", "threshold": 80},
    {"title": "Risk", "value": "23", "icon": "⚠️", "trend": "-4", "subtitle": "Medium", "status": "warning", "threshold": 30},
    {"title": "AI Confidence", "value": "94%", "icon": "🧠", "trend": "+3%", "subtitle": "High certainty", "status": "success", "threshold": 85},
    {"title": "Rollback Ready", "value": "98%", "icon": "↩️", "trend": "+1%", "subtitle": "Ready", "status": "success", "threshold": 90},
]

# AI release decision
RA_DECISION = {
    "decision": "GO WITH RISKS",
    "confidence": 94,
    "reason": "Release is acceptable. Quality and security exceed thresholds; performance and flaky tests require attention but are non-blocking.",
    "evidence": [
        "Quality score 87% exceeds 85% threshold (+4.2%)",
        "Zero critical security vulnerabilities",
        "Coverage 78.5% above 75% gate",
        "12 flaky tests detected in checkout/payment",
        "Performance 8% slower than previous release",
    ],
    "blocking_issues": [
        "Performance Gate below threshold (79 < 85)",
        "Security Approval pending",
    ],
    "non_blocking_issues": [
        "12 flaky tests (checkout/payment)",
        "API coverage 65% (below 80% target)",
        "3 high-severity bugs open",
    ],
    "business_impact": "LOW",
    "technical_impact": "MEDIUM",
    "recommended_action": "Proceed after confirming Performance Gate and obtaining Security Approval.",
}

# Decision explanation signals
RA_DECISION_SIGNALS = {
    "quality": {"label": "Quality", "status": "pass", "detail": "Above threshold (87 ≥ 85)", "color": "success"},
    "security": {"label": "Security", "status": "pass", "detail": "No critical vulnerabilities", "color": "success"},
    "performance": {"label": "Performance", "status": "warn", "detail": "8% slower than previous release", "color": "warning"},
    "flaky": {"label": "Flaky Tests", "status": "warn", "detail": "12 unstable tests", "color": "warning"},
    "coverage": {"label": "Coverage", "status": "pass", "detail": "78.5% above gate", "color": "success"},
    "business": {"label": "Business Flow", "status": "pass", "detail": "Checkout covered", "color": "success"},
    "regression": {"label": "Regression", "status": "pass", "detail": "95% pass (≥ 90)", "color": "success"},
    "approval": {"label": "Approvals", "status": "warn", "detail": "2 of 8 pending", "color": "warning"},
}

# Decision path (reasoning steps)
RA_DECISION_PATH = [
    {"step": "Collect Signals", "detail": "Gathered 487 metrics across 11 gates", "result": "complete", "color": "success"},
    {"step": "Evaluate Gates", "detail": "9 of 11 gates passed, 2 warnings", "result": "partial", "color": "warning"},
    {"step": "Assess Risks", "detail": "Overall risk 23 (Medium), 0 critical", "result": "pass", "color": "success"},
    {"step": "Check Approvals", "detail": "6 of 8 approved, 2 pending", "result": "partial", "color": "warning"},
    {"step": "Business Impact", "detail": "Low impact, checkout protected", "result": "pass", "color": "success"},
    {"step": "Rollback Check", "detail": "Rollback ready, 98% confidence", "result": "pass", "color": "success"},
    {"step": "AI Verdict", "detail": "GO WITH RISKS — 94% confidence", "result": "decision", "color": "warning"},
]

# Quality gates (11)
RA_QUALITY_GATES = [
    {"gate": "Frontend", "status": "pass", "score": 92, "threshold": 85, "owner": "Frontend Team", "last_run": "1h ago", "blocking": False, "recommendation": "Maintain", "color": "success"},
    {"gate": "Backend", "status": "pass", "score": 90, "threshold": 85, "owner": "Backend Team", "last_run": "2h ago", "blocking": False, "recommendation": "Maintain", "color": "success"},
    {"gate": "API", "status": "warning", "score": 65, "threshold": 80, "owner": "API Team", "last_run": "3h ago", "blocking": False, "recommendation": "Increase coverage to 80%", "color": "warning"},
    {"gate": "Database", "status": "pass", "score": 88, "threshold": 85, "owner": "Data Team", "last_run": "4h ago", "blocking": False, "recommendation": "Maintain", "color": "success"},
    {"gate": "Performance", "status": "fail", "score": 79, "threshold": 85, "owner": "Perf Team", "last_run": "2h ago", "blocking": True, "recommendation": "Optimize checkout critical path", "color": "error"},
    {"gate": "Accessibility", "status": "pass", "score": 91, "threshold": 90, "owner": "A11y Team", "last_run": "5h ago", "blocking": False, "recommendation": "Maintain", "color": "success"},
    {"gate": "Visual", "status": "pass", "score": 82, "threshold": 80, "owner": "QA Team", "last_run": "3h ago", "blocking": False, "recommendation": "Maintain", "color": "success"},
    {"gate": "Security", "status": "pass", "score": 94, "threshold": 90, "owner": "Security Team", "last_run": "1h ago", "blocking": False, "recommendation": "Maintain", "color": "success"},
    {"gate": "Regression", "status": "pass", "score": 95, "threshold": 90, "owner": "QA Team", "last_run": "1h ago", "blocking": False, "recommendation": "Maintain", "color": "success"},
    {"gate": "Documentation", "status": "pass", "score": 88, "threshold": 80, "owner": "Docs Team", "last_run": "8h ago", "blocking": False, "recommendation": "Maintain", "color": "success"},
    {"gate": "Business Approval", "status": "warning", "score": 75, "threshold": 80, "owner": "Product Team", "last_run": "6h ago", "blocking": True, "recommendation": "Obtain Security & Release Manager sign-off", "color": "warning"},
]

# Blocking gates
RA_BLOCKERS = [
    {"name": "Performance Gate", "type": "gate", "severity": "high", "detail": "79 < 85 threshold", "owner": "Perf Team", "color": "error"},
    {"name": "Security Approval", "type": "approval", "severity": "high", "detail": "Pending sign-off", "owner": "Security Team", "color": "warning"},
    {"name": "Business Approval", "type": "approval", "severity": "medium", "detail": "Pending sign-off", "owner": "Product Team", "color": "warning"},
]

# Approval matrix
RA_APPROVALS = [
    {"role": "QA Lead", "name": "Sarah Chen", "status": "approved", "timestamp": "2h ago", "comment": "Quality acceptable, flaky tests tracked", "risk": "low", "color": "success"},
    {"role": "Developer", "name": "Mike Ross", "status": "approved", "timestamp": "3h ago", "comment": "Code reviewed, no blockers", "risk": "low", "color": "success"},
    {"role": "Product Owner", "name": "Emma Davis", "status": "approved", "timestamp": "4h ago", "comment": "Features delivered as scoped", "risk": "low", "color": "success"},
    {"role": "Engineering Manager", "name": "James Lee", "status": "approved", "timestamp": "5h ago", "comment": "Tech debt within limits", "risk": "low", "color": "success"},
    {"role": "Security", "name": "Alan Park", "status": "pending", "timestamp": "—", "comment": "Awaiting pentest review", "risk": "medium", "color": "warning"},
    {"role": "Performance", "name": "Lisa Wong", "status": "warning", "timestamp": "1h ago", "comment": "8% regression — investigate", "risk": "high", "color": "warning"},
    {"role": "Accessibility", "name": "Tom Hall", "status": "approved", "timestamp": "5h ago", "comment": "WCAG AA met", "risk": "low", "color": "success"},
    {"role": "Release Manager", "name": "Nina Vega", "status": "pending", "timestamp": "—", "comment": "Pending final decision", "risk": "medium", "color": "warning"},
]

# Risk intelligence
RA_RISKS = [
    {"risk": "Business Risk", "category": "Business", "probability": 30, "impact": "High", "severity": "medium", "owner": "Product Team", "status": "mitigated", "mitigation": "Monitor checkout conversions", "recommendation": "Add canary rollout", "color": "warning", "impact_level": "medium", "prob_level": "medium"},
    {"risk": "Technical Risk", "category": "Technical", "probability": 55, "impact": "High", "severity": "high", "owner": "Eng Team", "status": "open", "mitigation": "Refactor payment service", "recommendation": "Schedule post-release refactor", "color": "error", "impact_level": "high", "prob_level": "high"},
    {"risk": "Security Risk", "category": "Security", "probability": 15, "impact": "Critical", "severity": "low", "owner": "Security Team", "status": "mitigated", "mitigation": "SAST + pentest cadence", "recommendation": "Maintain cadence", "color": "success", "impact_level": "critical", "prob_level": "low"},
    {"risk": "Performance Risk", "category": "Performance", "probability": 40, "impact": "Medium", "severity": "medium", "owner": "Perf Team", "status": "open", "mitigation": "Optimize checkout path", "recommendation": "Load test before deploy", "color": "warning", "impact_level": "medium", "prob_level": "medium"},
    {"risk": "Automation Risk", "category": "Automation", "probability": 35, "impact": "Medium", "severity": "medium", "owner": "QA Team", "status": "open", "mitigation": "Close API coverage gaps", "recommendation": "Add API contract tests", "color": "warning", "impact_level": "medium", "prob_level": "medium"},
    {"risk": "Accessibility Risk", "category": "Accessibility", "probability": 12, "impact": "Medium", "severity": "low", "owner": "A11y Team", "status": "mitigated", "mitigation": "Maintain WCAG AA", "recommendation": "Maintain", "color": "success", "impact_level": "medium", "prob_level": "low"},
    {"risk": "Infrastructure Risk", "category": "Infrastructure", "probability": 20, "impact": "High", "severity": "low", "owner": "DevOps Team", "status": "mitigated", "mitigation": "Auto-scaling configured", "recommendation": "Verify capacity", "color": "success", "impact_level": "high", "prob_level": "low"},
    {"risk": "Data Risk", "category": "Data", "probability": 18, "impact": "Critical", "severity": "low", "owner": "Data Team", "status": "mitigated", "mitigation": "Backups verified, migration reversible", "recommendation": "Maintain", "color": "success", "impact_level": "critical", "prob_level": "low"},
]

# AI risk predictions
RA_RISK_PREDICTIONS = [
    {"failure": "Checkout Failure", "probability": 18, "impact": "High", "confidence": 91, "affected_flow": "Checkout", "affected_component": "Payment Service", "recommendation": "Run targeted payment regression", "color": "warning"},
    {"failure": "Payment Latency Spike", "probability": 24, "impact": "Medium", "confidence": 88, "affected_flow": "Payment", "affected_component": "Gateway Adapter", "recommendation": "Add latency guard + circuit breaker", "color": "warning"},
    {"failure": "Search Index Drift", "probability": 9, "impact": "Low", "confidence": 82, "affected_flow": "Search", "affected_component": "Search Indexer", "recommendation": "Reindex after deploy", "color": "info"},
    {"failure": "Session Expiry Race", "probability": 14, "impact": "Medium", "confidence": 85, "affected_flow": "Account", "affected_component": "Session Store", "recommendation": "Validate token refresh path", "color": "info"},
]

# Coverage intelligence (current vs previous vs target)
RA_COVERAGE = [
    {"area": "Functional", "current": 94, "previous": 90, "target": 90, "trend": "+4%", "color": "success"},
    {"area": "Automation", "current": 78, "previous": 73, "target": 85, "trend": "+5%", "color": "warning"},
    {"area": "Business Flow", "current": 85, "previous": 82, "target": 80, "trend": "+3%", "color": "success"},
    {"area": "API", "current": 65, "previous": 60, "target": 80, "trend": "+5%", "color": "error"},
    {"area": "Security", "current": 94, "previous": 93, "target": 90, "trend": "+1%", "color": "success"},
    {"area": "Accessibility", "current": 91, "previous": 89, "target": 90, "trend": "+2%", "color": "success"},
    {"area": "Performance", "current": 79, "previous": 71, "target": 85, "trend": "+8%", "color": "warning"},
    {"area": "Visual", "current": 82, "previous": 80, "target": 85, "trend": "+2%", "color": "warning"},
]

# Business impact (flows)
RA_BUSINESS_IMPACT = [
    {"flow": "Login", "coverage": 100, "pass_rate": 98, "risk": "low", "revenue_impact": "Critical", "customer_impact": "High", "blocking": False, "confidence": 99, "icon": "🔐", "color": "success"},
    {"flow": "Search", "coverage": 82, "pass_rate": 88, "risk": "medium", "revenue_impact": "High", "customer_impact": "High", "blocking": False, "confidence": 90, "icon": "🔍", "color": "warning"},
    {"flow": "Product Discovery", "coverage": 88, "pass_rate": 92, "risk": "low", "revenue_impact": "High", "customer_impact": "Medium", "blocking": False, "confidence": 94, "icon": "📦", "color": "success"},
    {"flow": "Cart", "coverage": 90, "pass_rate": 95, "risk": "low", "revenue_impact": "Critical", "customer_impact": "High", "blocking": False, "confidence": 96, "icon": "🛒", "color": "success"},
    {"flow": "Checkout", "coverage": 75, "pass_rate": 82, "risk": "high", "revenue_impact": "Critical", "customer_impact": "Critical", "blocking": True, "confidence": 85, "icon": "💳", "color": "error"},
    {"flow": "Payment", "coverage": 71, "pass_rate": 78, "risk": "critical", "revenue_impact": "Critical", "customer_impact": "Critical", "blocking": True, "confidence": 80, "icon": "💰", "color": "error"},
    {"flow": "Order", "coverage": 84, "pass_rate": 90, "risk": "low", "revenue_impact": "High", "customer_impact": "Medium", "blocking": False, "confidence": 92, "icon": "📝", "color": "success"},
    {"flow": "Cancellation", "coverage": 68, "pass_rate": 85, "risk": "medium", "revenue_impact": "Medium", "customer_impact": "Low", "blocking": False, "confidence": 86, "icon": "❌", "color": "warning"},
    {"flow": "Refund", "coverage": 62, "pass_rate": 80, "risk": "medium", "revenue_impact": "Medium", "customer_impact": "Medium", "blocking": False, "confidence": 82, "icon": "💸", "color": "warning"},
    {"flow": "Account", "coverage": 70, "pass_rate": 88, "risk": "low", "revenue_impact": "Medium", "customer_impact": "Medium", "blocking": False, "confidence": 88, "icon": "👤", "color": "success"},
]

# Release comparison
RA_RELEASE_COMPARISON = {
    "current": "v3.2.1 (Build #1247)",
    "previous": "v3.2.0 (Build #1180)",
    "metrics": [
        {"metric": "Quality", "current": 87, "previous": 81, "color": "success", "unit": "%"},
        {"metric": "Pass Rate", "current": 94.2, "previous": 92.9, "color": "success", "unit": "%"},
        {"metric": "Coverage", "current": 78.5, "previous": 73.3, "color": "success", "unit": "%"},
        {"metric": "Bugs", "current": 43, "previous": 58, "color": "success", "unit": ""},
        {"metric": "Flaky Tests", "current": 28, "previous": 41, "color": "success", "unit": ""},
        {"metric": "Performance", "current": 79, "previous": 71, "color": "success", "unit": "%"},
        {"metric": "Security", "current": 94, "previous": 93, "color": "success", "unit": "%"},
        {"metric": "Accessibility", "current": 91, "previous": 89, "color": "success", "unit": "%"},
        {"metric": "AI Confidence", "current": 94, "previous": 88, "color": "success", "unit": "%"},
        {"metric": "Release Risk", "current": 23, "previous": 31, "color": "success", "unit": ""},
    ],
}

# Release history timeline
RA_RELEASE_HISTORY = [
    {"step": "Build Created", "icon": "🔨", "detail": "Build #1247 triggered on main (a1b2c3d)", "color": "primary", "time": "T+0m"},
    {"step": "Tests Started", "icon": "🧪", "detail": "1,247 tests across 3 browsers", "color": "secondary", "time": "T+5m"},
    {"step": "Tests Completed", "icon": "✅", "detail": "1,162 passed, 47 failed, 38 retries", "color": "success", "time": "T+45m"},
    {"step": "AI Analysis", "icon": "🧠", "detail": "AI analyzed failures, 94% confidence", "color": "info", "time": "T+47m"},
    {"step": "Bugs Detected", "icon": "🐛", "detail": "7 new bugs, 4 regressions filed", "color": "warning", "time": "T+52m"},
    {"step": "Human Review", "icon": "👀", "detail": "3 high-severity reviewed", "color": "accent", "time": "T+60m"},
    {"step": "Quality Gates", "icon": "🚦", "detail": "9/11 gates passed, 2 blocking", "color": "warning", "time": "T+62m"},
    {"step": "Approvals", "icon": "✍️", "detail": "6/8 approvals, 2 pending", "color": "warning", "time": "T+64m"},
    {"step": "Release Candidate", "icon": "🏷️", "detail": "RC-3 promoted", "color": "info", "time": "T+65m"},
    {"step": "AI Decision", "icon": "🤖", "detail": "GO WITH RISKS — 94% confidence", "color": "success", "time": "T+66m"},
]

# Rollback readiness
RA_ROLLBACK = {
    "available": True,
    "status": "ROLLBACK READY",
    "version": "v3.2.0",
    "duration": "4m 32s",
    "db_compatible": True,
    "migration_status": "Reversible",
    "backup_status": "Verified",
    "dependency_compatible": True,
    "confidence": 98,
    "risk": "low",
    "steps": [
        {"step": "Halt new traffic", "duration": "15s", "status": "ready", "color": "success"},
        {"step": "Revert deploy", "duration": "1m 20s", "status": "ready", "color": "success"},
        {"step": "Rollback migration", "duration": "2m 10s", "status": "ready", "color": "success"},
        {"step": "Verify health", "duration": "47s", "status": "ready", "color": "success"},
    ],
}

# Release impact simulation outcomes (mock)
RA_SIMULATIONS = {
    "Release": {
        "business_impact": "LOW", "technical_impact": "MEDIUM", "customer_impact": "LOW",
        "risk": "Medium", "estimated_recovery": "4m 32s", "confidence": 94, "color": "warning",
        "summary": "Proceed with canary rollout. Monitor checkout & payment for 30 min.",
    },
    "Rollback": {
        "business_impact": "LOW", "technical_impact": "LOW", "customer_impact": "LOW",
        "risk": "Low", "estimated_recovery": "4m 32s", "confidence": 98, "color": "success",
        "summary": "Revert to v3.2.0. Migration reversible, backups verified.",
    },
    "Delay Release": {
        "business_impact": "MEDIUM", "technical_impact": "LOW", "customer_impact": "LOW",
        "risk": "Low", "estimated_recovery": "N/A", "confidence": 90, "color": "info",
        "summary": "Hold for Performance Gate fix + Security sign-off. ETA +2 days.",
    },
    "Proceed With Risks": {
        "business_impact": "LOW", "technical_impact": "MEDIUM", "customer_impact": "LOW",
        "risk": "Medium", "estimated_recovery": "4m 32s", "confidence": 94, "color": "warning",
        "summary": "Release with active monitoring + rollback on-call. Accept flaky/perf risk.",
    },
}

# AI recommendations
RA_RECOMMENDATIONS = [
    {"priority": "critical", "finding": "Security Approval missing", "impact": "Release gate", "recommendation": "Complete Security Approval", "expected": "Unblocks release gate", "confidence": 96, "color": "error"},
    {"priority": "high", "finding": "Performance regression", "impact": "User experience", "recommendation": "Investigate payment latency", "expected": "-12% P95 latency", "confidence": 88, "color": "warning"},
    {"priority": "medium", "finding": "Checkout flaky tests", "impact": "Release confidence", "recommendation": "Reduce checkout flaky tests", "expected": "+5% release confidence", "confidence": 94, "color": "warning"},
    {"priority": "medium", "finding": "API coverage gap", "impact": "Critical logic exposed", "recommendation": "Increase API coverage to 80%", "expected": "+15% API coverage", "confidence": 92, "color": "info"},
    {"priority": "low", "finding": "Documentation", "impact": "Onboarding", "recommendation": "Improve release notes", "expected": "Faster rollback decisions", "confidence": 85, "color": "success"},
]

# Quick actions
RA_QUICK_ACTIONS = [
    {"name": "Run Quality Analysis", "icon": "🔬", "description": "Recalculate quality scores", "color": "primary"},
    {"name": "Recalculate Decision", "icon": "🤖", "description": "Re-run AI decision engine", "color": "accent"},
    {"name": "Compare Release", "icon": "⚖️", "description": "Compare current vs previous", "color": "info"},
    {"name": "Analyze Risks", "icon": "⚠️", "description": "Analyze release risks", "color": "warning"},
    {"name": "Analyze Coverage", "icon": "📊", "description": "Analyze coverage gaps", "color": "secondary"},
    {"name": "Review Approvals", "icon": "✍️", "description": "Review approval matrix", "color": "success"},
    {"name": "Generate Report", "icon": "📄", "description": "Generate release report", "color": "primary"},
    {"name": "Open Reports", "icon": "📈", "description": "Open Reports & Analytics", "color": "secondary"},
    {"name": "Knowledge Graph", "icon": "🕸️", "description": "Open Knowledge Graph", "color": "info"},
    {"name": "AI Chat", "icon": "💬", "description": "Open AI Chat Workspace", "color": "accent"},
    {"name": "Open Mission", "icon": "🎯", "description": "Open Mission Planner", "color": "success"},
    {"name": "Open Execution", "icon": "⚡", "description": "Open Live Execution", "color": "warning"},
    {"name": "Human Review", "icon": "🔍", "description": "Open Human Review Center", "color": "primary"},
]

# Bottom workspace tabs
RA_BOTTOM_TABS = ["Overview", "Quality Gates", "Approvals", "Risks", "Coverage", "History", "Rollback"]

# Risk heatmap axes
RA_HEATMAP_IMPACTS = ["Low", "Medium", "High", "Critical"]
RA_HEATMAP_PROBABILITIES = ["Low", "Medium", "High", "Critical"]
