# Architecture Documentation

## System Overview

The Agent Control Tower is built as a Streamlit application with a component-based architecture. It follows a modular design pattern where each UI component is self-contained and reusable.

## Design Principles

### 1. Component Isolation
Each component is designed to be independent and can be used in any part of the application without tight coupling.

### 2. State Management
Session state is managed centrally through `SessionState` class, providing a clean API for reading and writing state.

### 3. Data Flow
```
User Action → Session State Update → Component Re-render
```

### 4. Separation of Concerns
- **Data Layer**: `src/data/mock_data.py` - Data models and mock generation
- **Style Layer**: `src/styles/theme.py` - CSS and visual theming
- **UI Layer**: `src/components/*.py` - Reusable UI components
- **Logic Layer**: `src/utils/session.py` - State management and utilities
- **Presentation Layer**: `pages/*.py` - Page compositions

## Component Hierarchy

```
pages/
└── Agent_Control_Tower.py
    ├── inject_custom_css()
    ├── initialize_session()
    └── render_main_layout()
        ├── render_mission_header()
        ├── st.columns([left, center, right])
        │   ├── Left Sidebar
        │   │   ├── left_sidebar()
        │   │   └── render_category_stats()
        │   ├── Center Workspace
        │   │   ├── search_bar()
        │   │   ├── render_simple_communication_flow()
        │   │   ├── agent_card() [×N]
        │   │   └── timeline()
        │   └── Right Sidebar
        │       ├── render_refresh_controls()
        │       ├── agent_queue()
        │       ├── render_health_dashboard()
        │       ├── resource_panel()
        │       ├── model_panel()
        │       └── event_stream()
        └── agent_drawer() [conditional]
```

## Data Models

### Agent Model

```python
{
    "id": str,              # Unique identifier
    "name": str,            # Display name
    "category": AgentCategory,  # Category enum
    "icon": str,            # Emoji icon
    "status": AgentStatus,  # Current status
    "mission": str,         # Current mission description
    "current_task": str,    # Task being executed
    "progress": float,      # 0-100 percentage
    "confidence": float,    # 0-1 confidence score
    "cpu": float,           # CPU usage percentage
    "memory": float,        # Memory usage percentage
    "gpu": float,           # GPU usage percentage
    "current_tool": AgentTool,  # Current tool in use
    "current_model": AIModel,   # AI model being used
    "execution_time": int,  # Total execution time in seconds
    "messages_processed": int,  # Number of messages handled
    "health": float,        # Health score 0-1
    "decisions": int,       # Number of decisions made
    "retries": int,         # Number of retries
    "failures": int,        # Number of failures
    "current_prompt": str,   # Current prompt context
    "current_context": dict,    # Execution context
    "current_memory": dict,     # Memory state
    "execution_history": list,  # Recent executions
    "health_history": list,     # Health over time
    "recent_events": list,      # Recent events
}
```

### Event Model

```python
{
    "id": int,              # Unique identifier
    "timestamp": datetime,  # Event timestamp
    "type": EventType,      # Event type enum
    "message": str,         # Event message
    "severity": str,        # info/success/warning/error
}
```

### Metrics Model

```python
{
    "total_cpu": float,
    "total_memory": float,
    "total_gpu": float,
    "token_usage": {
        "input": int,
        "output": int,
        "total": int,
    },
    "requests": {
        "total": int,
        "pending": int,
        "completed": int,
    },
    "queue": {
        "waiting": int,
        "processing": int,
        "max_size": int,
    },
    "latency": {
        "avg_ms": float,
        "p95_ms": float,
        "p99_ms": float,
    },
    "model_usage": dict[str, int],
}
```

## State Flow

### Application Startup
1. Streamlit initializes
2. `render_page_config()` sets page configuration
3. `render_main_layout()` is called
4. `initialize_session()` loads initial data
5. Components render with current state

### User Interactions
1. User clicks agent card → `SessionState.select_agent()` → Drawer opens
2. User searches → `SessionState.set_search()` → Grid filters
3. User changes category → `SessionState.set_filter()` → Grid updates
4. User toggles refresh → `st.session_state.auto_refresh` updates → Auto-refresh loop starts

### Auto-Refresh Loop
1. `AutoRefresh.should_refresh()` checks elapsed time
2. If interval exceeded, regenerate agent data
3. Add new events to stream
4. Update timestamp
5. `st.rerun()` triggers re-render

## Component API

### agent_card(agent, key)
**Purpose**: Render single agent card

**Parameters**:
- `agent`: Agent dictionary
- `key`: Optional unique key

**Returns**: None (renders to Streamlit)

### agent_drawer(agent)
**Purpose**: Render detailed agent panel

**Parameters**:
- `agent`: Agent dictionary

**Returns**: None (renders to Streamlit)

### resource_panel(metrics)
**Purpose**: Render resource monitoring

**Parameters**:
- `metrics`: Metrics dictionary

**Returns**: None (renders to Streamlit)

## Session State API

```python
class SessionState:
    @classmethod
    def initialize(cls) -> None:
        """Initialize all session variables"""
    
    @classmethod
    def select_agent(cls, agent: dict) -> None:
        """Select and open agent drawer"""
    
    @classmethod
    def close_drawer(cls) -> None:
        """Close drawer"""
    
    @classmethod
    def set_filter(cls, category: str = None, status: str = None) -> None:
        """Update filters"""
    
    @classmethod
    def set_search(cls, query: str) -> None:
        """Update search query"""
    
    @classmethod
    def get_filtered_agents(cls, agents: list) -> list:
        """Get agents matching current filters"""
```

## Animation System

### CSS Animations
- `pulse-glow`: Status indicator pulsing
- `shimmer`: Progress bar shine effect
- `flow`: Message flow animation
- `fadeIn`: Card entrance animation

### JavaScript Animations
- Particle movement in communication graph
- Smooth transitions on hover states

## Responsive Design

Breakpoints:
- Desktop: > 1200px (3-column layout)
- Tablet: 768-1200px (2-column layout)
- Mobile: < 768px (single column)

Grid System:
- Agent cards: `repeat(auto-fill, minmax(320px, 1fr))`
- Sidebar: Fixed 25% width
- Main content: Flexible 1fr
- Right panel: Fixed 35% width

## Performance Considerations

1. **Memoization**: Use `@st.cache_data` for expensive operations
2. **Lazy Loading**: Expanders for heavy components
3. **Batch Updates**: Group state changes
4. **Efficient Renders**: Minimize full re-renders

## Security Notes

- No backend authentication (frontend only)
- No sensitive data handling
- All data is mocked/simulated
- CSP headers recommended for production

## Extending the System

### Adding New Agents
1. Add agent config to `AGENTS_CONFIG` in `mock_data.py`
2. Add category if needed to `AgentCategory` enum
3. Update `COMMUNICATION_PIPELINE` if applicable

### Adding New Components
1. Create component file in `src/components/`
2. Follow naming convention: `component_name.py`
3. Add component function with appropriate parameters
4. Import and use in page file

### Adding New Metrics
1. Extend metrics dictionary in `get_system_metrics()`
2. Add visualization in `resource_panel()`
3. Update mock data generation

## Testing Strategy

1. **Unit Tests**: Test individual component functions
2. **Integration Tests**: Test component interactions
3. **Visual Regression**: Screenshot comparisons
4. **Performance Tests**: Load testing with multiple agents
