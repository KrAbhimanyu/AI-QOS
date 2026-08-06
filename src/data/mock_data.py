"""Mock data for Agent Control Tower - Enterprise AI Agent Monitoring Dashboard."""

from datetime import datetime, timedelta
from enum import Enum
from typing import Any
import random


class AgentStatus(str, Enum):
    """Agent execution status."""
    RUNNING = "running"
    WAITING = "waiting"
    PAUSED = "paused"
    FAILED = "failed"
    COMPLETED = "completed"
    IDLE = "idle"


class AgentCategory(str, Enum):
    """Agent category classification."""
    INTELLIGENCE = "Intelligence"
    TESTING = "Testing"
    DOCUMENTATION = "Documentation"
    INFRASTRUCTURE = "Infrastructure"
    LEARNING = "Learning"
    SECURITY = "Security"
    SUPPORT = "Support"


class AIModel(str, Enum):
    """Supported AI models."""
    GPT4 = "GPT-4"
    GPT35 = "GPT-3.5"
    CLAUDE = "Claude"
    GEMINI = "Gemini"
    DEEPSEEK = "DeepSeek"
    QWEN = "Qwen"


class AgentTool(str, Enum):
    """Available agent tools."""
    BROWSER_AUTOMATION = "Browser Automation"
    API_CLIENT = "API Client"
    CODE_ANALYZER = "Code Analyzer"
    DATABASE_QUERY = "Database Query"
    FILE_SYSTEM = "File System"
    VISUAL_VALIDATOR = "Visual Validator"
    SECURITY_SCANNER = "Security Scanner"
    DOCUMENTATION_GENERATOR = "Documentation Generator"


