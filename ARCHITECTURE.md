# GOAT Data Analyst Architecture


C:\Projects\goat-data-analyst\
│
├── main.py                 # FastAPI backend
├── app.py                  # Streamlit frontend
├── project-tracker.py      # Your debugging tool
│
├── 📂 backend/
│   ├── 📂 connectors/      # Data input
│   │   └── csv_handler.py
│   │
│   ├── 📂 processing/      # Data analysis
│   │   └── profiler.py
│   │
│   ├── 📂 domain/          # Domain detection
│   │   ├── keyword_detector.py  (rename domain_detector.py)
│   │   ├── ai_detector.py       (rename ai_domain_detector.py)
│   │   └── patterns.py
│   │
│   ├── 📂 analytics/       # Statistics & insights
│   │   ├── stats.py             (rename simple_analytics.py)
│   │   └── ai_insights.py
│   │
│   ├── 📂 charts/          # Visualizations
│   │   └── chart_builder.py     (rename universal_charts.py)
│   │
│   └── 📂 reports/         # HTML generation
│       ├── quality_section.py   (extract from quality_report.py)
│       ├── domain_section.py    (new)
│       ├── analytics_section.py (new)
│       ├── charts_section.py    (new)
│       ├── ai_section.py        (new)
│       └── assembler.py         (glues sections together)
│
├── 📂 tests/               # All test files
│   ├── test_ai_domains.py
│   ├── test_api.py
│   └── test_deployment.py
│
└── 📂 sample_data/         # Optional - keep or delete





## Current State (Dec 1, 2025)
- 38 Python files
- Monolithic report generation
- Need: modular puzzle-piece approach

## Target State (Phase 1 Goal)
- Section-based architecture
- Each HTML section = independent module
- Easy to add/remove features

## Next Refactoring
Split ultimate_report.py into:
- quality_section.py
- domain_section.py
- analytics_section.py
- charts_section.py
- ai_section.py
- assembler.py

# GOAT Data Analyst - Architecture

**Last Updated:** December 1, 2025

## Vision
Modular "puzzle piece" architecture where each component does ONE thing and can be added/removed independently.

## Current Structure

### Entry Points
- `main.py` - FastAPI backend (Railway)
- `app.py` - Streamlit frontend (Streamlit Cloud)

### Backend Modules

**Data Input**
- `backend/connectors/csv_handler.py` - CSV loading & encoding

**Data Processing**
- `backend/data_processing/profiler.py` - Column analysis & type detection

**Domain Detection**
- `backend/domain_detection/domain_detector.py` - Keyword-based detection
- `backend/domain_detection/ai_domain_detector.py` - AI-enhanced detection
- `backend/domain_detection/patterns.py` - Domain pattern definitions

**Analytics**
- `backend/analytics/simple_analytics.py` - Basic statistics
- `backend/analytics/ai_insights.py` - AI-generated insights (Groq)

**Visualizations**
- `backend/visualizations/universal_charts.py` - 4 chart types (time series, top-N, distribution, correlation)

**Report Generation**
- `backend/export_engine/quality_report.py` - Quality checks HTML
- `backend/export_engine/ultimate_report.py` - Assembles final report

## Refactoring Goal

Split `ultimate_report.py` into independent sections:

backend/reports/
├── sections/
│ ├── quality_section.py
│ ├── domain_section.py
│ ├── analytics_section.py
│ ├── charts_section.py
│ └── ai_section.py
└── assembler.py



## Phase 1 Priority

Extract sections we need to modify for Phase 1 roadmap:
1. Domain section (adjust wording)
2. AI insights section (improve prompts)

## Principles

- Each section = pure function (input → HTML output)
- No dependencies between sections
- Easy to add new sections
- Easy to remove sections
- Easy to test independently
