# Agent Control Tower Documentation

## Overview

The Agent Control Tower is a Kubernetes Dashboard + Datadog + Mission Control style command center where users can observe every AI Agent working together in real-time. It provides a comprehensive view of all agents, their status, communications, and resource usage.

## Features

- **Agent Grid** - Visual cards for all 16 agents
- **Communication Graph** - Animated agent interaction visualization
- **Resource Dashboard** - CPU, Memory, GPU, Token usage
- **Agent Queue** - Running, Waiting, Paused, Failed status
- **AI Model Panel** - Model routing and usage
- **Event Stream** - Live event feed
- **Mission Health** - Overall health metrics

## Folder Structure

```
frontend/
├── pages/
│   └── agent_control_tower.py  # Main Control Tower page
├── components/
│   └── agent_components.py      # Agent components
└── ...
```

## Supported Agents (16)

### Intelligence
- Requirement Agent 📋
- Application Intelligence Agent 🔍
- DOM Intelligence Agent 📐
- Locator Intelligence Agent 🎯
- Bug Analysis Agent 🐛

### Testing
- Frontend Testing Agent 🖥️
- Backend Testing Agent ⚙️
- API Testing Agent 🔗
- Database Testing Agent 🗄️
- Security Testing Agent 🔐
- Performance Testing Agent ⚡
- Accessibility Agent ♿
- Visual Testing Agent 👁️

### Documentation
- Documentation Agent 📝

### Learning
- Learning Agent 🧠

### Support
- Release Advisor Agent 🚀

## Session State Structure

```python
st.session_state.agent_selected     # Selected agent ID
st.session_state.agent_filters      # Status/Category filters
st.session_state.agent_search        # Search query
st.session_state.agent_events       # Event history
```

## Page Structure

### Header
- Mission name
- Environment
- Running agents count
- Overall health
- Execution time

### Left Sidebar
- Agent Categories with counts
- Mission Health metrics

### Center Panel
- Communication Graph
- Agent Grid (16 agents)
- Agent Queue

### Right Sidebar
- Resource Dashboard
- AI Model Panel
- Event Stream

### Bottom Section
- Agent Details (expandable drawers)

## Components

### Agent Components (`agent_components.py`)

| Component | Description |
|-----------|-------------|
| `agent_header()` | Header with mission info |
| `agent_card()` | Individual agent card with metrics |
| `agent_categories()` | Category sidebar |
| `communication_graph()` | Animated agent connections |
| `agent_queue()` | Queue status display |
| `resource_dashboard()` | Resource usage metrics |
| `ai_model_panel()` | AI model routing |
| `event_stream()` | Live event feed |
| `mission_health()` | Health metrics |
| `agent_drawer()` | Detailed agent info |

## Agent Card Metrics

Each agent card displays:
- Name, Icon, Status
- Current Task
- Progress (0-100%)
- CPU Usage
- Memory Usage
- Health
- Confidence
- Current Tool
- Current Model
- Execution Time
- Messages Processed

## Communication Graph

Visualizes agent communication flow:
```
Requirement → Application
         ↘ DOM ↙
           Locator
         ↙     ↘
       Frontend → API
            ↘   ↙
           Docs
```

## Resource Metrics

- CPU Usage (%)
- Memory Usage (%)
- GPU Usage (%)
- Token Usage (tokens)
- Requests (count)
- Queue (count)
- Latency (ms)

## AI Models

- GPT-4
- Claude-3
- Gemini-Pro
- DeepSeek-Coder
- Qwen-2

## Design Principles

- **Kubernetes Dashboard** aesthetic
- **Datadog** monitoring style
- **Mission Control** visualization
- **Glassmorphism** panels
- **Real-time** animations

## Running the Agent Control Tower

```bash
cd frontend
streamlit run app.py
```

Navigate to **🤖 Agent Control** in the sidebar.

## Future Backend Integration Points

### API Endpoints

```python
# Get all agents
GET /api/v1/agents

# Get agent details
GET /api/v1/agents/{agent_id}

# Get agent events
GET /api/v1/agents/{agent_id}/events

# Get resource metrics
GET /api/v1/resources

# Get model usage
GET /api/v1/models/usage

# Control agent
POST /api/v1/agents/{agent_id}/pause
POST /api/v1/agents/{agent_id}/resume
POST /api/v1/agents/{agent_id}/stop
```

### WebSocket Events

```python
# Agent status changed
{
    "event": "agent_status",
    "agent_id": "frontend_test",
    "status": "running",
    "task": "Executing test"
}

# Resource updated
{
    "event": "resource_update",
    "cpu": 45,
    "memory": 62
}

# Event occurred
{
    "event": "agent_event",
    "type": "task_completed",
    "agent": "Locator Agent",
    "message": "Generated 24 locators"
}
```

## Agent States

| State | Color | Description |
|-------|-------|-------------|
| Running | Green | Actively processing |
| Idle | Gray | Waiting for tasks |
| Paused | Yellow | Manually paused |
| Failed | Red | Error occurred |

## Visual Features

- **Pulsing animations** on running agents
- **Glowing effects** on active nodes
- **Flowing connections** in communication graph
- **Blinking indicators** in event stream
- **Progress bars** with gradients
