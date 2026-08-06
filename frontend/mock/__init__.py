"""Mock data module for AI-QOS frontend.

This module provides mock data organized by domain:
- agents: Agent and queue data
- chat: Chat and conversation data
- missions: Mission and execution data
- reports: Review and report data
- knowledge: Knowledge graph data
- release: Release information data
- dom: DOM exploration data
- application: Application discovery data
"""
from frontend.mock.agents import (
    MOCK_AGENTS as AGENTS,
    MOCK_EVENTS as EVENTS,
    MOCK_QUEUE as QUEUE,
    MOCK_MODELS as MODELS,
)
from frontend.mock.chat import (
    MOCK_CONVERSATIONS as CONVERSATIONS,
    MOCK_MESSAGES as MESSAGES,
    MOCK_MISSION_CONTEXT as MISSION_CONTEXT,
    MOCK_QUICK_ACTIONS as QUICK_ACTIONS,
    MOCK_PROMPT_TEMPLATES as PROMPT_TEMPLATES,
)
from frontend.mock.missions import (
    MOCK_LOGS as LOGS,
    MOCK_NETWORK as NETWORK,
    MOCK_EXECUTION_STEPS as EXECUTION_STEPS,
)
from frontend.mock.reports import (
    MOCK_ASSERTIONS as ASSERTIONS,
    MOCK_EVIDENCE as EVIDENCE,
    MOCK_AI_REVIEW as AI_REVIEW,
)
from frontend.mock.application import (
    MOCK_DISCOVERED_PAGES as DISCOVERED_PAGES,
    MOCK_TECH_STACK as TECH_STACK,
    MOCK_AI_THOUGHTS as AI_THOUGHTS,
)

__all__ = [
    "AGENTS",
    "EVENTS",
    "QUEUE",
    "MODELS",
    "CONVERSATIONS",
    "MESSAGES",
    "MISSION_CONTEXT",
    "QUICK_ACTIONS",
    "PROMPT_TEMPLATES",
    "LOGS",
    "NETWORK",
    "EXECUTION_STEPS",
    "ASSERTIONS",
    "EVIDENCE",
    "AI_REVIEW",
    "DISCOVERED_PAGES",
    "TECH_STACK",
    "AI_THOUGHTS",
]
