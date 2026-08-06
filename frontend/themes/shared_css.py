"""Shared CSS for AI-QOS Design System.

This module provides centralized CSS for the entire application.
Import and use via st.markdown(shared_css(), unsafe_allow_html=True)
"""
from frontend.themes.tokens import ANIMATIONS, TYPOGRAPHY, SPACING, BORDERS, SHADOWS, COLORS

# Keyframe animations (must be injected via st.markdown)
ANIMATION_KEYFRAMES = f"""
{ANIMATIONS.KEYFRAMES}
"""

# Full shared CSS with design tokens
SHARED_CSS = f"""
/* AI-QOS Design System - Shared CSS */
/* Generated from design tokens */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {{
    /* Color Tokens */
    --color-primary: {COLORS.PRIMARY};
    --color-primary-light: {COLORS.PRIMARY_LIGHT};
    --color-primary-dark: {COLORS.PRIMARY_DARK};
    --color-secondary: {COLORS.SECONDARY};
    --color-success: {COLORS.SUCCESS};
    --color-warning: {COLORS.WARNING};
    --color-error: {COLORS.ERROR};
    --color-info: {COLORS.INFO};
    
    --color-background: {COLORS.BACKGROUND};
    --color-surface: {COLORS.SURFACE};
    --color-surface-hover: {COLORS.SURFACE_HOVER};
    
    --color-border: {COLORS.BORDER};
    --color-border-light: {COLORS.BORDER_LIGHT};
    
    --color-text-primary: {COLORS.TEXT_PRIMARY};
    --color-text-secondary: {COLORS.TEXT_SECONDARY};
    --color-text-muted: {COLORS.TEXT_MUTED};
    
    /* Glass Tokens */
    --glass: {COLORS.GLASS};
    --glass-light: {COLORS.GLASS_LIGHT};
    --glass-border: {COLORS.GLASS_BORDER};
    
    /* Typography Tokens */
    --font-family: {TYPOGRAPHY.FONT_FAMILY};
    --font-size-xs: {TYPOGRAPHY.FONT_SIZE_XS};
    --font-size-sm: {TYPOGRAPHY.FONT_SIZE_SM};
    --font-size-base: {TYPOGRAPHY.FONT_SIZE_BASE};
    --font-size-md: {TYPOGRAPHY.FONT_SIZE_MD};
    --font-size-lg: {TYPOGRAPHY.FONT_SIZE_LG};
    --font-size-xl: {TYPOGRAPHY.FONT_SIZE_XL};
    --font-size-2xl: {TYPOGRAPHY.FONT_SIZE_2XL};
    --font-size-3xl: {TYPOGRAPHY.FONT_SIZE_3XL};
    
    /* Spacing Tokens */
    --space-1: {SPACING.SPACE_1};
    --space-2: {SPACING.SPACE_2};
    --space-3: {SPACING.SPACE_3};
    --space-4: {SPACING.SPACE_4};
    --space-5: {SPACING.SPACE_5};
    --space-6: {SPACING.SPACE_6};
    --space-8: {SPACING.SPACE_8};
    
    /* Border Tokens */
    --radius-sm: {BORDERS.RADIUS_SM};
    --radius-md: {BORDERS.RADIUS_MD};
    --radius-lg: {BORDERS.RADIUS_LG};
    --radius-xl: {BORDERS.RADIUS_XL};
    --radius-full: {BORDERS.RADIUS_FULL};
    
    /* Shadow Tokens */
    --shadow-card: {SHADOWS.CARD};
    --shadow-card-hover: {SHADOWS.CARD_HOVER};
    --shadow-glow: {SHADOWS.GLOW_PRIMARY};
}}

/* Global Styles */
* {{
    font-family: var(--font-family);
}}

.stApp {{
    background: linear-gradient(135deg, {COLORS.BACKGROUND} 0%, {COLORS.BACKGROUND_ALT} 100%);
}}

/* Card Components */
.aiqos-card {{
    background: var(--glass);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-6);
    box-shadow: var(--shadow-card);
    transition: all {ANIMATIONS.DURATION_NORMAL} ease;
}}

.aiqos-card:hover {{
    border-color: var(--color-primary);
    box-shadow: var(--shadow-card-hover);
    transform: translateY(-2px);
}}

.aiqos-card-glass {{
    background: var(--glass);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-lg);
    padding: var(--space-6);
    backdrop-filter: blur(12px);
}}

.aiqos-metric-card {{
    background: linear-gradient(135deg, var(--color-surface) 0%, rgba(99, 102, 241, 0.1) 100%);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-6);
    text-align: center;
}}

/* Badge Components */
.aiqos-badge {{
    display: inline-flex;
    align-items: center;
    gap: var(--space-1);
    padding: var(--space-1) var(--space-3);
    border-radius: var(--radius-full);
    font-size: var(--font-size-sm);
    font-weight: 500;
}}

.aiqos-badge-success {{
    background: rgba({COLORS.SUCCESS_RGB}, 0.2);
    color: {COLORS.SUCCESS};
}}

.aiqos-badge-warning {{
    background: rgba({COLORS.WARNING_RGB}, 0.2);
    color: {COLORS.WARNING};
}}

.aiqos-badge-error {{
    background: rgba({COLORS.ERROR_RGB}, 0.2);
    color: {COLORS.ERROR};
}}

.aiqos-badge-info {{
    background: rgba({COLORS.PRIMARY_RGB}, 0.2);
    color: {COLORS.PRIMARY};
}}

/* Button Components */
.aiqos-button {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-2);
    padding: var(--space-2) var(--space-4);
    border-radius: var(--radius-md);
    font-size: var(--font-size-base);
    font-weight: 500;
    cursor: pointer;
    transition: all {ANIMATIONS.DURATION_NORMAL} ease;
}}

.aiqos-button-primary {{
    background: var(--color-primary);
    color: white;
    border: none;
}}

.aiqos-button-secondary {{
    background: transparent;
    color: var(--color-text-primary);
    border: 1px solid var(--color-border);
}}

.aiqos-button-success {{
    background: var(--color-success);
    color: white;
    border: none;
}}

.aiqos-button-danger {{
    background: var(--color-error);
    color: white;
    border: none;
}}

/* Header Components */
.aiqos-header {{
    font-size: var(--font-size-2xl);
    font-weight: 600;
    color: var(--color-text-primary);
    margin-bottom: var(--space-4);
}}

.aiqos-subheader {{
    font-size: var(--font-size-lg);
    font-weight: 500;
    color: var(--color-text-secondary);
}}

/* Input Components */
.aiqos-input {{
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-2) var(--space-3);
    color: var(--color-text-primary);
    font-size: var(--font-size-base);
}}

.aiqos-input:focus {{
    border-color: var(--color-primary);
    outline: none;
}}

/* Panel Components */
.aiqos-panel {{
    background: var(--glass-light);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-lg);
    padding: var(--space-6);
}}

/* Progress Bar */
.aiqos-progress {{
    height: 6px;
    background: var(--color-border);
    border-radius: var(--radius-full);
    overflow: hidden;
}}

.aiqos-progress-fill {{
    height: 100%;
    background: linear-gradient(90deg, var(--color-primary), var(--color-primary-dark));
    border-radius: var(--radius-full);
    transition: width {ANIMATIONS.DURATION_SLOWER} ease;
}}

/* Timeline */
.aiqos-timeline-item {{
    position: relative;
    padding-left: var(--space-8);
    padding-bottom: var(--space-4);
}}

.aiqos-timeline-item::before {{
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 2px;
    background: var(--color-border);
}}

.aiqos-timeline-dot {{
    position: absolute;
    left: -4px;
    top: 0;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--color-primary);
}}

/* Streamlit Overrides */
div[data-testid="stSidebar"] {{
    background: rgba(15, 15, 35, 0.95);
    border-right: 1px solid var(--color-border);
}}

div[data-testid="stMetric"] {{
    background: var(--color-surface);
    padding: var(--space-4);
    border-radius: var(--radius-lg);
    border: 1px solid var(--color-border);
}}

div[data-testid="stMetricLabel"] {{
    color: var(--color-text-secondary);
}}

div[data-testid="stMetricValue"] {{
    color: var(--color-primary);
    font-weight: 600;
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: var(--space-2);
    background: var(--color-surface);
    padding: var(--space-2);
    border-radius: var(--radius-lg);
}}

.stTabs [data-baseweb="tab"] {{
    border-radius: var(--radius-md);
    padding: var(--space-3) var(--space-6);
}}

.stTabs button[aria-selected="true"] {{
    background: var(--color-primary) !important;
    color: white !important;
}}

/* Scrollbar */
::-webkit-scrollbar {{
    width: 8px;
    height: 8px;
}}

::-webkit-scrollbar-track {{
    background: var(--color-surface);
    border-radius: 4px;
}}

::-webkit-scrollbar-thumb {{
    background: var(--color-border);
    border-radius: 4px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: var(--color-text-muted);
}}

/* Animation Classes */
.animate-pulse {{
    animation: pulse 2s infinite ease-in-out;
}}

.animate-glow {{
    animation: glow 2s infinite ease-in-out;
}}

.animate-slide-in {{
    animation: slideIn {ANIMATIONS.DURATION_SLOW} ease-out;
}}

.animate-fade-in {{
    animation: fadeIn {ANIMATIONS.DURATION_NORMAL} ease-out;
}}

.animate-spin {{
    animation: spin 1s linear infinite;
}}
"""

