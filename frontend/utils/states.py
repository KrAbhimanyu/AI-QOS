"""State management utilities for AI-QOS.

This module provides utilities for managing application states
including loading, empty, error, and offline states.
"""
from typing import Optional, Callable, Any
import streamlit as st


# =============================================================================
# STATE DEFINITIONS
# =============================================================================

class AppState:
    """Application state definitions."""
    
    LOADING = "loading"
    READY = "ready"
    ERROR = "error"
    EMPTY = "empty"
    OFFLINE = "offline"
    INITIALIZING = "initializing"


# =============================================================================
# STATE INDICATOR
# =============================================================================

def state_indicator(
    state: str,
    message: str = None,
) -> None:
    """Display a state indicator.
    
    Args:
        state: Current state
        message: Optional custom message
    """
    states = {
        AppState.LOADING: ("⏳", "Loading...", "#6366F1"),
        AppState.READY: ("✅", "Ready", "#10B981"),
        AppState.ERROR: ("❌", "Error", "#EF4444"),
        AppState.EMPTY: ("📭", "No Data", "#64748B"),
        AppState.OFFLINE: ("📡", "Offline", "#F59E0B"),
        AppState.INITIALIZING: ("🔄", "Initializing...", "#22D3EE"),
    }
    
    icon, default_message, color = states.get(state, states[AppState.LOADING])
    display_message = message or default_message
    
    st.markdown(f"""
    <div style="
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 8px;
        border-left: 3px solid {color};
    ">
        <span style="font-size: 1.5rem;">{icon}</span>
        <span style="color: #F1F5F9; font-size: 0.875rem;">{display_message}</span>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# LOADING STATES
# =============================================================================

def loading_spinner(
    message: str = "Loading...",
    show_animation: bool = True,
) -> None:
    """Display a loading spinner.
    
    Args:
        message: Loading message
        show_animation: Whether to show animation
    """
    if show_animation:
        st.markdown(f"""
        <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1rem;
            padding: 2rem;
        ">
            <div style="
                width: 40px;
                height: 40px;
                border: 3px solid rgba(99, 102, 241, 0.3);
                border-top-color: #6366F1;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            "></div>
            <span style="color: #94A3B8; font-size: 0.875rem;">{message}</span>
        </div>
        <style>
            @keyframes spin {{
                to {{ transform: rotate(360deg); }}
            }}
        </style>
        """, unsafe_allow_html=True)
    else:
        with st.spinner(message):
            pass


def loading_progress(
    current: int,
    total: int,
    message: str = "Loading",
) -> None:
    """Display a loading progress indicator.
    
    Args:
        current: Current progress value
        total: Total progress value
        message: Progress message
    """
    percentage = (current / total) * 100 if total > 0 else 0
    
    st.markdown(f"""
    <div style="padding: 1rem;">
        <div style="margin-bottom: 0.5rem; color: #94A3B8; font-size: 0.75rem;">
            {message} {current}/{total}
        </div>
        <div style="
            height: 6px;
            background: #334155;
            border-radius: 3px;
            overflow: hidden;
        ">
            <div style="
                width: {percentage}%;
                height: 100%;
                background: linear-gradient(90deg, #6366F1, #818CF8);
                border-radius: 3px;
                transition: width 0.3s ease;
            "></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def loading_skeleton(
    lines: int = 5,
    height: str = "1rem",
) -> None:
    """Display a loading skeleton.
    
    Args:
        lines: Number of skeleton lines
        height: Height of each line
    """
    skeletons = ""
    for i in range(lines):
        width = 100 if i == 0 else (90 - i * 5)
        skeletons += f"""
        <div style="
            height: {height};
            width: {width}%;
            background: linear-gradient(
                90deg,
                rgba(51, 65, 85, 0.3) 25%,
                rgba(51, 65, 85, 0.5) 50%,
                rgba(51, 65, 85, 0.3) 75%
            );
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
            border-radius: 4px;
            margin-bottom: 0.75rem;
        "></div>
        """
    
    st.markdown(f"""
    <div style="padding: 1rem;">
        {skeletons}
    </div>
    <style>
        @keyframes shimmer {{
            0% {{ background-position: 200% 0; }}
            100% {{ background-position: -200% 0; }}
        }}
    </style>
    """, unsafe_allow_html=True)


# =============================================================================
# EMPTY STATES
# =============================================================================

def empty_state(
    icon: str = "📭",
    title: str = "No Data",
    message: str = "",
    action_label: str = None,
    action_key: str = None,
) -> Optional[bool]:
    """Display an empty state with optional action.
    
    Args:
        icon: Empty state icon
        title: Empty state title
        message: Additional message
        action_label: Optional action button label
        action_key: Key for action button
    
    Returns:
        True if action clicked, None otherwise
    """
    st.markdown(f"""
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem 1rem;
        text-align: center;
    ">
        <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
        <h3 style="
            color: #94A3B8;
            font-size: 1.125rem;
            font-weight: 500;
            margin: 0 0 0.5rem;
        ">{title}</h3>
        {f'<p style="color: #64748B; font-size: 0.875rem; margin: 0;">{message}</p>' if message else ''}
    </div>
    """, unsafe_allow_html=True)
    
    if action_label:
        return st.button(action_label, key=action_key, type="primary")


def empty_search_results(
    query: str = "",
) -> None:
    """Display empty search results state.
    
    Args:
        query: Search query that returned no results
    """
    st.markdown(f"""
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 2rem;
        text-align: center;
    ">
        <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔍</div>
        <h3 style="color: #94A3B8; margin: 0 0 0.5rem;">No Results Found</h3>
        {f'<p style="color: #64748B; font-size: 0.875rem; margin: 0;">No matches for "{query}"</p>' if query else ''}
        <p style="color: #64748B; font-size: 0.75rem; margin: 1rem 0 0;">
            Try adjusting your search or filters
        </p>
    </div>
    """, unsafe_allow_html=True)


def empty_list(
    item_type: str = "items",
    action_label: str = None,
    action_key: str = None,
) -> Optional[bool]:
    """Display empty list state.
    
    Args:
        item_type: Type of items expected
        action_label: Optional action to add first item
        action_key: Key for action button
    
    Returns:
        True if action clicked, None otherwise
    """
    return empty_state(
        icon="📋",
        title=f"No {item_type.title()}",
        message=f"Add your first {item_type} to get started",
        action_label=action_label,
        action_key=action_key,
    )


# =============================================================================
# ERROR STATES
# =============================================================================

def error_state(
    error: str = "Something went wrong",
    message: str = "",
    retry_key: str = None,
    show_retry: bool = True,
) -> Optional[bool]:
    """Display an error state with retry option.
    
    Args:
        error: Error title
        message: Error details
        retry_key: Key for retry button
        show_retry: Whether to show retry button
    
    Returns:
        True if retry clicked, None otherwise
    """
    st.markdown(f"""
    <div style="
        padding: 2rem;
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px;
        text-align: center;
    ">
        <div style="font-size: 2.5rem; margin-bottom: 1rem;">❌</div>
        <h3 style="color: #EF4444; margin: 0 0 0.5rem;">{error}</h3>
        {f'<p style="color: #94A3B8; font-size: 0.875rem; margin: 0 0 1rem;">{message}</p>' if message else ''}
    </div>
    """, unsafe_allow_html=True)
    
    if show_retry:
        return st.button("🔄 Retry", key=retry_key, type="secondary")


def error_message(
    message: str,
    dismissible: bool = True,
) -> None:
    """Display an inline error message.
    
    Args:
        message: Error message
        dismissible: Whether user can dismiss
    """
    st.error(message)


def warning_message(
    message: str,
) -> None:
    """Display an inline warning message.
    
    Args:
        message: Warning message
    """
    st.warning(message)


def info_message(
    message: str,
) -> None:
    """Display an inline info message.
    
    Args:
        message: Info message
    """
    st.info(message)


def success_message(
    message: str,
) -> None:
    """Display an inline success message.
    
    Args:
        message: Success message
    """
    st.success(message)


# =============================================================================
# OFFLINE STATE
# =============================================================================

def offline_state(
    message: str = "You appear to be offline",
    action_label: str = "Retry Connection",
    action_key: str = None,
) -> Optional[bool]:
    """Display an offline state.
    
    Args:
        message: Offline message
        action_label: Label for retry button
        action_key: Key for retry button
    
    Returns:
        True if retry clicked, None otherwise
    """
    st.markdown(f"""
    <div style="
        padding: 3rem 2rem;
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 12px;
        text-align: center;
    ">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📡</div>
        <h3 style="color: #F59E0B; margin: 0 0 0.5rem;">Connection Lost</h3>
        <p style="color: #94A3B8; font-size: 0.875rem; margin: 0 0 1.5rem;">{message}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if action_label:
        return st.button(action_label, key=action_key, type="primary")


# =============================================================================
# STATE WRAPPER
# =============================================================================

def with_state_handling(
    data: Any,
    loading: bool = False,
    error: str = None,
    empty_message: str = "No data available",
    show_retry: bool = True,
) -> bool:
    """Handle multiple states for data display.
    
    Args:
        data: Data to display
        loading: Whether data is loading
        error: Error message if any
        empty_message: Message for empty state
        show_retry: Whether to show retry option
    
    Returns:
        True if data is ready to display
    """
    if loading:
        loading_spinner()
        return False
    
    if error:
        error_state(error=error, show_retry=show_retry)
        return False
    
    if data is None or (hasattr(data, '__len__') and len(data) == 0):
        empty_state(message=empty_message)
        return False
    
    return True


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "AppState",
    "state_indicator",
    "loading_spinner",
    "loading_progress",
    "loading_skeleton",
    "empty_state",
    "empty_search_results",
    "empty_list",
    "error_state",
    "error_message",
    "warning_message",
    "info_message",
    "success_message",
    "offline_state",
    "with_state_handling",
]
