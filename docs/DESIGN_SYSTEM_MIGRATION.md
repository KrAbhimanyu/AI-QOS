# AI-QOS Design System - Migration Guide

**Date:** August 6, 2026  
**Version:** 1.0.0  
**Status:** Ready for Migration

---

## Overview

This document describes the enterprise design system created for AI-QOS and provides a step-by-step guide for migrating existing components to use the centralized design tokens and shared components.

## Design System Architecture

```
frontend/
├── themes/
│   ├── __init__.py           # Exports all theme modules
│   ├── theme_config.py        # Streamlit theme configuration
│   ├── tokens.py              # Design tokens (colors, spacing, etc.)
│   └── shared_css.py          # Shared CSS with CSS variables
├── components/
│   ├── __init__.py            # Exports all shared components
│   ├── shared.py              # Shared UI components library
│   ├── core_components.py     # (To be migrated)
│   ├── agent_components.py    # (To be migrated)
│   └── ...                    # (Other components)
└── mock/                      # Mock data (already migrated)
```

---

## Design Tokens

### Color Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `COLORS.PRIMARY` | `#6366F1` | Primary actions, highlights |
| `COLORS.SECONDARY` | `#22D3EE` | Secondary accents |
| `COLORS.SUCCESS` | `#10B981` | Success states, passed tests |
| `COLORS.WARNING` | `#F59E0B` | Warning states, paused |
| `COLORS.ERROR` | `#EF4444` | Error states, failed tests |
| `COLORS.BACKGROUND` | `#0F0F23` | Page background |
| `COLORS.SURFACE` | `#1E1E3F` | Card/panel backgrounds |
| `COLORS.TEXT_PRIMARY` | `#F1F5F9` | Primary text |
| `COLORS.TEXT_SECONDARY` | `#94A3B8` | Secondary text |
| `COLORS.TEXT_MUTED` | `#64748B` | Muted/disabled text |
| `COLORS.BORDER` | `#334155` | Border colors |
| `COLORS.GLASS` | `rgba(30, 30, 63, 0.8)` | Glassmorphism background |
| `COLORS.GLASS_BORDER` | `rgba(99, 102, 241, 0.2)` | Glassmorphism border |

### Typography Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `TYPOGRAPHY.FONT_FAMILY` | `Inter, sans-serif` | Primary font |
| `TYPOGRAPHY.FONT_SIZE_SM` | `0.75rem` | Small text |
| `TYPOGRAPHY.FONT_SIZE_BASE` | `0.875rem` | Base text |
| `TYPOGRAPHY.FONT_SIZE_LG` | `1.125rem` | Large text |
| `TYPOGRAPHY.FONT_SIZE_XL` | `1.25rem` | Extra large text |
| `TYPOGRAPHY.FONT_SIZE_2XL` | `1.5rem` | Headers |

### Spacing Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `SPACING.SPACE_1` | `0.25rem` | Tight spacing |
| `SPACING.SPACE_2` | `0.5rem` | Small spacing |
| `SPACING.SPACE_3` | `0.75rem` | Medium-small |
| `SPACING.SPACE_4` | `1rem` | Medium spacing |
| `SPACING.SPACE_6` | `1.5rem` | Large spacing |
| `SPACING.SPACE_8` | `2rem` | Extra large |

### Border Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `BORDERS.RADIUS_SM` | `4px` | Small radius |
| `BORDERS.RADIUS_MD` | `8px` | Medium radius |
| `BORDERS.RADIUS_LG` | `12px` | Large radius (cards) |
| `BORDERS.RADIUS_FULL` | `9999px` | Full radius (badges) |

### Shadow Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `SHADOWS.CARD` | `0 4px 20px rgba(0, 0, 0, 0.4)` | Card shadow |
| `SHADOWS.CARD_HOVER` | `0 8px 30px rgba(99, 102, 241, 0.15)` | Hover shadow |
| `SHADOWS.GLOW_PRIMARY` | `0 0 20px rgba(99, 102, 241, 0.3)` | Primary glow |

---

## Migration Examples

### Before (Hardcoded Colors)

```python
# ❌ BAD - Hardcoded values
st.markdown(f"""
    <div style="
        background: rgba(30, 30, 63, 0.8);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        color: #F1F5F9;
    ">
        Content
    </div>
""", unsafe_allow_html=True)
```

