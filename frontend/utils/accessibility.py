"""Accessibility utilities for AI-QOS.

This module provides accessibility helpers for creating
WCAG 2.1 AA compliant components.
"""
from typing import Optional, List, Dict, Any
import streamlit as st


# =============================================================================
# ACCESSIBILITY HELPERS
# =============================================================================

def aria_label(text: str) -> str:
    """Generate an ARIA label from text.
    
    Args:
        text: Text to convert to ARIA label
    
    Returns:
        ARIA label string
    """
    return text.lower().replace(" ", "-").replace("_", "-")


def described_by(label_id: str) -> Dict[str, str]:
    """Generate described-by ARIA attribute.
    
    Args:
        label_id: ID of the describing element
    
    Returns:
        Dictionary with aria-describedby attribute
    """
    return {"aria-describedby": label_id}


def labeled_by(label_id: str) -> Dict[str, str]:
    """Generate labeled-by ARIA attribute.
    
    Args:
        label_id: ID of the label element
    
    Returns:
        Dictionary with aria-labelledby attribute
    """
    return {"aria-labelledby": label_id}


# =============================================================================
# KEYBOARD NAVIGATION
# =============================================================================

def keyboard_shortcut(
    key: str,
    action: str,
    description: str,
) -> None:
    """Document a keyboard shortcut.
    
    Args:
        key: Keyboard key (e.g., "Ctrl+S")
        action: Action description
        description: Full description
    """
    st.markdown(f"""
    <div class="keyboard-shortcut" aria-label="{action}">
        <kbd>{key}</kbd>
        <span class="shortcut-desc">{description}</span>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# SKIP LINKS
# =============================================================================

def skip_link(target_id: str, text: str = "Skip to main content") -> None:
    """Generate a skip link for keyboard users.
    
    Args:
        target_id: ID of the main content element
        text: Link text
    """
    st.markdown(f"""
    <a href="#{target_id}" class="skip-link" style="
        position: absolute;
        left: -9999px;
        top: auto;
        width: 1px;
        height: 1px;
        overflow: hidden;
    " onfocus="this.style.position='fixed'; this.style.left='10px'; this.style.top='10px'; this.style.width='auto'; this.style.height='auto'; this.style.zIndex='9999';">
        {text}
    </a>
    """, unsafe_allow_html=True)


# =============================================================================
# LIVE REGIONS (FOR DYNAMIC CONTENT)
# =============================================================================

def live_region(
    content: str,
    level: str = "polite",
    atomic: bool = True,
) -> None:
    """Generate an ARIA live region for screen readers.
    
    Args:
        content: Content to announce
        level: Announcement level ("polite", "assertive")
        atomic: Whether to announce entire region
    """
    st.markdown(f"""
    <div aria-live="{level}" aria-atomic="{str(atomic).lower()}" class="sr-only">
        {content}
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# SCREEN READER ONLY CONTENT
# =============================================================================

def sr_only(text: str, element: str = "span") -> None:
    """Generate screen-reader-only text.
    
    Args:
        text: Text for screen readers only
        element: HTML element to use
    """
    st.markdown(f"""
    <{element} class="sr-only" style="
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
    ">
        {text}
    </{element}>
    """, unsafe_allow_html=True)


# =============================================================================
# FOCUS MANAGEMENT
# =============================================================================

def focus_element(element_id: str) -> None:
    """Generate JavaScript to focus an element.
    
    Args:
        element_id: ID of element to focus
    """
    st.markdown(f"""
    <script>
        setTimeout(() => {{
            const element = document.getElementById('{element_id}');
            if (element) element.focus();
        }}, 100);
    </script>
    """, unsafe_allow_html=True)


# =============================================================================
# ACCESSIBLE ICON BUTTONS
# =============================================================================

def icon_button(
    icon: str,
    label: str,
    key: str = None,
    help: str = None,
) -> bool:
    """Create an accessible icon button.
    
    Args:
        icon: Icon emoji
        label: Accessible label (shown to screen readers)
        key: Streamlit key
        help: Tooltip text
    
    Returns:
        True if button clicked
    """
    # Use st.button with accessible label
    button_label = f"{icon} {label}"
    help_text = help or f"Click to {label.lower()}"
    
    return st.button(
        button_label,
        key=key,
        help=help_text,
    )


# =============================================================================
# ACCESSIBLE TABS
# =============================================================================

def accessible_tabs(
    tabs: List[str],
    key: str = "tabs",
) -> str:
    """Create accessible tabs with proper ARIA attributes.
    
    Args:
        tabs: List of tab labels
        key: Session state key
    
    Returns:
        Selected tab label
    """
    return st.tabs(tabs)


# =============================================================================
# ACCESSIBLE EXPANDER
# =============================================================================

def accessible_expander(
    label: str,
    content: str,
    help: str = None,
) -> None:
    """Create an accessible expander.
    
    Args:
        label: Expander label
        content: Content to show when expanded
        help: Optional help text
    """
    with st.expander(label, help=help):
        st.markdown(content)


# =============================================================================
# CONTRAST CHECKER
# =============================================================================

def check_contrast(
    foreground: str,
    background: str,
) -> Dict[str, Any]:
    """Check color contrast ratio for WCAG compliance.
    
    Args:
        foreground: Foreground color hex
        background: Background color hex
    
    Returns:
        Dictionary with contrast info
    """
    def hex_to_rgb(hex_color: str) -> tuple:
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def get_luminance(rgb: tuple) -> float:
        def adjust(c):
            c = c / 255
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        return 0.2126 * adjust(rgb[0]) + 0.7152 * adjust(rgb[1]) + 0.0722 * adjust(rgb[2])
    
    fg_rgb = hex_to_rgb(foreground)
    bg_rgb = hex_to_rgb(background)
    
    l1 = get_luminance(fg_rgb)
    l2 = get_luminance(bg_rgb)
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    contrast_ratio = (lighter + 0.05) / (darker + 0.05)
    
    return {
        "ratio": round(contrast_ratio, 2),
        "aa_normal": contrast_ratio >= 4.5,
        "aa_large": contrast_ratio >= 3.0,
        "aaa_normal": contrast_ratio >= 7.0,
        "aaa_large": contrast_ratio >= 4.5,
    }


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "aria_label",
    "described_by",
    "labeled_by",
    "keyboard_shortcut",
    "skip_link",
    "live_region",
    "sr_only",
    "focus_element",
    "icon_button",
    "accessible_tabs",
    "accessible_expander",
    "check_contrast",
]
