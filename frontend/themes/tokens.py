"""Design System Tokens for AI-QOS Enterprise UI.

This module provides centralized design tokens for the entire application.
All colors, spacing, typography, and other design values should be
referenced from this module to ensure consistency.

Usage:
    from frontend.themes.tokens import (
        COLORS, SPACING, TYPOGRAPHY, 
        glass_card, status_badge, button
    )
"""
from typing import Dict, Any, Callable
from dataclasses import dataclass
from enum import Enum


# =============================================================================
# COLOR TOKENS
# =============================================================================

class Colors:
    """Color palette tokens."""
    
    # Primary Colors
    PRIMARY = "#6366F1"
    PRIMARY_LIGHT = "#818CF8"
    PRIMARY_DARK = "#4F46E5"
    PRIMARY_RGB = "99, 102, 241"
    
    # Secondary Colors
    SECONDARY = "#22D3EE"
    SECONDARY_LIGHT = "#67E8F9"
    SECONDARY_DARK = "#06B6D4"
    SECONDARY_RGB = "34, 211, 238"
    
    # Accent Colors
    ACCENT = "#F472B6"
    ACCENT_RGB = "244, 114, 182"
    
    # Semantic Colors
    SUCCESS = "#10B981"
    SUCCESS_RGB = "16, 185, 129"
    WARNING = "#F59E0B"
    WARNING_RGB = "245, 158, 11"
    ERROR = "#EF4444"
    ERROR_RGB = "239, 68, 68"
    INFO = "#3B82F6"
    INFO_RGB = "59, 130, 246"
    
    # Background Colors
    BACKGROUND = "#0F0F23"
    BACKGROUND_ALT = "#1A1A2E"
    SURFACE = "#1E1E3F"
    SURFACE_HOVER = "#2A2A4A"
    SURFACE_RGB = "30, 30, 63"
    
    # Border Colors
    BORDER = "#334155"
    BORDER_LIGHT = "#475569"
    BORDER_RGB = "51, 65, 85"
    
    # Text Colors
    TEXT_PRIMARY = "#F1F5F9"
    TEXT_SECONDARY = "#94A3B8"
    TEXT_MUTED = "#64748B"
    TEXT_DISABLED = "#475569"
    
    # Glass Colors (for glassmorphism)
    GLASS = f"rgba({SURFACE_RGB}, 0.8)"
    GLASS_LIGHT = f"rgba({SURFACE_RGB}, 0.6)"
    GLASS_BORDER = f"rgba({PRIMARY_RGB}, 0.2)"
    GLASS_BORDER_HOVER = f"rgba({PRIMARY_RGB}, 0.4)"
    
    # Status Colors (mapped)
    STATUS_COLORS: Dict[str, str] = {
        "success": SUCCESS,
        "completed": SUCCESS,
        "passed": SUCCESS,
        "running": PRIMARY,
        "active": PRIMARY,
        "info": INFO,
        "warning": WARNING,
        "paused": WARNING,
        "pending": TEXT_MUTED,
        "idle": TEXT_MUTED,
        "error": ERROR,
        "failed": ERROR,
    }
    
    # Priority Colors
    PRIORITY_COLORS: Dict[str, str] = {
        "critical": ERROR,
        "high": WARNING,
        "medium": PRIMARY,
        "low": SUCCESS,
    }


COLORS = Colors()


# =============================================================================
# TYPOGRAPHY TOKENS
# =============================================================================

class Typography:
    """Typography tokens."""
    
    # Font Family
    FONT_FAMILY = "Inter, -apple-system, BlinkMacSystemFont, sans-serif"
    FONT_MONO = "'JetBrains Mono', 'Fira Code', monospace"
    
    # Font Sizes
    FONT_SIZE_XS = "0.625rem"   # 10px
    FONT_SIZE_SM = "0.75rem"    # 12px
    FONT_SIZE_BASE = "0.875rem"  # 14px
    FONT_SIZE_MD = "1rem"       # 16px
    FONT_SIZE_LG = "1.125rem"   # 18px
    FONT_SIZE_XL = "1.25rem"    # 20px
    FONT_SIZE_2XL = "1.5rem"    # 24px
    FONT_SIZE_3XL = "1.875rem"  # 30px
    FONT_SIZE_4XL = "2.25rem"   # 36px
    
    # Font Weights
    FONT_WEIGHT_LIGHT = 300
    FONT_WEIGHT_NORMAL = 400
    FONT_WEIGHT_MEDIUM = 500
    FONT_WEIGHT_SEMIBOLD = 600
    FONT_WEIGHT_BOLD = 700
    
    # Line Heights
    LINE_HEIGHT_TIGHT = 1.25
    LINE_HEIGHT_NORMAL = 1.5
    LINE_HEIGHT_LOOSE = 1.75
    
    # Letter Spacing
    LETTER_TIGHT = "-0.025em"
    LETTER_NORMAL = "0"
    LETTER_WIDE = "0.025em"
    LETTER_WIDER = "0.05em"