### After (Using Design Tokens)

```python
# ✅ GOOD - Using tokens
from frontend.themes.tokens import COLORS, SPACING, BORDERS

st.markdown(f"""
    <div style="
        background: {COLORS.GLASS};
        border: {BORDERS.WIDTH_THIN} solid {COLORS.GLASS_BORDER};
        border-radius: {BORDERS.RADIUS_LG};
        padding: {SPACING.SPACE_6};
        color: {COLORS.TEXT_PRIMARY};
    ">
        Content
    </div>
""", unsafe_allow_html=True)
```

### Using Shared Components

```python
# ✅ BEST - Using shared components
from frontend.components.shared import card, badge, status_badge

# Instead of writing complex HTML, use:
card(
    title="Agent Status",
    content="Agent is running successfully",
    badge="Running",
    badge_type="success",
    icon="🤖"
)

# Status badges automatically color based on status:
status_badge("running", show_dot=True)  # Shows green dot
status_badge("failed", show_dot=True)  # Shows red dot
```

---

## Shared Components

### Available Components

| Component | Description | Usage |
|-----------|-------------|-------|
| `card()` | Styled card | `card(title, content, icon, badge)` |
| `metric_card()` | Metric display | `metric_card(title, value, trend)` |
| `glass_card()` | Glassmorphism card | `glass_card(content)` |
| `badge()` | Status badge | `badge(text, type)` |
| `status_badge()` | Auto-colored status | `status_badge(status)` |
| `priority_badge()` | Priority indicator | `priority_badge(priority)` |
| `progress_bar()` | Progress indicator | `progress_bar(value, max)` |
| `health_bar()` | Health percentage | `health_bar(health)` |
| `confidence_bar()` | Confidence level | `confidence_bar(confidence)` |
| `glass_panel()` | Glassmorphism panel | `glass_panel(title, content)` |
| `header()` | Page header | `header(title, subtitle, icon)` |
| `section_header()` | Section divider | `section_header(title, icon)` |
| `timeline_item()` | Timeline entry | `timeline_item(title, desc, status)` |
| `empty_state()` | Empty state | `empty_state(icon, title, desc)` |
| `notification()` | Toast message | `notification(message, type)` |
| `divider()` | Horizontal line | `divider()` |
| `spacer()` | Vertical space | `spacer(size)` |

---

## Helper Functions

### Status Colors

```python
from frontend.themes.tokens import get_status_color, get_health_color, get_confidence_color

# Get color based on status
color = get_status_color("running")   # Returns #6366F1
color = get_status_color("failed")     # Returns #EF4444
color = get_status_color("completed")  # Returns #10B981

# Get color based on percentage
health_color = get_health_color(95)     # Green (>80%)
health_color = get_health_color(60)    # Yellow (50-80%)
health_color = get_health_color(30)    # Red (<50%)

confidence_color = get_confidence_color(85)  # Green (>80%)
confidence_color = get_confidence_color(65) # Yellow (60-80%)
confidence_color = get_confidence_color(45)  # Red (<60%)
```

### Glass Background

```python
from frontend.themes.tokens import glass_background

# Generate glass background with custom opacity
bg = glass_background(0.8)   # background: rgba(30, 30, 63, 0.8);
bg = glass_background(0.6)   # background: rgba(30, 30, 63, 0.6);
```

---

## Migration Checklist

### Phase 1: Imports

- [ ] Add `from frontend.themes.tokens import COLORS, SPACING, BORDERS, etc.`
- [ ] Add `from frontend.components.shared import *` for shared components

### Phase 2: Replace Hardcoded Colors

| Old | New |
|-----|-----|
| `#6366F1` | `COLORS.PRIMARY` |
| `#10B981` | `COLORS.SUCCESS` |
| `#EF4444` | `COLORS.ERROR` |
| `#F59E0B` | `COLORS.WARNING` |
| `#F1F5F9` | `COLORS.TEXT_PRIMARY` |
| `#94A3B8` | `COLORS.TEXT_SECONDARY` |
| `#64748B` | `COLORS.TEXT_MUTED` |
| `#334155` | `COLORS.BORDER` |
| `#0F0F23` | `COLORS.BACKGROUND` |
| `#1E1E3F` | `COLORS.SURFACE` |
| `rgba(30, 30, 63, 0.8)` | `COLORS.GLASS` |
| `rgba(99, 102, 241, 0.2)` | `COLORS.GLASS_BORDER` |

