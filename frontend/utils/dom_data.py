"""Mock data for DOM Intelligence Explorer - AI-Powered DOM Analysis."""

from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional
import random


class ElementType(str, Enum):
    """DOM element types."""
    HTML = "html"
    HEAD = "head"
    BODY = "body"
    HEADER = "header"
    MAIN = "main"
    SECTION = "section"
    DIV = "div"
    FORM = "form"
    INPUT = "input"
    BUTTON = "button"
    TABLE = "table"
    THEAD = "thead"
    TBODY = "tbody"
    TR = "tr"
    TH = "th"
    TD = "td"
    A = "a"
    IMG = "img"
    NAV = "nav"
    UL = "ul"
    LI = "li"
    SPAN = "span"
    P = "p"
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    LABEL = "label"
    SELECT = "select"
    OPTION = "option"
    TEXTAREA = "textarea"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    DIALOG = "dialog"
    MODAL = "modal"
    FOOTER = "footer"
    ASIDE = "aside"
    ARTICLE = "article"
    FIGURE = "figure"
    CANVAS = "canvas"
    SVG = "svg"


class LocatorType(str, Enum):
    """Locator types for automation."""
    ID = "id"
    DATA_TEST_ID = "data-testid"
    ROLE = "role"
    TEXT = "text"
    CSS = "css"
    XPATH = "xpath"
    RELATIVE_XPATH = "relative_xpath"
    LABEL = "label"
    PLACEHOLDER = "placeholder"
    TITLE = "title"
    CLASS = "class"
    NAME = "name"
    TYPE = "type"
    ARIA_LABEL = "aria-label"
    ARIA_ROLE = "aria-role"


class AutomationDifficulty(str, Enum):
    """Automation difficulty levels."""
    EASY = "Easy"
    MODERATE = "Moderate"
    COMPLEX = "Complex"
    VERY_COMPLEX = "Very Complex"


