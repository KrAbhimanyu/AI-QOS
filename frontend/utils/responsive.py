"""Responsive layout utilities for AI-QOS.

This module provides responsive layout helpers for creating
layouts that work across desktop, laptop, tablet, and mobile.
"""
from typing import List, Tuple, Optional
import streamlit as st


# =============================================================================
# BREAKPOINT TOKENS
# =============================================================================

class Breakpoints:
    """Responsive breakpoints matching design system."""
    
    MOBILE = "640px"
    TABLET = "768px"
    DESKTOP = "1024px"
    LARGE = "1280px"
    XLARGE = "1536px"


# =============================================================================
# COLUMN CONFIGURATIONS
# =============================================================================

class ColumnConfig:
    """Predefined column layouts for responsive design."""
    
    # Single column
    SINGLE = (1,)
    
    # Two columns
    HALF_HALF = (1, 1)
    THIRD_TWO_THIRDS = (1, 2)
    TWO_THIRDS_THIRD = (2, 1)
    
    # Three columns
    THIRDS = (1, 1, 1)
    QUARTER_THREE_QUARTERS = (1, 3)
    THREE_QUARTERS_QUARTER = (3, 1)
    
    # Four columns
    QUARTERS = (1, 1, 1, 1)
    HALF_QUARTER_QUARTER = (2, 1, 1)
    
    # Six columns (for metrics)
    SIXTHS = (1, 1, 1, 1, 1, 1)
    
    # Sidebar layouts
    SIDEBAR_MAIN = (1, 3)
    SIDEBAR_MAIN_WIDE = (1, 4)
    MAIN_SIDEBAR = (3, 1)
    
    # Dashboard layouts
    METRICS_ROW = (1, 1, 1, 1)  # 4 equal columns
    METRICS_ROW_3 = (1, 1, 1)   # 3 equal columns


# =============================================================================
# RESPONSIVE COLUMN HELPER
# =============================================================================

def responsive_columns(
    config: Tuple[int, ...],
    gap: str = "small",
) -> List:
    """Create responsive columns with consistent gap.
    
    Args:
        config: Column configuration tuple
        gap: Gap size ("small", "medium", "large")
    
    Returns:
        List of column objects
    """
    gap_map = {
        "small": "1rem",
        "medium": "1.5rem",
        "large": "2rem",
    }
    
    with st.container():
        return st.columns(config)


def metrics_row(
    num_metrics: int = 4,
    min_width: int = 150,
) -> List:
    """Create a metrics row with responsive sizing.
    
    Args:
        num_metrics: Number of metrics to display
        min_width: Minimum pixel width per metric
    
    Returns:
        List of column objects
    """
    # Calculate column ratios
    ratios = tuple(1 for _ in range(num_metrics))
    return st.columns(ratios)


def responsive_grid(
    items: List,
    columns_desktop: int = 4,
    columns_tablet: int = 2,
    columns_mobile: int = 1,
) -> List:
    """Create a responsive grid that adjusts columns based on viewport.
    
    Note: Streamlit doesn't natively support viewport detection.
    This function provides the structure; actual responsive behavior
    requires CSS media queries.
    
    Args:
        items: List of items to render
        columns_desktop: Columns on desktop
        columns_tablet: Columns on tablet
        columns_mobile: Columns on mobile
    
    Returns:
        List of column objects
    """
    # Use desktop columns as default (Streamlit limitation)
    return st.columns(tuple(1 for _ in range(columns_desktop)))


# =============================================================================
# BREAKPOINT CSS INJECTION
# =============================================================================