TYPOGRAPHY = Typography()


# =============================================================================
# SPACING TOKENS
# =============================================================================

class Spacing:
    """Spacing tokens."""
    
    # Base spacing unit: 4px
    UNIT = 4
    
    # Spacing scale
    PX_0 = "0px"
    PX_1 = "1px"
    PX_2 = "2px"
    PX_3 = "3px"
    PX_4 = "4px"
    
    SPACE_1 = "0.25rem"   # 4px
    SPACE_2 = "0.5rem"    # 8px
    SPACE_3 = "0.75rem"   # 12px
    SPACE_4 = "1rem"      # 16px
    SPACE_5 = "1.25rem"   # 20px
    SPACE_6 = "1.5rem"    # 24px
    SPACE_8 = "2rem"      # 32px
    SPACE_10 = "2.5rem"   # 40px
    SPACE_12 = "3rem"     # 48px
    SPACE_16 = "4rem"     # 64px
    SPACE_20 = "5rem"     # 80px
    
    # Common padding combinations
    PADDING_SM = SPACE_2
    PADDING_MD = SPACE_4
    PADDING_LG = SPACE_6
    PADDING_XL = SPACE_8
    
    # Common margin combinations
    MARGIN_SM = SPACE_2
    MARGIN_MD = SPACE_4
    MARGIN_LG = SPACE_6
    MARGIN_XL = SPACE_8


SPACING = Spacing()


# =============================================================================
# BORDER & RADIUS TOKENS
# =============================================================================

class Borders:
    """Border and radius tokens."""
    
    # Border widths
    WIDTH_NONE = "0"
    WIDTH_THIN = "1px"
    WIDTH_MEDIUM = "2px"
    WIDTH_THICK = "3px"
    
    # Border styles
    STYLE_SOLID = "solid"
    STYLE_DASHED = "dashed"
    STYLE_DOTTED = "dotted"
    
    # Radius
    RADIUS_NONE = "0"
    RADIUS_SM = "4px"
    RADIUS_MD = "8px"
    RADIUS_LG = "12px"
    RADIUS_XL = "16px"
    RADIUS_2XL = "20px"
    RADIUS_FULL = "9999px"
    
    # Common radius
    RADIUS_CARD = RADIUS_LG
    RADIUS_BUTTON = RADIUS_MD
    RADIUS_INPUT = RADIUS_MD
    RADIUS_BADGE = RADIUS_FULL
    RADIUS_PILL = RADIUS_FULL


BORDERS = Borders()


# =============================================================================
# SHADOW TOKENS
# =============================================================================

class Shadows:
    """Shadow tokens."""
    
    # Basic shadows
    NONE = "none"
    SM = "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
    MD = "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)"
    LG = "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)"
    XL = "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)"
    
    # Card shadows
    CARD = "0 4px 20px rgba(0, 0, 0, 0.4)"
    CARD_HOVER = "0 8px 30px rgba(99, 102, 241, 0.15)"
    
    # Glow shadows
    GLOW_PRIMARY = "0 0 20px rgba(99, 102, 241, 0.3)"
    GLOW_SUCCESS = "0 0 20px rgba(16, 185, 129, 0.3)"
    GLOW_ERROR = "0 0 20px rgba(239, 68, 68, 0.3)"
    
    # Inner shadows
    INNER_SM = "inset 0 1px 2px 0 rgba(0, 0, 0, 0.05)"
    INNER_LG = "inset 0 2px 4px 0 rgba(0, 0, 0, 0.1)"


SHADOWS = Shadows()


# =============================================================================
# ANIMATION TOKENS
# =============================================================================