# Just the CSS variables for inline use
CSS_VARIABLES = f"""
--color-primary: {COLORS.PRIMARY};
--color-primary-light: {COLORS.PRIMARY_LIGHT};
--color-success: {COLORS.SUCCESS};
--color-warning: {COLORS.WARNING};
--color-error: {COLORS.ERROR};
--color-background: {COLORS.BACKGROUND};
--color-surface: {COLORS.SURFACE};
--color-text-primary: {COLORS.TEXT_PRIMARY};
--color-text-secondary: {COLORS.TEXT_SECONDARY};
--color-text-muted: {COLORS.TEXT_MUTED};
--color-border: {COLORS.BORDER};
--glass: {COLORS.GLASS};
--glass-border: {COLORS.GLASS_BORDER};
--radius-lg: {BORDERS.RADIUS_LG};
--radius-md: {BORDERS.RADIUS_MD};
--radius-full: {BORDERS.RADIUS_FULL};
"""


def get_shared_css() -> str:
    """Get the full shared CSS string."""
    return SHARED_CSS


def get_animation_keyframes() -> str:
    """Get the animation keyframes."""
    return ANIMATION_KEYFRAMES


def get_css_variables() -> str:
    """Get just the CSS variables for inline style use."""
    return CSS_VARIABLES
