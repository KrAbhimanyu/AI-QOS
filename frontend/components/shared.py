"""Shared UI Components for AI-QOS Design System.

This module provides reusable UI components that use design tokens
for consistent styling across the application.

Usage:
    from .shared import (
        card, badge, progress_bar, panel, header
    )
"""
import streamlit as st
from typing import Optional, List, Dict, Any, Union

try:
    from ..themes.tokens import (
        COLORS, SPACING, TYPOGRAPHY, BORDERS, SHADOWS, ANIMATIONS,
        get_status_color, get_priority_color, get_health_color, get_confidence_color,
    )
except ImportError:  # pragma: no cover - fallback for direct execution
    from themes.tokens import (
        COLORS, SPACING, TYPOGRAPHY, BORDERS, SHADOWS, ANIMATIONS,
        get_status_color, get_priority_color, get_health_color, get_confidence_color,
    )


# =============================================================================
# CARD COMPONENTS
# =============================================================================

def card(
    title: str,
    content: str = "",
    icon: str = "",
    badge: str = None,
    badge_type: str = "info",
    footer: str = "",
    key: str = None,
) -> None:
    """Render a styled card component.
    
    Args:
        title: Card title
        content: Card body content
        icon: Optional icon emoji
        badge: Optional badge text
        badge_type: Badge type (success, warning, error, info)
        footer: Optional footer content
        key: Optional Streamlit key
    """
    # Build badge HTML
    badge_html = ""
    if badge:
        badge_html = f'''<span style="
            display: inline-flex;
            align-items: center;
            padding: {SPACING.SPACE_1} {SPACING.SPACE_3};
            border-radius: {BORDERS.RADIUS_FULL};
            font-size: {TYPOGRAPHY.FONT_SIZE_SM};
            font-weight: 500;
        ">{badge}</span>'''
    
    # Build icon HTML
    icon_html = f'<span style="font-size: 1.5rem;">{icon}</span>' if icon else ""
    
    # Build content HTML
    content_html = f'<p style="color: {COLORS.TEXT_SECONDARY}; margin: 0 0 {SPACING.SPACE_4};">{content}</p>' if content else ""
    
    # Build footer HTML
    footer_html = f'<div style="border-top: 1px solid {COLORS.BORDER}; padding-top: {SPACING.SPACE_4}; margin-top: {SPACING.SPACE_4};">{footer}</div>' if footer else ""
    
    st.markdown(f"""
    <div style="
        background: {COLORS.GLASS};
        border: {BORDERS.WIDTH_THIN} solid {COLORS.BORDER};
        border-radius: {BORDERS.RADIUS_LG};
        padding: {SPACING.SPACE_6};
        margin-bottom: {SPACING.SPACE_4};
    ">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: {SPACING.SPACE_3};">
            <div style="display: flex; align-items: center; gap: {SPACING.SPACE_3};">
                {icon_html}
                <h3 style="color: {COLORS.TEXT_PRIMARY}; margin: 0; font-size: {TYPOGRAPHY.FONT_SIZE_LG}; font-weight: 600;">
                    {title}
                </h3>
            </div>
            {badge_html}
        </div>
        {content_html}
        {footer_html}
    </div>
    """, unsafe_allow_html=True)


