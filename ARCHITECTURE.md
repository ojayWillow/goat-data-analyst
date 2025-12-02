# GOAT Data Analyst - Architecture Documentation

**Last Updated**: December 2, 2025  
**Version**: 2.0 (Post-Rebuild)

---

## Core Principle: One Brain

Everything flows through **AnalysisEngine** - one central orchestrator.

CSV → AnalysisEngine.analyze(df) → AnalysisResult → UI/API

No duplicate logic. No parallel paths. One source of truth.

---

## System Flow

### 1. Entry Points
**Streamlit (app.py)**
- User uploads CSV
- Calls engine.analyze(df)
- Displays esult.report_html

**FastAPI (main.py)**
- POST /analyze/html with CSV
- Calls engine.analyze(df)
- Returns esult.report_html

### 2. The Brain (backend/core/engine.py)
**AnalysisEngine** orchestrates 7 steps:

1. **Profile**: What IS this data? → DataProfiler
2. **Domain**: What TYPE of data? → DomainDetector
3. **Quality**: What's WRONG? → Built-in quality checks
4. **Analytics**: What PATTERNS exist? → StatisticalAnalyzer
5. **AI Insights**: What does it MEAN? → InsightGenerator
6. **Charts**: SHOW me visually → ChartOrchestrator
7. **Report**: Package it BEAUTIFULLY → UltimateReportGenerator

### 3. Output (backend/core/models.py)
**AnalysisResult** contains everything:
- profile (dict)
- domain (dict)
- quality (dict)
- analytics (dict)
- ai_insights (dict)
- charts (dict)
- report_html (string)
- errors/warnings (lists)

---

## Plugin System

Each analysis step is a **plugin** to the engine:

### Active Plugins
- **DataProfiler** (backend/data_processing/profiler.py)
  - Detects column types
  - Calculates statistics
  - Finds quality issues

- **ChartOrchestrator** (backend/visualizations/chart_orchestrator.py)
  - Generates time series charts
  - Creates distributions
  - Shows category breakdowns

### Inactive Plugins (Not Yet Wired)
- **DomainDetector** - Detects data type (sales, finance, etc.)
- **StatisticalAnalyzer** - Advanced statistics
- **InsightGenerator** - AI-powered insights
- **UltimateReportGenerator** - Professional HTML reports

---

## How to Add New Features

### Add a New Chart Type
1. Create ackend/visualizations/charts/my_chart.py
2. Inherit from BaseChart
3. Add to ChartOrchestrator.AVAILABLE_CHARTS
4. Engine automatically uses it

### Add a New Analysis Step
1. Create your module (e.g., ackend/analytics/my_analyzer.py)
2. Import in engine.py
3. Initialize in AnalysisEngine.__init__()
4. Call in AnalysisEngine.analyze() at appropriate step
5. Store result in AnalysisResult

### Add a New Domain Sensor
1. Edit ackend/domain/detector.py
2. Add detection patterns
3. Engine automatically picks it up

---

## File Structure

backend/
├── core/
│ ├── models.py # AnalysisResult dataclass
│ └── engine.py # AnalysisEngine (THE BRAIN)
├── data_processing/
│ └── profiler.py # DataProfiler plugin
├── visualizations/
│ ├── chart_orchestrator.py
│ ├── base_chart.py
│ └── charts/
│ ├── timeseries_chart.py
│ ├── distribution_chart.py
│ └── category_chart.py
├── domain/ # (To be created)
├── analytics/ # (To be wired)
├── ai/ # (To be wired)
└── reports/ # (To be wired)

app.py # Streamlit UI
main.py # FastAPI backend


---

## Design Decisions

### Why One Brain?
- **Before**: Duplicate logic in Streamlit, FastAPI, notebooks
- **After**: One function does everything
- **Benefit**: Bug fixes happen once, features propagate automatically

### Why Plugins?
- **Modularity**: Each plugin is independent
- **Testability**: Test plugins separately
- **Flexibility**: Easy to add/remove features
- **Graceful Degradation**: Missing plugins show warnings, don't crash

### Why AnalysisResult?
- **Type Safety**: One standardized output format
- **Predictability**: UI/API always know what to expect
- **Debugging**: Easy to inspect at any point

---

## Current Status

✅ **Working**
- Core engine architecture
- Streamlit integration
- FastAPI integration
- Data profiling
- Chart generation
- Fallback HTML reports

⚠️ **Warnings (Expected)**
- DomainDetector not available
- StatisticalAnalyzer not available
- ReportGenerator not available

🔜 **Next Steps (Days 6-10)**
- Wire narrative generation
- Add human-like communication
- Implement context recognition

---

## Questions?

**Where does profiling happen?**  
→ engine.py calls DataProfiler.profile(df) in Step 1

**Where do I add a new chart?**  
→ Create in charts/, add to ChartOrchestrator.AVAILABLE_CHARTS

**Where do I change report layout?**  
→ Edit UltimateReportGenerator (once wired)

**How do I skip AI insights?**  
→ Pass options={'skip_ai': True} to engine.analyze(df, options)

**Where are errors logged?**  
→ Check esult.errors and esult.warnings lists

---

**Remember**: If you're not sure where something goes, it probably goes in the engine as a plugin.
