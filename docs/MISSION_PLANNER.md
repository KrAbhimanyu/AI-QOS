# Mission Planner Documentation

## Overview

The Mission Planner is the heart of AI-QOS - a multi-step wizard for creating and configuring AI-powered testing missions. It provides a professional, enterprise-grade interface similar to creating a GitHub Action, Azure DevOps Pipeline, or Cursor AI Task.

## Features

- **5-Step Wizard** - Structured mission creation process
- **Session State Persistence** - Progress saved between steps
- **Real-time Validation** - Prevents invalid configurations
- **Glassmorphism UI** - Modern, professional design
- **AI Assistant Panel** - Context-aware tips and suggestions
- **Progress Tracking** - Visual step completion indicators

## Folder Structure

```
frontend/
├── pages/
│   └── mission_planner.py     # Main wizard page
├── components/
│   └── wizard_components.py   # Reusable wizard components
└── ...
```

## Session State Flow

```python
# Initial State
st.session_state.wizard_step = 1
st.session_state.wizard_data = {
    "mission_name": "",
    "mission_description": "",
    "project": "",
    "app_name": "",
    "app_url": "",
    "environment": None,
    "auth_required": None,
    "credentials": {"username": "", "password": ""},
    "estimated_time": "",
    "priority": None,
    "uploaded_files": [],
    "testing_types": [],
    "execution_mode": None,
    "parallel_workers": 1,
    "browser": None,
    "retry_count": 1,
    "timeout": 30,
    "screenshots": True,
    "video_recording": False,
    "logs_enabled": True,
    "generate_docs": True,
    "generate_bug_report": True,
}
st.session_state.wizard_validated = {}
```

## Navigation Flow

```
┌─────────────────────────────────────────────────────────┐
│                    WIZARD FLOW                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Step 1          Step 2          Step 3                 │
│  ┌─────┐    →    ┌─────┐    →    ┌─────┐              │
│  │Info │         │Docs │         │Test │              │
│  └─────┘    ←    └─────┘    ←    └─────┘              │
│    ↑                               │                    │
│    │                               │                    │
│  [Back]                         [Next]                 │
│                                  ↓                      │
│  Step 5          Step 4                               │
│  ┌─────┐    ←    ┌─────┐                               │
│  │Summ │         │Config│                              │
│  │     │  [Back] └─────┘                               │
│  │Launch│                                              │
│  └─────┘                                               │
└─────────────────────────────────────────────────────────┘
```

## Validation Rules

| Step | Field | Rule |
|------|-------|------|
| 1 | Mission Name | Required |
| 1 | Application URL | Required |
| 1 | Environment | Required |
| 1 | Priority | Required |
| 1 | Credentials | Required if auth_required = Yes |
| 2 | Uploaded Files | Optional |
| 3 | Testing Types | At least one required |
| 4 | Execution Mode | Required |
| 4 | Browser | Required |

## Components

### Wizard Components (`wizard_components.py`)

| Component | Description |
|-----------|-------------|
| `init_wizard_state()` | Initialize session state for wizard |
| `get_wizard_data()` | Get data from wizard state |
| `set_wizard_data()` | Set data in wizard state |
| `validate_step()` | Validate current step |
| `wizard_stepper()` | Horizontal progress indicator |
| `validation_badge()` | Show validation status |
| `step_section()` | Step section header |
| `glass_card()` | Glassmorphism card container |
| `input_field()` | Styled input field |
| `select_field()` | Styled select field |
| `checkbox_field()` | Styled checkbox field |
| `file_upload_card()` | File upload card |
| `testing_type_card()` | Selectable testing type card |
| `config_card()` | Configuration card |
| `summary_item()` | Summary list item |
| `ai_assistant_panel()` | AI tips sidebar |
| `progress_sidebar()` | Step progress sidebar |
| `wizard_actions()` | Action buttons |

## Step Details

### Step 1: Mission Information
- Mission Name (required)
- Mission Description
- Project selection
- Application Name
- Application URL (required)
- Environment (required)
- Priority (required)
- Estimated Execution Time
- Authentication toggle
- Credentials (if auth required)

### Step 2: Upload Documents
- Excel Test Cases
- BRD Document
- PRD Document
- Swagger/OpenAPI
- Postman Collection
- Feature Files
- Drag and drop upload
- File list with remove option

### Step 3: Testing Types
- 14 testing types available
- Beautiful selectable cards
- Quick selection presets
- Estimated time per type
- Multi-select functionality

### Step 4: Execution Configuration
- Execution Mode (Autonomous/Review/Hybrid/Manual)
- Parallel Workers (1-10)
- Browser Selection
- Retry Count
- Timeout
- Screenshots toggle
- Video Recording toggle
- Logs toggle
- Documentation generation toggle
- Bug Report generation toggle

### Step 5: Mission Summary
- Complete mission overview
- Selected testing types
- Uploaded files
- Execution configuration
- Estimated coverage
- Estimated cost

## Future Backend Integration Points

### API Endpoints (Future)

```python
# Mission Creation
POST /api/v1/missions
{
    "name": "Mission Name",
    "description": "Mission Description",
    "project_id": "uuid",
    "application": {
        "name": "App Name",
        "url": "https://app.example.com",
        "environment": "staging"
    },
    "testing_types": ["api", "smoke", "regression"],
    "files": ["file_id_1", "file_id_2"],
    "configuration": {
        "mode": "autonomous",
        "workers": 4,
        "browser": "chrome",
        "retries": 1,
        "timeout": 30
    }
}

# File Upload
POST /api/v1/uploads
Content-Type: multipart/form-data

# Get Mission Status
GET /api/v1/missions/{mission_id}

# List Missions
GET /api/v1/missions
```

### Database Schema (Future)

```sql
-- Missions Table
CREATE TABLE missions (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    project_id UUID,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    status VARCHAR(50),
    priority VARCHAR(20)
);

-- Mission Configurations
CREATE TABLE mission_configs (
    mission_id UUID REFERENCES missions(id),
    testing_types JSONB,
    execution_mode VARCHAR(50),
    parallel_workers INTEGER,
    browser VARCHAR(50),
    -- ... other config fields
);
```

## Design Principles

- **Dark Theme** - Consistent with AI-QOS design system
- **Glassmorphism** - Subtle blur effects on cards
- **Minimal** - Clean, uncluttered interface
- **Professional** - Enterprise-grade appearance
- **Responsive** - Adapts to different screen sizes
- **Accessible** - Clear labels and proper contrast

## Running the Wizard

```bash
cd frontend
streamlit run app.py
```

Navigate to "Mission Planner" in the sidebar to access the wizard.

## Keyboard Shortcuts

- `Tab` - Navigate between fields
- `Enter` - Submit/Continue
- `Escape` - Cancel (with confirmation)

## Future Improvements

- [ ] Add keyboard navigation between steps
- [ ] Auto-save draft every 30 seconds
- [ ] Import mission from template
- [ ] Clone existing mission
- [ ] Add more file type support
- [ ] Custom testing type creation
- [ ] Save as template functionality
- [ ] Real-time collaboration
- [ ] Mission preview before launch
- [ ] Schedule mission execution