class Animations:
    """Animation tokens."""
    
    # Durations
    DURATION_INSTANT = "0ms"
    DURATION_FAST = "100ms"
    DURATION_NORMAL = "200ms"
    DURATION_SLOW = "300ms"
    DURATION_SLOWER = "500ms"
    
    # Easing
    EASE_LINEAR = "linear"
    EASE_IN = "ease-in"
    EASE_OUT = "ease-out"
    EASE_IN_OUT = "ease-in-out"
    EASE_BOUNCE = "cubic-bezier(0.68, -0.55, 0.265, 1.55)"
    EASE_STEP_START = "step-start"
    
    # Animation names
    ANIM_PULSE = "pulse"
    ANIM_GLOW = "glow"
    ANIM_SLIDE_IN = "slideIn"
    ANIM_FADE_IN = "fadeIn"
    ANIM_BOUNCE = "bounce"
    ANIM_SPIN = "spin"
    ANIM_SHIMMER = "shimmer"
    ANIM_BLINK = "blink"
    ANIM_FLOAT = "float"
    ANIM_FLOW = "flow"
    ANIM_CLICK = "click"
    ANIM_TYPING = "typing"
    ANIM_SCROLL = "scroll"
    
    # Full animation strings
    PULSE = "pulse 2s infinite ease-in-out"
    GLOW = "glow 2s infinite ease-in-out"
    SLIDE_IN = "slideIn 300ms ease-out"
    FADE_IN = "fadeIn 200ms ease-out"
    BOUNCE = "bounce 1.4s infinite ease-in-out"
    SPIN = "spin 1s linear infinite"
    SHIMMER = "shimmer 2s infinite ease-in-out"
    BLINK = "blink 1s infinite step-start"
    FLOAT = "float 3s infinite ease-in-out"
    
    # Keyframes CSS
    KEYFRAMES = """
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px rgba(99, 102, 241, 0.5); }
        50% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.8); }
    }
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    """


ANIMATIONS = Animations()


# =============================================================================
# Z-INDEX TOKENS
# =============================================================================

class ZIndex:
    """Z-index tokens."""
    
    BASE = 0
    DROPDOWN = 100
    STICKY = 200
    FIXED = 300
    MODAL_BACKDROP = 400
    MODAL = 500
    POPOVER = 600
    TOOLTIP = 700
    TOAST = 800


Z_INDEX = ZIndex()


# =============================================================================
# BREAKPOINT TOKENS
# =============================================================================

class Breakpoints:
    """Breakpoint tokens."""
    
    SM = "640px"
    MD = "768px"
    LG = "1024px"
    XL = "1280px"
    XXL = "1536px"


BREAKPOINTS = Breakpoints()


# =============================================================================
# LAYOUT TOKENS
# =============================================================================

class Layout:
    """Layout tokens."""
    
    # Container widths
    CONTAINER_SM = "640px"
    CONTAINER_MD = "768px"
    CONTAINER_LG = "1024px"
    CONTAINER_XL = "1280px"
    CONTAINER_2XL = "1536px"
    
    # Sidebar
    SIDEBAR_WIDTH = "280px"
    SIDEBAR_COLLAPSED = "64px"
    
    # Header
    HEADER_HEIGHT = "64px"
    
    # Content
    CONTENT_MAX_WIDTH = "1400px"


LAYOUT = Layout()


# =============================================================================
# COMPONENT STYLES
# =============================================================================

def _hex_to_rgb(hex_color: str) -> str:
    """Convert a hex color (#RRGGBB) to an 'r, g, b' string for rgba() usage."""
    h = hex_color.lstrip('#')
    return f"{int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}"


