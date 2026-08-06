"""Mock data for Knowledge Graph & AI Reasoning Center."""

from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional
import random


class NodeType(str, Enum):
    """Knowledge graph node types."""
    MISSION = "mission"
    APPLICATION = "application"
    BUSINESS_DOMAIN = "business_domain"
    BUSINESS_FLOW = "business_flow"
    PAGE = "page"
    COMPONENT = "component"
    DOM_ELEMENT = "dom_element"
    FORM = "form"
    BUTTON = "button"
    INPUT = "input"
    TABLE = "table"
    DIALOG = "dialog"
    LOCATOR = "locator"
    ASSERTION = "assertion"
    API = "api"
    DATABASE_TABLE = "database_table"
    BUSINESS_RULE = "business_rule"
    FEATURE_FILE = "feature_file"
    SCENARIO = "scenario"
    TEST_CASE = "test_case"
    EXECUTION = "execution"
    EVIDENCE = "evidence"
    BUG = "bug"
    REPORT = "report"
    RELEASE = "release"
    USER = "user"
    ROLE = "role"


class RelationshipType(str, Enum):
    """Knowledge graph relationship types."""
    CONTAINS = "contains"
    HAS = "has"
    USES = "uses"
    CALLS = "calls"
    VALIDATES = "validates"
    DEPENDS_ON = "depends_on"
    GENERATES = "generates"
    COVERS = "covers"
    AFFECTS = "affects"
    RELATED_TO = "related_to"
    PARENT_OF = "parent_of"
    IMPLEMENTS = "implements"
    TESTS = "tests"
    BUGS = "bugs"
    RELEASES = "releases"


# Graph Information
GRAPH_INFO = {
    "mission": "E2E Regression v2.1",
    "project": "AI-QOS Enterprise",
    "application": "E-Commerce Platform",
    "version": "3.2.1",
    "graph_version": "2.1.45",
    "graph_status": "healthy",
    "knowledge_version": "2.0",
    "total_nodes": 487,
    "relationships": 1234,
    "business_flows": 15,
    "pages": 45,
    "components": 312,
    "dom_elements": 1247,
    "forms": 23,
    "buttons": 156,
    "inputs": 89,
    "tables": 34,
    "dialogs": 12,
    "locators": 567,
    "assertions": 234,
    "apis": 67,
    "endpoints": 156,
    "database_tables": 34,
    "business_rules": 89,
    "feature_files": 23,
    "scenarios": 89,
    "test_cases": 245,
    "executions": 1234,
    "evidences": 567,
    "bugs": 12,
    "reports": 45,
    "releases": 8,
    "coverage": 78.5,
    "automation_readiness": 82.3,
    "graph_health": 94,
    "confidence": 92,
    "risk": 18,
    "last_update": datetime.now() - timedelta(minutes=5),
}


# Navigator Tree Structure
NAVIGATOR_TREE = {
    "Mission": {
        "icon": "🎯",
        "expanded": True,
        "children": {
            "E2E Regression v2.1": {"icon": "📋", "node_id": "node_mission"},
        }
    },
    "Application": {
        "icon": "🏢",
        "expanded": True,
        "children": {
            "E-Commerce Platform": {"icon": "🛒", "node_id": "node_app"},
        }
    },
    "Business Domains": {
        "icon": "🏛️",
        "expanded": False,
        "children": {
            "Authentication": {"icon": "🔐", "node_id": "node_domain_auth"},
            "Catalog": {"icon": "📦", "node_id": "node_domain_catalog"},
            "Cart": {"icon": "🛒", "node_id": "node_domain_cart"},
            "Checkout": {"icon": "💳", "node_id": "node_domain_checkout"},
            "Orders": {"icon": "📝", "node_id": "node_domain_orders"},
        }
    },
    "Pages": {
        "icon": "📄",
        "expanded": False,
        "count": 45,
    },
    "Components": {
        "icon": "🧩",
        "expanded": False,
        "count": 312,
    },
    "DOM Elements": {
        "icon": "🏗️",
        "expanded": False,
        "count": 1247,
    },
    "Forms": {
        "icon": "📝",
        "expanded": False,
        "count": 23,
    },
    "Buttons": {
        "icon": "🔘",
        "expanded": False,
        "count": 156,
    },
    "Inputs": {
        "icon": "⌨️",
        "expanded": False,
        "count": 89,
    },
    "Tables": {
        "icon": "📊",
        "expanded": False,
        "count": 34,
    },
    "Dialogs": {
        "icon": "💬",
        "expanded": False,
        "count": 12,
    },
    "Locators": {
        "icon": "🎯",
        "expanded": False,
        "count": 567,
    },
    "Assertions": {
        "icon": "✅",
        "expanded": False,
        "count": 234,
    },
    "API Endpoints": {
        "icon": "🔗",
        "expanded": False,
        "count": 156,
    },
    "Database Tables": {
        "icon": "🗄️",
        "expanded": False,
        "count": 34,
    },
    "Business Rules": {
        "icon": "⚖️",
        "expanded": False,
        "count": 89,
    },
    "Feature Files": {
        "icon": "📦",
        "expanded": False,
        "count": 23,
    },
    "Test Cases": {
        "icon": "🧪",
        "expanded": False,
        "count": 245,
    },
    "Executions": {
        "icon": "⚡",
        "expanded": False,
        "count": 1234,
    },
    "Evidences": {
        "icon": "📸",
        "expanded": False,
        "count": 567,
    },
    "Bugs": {
        "icon": "🐛",
        "expanded": False,
        "count": 12,
    },
    "Reports": {
        "icon": "📈",
        "expanded": False,
        "count": 45,
    },
    "Releases": {
        "icon": "🚀",
        "expanded": False,
        "count": 8,
    },
}


