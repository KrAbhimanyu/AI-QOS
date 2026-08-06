"""Mock data for Application Explorer - Digital Twin of applications."""

from datetime import datetime, timedelta
from enum import Enum
from typing import Any
import random


class Technology(str, Enum):
    """Application technology stack."""
    REACT = "React"
    VUE = "Vue.js"
    ANGULAR = "Angular"
    FLUTTER = "Flutter"
    SWIFT = "Swift"
    KOTLIN = "Kotlin"
    DJANGO = "Django"
    FLASK = "Flask"
    NEXTJS = "Next.js"
    NUXT = "Nuxt.js"


class Environment(str, Enum):
    """Deployment environment."""
    PRODUCTION = "Production"
    STAGING = "Staging"
    DEVELOPMENT = "Development"
    LOCAL = "Local"


class ComponentType(str, Enum):
    """UI Component types."""
    BUTTON = "Button"
    INPUT = "Input"
    TABLE = "Table"
    DROPDOWN = "Dropdown"
    DIALOG = "Dialog"
    CARD = "Card"
    CHART = "Chart"
    MODAL = "Modal"
    NAVIGATION = "Navigation"
    FORM = "Form"
    MENU = "Menu"
    CHECKBOX = "Checkbox"
    RADIO = "Radio"
    TOGGLE = "Toggle"
    DATEPICKER = "DatePicker"
    TABS = "Tabs"


class CoverageLevel(str, Enum):
    """Coverage level."""
    COMPLETE = "Complete"
    PARTIAL = "Partial"
    NONE = "None"


