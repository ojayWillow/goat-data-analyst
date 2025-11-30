# GOAT Data Analyst - Session Workflow

**Goal:** Maximum speed + quality. No guessing. Finish what we start.

---

## START OF SESSION

1. Open PowerShell in project root
2. Activate venv: `venv\Scripts\Activate.ps1`
3. Check git: `git status`
4. Review `.project/PROGRESS_LOG.md` - What to do today?

---

## DURING SESSION

### One Task at a Time

**For each task:**

1. **Understand** - What exactly needs to happen?
2. **Plan** - 3-5 concrete steps
3. **Execute** - Copy-paste commands / full file code
4. **Test** - Local test immediately
5. **Verify** - Show logs, not guesses
6. **Checkpoint** - Yes/no question before next step

**Do NOT:**
- Leave loose ends
- Jump between tasks
- Partial code (always full files)
- Explain instead of show
- Parallel work

---

## TESTING FLOW
```
Local PowerShell Test
    ↓
Does it work?
├─ YES → git add -A; git commit; git push
│   ↓
│   Auto-deploy to cloud
│   ↓
│   Test live URLs
│   ↓
│   DONE ✅
│
└─ NO → Show error log
    ↓
    Fix specific area (inspect with Python line-by-line)
    ↓
    Re-test
```

---

## COMMUNICATION STYLE

| Do | Don't |
|----|-------|
| "Step 1: Run X" | "You might want to consider..." |
| Full file code | "Change this part..." |
| Test after each change | Multiple tasks at once |
| Show actual logs | Guess what went wrong |
| Yes/no checkpoints | Long explanations |
| One action per message | Options and decisions |

---

## Tools Used

- **PowerShell** - Run scripts, test locally
- **Notepad** - Edit files (save as UTF-8)
- **Git/GitHub** - Commit + push
- **Browser** - Test live URLs
- **venv** - Python environment
- **Python** - Debug line-by-line when needed

---

## Session Structure
```
START
    ↓
Review PROGRESS_LOG.md (what to do today)
    ↓
TASK 1: [Step 1] → [Step 2] → [Step 3] → TEST → COMMIT
    ↓
TASK 2: [Step 1] → [Step 2] → [Step 3] → TEST → COMMIT
    ↓
[Repeat until done]
    ↓
Update PROGRESS_LOG.md with session notes
    ↓
FINISH
```

---

## Key Rule

**Efficiency over perfection, but no compromise on quality.**

- Fast execution
- Clear communication
- Real testing (not assumptions)
- Finish before moving on
- Update tracking files

---