# Coverage Map Data
COVERAGE_MAP = {
    "visual_testing": {"coverage": 85, "status": "good"},
    "accessibility": {"coverage": 72, "status": "medium"},
    "api_coverage": {"coverage": 80, "status": "good"},
    "database_coverage": {"coverage": 68, "status": "medium"},
    "performance_coverage": {"coverage": 45, "status": "low"},
    "security_coverage": {"coverage": 78, "status": "good"},
}


# Bug Heatmap Data
BUG_HEATMAP = {
    "by_component": [
        {"name": "Checkout Flow", "failures": 45, "flaky": 12, "risk": "critical"},
        {"name": "Payment Gateway", "failures": 38, "flaky": 8, "risk": "high"},
        {"name": "Search", "failures": 28, "flaky": 15, "risk": "medium"},
        {"name": "User Profile", "failures": 15, "flaky": 5, "risk": "low"},
        {"name": "Product Catalog", "failures": 12, "flaky": 3, "risk": "low"},
    ],
    "by_api": [
        {"name": "POST /checkout", "failures": 34, "risk": "critical"},
        {"name": "GET /products", "failures": 22, "risk": "medium"},
        {"name": "POST /auth/login", "failures": 18, "risk": "medium"},
    ],
    "by_page": [
        {"name": "Checkout", "failures": 45, "risk": "critical"},
        {"name": "Payment", "failures": 38, "risk": "high"},
        {"name": "Search Results", "failures": 28, "risk": "medium"},
    ],
}


# Graph Timeline Data
GRAPH_TIMELINE = [
    {"date": "2024-08-01", "nodes_added": 45, "nodes_removed": 2, "relationships_changed": 123, "version": "2.0.1"},
    {"date": "2024-08-05", "nodes_added": 23, "nodes_removed": 5, "relationships_changed": 67, "version": "2.0.2"},
    {"date": "2024-08-10", "nodes_added": 67, "nodes_removed": 3, "relationships_changed": 189, "version": "2.0.3"},
    {"date": "2024-08-15", "nodes_added": 34, "nodes_removed": 8, "relationships_changed": 98, "version": "2.1.0"},
    {"date": "2024-08-20", "nodes_added": 12, "nodes_removed": 1, "relationships_changed": 45, "version": "2.1.1"},
]


# Graph Analytics
GRAPH_ANALYTICS = {
    "total_nodes": 487,
    "total_relationships": 1234,
    "business_flows": 15,
    "coverage": 78.5,
    "automation_readiness": 82.3,
    "knowledge_completeness": 92.0,
    "confidence": 89,
    "risk": 23,
    "flaky_components": 6,
    "most_connected": {"node": "Authentication API", "connections": 45},
    "least_connected": {"node": "Legacy Report", "connections": 2},
    "critical_path": ["Login", "Dashboard", "Checkout", "Payment", "Confirmation"],
}


# Node execution history
NODE_EXECUTION_HISTORY = [
    {"date": datetime.now() - timedelta(hours=i*2), "status": "passed", "duration": random.randint(5, 30), "agent": "Frontend Agent"} 
    for i in range(10)
]


