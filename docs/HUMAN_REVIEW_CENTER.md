# Human Review Center Documentation

## Overview

The Human Review Center is a flagship collaboration experience of AI-QOS, where AI and human reviewers work together to validate test execution before continuing. It provides a GitHub PR Review-style interface for QA teams.

## Features

- **Evidence Summary** - Expected vs Actual results
- **Browser Comparison** - Screenshot with annotations
- **AI Review** - Automated analysis and recommendations
- **Review Timeline** - Visual progress tracking
- **Bug Generation** - One-click bug creation
- **Modification Panel** - Edit test parameters
- **Review Tabs** - Overview, Browser, DOM, Network, Console, Screenshots, Accessibility

## Folder Structure

```
frontend/
├── pages/
│   └── human_review_center.py  # Main Review page
├── components/
│   └── review_components.py   # Reusable review components
└── ...
```

## Session State Structure

```python
st.session_state.review_current_test     # Current test name
st.session_state.review_current_step    # Current step name
st.session_state.review_agent           # Active agent
st.session_state.review_confidence     # AI confidence
st.session_state.review_status          # Review status
st.session_state.review_decision        # User decision
st.session_state.show_bug_panel         # Show bug panel
st.session_state.show_modify_panel      # Show modify panel
```

## Page Structure

### Header
- Breadcrumb navigation
- Test name, agent, confidence
- Review status indicator

### Action Buttons
- Approve & Continue
- Retry
- Modify
- Generate Bug
- Skip
- Pause Mission

### Left Panel
- Evidence Summary (Expected/Actual)
- Assertions list
- Execution details
- Review Timeline

### Center Panel
- Browser Comparison View
- AI Highlights & Bounding Boxes
- Review Tabs

### Right Panel
- AI Review findings
- Observations
- Reasoning
- Potential Risks
- Best Practices

### Bottom Section
- Bug Generation Panel
- Modification Panel

## Components

### Review Components (`review_components.py`)

| Component | Description |
|-----------|-------------|
| `review_header()` | Header with mission info |
| `review_action_buttons()` | Action buttons |
| `evidence_panel()` | Expected vs Actual display |
| `browser_comparison()` | Screenshot with annotations |
| `ai_review_panel()` | AI analysis findings |
| `review_timeline()` | Visual timeline |
| `bug_preview_panel()` | Bug report preview |
| `modification_panel()` | Test modification form |
| `review_tabs()` | Tabbed interface |

## Mock Data

### Assertions
- Page Title Contains 'Dashboard' - PASSED
- User Name Displayed - PASSED
- Logout Button Visible - PASSED
- Sidebar Navigation Present - FAILED

### AI Review
- Observation: Dashboard page loaded with all expected elements
- Confidence: 92%
- Suggested Action: Approve
- Risks: Sidebar state may vary

## Navigation Flow

```
Execution Center → [Test Fails] → Human Review Center
                                              ↓
                                    User Actions:
                                    - Approve & Continue
                                    - Retry
                                    - Modify
                                    - Generate Bug
                                    - Skip
```

## Running the Human Review Center

```bash
cd frontend
streamlit run app.py
```

Navigate to **🔍 Human Review** in the sidebar.

## Future Backend Integration Points

### API Endpoints

```python
# Get review data
GET /api/v1/reviews/{review_id}

# Submit decision
POST /api/v1/reviews/{review_id}/decide

# Generate bug
POST /api/v1/bugs

# Get evidence
GET /api/v1/reviews/{review_id}/evidence

# Get screenshots
GET /api/v1/reviews/{review_id}/screenshots
```

### WebSocket Events

```python
# Review submitted
{
    "event": "review_submitted",
    "review_id": "abc123",
    "decision": "approved",
    "comments": ["Looks good"]
}

# Bug generated
{
    "event": "bug_created",
    "bug_id": "BUG-001",
    "severity": "Medium"
}
```

## Design Principles

- **GitHub PR Review** aesthetic
- **Collaboration** focus
- **Evidence-based** decisions
- **Professional** interface
- **Glassmorphism** styling