def inject_responsive_css() -> None:
    """Inject responsive CSS for media queries."""
    st.markdown("""
    <style>
    /* Responsive CSS for AI-QOS */
    
    /* Mobile (up to 640px) */
    @media (max-width: 640px) {
        .stColumns {
            gap: 0.5rem !important;
        }
        
        .stHorizontalBlock {
            flex-wrap: wrap !important;
        }
        
        div[data-testid="stHorizontalBlock"] > div {
            min-width: 100% !important;
            flex: 1 1 100% !important;
        }
    }
    
    /* Tablet (641px - 1024px) */
    @media (min-width: 641px) and (max-width: 1024px) {
        .stHorizontalBlock > div {
            flex: 1 1 calc(50% - 1rem) !important;
        }
    }
    
    /* Desktop (1025px+) */
    @media (min-width: 1025px) {
        .stHorizontalBlock > div {
            flex: 1 1 auto !important;
        }
    }
    
    /* Hide elements on mobile */
    @media (max-width: 640px) {
        .hide-mobile {
            display: none !important;
        }
    }
    
    /* Show elements on mobile only */
    @media (min-width: 641px) {
        .show-mobile-only {
            display: none !important;
        }
    }
    
    /* Responsive spacing */
    @media (max-width: 640px) {
        .stMetric {
            padding: 0.5rem !important;
        }
        
        div[data-testid="stMetric"] {
            background: transparent !important;
            border: none !important;
        }
    }
    
    /* Responsive typography */
    @media (max-width: 640px) {
        h1 {
            font-size: 1.5rem !important;
        }
        h2 {
            font-size: 1.25rem !important;
        }
        h3 {
            font-size: 1rem !important;
        }
    }
    
    /* Responsive cards */
    @media (max-width: 640px) {
        .aiqos-card {
            padding: 1rem !important;
            margin-bottom: 0.75rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


# =============================================================================
# RESPONSIVE UTILITY CLASSES
# =============================================================================

def responsive_container(
    max_width: str = "1200px",
    padding: str = "2rem",
) -> None:
    """Create a responsive container with max-width.
    
    Args:
        max_width: Maximum width of container
        padding: Container padding
    """
    st.markdown(f"""
    <style>
        .responsive-container {{
            max-width: {max_width};
            margin: 0 auto;
            padding: {padding};
        }}
        
        @media (max-width: 640px) {{
            .responsive-container {{
                padding: 1rem;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)


def hide_on_mobile(element_class: str) -> None:
    """Add CSS to hide an element on mobile.
    
    Args:
        element_class: CSS class of element to hide
    """
    st.markdown(f"""
    <style>
        .{element_class} {{
            display: none;
        }}
        
        @media (min-width: 641px) {{
            .{element_class} {{
                display: block;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)


def show_on_mobile_only(element_class: str) -> None:
    """Add CSS to show an element only on mobile.
    
    Args:
        element_class: CSS class of element to show
    """
    st.markdown(f"""
    <style>
        @media (min-width: 641px) {{
            .{element_class} {{
                display: none;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)


# =============================================================================
# RESPONSIVE SIDEBAR
# =============================================================================

def responsive_sidebar(
    collapsed_default: bool = False,
) -> None:
    """Configure responsive sidebar behavior.
    
    Args:
        collapsed_default: Start with sidebar collapsed
    """
    state = "collapsed" if collapsed_default else "expanded"
    
    st.markdown(f"""
    <style>
        [data-testid="stSidebar"] {{
            transition: width 0.3s ease;
        }}
        
        @media (max-width: 640px) {{
            [data-testid="stSidebar"] {{
                width: 100% !important;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)


# =============================================================================
# RESPONSIVE TABLES
# =============================================================================

def responsive_table(
    max_height: str = "400px",
    hide_header_mobile: bool = False,
) -> None:
    """Configure responsive table behavior.
    
    Args:
        max_height: Maximum height of table
        hide_header_mobile: Hide header on mobile
    """
    css = f"""
    <style>
        .responsive-table {{
            max-height: {max_height};
            overflow-y: auto;
        }}
        
        .responsive-table table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .responsive-table th,
        .responsive-table td {{
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--color-border);
        }}
        
        .responsive-table th {{
            background: var(--color-surface);
            font-weight: 600;
            position: sticky;
            top: 0;
        }}
    """
    
    if hide_header_mobile:
        css += """
        @media (max-width: 640px) {
            .responsive-table th {
                display: none;
            }
        }
        """
    
    css += "</style>"
    st.markdown(css, unsafe_allow_html=True)


# =============================================================================
# RESPONSIVE CHARTS
# =============================================================================

def responsive_chart(
    height_mobile: int = 250,
    height_tablet: int = 350,
    height_desktop: int = 450,
) -> Dict[str, int]:
    """Get responsive chart height based on viewport.
    
    Note: Streamlit doesn't support dynamic viewport detection.
    This returns desktop height; implement JS for dynamic behavior.
    
    Args:
        height_mobile: Height for mobile
        height_tablet: Height for tablet
        height_desktop: Height for desktop
    
    Returns:
        Dictionary with viewport heights
    """
    return {
        "mobile": height_mobile,
        "tablet": height_tablet,
        "desktop": height_desktop,
    }


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "Breakpoints",
    "ColumnConfig",
    "responsive_columns",
    "metrics_row",
    "responsive_grid",
    "inject_responsive_css",
    "responsive_container",
    "hide_on_mobile",
    "show_on_mobile_only",
    "responsive_sidebar",
    "responsive_table",
    "responsive_chart",
]
