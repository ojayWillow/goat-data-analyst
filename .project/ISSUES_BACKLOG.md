\# Issues Backlog \& Technical Debt



\*\*Last Updated:\*\* 2025-11-29 (Session 1)



---



\## Critical Issues (Must Fix Before Next Release)



\### 1. Datetime Detection Too Simplistic

\- \*\*File:\*\* `backend/data\_processing/profiler.py`

\- \*\*Issue:\*\* Uses simple heuristic: try parsing first 100 values, suppress warnings

\- \*\*Risk:\*\* May incorrectly classify or crash on edge cases

\- \*\*Fix:\*\* Replace with explicit format checks + threshold-based parsing

\- \*\*Effort:\*\* 1–2 hours

\- \*\*Priority:\*\* Medium (works but fragile)



\### 2. Domain Pattern Weights Not Data-Driven

\- \*\*File:\*\* `backend/domain\_detection/patterns.py`

\- \*\*Issue:\*\* Weights (e-commerce: 1.2, customer: 1.1, etc.) chosen arbitrarily

\- \*\*Risk:\*\* May misclassify mixed-domain or ambiguous datasets

\- \*\*Fix:\*\* Run grid search to find optimal weights that maximize precision/recall

\- \*\*Effort:\*\* 2–3 hours

\- \*\*Priority:\*\* Medium (functional but not optimized)



\### 3. Scoring Algorithm Only Has One Variant

\- \*\*File:\*\* `backend/domain\_detection/domain\_detector.py`

\- \*\*Issue:\*\* Changed to keyword-based scoring but never tested alternatives

\- \*\*Risk:\*\* Might not handle edge cases (mixed domains, sparse data)

\- \*\*Fix:\*\* Test 2–3 scoring variants (cosine similarity, TF-IDF, etc.), benchmark

\- \*\*Effort:\*\* 3–4 hours

\- \*\*Priority:\*\* Low (works well on known datasets)



\### 4. Performance Not Tested at Scale (1M+ rows)

\- \*\*Files:\*\* `generate\_final\_report.py`, data loading pipeline

\- \*\*Issue:\*\* Tested up to 233K rows, but plan called for 1M rows

\- \*\*Risk:\*\* Unknown behavior at scale; may run out of memory or timeout

\- \*\*Fix:\*\* Generate synthetic 1M-row dataset, run full pipeline, measure memory/time

\- \*\*Effort:\*\* 1 hour

\- \*\*Priority:\*\* Medium (needed before production launch)



\### 5. AI Insights Quality Not Systematically Validated

\- \*\*File:\*\* `backend/analytics/ai\_insights.py`

\- \*\*Issue:\*\* Generates 7 insights per dataset but quality not checked

\- \*\*Risk:\*\* May ship low-quality or irrelevant insights to users

\- \*\*Fix:\*\* Spot-check insights for 5+ datasets, validate against domain expertise

\- \*\*Effort:\*\* 1–2 hours

\- \*\*Priority:\*\* High (core user-facing feature)



---



\## Important Issues (Should Fix Soon)



\### 6. Edge Cases Not Thoroughly Tested

\- \*\*Test Cases Missing:\*\*

&nbsp; - Empty CSV (0 rows, but headers exist)

&nbsp; - Huge file (> 500MB)

&nbsp; - Malformed CSV (inconsistent columns, weird delimiters)

&nbsp; - CSV with all null columns

&nbsp; - Single-row CSV

\- \*\*Risk:\*\* App crashes instead of graceful error handling

\- \*\*Fix:\*\* Add 5 test CSVs, test each, add error handling

\- \*\*Effort:\*\* 2 hours

\- \*\*Priority:\*\* Medium (user experience)



\### 7. Report Generator Two-File Architecture

\- \*\*Files:\*\* `backend/export\_engine/ultimate\_report.py`, `backend/export\_engine/quality\_report.py`

\- \*\*Issue:\*\* Split across two files for no clear reason (historical accident)

\- \*\*Risk:\*\* Hard to maintain, confusing for new developers

\- \*\*Fix:\*\* Consider merging if it saves >20% code, otherwise document why separated

\- \*\*Effort:\*\* 1–2 hours (if merging; 15 min if just documenting)

\- \*\*Priority:\*\* Low (works, just messy)



\### 8. Emoji/Encoding Handling Is Workaround

\- \*\*Files:\*\* Multiple (stripped emojis from headers/outputs)

\- \*\*Issue:\*\* Works but not ideal; true solution is stable UTF-8 everywhere

\- \*\*Risk:\*\* May lose information (emoji summaries become bland)

\- \*\*Fix:\*\* Reinstate after ensuring reliable UTF-8 encoding in pipeline

\- \*\*Effort:\*\* 1 hour

\- \*\*Priority:\*\* Low (cosmetic, not functional)



\### 9. Documentation Incomplete

\- \*\*Missing:\*\*

&nbsp; - README.md: No screenshots, no feature list

&nbsp; - Inline comments: Domain pattern design decisions

&nbsp; - Docstrings: Updated after today's changes

&nbsp; - API docs: No usage examples

\- \*\*Risk:\*\* New developers (and you) won't know why code works this way

\- \*\*Fix:\*\* Add 1-page README, 10+ docstrings, API examples

\- \*\*Effort:\*\* 1–2 hours

\- \*\*Priority:\*\* Medium (onboarding)



---



\## Low-Priority Issues (Nice-to-Have)



\### 10. CLI Argument Handling Could Be Robust

\- \*\*File:\*\* `generate\_final\_report.py`

\- \*\*Issue:\*\* Basic sys.argv handling, no validation

\- \*\*Fix:\*\* Add argparse for better help, file existence checks

\- \*\*Effort:\*\* 30 min

\- \*\*Priority:\*\* Low



\### 11. Performance Test Could Output CSV Report

\- \*\*File:\*\* `performance\_test.py`

\- \*\*Issue:\*\* Prints to console; hard to track over time

\- \*\*Fix:\*\* Export results to CSV with timestamp

\- \*\*Effort:\*\* 30 min

\- \*\*Priority:\*\* Low



---



\## Fixed (Completed Today)



\- ✅ E-commerce confidence: 0.08% → 86%

\- ✅ Multi-domain support: Added media + customer patterns

\- ✅ CLI argument support: Flexible CSV testing

\- ✅ Streamlit Cloud deployment: Fixed connection refused error



---



\## Guidelines for Using This File



\*\*At Start of Session:\*\*

\- \[ ] Read "Critical Issues" section

\- \[ ] Decide which to work on today

\- \[ ] Check if any blocker issues were discovered



\*\*During Session:\*\*

\- \[ ] Log any new bugs found

\- \[ ] Note corner-cuts made

\- \[ ] Update effort/priority estimates



\*\*At End of Session:\*\*

\- \[ ] Mark completed issues as fixed

\- \[ ] Update "Last Updated" date

\- \[ ] Commit to Git



---



\## Next Review: 2025-12-01 (Dec 1 session)



