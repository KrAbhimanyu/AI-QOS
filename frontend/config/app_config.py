"""Application configuration for AI-QOS."""
from typing import Final
from dataclasses import dataclass


APP_NAME: Final[str] = "AI-QOS"
APP_VERSION: Final[str] = "1.0.0"
APP_DESCRIPTION: Final[str] = "AI Quality Operating System"

# Page configuration
DEFAULT_PAGE_ICON: Final[str] = "🤖"
PAGE_ICONS: Final[dict[str, str]] = {
    "Dashboard": "📊",
    "Missions": "🎯",
    "Agents": "🤖",
    "Executions": "⚡",
    "Monitoring": "📡",
    "Quality": "✅",
    "Reports": "📈",
    "Settings": "⚙️",
}

# API Configuration
API_TIMEOUT: Final[int] = 30
MAX_RETRIES: Final[int] = 3

# UI Configuration
MAX_DISPLAY_ITEMS: Final[int] = 50
ANIMATION_DURATION: Final[int] = 300