class ComponentStyles:
    """Pre-built component style strings."""

    # Card Styles
    @staticmethod
    def card(padding: str = SPACING.PADDING_LG) -> str:
        return f"""
            background: {COLORS.GLASS};
            border: {BORDERS.WIDTH_THIN} solid {COLORS.BORDER};
            border-radius: {BORDERS.RADIUS_CARD};
            padding: {padding};
            box-shadow: {SHADOWS.CARD};
            box-sizing: border-box;
            max-width: 100%;
            min-width: 0;
        """
    
    @staticmethod
    def card_hover() -> str:
        return f"""
            border-color: {COLORS.PRIMARY};
            box-shadow: {SHADOWS.CARD_HOVER};
            transform: translateY(-2px);
        """
    
    @staticmethod
    def glass_card(padding: str = SPACING.PADDING_LG) -> str:
        return f"""
            background: {COLORS.GLASS};
            border: {BORDERS.WIDTH_THIN} solid {COLORS.GLASS_BORDER};
            border-radius: {BORDERS.RADIUS_CARD};
            padding: {padding};
            backdrop-filter: blur(12px);
            box-sizing: border-box;
            max-width: 100%;
            min-width: 0;
        """

    @staticmethod
    def metric_card() -> str:
        return f"""
            background: linear-gradient(135deg, {COLORS.SURFACE} 0%, rgba({COLORS.PRIMARY_RGB}, 0.1) 100%);
            border: {BORDERS.WIDTH_THIN} solid {COLORS.BORDER};
            border-radius: {BORDERS.RADIUS_CARD};
            padding: {SPACING.PADDING_LG};
            text-align: center;
            box-sizing: border-box;
            max-width: 100%;
            min-width: 0;
        """
    
    # Badge Styles
    @staticmethod
    def badge(status: str) -> str:
        color = COLORS.STATUS_COLORS.get(status, COLORS.TEXT_MUTED)
        return f"""
            display: inline-flex;
            align-items: center;
            gap: {SPACING.SPACE_1};
            padding: {SPACING.SPACE_1} {SPACING.SPACE_3};
            background: rgba({_hex_to_rgb(color)}, 0.2);
            color: {color};
            border-radius: {BORDERS.RADIUS_BADGE};
            font-size: {TYPOGRAPHY.FONT_SIZE_SM};
            font-weight: {TYPOGRAPHY.FONT_WEIGHT_MEDIUM};
            white-space: nowrap;
        """
    
    @staticmethod
    def badge_success() -> str:
        return f"""
            background: rgba({COLORS.SUCCESS_RGB}, 0.2);
            color: {COLORS.SUCCESS};
            border-radius: {BORDERS.RADIUS_BADGE};
            padding: {SPACING.SPACE_1} {SPACING.SPACE_3};
            font-size: {TYPOGRAPHY.FONT_SIZE_SM};
        """
    
    @staticmethod
    def badge_error() -> str:
        return f"""
            background: rgba({COLORS.ERROR_RGB}, 0.2);
            color: {COLORS.ERROR};
            border-radius: {BORDERS.RADIUS_BADGE};
            padding: {SPACING.SPACE_1} {SPACING.SPACE_3};
            font-size: {TYPOGRAPHY.FONT_SIZE_SM};
        """
    
    @staticmethod
    def badge_warning() -> str:
        return f"""
            background: rgba({COLORS.WARNING_RGB}, 0.2);
            color: {COLORS.WARNING};
            border-radius: {BORDERS.RADIUS_BADGE};
            padding: {SPACING.SPACE_1} {SPACING.SPACE_3};
            font-size: {TYPOGRAPHY.FONT_SIZE_SM};
        """
    
    @staticmethod
    def badge_info() -> str:
        return f"""
            background: rgba({COLORS.PRIMARY_RGB}, 0.2);
            color: {COLORS.PRIMARY};
            border-radius: {BORDERS.RADIUS_BADGE};
            padding: {SPACING.SPACE_1} {SPACING.SPACE_3};
            font-size: {TYPOGRAPHY.FONT_SIZE_SM};
        """
    
    # Progress Bar
    @staticmethod
    def progress_bar(height: str = "6px") -> str:
        return f"""
            height: {height};
            background: {COLORS.BORDER};
            border-radius: {BORDERS.RADIUS_FULL};
            overflow: hidden;
        """
    
    @staticmethod
    def progress_fill(color: str = COLORS.PRIMARY) -> str:
        return f"""
            height: 100%;
            background: linear-gradient(90deg, {color}, {color}cc);
            border-radius: {BORDERS.RADIUS_FULL};
            transition: width {ANIMATIONS.DURATION_SLOWER} {ANIMATIONS.EASE_OUT};
        """
    
    # Button Base
    @staticmethod
    def button_base() -> str:
        return f"""
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: {SPACING.SPACE_2};
            padding: {SPACING.SPACE_2} {SPACING.SPACE_4};
            border-radius: {BORDERS.RADIUS_BUTTON};
            font-size: {TYPOGRAPHY.FONT_SIZE_BASE};
            font-weight: {TYPOGRAPHY.FONT_WEIGHT_MEDIUM};
            cursor: pointer;
            transition: all {ANIMATIONS.DURATION_NORMAL} {ANIMATIONS.EASE_OUT};
        """
    
    @staticmethod
    def button_primary() -> str:
        return f"""
            {ComponentStyles.button_base()}
            background: {COLORS.PRIMARY};
            color: white;
            border: none;
        """
    
    @staticmethod
    def button_secondary() -> str:
        return f"""
            {ComponentStyles.button_base()}
            background: transparent;
            color: {COLORS.TEXT_PRIMARY};
            border: {BORDERS.WIDTH_THIN} solid {COLORS.BORDER};
        """
    
    # Input Base
    @staticmethod
    def input_base() -> str:
        return f"""
            background: {COLORS.SURFACE};
            border: {BORDERS.WIDTH_THIN} solid {COLORS.BORDER};
            border-radius: {BORDERS.RADIUS_INPUT};
            padding: {SPACING.SPACE_2} {SPACING.SPACE_3};
            color: {COLORS.TEXT_PRIMARY};
            font-size: {TYPOGRAPHY.FONT_SIZE_BASE};
            transition: border-color {ANIMATIONS.DURATION_NORMAL} {ANIMATIONS.EASE_OUT};
        """
    
    # Panel
    @staticmethod
    def panel() -> str:
        return f"""
            background: {COLORS.GLASS_LIGHT};
            border: {BORDERS.WIDTH_THIN} solid {COLORS.GLASS_BORDER};
            border-radius: {BORDERS.RADIUS_LG};
            padding: {SPACING.PADDING_LG};
        """
    
    # Header
    @staticmethod
    def header_gradient() -> str:
        return f"""
            background: linear-gradient(135deg, {COLORS.SURFACE} 0%, rgba({COLORS.PRIMARY_RGB}, 0.15) 100%);
            border: {BORDERS.WIDTH_THIN} solid {COLORS.GLASS_BORDER};
            border-radius: {BORDERS.RADIUS_XL};
            padding: {SPACING.PADDING_LG};
        """


