"""Mock data for AI Reports & Analytics Center."""

from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional
import random


class ReportType(str, Enum):
    """Report types."""
    EXECUTIVE_SUMMARY = "Executive Summary"
    TEST_COVERAGE = "Test Coverage"
    QUALITY_METRICS = "Quality Metrics"
    AI_PERFORMANCE = "AI Performance"
    REGRESSION_ANALYSIS = "Regression Analysis"
    FLAKY_TEST_ANALYSIS = "Flaky Test Analysis"
    TREND_ANALYSIS = "Trend Analysis"
    RISK_ASSESSMENT = "Risk Assessment"
    COMPLIANCE_REPORT = "Compliance Report"
    CUSTOM = "Custom Report"


class ReportStatus(str, Enum):
    """Report status."""
    GENERATED = "generated"
    SCHEDULED = "scheduled"
    FAILED = "failed"
    DRAFT = "draft"


class MetricCategory(str, Enum):
    """Metric categories."""
    COVERAGE = "Coverage"
    QUALITY = "Quality"
    PERFORMANCE = "Performance"
    AI = "AI Metrics"
    SECURITY = "Security"
    ACCESSIBILITY = "Accessibility"


# Report Dashboard Info
REPORTS_INFO = {
    "total_reports": 156,
    "generated_today": 12,
    "scheduled_reports": 8,
    "total_metrics": 487,
    "dashboards": 15,
    "last_generated": datetime.now() - timedelta(minutes=15),
    "report_types": 10,
}


# Executive Summary Report
EXECUTIVE_REPORT = {
    "id": "exec_001",
    "title": "Q3 2024 Executive Summary",
    "type": ReportType.EXECUTIVE_SUMMARY,
    "created": datetime.now() - timedelta(days=1),
    "period": "Last 90 days",
    "overall_health": 87,
    "key_metrics": {
        "total_test_cases": 1247,
        "automated_tests": 978,
        "coverage": 78.5,
        "pass_rate": 94.2,
        "flaky_rate": 2.3,
        "avg_execution_time": "45m",
        "defect_leakage": 0.8,
    },
    "trends": {
        "coverage_trend": "+5.2%",
        "pass_rate_trend": "+1.3%",
        "flaky_rate_trend": "-0.5%",
        "execution_time_trend": "-8m",
    },
    "highlights": [
        "Test coverage increased from 73% to 78.5%",
        "Flaky test rate reduced by 22%",
        "Execution time improved by 15%",
        "Zero critical defects in production",
    ],
    "concerns": [
        "API test coverage below target (65%)",
        "3 components with high risk score",
    ],
}


# Test Coverage Report
COVERAGE_REPORT = {
    "id": "coverage_001",
    "title": "Test Coverage Analysis",
    "type": ReportType.TEST_COVERAGE,
    "created": datetime.now() - timedelta(hours=6),
    "overall_coverage": 78.5,
    "by_module": [
        {"name": "Authentication", "coverage": 95, "tests": 45, "critical": True},
        {"name": "Product Catalog", "coverage": 88, "tests": 123, "critical": True},
        {"name": "Shopping Cart", "coverage": 82, "tests": 67, "critical": True},
        {"name": "Checkout Flow", "coverage": 76, "tests": 89, "critical": False},
        {"name": "Payment Processing", "coverage": 71, "tests": 56, "critical": True},
        {"name": "User Profile", "coverage": 65, "tests": 34, "critical": False},
        {"name": "Search", "coverage": 58, "tests": 28, "critical": False},
        {"name": "API Endpoints", "coverage": 45, "tests": 67, "critical": True},
    ],
    "by_type": {
        "unit_tests": {"count": 456, "coverage": 85},
        "integration_tests": {"count": 234, "coverage": 72},
        "e2e_tests": {"count": 123, "coverage": 65},
        "api_tests": {"count": 89, "coverage": 45},
        "visual_tests": {"count": 67, "coverage": 78},
    },
    "gaps": [
        {"module": "API Endpoints", "gap": 55, "priority": "high"},
        {"module": "Search", "gap": 42, "priority": "medium"},
        {"module": "User Profile", "gap": 35, "priority": "medium"},
    ],
}


