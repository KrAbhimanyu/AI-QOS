"""Components module for AI-QOS.

This module provides UI components for the AI-QOS frontend.
Use shared components for consistent styling across the application.
"""
# Shared UI Components (use these for consistent design)
from .shared import (
    # Card components
    card,
    metric_card,
    glass_card,
    # Badge components
    badge,
    status_badge,
    priority_badge,
    # Progress components
    progress_bar,
    health_bar,
    confidence_bar,
    # Panel components
    panel,
    glass_panel,
    # Header components
    header,
    section_header,
    # Timeline components
    timeline_item,
    # Button components
    button_primary,
    button_secondary,
    # Icon & label
    icon_label,
    stat_item,
    # Utilities
    divider,
    spacer,
    loading_spinner,
    pulse_dot,
    empty_state,
    notification,
)

__all__ = [
    # Cards
    "card",
    "metric_card",
    "glass_card",
    # Badges
    "badge",
    "status_badge",
    "priority_badge",
    # Progress
    "progress_bar",
    "health_bar",
    "confidence_bar",
    # Panels
    "panel",
    "glass_panel",
    # Headers
    "header",
    "section_header",
    # Timeline
    "timeline_item",
    # Buttons
    "button_primary",
    "button_secondary",
    # Icon & Label
    "icon_label",
    "stat_item",
    # Utilities
    "divider",
    "spacer",
    "loading_spinner",
    "pulse_dot",
    "empty_state",
    "notification",
]
