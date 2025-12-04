# 🐐 GOAT Data Analyst

**The AI analyst that understands context, identifies pain points, and provides clear guidance**

Enterprise-grade data analysis that goes beyond dashboards—GOAT provides human-like insights, actionable recommendations, and automated data fixes.

---

## ✨ Features

### 🎯 Smart Analysis
- **Context Recognition**: Understands your data type (sales, finance, healthcare, etc.)
- **Data Quality Assessment**: Identifies missing values, duplicates, outliers
- **Automated Insights**: AI-powered pain point detection and action plans

### 🎨 Beautiful Reports
- **4 Professional Themes**: Bold Borders, Glassmorphism, Color Coded, Neon Dark
- **Human-like Narrative**: "I See You", "What Hurts", "Your Path Forward"
- **Interactive Charts**: Built with Plotly

### 🔧 Auto-Fix Tools
- One-click data cleaning
- Missing value handling
- Duplicate removal
- Date normalization

### 📊 Batch Analysis
- Analyze multiple files at once
- Company-level health dashboard
- Executive summary reports

---

## 🚀 Quick Start

### Installation

Clone repository
git clone https://github.com/ojayWillow/goat-data-analyst.git
cd goat-data-analyst

Install dependencies
pip install -r requirements.txt

Optional: Set up AI features
Add GROQ_API_KEY to .env file


### Run Locally

Streamlit UI
streamlit run app.py

FastAPI Backend (optional)
uvicorn main:app --reload


---

## 📁 Project Structure

goat-data-analyst/
├── app.py # Streamlit UI (main entry)
├── main.py # FastAPI endpoints
├── backend/
│ ├── core/ # AnalysisEngine + BatchEngine
│ │ ├── engine.py # Main analysis orchestrator
│ │ ├── batch_engine.py # Multi-file analysis
│ │ └── models.py # Data models
│ ├── data_processing/ # Data operations
│ │ ├── profiler.py # Data profiling
│ │ └── data_fixer.py # Auto-fix tools
│ ├── domain_detection/ # Business type detection
│ │ ├── detector.py
│ │ └── patterns.py
│ ├── ai/ # AI insights (optional)
│ │ └── ai_engine.py
│ ├── narrative/ # Human-like reports
│ │ └── narrative_generator.py
│ ├── visualizations/ # Chart engine
│ │ ├── chart_orchestrator.py
│ │ ├── profile_intelligence.py
│ │ └── charts/ # Individual chart types
│ │ ├── category_chart.py
│ │ ├── distribution_chart.py
│ │ └── timeseries_chart.py
│ └── reports/ # 4 themed report styles
│ ├── style_a_bold_borders.py
│ ├── style_b_glassmorphism.py
│ ├── style_c_color_coded.py
│ ├── style_d_neon_tech.py
│ └── company_health_report.py
└── sample_data/ # Example datasets


---

## 🛠️ Tech Stack

- **UI**: Streamlit
- **API**: FastAPI
- **Data**: Pandas, NumPy
- **Viz**: Plotly
- **AI**: Groq (optional)
- **Deployment**: Railway, Streamlit Cloud

---

## 🌐 Live Demo

- **Streamlit UI**: https://goat-data-analyst-a6idzyddvy2pevnsqdzskt.streamlit.app/
- **API Docs**: https://goat-data-analyst-production.up.railway.app/docs

---

## 🔑 Environment Variables

Create `.env` file (optional for AI features):

GROQ_API_KEY=your_key_here


**Without API key**: System uses rule-based analysis (still works great!)

---

## 📖 Usage

### Single File Analysis
1. Upload CSV file
2. Choose report style (A/B/C/D)
3. Click "Run Analysis"
4. Get instant insights + recommendations
5. Download cleaned data if needed

### Multiple Files Analysis
1. Upload folder or multiple CSVs
2. Get company-level health dashboard
3. Drill into individual file reports
4. Export executive summary

---

## 🏗️ Architecture

CSV → AnalysisEngine → AnalysisResult → Report (HTML)
↓
[DataProfiler]
[DomainDetector]
[QualityAnalyzer]
[NarrativeGenerator]
[ChartOrchestrator]


**Key Principle**: One central brain (`AnalysisEngine`) orchestrates all plugins.

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed documentation.

---

## 🎯 Development Roadmap

**Completed (Days 1-19):**
- ✅ Clean architecture with single AnalysisEngine
- ✅ Human-like narrative system
- ✅ Auto-fix data quality tools
- ✅ Batch/folder analysis
- ✅ 4 professional report themes
- ✅ Deployment-ready code

**Future Enhancements:**
- Database connectors (Postgres, MySQL, Snowflake)
- Slack bot integration
- Real-time monitoring
- Team collaboration features
- API authentication

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit PR

---

## 📄 License

MIT License

---

## 👨‍💻 Author

Built with 🐐 by **ojayWillow**

**GitHub**: https://github.com/ojayWillow/goat-data-analyst

---

**Made with 🐐 by GOAT Data Analyst**