# Latest changes
LATEST_CHANGES = [
    {"type": "node_added", "item": "Payment Gateway Component", "time": datetime.now() - timedelta(minutes=15)},
    {"type": "relationship_added", "item": "Checkout → Payment API", "time": datetime.now() - timedelta(minutes=30)},
    {"type": "coverage_updated", "item": "Login Form: 95%", "time": datetime.now() - timedelta(hours=1)},
    {"type": "rule_modified", "item": "Discount Calculation Rule", "time": datetime.now() - timedelta(hours=2)},
    {"type": "test_added", "item": "New regression test for checkout", "time": datetime.now() - timedelta(hours=3)},
]


# Knowledge Graph Nodes
KNOWLEDGE_NODES = [
    # Application
    {
        "id": "node_app",
        "type": NodeType.APPLICATION,
        "name": "E-Commerce Platform",
        "description": "Main e-commerce web application",
        "business_purpose": "Enable online product sales and order management",
        "dependencies": [],
        "automation_coverage": 78.5,
        "risk": "low",
        "confidence": 95,
        "priority": "critical",
        "owner": "Platform Team",
        "status": "active",
    },
    # Pages
    {
        "id": "node_home",
        "type": NodeType.PAGE,
        "name": "Home Page",
        "description": "Main landing page with product highlights",
        "business_purpose": "First impression and product discovery",
        "dependencies": ["node_app"],
        "automation_coverage": 95,
        "risk": "low",
        "confidence": 98,
        "priority": "high",
        "owner": "Frontend Team",
        "status": "active",
    },
    {
        "id": "node_products",
        "type": NodeType.PAGE,
        "name": "Products Page",
        "description": "Product catalog with filtering and search",
        "business_purpose": "Enable product browsing and discovery",
        "dependencies": ["node_app", "node_home"],
        "automation_coverage": 88,
        "risk": "medium",
        "confidence": 92,
        "priority": "critical",
        "owner": "Frontend Team",
        "status": "active",
    },
    {
        "id": "node_product_detail",
        "type": NodeType.PAGE,
        "name": "Product Detail",
        "description": "Detailed product view with add to cart",
        "business_purpose": "Drive product purchases",
        "dependencies": ["node_app", "node_products"],
        "automation_coverage": 85,
        "risk": "low",
        "confidence": 94,
        "priority": "critical",
        "owner": "Frontend Team",
        "status": "active",
    },
    {
        "id": "node_cart",
        "type": NodeType.PAGE,
        "name": "Shopping Cart",
        "description": "Cart management and quantity updates",
        "business_purpose": "Manage selected products before checkout",
        "dependencies": ["node_app", "node_product_detail"],
        "automation_coverage": 90,
        "risk": "low",
        "confidence": 96,
        "priority": "critical",
        "owner": "Frontend Team",
        "status": "active",
    },
    {
        "id": "node_checkout",
        "type": NodeType.PAGE,
        "name": "Checkout",
        "description": "Multi-step checkout process",
        "business_purpose": "Complete order placement and payment",
        "dependencies": ["node_app", "node_cart"],
        "automation_coverage": 75,
        "risk": "high",
        "confidence": 85,
        "priority": "critical",
        "owner": "Payments Team",
        "status": "active",
    },
    {
        "id": "node_login",
        "type": NodeType.PAGE,
        "name": "Login",
        "description": "User authentication page",
        "business_purpose": "Enable user identity and personalization",
        "dependencies": ["node_app"],
        "automation_coverage": 100,
        "risk": "low",
        "confidence": 99,
        "priority": "critical",
        "owner": "Auth Team",
        "status": "active",
    },
    {
        "id": "node_profile",
        "type": NodeType.PAGE,
        "name": "User Profile",
        "description": "User account management",
        "business_purpose": "Enable account customization and history",
        "dependencies": ["node_app", "node_login"],
        "automation_coverage": 70,
        "risk": "medium",
        "confidence": 88,
        "priority": "medium",
        "owner": "User Team",
        "status": "active",
    },
    # Components
    {
        "id": "node_header",
        "type": NodeType.COMPONENT,
        "name": "Header Component",
        "description": "Global navigation header",
        "business_purpose": "Provide consistent navigation across app",
        "dependencies": ["node_app"],
        "automation_coverage": 95,
        "risk": "low",
        "confidence": 97,
        "priority": "high",
        "owner": "Frontend Team",
        "status": "active",
    },
    {
        "id": "node_product_card",
        "type": NodeType.COMPONENT,
        "name": "Product Card",
        "description": "Reusable product display card",
        "business_purpose": "Display product information consistently",
        "dependencies": ["node_app"],
        "automation_coverage": 88,
        "risk": "low",
        "confidence": 94,
        "priority": "high",
        "owner": "Frontend Team",
        "status": "active",
    },
    {
        "id": "node_search_bar",
        "type": NodeType.COMPONENT,
        "name": "Search Bar",
        "description": "Product search functionality",
        "business_purpose": "Enable product discovery through search",
        "dependencies": ["node_app", "node_products"],
        "automation_coverage": 82,
        "risk": "medium",
        "confidence": 90,
        "priority": "high",
        "owner": "Search Team",
        "status": "active",
    },
    {
        "id": "node_add_to_cart_btn",
        "type": NodeType.COMPONENT,
        "name": "Add to Cart Button",
        "description": "Button to add products to cart",
        "business_purpose": "Enable product selection for purchase",
        "dependencies": ["node_product_card", "node_cart"],
        "automation_coverage": 95,
        "risk": "low",
        "confidence": 98,
        "priority": "critical",
        "owner": "Frontend Team",
        "status": "active",
    },
    {
        "id": "node_checkout_form",
        "type": NodeType.COMPONENT,
        "name": "Checkout Form",
        "description": "Multi-field checkout form",
        "business_purpose": "Collect customer and payment information",
        "dependencies": ["node_checkout"],
        "automation_coverage": 78,
        "risk": "high",
        "confidence": 88,
        "priority": "critical",
        "owner": "Payments Team",
        "status": "active",
    },
    # APIs
    {
        "id": "node_api_products",
        "type": NodeType.API,
        "name": "Products API",
        "description": "REST API for product catalog",
        "business_purpose": "Serve product data to frontend",
        "dependencies": ["node_app"],
        "automation_coverage": 85,
        "risk": "medium",
        "confidence": 92,
        "priority": "high",
        "owner": "API Team",
        "status": "active",
    },
    {
        "id": "node_api_cart",
        "type": NodeType.API,
        "name": "Cart API",
        "description": "REST API for cart management",
        "business_purpose": "Manage shopping cart operations",
        "dependencies": ["node_app", "node_api_products"],
        "automation_coverage": 80,
        "risk": "medium",
        "confidence": 90,
        "priority": "high",
        "owner": "API Team",
        "status": "active",
    },
    {
        "id": "node_api_checkout",
        "type": NodeType.API,
        "name": "Checkout API",
        "description": "REST API for order processing",
        "business_purpose": "Process orders and payments",
        "dependencies": ["node_app", "node_api_cart"],
        "automation_coverage": 72,
        "risk": "high",
        "confidence": 85,
        "priority": "critical",
        "owner": "Payments Team",
        "status": "active",
    },
    {
        "id": "node_api_auth",
        "type": NodeType.API,
        "name": "Authentication API",
        "description": "REST API for user authentication",
        "business_purpose": "Enable secure user login",
        "dependencies": ["node_app"],
        "automation_coverage": 95,
        "risk": "high",
        "confidence": 98,
        "priority": "critical",
        "owner": "Auth Team",
        "status": "active",
    },
    # Database Tables
    {
        "id": "node_db_products",
        "type": NodeType.DATABASE_TABLE,
        "name": "Products Table",
        "description": "Product catalog storage",
        "business_purpose": "Store product information",
        "dependencies": [],
        "automation_coverage": 70,
        "risk": "low",
        "confidence": 88,
        "priority": "high",
        "owner": "DBA Team",
        "status": "active",
    },
    {
        "id": "node_db_orders",
        "type": NodeType.DATABASE_TABLE,
        "name": "Orders Table",
        "description": "Order and transaction storage",
        "business_purpose": "Store order history and details",
        "dependencies": ["node_db_products"],
        "automation_coverage": 65,
        "risk": "medium",
        "confidence": 85,
        "priority": "critical",
        "owner": "DBA Team",
        "status": "active",
    },
    {
        "id": "node_db_users",
        "type": NodeType.DATABASE_TABLE,
        "name": "Users Table",
        "description": "User account storage",
        "business_purpose": "Store user information",
        "dependencies": [],
        "automation_coverage": 75,
        "risk": "high",
        "confidence": 90,
        "priority": "critical",
        "owner": "DBA Team",
        "status": "active",
    },
    # Business Rules
    {
        "id": "node_rule_cart_limit",
        "type": NodeType.BUSINESS_RULE,
        "name": "Cart Item Limit",
        "description": "Maximum 50 items per cart",
        "business_purpose": "Prevent excessive cart size",
        "dependencies": ["node_cart", "node_api_cart"],
        "automation_coverage": 90,
        "risk": "low",
        "confidence": 95,
        "priority": "medium",
        "owner": "Business Team",
        "status": "active",
    },
    {
        "id": "node_rule_price_calc",
        "type": NodeType.BUSINESS_RULE,
        "name": "Price Calculation",
        "description": "Calculate totals with tax and discounts",
        "business_purpose": "Accurate pricing for customers",
        "dependencies": ["node_checkout", "node_api_checkout"],
        "automation_coverage": 85,
        "risk": "high",
        "confidence": 92,
        "priority": "critical",
        "owner": "Finance Team",
        "status": "active",
    },
    {
        "id": "node_rule_inventory",
        "type": NodeType.BUSINESS_RULE,
        "name": "Inventory Check",
        "description": "Verify product availability before checkout",
        "business_purpose": "Prevent overselling",
        "dependencies": ["node_api_products", "node_api_checkout"],
        "automation_coverage": 80,
        "risk": "high",
        "confidence": 88,
        "priority": "critical",
        "owner": "Operations Team",
        "status": "active",
    },
    {
        "id": "node_rule_auth",
        "type": NodeType.BUSINESS_RULE,
        "name": "Authentication Flow",
        "description": "Standard OAuth2 authentication",
        "business_purpose": "Secure user identity verification",
        "dependencies": ["node_login", "node_api_auth"],
        "automation_coverage": 95,
        "risk": "critical",
        "confidence": 99,
        "priority": "critical",
        "owner": "Security Team",
        "status": "active",
    },
    # Test Cases
    {
        "id": "node_test_login",
        "type": NodeType.TEST_CASE,
        "name": "Login Test",
        "description": "Test user login with valid credentials",
        "business_purpose": "Verify authentication works correctly",
        "dependencies": ["node_login", "node_api_auth"],
        "automation_coverage": 100,
        "risk": "low",
        "confidence": 99,
        "priority": "critical",
        "owner": "QA Team",
        "status": "passing",
    },
    {
        "id": "node_test_add_to_cart",
        "type": NodeType.TEST_CASE,
        "name": "Add to Cart Test",
        "description": "Test adding products to cart",
        "business_purpose": "Verify cart functionality",
        "dependencies": ["node_product_detail", "node_cart", "node_api_cart"],
        "automation_coverage": 95,
        "risk": "low",
        "confidence": 96,
        "priority": "high",
        "owner": "QA Team",
        "status": "passing",
    },
    {
        "id": "node_test_checkout",
        "type": NodeType.TEST_CASE,
        "name": "Checkout Flow Test",
        "description": "Test complete checkout process",
        "business_purpose": "Verify order placement works",
        "dependencies": ["node_checkout", "node_api_checkout", "node_rule_price_calc"],
        "automation_coverage": 78,
        "risk": "high",
        "confidence": 85,
        "priority": "critical",
        "owner": "QA Team",
        "status": "failing",
    },
    {
        "id": "node_test_search",
        "type": NodeType.TEST_CASE,
        "name": "Product Search Test",
        "description": "Test product search functionality",
        "business_purpose": "Verify search works correctly",
        "dependencies": ["node_products", "node_search_bar", "node_api_products"],
        "automation_coverage": 82,
        "risk": "medium",
        "confidence": 88,
        "priority": "medium",
        "owner": "QA Team",
        "status": "passing",
    },
    # Bugs
    {
        "id": "node_bug_price",
        "type": NodeType.BUG,
        "name": "Price Calculation Bug",
        "description": "Discount not applied correctly for bulk orders",
        "business_purpose": "Affects revenue calculation",
        "dependencies": ["node_rule_price_calc", "node_test_checkout"],
        "automation_coverage": 60,
        "risk": "high",
        "confidence": 85,
        "priority": "high",
        "owner": "Dev Team",
        "status": "open",
    },
    {
        "id": "node_bug_cart",
        "type": NodeType.BUG,
        "name": "Cart Persistence Bug",
        "description": "Cart clears on page refresh",
        "business_purpose": "Poor user experience",
        "dependencies": ["node_cart", "node_api_cart"],
        "automation_coverage": 75,
        "risk": "medium",
        "confidence": 90,
        "priority": "medium",
        "owner": "Dev Team",
        "status": "open",
    },
]


