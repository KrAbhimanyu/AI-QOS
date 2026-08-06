"""Session state management for Agent Control Tower."""

from datetime import datetime
from typing import Any, Callable
import streamlit as st


class SessionState:
    """Manages session state for the Agent Control Tower application."""
    
    _initialized = False
    
    @classmethod
    def initialize(cls) -> None:
        """Initialize all session state variables."""
        if cls._initialized:
            return
            
        # Agent data
        if "agents" not in st.session_state:
            st.session_state.agents = []
        
        # Selected agent
        if "selected_agent" not in st.session_state:
            st.session_state.selected_agent = None
        
        # Drawer state
        if "drawer_open" not in st.session_state:
            st.session_state.drawer_open = False
        
        # Filters
        if "filter_category" not in st.session_state:
            st.session_state.filter_category = "All"
        
        if "filter_status" not in st.session_state:
            st.session_state.filter_status = "All"
        
        if "search_query" not in st.session_state:
            st.session_state.search_query = ""
        
        # Graph state
        if "graph_animating" not in st.session_state:
            st.session_state.graph_animating = True
        
        if "active_pipeline_step" not in st.session_state:
            st.session_state.active_pipeline_step = 0
        
        # Events
        if "events" not in st.session_state:
            st.session_state.events = []
        
        if "last_event_update" not in st.session_state:
            st.session_state.last_event_update = datetime.now()
        
        # Refresh state
        if "auto_refresh" not in st.session_state:
            st.session_state.auto_refresh = True
        
        if "refresh_interval" not in st.session_state:
            st.session_state.refresh_interval = 5
        
        # Mission info
        if "mission_name" not in st.session_state:
            st.session_state.mission_name = "AI-QOS Sprint 07"
        
        if "environment" not in st.session_state:
            st.session_state.environment = "production"
        
        if "execution_start" not in st.session_state:
            st.session_state.execution_start = datetime.now()
        
        cls._initialized = True
    
    @classmethod
    def select_agent(cls, agent: dict[str, Any] | None) -> None:
        """Select an agent and open drawer."""
        st.session_state.selected_agent = agent
        st.session_state.drawer_open = agent is not None
    
    @classmethod
    def close_drawer(cls) -> None:
        """Close the agent drawer."""
        st.session_state.drawer_open = False
        st.session_state.selected_agent = None
    
    @classmethod
    def set_filter(cls, category: str | None = None, status: str | None = None) -> None:
        """Update filter state."""
        if category is not None:
            st.session_state.filter_category = category
        if status is not None:
            st.session_state.filter_status = status
    
    @classmethod
    def set_search(cls, query: str) -> None:
        """Update search query."""
        st.session_state.search_query = query
    
    @classmethod
    def add_event(cls, event: dict[str, Any]) -> None:
        """Add an event to the event stream."""
        st.session_state.events.insert(0, event)
        if len(st.session_state.events) > 100:
            st.session_state.events = st.session_state.events[:100]
    
    @classmethod
    def get_filtered_agents(cls, agents: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Get filtered agents based on current state."""
        filtered = agents
        
        # Filter by category
        if st.session_state.filter_category != "All":
            filtered = [
                a for a in filtered 
                if a["category"].value == st.session_state.filter_category
            ]
        
        # Filter by status
        if st.session_state.filter_status != "All":
            filtered = [
                a for a in filtered 
                if a["status"].value == st.session_state.filter_status.lower()
            ]
        
        # Filter by search query
        if st.session_state.search_query:
            query = st.session_state.search_query.lower()
            filtered = [
                a for a in filtered
                if query in a["name"].lower()
                or query in a["description"].lower()
                or query in a["mission"].lower()
            ]
        
        return filtered
    
    @classmethod
    def advance_pipeline(cls) -> None:
        """Advance the communication pipeline animation."""
        from src.data.mock_data import COMMUNICATION_PIPELINE
        st.session_state.active_pipeline_step = (
            st.session_state.active_pipeline_step + 1
        ) % (len(COMMUNICATION_PIPELINE) + 1)
    
    @classmethod
    def toggle_animation(cls) -> None:
        """Toggle graph animation."""
        st.session_state.graph_animating = not st.session_state.graph_animating
    
    @classmethod
    def reset(cls) -> None:
        """Reset session state to defaults."""
        keys_to_reset = [
            "selected_agent", "drawer_open", "filter_category",
            "filter_status", "search_query", "events"
        ]
        for key in keys_to_reset:
            if key in st.session_state:
                if key == "filter_category":
                    st.session_state[key] = "All"
                elif key == "filter_status":
                    st.session_state[key] = "All"
                elif key in ["selected_agent", "drawer_open"]:
                    st.session_state[key] = None if "agent" in key else False
                else:
                    st.session_state[key] = "" if "search" in key else []


class AutoRefresh:
    """Auto-refresh manager for the application."""
    
    @classmethod
    def should_refresh(cls) -> bool:
        """Check if it's time to refresh."""
        if not st.session_state.get("auto_refresh", True):
            return False
        
        last_update = st.session_state.get("last_event_update", datetime.now())
        interval = st.session_state.get("refresh_interval", 5)
        
        elapsed = (datetime.now() - last_update).total_seconds()
        return elapsed >= interval
    
    @classmethod
    def update_timestamp(cls) -> None:
        """Update the last refresh timestamp."""
        st.session_state.last_event_update = datetime.now()


def render_page_config() -> None:
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Agent Control Tower - AI-QOS",
        page_icon="🎛️",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
