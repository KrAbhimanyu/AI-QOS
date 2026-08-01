# AI-QOS Documentation

Documentation for AI Quality Operating System.

## 📚 Contents

- [Frontend Documentation](../frontend/README.md)
- [API Documentation](./api.md) *(planned)*
- [Architecture](./architecture.md) *(planned)*
- [Deployment](./deployment.md) *(planned)*

## 🏗️ Architecture

AI-QOS follows a component-based architecture:

```
┌─────────────────────────────────────────┐
│           Streamlit Frontend            │
│  ┌─────────────────────────────────┐    │
│  │     Pages (Dashboard, etc.)     │    │
│  ├─────────────────────────────────┤    │
│  │     Components (Cards, etc.)     │    │
│  ├─────────────────────────────────┤    │
│  │     Theme & Configuration        │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

## 📋 Pages Overview

| Page | Description |
|------|-------------|
| Dashboard | System overview and key metrics |
| Missions | Mission creation and management |
| Agents | AI agent monitoring |
| Executions | Execution history tracking |
| Monitoring | Real-time system health |
| Quality | Code quality metrics |
| Reports | Report generation |

## 🔧 Configuration

See [frontend/config/app_config.py](../frontend/config/app_config.py) for configuration options.

## 🚀 Deployment

See [deployment.md](./deployment.md) for deployment instructions.