# Quality Metrics Report
QUALITY_REPORT = {
    "id": "quality_001",
    "title": "Quality Metrics Dashboard",
    "type": ReportType.QUALITY_METRICS,
    "created": datetime.now() - timedelta(hours=3),
    "metrics": {
        "code_quality_score": 87,
        "test_effectiveness": 92,
        "defect_density": 0.8,
        "mean_time_to_detect": "4.2h",
        "mean_time_to_resolve": "18h",
        "escaped_defects": 3,
        "requirements_coverage": 95,
    },
    "by_category": [
        {"category": "Functionality", "score": 94, "trend": "+2%"},
        {"category": "Reliability", "score": 88, "trend": "+5%"},
        {"category": "Usability", "score": 82, "trend": "+1%"},
        {"category": "Performance", "score": 79, "trend": "+8%"},
        {"category": "Security", "score": 91, "trend": "+3%"},
        {"category": "Maintainability", "score": 85, "trend": "+2%"},
    ],
    "defect_distribution": [
        {"severity": "Critical", "count": 0, "trend": "-100%"},
        {"severity": "High", "count": 3, "trend": "-50%"},
        {"severity": "Medium", "count": 12, "trend": "-25%"},
        {"severity": "Low", "count": 28, "trend": "-15%"},
    ],
}


# AI Performance Report
AI_PERFORMANCE_REPORT = {
    "id": "ai_001",
    "title": "AI Agent Performance Analysis",
    "type": ReportType.AI_PERFORMANCE,
    "created": datetime.now() - timedelta(hours=2),
    "agent_stats": {
        "total_agents": 16,
        "active_agents": 12,
        "avg_uptime": "99.2%",
        "avg_response_time": "1.2s",
        "total_tasks_completed": 4587,
        "success_rate": 96.5,
    },
    "by_agent_type": [
        {"type": "Intelligence", "agents": 4, "tasks": 1234, "success": 98},
        {"type": "Testing", "agents": 5, "tasks": 1567, "success": 95},
        {"type": "Documentation", "agents": 2, "tasks": 456, "success": 99},
        {"type": "Security", "agents": 2, "tasks": 234, "success": 97},
        {"type": "Infrastructure", "agents": 3, "tasks": 1096, "success": 94},
    ],
    "model_usage": [
        {"model": "GPT-4", "requests": 3456, "percentage": 45, "avg_latency": "1.5s"},
        {"model": "Claude", "requests": 2345, "percentage": 30, "avg_latency": "1.2s"},
        {"model": "Gemini", "requests": 1234, "percentage": 16, "avg_latency": "0.8s"},
        {"model": "DeepSeek", "requests": 678, "percentage": 9, "avg_latency": "1.0s"},
    ],
    "token_usage": {
        "total": "2.5M",
        "input": "1.8M",
        "output": "0.7M",
        "cost": "$127.50",
    },
}


# Flaky Test Analysis
FLAKY_REPORT = {
    "id": "flaky_001",
    "title": "Flaky Test Analysis",
    "type": ReportType.FLAKY_TEST_ANALYSIS,
    "created": datetime.now() - timedelta(hours=1),
    "summary": {
        "total_flaky": 28,
        "flaky_rate": 2.3,
        "fixed_this_week": 5,
        "pending_fix": 23,
    },
    "by_module": [
        {"module": "Checkout Flow", "flaky_count": 8, "rate": 8.9, "impact": "high"},
        {"module": "Payment Processing", "flaky_count": 5, "rate": 8.9, "impact": "critical"},
        {"module": "Search", "flaky_count": 4, "rate": 14.3, "impact": "medium"},
        {"module": "User Profile", "flaky_count": 3, "rate": 8.8, "impact": "low"},
        {"module": "Product Catalog", "flaky_count": 3, "rate": 2.4, "impact": "medium"},
    ],
    "top_flaky_tests": [
        {"name": "test_checkout_payment_validation", "rate": 15, "fails": 45, "reason": "Race condition"},
        {"name": "test_search_results_ordering", "rate": 12, "fails": 36, "reason": "Async timing"},
        {"name": "test_cart_persistence", "rate": 10, "fails": 30, "reason": "State management"},
        {"name": "test_payment_gateway_timeout", "rate": 9, "fails": 27, "reason": "Network flakiness"},
        {"name": "test_user_session_expiry", "rate": 8, "fails": 24, "reason": "Cache timing"},
    ],
    "root_causes": [
        {"cause": "Async/ Timing Issues", "percentage": 35, "count": 10},
        {"cause": "Network Flakiness", "percentage": 25, "count": 7},
        {"cause": "Test Isolation", "percentage": 20, "count": 6},
        {"cause": "Data Dependencies", "percentage": 15, "count": 4},
        {"cause": "Environment Issues", "percentage": 5, "count": 1},
    ],
}