# Knowledge Graph Relationships
KNOWLEDGE_RELATIONSHIPS = [
    # Application -> Pages
    {"source": "node_app", "target": "node_home", "type": RelationshipType.CONTAINS, "label": "contains"},
    {"source": "node_app", "target": "node_products", "type": RelationshipType.CONTAINS, "label": "contains"},
    {"source": "node_app", "target": "node_product_detail", "type": RelationshipType.CONTAINS, "label": "contains"},
    {"source": "node_app", "target": "node_cart", "type": RelationshipType.CONTAINS, "label": "contains"},
    {"source": "node_app", "target": "node_checkout", "type": RelationshipType.CONTAINS, "label": "contains"},
    {"source": "node_app", "target": "node_login", "type": RelationshipType.CONTAINS, "label": "contains"},
    {"source": "node_app", "target": "node_profile", "type": RelationshipType.CONTAINS, "label": "contains"},
    
    # Pages -> Components
    {"source": "node_home", "target": "node_header", "type": RelationshipType.HAS, "label": "has"},
    {"source": "node_products", "target": "node_header", "type": RelationshipType.HAS, "label": "has"},
    {"source": "node_products", "target": "node_search_bar", "type": RelationshipType.HAS, "label": "has"},
    {"source": "node_products", "target": "node_product_card", "type": RelationshipType.HAS, "label": "has"},
    {"source": "node_product_detail", "target": "node_product_card", "type": RelationshipType.HAS, "label": "has"},
    {"source": "node_product_detail", "target": "node_add_to_cart_btn", "type": RelationshipType.HAS, "label": "has"},
    {"source": "node_cart", "target": "node_header", "type": RelationshipType.HAS, "label": "has"},
    {"source": "node_checkout", "target": "node_checkout_form", "type": RelationshipType.HAS, "label": "has"},
    
    # Pages -> APIs
    {"source": "node_products", "target": "node_api_products", "type": RelationshipType.USES, "label": "uses"},
    {"source": "node_cart", "target": "node_api_cart", "type": RelationshipType.USES, "label": "uses"},
    {"source": "node_checkout", "target": "node_api_checkout", "type": RelationshipType.USES, "label": "uses"},
    {"source": "node_login", "target": "node_api_auth", "type": RelationshipType.USES, "label": "uses"},
    
    # APIs -> Database
    {"source": "node_api_products", "target": "node_db_products", "type": RelationshipType.CALLS, "label": "calls"},
    {"source": "node_api_cart", "target": "node_db_products", "type": RelationshipType.CALLS, "label": "calls"},
    {"source": "node_api_checkout", "target": "node_db_orders", "type": RelationshipType.CALLS, "label": "calls"},
    {"source": "node_api_auth", "target": "node_db_users", "type": RelationshipType.CALLS, "label": "calls"},
    
    # Pages -> Business Rules
    {"source": "node_cart", "target": "node_rule_cart_limit", "type": RelationshipType.VALIDATES, "label": "validates"},
    {"source": "node_checkout", "target": "node_rule_price_calc", "type": RelationshipType.VALIDATES, "label": "validates"},
    {"source": "node_checkout", "target": "node_rule_inventory", "type": RelationshipType.VALIDATES, "label": "validates"},
    {"source": "node_login", "target": "node_rule_auth", "type": RelationshipType.VALIDATES, "label": "validates"},
    
    # Test Cases -> Pages/Components/APIs
    {"source": "node_test_login", "target": "node_login", "type": RelationshipType.COVERS, "label": "covers"},
    {"source": "node_test_login", "target": "node_api_auth", "type": RelationshipType.COVERS, "label": "covers"},
    {"source": "node_test_add_to_cart", "target": "node_product_detail", "type": RelationshipType.COVERS, "label": "covers"},
    {"source": "node_test_add_to_cart", "target": "node_cart", "type": RelationshipType.COVERS, "label": "covers"},
    {"source": "node_test_add_to_cart", "target": "node_api_cart", "type": RelationshipType.COVERS, "label": "covers"},
    {"source": "node_test_checkout", "target": "node_checkout", "type": RelationshipType.COVERS, "label": "covers"},
    {"source": "node_test_checkout", "target": "node_api_checkout", "type": RelationshipType.COVERS, "label": "covers"},
    {"source": "node_test_search", "target": "node_products", "type": RelationshipType.COVERS, "label": "covers"},
    {"source": "node_test_search", "target": "node_api_products", "type": RelationshipType.COVERS, "label": "covers"},
    
    # Bugs -> Components
    {"source": "node_bug_price", "target": "node_rule_price_calc", "type": RelationshipType.AFFECTS, "label": "affects"},
    {"source": "node_bug_cart", "target": "node_cart", "type": RelationshipType.AFFECTS, "label": "affects"},
    {"source": "node_bug_cart", "target": "node_api_cart", "type": RelationshipType.AFFECTS, "label": "affects"},
    
    # Bugs -> Test Cases
    {"source": "node_bug_price", "target": "node_test_checkout", "type": RelationshipType.AFFECTS, "label": "blocks"},
    {"source": "node_bug_cart", "target": "node_test_add_to_cart", "type": RelationshipType.AFFECTS, "label": "may affect"},
]


