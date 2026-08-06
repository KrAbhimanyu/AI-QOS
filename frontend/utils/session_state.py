"""Session State Initializer for AI-QOS.

This module centralizes all session state initialization to ensure
consistent and optimized state management across the application.
"""
from typing import Dict, Any, Callable, List
import streamlit as st


# =============================================================================
# COMPONENT STATE DEFINITIONS
# =============================================================================

# Agent Control Tower state
AGENT_STATE = {
    "agent_selected": None,
    "agent_filter": "all",
    "agent_search": "",
    "agent_sort_by": "status",
    "agent_view_mode": "grid",
}

# Chat Workspace state
CHAT_STATE = {
    "chat_conversations": [],
    "chat_current_conversation": None,
    "chat_messages": [],
    "chat_prompt_history": [],
    "chat_pinned": [],
    "chat_selected_context": None,
}

# Execution Center state
EXECUTION_STATE = {
    "exec_is_running": True,
    "exec_paused": False,
    "exec_current_test": "test_login_flow",
    "exec_current_step": 3,
    "exec_progress": 67,
    "exec_passed": 24,
    "exec_failed": 2,
    "exec_skipped": 3,
    "exec_elapsed": 125,
    "exec_confidence": 92,
    "exec_current_url": "https://demo.app/dashboard",
    "exec_browser_screenshot": "dashboard",
}

# Intelligence Center state
INTELLIGENCE_STATE = {
    "intel_current_phase": 0,
    "intel_phase_progress": {},
    "intel_discovery_complete": False,
    "intel_paused": False,
    "intel_start_time": None,
    "intel_discovered_pages": [],
    "intel_technology_stack": {},
    "intel_stats": {
        "total_pages": 0,
        "forms": 0,
        "buttons": 0,
        "tables": 0,
        "dropdowns": 0,
        "dialogs": 0,
        "api_endpoints": 0,
    },
}

# Human Review state
REVIEW_STATE = {
    "review_current_test": "Login Flow - Dashboard Access",
    "review_current_step": "Verify Dashboard Loaded",
    "review_agent": "Frontend Agent",
    "review_confidence": 92,
    "review_status": "waiting",
    "review_evidence": {},
    "review_decision": None,
    "review_comments": [],
    "review_bug_draft": None,
}

# DOM Explorer state
DOM_STATE = {
    "dom_expanded_nodes": set(),
    "dom_selected_node": None,
    "dom_filter": "",
    "dom_view": "tree",
}

# Application Explorer state
EXPLORER_STATE = {
    "explorer_filter": "",
    "explorer_sort": "name",
    "explorer_page": 1,
}

# Knowledge Graph state
KNOWLEDGE_STATE = {
    "knowledge_search": "",
    "knowledge_selected_node": None,
    "knowledge_depth": 2,
}

# All state definitions combined
ALL_STATES: Dict[str, Dict[str, Any]] = {
    "agent": AGENT_STATE,
    "chat": CHAT_STATE,
    "execution": EXECUTION_STATE,
    "intelligence": INTELLIGENCE_STATE,
    "review": REVIEW_STATE,
    "dom": DOM_STATE,
    "explorer": EXPLORER_STATE,
    "knowledge": KNOWLEDGE_STATE,
}


# =============================================================================
# INITIALIZER CLASS
# =============================================================================

class SessionStateInitializer:
    """Centralized session state initialization."""
    
    @staticmethod
    def initialize_all() -> None:
        """Initialize all session state variables."""
        # Global state
        if "user" not in st.session_state:
            st.session_state.user = "Demo User"
        if "theme" not in st.session_state:
            st.session_state.theme = "dark"
        if "current_view" not in st.session_state:
            st.session_state.current_view = "dashboard"
        if "initialized" not in st.session_state:
            st.session_state.initialized = True
        
        # Component states
        for component_name, defaults in ALL_STATES.items():
            SessionStateInitializer.initialize_component(component_name, defaults)
    
    @staticmethod
    def initialize_component(component_name: str, defaults: Dict[str, Any]) -> None:
        """Initialize session state for a specific component.
        
        Args:
            component_name: Name of the component
            defaults: Dictionary of default values
        """
        for key, value in defaults.items():
            full_key = f"{component_name}_{key}"
            if full_key not in st.session_state:
                # Handle special types
                if isinstance(value, dict):
                    st.session_state[full_key] = value.copy()
                elif isinstance(value, set):
                    st.session_state[full_key] = value.copy()
                elif isinstance(value, list):
                    st.session_state[full_key] = value.copy()
                else:
                    st.session_state[full_key] = value
    
    @staticmethod
    def get_state(component: str, key: str, default: Any = None) -> Any:
        """Get a specific state value.
        
        Args:
            component: Component name
            key: State key
            default: Default value if not found
        
        Returns:
            State value or default
        """
        full_key = f"{component}_{key}"
        return st.session_state.get(full_key, default)
    
    @staticmethod
    def set_state(component: str, key: str, value: Any) -> None:
        """Set a specific state value.
        
        Args:
            component: Component name
            key: State key
            value: Value to set
        """
        full_key = f"{component}_{key}"
        st.session_state[full_key] = value
    
    @staticmethod
    def clear_component(component_name: str) -> int:
        """Clear all state for a component.
        
        Args:
            component_name: Name of the component
        
        Returns:
            Number of keys cleared
        """
        prefix = f"{component_name}_"
        keys_to_delete = [
            key for key in st.session_state.keys()
            if key.startswith(prefix)
        ]
        for key in keys_to_delete:
            del st.session_state[key]
        return len(keys_to_delete)
    
    @staticmethod
    def reset_all() -> None:
        """Reset all session state (use with caution!)."""
        for key in list(st.session_state.keys()):
            if key != "initialized":
                del st.session_state[key]
        SessionStateInitializer.initialize_all()


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def init_all_state() -> None:
    """Initialize all session state (convenience function)."""
    SessionStateInitializer.initialize_all()


def get_state(component: str, key: str, default: Any = None) -> Any:
    """Get session state value (convenience function)."""
    return SessionStateInitializer.get_state(component, key, default)


def set_state(component: str, key: str, value: Any) -> None:
    """Set session state value (convenience function)."""
    SessionStateInitializer.set_state(component, key, value)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # State definitions
    "AGENT_STATE",
    "CHAT_STATE",
    "EXECUTION_STATE",
    "INTELLIGENCE_STATE",
    "REVIEW_STATE",
    "DOM_STATE",
    "EXPLORER_STATE",
    "KNOWLEDGE_STATE",
    "ALL_STATES",
    # Initializer class
    "SessionStateInitializer",
    # Convenience functions
    "init_all_state",
    "get_state",
    "set_state",
]
