# AI-QOS Frontend

Enterprise-grade Streamlit frontend for AI Quality Operating System.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## 📁 Folder Structure

```
frontend/
├── app.py                 # Main Streamlit application
├── pages/                 # Page components
│   ├── dashboard.py       # Dashboard page
│   ├── missions.py        # Missions management
│   ├── agents.py          # AI agents management
│   ├── executions.py      # Execution tracking
│   ├── monitoring.py       # System monitoring
│   ├── quality.py          # Quality metrics
│   └── reports.py          # Reports generation
├── components/            # Reusable UI components
│   └── core_components.py # Core component library
├── themes/                # Theme configuration
│   └── theme_config.py    # Dark theme settings
├── config/                 # Application configuration
│   └── app_config.py       # App settings
├── utils/                  # Utility functions
│   └── helpers.py          # Helper functions
└── requirements.txt        # Python dependencies
```

## 🎨 UI Components

### Metric Card
Display key metrics with optional delta indicators.

### Status Badge
Visual status indicators for missions and agents.

### Mission Card
Card component for displaying mission information.

### Agent Card
Card component for displaying agent details.

### Page Header
Standardized page header with title, subtitle, and actions.

## 🎨 Design System

### Colors
- **Primary**: #6366F1 (Indigo)
- **Secondary**: #22D3EE (Cyan)
- **Accent**: #F472B6 (Pink)
- **Success**: #10B981 (Green)
- **Warning**: #F59E0B (Amber)
- **Error**: #EF4444 (Red)

### Typography
- Font Family: Inter
- Headings: 600 weight
- Body: 400 weight

### Components
- Border Radius: 12px
- Shadow: 0 4px 20px rgba(0, 0, 0, 0.4)
- Glass Effect: rgba(30, 30, 63, 0.8)

## 📝 Development

### Adding New Pages

1. Create a new file in `pages/`
2. Implement `render_page_name()` function
3. Import and route in `app.py`

### Adding Components

1. Add component function to `components/core_components.py`
2. Follow naming conventions: `component_name()`
3. Use consistent styling with theme

## 🔮 Future Improvements

- [ ] Add user authentication
- [ ] Implement real-time WebSocket updates
- [ ] Add more chart types
- [ ] Implement mobile responsive design
- [ ] Add export functionality (PDF, CSV)
- [ ] Implement dark/light theme toggle
