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

# ----------------------------------------------------------------------------
# Enterprise AI Command Center datasets (non-breaking additions)
# ----------------------------------------------------------------------------

MOCK_HERO_STATS = [
    {"label": "Agent", "value": "Frontend Agent", "icon": "🤖", "color": "primary"},
    {"label": "Model", "value": "AIQOS-Opus 1.4", "icon": "🧠", "color": "accent"},
    {"label": "Conversation", "value": "Login Flow Analysis", "icon": "💬", "color": "info"},
    {"label": "Tokens", "value": "4,812 / 16K", "icon": "🔢", "color": "secondary"},
    {"label": "Memory", "value": "8 entries", "icon": "🗂️", "color": "success"},
    {"label": "Knowledge", "value": "83 nodes", "icon": "📚", "color": "primary"},
    {"label": "Confidence", "value": "94%", "icon": "🎯", "color": "success"},
    {"label": "Status", "value": "Reasoning", "icon": "⚡", "color": "warning"},
]

MOCK_CONTEXT_STRIP = [
    {"label": "Mission", "value": "E2E Regression v2.1", "color": "primary", "live": True},
    {"label": "Page", "value": "/dashboard", "color": "secondary", "live": True},
    {"label": "DOM", "value": "nav#sidebar", "color": "info", "live": False},
    {"label": "URL", "value": "demo.app/dashboard", "color": "muted", "live": False},
    {"label": "Step", "value": "Verify Sidebar", "color": "accent", "live": True},
    {"label": "Agent", "value": "Frontend Agent", "color": "primary", "live": True},
    {"label": "Element", "value": "#hamburger-menu", "color": "success", "live": True},
    {"label": "Coverage", "value": "94%", "color": "success", "live": True},
]

MOCK_AI_THINKING_STAGES = [
    {"stage": "Understanding", "status": "completed", "detail": "Parsed user query about sidebar test failure"},
    {"stage": "Reasoning", "status": "completed", "detail": "Correlated DOM class with execution logs"},
    {"stage": "Searching Memory", "status": "completed", "detail": "Recalled 3 prior sidebar observations"},
    {"stage": "Connecting Knowledge", "status": "active", "detail": "Linking locator strategy to bug evidence"},
    {"stage": "Generating Response", "status": "pending", "detail": "Drafting updated test case"},
    {"stage": "Validating", "status": "pending", "detail": "Awaiting generated fix"},
    {"stage": "Confidence Update", "status": "pending", "detail": "Pending"},
    {"stage": "Recommendation", "status": "pending", "detail": "Pending"},
]

MOCK_AI_CONTEXT = {
    "current_thought": "Sidebar toggles via JS-applied `.hidden` class after page load.",
    "reasoning": "DOM observation matched against execution log; element present but not visible until hamburger interaction.",
    "confidence": 94,
    "evidence": "3 DOM observations + 1 console warning matched",
    "current_tool": "DOM Inspector → Class Mutation Tracker",
    "current_agent": "Frontend Agent",
    "current_model": "AIQOS-Opus 1.4",
    "knowledge_used": "8 pages, 83 endpoints, sidebar locator graph",
    "memory_used": "Prior run #2145, test sidebar_visible",
    "business_context": "Login flow regression gate for v2.1 release",
    "recommendation": "Add wait-for-class-removal before asserting visibility",
}

MOCK_MISSION_PANEL = {
    "mission": "E2E Regression v2.1",
    "application": "AIQOS Demo",
    "execution": "Paused at Review",
    "browser": "Chrome 121",
    "environment": "Staging",
    "coverage": "94%",
    "execution_status": "paused",
    "risk": "Medium",
    "connected_apis": ["POST /api/auth/login", "GET /api/dashboard", "GET /api/sidebar"],
    "database": "postgres://staging (read)",
    "knowledge_graph": "83 nodes / 142 edges",
    "business_flow": "Login → Dashboard → Sidebar Navigation",
}

MOCK_KNOWLEDGE_PANEL = {
    "detected_pages": 8,
    "detected_apis": 83,
    "detected_components": 47,
    "business_rules": 12,
    "dom_nodes": 1284,
    "current_locator": "#sidebar-menu",
    "latest_bug": "Sidebar hidden after load",
    "latest_screenshot": "dashboard_2145.png",
    "latest_report": "v2.1.45",
    "knowledge_confidence": 91,
}

MOCK_BOTTOM_TABS = [
    {"id": "attachments", "label": "Attachments", "icon": "📎"},
    {"id": "mission", "label": "Mission", "icon": "🎯"},
    {"id": "browser", "label": "Browser", "icon": "🌐"},
    {"id": "console", "label": "Console", "icon": "🖥️"},
    {"id": "knowledge", "label": "Knowledge", "icon": "🧠"},
    {"id": "reports", "label": "Reports", "icon": "📊"},
    {"id": "history", "label": "History", "icon": "🕘"},
    {"id": "bookmarks", "label": "Bookmarks", "icon": "🔖"},
    {"id": "memory", "label": "Memory", "icon": "🗂️"},
]

