"""Mock data for chat."""
from datetime import datetime

MOCK_CONVERSATIONS = [
    {"id": 1, "title": "Login Flow Analysis", "preview": "Analyzing the login authentication...", "time": "2 min ago", "pinned": True},
    {"id": 2, "title": "Dashboard Bug Discussion", "preview": "The sidebar visibility issue...", "time": "15 min ago", "pinned": False},
    {"id": 3, "title": "Test Optimization", "preview": "How can I speed up my tests...", "time": "1 hour ago", "pinned": False},
    {"id": 4, "title": "API Testing Strategy", "preview": "Best practices for API validation...", "time": "2 hours ago", "pinned": False},
    {"id": 5, "title": "Locator Generation", "preview": "Generate stable locators for...", "time": "3 hours ago", "pinned": True},
]

MOCK_MESSAGES = [
    {
        "role": "user",
        "content": "Why is the sidebar test failing?",
        "timestamp": datetime.now(),
    },
    {
        "role": "assistant",
        "content": ("Based on my analysis of the execution logs, the sidebar test is failing because:\n\n"
                   "**Root Cause:**\n"
                   "The sidebar element has `class=\"hidden\"` applied dynamically via JavaScript after page load.\n\n"
                   "**Evidence:**\n"
                   "1. DOM shows: `<nav id=\"sidebar\" class=\"hidden\">`\n"
                   "2. CSS rule: `.hidden { display: none; }`\n"
                   "3. The sidebar is only shown after clicking the hamburger menu\n\n"
                   "**Recommended Fix:**\n"
                   "```python\n"
                   "def test_sidebar_visible(self):\n"
                   "    self.click(\"#hamburger-menu\")\n"
                   "    self.wait_for_selector(\"#sidebar:not(.hidden)\", timeout=5000)\n"
                   "    assert self.is_visible(\"#sidebar\")\n"
                   "```\n\n"
                   "Would you like me to generate the updated test case?"),
        "timestamp": datetime.now(),
    },
    {
        "role": "user",
        "content": "Yes, please generate the updated test case",
        "timestamp": datetime.now(),
    },
    {
        "role": "assistant",
        "content": ("Here's the updated test case:\n\n"
                   "```python\n"
                   "class TestDashboard:\n"
                   "    def setup_method(self):\n"
                   "        self.page = Page()\n"
                   "        self.page.goto(\"https://demo.app/dashboard\")\n"
                   "        self.authenticate()\n\n"
                   "    def test_sidebar_visible(self):\n"
                   "        self.page.click(\"#hamburger-menu\")\n"
                   "        self.page.wait_for_timeout(500)\n"
                   "        sidebar = self.page.locator(\"#sidebar\")\n"
                   "        assert sidebar.is_visible()\n\n"
                   "    def test_navigation_links(self):\n"
                   "        self.page.click(\"#hamburger-menu\")\n"
                   "        self.page.click(\"#sidebar a:has-text('Profile')\")\n"
                   "        self.page.wait_for_url(\"**/profile\")\n"
                   "```\n\n"
                   "**Key Changes:**\n"
                   "1. Added hamburger menu click before checking sidebar\n"
                   "2. Added timeout wait for animation\n"
                   "3. Used more specific locator strategy\n\n"
                   "Should I add this to your test suite?"),
        "timestamp": datetime.now(),
    },
]

MOCK_MISSION_CONTEXT = {
    "mission_name": "E2E Regression Suite v2.1",
    "application": "AIQOS Demo",
    "environment": "Staging",
    "current_test": "Login Flow - Dashboard Access",
    "current_step": "Verify Sidebar Navigation",
    "current_agent": "Frontend Agent",
    "current_browser": "Chrome",
    "execution_status": "Paused at Review",
    "coverage": "94%",
    "pass_rate": "92.3%",
    "current_url": "https://demo.app/dashboard",
}

MOCK_QUICK_ACTIONS = [
    {"icon": "🧪", "name": "Generate Test Case", "description": "Create new test case"},
    {"icon": "📄", "name": "Generate Feature File", "description": "Create Gherkin feature"},
    {"icon": "📦", "name": "Generate Page Object", "description": "Create POM class"},
    {"icon": "❌", "name": "Explain Failure", "description": "Analyze test failure"},
    {"icon": "🎯", "name": "Explain Locator", "description": "Show locator strategy"},
    {"icon": "📐", "name": "Analyze DOM", "description": "Examine DOM structure"},
    {"icon": "🐛", "name": "Generate Bug", "description": "Create bug report"},
    {"icon": "⚡", "name": "Optimize Test", "description": "Improve test performance"},
    {"icon": "🔗", "name": "Create API Test", "description": "Generate API validation"},
    {"icon": "🗄️", "name": "SQL Validation", "description": "Create DB check"},
    {"icon": "📚", "name": "Documentation", "description": "Generate docs"},
    {"icon": "♿", "name": "Accessibility", "description": "A11y analysis"},
]

MOCK_PROMPT_TEMPLATES = [
    {"icon": "🔐", "name": "Generate Login Test", "prompt": "Generate a comprehensive login test case including..."},
    {"icon": "🔁", "name": "Generate Regression", "prompt": "Create a regression test suite for..."},
    {"icon": "💨", "name": "Generate Smoke Test", "prompt": "Create a smoke test covering critical paths..."},
    {"icon": "🐛", "name": "Explain Bug", "prompt": "Explain this bug and suggest fixes..."},
    {"icon": "⚡", "name": "Analyze Performance", "prompt": "Analyze the performance metrics and suggest..."},
    {"icon": "♿", "name": "Accessibility Review", "prompt": "Review for accessibility issues..."},
    {"icon": "🔗", "name": "API Test", "prompt": "Create API test cases for..."},
    {"icon": "📸", "name": "Screenshot Analysis", "prompt": "Analyze this screenshot and suggest..."},
]