# Business Flows
BUSINESS_FLOWS = [
    {
        "id": "flow_login",
        "name": "User Login Flow",
        "steps": ["node_login", "node_api_auth", "node_db_users", "node_profile"],
        "description": "Complete user authentication flow",
        "risk": "high",
        "automation_coverage": 100,
    },
    {
        "id": "flow_purchase",
        "name": "Product Purchase Flow",
        "steps": ["node_home", "node_products", "node_product_detail", "node_add_to_cart_btn", "node_cart", "node_api_cart", "node_checkout", "node_api_checkout", "node_rule_price_calc", "node_rule_inventory"],
        "description": "End-to-end product purchase process",
        "risk": "critical",
        "automation_coverage": 78,
    },
    {
        "id": "flow_search",
        "name": "Product Search Flow",
        "steps": ["node_products", "node_search_bar", "node_api_products", "node_db_products"],
        "description": "Product search and discovery",
        "risk": "low",
        "automation_coverage": 82,
    },
    {
        "id": "flow_checkout",
        "name": "Checkout Flow",
        "steps": ["node_cart", "node_checkout", "node_checkout_form", "node_api_checkout", "node_db_orders", "node_rule_price_calc"],
        "description": "Complete checkout process",
        "risk": "high",
        "automation_coverage": 75,
    },
]