class RiskLevel(str, Enum):
    """Risk level."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


# Application metadata
APPLICATION_INFO = {
    "name": "E-Commerce Platform",
    "version": "3.2.1",
    "environment": Environment.STAGING,
    "url": "https://shop.staging.example.com",
    "technology": Technology.REACT,
    "total_pages": 45,
    "total_components": 312,
    "total_forms": 28,
    "total_apis": 67,
    "coverage": 78.5,
    "risk_score": 23,
    "last_scan": datetime.now() - timedelta(hours=2),
    "discovery_started": datetime.now() - timedelta(days=7),
}


# Page tree structure
APPLICATION_TREE = {
    "id": "app_root",
    "name": "E-Commerce Platform",
    "icon": "🏪",
    "type": "application",
    "coverage": 78.5,
    "confidence": 95,
    "status": "active",
    "children": [
        {
            "id": "module_auth",
            "name": "Authentication",
            "icon": "🔐",
            "type": "module",
            "coverage": 95,
            "confidence": 98,
            "status": "active",
            "children": [
                {"id": "page_login", "name": "Login", "icon": "🔑", "type": "page", "url": "/auth/login", "coverage": 100, "confidence": 99},
                {"id": "page_register", "name": "Register", "icon": "📝", "type": "page", "url": "/auth/register", "coverage": 100, "confidence": 98},
                {"id": "page_forgot", "name": "Forgot Password", "icon": "🔄", "type": "page", "url": "/auth/forgot-password", "coverage": 85, "confidence": 92},
                {"id": "page_reset", "name": "Reset Password", "icon": "🔐", "type": "page", "url": "/auth/reset-password", "coverage": 90, "confidence": 95},
            ],
        },
        {
            "id": "module_catalog",
            "name": "Product Catalog",
            "icon": "📦",
            "type": "module",
            "coverage": 85,
            "confidence": 92,
            "status": "active",
            "children": [
                {"id": "page_home", "name": "Home", "icon": "🏠", "type": "page", "url": "/", "coverage": 95, "confidence": 99},
                {"id": "page_products", "name": "Products", "icon": "📋", "type": "page", "url": "/products", "coverage": 90, "confidence": 96},
                {"id": "page_product_detail", "name": "Product Detail", "icon": "🔍", "type": "page", "url": "/products/:id", "coverage": 88, "confidence": 94},
                {"id": "page_categories", "name": "Categories", "icon": "📂", "type": "page", "url": "/categories", "coverage": 82, "confidence": 90},
                {"id": "page_search", "name": "Search", "icon": "🔎", "type": "page", "url": "/search", "coverage": 75, "confidence": 88},
            ],
        },
        {
            "id": "module_orders",
            "name": "Orders",
            "icon": "🛒",
            "type": "module",
            "coverage": 72,
            "confidence": 88,
            "status": "active",
            "children": [
                {"id": "page_cart", "name": "Shopping Cart", "icon": "🛒", "type": "page", "url": "/cart", "coverage": 80, "confidence": 92},
                {"id": "page_checkout", "name": "Checkout", "icon": "💳", "type": "page", "url": "/checkout", "coverage": 70, "confidence": 85},
                {"id": "page_orders", "name": "My Orders", "icon": "📦", "type": "page", "url": "/orders", "coverage": 65, "confidence": 82},
                {"id": "page_order_detail", "name": "Order Detail", "icon": "📋", "type": "page", "url": "/orders/:id", "coverage": 72, "confidence": 88},
            ],
        },
        {
            "id": "module_account",
            "name": "Account",
            "icon": "👤",
            "type": "module",
            "coverage": 68,
            "confidence": 85,
            "status": "active",
            "children": [
                {"id": "page_profile", "name": "Profile", "icon": "👤", "type": "page", "url": "/account/profile", "coverage": 75, "confidence": 90},
                {"id": "page_addresses", "name": "Addresses", "icon": "📍", "type": "page", "url": "/account/addresses", "coverage": 60, "confidence": 80},
                {"id": "page_wishlist", "name": "Wishlist", "icon": "❤️", "type": "page", "url": "/account/wishlist", "coverage": 70, "confidence": 85},
                {"id": "page_settings", "name": "Settings", "icon": "⚙️", "type": "page", "url": "/account/settings", "coverage": 65, "confidence": 82},
            ],
        },
        {
            "id": "module_payments",
            "name": "Payments",
            "icon": "💳",
            "type": "module",
            "coverage": 58,
            "confidence": 78,
            "status": "partial",
            "children": [
                {"id": "page_payment_methods", "name": "Payment Methods", "icon": "💳", "type": "page", "url": "/payments/methods", "coverage": 55, "confidence": 75},
                {"id": "page_payment_process", "name": "Process Payment", "icon": "⚡", "type": "page", "url": "/payments/process", "coverage": 60, "confidence": 80},
            ],
        },
        {
            "id": "module_reports",
            "name": "Reports",
            "icon": "📊",
            "type": "module",
            "coverage": 45,
            "confidence": 70,
            "status": "partial",
            "children": [
                {"id": "page_sales", "name": "Sales Report", "icon": "📈", "type": "page", "url": "/reports/sales", "coverage": 50, "confidence": 75},
                {"id": "page_analytics", "name": "Analytics", "icon": "📉", "type": "page", "url": "/reports/analytics", "coverage": 40, "confidence": 65},
            ],
        },
    ],
}


def generate_page_detail(page_id: str) -> dict[str, Any]:
    """Generate detailed page information."""
    page_names = {
        "page_login": "Login",
        "page_register": "Register",
        "page_home": "Home",
        "page_products": "Products",
        "page_product_detail": "Product Detail",
        "page_cart": "Shopping Cart",
        "page_checkout": "Checkout",
        "page_orders": "My Orders",
        "page_profile": "Profile",
    }
    
    page = page_names.get(page_id, "Unknown Page")
    
    return {
        "id": page_id,
        "name": page,
        "url": f"/{page.lower().replace(' ', '-')}",
        "framework": Technology.REACT,
        "components": random.randint(8, 25),
        "forms": random.randint(1, 4),
        "buttons": random.randint(5, 20),
        "inputs": random.randint(3, 15),
        "tables": random.randint(0, 3),
        "dropdowns": random.randint(2, 8),
        "dialogs": random.randint(0, 5),
        "cards": random.randint(2, 10),
        "charts": random.randint(0, 5),
        "modals": random.randint(0, 3),
        "navigation": random.randint(3, 12),
        "validation_rules": random.randint(5, 20),
        "business_rules": random.randint(3, 15),
        "accessibility_score": random.uniform(75, 98),
        "performance_score": random.uniform(60, 95),
        "security_score": random.uniform(70, 99),
        "coverage": random.uniform(60, 100),
        "risk": random.choice([RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH]),
        "confidence": random.uniform(80, 99),
        "screenshot": f"https://picsum.photos/seed/{page_id}/800/600",
        "ai_summary": f"The {page} page is a critical component of the e-commerce platform. " + 
                      f"It handles user interactions for {page.lower()} operations and contains " +
                      f"{random.randint(8, 25)} distinct UI components.",
        "why_discovered": "Automatically discovered during sitemap analysis and user flow tracking.",
        "evidence": ["URL pattern matched", "DOM elements detected", "API responses analyzed"],
        "business_importance": random.choice(["Critical", "High", "Medium", "Low"]),
        "automation_complexity": random.choice(["Simple", "Moderate", "Complex"]),
        "testing_priority": random.randint(1, 10),
        "dependencies": ["Authentication Module", "API Gateway", "User Service"],
        "components_detail": _generate_components_detail(),
        "forms_detail": _generate_forms_detail(),
        "business_rules_detail": _generate_business_rules(),
        "accessibility_issues": _generate_accessibility_issues(),
        "performance_issues": _generate_performance_issues(),
        "security_warnings": _generate_security_warnings(),
        "automation_risks": _generate_automation_risks(),
    }


def _generate_components_detail() -> list[dict[str, Any]]:
    """Generate detailed component information."""
    components = []
    component_types = list(ComponentType)
    
    for i in range(random.randint(5, 15)):
        comp_type = random.choice(component_types)
        components.append({
            "id": f"comp_{i+1}",
            "name": f"{comp_type.value}_{i+1}",
            "type": comp_type,
            "test_id": f"testid-{comp_type.value.lower()}-{i+1}" if random.random() > 0.3 else None,
            "coverage": random.uniform(50, 100),
            "confidence": random.uniform(75, 99),
            "is_dynamic": random.random() < 0.2,
            "is_flaky": random.random() < 0.1,
            "automation_ready": random.random() > 0.2,
        })
    
    return components


def _generate_forms_detail() -> list[dict[str, Any]]:
    """Generate form information."""
    forms = []
    
    for i in range(random.randint(1, 4)):
        forms.append({
            "id": f"form_{i+1}",
            "name": f"Form {i+1}",
            "fields": [
                {
                    "name": f"field_{j+1}",
                    "type": random.choice(["text", "email", "password", "number", "select", "checkbox"]),
                    "required": random.random() > 0.3,
                    "validation": random.choice(["email", "phone", "none"]),
                    "has_test_id": random.random() > 0.4,
                }
                for j in range(random.randint(2, 8))
            ],
            "has_captcha": random.random() < 0.3,
            "has_csrf": random.random() > 0.5,
        })
    
    return forms


def _generate_business_rules() -> list[dict[str, Any]]:
    """Generate business rule information."""
    rules = [
        {"id": "rule_1", "name": "User Authentication", "description": "Validates user credentials", "complexity": "Low"},
        {"id": "rule_2", "name": "Session Management", "description": "Handles user session lifecycle", "complexity": "Medium"},
        {"id": "rule_3", "name": "Price Calculation", "description": "Calculates total with taxes and discounts", "complexity": "High"},
        {"id": "rule_4", "name": "Inventory Check", "description": "Verifies product availability", "complexity": "Medium"},
        {"id": "rule_5", "name": "Payment Processing", "description": "Processes payment through gateway", "complexity": "High"},
    ]
    return random.sample(rules, random.randint(2, 5))


def _generate_accessibility_issues() -> list[dict[str, Any]]:
    """Generate accessibility issues."""
    issues = [
        {"severity": "high", "issue": "Missing ARIA labels on form inputs", "element": "Input Field"},
        {"severity": "medium", "issue": "Insufficient color contrast", "element": "Button"},
        {"severity": "low", "issue": "Missing alt text on decorative images", "element": "Image"},
    ]
    return random.sample(issues, random.randint(0, 3))


def _generate_performance_issues() -> list[dict[str, Any]]:
    """Generate performance issues."""
    issues = [
        {"severity": "high", "issue": "Large image assets not optimized", "impact": "2.3s load time"},
        {"severity": "medium", "issue": "Unnecessary re-renders detected", "impact": "15% CPU increase"},
        {"severity": "low", "issue": "Third-party script blocking", "impact": "0.5s delay"},
    ]
    return random.sample(issues, random.randint(0, 2))


def _generate_security_warnings() -> list[dict[str, Any]]:
    """Generate security warnings."""
    warnings = [
        {"severity": "critical", "warning": "Sensitive data in localStorage", "location": "User Service"},
        {"severity": "high", "warning": "Missing CSP headers", "location": "Server Config"},
        {"severity": "medium", "warning": "Insecure cookie settings", "location": "Auth Module"},
    ]
    return random.sample(warnings, random.randint(0, 2))


def _generate_automation_risks() -> list[dict[str, Any]]:
    """Generate automation risks."""
    risks = [
        {"risk": "Dynamic element IDs", "impact": "Locator instability"},
        {"risk": "Conditional rendering", "impact": "Flaky tests"},
        {"risk": "Async data loading", "impact": "Timing issues"},
        {"risk": "Third-party widgets", "impact": "Limited control"},
    ]
    return random.sample(risks, random.randint(1, 4))


def generate_statistics() -> dict[str, Any]:
    """Generate application statistics."""
    return {
        "pages": {"total": 45, "discovered": 42, "covered": 38},
        "components": {"total": 312, "buttons": 89, "inputs": 67, "tables": 23},
        "forms": {"total": 28, "validated": 25, "complex": 8},
        "apis": {"total": 67, "documented": 58, "tested": 45},
        "coverage": {
            "ui_coverage": 78.5,
            "api_coverage": 67.2,
            "overall": 74.8,
        },
        "risk_score": 23,
        "automation_ready": 72.5,
        "database_tables": 34,
    }


def generate_application_map() -> list[dict[str, Any]]:
    """Generate application navigation map."""
    return [
        {"from": "Home", "to": "Products", "type": "navigation"},
        {"from": "Products", "to": "Product Detail", "type": "navigation"},
        {"from": "Product Detail", "to": "Shopping Cart", "type": "action"},
        {"from": "Home", "to": "Shopping Cart", "type": "direct"},
        {"from": "Shopping Cart", "to": "Checkout", "type": "action"},
        {"from": "Checkout", "to": "Order Confirmation", "type": "navigation"},
        {"from": "Home", "to": "Login", "type": "auth"},
        {"from": "Login", "to": "Profile", "type": "auth"},
        {"from": "Profile", "to": "Orders", "type": "navigation"},
        {"from": "Orders", "to": "Order Detail", "type": "navigation"},
    ]


def generate_discovery_timeline() -> list[dict[str, Any]]:
    """Generate discovery timeline."""
    base_time = datetime.now() - timedelta(days=7)
    return [
        {"step": 1, "name": "Discovery Started", "status": "completed", "time": base_time, "details": "Sitemap and crawl initiated"},
        {"step": 2, "name": "Pages Discovered", "status": "completed", "time": base_time + timedelta(hours=1), "details": "45 pages identified"},
        {"step": 3, "name": "Forms Identified", "status": "completed", "time": base_time + timedelta(hours=2), "details": "28 forms catalogued"},
        {"step": 4, "name": "Components Classified", "status": "completed", "time": base_time + timedelta(hours=4), "details": "312 components mapped"},
        {"step": 5, "name": "Business Rules Learned", "status": "completed", "time": base_time + timedelta(hours=6), "details": "87 rules identified"},
        {"step": 6, "name": "API Mapping Complete", "status": "completed", "time": base_time + timedelta(hours=12), "details": "67 endpoints documented"},
        {"step": 7, "name": "Blueprint Generated", "status": "completed", "time": base_time + timedelta(days=1), "details": "Test blueprint created"},
        {"step": 8, "name": "Application Ready", "status": "in_progress", "time": datetime.now(), "details": "Ready for testing"},
    ]


def generate_ai_discoveries() -> list[dict[str, Any]]:
    """Generate AI-powered discoveries."""
    return [
        {"type": "duplicate_ids", "count": 3, "severity": "medium", "description": "Found duplicate element IDs across pages"},
        {"type": "missing_labels", "count": 12, "severity": "low", "description": "Form inputs without labels detected"},
        {"type": "accessibility", "count": 8, "severity": "high", "description": "WCAG compliance issues found"},
        {"type": "performance", "count": 5, "severity": "medium", "description": "Performance bottlenecks identified"},
        {"type": "security", "count": 2, "severity": "critical", "description": "Security vulnerabilities detected"},
        {"type": "automation_risk", "count": 15, "severity": "medium", "description": "Potential flaky locators found"},
        {"type": "missing_test_ids", "count": 45, "severity": "high", "description": "Elements without test identifiers"},
        {"type": "dynamic_elements", "count": 23, "severity": "medium", "description": "Dynamically generated elements detected"},
        {"type": "suggestions", "count": 67, "severity": "info", "description": "Improvement suggestions generated"},
    ]


def generate_quick_actions() -> list[dict[str, Any]]:
    """Generate quick action items."""
    return [
        {"id": "action_1", "name": "Open DOM Explorer", "icon": "🔍", "category": "explorer"},
        {"id": "action_2", "name": "Generate Test Cases", "icon": "🧪", "category": "generation"},
        {"id": "action_3", "name": "Generate Feature File", "icon": "📝", "category": "generation"},
        {"id": "action_4", "name": "Generate Page Object", "icon": "📦", "category": "generation"},
        {"id": "action_5", "name": "Generate API Tests", "icon": "🔗", "category": "generation"},
        {"id": "action_6", "name": "Generate Accessibility Tests", "icon": "♿", "category": "generation"},
        {"id": "action_7", "name": "Generate Performance Tests", "icon": "⚡", "category": "generation"},
        {"id": "action_8", "name": "Generate Documentation", "icon": "📚", "category": "generation"},
        {"id": "action_9", "name": "Explain Page", "icon": "💡", "category": "ai"},
        {"id": "action_10", "name": "Open Browser", "icon": "🌐", "category": "browser"},
        {"id": "action_11", "name": "Open Knowledge Graph", "icon": "🕸️", "category": "explorer"},
        {"id": "action_12", "name": "Run Coverage Analysis", "icon": "📊", "category": "analysis"},
    ]


# Utility functions
from datetime import timedelta


def flatten_tree(tree: dict[str, Any], result: list[dict[str, Any]] = None) -> list[dict[str, Any]]:
    """Flatten application tree into list of pages."""
    if result is None:
        result = []
    
    if tree.get("type") == "page":
        result.append(tree)
    
    for child in tree.get("children", []):
        flatten_tree(child, result)
    
    return result


def get_all_pages() -> list[dict[str, Any]]:
    """Get all pages from application tree."""
    return flatten_tree(APPLICATION_TREE)


def search_pages(query: str) -> list[dict[str, Any]]:
    """Search pages by name or URL."""
    pages = get_all_pages()
    query_lower = query.lower()
    return [
        p for p in pages
        if query_lower in p["name"].lower() or query_lower in p.get("url", "").lower()
    ]
