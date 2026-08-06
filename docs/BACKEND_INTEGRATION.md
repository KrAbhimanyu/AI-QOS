# Backend Integration Guide

## Current State

The Agent Control Tower currently runs in **frontend-only mode** with mock data. This document outlines the architecture and provides guidance for integrating with a real backend.

## Mock Data Architecture

### Current Data Flow

```
mock_data.py → Session State → Components → UI
```

### Mock Data Generation

The mock data system in `src/data/mock_data.py` provides:

1. **Agent Configurations**: Static agent definitions
2. **Dynamic Instance Generation**: Runtime agent state
3. **Event Generation**: Simulated real-time events
4. **Metrics Simulation**: System metrics generation

### Key Functions

```python
# Get all agents with generated state
def get_all_agents() -> list[dict[str, Any]]

# Generate a single agent instance
def generate_agent_instance(config: dict) -> dict

# Generate live event
def generate_live_event() -> dict

# Get system metrics
def get_system_metrics() -> dict

# Get mission health
def get_mission_health() -> dict
```

## Integration Patterns

### Pattern 1: Replace Mock Functions

Replace mock functions with API calls:

```python
# Before (Mock)
def get_all_agents():
    from src.data.mock_data import get_all_agents as mock_get
    return mock_get()

# After (Real API)
def get_all_agents():
    response = requests.get(f"{API_BASE}/agents")
    return response.json()
```

### Pattern 2: WebSocket for Real-time Updates

For live event streaming:

```python
import websocket
import json

class EventStream:
    def __init__(self, url: str):
        self.ws = websocket.WebSocketApp(
            url,
            on_message=self.on_message,
            on_error=self.on_error,
        )
    
    def on_message(self, ws, message):
        event = json.loads(message)
        SessionState.add_event(event)
        st.rerun()
    
    def start(self):
        self.ws.run_forever()
```

### Pattern 3: REST API Polling

For periodic updates:

```python
def poll_agents():
    while True:
        agents = requests.get(f"{API_BASE}/agents").json()
        st.session_state.agents = agents
        st.rerun()
        time.sleep(st.session_state.refresh_interval)
```

## API Specification

### Endpoints Required

#### GET /api/agents
Returns list of all agents with current state.

```json
{
  "agents": [
    {
      "id": "requirement_agent",
      "name": "Requirement Agent",
      "status": "running",
      "cpu": 45.2,
      "memory": 62.1,
      ...
    }
  ]
}
```

#### GET /api/agents/{id}
Returns detailed agent information.

```json
{
  "id": "requirement_agent",
  "name": "Requirement Agent",
  "dna": {...},
  "capabilities": [...],
  "history": [...],
  ...
}
```

#### GET /api/metrics
Returns system-wide metrics.

```json
{
  "total_cpu": 45.5,
  "total_memory": 52.3,
  "token_usage": {...},
  ...
}
```

#### GET /api/health
Returns mission health data.

```json
{
  "overall": 0.95,
  "cpu_health": 0.92,
  "memory_health": 0.98,
  ...
}
```

#### GET /api/events
Returns recent events.

```json
{
  "events": [
    {
      "id": 12345,
      "type": "task_completed",
      "severity": "success",
      ...
    }
  ]
}
```

#### WebSocket /ws/events
Real-time event stream.

```json
{
  "type": "event",
  "data": {
    "id": 12346,
    "type": "agent_started",
    ...
  }
}
```

## Authentication

### Recommended Auth Flow

1. **Login Endpoint**: `POST /api/auth/login`
2. **Token Storage**: Secure session or JWT
3. **API Authorization**: Bearer token in headers

```python
headers = {
    "Authorization": f"Bearer {st.session_state.token}"
}
response = requests.get(f"{API_BASE}/agents", headers=headers)
```

### Streamlit Auth Considerations

- Use `st.session_state` for token storage
- Implement logout functionality
- Handle token refresh
- Secure credential management

## Data Transformation

### Transform Mock to API Format

```python
def transform_agent(api_data: dict) -> dict:
    """Transform API response to component format."""
    return {
        "id": api_data["agent_id"],
        "name": api_data["display_name"],
        "status": AgentStatus(api_data["state"]),
        "cpu": api_data["resources"]["cpu_percent"],
        "memory": api_data["resources"]["memory_percent"],
        # Map other fields...
    }
```

### Transform API to Mock Format

```python
def transform_for_component(api_data: dict) -> dict:
    """Transform API response to match mock format."""
    return {
        "id": api_data.get("id"),
        "name": api_data.get("name"),
        "category": AgentCategory(api_data.get("category")),
        # Match the format expected by components
    }
```

## Error Handling

### API Error Handling

