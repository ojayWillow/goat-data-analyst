a# GOAT Data Analyst — Complete Rebuild Roadmap

**Project Vision**: An AI-powered data analyst that understands context, identifies pain points, and provides clear, actionable guidance—not just charts and metrics.

**Timeline**: ~3-4 weeks (15-20 working days) to production-ready v1

**Your Workflow**:
- One task at a time
- Copy-paste ready code
- Test immediately after each step
- Check off boxes as you complete

---

## Phase 1: Clean Architecture Restart
**Goal**: Build one central brain (AnalysisEngine) and eliminate all duplicate code paths

**Duration**: 5 days

---

### Day 1: Create Core Engine Foundation
**Objective**: Build the heart of the system—one function that orchestrates everything

#### Tasks:
- [✅] Create `backend/core/` directory
- [✅] Create `backend/core/models.py` with `AnalysisResult` dataclass
- [✅] Create `backend/core/engine.py` with `AnalysisEngine` class
- [✅] Wire existing logic (profiler, domain, analytics, AI, charts, report) into `engine.analyze(df)`

#### Success Criteria:
```python
# Test in Python console:
from backend.core.engine import AnalysisEngine
import pandas as pd

df = pd.read_csv("test.csv")
engine = AnalysisEngine()
result = engine.analyze(df)
print(result.report_html[:200])
# Should print HTML without errors
```

#### Deliverable:
- [✅ ] `backend/core/models.py` exists and contains `AnalysisResult`
- [✅] `backend/core/engine.py` exists and contains `AnalysisEngine`
- [✅] `engine.analyze(df)` runs successfully in console
- [✅] No import errors

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

### Day 2: Wire Streamlit to Engine
**Objective**: Make Streamlit UI use the engine only—no duplicate logic

#### Tasks:
- [✅] Edit `app.py` to import `AnalysisEngine`
- [✅] Remove all direct calls to profiler, analytics, chart generators
- [✅] Simplify to: `result = engine.analyze(df)` then display `result.report_html`
- [✅] Delete old UniversalChartGenerator and ReportAssembler imports from `app.py`

#### Success Criteria:
```bash
# Run Streamlit:
streamlit run app.py
# Upload CSV, click "Run Analysis"
# Report displays correctly with no console errors
```

#### Deliverable:
- [✅ ] `app.py` uses only `AnalysisEngine`
- [✅ ] Streamlit displays report successfully
- [✅] No errors in terminal

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

### Day 3: Wire FastAPI to Engine
**Objective**: Make API use the engine only

#### Tasks:
- [✅] Edit `main.py` to import `AnalysisEngine`
- [✅] Simplify `/analyze/html` endpoint to call `engine.analyze(df)` and return `result.report_html`
- [✅ ] Remove duplicate profiling/chart/report logic from `main.py`
- [✅ ] Keep `/analyze` (JSON) endpoint for now, or wire to engine too

#### Success Criteria:
```bash
# Run API:
uvicorn main:app --reload
# POST CSV to http://localhost:8000/analyze/html
# Should return HTML report correctly
```

#### Deliverable:
- [✅ ] `main.py` uses only `AnalysisEngine`
- [✅ ] `/analyze/html` returns correct report
- [✅ ] No duplicate logic in `main.py`

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

### Day 4: Delete Old Duplicate Code
**Objective**: Clean up the codebase—remove all dead/duplicate paths

#### Tasks:
- [✅ ] Search for and identify unused modules:
  - `backend/visualizations/universal_charts.py` (if replaced)
  - `backend/reports/assembler.py` (if replaced)
  - Any other unused files
- [✅ ] Move them to an `archive/` folder or delete them
- [✅ ] Test Streamlit and API to confirm nothing broke
- [✅ ] Run `git status` to see what was removed

#### Success Criteria:
```bash
# Both should work:
streamlit run app.py
uvicorn main:app --reload
# No import errors, reports display correctly
```