MOCK_CONSOLE_LOGS = [
    {"level": "info", "source": "browser", "message": "Navigated to https://demo.app/dashboard", "time": "10:00:01"},
    {"level": "warning", "source": "dom", "message": "Element nav#sidebar has class 'hidden' applied", "time": "10:00:03"},
    {"level": "info", "source": "agent", "message": "Frontend Agent scanning for toggle trigger", "time": "10:00:04"},
    {"level": "error", "source": "test", "message": "Assertion failed: expected #sidebar visible", "time": "10:00:05"},
    {"level": "info", "source": "ai", "message": "Linked class mutation to hamburger click handler", "time": "10:00:06"},
]

MOCK_BROWSER_FRAME = {
    "url": "https://demo.app/dashboard",
    "title": "Dashboard | AIQOS Demo",
    "highlighted_element": "#hamburger-menu",
    "locator": "#hamburger-menu",
    "role": "button",
    "text": "☰",
    "confidence": 96,
    "action": "inspect",
}

MOCK_SLASH_COMMANDS = [
    {"/new": "Start new conversation"},
    {"/tests": "List test cases"},
    {"/bugs": "Open bugs in mission"},
    {"/dom": "Current DOM structure"},
    {"/network": "Network activity"},
    {"/report": "Generate report"},
    {"/screenshot": "Latest screenshot analysis"},
    {"/locator": "Current locator strategy"},
    {"/execution": "Execution status"},
    {"/history": "Conversation history"},
    {"/help": "Available commands"},
]

MOCK_PROMPT_VARIABLES = [
    {"name": "mission", "value": "E2E Regression v2.1"},
    {"name": "page", "value": "/dashboard"},
    {"name": "element", "value": "#hamburger-menu"},
    {"name": "agent", "value": "Frontend Agent"},
    {"name": "locator", "value": "#sidebar-menu"},
]

MOCK_PROMPT_EDITOR_TOOLS = [
    {"icon": "🔗", "label": "Link", "placeholder": True},
    {"icon": "📎", "label": "Attach", "placeholder": True},
    {"icon": "🖼️", "label": "Image", "placeholder": True},
    {"icon": "🎤", "label": "Voice", "placeholder": True},
    {"icon": "⌨️", "label": "Code", "placeholder": True},
    {"icon": "/", "label": "Commands", "placeholder": True},
]

MOCK_MESSAGE_TYPE_EXAMPLES = [
    {"type": "user", "icon": "👤", "label": "User", "color": "primary"},
    {"type": "assistant", "icon": "🤖", "label": "Assistant", "color": "accent"},
    {"type": "system", "icon": "⚙️", "label": "System", "color": "muted"},
    {"type": "mission", "icon": "🎯", "label": "Mission", "color": "primary"},
    {"type": "warning", "icon": "⚠️", "label": "Warning", "color": "warning"},
    {"type": "tool", "icon": "🔧", "label": "Tool Output", "color": "secondary"},
    {"type": "execution", "icon": "⚡", "label": "Execution", "color": "info"},
    {"type": "knowledge", "icon": "🧠", "label": "Knowledge", "color": "success"},
    {"type": "error", "icon": "❌", "label": "Error", "color": "error"},
]

MOCK_QUICK_ACTIONS_PREMIUM = [
    {"icon": "🧪", "name": "Generate Test", "description": "Create new test case"},
    {"icon": "✨", "name": "Generate Feature", "description": "Create Gherkin feature"},
    {"icon": "📦", "name": "Generate Page Object", "description": "Create POM class"},
    {"icon": "🔗", "name": "Generate API Test", "description": "API validation"},
    {"icon": "🗄️", "name": "Generate SQL", "description": "Create DB check"},
    {"icon": "🐛", "name": "Generate Bug", "description": "Create bug report"},
    {"icon": "❌", "name": "Explain Failure", "description": "Analyze test failure"},
    {"icon": "📐", "name": "Analyze DOM", "description": "Examine DOM structure"},
    {"icon": "📸", "name": "Analyze Screenshot", "description": "Visual analysis"},
    {"icon": "📊", "name": "Generate Report", "description": "Quality report"},
    {"icon": "🕸️", "name": "Open Knowledge Graph", "description": "Graph explorer"},
    {"icon": "🔍", "name": "Open DOM Explorer", "description": "DOM tree"},
    {"icon": "✅", "name": "Open Review", "description": "Human review"},
]
