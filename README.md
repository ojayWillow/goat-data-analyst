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

```bash
# Clone repository
git clone https://github.com/ojayWillow/goat-data-analyst.git
cd goat-data-analyst

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Run Locally

```bash
# Streamlit UI
streamlit run app.py

# FastAPI Backend (optional)
uvicorn main:app --reload
```

---

## 🔑 Environment Variables

Create `.env` file from template:

```bash
cp .env.example .env
```

Required variables:

```bash
# AI APIs
PERPLEXITY_API_KEY=your_perplexity_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# Supabase Auth
SUPABASE_URL=your_supabase_project_url_here
SUPABASE_KEY=your_supabase_anon_key_here
SECRET_KEY=your_secret_key_for_jwt_here
```

**Setup Instructions:**
1. Copy `.env.example` to `.env`
2. Get API keys:
   - **Perplexity**: https://www.perplexity.ai/settings/api
   - **Groq**: https://console.groq.com/keys
   - **Supabase**: https://supabase.com/dashboard (project settings)
3. Add keys to `.env` file
4. Never commit `.env` to Git (already in .gitignore)

**Without API keys**: System uses rule-based analysis (limited features)

---

## 📁 Project Structure

```
goat-data-analyst/
├── app.py                      # Streamlit UI (main entry)
├── main.py                     # FastAPI endpoints
├── backend/
│   ├── core/                   # AnalysisEngine + BatchEngine
│   │   ├── engine.py           # Main analysis orchestrator
│   │   ├── batch_engine.py     # Multi-file analysis
│   │   └── models.py           # Data models
│   ├── data_processing/        # Data operations
│   │   ├── profiler.py         # Data profiling
│   │   └── data_fixer.py       # Auto-fix tools
│   ├── domain_detection/       # Business type detection
│   │   ├── detector.py
│   │   └── patterns.py
│   ├── ai/                     # AI insights (optional)
│   │   └── ai_engine.py
│   ├── narrative/              # Human-like reports
│   │   └── narrative_generator.py
│   ├── visualizations/         # Chart engine
│   │   ├── chart_orchestrator.py
│   │   ├── profile_intelligence.py
│   │   └── charts/             # Individual chart types
│   │       ├── category_chart.py
│   │       ├── distribution_chart.py
│   │       └── timeseries_chart.py
│   ├── reports/                # 4 themed report styles
│   │   ├── style_a_bold_borders.py
│   │   ├── style_b_glassmorphism.py
│   │   ├── style_c_color_coded.py
│   │   ├── style_d_neon_tech.py
│   │   └── company_health_report.py
│   ├── auth/                   # Authentication (Day 21-23)
│   │   ├── auth_manager.py
│   │   └── streamlit_auth.py
│   └── middleware/             # Rate limiting (Day 24)
│       └── rate_limiter.py
└── sample_data/                # Example datasets
```

---

## 🛠️ Tech Stack

- **UI**: Streamlit
- **API**: FastAPI
- **Data**: Pandas, NumPy
- **Viz**: Plotly
- **AI**: Groq (optional)
- **Auth**: Supabase
- **Deployment**: Railway, Streamlit Cloud

---

## 🌐 Live Demo

- **Streamlit UI**: https://goat-data-analyst-a6idzyddvy2pevnsqdzskt.streamlit.app/
- **API Docs**: https://goat-data-analyst-production.up.railway.app/docs

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

```
CSV → AnalysisEngine → AnalysisResult → Report (HTML)
         ↓
    [DataProfiler]
    [DomainDetector]
    [QualityAnalyzer]
    [NarrativeGenerator]
    [ChartOrchestrator]
```

**Key Principle**: One central brain (`AnalysisEngine`) orchestrates all plugins.

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed documentation.

---

## 🎯 Development Roadmap

**Completed (Days 1-24):**
- ✅ Clean architecture with single AnalysisEngine
- ✅ Human-like narrative system
- ✅ Auto-fix data quality tools
- ✅ Batch/folder analysis
- ✅ 4 professional report themes
- ✅ Deployment-ready code
- ✅ Supabase authentication (Day 21-23)
- ✅ Rate limiting protection (Day 24)

**In Progress (Days 25-40):**
- 🔄 Secure API keys & secrets (Day 25)
- ⏳ Error handling & validation
- ⏳ Performance optimization
- ⏳ Monitoring & logging
- ⏳ Production deployment

**Future Enhancements:**
- Database connectors (Postgres, MySQL, Snowflake)
- Slack bot integration
- Real-time monitoring
- Team collaboration features

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