# Trend Analysis Data
TREND_DATA = {
    "coverage_trend": [
        {"date": "2024-07-01", "value": 68},
        {"date": "2024-07-15", "value": 70},
        {"date": "2024-08-01", "value": 72},
        {"date": "2024-08-15", "value": 74},
        {"date": "2024-09-01", "value": 76},
        {"date": "2024-09-15", "value": 78.5},
    ],
    "pass_rate_trend": [
        {"date": "2024-07-01", "value": 91},
        {"date": "2024-07-15", "value": 92},
        {"date": "2024-08-01", "value": 92.5},
        {"date": "2024-08-15", "value": 93.5},
        {"date": "2024-09-01", "value": 94},
        {"date": "2024-09-15", "value": 94.2},
    ],
    "flaky_rate_trend": [
        {"date": "2024-07-01", "value": 4.2},
        {"date": "2024-07-15", "value": 3.8},
        {"date": "2024-08-01", "value": 3.2},
        {"date": "2024-08-15", "value": 2.8},
        {"date": "2024-09-01", "value": 2.5},
        {"date": "2024-09-15", "value": 2.3},
    ],
    "execution_time_trend": [
        {"date": "2024-07-01", "value": 65},
        {"date": "2024-07-15", "value": 60},
        {"date": "2024-08-01", "value": 55},
        {"date": "2024-08-15", "value": 52},
        {"date": "2024-09-01", "value": 48},
        {"date": "2024-09-15", "value": 45},
    ],
}


# Risk Assessment Report
RISK_REPORT = {
    "id": "risk_001",
    "title": "Risk Assessment Report",
    "type": ReportType.RISK_ASSESSMENT,
    "created": datetime.now() - timedelta(hours=4),
    "overall_risk_score": 23,
    "risk_level": "Medium",
    "high_risk_areas": [
        {
            "area": "Payment Processing",
            "score": 78,
            "factors": ["Low coverage (71%)", "3 flaky tests", "High defect history"],
        },
        {
            "area": "API Endpoints",
            "score": 65,
            "factors": ["Very low coverage (45%)", "Critical business logic"],
        },
    ],
    "medium_risk_areas": [
        {
            "area": "Search Functionality",
            "score": 45,
            "factors": ["Moderate coverage (58%)", "4 flaky tests"],
        },
        {
            "area": "User Profile",
            "score": 38,
            "factors": ["Moderate coverage (65%)", "Data consistency issues"],
        },
    ],
    "mitigation_recommendations": [
        "Increase API test coverage to 80%",
        "Fix all flaky tests in checkout flow",
        "Add performance benchmarks for critical paths",
        "Implement contract testing for microservices",
    ],
}


# Recent Reports List
RECENT_REPORTS = [
    {"id": "r001", "title": "Weekly QA Summary", "type": ReportType.QUALITY_METRICS, "created": datetime.now() - timedelta(hours=2), "status": ReportStatus.GENERATED},
    {"id": "r002", "title": "Test Coverage Analysis", "type": ReportType.TEST_COVERAGE, "created": datetime.now() - timedelta(hours=6), "status": ReportStatus.GENERATED},
    {"id": "r003", "title": "AI Performance Dashboard", "type": ReportType.AI_PERFORMANCE, "created": datetime.now() - timedelta(hours=12), "status": ReportStatus.GENERATED},
    {"id": "r004", "title": "Monthly Executive Summary", "type": ReportType.EXECUTIVE_SUMMARY, "created": datetime.now() - timedelta(days=1), "status": ReportStatus.GENERATED},
    {"id": "r005", "title": "Flaky Test Analysis", "type": ReportType.FLAKY_TEST_ANALYSIS, "created": datetime.now() - timedelta(days=1), "status": ReportStatus.GENERATED},
    {"id": "r006", "title": "Regression Test Report", "type": ReportType.REGRESSION_ANALYSIS, "created": datetime.now() - timedelta(days=2), "status": ReportStatus.GENERATED},
    {"id": "r007", "title": "Security Scan Report", "type": ReportType.COMPLIANCE_REPORT, "created": datetime.now() - timedelta(days=3), "status": ReportStatus.GENERATED},
    {"id": "r008", "title": "Q3 Trend Analysis", "type": ReportType.TREND_ANALYSIS, "created": datetime.now() - timedelta(days=5), "status": ReportStatus.GENERATED},
]


