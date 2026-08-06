# Component Documentation

## Overview

The Agent Control Tower is composed of reusable UI components located in `src/components/`. Each component is self-contained and follows a consistent pattern.

## Component Index

| Component | File | Description |
|-----------|------|-------------|
| AgentCard | `agent_card.py` | Individual agent display card |
| AgentDrawer | `agent_drawer.py` | Detailed agent information panel |
| CommunicationGraph | `communication_graph.py` | Agent communication flow visualization |
| EventStream | `event_stream.py` | Real-time event feed |
| HealthGauge | `health_gauge.py` | Health metrics visualization |
| LeftSidebar | `left_sidebar.py` | Category navigation sidebar |
| MissionHeader | `mission_header.py` | Top mission status header |
| ModelPanel | `model_panel.py` | AI model usage panel |
| ResourcePanel | `resource_panel.py` | Resource monitoring dashboard |
| SearchBar | `search_bar.py` | Search and filter controls |
| Timeline | `timeline.py` | Activity timeline |
| AgentQueue | `agent_queue.py` | Queue status visualization |

---

## AgentCard

**File**: `src/components/agent_card.py`

**Purpose**: Displays individual agent information in a card format.

### API

```python
def agent_card(agent: dict[str, Any], key: str | None = None) -> None:
    """
    Render an agent card with full details.
    
    Args:
        agent: Agent data dictionary
        key: Optional unique key for the card
    """
```

### Features
- Agent icon and name
- Category badge
- Status indicator with animation
- Current mission display
- Progress bar
- Metric grid (CPU, Memory, Confidence, Health)
- Tool and model display
- Execution time
- Messages processed count
- Health bar

### Styling
- Glassmorphism card effect
- Hover animation
- Status-based color coding
- Responsive layout

---

## AgentDrawer

**File**: `src/components/agent_drawer.py`

**Purpose**: Detailed agent information panel displayed as a side drawer.

### API

```python
def agent_drawer(agent: dict[str, Any]) -> None:
    """
    Render the agent detail drawer.
    
    Args:
        agent: Agent data dictionary
    """
```

### Sections
1. **Agent DNA**: Core identity (ID, category, status, model, tool, confidence)
2. **Current Mission**: Mission description and task progress
3. **Capabilities**: List of agent capabilities
4. **Tools**: Available tools
5. **Current Context**: Execution context (project, module, branch, environment)
6. **Memory State**: Memory metrics
7. **Health History**: Chart showing health over time
8. **Execution History**: Table of recent executions
9. **Recent Events**: Event log

### Styling
- Slide-in animation
- Dark overlay
- Section separators
- Interactive charts

---

## CommunicationGraph

**File**: `src/components/communication_graph.py`

**Purpose**: Visualizes the agent communication pipeline.

### API

```python
def render_simple_communication_flow(
    pipeline: list[tuple[str, str]],
    agents: list[dict[str, Any]]
) -> None:
    """Render a simplified vertical flow diagram."""
```

### Features
- Vertical node layout
- Animated connectors
- Status-based highlighting
- Hover tooltips

---

## EventStream

**File**: `src/components/event_stream.py`

**Purpose**: Displays real-time event feed from agents.

### API

```python
def event_stream(events: list[dict[str, Any]], max_display: int = 15) -> None:
    """
    Render the event stream component.
    
    Args:
        events: List of event dictionaries
        max_display: Maximum number of events to display
    """
```

### Event Types
- `info`: General information events
- `success`: Successful operations
- `warning`: Warnings and cautions
- `error`: Error events

### Features
- Severity color coding
- Time formatting (relative)
- Event statistics
- Expandable event list

---

## HealthGauge

**File**: `src/components/health_gauge.py`

**Purpose**: Visualizes health metrics with gauges and bars.

### API

```python
def render_health_dashboard(health_data: dict[str, Any]) -> None:
    """Render comprehensive health dashboard."""
```

### Metrics Displayed
- Overall health score (large circular gauge)
- CPU health
- Memory health
- Failure rate
- Retry rate
- Average confidence
- Active warnings count

### Color Coding
- Green (≥90%): Excellent
- Cyan (75-90%): Good
- Yellow (50-75%): Warning
- Red (<50%): Critical

---

## LeftSidebar

**File**: `src/components/left_sidebar.py`

**Purpose**: Category navigation and statistics.

