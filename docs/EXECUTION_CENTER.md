# Live Execution Center Documentation

## Overview

The Live Execution Center is the flagship screen of AI-QOS - a NASA Mission Control-style dashboard for real-time test execution monitoring. It provides an immersive experience showing AI agents executing tests on a live browser.

## Features

- **Real-time Browser View** - Live visualization of browser actions
- **AI Thinking Panel** - Real-time AI reasoning and decisions
- **Active Agents Display** - Monitor multiple AI agents
- **Log Console** - Professional terminal for execution logs
- **Network Monitor** - Track API requests
- **Execution Timeline** - Visual progress tracking
- **Screenshots Gallery** - Captured screenshots

## Folder Structure

```
frontend/
├── pages/
│   └── execution_center.py      # Main Execution Center page
├── components/
│   └── execution_components.py # Reusable execution components
└── ...
```

## Session State Structure

```python
st.session_state.exec_is_running     # Execution running flag
st.session_state.exec_paused         # Pause state
st.session_state.exec_current_test   # Current test name
st.session_state.exec_progress       # Overall progress (0-100)
st.session_state.exec_passed         # Passed test count
st.session_state.exec_failed         # Failed test count
st.session_state.exec_skipped        # Skipped test count
st.session_state.exec_elapsed        # Elapsed seconds
st.session_state.exec_confidence     # AI confidence score
st.session_state.exec_current_url    # Current browser URL
```

## Page Structure

### Top Metrics Bar
- Running Time, CPU, Memory
- Agent Count, Browser Count
- API Calls, Screenshots, Videos
- Assertions

### Header
- Breadcrumb navigation
- Mission name and status
- Browser, Environment, Elapsed, Progress
- Action buttons (Pause, Resume, Stop, Restart, Report, AI Chat)

### Left Panel
- Mission Info Card
- Execution Statistics
- Test Details Card

### Center Panel
- Browser Viewer (animated)
- Execution Steps (visual progress)

### Right Panel
- AI Thinking Panel
- Active Agents Cards
- Recent Notifications

### Bottom Section
- Execution Timeline
- Log Console
- Network Activity
- Screenshots Gallery

## Components

### Execution Components (`execution_components.py`)

| Component | Description |
|-----------|-------------|
| `execution_header()` | Header with mission info and actions |
| `browser_viewer()` | Animated browser mockup |
| `ai_thinking_panel()` | AI reasoning and decisions |
| `agent_status_card()` | Individual agent status |
| `execution_timeline()` | Visual timeline |
| `console_viewer()` | Log console |
| `network_viewer()` | Network request table |
| `execution_stats()` | Statistics display |
| `mission_info_panel()` | Mission information |
| `execution_details_card()` | Current test details |
| `top_metrics_bar()` | Top metrics display |
| `notification_toast()` | Notification messages |

## Mock Data

### Active Agents
- Frontend Agent - Running, CPU: 45%, Memory: 62%
- DOM Agent - Running, CPU: 32%, Memory: 48%
- Locator Agent - Running, CPU: 28%, Memory: 35%
- API Agent - Idle, CPU: 15%, Memory: 22%
- Documentation Agent - Idle, CPU: 10%, Memory: 18%

### Network Requests
- POST /api/auth/login - 200, 234ms
- GET /api/user/profile - 200, 156ms
- GET /api/dashboard/metrics - 200, 89ms

### Execution Timeline
1. Browser Started ✓
2. Application Loaded ✓
3. DOM Ready ✓
4. Locators Found ✓
5. Login Executed ✓
6. Dashboard Loaded ✓
7. Assertions Running ●
8. Execution Complete ○

## Design Principles

- **Mission Control Aesthetic** - NASA-style monitoring
- **Glassmorphism** - Modern translucent panels
- **Real-time Animations** - Pulse, glow, transitions
- **Professional Terminal** - Dark console styling
- **Enterprise Grade** - Datadog/GitHub Actions feel

## Navigation Flow

```
Mission Planner → [Launch] → Intelligence Center → [Continue] → Execution Center
                                                                         ↓
                                                               User Actions:
                                                               - Pause/Resume
                                                               - Stop/Restart
                                                               - Generate Report
                                                               - AI Chat
```

## Running the Execution Center

```bash
cd frontend
streamlit run app.py
```

Navigate to **🚀 Live Execution** in the sidebar.

## Future Backend Integration Points

### API Endpoints

```python
# Get execution status
GET /api/v1/executions/{execution_id}

# Get current test
GET /api/v1/executions/{execution_id}/current-test

# Get agent status
GET /api/v1/executions/{execution_id}/agents

# Get logs stream
GET /api/v1/executions/{execution_id}/logs/stream

# Pause/Resume execution
POST /api/v1/executions/{execution_id}/pause
POST /api/v1/executions/{execution_id}/resume

# Stop execution
POST /api/v1/executions/{execution_id}/stop

# Get screenshots
GET /api/v1/executions/{execution_id}/screenshots

# Get network requests
GET /api/v1/executions/{execution_id}/network
```

### WebSocket Events

```python
# Test completed
{
    "event": "test_completed",
    "test": "login_flow",
    "status": "passed",
    "duration": 12500
}

# Agent status update
{
    "event": "agent_status",
    "agent": "frontend",
    "cpu": 45,
    "memory": 62
}

# Screenshot captured
{
    "event": "screenshot",
    "timestamp": "2024-01-15T10:30:00Z",
    "url": "/screenshots/abc123.png"
}

# Assertion result
{
    "event": "assertion",
    "expected": "Login successful",
    "actual": "Login successful",
    "status": "passed"
}
```

## Key Visual Elements

### Browser Viewer
- Professional browser chrome (traffic lights)
- URL bar with secure indicator
- Simulated page content
- Highlighted element with animation
- Element info tooltip

### AI Thinking Panel
- Current thought bubble
- Reasoning explanation
- Decision highlight
- Confidence meter
- Next action preview
- Risk warnings

### Agent Cards
- Status indicator
- Health, CPU, Memory metrics
- Current task
- Progress bar

## Animations

- **Pulse** - Active elements pulse
- **Glow** - AI agent icon glows
- **Progress** - Smooth progress bars
- **Notifications** - Slide in animations

## Future Improvements

- [ ] Real WebSocket integration
- [ ] Video recording playback
- [ ] Screenshot comparison view
- [ ] Interactive DOM inspector
- [ ] Command palette (Ctrl+K)
- [ ] Keyboard shortcuts
- [ ] Export to PDF/HTML
- [ ] Multi-browser support
- [ ] Parallel execution view
