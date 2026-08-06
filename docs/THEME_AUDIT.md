# Theme Audit Report

**Date:** August 6, 2026  
**Project:** AI-QOS Frontend  
**Auditor:** Automated Theme Audit

---

## Executive Summary

This audit evaluates the AI-QOS frontend for **dark mode consistency**, **glassmorphism consistency**, **color token usage**, **hardcoded colors**, and **inline CSS**. 

**Overall Status:** ⚠️ **Needs Improvement**

The theme configuration exists and defines CSS variables, but components are **not using them**, resulting in widespread hardcoded colors and inconsistent styling.

---

## 1. Dark Mode Consistency

### Status: ⚠️ **Issues Found**

### Background Colors
The theme defines:
```css
--background: #0F0F23;  /* Dark navy */
--surface: #1E1E3F;     /* Surface color */
```

**Issues Found:**
| Pattern | Count | Theme Token | Status |
|---------|-------|-------------|--------|
| `rgba(30, 30, 63, 0.8)` | 16+ | ❌ Not a token | ⚠️ Inconsistent |
| `rgba(30, 41, 59, 0.6)` | 13+ | ❌ Not a token | ⚠️ Inconsistent |
| `#0F0F23` | Rare | ✅ `--background` | ✅ OK |
| `#1E1E3F` | Rare | ✅ `--surface` | ✅ OK |

**Findings:**
- Two different glass background colors are used:
  - `rgba(30, 30, 63, 0.8)` - Slightly purple-tinted
  - `rgba(30, 41, 59, 0.6)` - More neutral, lower opacity
- These are NOT defined in the theme as glass tokens

### Text Colors
| Pattern | Count | Theme Token | Status |
|---------|-------|-------------|--------|
| `#F1F5F9` | 20+ | ✅ `--text-primary` | ⚠️ Not used |
| `#94A3B8` | 15+ | ✅ `--text-secondary` | ⚠️ Not used |
| `#64748B` | 30+ | ✅ `--text-muted` | ⚠️ Not used |

**Recommendation:** Text colors ARE defined in theme but NOT used in components.

---

## 2. Glassmorphism Consistency

### Status: ⚠️ **Inconsistent**

### Glass Background Patterns Found:
```python
# Pattern A: Purple-tinted glass
"background: rgba(30, 30, 63, 0.8)"
"background: linear-gradient(135deg, rgba(30, 30, 63, 0.95), rgba(99, 102, 241, 0.1))"

# Pattern B: Neutral glass
"background: rgba(30, 41, 59, 0.6)"
"background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95))"
```

### Theme Defines:
```css
--glass: rgba(30, 30, 63, 0.8);         /* Defined but NOT used */
--glass-border: rgba(99, 102, 241, 0.2);  /* Defined but NOT used */
```

**Issues:**
1. Theme defines `--glass` token but components don't use it
2. Two incompatible glass patterns exist
3. Different opacity levels (0.6 vs 0.8) create visual inconsistency

### Glassmorphism Border Patterns:
| Pattern | Count | Status |
|---------|-------|--------|
| `border: 1px solid rgba(99, 102, 241, 0.3)` | 10+ | ✅ Consistent |
| `border: 1px solid rgba(99, 102, 241, 0.2)` | 5+ | ✅ Consistent |
| `border: 1px solid #334155` | 7+ | ⚠️ Not glass-like |

---

## 3. Color Tokens

### Status: ⚠️ **Defined but Unused**

### Theme Color Tokens (Defined in `theme_config.py`):
```css
:root {
    --primary: #6366F1;
    --primary-light: #818CF8;
    --primary-dark: #4F46E5;
    --secondary: #22D3EE;
    --accent: #F472B6;
    --success: #10B981;
    --warning: #F59E0B;
    --error: #EF4444;
    --background: #0F0F23;
    --surface: #1E1E3F;
    --surface-hover: #2A2A4A;
    --border: #334155;
    --text-primary: #F1F5F9;
    --text-secondary: #94A3B8;
    --text-muted: #64748B;
}
```

### Usage Statistics:
| Token | Defined | Used in Components | Usage % |
|-------|---------|-------------------|---------|
| `--primary` | ✅ | ❌ Hardcoded `#6366F1` | 0% |
| `--success` | ✅ | ❌ Hardcoded `#10B981` | 0% |
| `--error` | ✅ | ❌ Hardcoded `#EF4444` | 0% |
| `--warning` | ✅ | ❌ Hardcoded `#F59E0B` | 0% |
| `--text-primary` | ✅ | ❌ Hardcoded `#F1F5F9` | 0% |
| `--glass` | ✅ | ❌ Hardcoded pattern | 0% |

**Conclusion:** Theme tokens exist but are **100% unused** in components.

---

## 4. Hardcoded Colors

### Status: 🔴 **Critical Issues**

### Total Hardcoded Colors Found: **599 instances**

### Top Offenders:
| Color | Hex | Count | Should Be |
|-------|-----|-------|-----------|
| Primary Purple | `#6366F1` | 45+ | `--primary` |
| Success Green | `#10B981` | 40+ | `--success` |
| Error Red | `#EF4444` | 35+ | `--error` |
| Warning Amber | `#F59E0B` | 30+ | `--warning` |
| Muted Gray | `#64748B` | 30+ | `--text-muted` |
| Border Gray | `#334155` | 25+ | `--border` |
| Cyan | `#22D3EE` | 20+ | `--secondary` |
| Text Light | `#F1F5F9` | 20+ | `--text-primary` |