# AI Discoveries
AI_DISCOVERIES = [
    {"type": "duplicate_components", "count": 3, "severity": "low", "description": "Components with similar functionality found"},
    {"type": "dead_pages", "count": 2, "severity": "medium", "description": "Pages with no recent traffic or updates"},
    {"type": "unused_apis", "count": 5, "severity": "low", "description": "APIs not called by any page"},
    {"type": "broken_relationships", "count": 4, "severity": "high", "description": "Orphaned nodes with missing dependencies"},
    {"type": "missing_business_rules", "count": 8, "severity": "medium", "description": "Business rules not yet implemented"},
    {"type": "automation_gaps", "count": 15, "severity": "high", "description": "Test coverage gaps identified"},
    {"type": "accessibility_issues", "count": 23, "severity": "medium", "description": "WCAG compliance issues found"},
    {"type": "security_risks", "count": 7, "severity": "critical", "description": "Potential security vulnerabilities"},
    {"type": "flaky_components", "count": 6, "severity": "medium", "description": "Components with unstable behavior"},
]


# Graph Statistics
GRAPH_STATISTICS = {
    "total_nodes": 487,
    "total_relationships": 1234,
    "coverage": 78.5,
    "automation_readiness": 72.3,
    "business_coverage": 85.0,
    "knowledge_completeness": 92.0,
    "risk_score": 23,
    "confidence_score": 89,
    "by_type": {
        "pages": {"count": 45, "coverage": 82},
        "components": {"count": 312, "coverage": 75},
        "apis": {"count": 67, "coverage": 80},
        "business_rules": {"count": 89, "coverage": 68},
        "test_cases": {"count": 245, "coverage": 78},
    },
}