# Agent definitions with full metadata
AGENTS_CONFIG: list[dict[str, Any]] = [
    {
        "id": "requirement_agent",
        "name": "Requirement Agent",
        "category": AgentCategory.INTELLIGENCE,
        "icon": "📋",
        "description": "Analyzes and processes project requirements",
        "capabilities": ["Natural language understanding", "Requirements parsing", "Priority analysis"],
        "tools": [AgentTool.BROWSER_AUTOMATION, AgentTool.FILE_SYSTEM],
    },
    {
        "id": "app_intel_agent",
        "name": "Application Intelligence Agent",
        "category": AgentCategory.INTELLIGENCE,
        "icon": "🔍",
        "description": "Deep application structure analysis",
        "capabilities": ["Code structure analysis", "Dependency mapping", "Architecture detection"],
        "tools": [AgentTool.CODE_ANALYZER, AgentTool.FILE_SYSTEM],
    },
    {
        "id": "dom_intel_agent",
        "name": "DOM Intelligence Agent",
        "category": AgentCategory.INTELLIGENCE,
        "icon": "🌐",
        "description": "DOM structure and element analysis",
        "capabilities": ["DOM traversal", "Selector optimization", "Element mapping"],
        "tools": [AgentTool.BROWSER_AUTOMATION, AgentTool.CODE_ANALYZER],
    },
    {
        "id": "locator_intel_agent",
        "name": "Locator Intelligence Agent",
        "category": AgentCategory.INTELLIGENCE,
        "icon": "🎯",
        "description": "Intelligent element locator generation",
        "capabilities": ["Locator strategy", "Fallback generation", "Robustness scoring"],
        "tools": [AgentTool.BROWSER_AUTOMATION],
    },
    {
        "id": "frontend_test_agent",
        "name": "Frontend Testing Agent",
        "category": AgentCategory.TESTING,
        "icon": "🧪",
        "description": "Frontend component and UI testing",
        "capabilities": ["Component testing", "Interaction testing", "State validation"],
        "tools": [AgentTool.BROWSER_AUTOMATION, AgentTool.VISUAL_VALIDATOR],
    },
    {
        "id": "backend_test_agent",
        "name": "Backend Testing Agent",
        "category": AgentCategory.TESTING,
        "icon": "⚙️",
        "description": "Backend API and service testing",
        "capabilities": ["API testing", "Service integration", "Data validation"],
        "tools": [AgentTool.API_CLIENT, AgentTool.CODE_ANALYZER],
    },
    {
        "id": "api_test_agent",
        "name": "API Testing Agent",
        "category": AgentCategory.TESTING,
        "icon": "🔗",
        "description": "Comprehensive API testing and validation",
        "capabilities": ["REST/GraphQL testing", "Contract validation", "Load testing"],
        "tools": [AgentTool.API_CLIENT],
    },
    {
        "id": "database_test_agent",
        "name": "Database Testing Agent",
        "category": AgentCategory.TESTING,
        "icon": "🗄️",
        "description": "Database integrity and query testing",
        "capabilities": ["Query validation", "Data integrity", "Performance testing"],
        "tools": [AgentTool.DATABASE_QUERY],
    },
    {
        "id": "security_test_agent",
        "name": "Security Testing Agent",
        "category": AgentCategory.SECURITY,
        "icon": "🛡️",
        "description": "Security vulnerability assessment",
        "capabilities": ["Penetration testing", "Vulnerability scanning", "Compliance checking"],
        "tools": [AgentTool.SECURITY_SCANNER, AgentTool.API_CLIENT],
    },
    {
        "id": "performance_test_agent",
        "name": "Performance Testing Agent",
        "category": AgentCategory.TESTING,
        "icon": "⚡",
        "description": "Performance benchmarking and optimization",
        "capabilities": ["Load testing", "Profiling", "Optimization suggestions"],
        "tools": [AgentTool.API_CLIENT, AgentTool.BROWSER_AUTOMATION],
    },
    {
        "id": "accessibility_agent",
        "name": "Accessibility Agent",
        "category": AgentCategory.TESTING,
        "icon": "♿",
        "description": "Accessibility compliance verification",
        "capabilities": ["WCAG compliance", "Screen reader testing", "Keyboard navigation"],
        "tools": [AgentTool.BROWSER_AUTOMATION, AgentTool.VISUAL_VALIDATOR],
    },
    {
        "id": "visual_test_agent",
        "name": "Visual Testing Agent",
        "category": AgentCategory.TESTING,
        "icon": "👁️",
        "description": "Visual regression and UI comparison",
        "capabilities": ["Screenshot comparison", "Layout verification", "Responsive testing"],
        "tools": [AgentTool.VISUAL_VALIDATOR, AgentTool.BROWSER_AUTOMATION],
    },
    {
        "id": "documentation_agent",
        "name": "Documentation Agent",
        "category": AgentCategory.DOCUMENTATION,
        "icon": "📝",
        "description": "Automated documentation generation",
        "capabilities": ["Docstring generation", "API documentation", "README creation"],
        "tools": [AgentTool.DOCUMENTATION_GENERATOR, AgentTool.FILE_SYSTEM],
    },
    {
        "id": "bug_analysis_agent",
        "name": "Bug Analysis Agent",
        "category": AgentCategory.SUPPORT,
        "icon": "🐛",
        "description": "Automated bug analysis and reporting",
        "capabilities": ["Root cause analysis", "Stack trace parsing", "Issue categorization"],
        "tools": [AgentTool.CODE_ANALYZER, AgentTool.API_CLIENT],
    },
    {
        "id": "release_advisor_agent",
        "name": "Release Advisor Agent",
        "category": AgentCategory.INFRASTRUCTURE,
        "icon": "🚀",
        "description": "Release readiness assessment",
        "capabilities": ["Risk assessment", "Change analysis", "Deployment planning"],
        "tools": [AgentTool.API_CLIENT, AgentTool.CODE_ANALYZER],
    },
    {
        "id": "learning_agent",
        "name": "Learning Agent",
        "category": AgentCategory.LEARNING,
        "icon": "🧠",
        "description": "Continuous learning and improvement",
        "capabilities": ["Pattern recognition", "Knowledge synthesis", "Strategy optimization"],
        "tools": [AgentTool.API_CLIENT, AgentTool.DATABASE_QUERY],
    },
]


def generate_agent_instance(config: dict[str, Any]) -> dict[str, Any]:
    """Generate a fully populated agent instance with dynamic data."""
    status_weights = {
        AgentStatus.RUNNING: 0.35,
        AgentStatus.WAITING: 0.20,
        AgentStatus.PAUSED: 0.05,
        AgentStatus.FAILED: 0.05,
        AgentStatus.COMPLETED: 0.25,
        AgentStatus.IDLE: 0.10,
    }
    statuses = list(status_weights.keys())
    weights = list(status_weights.values())
    status = random.choices(statuses, weights=weights)[0]
    
    missions = [
        "Analyzing user authentication flow",
        "Validating API endpoint responses",
        "Mapping DOM element hierarchy",
        "Generating test coverage report",
        "Optimizing query performance",
        "Scanning for security vulnerabilities",
        "Documenting component interfaces",
        "Running regression tests",
        "Processing data transformations",
        "Monitoring system health",
        "Generating locator strategies",
        "Validating accessibility compliance",
    ]
    
    tasks = [
        "Processing requirements document",
        "Executing test suite",
        "Analyzing code structure",
        "Generating documentation",
        "Scanning vulnerabilities",
        "Optimizing performance",
        "Validating accessibility",
        "Running integration tests",
    ]
    
    models = list(AIModel)
    current_model = random.choice(models)
    
    cpu = random.uniform(5, 95) if status == AgentStatus.RUNNING else random.uniform(0, 30)
    memory = random.uniform(10, 85) if status == AgentStatus.RUNNING else random.uniform(5, 40)
    
    return {
        "id": config["id"],
        "name": config["name"],
        "category": config["category"],
        "icon": config["icon"],
        "description": config["description"],
        "capabilities": config["capabilities"],
        "tools": config["tools"],
        "status": status,
        "mission": random.choice(missions),
        "current_task": random.choice(tasks),
        "progress": random.uniform(0, 100) if status == AgentStatus.RUNNING else (100 if status == AgentStatus.COMPLETED else 0),
        "confidence": random.uniform(0.75, 0.99),
        "cpu": round(cpu, 1),
        "memory": round(memory, 1),
        "gpu": round(random.uniform(0, 80) if status == AgentStatus.RUNNING else 0, 1),
        "current_tool": random.choice(config["tools"]) if status == AgentStatus.RUNNING else None,
        "current_model": current_model,
        "execution_time": random.randint(10, 3600),
        "messages_processed": random.randint(50, 5000),
        "health": round(random.uniform(0.85, 1.0), 2),
        "decisions": random.randint(10, 200),
        "retries": random.randint(0, 5),
        "failures": random.randint(0, 3),
        "last_updated": datetime.now() - timedelta(seconds=random.randint(1, 300)),
        "current_prompt": _generate_prompt(config),
        "current_context": _generate_context(),
        "current_memory": _generate_memory(),
        "execution_history": _generate_history(status),
        "health_history": _generate_health_history(),
        "recent_events": _generate_events(),
    }