### By Component:
| Component | Hardcoded Colors | Priority |
|-----------|-----------------|----------|
| `core_components.py` | 80+ | High |
| `agent_components.py` | 70+ | High |
| `execution_components.py` | 65+ | High |
| `chat_components.py` | 55+ | Medium |
| `intelligence_components.py` | 50+ | Medium |
| `review_components.py` | 45+ | Medium |

---

## 5. Inline CSS

### Status: 🔴 **Critical Issues**

### Total Inline CSS Blocks: **334 instances**

### Patterns Found:
```python
# Pattern 1: st.markdown with HTML/CSS
st.markdown(f"<div style='color: #F1F5F9;'>...", unsafe_allow_html=True)

# Pattern 2: f-strings with inline styles
f"""<div style="background: rgba(30, 30, 63, 0.8);">..."""

# Pattern 3: st.html (rare)
st.html("<style>...</style>")
```

### Inline CSS Types:
| Type | Count | Status |
|------|-------|--------|
| Background colors | 120+ | 🔴 Should use tokens |
| Text colors | 80+ | 🔴 Should use tokens |
| Border colors | 50+ | 🔴 Should use tokens |
| Border radius | 40+ | ⚠️ Should use `--radius` |
| Shadows | 20+ | ⚠️ Should use `--shadow` |
| Padding/margins | 25+ | ✅ Acceptable |

### Animation Keyframes Issues:
Found **duplicate keyframe definitions** across files:
- `@keyframes pulse` - Defined 3 times with different values
- `@keyframes glow` - Defined 3 times with different values
- `@keyframes slideIn` - Defined 2 times

---

## 6. Animation Consistency

### Status: ⚠️ **Inconsistent**

### Keyframe Definitions Found:
| Animation | Definitions | Locations | Consistency |
|-----------|-------------|-----------|-------------|
| `pulse` | 3 | Various | ❌ Different durations |
| `glow` | 3 | Various | ❌ Different colors/sizes |
| `slideIn` | 2 | Various | ⚠️ Similar |
| `shimmer` | 2 | Various | ⚠️ Similar |

### Theme Should Define:
```css
--animation-pulse: pulse 2s infinite;
--animation-glow: glow 2s infinite;
--animation-slideIn: slideIn 0.3s ease;
```

---

## Recommendations

### High Priority (Critical)
1. **Create a theme utility module** with color/style functions:
   ```python
   # frontend/themes/tokens.py
   COLORS = {
       "primary": "#6366F1",
       "success": "#10B981",
       # ...
   }
   
   def glass_background(opacity=0.8):
       return f"background: rgba(30, 30, 63, {opacity});"
   ```

2. **Replace all hardcoded colors** with theme token references
3. **Remove inline CSS** and use CSS classes from theme

### Medium Priority
4. **Consolidate animation keyframes** into theme
5. **Standardize glass background** to single pattern
6. **Create glassmorphism utility functions**

### Low Priority
7. **Document component styling guidelines**
8. **Add ESLint/Prettier for style consistency**
9. **Create Storybook for visual regression testing**

---

## Summary Table

| Category | Status | Score | Issues |
|----------|--------|-------|--------|
| Dark Mode Consistency | ⚠️ | 5/10 | Inconsistent backgrounds |
| Glassmorphism | ⚠️ | 4/10 | 2 patterns, theme unused |
| Color Tokens | 🔴 | 0/10 | Defined but unused |
| Hardcoded Colors | 🔴 | 0/10 | 599 instances |
| Inline CSS | 🔴 | 0/10 | 334 instances |

**Overall Score: 2/10** - Major refactoring needed.

---

## Files Affected

```
frontend/
├── themes/
│   └── theme_config.py     ✅ Good - defines tokens
├── components/
│   ├── core_components.py          🔴 80+ hardcoded colors
│   ├── agent_components.py         🔴 70+ hardcoded colors
│   ├── execution_components.py      🔴 65+ hardcoded colors
│   ├── chat_components.py           ⚠️ 55+ hardcoded colors
│   ├── intelligence_components.py  ⚠️ 50+ hardcoded colors
│   ├── review_components.py         ⚠️ 45+ hardcoded colors
│   ├── event_stream.py             ⚠️ 40+ hardcoded colors
│   ├── agent_drawer.py             ⚠️ 35+ hardcoded colors
│   ├── search_bar.py                ⚠️ 30+ hardcoded colors
│   ├── reports_components.py        ⚠️ 30+ hardcoded colors
│   ├── model_panel.py              ⚠️ 25+ hardcoded colors
│   ├── health_gauge.py              ⚠️ 20+ hardcoded colors
│   ├── resource_panel.py            ⚠️ 15+ hardcoded colors
│   ├── timeline.py                  ⚠️ 15+ hardcoded colors
│   ├── mission_header.py            ⚠️ 10+ hardcoded colors
│   ├── explorer_components.py       ⚠️ 10+ hardcoded colors
│   ├── dom_components.py            ⚠️ 5+ hardcoded colors
│   ├── knowledge_graph_components.py ⚠️ 5+ hardcoded colors
│   ├── wizard_components.py         ⚠️ 5+ hardcoded colors
│   └── communication_graph.py        ⚠️ 5+ hardcoded colors
└── mock/
    └── (data files - no styling)
```

---

## Conclusion

The AI-QOS frontend has a well-defined theme configuration, but **components do not use it**. All styling is done with hardcoded colors and inline CSS, leading to:

1. **Inconsistency** - Same colors defined multiple ways
2. **Maintenance burden** - Changing a color requires editing 500+ places
3. **Theme unused** - The `--variables` defined in CSS are never referenced
4. **Visual drift** - No centralized control over appearance

**Recommended Action:** Create a theme utility module and refactor components to use theme tokens and CSS classes instead of hardcoded values.
