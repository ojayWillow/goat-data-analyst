\# Session Checklist



\*\*Purpose:\*\* Quick start/end routine for every session. Prevents forgotten issues.



---



\## START OF SESSION



\### Pre-Work (5 min)

\- \[ ] Read ISSUES\_BACKLOG.md "Critical Issues" section

\- \[ ] Check git log: `git log --oneline -5`

\- \[ ] Verify current branch is main: `git branch`

\- \[ ] Pull latest: `git pull`

\- \[ ] Check Streamlit/API still running



\### Session Goals (Write at top of session)

\- Goal 1: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

\- Goal 2: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

\- Goal 3: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_



\### Known Blockers (Check these)

\- \[ ] Datetime detection fragile? (OK for now)

\- \[ ] Domain weights not data-driven? (OK for MVP)

\- \[ ] 1M-row performance untested? (TODO)

\- \[ ] AI insights quality not validated? (TODO)



---



\## DURING SESSION



\### After Each Major Change

\- \[ ] Tested locally first?

\- \[ ] Did it break anything?

\- \[ ] Committed to git?

\- \[ ] Updated ISSUES\_BACKLOG.md?



\### Workflow Discipline

\- \[ ] Read code before changing it

\- \[ ] Test after every change

\- \[ ] Keep responses short (no essays)

\- \[ ] Log corners cut, don't hide them



---



\## END OF SESSION



\### Testing (15 min)

\- \[ ] Run `python performance\_test.py` (all datasets still work?)

\- \[ ] Test Streamlit: Does it load?

\- \[ ] Test main report generation: `python generate\_final\_report.py`

\- \[ ] Check for console errors/warnings



\### Documentation (10 min)

\- \[ ] Updated ISSUES\_BACKLOG.md with new issues?

\- \[ ] Updated SESSION\_CHECKLIST.md with lessons?

\- \[ ] Wrote clear git commit message?



\### Commit \& Push (5 min)