#### Deliverable:
- [✅ ] Unused code removed or archived
- [✅ ] Streamlit works
- [✅ ] API works
- [✅ ] Codebase is leaner

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

### Day 5: Document the New Architecture
**Objective**: Create clear documentation so you never lose clarity again

#### Tasks:
- [✅ ] Create or update `ARCHITECTURE.md`
- [✅ ] Draw simple diagram: `CSV → AnalysisEngine → AnalysisResult → UI/API`
- [✅ ] List all plugins (sensors, insights, charts, reports)
- [✅ ] Explain "one brain" principle
- [✅ ] Add inline comments to `engine.py` explaining each step
- [✅ ] Document where to add new features (charts, sensors, etc.)

#### Success Criteria:
- You can answer these without looking at code:
  - Where does profiling happen? → `engine.py` calls `DataProfiler`
  - Where do I add a new chart? → Add to `ChartOrchestrator`, engine uses it automatically
  - Where do I change report layout? → `UltimateReportGenerator`

#### Deliverable:
- [✅ ] `ARCHITECTURE.md` exists and is clear
- [✅ ] `engine.py` has helpful comments
- [✅] You can explain the system to someone else

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

## Phase 2: Analyst Voice & Narrative
**Goal**: Make GOAT talk like a human analyst, not a dashboard

**Duration**: 5 days

---

### Day 6: Design Narrative Structure
**Objective**: Create the framework for human-like communication

#### Tasks:
- [✅ ] Create `backend/narrative/` directory
- [✅ ] Create `backend/narrative/narrative_generator.py`
- [✅ ] Define three main sections:
  - "I See You" (context recognition)
  - "What Hurts" (pain points)
  - "Your Path Forward" (action plan)
- [✅ ] Stub out methods with placeholder text

#### Success Criteria:
```python
# Test in console:
from backend.narrative.narrative_generator import NarrativeGenerator
gen = NarrativeGenerator()
# Methods exist and return strings (even if placeholder)
```

#### Deliverable:
- [✅ ] `backend/narrative/narrative_generator.py` exists
- [✅ ] Three methods defined: `generate_context()`, `generate_pain_points()`, `generate_action_plan()`
- [✅ ] File imports cleanly

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

### Day 7: Implement "I See You" Section
**Objective**: Context recognition—let users know GOAT understands their data

#### Tasks:
- [ ] Use `AnalysisResult.domain` and `AnalysisResult.profile` to detect:
  - Dataset type (sales, finance, healthcare, etc.)
  - Key columns
  - Row/column counts
  - Date ranges if time-based
- [ ] Generate human-like intro paragraph
- [ ] Test with 3 different CSV types

#### Example Output:
```
"Hi—I can see you're working with sales transaction data from an 
e-commerce system. You have 12,450 rows across 8 columns, with 
timestamps spanning January 2023 to December 2024."
```

#### Deliverable:
- [✅ ] `generate_context()` returns accurate, contextual intro
- [✅ ] Works with sales, finance, and generic CSVs
- [✅ ] Text feels human, not robotic

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

### Day 8: Implement "What Hurts" Section
**Objective**: Identify and prioritize data quality issues in plain language

#### Tasks:
- [✅ ] Use `AnalysisResult.quality` to detect:
  - Missing values (% and which columns)
  - Duplicate rows
  - Outliers
  - Data type mismatches
- [✅ ] Prioritize issues by severity
- [✅ ] Generate clear, actionable descriptions

#### Example Output:
```
"Here's what needs attention:
1. Missing values: 12% of your 'amount' column is empty—this will break totals.
2. Duplicates: 47 duplicate transaction IDs found.
3. Outliers: 3 extreme values in 'price' (99999) look like data entry errors."
```

#### Deliverable:
- [✅ ] `generate_pain_points()` returns prioritized issue list
- [✅ ] Test with messy CSV (missing values, dupes, outliers)
- [✅ ] Issues described clearly and actionably

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