### Phase 3: Replace Hardcoded Spacing

| Old | New |
|-----|-----|
| `0.25rem` | `SPACING.SPACE_1` |
| `0.5rem` | `SPACING.SPACE_2` |
| `0.75rem` | `SPACING.SPACE_3` |
| `1rem` | `SPACING.SPACE_4` |
| `1.5rem` | `SPACING.SPACE_6` |
| `2rem` | `SPACING.SPACE_8` |
| `1px` | `BORDERS.WIDTH_THIN` |

### Phase 4: Replace Hardcoded Radius

| Old | New |
|-----|-----|
| `4px` | `BORDERS.RADIUS_SM` |
| `8px` | `BORDERS.RADIUS_MD` |
| `12px` | `BORDERS.RADIUS_LG` |
| `16px` | `BORDERS.RADIUS_XL` |
| `9999px` | `BORDERS.RADIUS_FULL` |

### Phase 5: Replace Complex Components

Replace inline HTML cards with shared components:

```python
# Before
st.markdown(f"""
    <div style="background: {COLORS.GLASS}; border: ...; border-radius: {BORDERS.RADIUS_LG};">
        <h3>{title}</h3>
        <p>{content}</p>
    </div>
""", unsafe_allow_html=True)

# After
card(title=title, content=content, icon=icon)
```

---

## Animation Migration

### Before (Inline Keyframes)

```python
# ❌ BAD - Duplicate keyframe definitions
st.markdown("""
    <style>
        @keyframes glow {
            0%, 100% { box-shadow: 0 0 5px rgba(99, 102, 241, 0.5); }
            50% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.8); }
        }
    </style>
""", unsafe_allow_html=True)
```

### After (Centralized Animations)

```python
# ✅ GOOD - Import from tokens
from frontend.themes.tokens import ANIMATIONS

# Use predefined animations
st.markdown(f"""
    <style>
        {ANIMATIONS.KEYFRAMES}
    </style>
""", unsafe_allow_html=True)

# Or use animation strings directly
st.markdown('<div style="animation: glow 2s infinite ease-in-out;">Content</div>', unsafe_allow_html=True)
```

---

## Shared CSS Usage

### Option 1: Full Shared CSS

```python
from frontend.themes.shared_css import get_shared_css

st.markdown(get_shared_css(), unsafe_allow_html=True)
```

### Option 2: CSS Variables Only

```python
from frontend.themes.shared_css import get_css_variables

st.markdown(f"""
    <style>
        :root {{
            {get_css_variables()}
        }}
    </style>
""", unsafe_allow_html=True)
```

### Option 3: Animation Keyframes Only

```python
from frontend.themes.shared_css import get_animation_keyframes

st.markdown(f"""
    <style>
        {get_animation_keyframes()}
    </style>
""", unsafe_allow_html=True)
```

---

## Testing the Migration

### Verify Token Usage

```python
# Check if component uses tokens
import re

hardcoded_patterns = [
    r'#[0-9A-Fa-f]{6}',
    r'rgba?\([0-9,.\s]+\)',
    r'\d+px',
]

def check_component(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check for hardcoded values
    for pattern in hardcoded_patterns:
        matches = re.findall(pattern, content)
        if matches:
            print(f"Found {len(matches)} hardcoded values")
            return False
    return True
```

---

## Rollback Plan

If issues arise during migration:

1. **Component-level rollback**: Keep old code in comments for quick restore
2. **Feature flags**: Use session state to toggle between old/new implementations
3. **Gradual rollout**: Migrate one component at a time, test thoroughly

---

## Questions?

Contact the Frontend Team or refer to:
- `/docs/THEME_AUDIT.md` - Detailed theme analysis
- `/docs/COMPONENT_AUDIT.md` - Component audit results
- `frontend/themes/tokens.py` - Design token definitions
- `frontend/components/shared.py` - Shared component source