```python
def fetch_with_retry(url: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                st.error(f"Failed to fetch data: {e}")
                return None
            time.sleep(1 * (attempt + 1))
```

### Graceful Degradation

```python
def get_agents_safe():
    try:
        return fetch_agents_from_api()
    except Exception as e:
        st.warning(f"API unavailable, using cached data: {e}")
        return st.session_state.get("cached_agents", [])
```

## Caching Strategy

### Streamlit Caching

```python
@st.cache_data(ttl=60)
def fetch_agents_cached():
    return requests.get(f"{API_BASE}/agents").json()

@st.cache_data(ttl=300)
def fetch_metrics_cached():
    return requests.get(f"{API_BASE}/metrics").json()
```

### Session Caching

```python
def get_agents():
    if "agents" not in st.session_state:
        st.session_state.agents = fetch_agents_from_api()
    return st.session_state.agents
```

## Performance Optimization

### Lazy Loading

```python
def render_agent_detail(agent_id: str):
    with st.expander("Agent Details"):
        if st.session_state.get(f"detail_{agent_id}"):
            render_detail(st.session_state[f"detail_{agent_id}"])
        else:
            if st.button("Load Details"):
                st.session_state[f"detail_{agent_id}"] = fetch_detail(agent_id)
                st.rerun()
```

### Pagination

```python
def fetch_agents_page(page: int, page_size: int = 20):
    offset = page * page_size
    return requests.get(
        f"{API_BASE}/agents",
        params={"offset": offset, "limit": page_size}
    ).json()
```

### Batch Requests

```python
def fetch_dashboard_data():
    # Parallel requests
    agents, metrics, health, events = await asyncio.gather(
        fetch_agents(),
        fetch_metrics(),
        fetch_health(),
        fetch_events(),
    )
    return {
        "agents": agents,
        "metrics": metrics,
        "health": health,
        "events": events,
    }
```

## WebSocket Integration

### Client Implementation

```python
import websocket
import threading
import json

class AgentWebSocket:
    def __init__(self, url: str, on_message: callable):
        self.url = url
        self.on_message = on_message
        self.ws = None
        self.thread = None
    
    def connect(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=lambda ws, msg: self.on_message(json.loads(msg)),
            on_error=lambda ws, err: print(f"Error: {err}"),
            on_close=lambda ws: print("Connection closed"),
        )
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.daemon = True
        self.thread.start()
    
    def disconnect(self):
        if self.ws:
            self.ws.close()
```

### Integration with Streamlit

```python
def main():
    # Initialize WebSocket
    if "ws" not in st.session_state:
        st.session_state.ws = AgentWebSocket(
            "wss://api.example.com/ws/events",
            on_message=handle_event
        )
        st.session_state.ws.connect()
    
    # UI rendering
    render_dashboard()
    
    # Cleanup on session end
    atexit.register(lambda: st.session_state.ws.disconnect())
```

## Testing Strategy

### Mock API Server

```python
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class MockAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/agents":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(AGENTS_DATA).encode())
        # Handle other endpoints...

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), MockAPIHandler)
    server.serve_forever()
```

### Test Components

```python
import pytest
from src.components.agent_card import agent_card

def test_agent_card_renders():
    agent = {
        "id": "test",
        "name": "Test Agent",
        "status": {"value": "running"},
        ...
    }
    
    # Use pytest- Streamlit for testing
    # ...
```

## Deployment Considerations

### Environment Variables

```bash
# .env file
API_BASE_URL=https://api.example.com
API_KEY=your_api_key
WS_URL=wss://api.example.com/ws
REFRESH_INTERVAL=5
```

### Production Settings

```python
import os

API_BASE = os.getenv("API_BASE_URL", "https://api.example.com")
API_KEY = os.getenv("API_KEY")
REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL", "5"))
```

### Container Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

## Monitoring & Observability

### Logging

```python
import logging

logger = logging.getLogger(__name__)

def fetch_agents():
    try:
        response = requests.get(f"{API_BASE}/agents")
        logger.info(f"Fetched {len(response.json())} agents")
        return response.json()
    except Exception as e:
        logger.error(f"Failed to fetch agents: {e}")
        raise
```

### Metrics Export

```python
from prometheus_client import Counter, Histogram

api_requests = Counter("api_requests_total", "Total API requests")
api_latency = Histogram("api_latency_seconds", "API latency")
```

## Security Checklist

- [ ] Use HTTPS for all API calls
- [ ] Implement proper authentication
- [ ] Sanitize user inputs
- [ ] Validate API responses
- [ ] Handle sensitive data appropriately
- [ ] Implement rate limiting
- [ ] Log security events
- [ ] Use secure WebSocket connections (WSS)