### Day 9: Implement "Your Path Forward" Section
**Objective**: Give users a sequenced, actionable plan

#### Tasks:
- [✅ ] Use pain points + domain to generate step-by-step plan
- [✅ ] Sequence steps logically: clean → validate → analyze → visualize
- [✅ ] Make steps specific to the actual data issues found
- [✅ ] Test with multiple scenarios

#### Example Output:
```
"Your Path Forward:
1. Clean: Remove 47 duplicate rows.
2. Fix: Fill missing 'amount' values with median.
3. Validate: Check for negative prices (found 2).
4. Analyze: Segment customers by purchase frequency.
5. Visualize: Build revenue trend by month."
```

#### Deliverable:
- [✅ ] `generate_action_plan()` returns ordered steps
- [✅ ] Steps are specific, not generic
- [✅ ] Sequence makes logical sense

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

### Day 10: Integrate Narrative into Report
**Objective**: Make the narrative appear in the actual HTML report

#### Tasks:
- [✅ ] Edit `UltimateReportGenerator` to call `NarrativeGenerator`
- [✅ ] Add narrative sections to report template:
  - At top: "I See You" context
  - After profile: "What Hurts" issues
  - Before charts: "Your Path Forward" plan
- [✅ ] Style narrative sections to stand out (bold headers, clean formatting)
- [✅ ] Test full report with narrative included

#### Success Criteria:
```bash
# Run Streamlit or API, upload CSV
# Report should now include:
# 1. Context intro paragraph
# 2. Pain points list
# 3. Action plan
# Plus all existing charts and metrics
```

#### Deliverable:
- [✅ ] Narrative appears in HTML report
- [✅ ] Sections are clearly formatted
- [✅ ] Report feels more human and helpful

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

## Phase 3: Auto-Fix Features
**Goal**: Let users fix common issues with one click

**Duration**: 3 days

---

### Day 11: Build DataFixer Module
**Objective**: Create the auto-fix engine

#### Tasks:
- [✅ ] Create `backend/data_processing/data_fixer.py`
- [✅ ] Implement common fix operations:
  - Remove duplicate rows
  - Fill missing values (median, mode, forward-fill)
  - Normalize date formats
  - Remove outliers
  - Standardize column names
