# ðŸ GOAT Data Analyst

**The AI analyst that understands context, identifies pain points, and provides clear guidance**

Enterprise-grade data analysis that goes beyond dashboardsâ€”GOAT provides human-like insights, actionable recommendations, and automated data fixes.

---

## âœ¨ Features

### ðŸŽ¯ Smart Analysis
- **Context Recognition**: Understands your data type (sales, finance, healthcare, etc.)
- **Data Quality Assessment**: Identifies missing values, duplicates, outliers
- **Automated Insights**: AI-powered pain point detection and action plans

### ðŸŽ¨ Beautiful Reports
- **4 Professional Themes**: Bold Borders, Glassmorphism, Color Coded, Neon Dark
- **Human-like Narrative**: "I See You", "What Hurts", "Your Path Forward"
- **Interactive Charts**: Built with Plotly

### ðŸ”§ Auto-Fix Tools
- One-click data cleaning
- Missing value handling
- Duplicate removal
- Date normalization

### ðŸ“Š Batch Analysis
- Analyze multiple files at once
- Company-level health dashboard
- Executive summary reports

---

## ðŸš€ Quick Start

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

## ðŸ”‘ Environment Variables

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

## ðŸ“ Project Structure

```
goat-data-analyst/
â”œâ”€â”€ app.py                      # Streamlit UI (main entry)
â”œâ”€â”€ main.py                     # FastAPI endpoints
â”œâ”€â”€ backend/
â”‚   â”œâ”€â”€ core/                   # AnalysisEngine + BatchEngine
â”‚   â”‚   â”œâ”€â”€ engine.py           # Main analysis orchestrator
â”‚   â”‚   â”œâ”€â”€ batch_engine.py     # Multi-file analysis
â”‚   â”‚   â””â”€â”€ models.py           # Data models
â”‚   â”œâ”€â”€ data_processing/        # Data operations
â”‚   â”‚   â”œâ”€â”€ profiler.py         # Data profiling
â”‚   â”‚   â””â”€â”€ data_fixer.py       # Auto-fix tools
â”‚   â”œâ”€â”€ domain_detection/       # Business type detection
â”‚   â”‚   â”œâ”€â”€ detector.py
â”‚   â”‚   â””â”€â”€ patterns.py
â”‚   â”œâ”€â”€ ai/                     # AI insights (optional)
â”‚   â”‚   â””â”€â”€ ai_engine.py
â”‚   â”œâ”€â”€ narrative/              # Human-like reports
â”‚   â”‚   â””â”€â”€ narrative_generator.py
â”‚   â”œâ”€â”€ visualizations/         # Chart engine
â”‚   â”‚   â”œâ”€â”€ chart_orchestrator.py
â”‚   â”‚   â”œâ”€â”€ profile_intelligence.py
â”‚   â”‚   â””â”€â”€ charts/             # Individual chart types
â”‚   â”‚       â”œâ”€â”€ category_chart.py
â”‚   â”‚       â”œâ”€â”€ distribution_chart.py
â”‚   â”‚       â””â”€â”€ timeseries_chart.py
â”‚   â”œâ”€â”€ reports/                # 4 themed report styles
â”‚   â”‚   â”œâ”€â”€ style_a_bold_borders.py
â”‚   â”‚   â”œâ”€â”€ style_b_glassmorphism.py
â”‚   â”‚   â”œâ”€â”€ style_c_color_coded.py
â”‚   â”‚   â”œâ”€â”€ style_d_neon_tech.py
â”‚   â”‚   â””â”€â”€ company_health_report.py
â”‚   â”œâ”€â”€ auth/                   # Authentication (Day 21-23)
â”‚   â”‚   â”œâ”€â”€ auth_manager.py
â”‚   â”‚   â””â”€â”€ streamlit_auth.py
â”‚   â””â”€â”€ middleware/             # Rate limiting (Day 24)
â”‚       â””â”€â”€ rate_limiter.py
â””â”€â”€ sample_data/                # Example datasets
```

---

## ðŸ› ï¸ Tech Stack

- **UI**: Streamlit
- **API**: FastAPI
- **Data**: Pandas, NumPy
- **Viz**: Plotly
- **AI**: Groq (optional)
- **Auth**: Supabase
- **Deployment**: Railway, Streamlit Cloud

---

## ðŸŒ Live Demo

- **Streamlit UI**: https://goat-data-analyst-a6idzyddvy2pevnsqdzskt.streamlit.app/
- **API Docs**: https://goat-data-analyst-production.up.railway.app/docs

---

## ðŸ“– Usage

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

## ðŸ—ï¸ Architecture

```
CSV â†’ AnalysisEngine â†’ AnalysisResult â†’ Report (HTML)
         â†“
    [DataProfiler]
    [DomainDetector]
    [QualityAnalyzer]
    [NarrativeGenerator]
    [ChartOrchestrator]
```

**Key Principle**: One central brain (`AnalysisEngine`) orchestrates all plugins.

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed documentation.

---

## ðŸŽ¯ Development Roadmap

**Completed (Days 1-24):**
- âœ… Clean architecture with single AnalysisEngine
- âœ… Human-like narrative system
- âœ… Auto-fix data quality tools
- âœ… Batch/folder analysis
- âœ… 4 professional report themes
- âœ… Deployment-ready code
- âœ… Supabase authentication (Day 21-23)
- âœ… Rate limiting protection (Day 24)

**In Progress (Days 25-40):**
- ðŸ”„ Secure API keys & secrets (Day 25)
- â³ Error handling & validation
- â³ Performance optimization
- â³ Monitoring & logging
- â³ Production deployment

**Future Enhancements:**
- Database connectors (Postgres, MySQL, Snowflake)
- Slack bot integration
- Real-time monitoring
- Team collaboration features

---

## ðŸ¤ Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit PR

---

## ðŸ“„ License

MIT License

---

## ðŸ‘¨â€ðŸ’» Author

Built with ðŸ by **ojayWillow**

**GitHub**: https://github.com/ojayWillow/goat-data-analyst

---

**Made with ðŸ by GOAT Data Analyst**
