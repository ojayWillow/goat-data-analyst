# 🏆 GOAT Data Analyst - Enterprise Edition

AI-powered data analyst agent that automatically analyzes business data and generates insights.

## 🎯 Features

- ✅ Auto-detects 20+ business types
- ✅ Runs 20+ advanced analyses
- ✅ AI-generated insights & recommendations
- ✅ Beautiful dashboards & reports
- ✅ Professional PDF & Excel exports

## 📊 Current Status

**Stage 0 - Foundation (Week 1)**
- [x] Project structure created
- [ ] CSV data pipeline
- [ ] Domain detection
- [ ] RFM analysis
- [ ] AI insights
- [ ] REST API

## 🚀 Quick Start

\\\ash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Start API server
python backend/api/main.py

# Start dashboard
streamlit run frontend/streamlit_app/app.py
\\\

## 📁 Project Structure

\\\
goat-data-analyst/
├── backend/
│   ├── connectors/         # CSV/Excel/API data connectors
│   ├── domain_detection/   # Auto-detect business type
│   ├── data_processing/    # Cleaning, validation, profiling
│   ├── analyzers/         # Analysis modules (RFM, LTV, etc.)
│   ├── ai_engine/         # OpenAI integration
│   ├── visualizations/    # Chart generators
│   ├── export_engine/     # PDF/Excel export
│   └── api/               # FastAPI REST endpoints
├── frontend/
│   └── streamlit_app/     # Interactive dashboard
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
├── sample_data/
└── infrastructure/
\\\

## 🛠️ Tech Stack

- **Backend:** Python 3.11+, FastAPI, Pandas
- **AI:** OpenAI GPT-4
- **Visualization:** Plotly, Streamlit
- **Testing:** pytest
- **Deployment:** Docker, GitHub Actions

## 📝 License

MIT License
