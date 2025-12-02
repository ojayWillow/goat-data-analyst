# 🗺️ GOAT DATA ANALYST – ROADMAP V2
# Full‑Stack Data Analyst Copilot • Product-First • Well‑Oiled Engine

## 🎯 Vision

GOAT Data Analyst is a copilot for full‑stack data analysts.

It does the first 30–40% of the work on a new dataset:
- Ingests and profiles the data
- Checks quality and schema
- Detects rough domain and key entities
- Builds core charts
- Generates structured AI observations

The goal is not to replace analysts, but to help them get to the real questions and stakeholder conversations faster.

Current focus:
- Product quality
- Stability and speed
- “Feels good to use as an analyst”

Revenue, pricing, and aggressive growth are explicitly secondary for now.

---

## ✅ CURRENT STATUS (REALITY SNAPSHOT)

Project start: November 26–27, 2025

What is already working:

- CSV ingestion with encoding handling
- Data profiling with type detection
- Quality report generator (HTML)
- Domain detection (keyword-based + AI-enhanced)
- Simple analytics (summary, numeric, categorical)
- AI insights generation (Groq-integrated)
- Universal charts (time series, top-N, distribution, correlation)
- Ultimate HTML report that combines all of the above
- FastAPI backend on Railway
- Streamlit frontend on Streamlit Cloud
- Performance tested up to ~1M rows (≈14–15s end-to-end)
- Local + cloud both working with the new “Visual Analytics” and “Domain Intelligence”

Initial roadmap was MRR- and marketing-heavy.  
New roadmap is product-first and analyst-focused.

---

## 🎯 HIGH-LEVEL GOALS (V2)

1. Make GOAT feel like a serious tool an analyst can trust:
   - Stable, predictable behavior
   - Clear errors instead of silent failures
   - Clean, logical report structure

2. Make the first-pass analysis genuinely useful:
   - Solid data overview and quality checks
   - Domain + entity detection as orientation
   - Core metrics and distributions
   - Visuals that make sense for tabular data
   - AI observations that sound like an analyst, not a chatty bot

3. Keep scope realistic:
   - Focus on product and engine quality
   - Do light marketing (demo videos, a few posts) mainly to get feedback
   - No short-term pressure around $X MRR by week Y

---

## PHASE 1 – TIGHTEN THE CORE PRODUCT

Timeline: Next 2–3 weeks (flexible, product-first)

### 1. Report Structure & UX Cleanup

Goal: Make the HTML report read like a real analyst’s first-pass output, not a feature showcase.

Target section order:

1. Overview
   - Rows, columns
   - Missingness
   - Memory usage

2. Data Quality & Schema
   - Data types summary
   - Missing value distribution
   - Potential issues (constant columns, weird distributions)

3. Domain & Key Entities
   - Detected domain (as a “best guess”)
   - Confidence (normalized, 0–100%)
   - Top 3 domain candidates with bars (optional)
   - Key entities/tokens (e.g. customer, product, region)

4. Core Analytics
   - Summary stats
   - Numeric analysis
   - Categorical breakdowns

5. Visual Analytics
   - Time series (when date + value found)
   - Top-N bar chart
   - Distribution chart
   - Correlation heatmap

6. AI Observations (Analyst Style)
   - Short, numbered insights
   - Tied to actual columns and metrics

What we already have:

- All main building blocks exist (`ultimate_report.py`, analytics, AI insights, charts).
- Sections are present but order and emphasis can be improved.

Tasks:

- [ ] Reorder and clean sections in `UltimateReportGenerator.generate_html()`  
- [ ] Ensure each section is optional and degrades gracefully:
  - If no charts, hide Visual Analytics card
  - If no AI insights, omit AI section cleanly
- [ ] Slightly simplify headings and reduce visual clutter

---

### 2. AI Insights – Make Them Look Like Analyst Notes

Goal: AI insights should look like notes a real analyst could paste into a slide or email.

What we have:

- AI engine (Groq) integrated
- AI insights section already wired into final report

Improvements:

- Prompt should ask for:
  - 5–7 short, numbered points
  - References to actual column names and summary stats (when possible)
  - Focus on anomalies, strong correlations, skew, concentration, trends
  - Avoid generic advice like “optimize your business strategy” with no link to the data

Tasks:

- [ ] Update `ai_insights.py` (or equivalent) prompts to “short, numbered, analyst-style findings”  
- [ ] Keep max number of insights small (e.g. 7)  
- [ ] Keep formatting clean (avoid double numbering, weird bullets)

---

### 3. Domain & Confidence – Practical Orientation

Goal: Use domain detection to orient the analyst, not to claim magical understanding.

What we have:

- Keyword-based domain detector
- AI-enhanced domain detector
- “🎯 Domain Intelligence” card in the report
- Confidence normalization fix (no more 9800%)

Improvements:

- Present domain as:
  - “Best guess based on column names and patterns”
  - Not as absolute truth
