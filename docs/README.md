# AI-QOS - Agent Control Tower

## Overview

The Agent Control Tower is an enterprise-grade monitoring dashboard for AI agents in the AI-QOS system. It provides a comprehensive command center where users can observe every AI agent working together in real-time.

## Features

### 🎛️ Agent Monitoring
- Real-time agent status tracking
- Health monitoring with confidence scores
- CPU, Memory, and GPU utilization
- Execution time and message processing metrics

### 🔀 Communication Pipeline
- Visual representation of agent communication flow
- Animated message passing between agents
- Pipeline state tracking

### 📊 Resource Dashboard
- System-wide CPU, Memory, GPU usage
- Token usage tracking
- Latency metrics (avg, p95, p99)
- Queue status visualization

### 🤖 AI Model Panel
- Multi-model support (GPT-4, Claude, Gemini, DeepSeek, Qwen)
- Request distribution visualization
- Routing simulation

### 💚 Health Monitoring
- Overall health score
- Resource health metrics
- Failure and retry rates
- Active warnings

### 🔔 Event Stream
- Real-time event feed
- Event categorization (info, success, warning, error)
- Timeline visualization

### 📋 Agent Queue
- Queue status distribution
- Visual grid representation
- Running, waiting, paused, failed, completed counts

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

Or directly:

```bash
streamlit run pages/Agent_Control_Tower.py
```

### Access

Open your browser and navigate to:
- Local: http://localhost:8501
- Network: http://[your-ip]:8501

## Project Structure

```
AI-QOS/
├── app.py                      # Main entry point
├── pages/
│   └── Agent_Control_Tower.py  # Main dashboard page
├── src/
│   ├── components/             # UI components
│   │   ├── agent_card.py
│   │   ├── agent_drawer.py
│   │   ├── communication_graph.py
│   │   ├── event_stream.py
│   │   ├── health_gauge.py
│   │   ├── left_sidebar.py
│   │   ├── mission_header.py
│   │   ├── model_panel.py
│   │   ├── resource_panel.py
│   │   ├── search_bar.py
│   │   ├── timeline.py
│   │   └── agent_queue.py
│   ├── data/                   # Mock data and configurations
│   │   └── mock_data.py
│   ├── styles/                 # Styling and theming
│   │   └── theme.py
│   └── utils/                  # Utilities
│       └── session.py
├── docs/                       # Documentation
└── requirements.txt            # Dependencies
```

## Architecture

### Design System

The Control Tower uses a glassmorphism design system with:
- Dark theme with blue/purple accents
- Glass-like translucent panels
- Smooth animations and transitions
- Responsive layout

### Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Mission Header                           │
│  [Mission] [Environment] [Agents] [Running] [Time] [Refresh] │
├──────────┬──────────────────────────────────┬───────────────┤
│          │                                  │               │
│  Left    │       Center Workspace            │    Right      │
│  Sidebar │                                  │    Sidebar    │
│          │  ┌────────────────────────────┐  │               │
│ Category │  │ Communication Pipeline     │  │  Agent Queue  │
│  Nav     │  └────────────────────────────┘  │               │
│          │                                  │  Mission      │
│  Stats   │  ┌────────────────────────────┐  │  Health       │
│          │  │     Agent Grid              │  │               │
│          │  │  ┌────┐ ┌────┐ ┌────┐      │  │  Resource     │
│          │  │  │Card│ │Card│ │Card│      │  │  Dashboard    │
│          │  │  └────┘ └────┘ └────┘      │  │               │
│          │  └────────────────────────────┘  │  AI Model     │
│          │                                  │  Panel        │
│          │  ┌────────────────────────────┐  │               │
│          │  │     Timeline               │  │  Event Stream │
│          │  └────────────────────────────┘  │               │
│          │                                  │               │
├──────────┴──────────────────────────────────┴───────────────┤
│                     Timeline                                 │
└─────────────────────────────────────────────────────────────┘
```

## Supported Agents

The following AI agents are monitored by the Control Tower:

### Intelligence Agents
- Requirement Agent
- Application Intelligence Agent
- DOM Intelligence Agent
- Locator Intelligence Agent

### Testing Agents
- Frontend Testing Agent
- Backend Testing Agent
- API Testing Agent
- Database Testing Agent
- Performance Testing Agent
- Accessibility Agent
- Visual Testing Agent

### Documentation Agents
- Documentation Agent

### Infrastructure Agents
- Release Advisor Agent

### Learning Agents
- Learning Agent

### Security Agents
- Security Testing Agent

### Support Agents
- Bug Analysis Agent

## Session State

The application maintains the following session state:

| Key | Type | Description |
|-----|------|-------------|
| `agents` | list | All agent instances |
| `selected_agent` | dict | Currently selected agent |
| `drawer_open` | bool | Drawer visibility |
| `filter_category` | str | Category filter |
| `filter_status` | str | Status filter |
| `search_query` | str | Search query |
| `events` | list | Event stream |
| `auto_refresh` | bool | Auto-refresh toggle |
| `refresh_interval` | int | Refresh interval (seconds) |

## Future Backend Integration

The current implementation uses mock data. To integrate with a real backend:

1. Replace `src/data/mock_data.py` with API calls
2. Implement WebSocket connections for real-time updates
3. Add authentication and authorization
4. Connect to actual agent management systems

## License

MIT License
