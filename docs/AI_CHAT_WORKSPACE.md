# AI Chat Workspace Documentation

## Overview

The AI Chat Workspace is the central collaboration hub of AI-QOS, allowing users to interact naturally with the AI while maintaining full awareness of the current mission and execution context. It combines ChatGPT-style conversations with Cursor AI and GitHub Copilot features.

## Features

- **Three-Panel Layout** - Conversation history, chat, and context
- **Professional Chat UI** - Markdown, code blocks, syntax highlighting
- **Mission Context** - Real-time mission information display
- **Quick Actions** - One-click AI commands
- **Prompt Library** - Pre-built prompt templates
- **Context Cards** - Quick access to mission elements
- **AI Thinking Panel** - See AI reasoning in real-time

## Folder Structure

```
frontend/
├── pages/
│   └── ai_chat_workspace.py   # Main chat page
├── components/
│   └── chat_components.py      # Chat components
└── ...
```

## Session State Structure

```python
st.session_state.chat_conversations      # List of conversations
st.session_state.chat_current_conversation  # Current chat ID
st.session_state.chat_messages           # Messages in current chat
st.session_state.chat_prompt_history    # Prompt history
st.session_state.chat_pinned            # Pinned conversations
st.session_state.chat_selected_context   # Selected context card
```

## Page Structure

### Header
- Breadcrumb navigation
- Mission name and status
- Agent and test information
- Action buttons (New Chat, Export, Clear, Search, Settings)

### Left Sidebar
- Pinned conversations
- Recent conversations
- Quick actions

### Center Panel
- Conversation title
- Chat messages with:
  - User/AI avatars
  - Timestamps
  - Message actions (Copy, Edit, Retry, Bookmark)
  - Code blocks with syntax highlighting
- Context cards
- Prompt editor

### Right Panel
- Mission Context card
- AI Knowledge panel
- AI Thinking panel

### Bottom Section
- Quick Actions grid
- Prompt Library
- Prompt Editor

## Components

### Chat Components (`chat_components.py`)

| Component | Description |
|-----------|-------------|
| `chat_header()` | Header with mission info |
| `chat_action_buttons()` | Action buttons |
| `conversation_sidebar()` | Conversation history |
| `chat_message()` | Chat bubble display |
| `typing_indicator()` | AI typing animation |
| `prompt_editor()` | Prompt input |
| `context_panel()` | Mission context |
| `ai_knowledge_panel()` | AI knowledge display |
| `quick_actions_grid()` | Quick action buttons |
| `prompt_library()` | Prompt templates |
| `ai_thinking_panel()` | AI reasoning display |

## Mock Data

### Conversations
- Login Flow Analysis (Pinned)
- Dashboard Bug Discussion
- Test Optimization
- API Testing Strategy
- Locator Generation (Pinned)

### Quick Actions
- Generate Test Case
- Generate Feature File
- Generate Page Object
- Explain Failure
- Explain Locator
- Analyze DOM
- Generate Bug
- Optimize Test
- Create API Test
- SQL Validation
- Documentation
- Accessibility

### Prompt Templates
- Generate Login Test
- Generate Regression
- Generate Smoke Test
- Explain Bug
- Analyze Performance
- Accessibility Review
- API Test
- Screenshot Analysis

## Slash Commands

| Command | Description |
|---------|-------------|
| /new | Start new chat |
| /help | Show help |
| /tests | View test cases |
| /bugs | View bugs |
| /dom | Show DOM |
| /network | Network activity |
| /report | Generate report |
| /screenshot | Analyze screenshot |
| /locator | Show locator |
| /execution | Execution status |
| /history | Chat history |

## Design Principles

- **ChatGPT-style** interface
- **Cursor AI** context awareness
- **GitHub Copilot** code suggestions
- **Glassmorphism** styling
- **Professional** enterprise look

## Running the AI Chat Workspace

```bash
cd frontend
streamlit run app.py
```

Navigate to **💬 AI Chat** in the sidebar.

## Future Backend Integration Points

### API Endpoints

```python
# Get conversations
GET /api/v1/chat/conversations

# Get messages
GET /api/v1/chat/conversations/{id}/messages

# Send message
POST /api/v1/chat/messages

# Create conversation
POST /api/v1/chat/conversations

# Delete conversation
DELETE /api/v1/chat/conversations/{id}

# Get context
GET /api/v1/chat/context

# Search conversations
GET /api/v1/chat/search?q={query}
```

### WebSocket Events

```python
# Message received
{
    "event": "message_received",
    "role": "assistant",
    "content": "...",
    "timestamp": "..."
}

# Typing indicator
{
    "event": "typing_start"
}

{
    "event": "typing_stop"
}

# Stream chunk
{
    "event": "stream_chunk",
    "chunk": "..."
}
```

## Navigation Flow

```
Mission Planner → [Launch] → Intelligence Center → Execution Center
                                                        ↓
                                                    Human Review
                                                        ↓
                                              AI Chat Workspace ↔ Execution Context
                                                        ↓
                                                Mission Context Always Visible
```

## Key Visual Elements

### Chat Bubbles
- User: Gradient purple background, right-aligned
- AI: Dark panel, left-aligned, with avatar
- Code blocks with syntax highlighting
- Timestamp and action buttons

### Context Cards
- Mission, Execution, Bug, Screenshot, DOM, API
- Icon + Name + Description
- Click to inject context

### AI Thinking Panel
- Current thought
- Confidence score
- Reasoning
- Evidence
- Recommendation
- Next step

### Prompt Editor
- Multi-line input
- Placeholder with examples
- Slash command hints
- Send button
- Prompt suggestions
