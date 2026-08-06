"""Utility functions for AI-QOS."""
from datetime import datetime
from typing import Any, Optional


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Format timestamp for display."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%b %d, %Y %H:%M")


def format_duration(seconds: int) -> str:
    """Format duration in human readable format."""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def get_status_color(status: str) -> str:
    """Get color for status badge."""
    colors = {
        "success": "#10B981",
        "completed": "#10B981",
        "running": "#6366F1",
        "active": "#6366F1",
        "pending": "#F59E0B",
        "warning": "#F59E0B",
        "error": "#EF4444",
        "failed": "#EF4444",
        "inactive": "#64748B",
    }
    return colors.get(status.lower(), "#64748B")


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + "..."


def calculate_percentage(part: int, total: int) -> float:
    """Calculate percentage with division by zero handling."""
    if total == 0:
        return 0.0
    return round((part / total) * 100, 1)


def format_large_number(num: int) -> str:
    """Format large numbers with K, M suffixes."""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)
