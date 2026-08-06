# Component Audit Report

**Date:** August 6, 2026  
**Project:** AI-QOS Frontend

---

## Executive Summary

This audit identifies duplicate components, cards, charts, utilities, and CSS patterns in the codebase. While many functions share similar names across files, most are **intentionally different implementations** serving different purposes. However, a few true duplicates were identified.

---

## 1. Component Duplicates

### Found 9 functions with duplicate definitions across files:

| Function | Files | Status |
|----------|-------|--------|
| `notification_toast` | chat_components.py, execution_components.py, intelligence_components.py | ⚠️ Partial duplicates |
| `ai_thinking_panel` | chat_components.py, execution_components.py | ⚠️ Partial duplicates |
| `search_bar` | core_components.py, search_bar.py | ✅ Intentional - different signatures |
| `metric_card` | core_components.py, reports_components.py | ⚠️ Partial duplicates |
| `event_stream` | agent_components.py, event_stream.py | ⚠️ Partial duplicates |
| `ai_discoveries_panel` | explorer_components.py, knowledge_graph_components.py | ⚠️ Partial duplicates |
| `agent_queue` | agent_components.py, agent_queue.py | ⚠️ Partial duplicates |
| `agent_drawer` | agent_components.py, agent_drawer.py | ✅ Intentional - different UIs |
| `agent_card` | agent_components.py, core_components.py | ⚠️ Partial duplicates |

### Analysis:

**TRUE DUPLICATES (Similar implementations):**
1. **`notification_toast`** - Defined 3 times with slight variations:
   - `chat_components.py`: Simple HTML toast
   - `execution_components.py`: Flex layout variant
   - `intelligence_components.py`: Same as execution_components.py
   - **Recommendation:** Consolidate into a shared utility function

2. **`metric_card`** - Two different implementations:
   - `core_components.py`: Uses Streamlit `st.metric()`
   - `reports_components.py`: Custom HTML/CSS styling
   - **Recommendation:** Keep both - serve different UI needs

3. **`agent_card`** - Two implementations with different signatures:
   - `agent_components.py`: Takes a Dict parameter
   - `core_components.py`: Takes individual parameters
   - **Recommendation:** Keep both - serve different contexts

---

## 2. Card Duplicates

### Found: Multiple card-style implementations across components

| Card Type | Files | Status |
|-----------|-------|--------|
| Agent Cards | agent_components.py, core_components.py | ✅ Intentional - different contexts |
| Report Cards | reports_components.py | Unique |
| Health Cards | health_gauge.py | Unique |
| Mission Cards | core_components.py | Unique |

### CSS Card Patterns Found:
```python
# Common patterns scattered across 39+ files
border-radius: 12px;  # 39 occurrences
border-radius: 16px;  # 33 occurrences
background: rgba(30, 41, 59, 0.6);  # 20+ occurrences
```

**Recommendation:** Create a shared CSS constants module for common styling patterns.

---

## 3. Chart Duplicates

### Found: 13 chart-related functions across files:

| Chart Type | Location | Status |
|------------|----------|--------|
| `coverage_chart` | reports_components.py | ✅ Unique |
| `trend_chart` | reports_components.py | ✅ Unique |
| `pie_chart` | reports_components.py | ✅ Unique |
| `comparison_chart` | reports_components.py | ✅ Unique |
| `metric_gauge` | reports_components.py | ✅ Unique |
| `render_circular_gauge` | health_gauge.py | ✅ Unique |
| `render_multi_metric_gauges` | health_gauge.py | ✅ Unique |
| `render_metric_gauge` | resource_panel.py | ✅ Unique |
| `render_model_pie_chart` | model_panel.py | ✅ Unique |
| `render_health_history_chart` | agent_drawer.py | ✅ Unique |
| `render_latency_chart` | resource_panel.py | ✅ Unique |
| `render_token_usage_chart` | resource_panel.py | ✅ Unique |
| `render_queue_chart` | resource_panel.py | ✅ Unique |

**Status:** ✅ No duplicate chart implementations

---

## 4. Utility Duplicates

### Found 3 duplicate definitions in `utils/`:

