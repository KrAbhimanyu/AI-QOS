"""Performance optimization utilities for AI-QOS.

This module provides caching, memoization, and performance utilities
for optimizing Streamlit application performance.
"""
from typing import Any, Callable, Optional, Dict, List, TypeVar, Generic
from functools import wraps
import streamlit as st

# Type variable for generic caching
T = TypeVar('T')


# =============================================================================
# CACHING UTILITIES
# =============================================================================

def cache_with_session(key: str, ttl: int = 3600):
    """Cache data with session state backup for persistence.
    
    Args:
        key: Cache key
        ttl: Time to live in seconds (default 1 hour)
    
    Usage:
        @cache_with_session("my_data")
        def get_data():
            return expensive_computation()
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            # Check if cached in session state
            cache_key = f"cache_{key}"
            cache_time_key = f"cache_time_{key}"
            
            if cache_key in st.session_state:
                cached_time = st.session_state.get(cache_time_key, 0)
                import time
                if time.time() - cached_time < ttl:
                    return st.session_state[cache_key]
            
            # Compute and cache
            result = func(*args, **kwargs)
            import time
            st.session_state[cache_key] = result
            st.session_state[cache_time_key] = time.time()
            return result
        return wrapper
    return decorator


def memoize(func: Callable[..., T]) -> Callable[..., T]:
    """Simple memoization decorator using session state.
    
    Usage:
        @memoize
        def expensive_function(arg1, arg2):
            return compute(arg1, arg2)
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        # Create cache key from function name and arguments
        cache_key = f"memo_{func.__name__}_{str(args)}_{str(kwargs)}"
        
        if cache_key in st.session_state:
            return st.session_state[cache_key]
        
        result = func(*args, **kwargs)
        st.session_state[cache_key] = result
        return result
    return wrapper


# =============================================================================
# LAZY LOADING UTILITIES
# =============================================================================

class LazyLoader:
    """Lazy loader for deferring expensive imports.
    
    Usage:
        plotly = LazyLoader("plotly.graph_objects", "go")
        
        # Later, when needed:
        fig = plotly.Figure()
    """
    
    def __init__(self, module_name: str, alias: str = None):
        self.module_name = module_name
        self.alias = alias or module_name.split('.')[-1]
        self._module = None
    
    @property
    def module(self):
        if self._module is None:
            import importlib
            self._module = importlib.import_module(self.module_name)
        return self._module
    
    def __getattr__(self, name: str) -> Any:
        return getattr(self.module, name)


# Lazy-loaded modules
PLOTLY_FIGURES = LazyLoader("plotly.graph_objects", "go")
PLOTLY_EXPRESS = LazyLoader("plotly.express", "px")
PANDAS = LazyLoader("pandas", "pd")


# =============================================================================
# SESSION STATE UTILITIES
# =============================================================================

class SessionStateManager:
    """Manager for optimized session state operations."""
    
    @staticmethod
    def get(key: str, default: Any = None, validator: Callable = None) -> Any:
        """Get value with optional validation.
        
        Args:
            key: Session state key
            default: Default value if not found
            validator: Optional function to validate the value
        
        Returns:
            Session state value or default
        """
        value = st.session_state.get(key, default)
        
        if validator and value is not None:
            if not validator(value):
                return default
        
        return value
    
    @staticmethod
    def set_if_not_exists(key: str, value: Any) -> bool:
        """Set value only if key doesn't exist.
        
        Args:
            key: Session state key
            value: Value to set
        
        Returns:
            True if set, False if already exists
        """
        if key not in st.session_state:
            st.session_state[key] = value
            return True
        return False
    
    @staticmethod
    def initialize_defaults(defaults: Dict[str, Any]) -> None:
        """Initialize multiple defaults efficiently.
        
        Args:
            defaults: Dictionary of key-value pairs
        """
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    @staticmethod
    def clear_prefix(prefix: str) -> int:
        """Clear all session state keys with given prefix.
        
        Args:
            prefix: Key prefix to match
        
        Returns:
            Number of keys cleared
        """
        keys_to_delete = [
            key for key in st.session_state.keys()
            if key.startswith(prefix)
        ]
        for key in keys_to_delete:
            del st.session_state[key]
        return len(keys_to_delete)
    
    @staticmethod
    def get_all(prefix: str) -> Dict[str, Any]:
        """Get all session state values with given prefix.
        
        Args:
            prefix: Key prefix to match
        
        Returns:
            Dictionary of matching keys and values
        """
        return {
            key: value
            for key, value in st.session_state.items()
            if key.startswith(prefix)
        }


# =============================================================================
# RENDERING OPTIMIZATION
# =============================================================================

