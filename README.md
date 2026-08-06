# AI-QOS - Agent Control Tower

## 🎛️ Enterprise AI Agent Monitoring Dashboard

The Agent Control Tower is a comprehensive command center for observing and managing AI agents working together in real-time. Built with Streamlit, it provides enterprise-grade monitoring capabilities inspired by Kubernetes Dashboard, Datadog, and Mission Control.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## ✨ Features

### 🤖 Agent Monitoring
- Real-time agent status tracking across 16 different AI agents
- Health monitoring with confidence scores
- CPU, Memory, and GPU utilization per agent
- Execution metrics and message processing counts

### 🔀 Communication Pipeline
- Visual representation of agent communication flow
- Animated message passing between agents
- Pipeline state tracking

### 📊 Resource Dashboard
- System-wide CPU, Memory, GPU usage
- Token usage tracking (input/output/total)
- Latency metrics (avg, p95, p99)
- Queue status visualization

### 🤖 AI Model Panel
- Multi-model support visualization
- Request distribution across models
- Model routing simulation

### 💚 Health Monitoring
- Overall health score
- Resource health metrics
- Failure and retry rates
- Active warnings tracking

### 🔔 Event Stream
- Real-time event feed
- Event categorization (info, success, warning, error)
- Timeline visualization

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/AI-QOS.git
cd AI-QOS

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Run from root
streamlit run app.py

# Or run directly
streamlit run pages/Agent_Control_Tower.py
```

### Access
Open your browser and navigate to:
- **Local**: http://localhost:8501
- **Network**: http://[your-ip]:8501

---

## 📁 Project Structure

```
AI-QOS/
├── app.py                      # Main entry point
├── pages/
│   └── Agent_Control_Tower.py  # Main dashboard page
├── src/
│   ├── components/             # UI components
│   │   ├── agent_card.py       # Agent card display
│   │   ├── agent_drawer.py     # Detailed agent panel
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
│   ├── README.md
│   ├── ARCHITECTURE.md
│   ├── COMPONENTS.md
│   └── BACKEND_INTEGRATION.md
├── requirements.txt            # Dependencies
└── pyproject.toml              # Project configuration
```

---

## 🤖 Supported Agents

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

### Documentation & Support
- Documentation Agent
- Bug Analysis Agent
- Release Advisor Agent
- Learning Agent

### Security
- Security Testing Agent

---

## 🎨 Design System

The Control Tower uses a glassmorphism design system featuring:
- Dark theme with blue/purple accents
- Translucent glass-like panels
- Smooth animations and transitions
- Responsive layout
- Enterprise-grade aesthetics

---

## 🔧 Configuration

### Environment Variables

```bash
# Optional configuration
REFRESH_INTERVAL=5  # Auto-refresh interval in seconds
```

### Customization

Modify `src/styles/theme.py` to customize:
- Color scheme
- Glassmorphism effects
- Animation timing
- Typography

---

## 📖 Documentation

- [Architecture Documentation](docs/ARCHITECTURE.md)
- [Component Documentation](docs/COMPONENTS.md)
- [Backend Integration Guide](docs/BACKEND_INTEGRATION.md)

---

## 🔮 Future Enhancements

- [ ] Real backend API integration
- [ ] WebSocket support for live updates
- [ ] User authentication
- [ ] Agent control actions (start/stop/pause)
- [ ] Custom agent creation
- [ ] Alerting system
- [ ] Export capabilities
- [ ] Dark/Light theme toggle

---

## 📝 License

MIT License - See LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

---

## 📧 Contact

For questions and support, please open an issue on GitHub.