- [✅ ] Each operation returns a new DataFrame (doesn't modify original)
- [✅ ] Add preview capability (show what will change)

#### Success Criteria:
```python
# Test in console:
from backend.data_processing.data_fixer import DataFixer
fixer = DataFixer()
clean_df = fixer.remove_duplicates(df)
# Should return DataFrame with dupes removed
```

#### Deliverable:
- [✅ ] `data_fixer.py` exists with 5+ fix operations
- [✅ ] Each operation tested and works
- [✅ ] Operations are safe (don't corrupt data)

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

### Day 12: Add Fix Suggestions to Report
**Objective**: Show "Auto-Fix" buttons in the report

#### Tasks:
- [✅ ] Modify narrative generator to include fix suggestions with each pain point
- [✅ ] Add HTML buttons/links for each fixable issue
- [✅ ] Design simple modal or section showing "Preview Changes"
- [✅ ] Style buttons to be clear and inviting

#### Example in Report:
```
"Missing values: 12% of 'amount' column is empty.
[Preview Fix] [Auto-Fix Now]"
```

#### Deliverable:
- [✅ ] Fix buttons appear in report
- [✅ ] Buttons are styled and clickable
- [✅ ] Preview shows what will change

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

### Day 13: Wire Fix Actions to Streamlit
**Objective**: Make auto-fix actually work in the UI

#### Tasks:
- [✅ ] Add Streamlit buttons for each suggested fix
- [✅ ] When clicked:
  - Show preview of changes
  - User confirms
  - Apply fix, regenerate report
  - Download cleaned CSV
- [✅ ] Test full flow: upload → analyze → fix → download

#### Success Criteria:
```bash
# In Streamlit:
# 1. Upload messy CSV
# 2. Click "Fix missing values"
# 3. Preview shows changes
# 4. Confirm, get cleaned CSV
# 5. Re-analyze shows issue resolved
```

#### Deliverable:
- [✅ ] Auto-fix works end-to-end in Streamlit
- [✅ ] User can download cleaned CSV
- [✅ ] Flow is smooth and intuitive

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

## Phase 4: Multi-File / Folder Scanning
**Goal**: Move from single CSV to analyzing entire folders or databases

**Duration**: 3 days

---

### Day 14: Build Batch Analyzer
**Objective**: Scan multiple files at once

#### Tasks:
- [✅ ] Create `backend/core/batch_engine.py`
- [✅ ] Implement folder scanning:
  - Accept folder path
  - Find all CSVs in folder
  - Run `engine.analyze()` on each
  - Aggregate results
- [✅ ] Generate company-level summary:
  - Total files analyzed
  - Health score per file
  - Cross-file issues (if applicable)
  - Prioritized action list

#### Success Criteria:
```python
# Test in console:
from backend.core.batch_engine import BatchEngine
batch = BatchEngine()
results = batch.analyze_folder("./data_folder")
# Should return list of AnalysisResults
```

#### Deliverable:
- [✅ ] `batch_engine.py` exists
- [✅ ] Can analyze folder of CSVs
- [✅ ] Returns aggregated results

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

### Day 15: Add Folder Upload to UI
**Objective**: Let users upload folders in Streamlit

#### Tasks:
- [✅ ] Add folder upload option to Streamlit UI
- [✅ ] Call `BatchEngine.analyze_folder()`
- [✅ ] Display company-level dashboard:
  - List all files with health scores
  - Show top issues across all files
  - Prioritized action list
- [✅ ] Allow drilling into individual file reports

#### Success Criteria:
```bash
# In Streamlit:
# 1. Upload folder with 5 CSVs
# 2. See dashboard with all 5 files listed
# 3. Click any file to see detailed report
# 4. See cross-file summary
```

#### Deliverable:
- [✅ ] Folder upload works in Streamlit
- [✅ ] Company dashboard displays
- [✅ ] Can view individual file reports

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

### Day 16: Create Company Health Report
**Objective**: Generate executive summary for multi-file analysis

#### Tasks:
- [✅ ] Create new report template for batch analysis
- [✅ ] Include:
  - Overall data health score
  - Top 5 issues across all files
  - Prioritized action plan for the company
  - File-by-file summary table
- [✅ ] Generate downloadable PDF or HTML report

#### Success Criteria:
- Report answers:
  - "Which files need attention first?"
  - "What are our biggest data quality risks?"
  - "What should we fix this week?"

#### Deliverable:
- [✅ ] Company health report generates
- [✅ ] Report is clear and executive-friendly
- [✅ ] Can download/share report

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

## Phase 5: Polish & Deployment
**Goal**: Make it production-ready and deploy

**Duration**: 2-3 days

---

### Day 17: UI/UX Polish
**Objective**: Make the interface professional and pleasant

#### Tasks:
- [✅ ] Improve Streamlit styling:
  - Custom CSS for better look
  - Clear section headers
  - Progress indicators during analysis
  - Better error messages
- [✅ ] Add loading animations
- [✅ ] Add sample data option ("Try with example CSV")
- [✅ ] Improve mobile responsiveness

#### Deliverable:
- [ ] UI looks professional
- [ ] User experience is smooth
- [ ] No confusing elements

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

### Day 18: Testing & Bug Fixes
**Objective**: Find and fix issues before deployment

#### Tasks:
- [✅ ] Test with 10+ different CSV types:
  - Sales data
  - Financial data
  - Generic data
  - Messy data (encoding issues, weird characters)
  - Large files (100k+ rows)
- [✅ ] Fix any bugs found
- [✅ ] Test all auto-fix operations
- [✅ ] Test folder scanning
- [✅ ] Verify all narratives make sense

#### Deliverable:
- [✅ ] All major bugs fixed
- [✅ ] System handles edge cases gracefully
- [✅ ] No crashes with real-world data

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

### Day 19: Deployment Prep
**Objective**: Get ready to deploy to cloud

#### Tasks:
- [ ] Clean up code:
  - Remove debug prints
  - Update requirements.txt
  - Add environment variable handling
- [ ] Update README.md with:
  - What GOAT does
  - How to use it
  - Setup instructions
- [ ] Commit all changes to GitHub
- [ ] Test that Railway and Streamlit Cloud can build

#### Deliverable:
- [ ] Code is clean and documented
- [ ] README is clear
- [ ] Ready for deployment

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

### Day 20: Deploy & Launch
**Objective**: Get GOAT live and accessible

#### Tasks:
- [ ] Push final code to GitHub
- [ ] Deploy to Railway (API)
- [ ] Deploy to Streamlit Cloud (UI)
- [ ] Test live URLs
- [ ] Share with first users
- [ ] Create demo video or screenshots
- [ ] Post on social media / share with community

#### Success Criteria:
- Both URLs work:
  - Streamlit: https://goat-data-analyst-...streamlit.app
  - API: https://goat-data-analyst-production.up.railway.app
- Can upload CSV and get full analyst report
- Narrative, charts, and auto-fix all work

#### Deliverable:
- [ ] GOAT is live and public
- [ ] Demo materials ready
- [ ] First users can access

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

## Future Enhancements (Post-Launch)
**These come AFTER the core product is solid**

### Phase 6: Integrations
- [ ] Slack bot integration
- [ ] Google Sheets add-on
- [ ] Python SDK (`pip install goat-analyst`)
- [ ] API authentication and user accounts

### Phase 7: Advanced Features
- [ ] Database connectors (Postgres, MySQL, Snowflake)
- [ ] Real-time monitoring / scheduled scans
- [ ] Team collaboration features
- [ ] Custom domain-specific rules

### Phase 8: AI Enhancements
- [ ] Chat interface ("Why is revenue down?")
- [ ] Anomaly explanation with context
- [ ] Predictive recommendations
- [ ] Automated insight prioritization

---

## Success Metrics

**After Phase 1-2 (Day 10):**
- [ ] Single AnalysisEngine powers everything
- [ ] Narrative makes reports feel human
- [ ] You can explain architecture clearly

**After Phase 3 (Day 13):**
- [ ] Users can fix data issues with one click
- [ ] Cleaned CSVs download successfully

**After Phase 4 (Day 16):**
- [ ] Can analyze entire folders
- [ ] Company health dashboard works
- [ ] Cross-file insights provided

**After Phase 5 (Day 20):**
- [ ] GOAT is live and accessible
- [ ] First users providing feedback
- [ ] You're confident in the system

---

## Daily Workflow Template

**Each day:**
1. Open this file and find your current day
2. Read objectives and tasks
3. Get code from AI assistant (copy-paste ready)
4. Test immediately after each change
5. Check off completed items
6. Mark day status: ⬜ → 🟡 → ✅
7. Move to next day when all checkboxes done

**If stuck:**
- Re-read success criteria
- Test in smaller pieces
- Ask for clarification
- It's okay to take 2 days on one task

**Remember:**
- One task at a time
- Test before moving on
- Check boxes give you momentum
- The architecture restart (Days 1-5) is the foundation for everything else

---

## Project Principles

**Always remember:**
1. **One Brain**: Everything goes through AnalysisEngine
2. **Plugins**: New features are plugins, not parallel systems
3. **Human Voice**: Talk to users like a colleague, not a dashboard
4. **Action-Oriented**: Always provide next steps, not just data
5. **Test First**: Never move forward without confirming current step works

---

**Last Updated**: December 2, 2025
**Version**: 1.0
**Status**: Ready to begin Phase 1

---

## Notes Section
*(Use this space to track thoughts, blockers, or ideas as you work)*