# Scheduled Reports
SCHEDULED_REPORTS = [
    {"id": "s001", "title": "Daily QA Summary", "schedule": "Daily at 8:00 AM", "next_run": datetime.now() + timedelta(hours=12), "recipients": 5},
    {"id": "s002", "title": "Weekly Coverage Report", "schedule": "Every Monday", "next_run": datetime.now() + timedelta(days=3), "recipients": 8},
    {"id": "s003", "title": "Monthly Executive Summary", "schedule": "1st of month", "next_run": datetime.now() + timedelta(days=25), "recipients": 12},
    {"id": "s004", "title": "Flaky Test Alert", "schedule": "Daily at 6:00 PM", "next_run": datetime.now() + timedelta(hours=18), "recipients": 3},
    {"id": "s005", "title": "AI Performance Weekly", "schedule": "Every Monday", "next_run": datetime.now() + timedelta(days=3), "recipients": 4},
]


# Report Templates
REPORT_TEMPLATES = [
    {
        "id": "t001",
        "name": "Executive Dashboard",
        "description": "High-level overview for leadership",
        "sections": ["Overview", "Key Metrics", "Trends", "Recommendations"],
        "default_period": "30 days",
    },
    {
        "id": "t002",
        "name": "QA Weekly Report",
        "description": "Detailed weekly quality analysis",
        "sections": ["Test Results", "Coverage", "Flaky Tests", "Defects", "AI Performance"],
        "default_period": "7 days",
    },
    {
        "id": "t003",
        "name": "Coverage Deep Dive",
        "description": "Detailed coverage analysis by module",
        "sections": ["Overall Coverage", "By Module", "By Type", "Gaps", "Recommendations"],
        "default_period": "14 days",
    },
    {
        "id": "t004",
        "name": "AI Agent Report",
        "description": "AI agent performance and usage",
        "sections": ["Agent Stats", "Model Usage", "Token Usage", "Efficiency"],
        "default_period": "7 days",
    },
    {
        "id": "t005",
        "name": "Risk Assessment",
        "description": "Quality risk analysis and mitigation",
        "sections": ["Risk Score", "High Risk Areas", "Mitigations"],
        "default_period": "30 days",
    },
]


def get_report_by_id(report_id: str) -> Optional[dict[str, Any]]:
    """Get a report by ID."""
    reports_map = {
        "exec_001": EXECUTIVE_REPORT,
        "coverage_001": COVERAGE_REPORT,
        "quality_001": QUALITY_REPORT,
        "ai_001": AI_PERFORMANCE_REPORT,
        "flaky_001": FLAKY_REPORT,
        "risk_001": RISK_REPORT,
    }
    return reports_map.get(report_id)


def get_metric_summary() -> dict[str, Any]:
    """Get summary of all metrics."""
    return {
        "total_tests": 1247,
        "automated": 978,
        "manual": 269,
        "coverage": 78.5,
        "pass_rate": 94.2,
        "flaky_rate": 2.3,
        "execution_time": "45m",
        "ai_agents": 16,
        "active_agents": 12,
        "total_tasks": 4587,
        "success_rate": 96.5,
    }


def generate_trend_chart_data(metric: str, days: int = 30) -> list[dict[str, Any]]:
    """Generate trend data for charts."""
    data = []
    base_value = {
        "coverage": 75,
        "pass_rate": 92,
        "flaky_rate": 3.0,
        "execution_time": 55,
    }.get(metric, 50)
    
    for i in range(days):
        date = datetime.now() - timedelta(days=days-i)
        variation = random.uniform(-2, 2) if metric != "execution_time" else random.uniform(-3, 1)
        value = base_value + (i * 0.1) + variation
        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "value": round(value, 1),
        })
    
    return data