# AI Recommendations
AI_RECOMMENDATIONS = [
    {"category": "tests", "priority": "high", "recommendation": "Add test cases for price calculation edge cases", "reason": "High risk rule with low coverage"},
    {"category": "tests", "priority": "medium", "recommendation": "Expand checkout flow test coverage", "reason": "Critical business flow with 75% coverage"},
    {"category": "automation", "priority": "high", "recommendation": "Implement locator healing for dynamic elements", "reason": "15 flaky components detected"},
    {"category": "coverage", "priority": "medium", "recommendation": "Add API contract tests for unused endpoints", "reason": "5 unused APIs need verification"},
    {"category": "accessibility", "priority": "medium", "recommendation": "Fix ARIA labels on form inputs", "reason": "23 accessibility issues found"},
    {"category": "security", "priority": "critical", "recommendation": "Review authentication flow for vulnerabilities", "reason": "7 security risks identified"},
]


def get_node_by_id(node_id: str) -> Optional[dict[str, Any]]:
    """Get a node by its ID."""
    for node in KNOWLEDGE_NODES:
        if node["id"] == node_id:
            return node
    return None


def get_connected_nodes(node_id: str) -> list[dict[str, Any]]:
    """Get all nodes connected to the given node."""
    connected_ids = set()
    
    for rel in KNOWLEDGE_RELATIONSHIPS:
        if rel["source"] == node_id:
            connected_ids.add(rel["target"])
        elif rel["target"] == node_id:
            connected_ids.add(rel["source"])
    
    return [get_node_by_id(nid) for nid in connected_ids if get_node_by_id(nid)]