def should_render(key: str, condition: bool = True, ttl: int = 1) -> bool:
    """Determine if a component should render based on throttle.
    
    Args:
        key: Unique key for the component
        condition: Additional condition to check
        ttl: Minimum time between renders in seconds
    
    Returns:
        True if should render, False otherwise
    """
    render_key = f"render_time_{key}"
    last_render = st.session_state.get(render_key, 0)
    
    import time
    current_time = time.time()
    
    if current_time - last_render >= ttl and condition:
        st.session_state[render_key] = current_time
        return True
    
    return False


def render_once(key: str, condition: bool = True) -> bool:
    """Render a component only once per session unless condition changes.
    
    Args:
        key: Unique key for the component
        condition: Condition that triggers re-render
    
    Returns:
        True if should render, False otherwise
    """
    render_key = f"rendered_{key}"
    condition_key = f"condition_{key}"
    
    current_condition = st.session_state.get(condition_key)
    
    if current_condition != condition or not st.session_state.get(render_key):
        st.session_state[render_key] = True
        st.session_state[condition_key] = condition
        return True
    
    return False


# =============================================================================
# DATA PROCESSING OPTIMIZATION
# =============================================================================

def paginate_data(data: List[Any], page: int = 1, per_page: int = 20) -> tuple:
    """Paginate data efficiently.
    
    Args:
        data: List of items
        page: Current page (1-indexed)
        per_page: Items per page
    
    Returns:
        Tuple of (paginated_data, total_pages, has_next, has_prev)
    """
    total_items = len(data)
    total_pages = max(1, (total_items + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    return (
        data[start_idx:end_idx],
        total_pages,
        page < total_pages,
        page > 1
    )


def chunk_data(data: List[Any], chunk_size: int = 100) -> List[List[Any]]:
    """Split data into chunks for processing.
    
    Args:
        data: List of items
        chunk_size: Size of each chunk
    
    Returns:
        List of data chunks
    """
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


def filter_dataframe_columns(df, columns: List[str]) -> 'pd.DataFrame':
    """Filter dataframe columns efficiently.
    
    Args:
        df: Pandas DataFrame
        columns: List of columns to keep
    
    Returns:
        Filtered DataFrame
    """
    return df[[c for c in columns if c in df.columns]]


# =============================================================================
# PERFORMANCE METRICS
# =============================================================================

class PerformanceTimer:
    """Context manager for timing operations."""
    
    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        import time
        self.start_time = time.time()
        return self
    
    def __exit__(self, *args):
        import time
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        st.session_state[f"perf_{self.name}"] = duration
    
    @property
    def duration_ms(self) -> float:
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time) * 1000
        return 0


def log_performance(name: str, duration_ms: float, threshold_ms: float = 100) -> None:
    """Log performance metrics to session state.
    
    Args:
        name: Operation name
        duration_ms: Duration in milliseconds
        threshold_ms: Threshold for warning
    """
    key = f"perf_log_{name}"
    st.session_state[key] = {
        "duration_ms": duration_ms,
        "warning": duration_ms > threshold_ms
    }


# =============================================================================
# MEMORY OPTIMIZATION
# =============================================================================

def cleanup_large_data(keys: List[str], max_size_mb: float = 10) -> int:
    """Clean up large session state data.
    
    Args:
        keys: List of keys to check and potentially delete
        max_size_mb: Maximum allowed size in MB
    
    Returns:
        Number of keys cleaned up
    """
    import sys
    
    cleaned = 0
    for key in keys:
        if key in st.session_state:
            value = st.session_state[key]
            # Estimate size
            size = sys.getsizeof(str(value)) / (1024 * 1024)
            
            if size > max_size_mb:
                del st.session_state[key]
                cleaned += 1
    
    return cleaned


def get_session_size() -> Dict[str, float]:
    """Get session state size breakdown.
    
    Returns:
        Dictionary with size info in MB
    """
    import sys
    
    total_size = 0
    breakdown = {}
    
    for key, value in st.session_state.items():
        size = sys.getsizeof(str(value)) / (1024 * 1024)
        breakdown[key] = size
        total_size += size
    
    return {
        "total_mb": total_size,
        "breakdown": breakdown
    }


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Caching
    "cache_with_session",
    "memoize",
    # Lazy loading
    "LazyLoader",
    "PLOTLY_FIGURES",
    "PLOTLY_EXPRESS",
    "PANDAS",
    # Session state
    "SessionStateManager",
    # Rendering
    "should_render",
    "render_once",
    # Data processing
    "paginate_data",
    "chunk_data",
    "filter_dataframe_columns",
    # Performance
    "PerformanceTimer",
    "log_performance",
    # Memory
    "cleanup_large_data",
    "get_session_size",
]