| Function/Class | Files | Status |
|-----------------|-------|--------|
| `RiskLevel` | dom_data.py, explorer_data.py | 🔴 TRUE DUPLICATE |
| `generate_discovery_timeline` | dom_data.py, explorer_data.py | ⚠️ Different content |
| `generate_ai_discoveries` | dom_data.py, explorer_data.py | ⚠️ Different content |

### Analysis:

**🔴 RISKLEVEL ENUM - TRUE DUPLICATE:**
```python
# Identical definitions in both files:
class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"
```
**Recommendation:** Move to a shared `enums.py` file

**⚠️ generate_discovery_timeline:**
- `dom_data.py`: Returns DOM-related discovery steps
- `explorer_data.py`: Returns application exploration steps
- **Recommendation:** Rename for clarity (e.g., `generate_dom_discovery_timeline`)

**⚠️ generate_ai_discoveries:**
- `dom_data.py`: DOM-specific discoveries (missing IDs, labels)
- `explorer_data.py`: Application-level discoveries (duplicate IDs, accessibility)
- **Recommendation:** Rename for clarity (e.g., `generate_dom_ai_discoveries`)

---

## 5. CSS Duplicates

### Inline Styles Found:
- **39+ occurrences:** `border-radius: 12px;`
- **33+ occurrences:** `border-radius: 16px;`
- **20+ occurrences:** `background: rgba(30, 41, 59, 0.6);`

### Animation Keyframes:
| Animation | Occurrences | Status |
|-----------|-------------|--------|
| `pulse` | 3 | ⚠️ Redundant definitions |
| `slideIn` | 2 | ⚠️ Redundant definitions |
| `glow` | 3 | ⚠️ Redundant definitions |

### Color Definitions (Repeated patterns):
```python
# Colors repeated in 10+ places:
# #10B981 (green/success)
# #6366F1 (purple/primary)
# #EF4444 (red/error)
# #F59E0B (amber/warning)
# #64748B (gray/neutral)
```

**Recommendation:** Create a centralized theme module with:
- Color constants
- Border radius constants
- Animation keyframes
- Common card styles

---

## Summary of Recommendations

### High Priority (True Duplicates):
1. **Move `RiskLevel` enum** to a shared `enums.py` file
2. **Consolidate `notification_toast`** into a single utility function

### Medium Priority (Naming Clarity):
3. **Rename `generate_discovery_timeline`** functions to be more specific
4. **Rename `generate_ai_discoveries`** functions to be more specific

### Low Priority (Code Organization):
5. **Create a theme/constants module** for shared CSS values
6. **Document intentional variations** in comments

---

## Files Audited

```
frontend/
├── components/
│   ├── __init__.py
│   ├── agent_components.py
│   ├── agent_drawer.py
│   ├── agent_queue.py
│   ├── chat_components.py
│   ├── communication_graph.py
│   ├── core_components.py
│   ├── dom_components.py
│   ├── event_stream.py
│   ├── execution_components.py
│   ├── explorer_components.py
│   ├── health_gauge.py
│   ├── intelligence_components.py
│   ├── knowledge_graph_components.py
│   ├── mission_header.py
│   ├── model_panel.py
│   ├── reports_components.py
│   ├── resource_panel.py
│   ├── review_components.py
│   ├── search_bar.py
│   ├── timeline.py
│   └── wizard_components.py
├── utils/
│   ├── __init__.py
│   ├── dom_data.py
│   ├── explorer_data.py
│   ├── helpers.py
│   ├── knowledge_graph_data.py
│   └── reports_data.py
└── themes/
    └── theme_config.py
```

---

## Conclusion

The codebase has **minimal true duplicates** but contains many functions with similar names serving different purposes. The primary issues are:

1. **One true duplicate:** `RiskLevel` enum (identical in 2 files)
2. **Redundant implementations:** `notification_toast` (3 versions)
3. **Ambiguous naming:** Functions with same name returning different data
4. **Scattered CSS:** Inline styles repeated throughout codebase

The overall architecture is well-organized with clear separation of concerns. The duplicates found are mostly cosmetic and don't indicate architectural problems.
