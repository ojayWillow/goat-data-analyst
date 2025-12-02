# GOAT Data Analyst - System Architecture

**Last Updated:** December 2, 2025, 2:45 PM EET

---

## 🎯 Vision

Modular "puzzle piece" architecture where each component:
- Does ONE thing well
- Can be added/removed independently
- Has clear inputs/outputs
- No hidden dependencies

---

## 📂 Directory Structure

```
C:\Projects\goat-data-analyst\
│
├── main.py                     # FastAPI backend (Railway)
├── app.py                      # Streamlit frontend (Streamlit Cloud)
├── requirements.txt
├── .env                        # API keys (not in git)
│
├── backend/
│   ├── connectors/
│   │   └── csv_handler.py      # CSV loading, encoding detection
│   │
│   ├── data_processing/
│   │   └── profiler.py         # DataProfiler + ProfileIntelligence
│   │
│   ├── domain_detection/
│   │   ├── domain_detector.py  # Keyword-based domain detection
│   │   ├── ai_domain_detector.py # AI-enhanced detection (Groq)
│   │   └── patterns.py         # Domain pattern definitions
│   │
│   ├── analytics/
│   │   ├── simple_analytics.py # Basic statistics
│   │   ├── ai_insights.py      # AI-generated insights (Groq)
│   │   ├── insights_engine.py  # Insights orchestration
│   │   └── visualizations.py   # (Legacy - to be replaced)
│   │
│   ├── visualizations/
│   │   ├── base_chart.py       # Abstract chart interface
│   │   ├── chart_orchestrator.py  # Chart manager
│   │   ├── charts/
│   │   │   ├── __init__.py
│   │   │   ├── timeseries_chart.py   # Only if datetime exists
│   │   │   ├── distribution_chart.py  # Uses ProfileIntelligence
│   │   │   ├── correlation_chart.py   # Uses ProfileIntelligence
│   │   │   └── category_chart.py      # Only if categorical exists
│   │   └── universal_charts.py # (DEPRECATED - being replaced)
│   │
│   ├── reports/
│   │   ├── assembler.py        # Orchestrates sections
│   │   └── sections/
│   │       ├── __init__.py
│   │       ├── quality_section.py   # Data quality HTML
│   │       ├── domain_section.py    # Domain detection HTML
│   │       ├── ai_section.py        # AI insights HTML
│   │       └── charts_section.py    # Visualization HTML
│   │
│   └── export_engine/
│       ├── quality_report.py   # (Legacy quality report)
│       └── ultimate_report.py  # (Delegates to assembler)
│
└── tests/
    ├── test_ai_domains.py
    ├── test_api.py
    └── test_deployment.py
```

---

## 🔄 Data Flow

### Request Pipeline

```
1. CSV Upload
      ↓
2. CSVHandler.load_csv()
   - Detects encoding
   - Loads as DataFrame
   - Returns (df, filename)
      ↓
3. DataProfiler.profile_data(df)
   - Column-level analysis
   - Type detection
   - Quality metrics
   - Creates ProfileIntelligence helper
   - Returns profile dict + intelligence
      ↓
4. Domain Detection (Parallel)
   ├─ DomainDetector (keyword patterns)
   └─ AIDomainDetector (Groq AI)
   - Combines results
   - Returns domain string
      ↓
5. ChartOrchestrator(df, domain)
   - Receives ProfileIntelligence
   - Passes to each chart via set_intelligence()
   - Each chart checks can_generate()
   - Returns {chart_name: html_string}
      ↓
6. AIInsightsEngine
   - Uses domain context
   - Generates McKinsey-style insights
   - Returns insights dict
      ↓
7. ReportAssembler
   - Receives: profile, domain, charts, insights
   - Calls each section generator
   - Wraps in HTML template
   - Returns complete HTML
      ↓
8. Response
   - FastAPI: JSON with report_html
   - Streamlit: Direct HTML render
```

---

## 🧩 Component Details

### 1. Data Processing Layer

**CSVHandler**
```python
Input: file_path or uploaded_file
Output: (DataFrame, filename)
```

**DataProfiler**
```python
Input: DataFrame
Output: {
    'dataset_name': str,
    'overall': {'rows': int, 'columns': int},
    'columns': {...},
    'quality_score': int
}
+ ProfileIntelligence instance
```

**ProfileIntelligence (NEW)**
```python
Methods:
- get_key_numeric_columns(max_cols=10) → List[str]
- is_identifier_column(col) → bool
- is_metadata_column(col) → bool

Purpose: Filter noise from charts (IDs, timestamps, flags)
```

### 2. Domain Detection Layer