def metric_card(
    title: str,
    value: Union[str, int, float],
    subtitle: str = "",
    trend: str = "",
    icon: str = "",
    delta: str = None,
) -> None:
    """Render a metric card component.
    
    Args:
        title: Metric title
        value: Metric value
        subtitle: Optional subtitle
        trend: Trend indicator (e.g., "+5%", "-10%")
        icon: Optional icon
        delta: Optional Streamlit delta value
    """
    trend_color = COLORS.SUCCESS if trend.startswith("+") else COLORS.ERROR if trend.startswith("-") else COLORS.TEXT_MUTED
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {COLORS.SURFACE} 0%, rgba({COLORS.PRIMARY_RGB}, 0.1) 100%);
        border: {BORDERS.WIDTH_THIN} solid {COLORS.BORDER};
        border-radius: {BORDERS.RADIUS_LG};
        padding: {SPACING.SPACE_6};
        text-align: center;
        margin-bottom: {SPACING.SPACE_4};
    ">
        <div style="font-size: 11px; color: {COLORS.TEXT_MUTED}; text-transform: uppercase; letter-spacing: 1px; margin-bottom: {SPACING.SPACE_2};">
            {title}
        </div>
        <div style="display: flex; align-items: center; justify-content: center; gap: {SPACING.SPACE_3};">
            <div style="font-size: 2rem; font-weight: 700; color: {COLORS.TEXT_PRIMARY}; font-family: {TYPOGRAPHY.FONT_MONO};">
                {value}
            </div>
            {f'<span style="font-size: 1.5rem;">{icon}</span>' if icon else ''}
        </div>
        {f'<div style="font-size: {TYPOGRAPHY.FONT_SIZE_SM}; color: {COLORS.TEXT_SECONDARY}; margin-top: {SPACING.SPACE_2};">{subtitle}</div>' if subtitle else ''}
        {f'<div style="font-size: {TYPOGRAPHY.FONT_SIZE_SM}; font-weight: 600; color: {trend_color}; margin-top: {SPACING.SPACE_2};">{trend}</div>' if trend else ''}
    </div>
    """, unsafe_allow_html=True)


def glass_card(
    content: str = "",
    children: str = "",
    padding: str = SPACING.SPACE_6,
) -> None:
    """Render a glassmorphism card component.
    
    Args:
        content: HTML content for the card
        children: Alternative content parameter
        padding: Card padding
    """
    card_content = content or children
    st.markdown(f"""
    <div style="
        background: {COLORS.GLASS};
        border: {BORDERS.WIDTH_THIN} solid {COLORS.GLASS_BORDER};
        border-radius: {BORDERS.RADIUS_LG};
        padding: {padding};
        backdrop-filter: blur(12px);
        margin-bottom: {SPACING.SPACE_4};
    ">
        {card_content}
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# BADGE COMPONENTS
# =============================================================================

def badge(
    text: str,
    badge_type: str = "info",
    icon: str = "",
) -> None:
    """Render a badge component.
    
    Args:
        text: Badge text
        badge_type: Type (success, warning, error, info)
        icon: Optional icon
    """
    colors = {
        "success": (COLORS.SUCCESS, COLORS.SUCCESS_RGB),
        "warning": (COLORS.WARNING, COLORS.WARNING_RGB),
        "error": (COLORS.ERROR, COLORS.ERROR_RGB),
        "info": (COLORS.PRIMARY, COLORS.PRIMARY_RGB),
    }
    
    color, rgb = colors.get(badge_type, colors["info"])
    
    st.markdown(f"""
    <span style="
        display: inline-flex;
        align-items: center;
        gap: {SPACING.SPACE_1};
        padding: {SPACING.SPACE_1} {SPACING.SPACE_3};
        background: rgba({rgb}, 0.2);
        color: {color};
        border-radius: {BORDERS.RADIUS_FULL};
        font-size: {TYPOGRAPHY.FONT_SIZE_SM};
        font-weight: 500;
    ">
        {f'{icon} ' if icon else ''}{text}
    </span>
    """, unsafe_allow_html=True)


def status_badge(
    status: str,
    show_dot: bool = True,
) -> None:
    """Render a status badge based on status value.
    
    Args:
        status: Status string (running, completed, failed, etc.)
        show_dot: Whether to show status dot
    """
    color = get_status_color(status)
    status_display = status.replace("_", " ").title()
    
    # Build dot HTML
    dot_html = ""
    if show_dot:
        dot_html = f'''<span style="
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: {color};
            animation: pulse 2s infinite;
        "></span>'''
    
    st.markdown(f"""
    <span style="
        display: inline-flex;
        align-items: center;
        gap: {SPACING.SPACE_2};
        padding: {SPACING.SPACE_1} {SPACING.SPACE_3};
        background: rgba({color.lstrip('#')}, 0.2);
        color: {color};
        border-radius: {BORDERS.RADIUS_FULL};
        font-size: {TYPOGRAPHY.FONT_SIZE_SM};
        font-weight: 500;
    ">
        {dot_html}
        {status_display}
    </span>
    """, unsafe_allow_html=True)


def priority_badge(priority: str) -> None:
    """Render a priority badge.
    
    Args:
        priority: Priority level (critical, high, medium, low)
    """
    color = get_priority_color(priority)
    priority_display = priority.replace("_", " ").title()
    
    st.markdown(f"""
    <span style="
        display: inline-flex;
        align-items: center;
        padding: {SPACING.SPACE_1} {SPACING.SPACE_3};
        background: rgba({color.lstrip('#')}, 0.2);
        color: {color};
        border-radius: {BORDERS.RADIUS_FULL};
        font-size: {TYPOGRAPHY.FONT_SIZE_SM};
        font-weight: 500;
    ">
        {priority_display}
    </span>
    """, unsafe_allow_html=True)


