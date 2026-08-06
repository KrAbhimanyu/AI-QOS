"""Mock data for application exploration and intelligence."""
MOCK_DISCOVERED_PAGES = [
    {"name": "Home", "url": "/", "forms": 1, "buttons": 8, "tables": 0, "status": "Analyzed", "coverage": "95%"},
    {"name": "Login", "url": "/login", "forms": 2, "buttons": 3, "tables": 0, "status": "Analyzed", "coverage": "100%"},
    {"name": "Dashboard", "url": "/dashboard", "forms": 3, "buttons": 12, "tables": 4, "status": "Analyzed", "coverage": "92%"},
    {"name": "User Profile", "url": "/profile", "forms": 4, "buttons": 6, "tables": 0, "status": "Analyzed", "coverage": "88%"},
    {"name": "Settings", "url": "/settings", "forms": 5, "buttons": 9, "tables": 1, "status": "Analyzed", "coverage": "85%"},
    {"name": "Products", "url": "/products", "forms": 2, "buttons": 5, "tables": 3, "status": "Analyzed", "coverage": "90%"},
    {"name": "Cart", "url": "/cart", "forms": 1, "buttons": 4, "tables": 2, "status": "Analyzed", "coverage": "94%"},
    {"name": "Checkout", "url": "/checkout", "forms": 6, "buttons": 7, "tables": 0, "status": "Analyzed", "coverage": "91%"},
]

MOCK_TECH_STACK = {
    "frontend": {"name": "React", "version": "18.2.0", "confidence": 98},
    "backend": {"name": "Node.js", "version": "20.x", "confidence": 95},
    "database": {"name": "PostgreSQL", "version": "15.0", "confidence": 92},
    "auth": {"name": "OAuth 2.0 + JWT", "version": "", "confidence": 97},
    "hosting": {"name": "AWS", "version": "", "confidence": 88},
    "analytics": {"name": "Mixpanel", "version": "", "confidence": 76},
}

MOCK_AI_THOUGHTS = [
    "Detected Role-Based Authentication system with 3 user roles",
    "Found 27 forms across the application",
    "Identified 4 different dashboard layouts",
    "Discovered 83 API endpoints",
    "Found complex shopping cart workflow",
    "Detected real-time notifications system",
    "Identified 12 different modal dialogs",
    "Found pagination in 6 tables",
]
