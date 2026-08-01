# Application Intelligence Center Documentation

## Overview

The Application Intelligence Center is a flagship screen of AI-QOS that simulates AI studying the application before any testing begins. It provides a real-time, animated visualization of the discovery process, similar to GitHub Actions + Datadog + Cursor AI.

## Features

- **Real-time Discovery Progress** - Animated phases showing AI studying the application
- **Application Blueprint** - Comprehensive view of detected technologies and components
- **AI Assistant Panel** - Real-time thoughts and findings from the AI
- **Timeline View** - Visual representation of discovery milestones
- **Discovered Pages Table** - Detailed list of analyzed pages with coverage metrics

## Folder Structure

```
frontend/
├── pages/
│   └── intelligence_center.py     # Main Intelligence Center page
├── components/
│   └── intelligence_components.py # Reusable intelligence components
└── ...
```

## Session State Structure

```python
st.session_state.intel_current_phase     # Current discovery phase (0-14)
st.session_state.intel_phase_progress    # Progress for each phase
st.session_state.intel_discovery_complete # Discovery completion flag
st.session_state.intel_paused           # Pause state
st.session_state.intel_start_time       # Mission start timestamp
st.session_state.intel_confidence       # AI confidence score
st.session_state.intel_notifications    # Recent notifications
st.session_state.intel_stats            # Application statistics
st.session_state.intel_timeline         # Discovery timeline
```

## Discovery Phases

| Phase | Name | Duration | Description |
|-------|------|----------|-------------|
| 1 | Discovering Website | 3s | Initial connection and page load |
| 2 | Detecting Technology Stack | 5s | Framework and library detection |
| 3 | Scanning Navigation | 4s | Menu and routing analysis |
| 4 | Studying DOM Structure | 6s | HTML structure analysis |
| 5 | Finding Forms | 4s | Form detection |
| 6 | Finding Buttons | 3s | Button element detection |
| 7 | Finding Tables | 4s | Table structure detection |
| 8 | Finding Menus | 3s | Navigation menu analysis |
| 9 | Finding Modals | 4s | Dialog and modal detection |
| 10 | Discovering APIs | 6s | API endpoint discovery |
| 11 | Reading Authentication Flow | 5s | Auth mechanism analysis |
| 12 | Learning Business Workflows | 6s | User journey mapping |
| 13 | Generating Application Blueprint | 8s | Blueprint creation |
| 14 | Preparing Automation Plan | 5s | Test plan generation |

## Page Structure

### Header
- Breadcrumb navigation
- Mission name and status
- Confidence indicator
- Action buttons (Pause, Resume, Restart, Export, Report, Continue)

### Left Panel
- **Mission Info Card** - Mission details, progress, timing
- **DOM Summary** - Element counts and statistics

### Center Panel
- **Discovery Progress** - Animated phases with progress bars
- **Application Overview** - Technology, pages, forms, buttons
- **Technology Stack** - Detected frameworks and services

### Right Panel
- **AI Assistant** - Current thoughts, activity, findings
- **Progress Stats** - Key metrics
- **Notifications** - Recent events

### Bottom Timeline
- Visual timeline of discovery milestones
- Status indicators for each step
- Timestamps and duration

### Discovered Pages
- Table with page details
- Coverage metrics
- Status indicators

## Components

### Intelligence Components (`intelligence_components.py`)

| Component | Description |
|-----------|-------------|
| `init_intelligence_state()` | Initialize intelligence session state |
| `mission_info_card()` | Mission information display card |
| `tech_card()` | Technology stack card |
| `ai_thinking_panel()` | AI assistant panel |
| `discovery_progress_bar()` | Animated progress bar |
| `phase_completed_badge()` | Completed phase badge |
| `application_overview_card()` | Application overview card |
| `dom_summary_card()` | DOM statistics card |
| `timeline_step()` | Timeline step component |
| `confidence_indicator()` | Circular confidence gauge |
| `notification_toast()` | Notification message |
| `skeleton_card()` | Loading skeleton |
| `glass_loading_panel()` | Glass morphism loading |

## Navigation Flow

```
Mission Planner → [Launch Mission] → Intelligence Center → Automation Phase
                                              ↓
                                    User Actions:
                                    - Pause/Resume
                                    - Restart Analysis
                                    - Export Blueprint
                                    - Continue to Automation
```

## Mock Data

The Intelligence Center uses realistic mock data for demonstration:

### Technology Stack
- React 18.2.0 (Frontend)
- Node.js 20.x (Backend)
- PostgreSQL 15.0 (Database)
- OAuth 2.0 + JWT (Authentication)
- AWS (Hosting)
- Mixpanel (Analytics)

### Discovered Pages
- 8 pages analyzed
- 27 forms detected
- 83 API endpoints
- Average 92% coverage

## Design Principles

- **Dark Theme** - Consistent with AI-QOS design system
- **Glassmorphism** - Subtle blur effects on panels
- **Animations** - Smooth transitions and progress indicators
- **Professional** - Enterprise-grade appearance
- **Informative** - Clear data visualization

## Auto-Advance System

The discovery phases automatically progress for demo purposes:

```python
def auto_advance_phases() -> None:
    # Increment phase progress
    # Move to next phase when current completes
    # Update confidence score
    # Add notifications
    # Update statistics
```

## Future Backend Integration Points

### API Endpoints

```python
# Get mission status
GET /api/v1/missions/{mission_id}

# Get discovery progress
GET /api/v1/missions/{mission_id}/discovery

# Get discovered pages
GET /api/v1/missions/{mission_id}/pages

# Get technology stack
GET /api/v1/missions/{mission_id}/tech-stack

# Pause/Resume discovery
POST /api/v1/missions/{mission_id}/pause
POST /api/v1/missions/{mission_id}/resume

# Get AI thoughts stream
GET /api/v1/missions/{mission_id}/thoughts/stream
```

### WebSocket Events

```python
# Discovery phase completed
{
    "event": "phase_completed",
    "phase": "forms",
    "timestamp": "2024-01-15T10:30:00Z"
}

# New page discovered
{
    "event": "page_discovered",
    "page": {
        "name": "Dashboard",
        "url": "/dashboard",
        "forms": 3
    }
}

# Technology detected
{
    "event": "tech_detected",
    "technology": {
        "name": "React",
        "version": "18.2.0",
        "confidence": 98
    }
}

# Confidence updated
{
    "event": "confidence_updated",
    "confidence": 75
}
```

## Running the Intelligence Center

```bash
cd frontend
streamlit run app.py
```

Navigate to **🔬 Intelligence Center** in the sidebar.

## Keyboard Shortcuts

- `Space` - Pause/Resume discovery
- `R` - Restart analysis
- `E` - Export blueprint
- `C` - Continue to automation

## Future Improvements

- [ ] Add real WebSocket integration
- [ ] Implement page detail drawer
- [ ] Add export functionality (JSON, YAML)
- [ ] Add animation controls (speed, pause points)
- [ ] Implement confidence explanations
- [ ] Add screenshot previews for pages
- [ ] Implement drag-and-drop page reordering
- [ ] Add custom discovery rules
- [ ] Implement comparison mode (vs previous runs)
- [ ] Add AI thought history