# =============================================================================
# PROGRESS COMPONENTS
# =============================================================================

def progress_bar(
    value: float,
    max_value: float = 100,
    color: str = None,
    height: str = "6px",
    show_label: bool = True,
) -> None:
    """Render a progress bar component.
    
    Args:
        value: Current progress value
        max_value: Maximum value
        color: Optional custom color
        height: Progress bar height
        show_label: Whether to show percentage label
    """
    percentage = min(100, (value / max_value) * 100) if max_value else 0
    progress_color = color or COLORS.PRIMARY
    
    # Build label HTML
    label_html = ""
    if show_label:
        font_size = TYPOGRAPHY.FONT_SIZE_SM
        label_html = f'<div style="display: flex; justify-content: space-between; margin-bottom: {SPACING.SPACE_1};">' \
            f'<span style="font-size: {font_size}; color: {COLORS.TEXT_SECONDARY};"></span>' \
            f'<span style="font-size: {font_size}; color: {COLORS.TEXT_PRIMARY}; font-weight: 500;">{percentage:.0f}%</span>' \
            f'</div>'
    
    st.markdown(f"""
    <div style="margin-bottom: {SPACING.SPACE_2};">
        {label_html}
        <div style="
            height: {height};
            background: {COLORS.BORDER};
            border-radius: {BORDERS.RADIUS_FULL};
            overflow: hidden;
        ">
            <div style="
                width: {percentage}%;
                height: 100%;
                background: linear-gradient(90deg, {progress_color}, {progress_color}cc);
                border-radius: {BORDERS.RADIUS_FULL};
                transition: width {ANIMATIONS.DURATION_SLOWER} ease;
            "></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def health_bar(health: float, label: str = "Health") -> None:
    """Render a health bar with automatic color based on value.
    
    Args:
        health: Health percentage (0-100)
        label: Label text
    """
    color = get_health_color(health)
    progress_bar(health, 100, color, "8px")


def confidence_bar(confidence: int, label: str = "Confidence") -> None:
    """Render a confidence bar with automatic color based on value.
    
    Args:
        confidence: Confidence percentage (0-100)
        label: Label text
    """
    color = get_confidence_color(confidence)
    progress_bar(confidence, 100, color, "8px")


# =============================================================================
# PANEL COMPONENTS
# =============================================================================

def panel(
    title: str = "",
    content: str = "",
    icon: str = "",
    collapsible: bool = False,
    expanded: bool = True,
) -> None:
    """Render a panel component.
    
    Args:
        title: Panel title
        content: Panel content
        icon: Optional icon
        collapsible: Whether panel can collapse
        expanded: Initial expansion state
    """
    with st.expander(f"{icon} {title}" if icon else title, expanded=collapsible and not expanded):
        st.markdown(content)


def glass_panel(
    title: str = "",
    content: str = "",
    icon: str = "",
) -> None:
    """Render a glassmorphism panel.
    
    Args:
        title: Panel title
        content: Panel content
        icon: Optional icon
    """
    title_html = ""
    if title:
        icon_span = f"<span>{icon}</span>" if icon else ""
        title_html = f'<h4 style="color: {COLORS.TEXT_PRIMARY}; margin: 0 0 {SPACING.SPACE_4}; display: flex; align-items: center; gap: {SPACING.SPACE_2};">{icon_span}{title}</h4>'
    
    st.markdown(f"""
    <div style="
        background: {COLORS.GLASS_LIGHT};
        border: {BORDERS.WIDTH_THIN} solid {COLORS.GLASS_BORDER};
        border-radius: {BORDERS.RADIUS_LG};
        padding: {SPACING.SPACE_6};
        backdrop-filter: blur(12px);
        margin-bottom: {SPACING.SPACE_4};
    ">
        {title_html}
        {content}
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# HEADER COMPONENTS
# =============================================================================

def header(
    title: str,
    subtitle: str = "",
    icon: str = "",
) -> None:
    """Render a page header.
    
    Args:
        title: Header title
        subtitle: Optional subtitle
        icon: Optional icon
    """
    st.markdown(f"""
    <div style="margin-bottom: {SPACING.SPACE_6};">
        <div style="display: flex; align-items: center; gap: {SPACING.SPACE_3}; margin-bottom: {SPACING.SPACE_2};">
            {f'<span style="font-size: 2rem;">{icon}</span>' if icon else ''}
            <h1 style="
                font-size: {TYPOGRAPHY.FONT_SIZE_2XL};
                font-weight: 600;
                color: {COLORS.TEXT_PRIMARY};
                margin: 0;
            ">
                {title}
            </h1>
        </div>
        {f'<p style="color: {COLORS.TEXT_SECONDARY}; font-size: {TYPOGRAPHY.FONT_SIZE_BASE}; margin: 0;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def section_header(
    title: str,
    icon: str = "",
    action: str = "",
) -> None:
    """Render a section header with optional action.
    
    Args:
        title: Section title
        icon: Optional icon
        action: Optional action HTML
    """
    st.markdown(f"""
    <div style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: {SPACING.SPACE_4};
        padding-bottom: {SPACING.SPACE_3};
        border-bottom: 1px solid {COLORS.BORDER};
    ">
        <h3 style="
            color: {COLORS.TEXT_PRIMARY};
            font-size: {TYPOGRAPHY.FONT_SIZE_LG};
            font-weight: 600;
            margin: 0;
            display: flex;
            align-items: center;
            gap: {SPACING.SPACE_2};
        ">
            {f'<span>{icon}</span>' if icon else ''}
            {title}
        </h3>
        {action if action else ''}
    </div>
    """ if action else f"""
    <h3 style="
        color: {COLORS.TEXT_PRIMARY};
        font-size: {TYPOGRAPHY.FONT_SIZE_LG};
        font-weight: 600;
        margin: 0 0 {SPACING.SPACE_4};
        display: flex;
        align-items: center;
        gap: {SPACING.SPACE_2};
    ">
        {f'<span>{icon}</span>' if icon else ''}
        {title}
    </h3>
    """, unsafe_allow_html=True)


# =============================================================================
# TIMELINE COMPONENTS
# =============================================================================

def timeline_item(
    title: str,
    description: str = "",
    status: str = "completed",
    time: str = "",
    icon: str = "",
) -> None:
    """Render a timeline item.
    
    Args:
        title: Item title
        description: Item description
        status: Status (completed, active, pending)
        time: Time string
        icon: Optional icon
    """
    status_colors = {
        "completed": COLORS.SUCCESS,
        "active": COLORS.PRIMARY,
        "pending": COLORS.TEXT_MUTED,
    }
    
    dot_color = status_colors.get(status, COLORS.TEXT_MUTED)
    
    st.markdown(f"""
    <div style="
        position: relative;
        padding-left: {SPACING.SPACE_8};
        padding-bottom: {SPACING.SPACE_6};
    ">
        <div style="
            position: absolute;
            left: 0;
            top: 4px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: {dot_color};
            {'animation: pulse 2s infinite;' if status == 'active' else ''}
        "></div>
        <div style="
            position: absolute;
            left: 5px;
            top: 20px;
            bottom: 0;
            width: 2px;
            background: {COLORS.BORDER};
        "></div>
        <div>
            <div style="display: flex; align-items: center; gap: {SPACING.SPACE_3}; margin-bottom: {SPACING.SPACE_1};">
                {f'<span>{icon}</span>' if icon else ''}
                <span style="color: {COLORS.TEXT_PRIMARY}; font-weight: 500;">{title}</span>
            </div>
            {f'<p style="color: {COLORS.TEXT_SECONDARY}; font-size: {TYPOGRAPHY.FONT_SIZE_SM}; margin: 0 0 {SPACING.SPACE_1};">{description}</p>' if description else ''}
            {f'<span style="color: {COLORS.TEXT_MUTED}; font-size: {TYPOGRAPHY.FONT_SIZE_XS};">{time}</span>' if time else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# BUTTON COMPONENTS
# =============================================================================

def button_primary(
    label: str,
    icon: str = "",
    key: str = None,
) -> None:
    """Render a primary button."""
    cols = st.columns([1, 1, 2])
    with cols[2]:
        if st.button(f"{icon} {label}" if icon else label, key=key, type="primary"):
            pass


def button_secondary(
    label: str,
    icon: str = "",
    key: str = None,
) -> None:
    """Render a secondary button."""
    cols = st.columns([1, 1, 2])
    with cols[2]:
        if st.button(f"{icon} {label}" if icon else label, key=key):
            pass


# =============================================================================
# ICON & LABEL COMPONENTS
# =============================================================================

def icon_label(
    icon: str,
    label: str,
    color: str = COLORS.TEXT_PRIMARY,
) -> None:
    """Render an icon with label.
    
    Args:
        icon: Icon emoji
        label: Label text
        color: Text color
    """
    st.markdown(f"""
    <span style="
        display: inline-flex;
        align-items: center;
        gap: {SPACING.SPACE_2};
        color: {color};
    ">
        <span>{icon}</span>
        <span>{label}</span>
    </span>
    """, unsafe_allow_html=True)


def stat_item(
    label: str,
    value: str,
    icon: str = "",
) -> None:
    """Render a stat item with label and value.
    
    Args:
        label: Stat label
        value: Stat value
        icon: Optional icon
    """
    st.markdown(f"""
    <div style="
        padding: {SPACING.SPACE_3};
        background: {COLORS.GLASS_LIGHT};
        border-radius: {BORDERS.RADIUS_MD};
    ">
        <div style="display: flex; align-items: center; gap: {SPACING.SPACE_2}; margin-bottom: {SPACING.SPACE_1};">
            {f'<span style="font-size: 1rem;">{icon}</span>' if icon else ''}
            <span style="color: {COLORS.TEXT_MUTED}; font-size: {TYPOGRAPHY.FONT_SIZE_SM};">{label}</span>
        </div>
        <div style="color: {COLORS.TEXT_PRIMARY}; font-size: {TYPOGRAPHY.FONT_SIZE_LG}; font-weight: 600;">
            {value}
        </div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# DIVIDER & SPACER
# =============================================================================

def divider() -> None:
    """Render a horizontal divider."""
    st.markdown(f"""
    <hr style="
        border: none;
        border-top: 1px solid {COLORS.BORDER};
        margin: {SPACING.SPACE_4} 0;
    ">
    """, unsafe_allow_html=True)


def spacer(size: str = SPACING.SPACE_4) -> None:
    """Render vertical spacing."""
    st.markdown(f"<div style='height: {size};'></div>", unsafe_allow_html=True)


# =============================================================================
# LOADING & ANIMATIONS
# =============================================================================

def loading_spinner(message: str = "Loading...") -> None:
    """Render a loading spinner with message."""
    with st.spinner(message):
        pass


def pulse_dot(color: str = COLORS.PRIMARY) -> None:
    """Render an animated pulse dot."""
    st.markdown(f"""
    <span style="
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: {color};
        animation: pulse 2s infinite ease-in-out;
    "></span>
    """, unsafe_allow_html=True)


# =============================================================================
# EMPTY STATE
# =============================================================================

def empty_state(
    icon: str = "📭",
    title: str = "No Data",
    description: str = "",
) -> None:
    """Render an empty state message.
    
    Args:
        icon: Empty state icon
        title: Title text
        description: Description text
    """
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: {SPACING.SPACE_12};
        color: {COLORS.TEXT_MUTED};
    ">
        <div style="font-size: 3rem; margin-bottom: {SPACING.SPACE_4};">{icon}</div>
        <h3 style="color: {COLORS.TEXT_SECONDARY}; margin-bottom: {SPACING.SPACE_2};">{title}</h3>
        {f'<p style="font-size: {TYPOGRAPHY.FONT_SIZE_SM};">{description}</p>' if description else ''}
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# NOTIFICATION / TOAST
# =============================================================================

def notification(
    message: str,
    notification_type: str = "info",
    icon: str = None,
) -> None:
    """Render a notification toast.
    
    Args:
        message: Notification message
        notification_type: Type (success, error, warning, info)
        icon: Optional custom icon
    """
    colors = {
        "success": (COLORS.SUCCESS, COLORS.SUCCESS_RGB, "✅"),
        "error": (COLORS.ERROR, COLORS.ERROR_RGB, "❌"),
        "warning": (COLORS.WARNING, COLORS.WARNING_RGB, "⚠️"),
        "info": (COLORS.PRIMARY, COLORS.PRIMARY_RGB, "ℹ️"),
    }
    
    color, rgb, default_icon = colors.get(notification_type, colors["info"])
    notification_icon = icon or default_icon
    
    st.markdown(f"""
    <div style="
        background: rgba({rgb}, 0.2);
        border: 1px solid {color};
        border-radius: {BORDERS.RADIUS_MD};
        padding: {SPACING.SPACE_3} {SPACING.SPACE_4};
        margin-bottom: {SPACING.SPACE_3};
        display: flex;
        align-items: center;
        gap: {SPACING.SPACE_3};
    ">
        <span>{notification_icon}</span>
        <span style="color: {COLORS.TEXT_PRIMARY};">{message}</span>
    </div>
    """, unsafe_allow_html=True)