- Show:
  - Primary domain (uppercased label)
  - One confidence number (proper 0–100%)
  - Optional top 2–3 alternative domains with bars

Tasks:

- [x] Normalize confidence to 0–1 range and display as 0–100%  
- [ ] Adjust wording in `_domain_html` to be slightly more neutral:
  - Clarify that this is a heuristic/AI guess
- [ ] Ensure entities are clearly shown and trimmed if too many

---

### 4. Visual Analytics – Robust Universal Charts

Goal: The four universal charts should “just work” in most datasets and be obviously useful.

What we have:

- Time series (if date + value found)
- Top N bar chart (category + value)
- Distribution chart (histogram)
- Correlation heatmap (numeric columns)

Improvements:

- Better column detection:
  - If multiple numeric columns, pick the “most business-y” one (revenue/amount/total etc.) when possible
- Defensive behavior:
  - If too many numeric columns, limit correlation to first N or top N by variance
  - If no suitable date/value, skip time series instead of forcing it
- Slightly more descriptive titles based on chosen columns

Tasks:

- [x] Implement `UniversalChartGenerator` and wire into report  
- [ ] Refine detection functions and add sensible limits (e.g. max 10 columns in heatmap)  
- [ ] Confirm charts behave well on:
  - Small (few rows)
  - Medium (10k–100k rows)
  - Wide (many columns) datasets

---

## PHASE 2 – ANALYST WORKFLOW & UX

Timeline: After Phase 1 feels solid

### 5. Streamlit UX for Analysts

Goal: Make the frontend feel like a tool an analyst could use daily, not just a demo shell.

What we have:

- Upload CSV and get a downloadable HTML report
- Simple UI on Streamlit
- Cloud deployment working

Improvements:

- Add “Report Mode”:
  - Quick: overview + core analytics only, no AI or charts
  - Full: everything (AI + charts)
- Better messaging:
  - Clear spinner/progress
  - Friendly error messages instead of raw stack traces

Tasks:

- [ ] Add report mode selector in `app.py` (radio or selectbox)  
- [ ] Use report mode to:
  - Skip AI insights or charts for “Quick” mode
  - Possibly limit rows processed
- [ ] Improve on-screen feedback during long runs

---

### 6. Light Personalization (No Heavy Settings)

Goal: Let analysts have minimal control without turning GOAT into a complex settings app.

Ideas (can be incremental):

- Toggle: “Include AI insights: Yes/No”
- Toggle: “Include charts: Yes/No”
- Option: “Max rows to sample” (e.g. 50k / 100k / 250k)

Tasks (minimal for now):

- [ ] Add “Include AI insights” toggle and respect it in backend  
- [ ] Optional: Add “Include charts” toggle

---

## PHASE 3 – DEEPEN VALUE (LATER EXPLORATIONS)

These are ideas for when the core feels really good. No timeline pressure.

### 7. Opinionated Analysis Templates

Idea: Provide modes tailored to typical analysis use cases for analysts, using the same engine.

Examples:

- Customer/CRM analysis
- Sales/transactions analysis
- Marketing performance
- Experiment / A/B test summary

Each template:

- Emphasizes different visuals
- Adjusts AI prompts to match the context
- Highlights different metrics

---

### 8. Multi-File & System View

Idea: Get closer to “understanding a business system” by supporting related files:

- Customers + Orders + Events
- Leads + Opportunities + Deals
- Campaigns + Clicks + Conversions

This is complex and can wait, but aligns with the long-term “system + growth assistant” vision.

---

## LIGHTWEIGHT MARKETING & FEEDBACK

New stance:

- Marketing is a support function, not the main focus.
- The goal is to get a few real users (analysts, data-savvy founders) trying GOAT and giving feedback.

Simple actions:

- [ ] Record 1–2 short demo videos:
  - “Upload CSV → watch GOAT generate a report”
- [ ] Update README with:
  - Clear value proposition
  - Screenshots / GIF
  - Link to live demo
- [ ] Occasionally share on LinkedIn:
  - Progress updates
  - Short clips of the tool in action
  - No pressure on “launch hype”

---

## SUCCESS METRICS (PRODUCT-FIRST)

Short term (next 1–2 months):

- Tool is stable:
  - No crashes on reasonable CSVs
  - Clear error messages
- You personally find:
  - It’s faster to run GOAT on a new dataset than to do all basic EDA manually
- HTML reports:
  - Are readable
  - Have a clear structure
  - Are something you’d be comfortable sending to a stakeholder as “first look”

Medium term:

- A few other analysts / power users say:
  - “Yeah, I would use this as a first step on new data.”
- You see repeat usage for your own work.

Long term (optional, later):

- You can evolve GOAT toward:
  - Niche-specific workflows
  - Paid tiers
  - Deeper “business system” insights

For now: build a well‑oiled, high-quality analyst copilot that you respect yourself.

---

**Updated:** December 1, 2025  
**Status:** Core engine working, charts + AI + domain integrated, now focusing on tightening UX and report structure.
