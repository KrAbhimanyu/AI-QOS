"""Mock data for test reviews and reports."""
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