### API

```python
def left_sidebar(
    agents: list[dict[str, Any]],
    selected_category: str,
    on_category_change: callable
) -> str:
    """
    Render the left sidebar with category navigation.
    
    Returns:
        Selected category name
    """
```

### Categories
- All Agents
- Intelligence
- Testing
- Documentation
- Infrastructure
- Learning
- Security
- Support

### Features
- Agent count per category
- Category icons
- Description text
- Interactive selection

---

## MissionHeader

**File**: `src/components/mission_header.py`

**Purpose**: Displays mission status at the top of the page.

### API

```python
def render_mission_header(
    mission_name: str,
    environment: str,
    agent_count: int,
    running_count: int,
    execution_time: datetime,
    auto_refresh: bool = True
) -> None:
    """Render the mission control header."""
```

### Displayed Information
- Mission name
- Environment badge (production/staging/development)
- Total agent count
- Running agent count
- Execution time (elapsed)

### Styling
- Gradient background
- Card-based stat display
- Color-coded environment badge

---

## ModelPanel

**File**: `src/components/model_panel.py`

**Purpose**: Shows AI model usage and routing.

### API

```python
def model_panel(model_usage: dict[str, int]) -> None:
    """
    Render the AI Model Panel.
    
    Args:
        model_usage: Dictionary mapping model names to request counts
    """
```

### Supported Models
- GPT-4
- GPT-3.5
- Claude
- Gemini
- DeepSeek
- Qwen

### Features
- Summary cards (primary model, total requests, average)
- Routing visualization
- Model distribution cards
- Pie chart (expandable)

---

## ResourcePanel

**File**: `src/components/resource_panel.py`

**Purpose**: Displays system resource utilization.

### API

```python
def resource_panel(metrics: dict[str, Any]) -> None:
    """
    Render the resource monitoring panel.
    
    Args:
        metrics: System metrics dictionary
    """
```

### Metrics Displayed
- Total CPU usage
- Total Memory usage
- Total GPU usage
- Token usage (input, output, total)
- Latency (average, p95, p99)
- Queue status (waiting, processing, available)
- Request counts

### Features
- Large metric cards
- Bar charts
- Stacked bar for queue
- Expandable details

---

## SearchBar

**File**: `src/components/search_bar.py`

**Purpose**: Search and filter agents.

### API

```python
def search_bar(
    agents: list[dict[str, Any]],
    categories: list[str],
    statuses: list[str]
) -> tuple[str, str, str]:
    """
    Render the complete search bar component.
    
    Returns:
        Tuple of (search_query, category, status)
    """
```

### Features
- Text search input
- Category dropdown filter
- Status dropdown filter
- Reset button
- Results count display

---

## Timeline

**File**: `src/components/timeline.py`

**Purpose**: Displays agent activity over time.

### API

```python
def timeline(agents: list[dict[str, Any]], events: list[dict[str, Any]]) -> None:
    """
    Render the bottom timeline component.
    
    Args:
        agents: List of agent dictionaries
        events: List of event dictionaries
    """
```

### Views
1. **Agent Progress**: List of agents with progress bars
2. **Event Stream**: Horizontal timeline of events

### Features
- Tab-based switching
- Agent sorting by status
- Event time buckets
- Color-coded severity

---

## AgentQueue

**File**: `src/components/agent_queue.py`

**Purpose**: Shows queue distribution and status.

### API

```python
def agent_queue(agents: list[dict[str, Any]]) -> None:
    """
    Render the Agent Queue component.
    
    Args:
        agents: List of agent dictionaries
    """
```

### Queue Statuses
- Running
- Waiting
- Paused
- Failed
- Completed
- Idle

### Features
- Summary cards (active agents, failed agents)
- Stacked bar distribution
- Individual status cards
- Visual grid (expandable)

---

## Usage Example

```python
import streamlit as st
from src.components.agent_card import agent_card
from src.data.mock_data import get_all_agents

# Get agents
agents = get_all_agents()

# Render agent cards
for agent in agents:
    agent_card(agent)
```

## Best Practices

1. **Import Order**: Follow PEP 8 conventions
2. **Type Hints**: Use type hints for all function parameters
3. **Docstrings**: Document purpose, parameters, and return values
4. **Styling**: Use CSS classes from theme for consistency
5. **Responsiveness**: Test on different screen sizes