STYLES = ComponentStyles()


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_status_color(status: str) -> str:
    """Get color for a status string."""
    return COLORS.STATUS_COLORS.get(status.lower(), COLORS.TEXT_MUTED)


def get_priority_color(priority: str) -> str:
    """Get color for a priority string."""
    return COLORS.PRIORITY_COLORS.get(priority.lower(), COLORS.TEXT_MUTED)


def get_health_color(health: float) -> str:
    """Get color based on health percentage."""
    if health >= 80:
        return COLORS.SUCCESS
    elif health >= 50:
        return COLORS.WARNING
    else:
        return COLORS.ERROR


def get_confidence_color(confidence: int) -> str:
    """Get color based on confidence percentage."""
    if confidence >= 80:
        return COLORS.SUCCESS
    elif confidence >= 60:
        return COLORS.WARNING
    else:
        return COLORS.ERROR


def glass_background(opacity: float = 0.8) -> str:
    """Generate glass background with specified opacity."""
    return f"background: rgba({COLORS.SURFACE_RGB}, {opacity});"


def border_color(color: str = COLORS.PRIMARY, opacity: float = 0.2) -> str:
    """Generate glass-like border color."""
    return f"border-color: rgba({_hex_to_rgb(color)}, {opacity});"


# =============================================================================
# DESIGN TOKENS SUMMARY
# =============================================================================

DESIGN_TOKENS = {
    "colors": {
        "primary": COLORS.PRIMARY,
        "secondary": COLORS.SECONDARY,
        "success": COLORS.SUCCESS,
        "warning": COLORS.WARNING,
        "error": COLORS.ERROR,
        "background": COLORS.BACKGROUND,
        "surface": COLORS.SURFACE,
        "text_primary": COLORS.TEXT_PRIMARY,
        "text_secondary": COLORS.TEXT_SECONDARY,
        "text_muted": COLORS.TEXT_MUTED,
        "border": COLORS.BORDER,
        "glass": COLORS.GLASS,
    },
    "spacing": {
        "unit": SPACING.UNIT,
        "sm": SPACING.SPACE_2,
        "md": SPACING.SPACE_4,
        "lg": SPACING.SPACE_6,
        "xl": SPACING.SPACE_8,
    },
    "typography": {
        "font_family": TYPOGRAPHY.FONT_FAMILY,
        "font_size_sm": TYPOGRAPHY.FONT_SIZE_SM,
        "font_size_base": TYPOGRAPHY.FONT_SIZE_BASE,
        "font_size_lg": TYPOGRAPHY.FONT_SIZE_LG,
        "font_size_xl": TYPOGRAPHY.FONT_SIZE_XL,
    },
    "borders": {
        "radius_sm": BORDERS.RADIUS_SM,
        "radius_md": BORDERS.RADIUS_MD,
        "radius_lg": BORDERS.RADIUS_LG,
        "radius_full": BORDERS.RADIUS_FULL,
    },
    "shadows": {
        "card": SHADOWS.CARD,
        "card_hover": SHADOWS.CARD_HOVER,
    },
    "animations": {
        "pulse": ANIMATIONS.PULSE,
        "glow": ANIMATIONS.GLOW,
        "slide_in": ANIMATIONS.SLIDE_IN,
    },
}
