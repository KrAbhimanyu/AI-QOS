"""Mock data for executions and missions."""
from datetime import datetime, timedelta

MOCK_AGENTS = [
    {"name": "Frontend Agent", "icon": "🖥️", "status": "running", "health": 98, "cpu": 45, "memory": 62, "task": "Clicking login button", "progress": 75},
    {"name": "DOM Agent", "icon": "📐", "status": "running", "health": 95, "cpu": 32, "memory": 48, "task": "Finding form elements", "progress": 60},
    {"name": "Locator Agent", "icon": "🎯", "status": "running", "health": 99, "cpu": 28, "memory": 35, "task": "Generating XPath", "progress": 85},
    {"name": "API Agent", "icon": "🔗", "status": "idle", "health": 100, "cpu": 15, "memory": 22, "task": "Waiting", "progress": 0},
    {"name": "Documentation Agent", "icon": "📝", "status": "idle", "health": 100, "cpu": 10, "memory": 18, "task": "Waiting", "progress": 0},
]

MOCK_LOGS = [
    {"time": datetime.now() - timedelta(seconds=5), "agent": "Frontend", "message": "Navigating to login page", "status": "info"},
    {"time": datetime.now() - timedelta(seconds=4), "agent": "Locator", "message": "Found username field with id='username'", "status": "success"},
    {"time": datetime.now() - timedelta(seconds=3), "agent": "Frontend", "message": "Entering credentials", "status": "info"},
    {"time": datetime.now() - timedelta(seconds=2), "agent": "API", "message": "Validating authentication endpoint", "status": "info"},
    {"time": datetime.now() - timedelta(seconds=1), "agent": "Frontend", "message": "Assertion passed: Login successful", "status": "success"},
    {"time": datetime.now(), "agent": "Frontend", "message": "Clicking dashboard link", "status": "info"},
]

MOCK_NETWORK = [
    {"method": "POST", "url": "/api/auth/login", "status": 200, "duration": 234, "size": "1.2 KB"},
    {"method": "GET", "url": "/api/user/profile", "status": 200, "duration": 156, "size": "2.4 KB"},
    {"method": "GET", "url": "/api/dashboard/metrics", "status": 200, "duration": 89, "size": "4.1 KB"},
    {"method": "GET", "url": "/api/dashboard/charts", "status": 200, "duration": 312, "size": "15.8 KB"},
    {"method": "POST", "url": "/api/analytics/event", "status": 201, "duration": 45, "size": "0.3 KB"},
]

MOCK_EXECUTION_STEPS = [
    {"name": "Browser Started", "status": "completed", "duration": "2s", "time": "10:00:00"},
    {"name": "Application Loaded", "status": "completed", "duration": "5s", "time": "10:00:02"},
    {"name": "DOM Ready", "status": "completed", "duration": "3s", "time": "10:00:07"},
    {"name": "Locators Found", "status": "completed", "duration": "8s", "time": "10:00:10"},
    {"name": "Login Executed", "status": "completed", "duration": "12s", "time": "10:00:18"},
    {"name": "Dashboard Loaded", "status": "completed", "duration": "6s", "time": "10:00:30"},
    {"name": "Assertions Running", "status": "active", "duration": "-", "time": "10:00:36"},
    {"name": "Execution Complete", "status": "pending", "duration": "-", "time": "-"},
]