class RiskLevel(str, Enum):
    """Risk levels."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


# DOM Page Information
DOM_PAGE_INFO = {
    "url": "https://shop.staging.example.com/products",
    "page": "Products Page",
    "dom_version": "3.2.1",
    "total_elements": 1247,
    "interactive_elements": 234,
    "forms": 3,
    "buttons": 45,
    "inputs": 67,
    "tables": 2,
    "dialogs": 1,
    "frames": 0,
    "shadow_dom": 2,
    "coverage": 82.5,
    "dom_health": 94,
    "last_scan": datetime.now() - timedelta(minutes=15),
}


# DOM Tree Structure
DOM_TREE = {
    "id": "node_html",
    "tag": "html",
    "type": ElementType.HTML,
    "expanded": True,
    "children": [
        {
            "id": "node_head",
            "tag": "head",
            "type": ElementType.HEAD,
            "expanded": True,
            "children": [
                {"id": "node_title", "tag": "title", "type": ElementType.H1, "text": "Products - E-Commerce"},
                {"id": "node_meta_1", "tag": "meta", "type": ElementType.DIV},
                {"id": "node_link_1", "tag": "link", "type": ElementType.DIV},
                {"id": "node_script_1", "tag": "script", "type": ElementType.DIV},
            ],
        },
        {
            "id": "node_body",
            "tag": "body",
            "type": ElementType.BODY,
            "expanded": True,
            "children": [
                {
                    "id": "node_header",
                    "tag": "header",
                    "type": ElementType.HEADER,
                    "expanded": True,
                    "children": [
                        {"id": "node_nav_1", "tag": "nav", "type": ElementType.NAV, "children": [
                            {"id": "node_logo", "tag": "a", "type": ElementType.A, "attributes": {"href": "/"}, "text": "Logo"},
                            {"id": "node_nav_links", "tag": "ul", "type": ElementType.UL, "children": [
                                {"id": "node_nav_home", "tag": "li", "type": ElementType.LI, "children": [
                                    {"id": "node_nav_home_link", "tag": "a", "type": ElementType.A, "attributes": {"href": "/"}, "text": "Home"}
                                ]},
                                {"id": "node_nav_products", "tag": "li", "type": ElementType.LI, "children": [
                                    {"id": "node_nav_products_link", "tag": "a", "type": ElementType.A, "attributes": {"href": "/products"}, "text": "Products"}
                                ]},
                                {"id": "node_nav_cart", "tag": "li", "type": ElementType.LI, "children": [
                                    {"id": "node_nav_cart_link", "tag": "a", "type": ElementType.A, "attributes": {"href": "/cart", "data-testid": "cart-link"}, "text": "Cart"}
                                ]},
                            ]},
                        ]},
                        {"id": "node_search_form", "tag": "form", "type": ElementType.FORM, "attributes": {"data-testid": "search-form"}, "children": [
                            {"id": "node_search_input", "tag": "input", "type": ElementType.INPUT, "attributes": {"name": "q", "placeholder": "Search products...", "data-testid": "search-input"}, "text": ""},
                            {"id": "node_search_btn", "tag": "button", "type": ElementType.BUTTON, "attributes": {"type": "submit", "data-testid": "search-button"}, "text": "Search"},
                        ]},
                    ],
                },
                {
                    "id": "node_main",
                    "tag": "main",
                    "type": ElementType.MAIN,
                    "expanded": True,
                    "children": [
                        {
                            "id": "node_section_1",
                            "tag": "section",
                            "type": ElementType.SECTION,
                            "attributes": {"data-testid": "products-section"},
                            "expanded": True,
                            "children": [
                                {"id": "node_h1_products", "tag": "h1", "type": ElementType.H1, "text": "Our Products"},
                                {"id": "node_filter_form", "tag": "form", "type": ElementType.FORM, "attributes": {"id": "filter-form"}, "children": [
                                    {"id": "node_category_select", "tag": "select", "type": ElementType.SELECT, "attributes": {"name": "category", "data-testid": "category-select"}, "children": [
                                        {"id": "node_cat_opt_all", "tag": "option", "type": ElementType.OPTION, "text": "All Categories"},
                                        {"id": "node_cat_opt_1", "tag": "option", "type": ElementType.OPTION, "text": "Electronics"},
                                        {"id": "node_cat_opt_2", "tag": "option", "type": ElementType.OPTION, "text": "Clothing"},
                                        {"id": "node_cat_opt_3", "tag": "option", "type": ElementType.OPTION, "text": "Home & Garden"},
                                    ]},
                                    {"id": "node_price_min", "tag": "input", "type": ElementType.INPUT, "attributes": {"type": "number", "name": "min_price", "placeholder": "Min Price", "aria-label": "Minimum Price"}},
                                    {"id": "node_price_max", "tag": "input", "type": ElementType.INPUT, "attributes": {"type": "number", "name": "max_price", "placeholder": "Max Price", "aria-label": "Maximum Price"}},
                                    {"id": "node_apply_filters", "tag": "button", "type": ElementType.BUTTON, "attributes": {"type": "submit", "data-testid": "apply-filters-btn"}, "text": "Apply Filters"},
                                ]},
                            ],
                        },
                        {
                            "id": "node_products_grid",
                            "tag": "div",
                            "type": ElementType.DIV,
                            "attributes": {"class": "products-grid", "data-testid": "products-grid"},
                            "children": [
                                {
                                    "id": "node_product_1",
                                    "tag": "div",
                                    "type": ElementType.DIV,
                                    "attributes": {"class": "product-card", "data-product-id": "123"},
                                    "children": [
                                        {"id": "node_prod1_img", "tag": "img", "type": ElementType.IMG, "attributes": {"src": "/img/product1.jpg", "alt": "Product 1", "data-testid": "product-image-1"}},
                                        {"id": "node_prod1_title", "tag": "h3", "type": ElementType.H3, "text": "Wireless Headphones", "attributes": {"data-testid": "product-title-1"}},
                                        {"id": "node_prod1_price", "tag": "span", "type": ElementType.SPAN, "text": "$99.99", "attributes": {"data-testid": "product-price-1", "class": "price"}},
                                        {"id": "node_prod1_add_btn", "tag": "button", "type": ElementType.BUTTON, "attributes": {"data-testid": "add-to-cart-1", "data-product-id": "123"}, "text": "Add to Cart", "role": "button"},
                                        {"id": "node_prod1_view_btn", "tag": "a", "type": ElementType.A, "attributes": {"href": "/products/123", "data-testid": "view-product-1"}, "text": "View Details"},
                                    ],
                                },
                                {
                                    "id": "node_product_2",
                                    "tag": "div",
                                    "type": ElementType.DIV,
                                    "attributes": {"class": "product-card", "data-product-id": "456"},
                                    "children": [
                                        {"id": "node_prod2_img", "tag": "img", "type": ElementType.IMG, "attributes": {"src": "/img/product2.jpg", "alt": "Product 2", "data-testid": "product-image-2"}},
                                        {"id": "node_prod2_title", "tag": "h3", "type": ElementType.H3, "text": "Smart Watch", "attributes": {"data-testid": "product-title-2"}},
                                        {"id": "node_prod2_price", "tag": "span", "type": ElementType.SPAN, "text": "$199.99", "attributes": {"data-testid": "product-price-2", "class": "price"}},
                                        {"id": "node_prod2_add_btn", "tag": "button", "type": ElementType.BUTTON, "attributes": {"data-testid": "add-to-cart-2", "data-product-id": "456"}, "text": "Add to Cart"},
                                        {"id": "node_prod2_view_btn", "tag": "a", "type": ElementType.A, "attributes": {"href": "/products/456", "data-testid": "view-product-2"}, "text": "View Details"},
                                    ],
                                },
                            ],
                        },
                        {
                            "id": "node_pagination",
                            "tag": "nav",
                            "type": ElementType.NAV,
                            "attributes": {"aria-label": "Pagination", "data-testid": "pagination"},
                            "children": [
                                {"id": "node_page_prev", "tag": "a", "type": ElementType.A, "attributes": {"href": "/products?page=1"}, "text": "Previous"},
                                {"id": "node_page_1", "tag": "a", "type": ElementType.A, "attributes": {"href": "/products?page=1"}, "text": "1"},
                                {"id": "node_page_2", "tag": "a", "type": ElementType.A, "attributes": {"href": "/products?page=2"}, "text": "2"},
                                {"id": "node_page_3", "tag": "a", "type": ElementType.A, "attributes": {"href": "/products?page=3"}, "text": "3"},
                                {"id": "node_page_next", "tag": "a", "type": ElementType.A, "attributes": {"href": "/products?page=2"}, "text": "Next"},
                            ],
                        },
                    ],
                },
                {
                    "id": "node_login_dialog",
                    "tag": "dialog",
                    "type": ElementType.DIALOG,
                    "attributes": {"id": "login-modal", "data-testid": "login-dialog"},
                    "children": [
                        {"id": "node_login_form", "tag": "form", "type": ElementType.FORM, "attributes": {"id": "login-form", "data-testid": "login-form"}},
                        {"id": "node_login_email", "tag": "input", "type": ElementType.INPUT, "attributes": {"type": "email", "name": "email", "id": "login-email", "required": True, "aria-label": "Email Address"}},
                        {"id": "node_login_password", "tag": "input", "type": ElementType.INPUT, "attributes": {"type": "password", "name": "password", "id": "login-password", "required": True, "aria-label": "Password"}},
                        {"id": "node_login_remember", "tag": "input", "type": ElementType.INPUT, "attributes": {"type": "checkbox", "name": "remember", "id": "login-remember"}},
                        {"id": "node_login_remember_label", "tag": "label", "type": ElementType.LABEL, "attributes": {"for": "login-remember"}, "text": "Remember me"},
                        {"id": "node_login_submit", "tag": "button", "type": ElementType.BUTTON, "attributes": {"type": "submit", "data-testid": "login-submit"}, "text": "Sign In"},
                    ],
                },
            ],
        },
    ],
}


def get_element_details(node_id: str) -> dict[str, Any]:
    """Get detailed information about a DOM element."""
    nodes = {
        "node_search_input": {
            "tag": "input",
            "id": "search-input",
            "classes": ["form-control", "search-input"],
            "attributes": {
                "type": "text",
                "name": "q",
                "placeholder": "Search products...",
                "data-testid": "search-input",
                "aria-label": "Search products",
                "autocomplete": "off",
            },
            "text": "",
            "value": "",
            "role": "searchbox",
            "xpath": '//header/nav//form/input[@data-testid="search-input"]',
            "css": "header nav form input[data-testid=\"search-input\"]",
            "playwright": 'page.locator("[data-testid=search-input]")',
            "selenium": 'driver.find_element(By.CSS_SELECTOR, "[data-testid=search-input]")',
        },
        "node_search_btn": {
            "tag": "button",
            "id": "",
            "classes": ["btn", "btn-primary", "search-btn"],
            "attributes": {
                "type": "submit",
                "data-testid": "search-button",
                "aria-label": "Search",
            },
            "text": "Search",
            "value": "",
            "role": "button",
            "xpath": '//button[@data-testid="search-button"]',
            "css": "button[data-testid=\"search-button\"]",
            "playwright": 'page.locator("button[data-testid=search-button]")',
            "selenium": 'driver.find_element(By.CSS_SELECTOR, "button[data-testid=search-button]")',
        },
        "node_category_select": {
            "tag": "select",
            "id": "",
            "classes": ["form-select"],
            "attributes": {
                "name": "category",
                "data-testid": "category-select",
                "aria-label": "Product Category",
            },
            "text": "",
            "value": "",
            "role": "combobox",
            "xpath": '//select[@data-testid="category-select"]',
            "css": "select[data-testid=\"category-select\"]",
            "playwright": 'page.locator("select[data-testid=category-select]")',
            "selenium": 'driver.find_element(By.CSS_SELECTOR, "select[data-testid=category-select]")',
        },
        "node_prod1_add_btn": {
            "tag": "button",
            "id": "",
            "classes": ["btn", "btn-cart", "add-to-cart"],
            "attributes": {
                "data-testid": "add-to-cart-1",
                "data-product-id": "123",
                "aria-label": "Add product to cart",
            },
            "text": "Add to Cart",
            "value": "",
            "role": "button",
            "xpath": '//button[@data-testid="add-to-cart-1"]',
            "css": "button[data-testid=\"add-to-cart-1\"]",
            "playwright": 'page.locator("[data-testid=add-to-cart-1]")',
            "selenium": 'driver.find_element(By.CSS_SELECTOR, "[data-testid=add-to-cart-1]")',
        },
        "node_login_email": {
            "tag": "input",
            "id": "login-email",
            "classes": ["form-control"],
            "attributes": {
                "type": "email",
                "name": "email",
                "required": True,
                "aria-label": "Email Address",
                "autocomplete": "email",
            },
            "text": "",
            "value": "user@example.com",
            "role": "textbox",
            "xpath": '//input[@id="login-email"]',
            "css": "#login-email",
            "playwright": 'page.locator("#login-email")',
            "selenium": 'driver.find_element(By.ID, "login-email")',
        },
        "node_login_password": {
            "tag": "input",
            "id": "login-password",
            "classes": ["form-control"],
            "attributes": {
                "type": "password",
                "name": "password",
                "required": True,
                "aria-label": "Password",
                "autocomplete": "current-password",
            },
            "text": "",
            "value": "********",
            "role": "textbox",
            "xpath": '//input[@id="login-password"]',
            "css": "#login-password",
            "playwright": 'page.locator("#login-password")',
            "selenium": 'driver.find_element(By.ID, "login-password")',
        },
    }
    
    # Generate mock details for any node
    if node_id not in nodes:
        return {
            "tag": "div",
            "id": f"element-{node_id}",
            "classes": ["element"],
            "attributes": {"data-element-id": node_id},
            "text": "",
            "value": "",
            "role": "presentation",
            "xpath": f'//{node_id}',
            "css": f'[data-element-id="{node_id}"]',
            "playwright": f'page.locator("[data-element-id=\"{node_id}\"]")',
            "selenium": f'driver.find_element(By.CSS_SELECTOR, "[data-element-id=\"{node_id}\"]")',
        }
    
    return nodes[node_id]


def generate_locators(element: dict[str, Any]) -> list[dict[str, Any]]:
    """Generate locator options for an element."""
    tag = element.get("tag", "div")
    test_id = element.get("attributes", {}).get("data-testid", "")
    element_id = element.get("id", "")
    classes = element.get("classes", [])
    role = element.get("role", "")
    text = element.get("text", "")[:50] if element.get("text") else ""
    
    locators = []
    
    # Data-testid (highest priority)
    if test_id:
        locators.append({
            "type": "data-testid",
            "locator": f'[data-testid="{test_id}"]',
            "playwright": f'page.locator("[data-testid={test_id}]")',
            "selenium": f'driver.find_element(By.CSS_SELECTOR, "[data-testid={test_id}]")',
            "confidence": 99,
            "reliability": 98,
            "dynamic_risk": "Low",
            "healing_strategy": "Cloud AI maintains testid registry",
        })
    
    # ID
    if element_id:
        locators.append({
            "type": "id",
            "locator": f"#{element_id}",
            "playwright": f'page.locator("#{element_id}")',
            "selenium": f'driver.find_element(By.ID, "{element_id}")',
            "confidence": 97,
            "reliability": 96,
            "dynamic_risk": "Low",
            "healing_strategy": "Static ID maintained by framework",
        })
    
    # Role + text
    if role and text:
        locators.append({
            "type": "role_text",
            "locator": f'role={role}[name="{text}"]',
            "playwright": f'page.get_by_role("{role}", name="{text}")',
            "selenium": f'Not directly supported',
            "confidence": 92,
            "reliability": 88,
            "dynamic_risk": "Medium",
            "healing_strategy": "AI validates role semantics",
        })
    
    # CSS class
    if classes:
        primary_class = classes[0] if classes else ""
        locators.append({
            "type": "css_class",
            "locator": f".{primary_class}",
            "playwright": f'page.locator(".{primary_class}")',
            "selenium": f'driver.find_element(By.CSS_SELECTOR, ".{primary_class}")',
            "confidence": 75,
            "reliability": 65,
            "dynamic_risk": "High",
            "healing_strategy": "AI detects class changes",
        })
    
    # XPath
    locators.append({
        "type": "xpath",
        "locator": f'//{tag}[@data-testid="{test_id}"]' if test_id else f'//{tag}[contains(@class, "{classes[0]}")]' if classes else f'//{tag}',
        "playwright": f'page.locator("xpath=//{tag}[@data-testid=\"{test_id}\"]")' if test_id else f'page.locator("xpath=//{tag}")',
        "selenium": f'driver.find_element(By.XPATH, "//{tag}[@data-testid=\"{test_id}\"]")' if test_id else f'driver.find_element(By.XPATH, "//{tag}")',
        "confidence": 85,
        "reliability": 80,
        "dynamic_risk": "Medium",
        "healing_strategy": "AI suggests stable path",
    })
    
    # Relative XPath (if possible)
    if test_id:
        locators.append({
            "type": "relative_xpath",
            "locator": f'//*[@data-testid="{test_id}"]',
            "playwright": f'page.locator("xpath=//*[@data-testid=\"{test_id}\"]")',
            "selenium": f'driver.find_element(By.XPATH, "//*[@data-testid=\"{test_id}\"]")',
            "confidence": 90,
            "reliability": 85,
            "dynamic_risk": "Medium",
            "healing_strategy": "Flexible path matching",
        })
    
    return sorted(locators, key=lambda x: x["confidence"], reverse=True)


def generate_accessibility_info(element: dict[str, Any]) -> dict[str, Any]:
    """Generate accessibility information for an element."""
    tag = element.get("tag", "")
    attributes = element.get("attributes", {})
    role = element.get("role", "")
    
    # Check for common accessibility issues
    has_aria_label = "aria-label" in attributes or "aria-labelledby" in attributes
    has_id = bool(element.get("id"))
    has_role = bool(role)
    
    issues = []
    score = 100
    
    # Check input labeling
    if tag in ["input", "textarea", "select"]:
        if not (has_aria_label or has_id):
            issues.append({"severity": "high", "issue": "Missing accessible label"})
            score -= 30
    
    # Check button accessible name
    if tag == "button":
        if not (element.get("text") or has_aria_label):
            issues.append({"severity": "medium", "issue": "Button lacks accessible name"})
            score -= 20
    
    # Check image alt
    if tag == "img":
        if not attributes.get("alt"):
            issues.append({"severity": "high", "issue": "Image missing alt text"})
            score -= 25
    
    # Check link text
    if tag == "a":
        if not element.get("text"):
            issues.append({"severity": "medium", "issue": "Link has no text content"})
            score -= 15
    
    # Color contrast would be calculated based on actual colors
    color_contrast_score = 100  # Mock - would need actual colors
    if color_contrast_score < 70:
        issues.append({"severity": "medium", "issue": "Poor color contrast"})
        score -= 15
    
    # Check keyboard accessibility
    is_focusable = tag in ["a", "button", "input", "select", "textarea"] or attributes.get("tabindex")
    if not is_focusable and role in ["button", "link"]:
        issues.append({"severity": "high", "issue": "Not keyboard accessible"})
        score -= 25
    
    return {
        "score": max(0, score),
        "aria_label": attributes.get("aria-label", "Not defined"),
        "aria_role": role or "presentation",
        "keyboard_support": "Full" if is_focusable else "Limited",
        "focus_manageable": is_focusable,
        "issues": issues,
        "suggestions": [
            "Add aria-label for screen readers" if not has_aria_label else "Good: has aria-label",
            "Ensure sufficient color contrast" if score < 80 else "Good: color contrast OK",
            "Make interactive elements keyboard accessible" if not is_focusable else "Good: keyboard accessible",
        ],
    }


def generate_automation_info(element: dict[str, Any]) -> dict[str, Any]:
    """Generate automation intelligence for an element."""
    tag = element.get("tag", "")
    attributes = element.get("attributes", {})
    has_test_id = "data-testid" in attributes
    is_dynamic = attributes.get("data-dynamic") == "true"
    
    # Determine difficulty
    if has_test_id:
        difficulty = AutomationDifficulty.EASY
        difficulty_score = 95
    elif tag in ["button", "a", "input"]:
        difficulty = AutomationDifficulty.MODERATE
        difficulty_score = 75
    else:
        difficulty = AutomationDifficulty.COMPLEX
        difficulty_score = 55
    
    # Flaky risk
    if is_dynamic:
        flaky_risk = "High"
        flaky_score = 40
    elif has_test_id:
        flaky_risk = "Low"
        flaky_score = 95
    else:
        flaky_risk = "Medium"
        flaky_score = 70
    
    # Wait strategy
    wait_strategies = []
    if tag in ["button", "a"]:
        wait_strategies = ["Wait for element to be clickable", "Wait for navigation"]
    elif tag in ["input", "select"]:
        wait_strategies = ["Wait for element to be visible", "Wait for value to be set"]
    else:
        wait_strategies = ["Wait for element to be attached"]
    
    return {
        "difficulty": difficulty,
        "difficulty_score": difficulty_score,
        "locator_stability": "High" if has_test_id else "Medium",
        "flaky_risk": flaky_risk,
        "flaky_score": flaky_score,
        "dynamic_content": is_dynamic,
        "wait_strategy": wait_strategies[0] if wait_strategies else "Wait for element",
        "retry_strategy": "Exponential backoff" if is_dynamic else "Fixed retry",
        "expected_assertions": [
            f"Element {tag} should be visible",
            f"Element {tag} should be enabled",
            f"Element {tag} should have correct text" if element.get("text") else f"Element {tag} should be clickable",
        ],
        "ai_generated_tests": [
            {
                "name": f"Test {tag} interaction",
                "steps": [f"Click {tag}", "Verify behavior"],
                "assertion": f"Element should respond to interaction",
            }
        ],
    }


def generate_dom_metrics() -> dict[str, Any]:
    """Generate DOM metrics."""
    return {
        "total_nodes": 1247,
        "interactive_nodes": 234,
        "hidden_nodes": 156,
        "dynamic_nodes": 89,
        "forms": 3,
        "buttons": 45,
        "inputs": 67,
        "tables": 2,
        "links": 123,
        "images": 45,
        "aria_elements": 89,
        "shadow_dom": 2,
        "iframes": 0,
    }


def generate_ai_discoveries() -> list[dict[str, Any]]:
    """Generate AI-powered DOM discoveries."""
    return [
        {
            "type": "missing_ids",
            "count": 12,
            "severity": "high",
            "description": "Interactive elements without stable IDs",
            "elements": ["search-form", "filter-form", "products-grid"],
        },
        {
            "type": "missing_labels",
            "count": 8,
            "severity": "high",
            "description": "Form inputs without accessible labels",
            "elements": ["price-min-input", "price-max-input"],
        },
        {
            "type": "dynamic_elements",
            "count": 15,
            "severity": "medium",
            "description": "Elements with dynamic IDs or classes",
            "elements": ["product-card-*", "item-*"],
        },
        {
            "type": "poor_locators",
            "count": 23,
            "severity": "medium",
            "description": "Locators that may break easily",
            "elements": ["div:nth-child(2)", ".col-md-4"],
        },
        {
            "type": "accessibility_issues",
            "count": 18,
            "severity": "high",
            "description": "WCAG compliance violations",
            "elements": ["missing-alt", "low-contrast"],
        },
        {
            "type": "shadow_dom",
            "count": 2,
            "severity": "low",
            "description": "Shadow DOM elements detected",
            "elements": ["custom-element-1", "custom-element-2"],
        },
        {
            "type": "flaky_components",
            "count": 7,
            "severity": "medium",
            "description": "Components with flaky behavior",
            "elements": ["autocomplete-dropdown", "lazy-images"],
        },
        {
            "type": "suggestions",
            "count": 45,
            "severity": "info",
            "description": "Improvement suggestions generated",
            "elements": [],
        },
    ]


def generate_discovery_timeline() -> list[dict[str, Any]]:
    """Generate DOM discovery timeline."""
    base_time = datetime.now() - timedelta(hours=2)
    return [
        {"step": 1, "name": "DOM Loaded", "status": "completed", "time": base_time, "details": "Page HTML received"},
        {"step": 2, "name": "Elements Parsed", "status": "completed", "time": base_time + timedelta(seconds=30), "details": "1,247 elements identified"},
        {"step": 3, "name": "Forms Found", "status": "completed", "time": base_time + timedelta(minutes=1), "details": "3 forms detected"},
        {"step": 4, "name": "Buttons Found", "status": "completed", "time": base_time + timedelta(minutes=1, seconds=30), "details": "45 buttons catalogued"},
        {"step": 5, "name": "Accessibility Scan", "status": "completed", "time": base_time + timedelta(minutes=2), "details": "18 issues found"},
        {"step": 6, "name": "Locator Generated", "status": "completed", "time": base_time + timedelta(minutes=3), "details": "156 locators created"},
        {"step": 7, "name": "Automation Ready", "status": "completed", "time": base_time + timedelta(minutes=4), "details": "82.5% automation ready"},
    ]


def generate_relationship_graph(element_id: str) -> list[dict[str, Any]]:
    """Generate element relationship graph."""
    relationships = {
        "node_search_btn": [
            {"target": "Search Form", "relationship": "Submits", "type": "form"},
            {"target": "Search API", "relationship": "Calls", "type": "api"},
            {"target": "Products Grid", "relationship": "Updates", "type": "ui"},
        ],
        "node_prod1_add_btn": [
            {"target": "Add to Cart API", "relationship": "Calls", "type": "api"},
            {"target": "Cart State", "relationship": "Updates", "type": "state"},
            {"target": "Success Toast", "relationship": "Triggers", "type": "ui"},
            {"target": "Product Service", "relationship": "Validates", "type": "service"},
        ],
        "node_login_email": [
            {"target": "Email Validation", "relationship": "Validated by", "type": "validation"},
            {"target": "Login Form", "relationship": "Part of", "type": "form"},
            {"target": "Auth API", "relationship": "Sent to", "type": "api"},
        ],
    }
    return relationships.get(element_id, [])


def generate_console_logs() -> list[dict[str, Any]]:
    """Generate mock console logs."""
    return [
        {"level": "info", "message": "DOM fully loaded", "time": "21:45:32.123"},
        {"level": "info", "message": "Analyzing page structure...", "time": "21:45:32.456"},
        {"level": "warn", "message": "Lazy-loaded image detected: product-3.jpg", "time": "21:45:33.789"},
        {"level": "info", "message": "Found 45 buttons", "time": "21:45:34.012"},
        {"level": "info", "message": "Found 67 input elements", "time": "21:45:34.123"},
        {"level": "info", "message": "Accessibility scan: 18 issues found", "time": "21:45:35.456"},
        {"level": "info", "message": "Generating locators...", "time": "21:45:36.789"},
        {"level": "success", "message": "156 locators generated", "time": "21:45:37.012"},
        {"level": "info", "message": "Automation readiness: 82.5%", "time": "21:45:37.234"},
        {"level": "warn", "message": "2 dynamic elements detected", "time": "21:45:38.567"},
        {"level": "success", "message": "DOM analysis complete", "time": "21:45:39.890"},
    ]


def find_node_by_id(tree: dict[str, Any], node_id: str) -> Optional[dict[str, Any]]:
    """Find a node in the DOM tree by ID."""
    if tree.get("id") == node_id:
        return tree
    for child in tree.get("children", []):
        found = find_node_by_id(child, node_id)
        if found:
            return found
    return None


def flatten_dom_tree(tree: dict[str, Any], result: list[dict[str, Any]] = None) -> list[dict[str, Any]]:
    """Flatten DOM tree into list of nodes."""
    if result is None:
        result = []
    
    result.append({
        "id": tree.get("id"),
        "tag": tree.get("tag"),
        "type": tree.get("type"),
        "text": tree.get("text", "")[:30] if tree.get("text") else "",
        "attributes": tree.get("attributes", {}),
        "expanded": tree.get("expanded", False),
        "has_children": bool(tree.get("children")),
    })
    
    for child in tree.get("children", []):
        flatten_dom_tree(child, result)
    
    return result


def search_elements(query: str) -> list[dict[str, Any]]:
    """Search DOM elements by various criteria."""
    flat_tree = flatten_dom_tree(DOM_TREE)
    query_lower = query.lower()
    
    results = []
    for node in flat_tree:
        tag = node.get("tag", "").lower()
        node_id = node.get("id", "").lower()
        text = node.get("text", "").lower()
        attrs = node.get("attributes", {})
        
        # Search by tag
        if query_lower in tag:
            results.append(node)
            continue
        
        # Search by ID
        if query_lower in node_id:
            results.append(node)
            continue
        
        # Search by text
        if query_lower in text:
            results.append(node)
            continue
        
        # Search by attribute values
        for key, value in attrs.items():
            if query_lower in str(value).lower():
                results.append(node)
                break
    
    return results