def _generate_prompt(config: dict[str, Any]) -> str:
    """Generate a realistic current prompt for the agent."""
    prompts = [
        f"Analyze the {config['name']} components and identify potential improvements.",
        f"Execute comprehensive testing for the user authentication module.",
        f"Generate detailed documentation for all public APIs.",
        f"Perform security scan and vulnerability assessment.",
        f"Optimize database queries and indexing strategy.",
        f"Validate UI components against design specifications.",
        f"Process and categorize incoming support tickets.",
    ]
    return random.choice(prompts)


def _generate_context() -> dict[str, Any]:
    """Generate current execution context."""
    return {
        "project": f"Project-{random.randint(100, 999)}",
        "module": f"module_{random.randint(1, 10)}",
        "branch": f"feature/agent-{random.randint(1, 50)}",
        "commit": f"{random.randint(1000, 9999)}abc{random.randint(1000, 9999)}",
        "environment": random.choice(["development", "staging", "production"]),
        "session_id": f"session_{random.randint(100000, 999999)}",
    }


def _generate_memory() -> dict[str, Any]:
    """Generate agent's current memory state."""
    return {
        "patterns_learned": random.randint(10, 500),
        "strategies_optimized": random.randint(5, 50),
        "knowledge_base_size": f"{random.randint(1, 100)}MB",
        "context_window_usage": f"{random.randint(60, 95)}%",
    }


def _generate_history(status: AgentStatus) -> list[dict[str, Any]]:
    """Generate execution history."""
    history = []
    for i in range(random.randint(5, 15)):
        history.append({
            "timestamp": datetime.now() - timedelta(hours=random.randint(1, 72)),
            "action": random.choice([
                "Task completed", "Decision made", "Error recovered",
                "Strategy optimized", "Context updated", "Tool executed"
            ]),
            "duration_ms": random.randint(100, 5000),
            "success": random.random() > 0.1,
        })
    return sorted(history, key=lambda x: x["timestamp"], reverse=True)


def _generate_health_history() -> list[dict[str, Any]]:
    """Generate health history over time."""
    history = []
    base_health = random.uniform(0.85, 0.98)
    for i in range(24):
        history.append({
            "timestamp": datetime.now() - timedelta(hours=24 - i),
            "health": round(min(1.0, max(0.5, base_health + random.uniform(-0.1, 0.1))), 2),
            "cpu": round(random.uniform(20, 80), 1),
            "memory": round(random.uniform(30, 70), 1),
        })
    return history


def _generate_events() -> list[dict[str, Any]]:
    """Generate recent events."""
    event_types = [
        ("Agent Started", "info"),
        ("Task Assigned", "info"),
        ("Task Completed", "success"),
        ("Message Sent", "info"),
        ("Retry Attempt", "warning"),
        ("Learning Updated", "success"),
        ("Error Occurred", "error"),
        ("Context Switch", "info"),
        ("Health Check Passed", "success"),
    ]
    events = []
    for _ in range(random.randint(10, 25)):
        event_type, severity = random.choice(event_types)
        events.append({
            "timestamp": datetime.now() - timedelta(seconds=random.randint(1, 600)),
            "type": event_type,
            "severity": severity,
            "message": f"{event_type} - {random.choice(['completed', 'processing', 'awaiting', 'success'])}",
        })
    return sorted(events, key=lambda x: x["timestamp"], reverse=True)