**DomainDetector (Keyword-based)**
```python
Input: DataFrame
Logic: Pattern matching on column names
Output: domain str ("sales", "hr", "ecommerce", etc.)
```

**AIDomainDetector (AI-enhanced)**
```python
Input: DataFrame sample
Logic: Groq AI analysis
Output: domain str + confidence
```

### 3. Visualization Layer

**ChartOrchestrator**
```python
Input: DataFrame, domain, ProfileIntelligence
Logic:
  - Instantiate all chart classes
  - Call chart.set_intelligence(intelligence)
  - Check chart.can_generate()
  - Call chart.generate() if applicable
Output: Dict[chart_name, html_string]
```

**Individual Charts**
```python
BaseChart (abstract)
  ↓
├─ TimeSeriesChart (conditional: datetime column exists)
├─ DistributionChart (conditional: numeric columns exist)
├─ CorrelationChart (conditional: 2+ numeric columns)
└─ CategoryChart (conditional: categorical column exists)

Each implements:
- can_generate() → bool
- generate() → str (HTML)
- chart_name → str (unique ID)
- set_intelligence(ProfileIntelligence)
```

### 4. Report Generation Layer

**ReportAssembler**
```python
Input:
  - profile: Dict
  - domain_data: Dict
  - insights_data: Dict
  - charts_data: Dict[str, str]
  - config: Dict[str, bool]

Logic:
  - Conditionally include sections based on config
  - Call each section.generate()
  - Wrap in HTML template with CSS

Output: Complete HTML string
```

**Sections** (All independent)
```python
QualitySection.generate(profile) → HTML
DomainSection.generate(domain_data) → HTML
AISection.generate(insights_data) → HTML
ChartsSection.generate(charts_data) → HTML
```

---

## 🔑 Key Design Principles

### 1. Intelligence Layer
**Profile drives visualization decisions**
- Charts query ProfileIntelligence for meaningful columns
- No hardcoded column name assumptions
- Filters IDs, metadata, noise automatically

### 2. Conditional Generation
**Components check applicability**
```python
if chart.can_generate():
    html = chart.generate()
```
- No forced charts
- Clean failure handling
- User sees only relevant visuals

### 3. Separation of Concerns
**Each layer has one job**
- Profiler: Analyze data
- Detector: Identify domain
- Orchestrator: Decide what to show
- Charts: Generate visuals
- Assembler: Build report

### 4. Dependency Injection
**Components receive what they need**
```python
chart.set_intelligence(intelligence)
section.generate(data)
```
- No global state
- Easy to test
- Clear contracts

---

## 🚧 Known Issues

### 1. Chart Display (CRITICAL)
- Correlation heatmap appears smaller than specified 1100px
- Plotly hardcodes dimensions in inline style
- Container CSS may be conflicting
- Needs visual debugging with screenshots

### 2. Dataset Name
- Always shows "CSV Analysis Report"
- Should show actual filename
- Issue in profile generation or upload handling

### 3. Legacy Code
- `universal_charts.py` still exists (deprecated)
- `quality_report.py` partially unused
- Cleanup needed after migration confirmed stable

---

## 📊 Architecture Quality Metrics

| Aspect | Status | Notes |
|--------|--------|-------|
| Modularity | ✅ | Each component independent |
| Testability | ✅ | Pure functions, clear inputs/outputs |
| Extensibility | ✅ | Easy to add new charts/sections |
| Maintainability | ✅ | Clear responsibilities |
| Performance | ⚠️ | Need to verify chart caching |
| Documentation | ✅ | Well-commented code |

---

## 🎯 Next Steps

### Phase 2: Optimization
1. Add chart result caching
2. Optimize profile generation
3. Parallel domain detection

### Phase 3: Advanced Features
1. Custom chart configuration
2. Export to PDF/Excel
3. Multi-file analysis
4. Dashboard mode

---

## 🔗 Deployment

**Backend:** Railway  
**Frontend:** Streamlit Cloud  
**Environment:** Python 3.11+  
**Key Dependencies:** pandas, plotly, groq, fastapi, streamlit

---

## 📝 Migration Notes

**From Monolithic to Modular:**
```
OLD: universal_charts.py (800 lines, all charts coupled)
NEW: base_chart.py + 4 independent chart modules (150 lines each)

Benefits:
- Fix one without breaking others
- Add new charts without touching existing
- Test each chart in isolation
- Clear conditional logic
```

**Intelligence Layer Addition:**
```
OLD: Charts blindly used first numeric column (often User_ID)
NEW: ProfileIntelligence filters meaningful columns

Result: Charts now show actual data (price, quantity, etc.)
```

---

**Last Refactor:** December 2, 2025  
**Status:** Modular system operational, display issues remain  
**Next Session:** Visual debugging of chart sizing