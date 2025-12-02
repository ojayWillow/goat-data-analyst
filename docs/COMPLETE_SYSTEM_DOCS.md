# GOAT Data Analyst - Complete System Documentation

**Generated:** December 2, 2025  
**Purpose:** Full technical reference for all Python modules, connections, and data flow

---

## Table of Contents
1. [System Architecture](#1-system-architecture)
2. [Complete Data Flow](#2-complete-data-flow)
3. [Module Reference](#3-module-reference)
4. [Connection Maps](#4-connection-maps)
5. [API Endpoints](#5-api-endpoints)
6. [Testing Commands](#6-testing-commands)
7. [Deployment](#7-deployment)

---

## 1. System Architecture

### Core Pipeline
```
CSV Upload → Profile → Detect Domain → Analyze → Visualize → Assemble → Export
```

### Layer Structure
```
┌─────────────────────────────────────────────┐
│ ENTRY LAYER                                 │
│ main.py (FastAPI) | app.py (Streamlit)     │
└──────────────┬──────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│ PROCESSING LAYER                             │
│ backend/data_processing/profiler.py          │
│ - DataProfiler.profile(df)                   │
└──────────────┬───────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│ DETECTION LAYER                              │
│ backend/domain_detection/                    │
│ - domain_detector.py (rule-based)            │
│ - ai_domain_detector.py (AI-powered)         │
└──────────────┬───────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│ ANALYTICS LAYER                              │
│ backend/analytics/                           │
│ - simple_analytics.py                        │
│ - ai_insights.py                             │
└──────────────┬───────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│ VISUALIZATION LAYER                          │
│ backend/visualizations/universal_charts.py   │
└──────────────┬───────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│ ASSEMBLY LAYER                               │
│ backend/reports/assembler.py                 │
│ ├─ sections/quality_section.py               │
│ ├─ sections/domain_section.py                │
│ ├─ sections/ai_section.py                    │
│ └─ sections/charts_section.py                │
└──────────────┬───────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│ EXPORT LAYER                                 │
│ backend/export_engine/ultimate_report.py     │
└──────────────────────────────────────────────┘
```

---

## 2. Complete Data Flow

### Step-by-Step Execution

```
┌─────────────────────────────────────────────┐
│ 1. USER UPLOADS CSV                         │
│    - Via FastAPI: POST /analyze             │
│    - Via Streamlit: file_uploader()         │
└──────────────┬──────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│ 2. DATA PROFILING                            │
│    File: backend/data_processing/profiler.py │
│    Class: DataProfiler                       │
│    Method: profile(df: pd.DataFrame)         │
│    Output: profile = {                       │
│        "row_count": 1000,                    │
│        "column_count": 5,                    │
│        "missing_values": {...},              │
│        "data_types": {...},                  │
│        "quality_score": 85.5                 │
│    }                                         │
└──────────────┬───────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│ 3. DOMAIN DETECTION                          │
│    File: backend/domain_detection/           │
│    Classes:                                  │
│    - DomainDetector (rule-based)             │
│    - AIDomainDetector (AI-powered)           │
│    Method: detect(df)                        │
│    Output: domain = {                        │
│        "domain": "sales",                    │
│        "confidence": 0.92,                   │
│        "indicators": ["revenue", "customer"] │
│    }                                         │
└──────────────┬───────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│ 4. ANALYTICS GENERATION                      │
│    File: backend/analytics/                  │
│    Classes:                                  │
│    - SimpleAnalytics (basic stats)           │
│    - AIInsightsEngine (AI insights)          │
│    Method: generate_insights(profile)        │
│    Output: insights = [                      │
│        {                                     │
│            "type": "correlation",            │
│            "description": "Strong positive", │
│            "severity": "high"                │
│        }                                     │
│    ]                                         │
└──────────────┬───────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│ 5. CHART GENERATION                          │
│    File: backend/visualizations/             │
│    Class: UniversalChartGenerator            │
│    Method: generate(df, domain)              │
│    Output: charts = [                        │
│        {                                     │
│            "type": "bar",                    │
│            "data": {...},                    │
│            "config": {...}                   │
│        }                                     │
│    ]                                         │
└──────────────┬───────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│ 6. REPORT ASSEMBLY                           │
│    File: backend/reports/assembler.py        │
│    Class: ReportAssembler                    │
│    Method: assemble(profile, domain,         │
│                     insights, charts)        │
│    Uses:                                     │
│    - QualitySection (quality metrics)        │
│    - DomainSection (domain info)             │
│    - AISection (insights)                    │
│    - ChartsSection (visualizations)          │
│    Output: report = {                        │
│        "quality": {...},                     │
│        "domain": {...},                      │
│        "insights": {...},                    │
│        "charts": {...}                       │
│    }                                         │
└──────────────┬───────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│ 7. EXPORT TO HTML/PDF                        │
│    File: backend/export_engine/              │
│    Class: UltimateReportGenerator            │
│    Method: generate(report)                  │
│    Output: HTML string                       │
└──────────────┬───────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│ 8. RETURN TO USER                            │
│    - FastAPI: JSON or HTML response          │
│    - Streamlit: Download button              │
└──────────────────────────────────────────────┘
```

---

## 3. Module Reference

### 3.1 main.py (FastAPI Backend)

**Location:** Root directory  
**Purpose:** REST API for CSV analysis

#### Imports
```python
# External
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Internal
from backend.data_processing.profiler import DataProfiler
from backend.domain_detection.domain_detector import DomainDetector
from backend.domain_detection.ai_domain_detector import AIDomainDetector
from backend.analytics.simple_analytics import SimpleAnalytics
from backend.analytics.ai_insights import AIInsightsEngine
from backend.visualizations.universal_charts import UniversalChartGenerator
from backend.export_engine.ultimate_report import UltimateReportGenerator
```

#### Key Functions
```python
@app.post("/analyze")
async def analyze_csv(file: UploadFile):
    # 1. Read CSV
    df = pd.read_csv(file.file)
    
    # 2. Profile data
    profiler = DataProfiler()
    profile = profiler.profile(df)
    
    # 3. Detect domain
    detector = DomainDetector()
    domain = detector.detect(df)
    
    # 4. Generate insights
    insights_engine = AIInsightsEngine()
    insights = insights_engine.generate_insights(profile)
    
    # 5. Generate charts
    chart_gen = UniversalChartGenerator()
    charts = chart_gen.generate(df, domain)
    
    # 6. Assemble report
    assembler = ReportAssembler()
    report = assembler.assemble(profile, domain, insights, charts)
    
    # 7. Return JSON
    return report
```

#### Endpoints
- `GET /` - Health check
- `POST /analyze` - Returns JSON report
- `POST /full-report` - Returns HTML report

---

### 3.2 app.py (Streamlit Frontend)

**Location:** Root directory  
**Purpose:** Web UI for CSV upload and analysis

#### Imports
```python
import streamlit as st
import pandas as pd
from datetime import datetime
from backend.data_processing.profiler import DataProfiler
from backend.export_engine.ultimate_report import UltimateReportGenerator
```

#### Key Functions
```python
def main():
    # 1. File upload
    uploaded_file = st.file_uploader("Upload CSV")
    
    # 2. Read CSV
    df = pd.read_csv(uploaded_file)
    
    # 3. Profile data
    profiler = DataProfiler()
    profile = profiler.profile(df)
    
    # 4. Display metrics
    st.metric("Rows", profile['row_count'])
    st.metric("Quality Score", profile['quality_score'])
    
    # 5. Generate report
    report_gen = UltimateReportGenerator()
    html_report = report_gen.generate(profile)
    
    # 6. Download button
    st.download_button("Download Report", html_report)
```

---

### 3.3 DataProfiler

**Location:** `backend/data_processing/profiler.py`  
**Purpose:** Analyzes data quality and statistics

#### Class: DataProfiler

**Method:** `profile(df: pd.DataFrame) -> Dict[str, Any]`

**Returns:**
```python
{
    "row_count": int,              # Total rows
    "column_count": int,           # Total columns
    "missing_values": {            # Missing per column
        "column_name": count
    },
    "data_types": {                # Type per column
        "column_name": "numeric" | "categorical" | "datetime"
    },
    "numeric_stats": {             # Stats for numeric columns
        "column_name": {
            "mean": float,
            "median": float,
            "std": float,
            "min": float,
            "max": float
        }
    },
    "categorical_stats": {         # Stats for categorical columns
        "column_name": {
            "unique_count": int,
            "top_value": str,
            "frequency": int
        }
    },
    "date_columns": List[str],     # Datetime columns
    "quality_score": float,        # 0-100 score
    "timestamp": str               # Generation time
}
```

**Used By:**
- main.py
- app.py
- ReportAssembler

---

### 3.4 DomainDetector

**Location:** `backend/domain_detection/domain_detector.py`  
**Purpose:** Rule-based domain detection

#### Class: DomainDetector

**Method:** `detect(df: pd.DataFrame) -> Dict[str, Any]`

**Returns:**
```python
{
    "domain": str,              # "sales" | "finance" | "hr" | "marketing" | "operations"
    "confidence": float,        # 0.0-1.0
    "indicators": List[str]     # Column names that indicated domain
}
```

**Detection Logic:**
- Scans column names for keywords
- Matches patterns (revenue, customer, salary, etc.)
- Returns highest confidence domain

**Used By:**
- main.py

---

### 3.5 AIDomainDetector

**Location:** `backend/domain_detection/ai_domain_detector.py`  
**Purpose:** AI-powered domain detection using GPT

#### Class: AIDomainDetector

**Method:** `detect(df: pd.DataFrame) -> Dict[str, Any]`

**Returns:** Same as DomainDetector

**Used By:**
- main.py (when AI detection enabled)

---

### 3.6 SimpleAnalytics

**Location:** `backend/analytics/simple_analytics.py`  
**Purpose:** Basic statistical analysis

#### Class: SimpleAnalytics

**Method:** `analyze(df: pd.DataFrame) -> Dict[str, Any]`

**Returns:**
```python
{
    "summary_stats": {...},
    "correlations": [...],
    "distributions": [...]
}
```

**Used By:**
- main.py

---

### 3.7 AIInsightsEngine

**Location:** `backend/analytics/ai_insights.py`  
**Purpose:** AI-powered insights generation

#### Class: AIInsightsEngine

**Method:** `generate_insights(profile: Dict) -> List[Dict]`

**Returns:**
```python
[
    {
        "type": str,           # "correlation" | "outlier" | "trend" | "anomaly"
        "description": str,    # Human-readable insight
        "severity": str,       # "low" | "medium" | "high"
        "recommendation": str  # Action to take
    }
]
```

**Used By:**
- main.py

---

### 3.8 UniversalChartGenerator

**Location:** `backend/visualizations/universal_charts.py`  
**Purpose:** Dynamic chart generation based on data

#### Class: UniversalChartGenerator

**Method:** `generate(df: pd.DataFrame, domain: str) -> List[Dict]`

**Returns:**
```python
[
    {
        "type": str,        # "bar" | "line" | "scatter" | "pie"
        "title": str,       # Chart title
        "data": {           # Chart data
            "x": [...],
            "y": [...]
        },
        "config": {         # Chart config
            "colors": [...],
            "labels": [...]
        }
    }
]
```

**Chart Selection Logic:**
- Numeric columns → scatter/line
- Categorical columns → bar/pie
- Time series → line
- Domain-specific charts (sales → revenue trend)

**Used By:**
- main.py

---

### 3.9 ReportAssembler

**Location:** `backend/reports/assembler.py`  
**Purpose:** Assembles complete report from sections

#### Imports
```python
from backend.reports.sections.quality_section import QualitySection
from backend.reports.sections.domain_section import DomainSection
from backend.reports.sections.ai_section import AISection
from backend.reports.sections.charts_section import ChartsSection
```

#### Class: ReportAssembler

**Method:** `assemble(profile, domain, insights, charts) -> Dict`

**Returns:**
```python
{
    "quality": {           # From QualitySection
        "html": str,
        "data": dict
    },
    "domain": {            # From DomainSection
        "html": str,
        "data": dict
    },
    "insights": {          # From AISection
        "html": str,
        "data": list
    },
    "charts": {            # From ChartsSection
        "html": str,
        "data": list
    },
    "metadata": {
        "generated_at": str,
        "version": str
    }
}
```

**Used By:**
- UltimateReportGenerator

---

### 3.10 QualitySection

**Location:** `backend/reports/sections/quality_section.py`  
**Purpose:** Generates quality metrics section

#### Class: QualitySection

**Method:** `generate(profile: Dict) -> Dict`

**Returns:**
```python
{
    "html": str,    # HTML for quality section
    "data": dict    # Quality metrics
}
```

**Used By:**
- ReportAssembler

---

### 3.11 DomainSection

**Location:** `backend/reports/sections/domain_section.py`  
**Purpose:** Generates domain detection section

#### Class: DomainSection

**Method:** `generate(domain: Dict) -> Dict`

**Returns:**
```python
{
    "html": str,    # HTML for domain section
    "data": dict    # Domain info
}
```

**Used By:**
- ReportAssembler

---

### 3.12 AISection

**Location:** `backend/reports/sections/ai_section.py`  
**Purpose:** Generates AI insights section

#### Class: AISection

**Method:** `generate(insights: List) -> Dict`

**Returns:**
```python
{
    "html": str,    # HTML for insights section
    "data": list    # Insights
}
```

**Used By:**
- ReportAssembler

---

### 3.13 ChartsSection

**Location:** `backend/reports/sections/charts_section.py`  
**Purpose:** Generates charts section

#### Class: ChartsSection

**Method:** `generate(charts: List) -> Dict`

**Returns:**
```python
{
    "html": str,    # HTML for charts section
    "data": list    # Chart data
}
```

**Used By:**
- ReportAssembler

---

### 3.14 UltimateReportGenerator

**Location:** `backend/export_engine/ultimate_report.py`  
**Purpose:** Exports final HTML/PDF report

#### Class: UltimateReportGenerator

**Method:** `generate(report: Dict) -> str`

**Returns:** HTML string (complete report)

**Used By:**
- main.py
- app.py

---

## 4. Connection Maps

### 4.1 main.py Connections
```
main.py
 ├─► DataProfiler
 ├─► DomainDetector
 ├─► AIDomainDetector
 ├─► SimpleAnalytics
 ├─► AIInsightsEngine
 ├─► UniversalChartGenerator
 └─► UltimateReportGenerator
```

### 4.2 app.py Connections
```
app.py
 ├─► DataProfiler
 └─► UltimateReportGenerator
```

### 4.3 ReportAssembler Connections
```
ReportAssembler
 ├─► QualitySection
 ├─► DomainSection
 ├─► AISection
 └─► ChartsSection
```

### 4.4 Full System Connections
```
main.py / app.py
    ↓
DataProfiler
    ↓
DomainDetector / AIDomainDetector
    ↓
SimpleAnalytics / AIInsightsEngine
    ↓
UniversalChartGenerator
    ↓
ReportAssembler
    ├─► QualitySection
    ├─► DomainSection
    ├─► AISection
    └─► ChartsSection
    ↓
UltimateReportGenerator
    ↓
HTML/PDF Report
```

---

## 5. API Endpoints

### FastAPI (main.py)

#### GET /
**Purpose:** Health check  
**Returns:** `{"status": "ok"}`

#### POST /analyze
**Purpose:** Analyze CSV and return JSON  
**Input:** CSV file (multipart/form-data)  
**Returns:**
```json
{
    "profile": {...},
    "domain": {...},
    "insights": [...],
    "charts": [...]
}
```

#### POST /full-report
**Purpose:** Generate complete HTML report  
**Input:** CSV file  
**Returns:** HTML string

---

## 6. Testing Commands

### Local Testing

#### Start FastAPI
```powershell
uvicorn main:app --reload
```
**URL:** http://localhost:8000/docs

#### Start Streamlit
```powershell
streamlit run app.py
```
**URL:** http://localhost:8501

#### Test DataProfiler
```powershell
python -c "import pandas as pd; from backend.data_processing.profiler import DataProfiler; df = pd.read_csv('test.csv'); print(DataProfiler().profile(df))"
```

#### Test Full Pipeline (API)
```powershell
curl -X POST -F "file=@test.csv" http://localhost:8000/analyze
```

#### Test Full Pipeline (UI)
```powershell
streamlit run app.py
# Upload test.csv via browser
```

### Create Test CSV
```powershell
echo "name,age,salary,department`nAlice,30,50000,Sales`nBob,25,45000,Marketing" > test.csv
```

---

## 7. Deployment

### Git Workflow
```powershell
git add .
git commit -m "Update"
git push origin main
```

### Auto-Deploy Targets
- **Railway:** FastAPI backend (main.py)
- **Streamlit Cloud:** Streamlit UI (app.py)

### Live URLs
- **API Docs:** https://goat-data-analyst-production.up.railway.app/docs
- **Streamlit UI:** https://goat-data-analyst-a6idzyddvy2pevnsqdzskt.streamlit.app/

### Environment Variables
```
OPENAI_API_KEY=your-api-key
PORT=8000
```

---

## 8. Quick Reference

### Key Data Structures

**Profile (from DataProfiler):**
```python
{"row_count": int, "quality_score": float, "missing_values": dict, ...}
```

**Domain (from DomainDetector):**
```python
{"domain": str, "confidence": float, "indicators": list}
```

**Insights (from AIInsightsEngine):**
```python
[{"type": str, "description": str, "severity": str}]
```

**Charts (from UniversalChartGenerator):**
```python
[{"type": str, "data": dict, "config": dict}]
```

### Common Debugging

**View logs:**
```powershell
# FastAPI
uvicorn main:app --reload --log-level debug

# Streamlit
streamlit run app.py --logger.level debug
```

**Check module imports:**
```powershell
python -c "from backend.data_processing.profiler import DataProfiler; print('OK')"
```

---

**End of Documentation**