def get_all_agents() -> list[dict[str, Any]]:
    """Get all agent instances with generated data."""
    return [generate_agent_instance(config) for config in AGENTS_CONFIG]


def get_agents_by_category(category: AgentCategory) -> list[dict[str, Any]]:
    """Get agents filtered by category."""
    return [a for a in get_all_agents() if a["category"] == category]


def get_agent_by_id(agent_id: str) -> dict[str, Any] | None:
    """Get specific agent by ID."""
    for config in AGENTS_CONFIG:
        if config["id"] == agent_id:
            return generate_agent_instance(config)
    return None


# Communication pipeline definition
COMMUNICATION_PIPELINE = [
    ("requirement_agent", "app_intel_agent"),
    ("app_intel_agent", "dom_intel_agent"),
    ("dom_intel_agent", "locator_intel_agent"),
    ("locator_intel_agent", "frontend_test_agent"),
    ("frontend_test_agent", "documentation_agent"),
]


# Event stream types
class EventType(str, Enum):
    """Event stream event types."""
    AGENT_STARTED = "agent_started"
    TASK_ASSIGNED = "task_assigned"
    TASK_COMPLETED = "task_completed"
    MESSAGE_SENT = "message_sent"
    RETRY = "retry"
    LEARNING_UPDATED = "learning_updated"
    ERROR = "error"
    HEALTH_CHECK = "health_check"


def generate_live_event() -> dict[str, Any]:
    """Generate a random live event for the event stream."""
    event_templates = {
        EventType.AGENT_STARTED: "Agent {agent} started execution",
        EventType.TASK_ASSIGNED: "Task '{task}' assigned to {agent}",
        EventType.TASK_COMPLETED: "{agent} completed task in {duration}ms",
        EventType.MESSAGE_SENT: "{agent} sent {count} messages to {target}",
        EventType.RETRY: "{agent} retrying operation (attempt {attempt})",
        EventType.LEARNING_UPDATED: "{agent} updated knowledge base",
        EventType.ERROR: "Error in {agent}: {error}",
        EventType.HEALTH_CHECK: "{agent} health check: {status}",
    }
    
    event_type = random.choice(list(EventType))
    template = event_templates[event_type]
    agents = [a["name"] for a in AGENTS_CONFIG]
    
    event_data = {
        "agent": random.choice(agents),
        "target": random.choice(agents),
        "task": random.choice(["analysis", "testing", "validation", "optimization"]),
        "duration": random.randint(100, 5000),
        "count": random.randint(1, 50),
        "attempt": random.randint(1, 5),
        "error": random.choice(["timeout", "validation failed", "resource unavailable"]),
        "status": random.choice(["healthy", "degraded", "critical"]),
    }
    
    return {
        "id": random.randint(10000, 99999),
        "timestamp": datetime.now(),
        "type": event_type,
        "message": template.format(**event_data),
        "severity": "error" if event_type == EventType.ERROR else "info",
    }


def get_system_metrics() -> dict[str, Any]:
    """Get current system metrics."""
    return {
        "total_cpu": round(random.uniform(30, 70), 1),
        "total_memory": round(random.uniform(40, 60), 1),
        "total_gpu": round(random.uniform(20, 50), 1),
        "token_usage": {
            "input": random.randint(100000, 500000),
            "output": random.randint(50000, 300000),
            "total": random.randint(150000, 800000),
        },
        "requests": {
            "total": random.randint(1000, 10000),
            "pending": random.randint(10, 100),
            "completed": random.randint(900, 9900),
        },
        "queue": {
            "waiting": random.randint(5, 50),
            "processing": random.randint(1, 20),
            "max_size": 100,
        },
        "latency": {
            "avg_ms": round(random.uniform(50, 200), 1),
            "p95_ms": round(random.uniform(200, 500), 1),
            "p99_ms": round(random.uniform(500, 1000), 1),
        },
        "model_usage": {
            "GPT-4": random.randint(100, 500),
            "GPT-3.5": random.randint(200, 800),
            "Claude": random.randint(150, 600),
            "Gemini": random.randint(50, 300),
            "DeepSeek": random.randint(100, 400),
            "Qwen": random.randint(50, 200),
        },
    }


def get_mission_health() -> dict[str, Any]:
    """Get overall mission health metrics."""
    return {
        "overall": round(random.uniform(0.85, 0.98), 2),
        "cpu_health": round(random.uniform(0.80, 0.95), 2),
        "memory_health": round(random.uniform(0.85, 0.98), 2),
        "failure_rate": round(random.uniform(0.01, 0.05), 3),
        "retry_rate": round(random.uniform(0.02, 0.08), 3),
        "warning_count": random.randint(0, 5),
        "confidence_avg": round(random.uniform(0.85, 0.95), 2),
        "uptime": round(random.uniform(99.0, 99.9), 2),
    }