def get_relationships_for_node(node_id: str) -> list[dict[str, Any]]:
    """Get all relationships for a node."""
    return [
        rel for rel in KNOWLEDGE_RELATIONSHIPS
        if rel["source"] == node_id or rel["target"] == node_id
    ]


def get_impact_analysis(node_id: str) -> dict[str, Any]:
    """Get impact analysis for a node."""
    node = get_node_by_id(node_id)
    if not node:
        return {}
    
    # Find affected nodes through relationships
    affected = {
        "pages": [],
        "components": [],
        "apis": [],
        "business_rules": [],
        "test_cases": [],
        "bugs": [],
    }
    
    for rel in KNOWLEDGE_RELATIONSHIPS:
        if rel["source"] == node_id or rel["target"] == node_id:
            other_id = rel["target"] if rel["source"] == node_id else rel["source"]
            other_node = get_node_by_id(other_id)
            if other_node:
                node_type = other_node["type"]
                if "page" in node_type:
                    affected["pages"].append(other_node)
                elif "component" in node_type:
                    affected["components"].append(other_node)
                elif "api" in node_type:
                    affected["apis"].append(other_node)
                elif "rule" in node_type:
                    affected["business_rules"].append(other_node)
                elif "test" in node_type:
                    affected["test_cases"].append(other_node)
                elif "bug" in node_type:
                    affected["bugs"].append(other_node)
    
    return {
        "node": node,
        "affected": affected,
        "total_affected": sum(len(v) for v in affected.values()),
    }


def generate_ai_reasoning(node: dict[str, Any]) -> dict[str, Any]:
    """Generate AI reasoning for a node."""
    return {
        "why_exists": f"This {node['type'].replace('_', ' ')} was discovered during application analysis to support {node['business_purpose']}",
        "business_importance": node.get("priority", "medium").capitalize(),
        "automation_importance": f"{node.get('automation_coverage', 0):.0f}% automated test coverage",
        "risk_assessment": f"{node.get('risk', 'low').capitalize()} risk - {node.get('confidence', 90):.0f}% AI confidence",
        "dependencies": f"{len(node.get('dependencies', []))} direct dependencies identified",
        "recommendation": f"Focus on {'increasing automation coverage' if node.get('automation_coverage', 0) < 80 else 'maintaining current coverage'}",
        "future_impact": "Changes here may affect multiple dependent nodes in the knowledge graph",
    }


def get_business_flow_by_id(flow_id: str) -> Optional[dict[str, Any]]:
    """Get a business flow by ID."""
    for flow in BUSINESS_FLOWS:
        if flow["id"] == flow_id:
            return flow
    return None


def search_nodes(query: str) -> list[dict[str, Any]]:
    """Search nodes by name or description."""
    query_lower = query.lower()
    results = []
    
    for node in KNOWLEDGE_NODES:
        if (query_lower in node["name"].lower() or 
            query_lower in node.get("description", "").lower() or
            query_lower in node.get("business_purpose", "").lower()):
            results.append(node)
    
    return results


def get_nodes_by_type(node_type: NodeType) -> list[dict[str, Any]]:
    """Get all nodes of a specific type."""
    return [n for n in KNOWLEDGE_NODES if n["type"] == node_type]


def get_graph_data_for_visualization() -> dict[str, Any]:
    """Get graph data formatted for visualization."""
    nodes = []
    edges = []
    
    for node in KNOWLEDGE_NODES:
        # Node colors based on type
        type_colors = {
            NodeType.APPLICATION: "#6366f1",
            NodeType.PAGE: "#22d3ee",
            NodeType.COMPONENT: "#10b981",
            NodeType.API: "#f59e0b",
            NodeType.DATABASE_TABLE: "#8b5cf6",
            NodeType.BUSINESS_RULE: "#ec4899",
            NodeType.TEST_CASE: "#14b8a6",
            NodeType.BUG: "#ef4444",
        }
        
        nodes.append({
            "id": node["id"],
            "label": node["name"],
            "type": node["type"].value,
            "color": type_colors.get(node["type"], "#64748b"),
            "size": 20 if node["type"] in [NodeType.APPLICATION, NodeType.PAGE] else 15,
            "data": node,
        })
    
    for rel in KNOWLEDGE_RELATIONSHIPS:
        edges.append({
            "source": rel["source"],
            "target": rel["target"],
            "label": rel["label"],
            "type": rel["type"].value,
        })
    
    return {"nodes": nodes, "edges": edges}
