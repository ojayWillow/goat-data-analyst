#!/usr/bin/env python3
"""
Session Bootstrap Script - Full Version
Automatically loads session context and reminds you what to do.
Run at start/end of every session.
"""

import os
from pathlib import Path
from datetime import datetime


def print_header(text):
    """Print formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def check_files_exist():
    """Check if required tracking files exist."""
    files = [
        '.project/ISSUES_BACKLOG.md',
        '.project/SESSION_CHECKLIST.md',
        '.project/ROADMAP.md',
        '.project/NEXT_SESSION_PLAN.md',
    ]
    missing = [f for f in files if not Path(f).exists()]
    if missing:
        print(f"⚠️  Missing files: {missing}")
        return False
    print(f"✅ All tracking files present\n")
    return True


def read_file(filename):
    """Read file content."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None


def extract_critical_issues():
    """Extract critical issues from ISSUES_BACKLOG.md"""
    content = read_file('.project/ISSUES_BACKLOG.md')
    if not content:
        return []
    
    lines = content.split('\n')
    critical = []
    in_critical = False
    
    for line in lines:
        if 'Critical Issues' in line:
            in_critical = True
            continue
        if in_critical and line.startswith('##') and 'Critical' not in line:
            break
        if in_critical and line.startswith('###'):
            critical.append(line.replace('###', '').strip())
    
    return critical[:5]


def extract_next_session_goals():
    """Extract next session goals from NEXT_SESSION_PLAN.md"""
    content = read_file('.project/NEXT_SESSION_PLAN.md')
    if not content:
        return []
    
    lines = content.split('\n')
    goals = []
    
    for line in lines:
        if line.startswith('## Priority'):
            goal = line.replace('##', '').strip()
            if goal:
                goals.append(goal)
    
    return goals[:3]


def show_roadmap_status():
    """Show roadmap progress."""
    content = read_file('.project/ROADMAP.md')
    if not content:
        return
    
    lines = content.split('\n')
    for line in lines:
        if 'Week 1' in line or 'current' in line.lower():
            print(f"📅 {line.strip()}")


def get_git_status():
    """Get recent git commits."""
    print("\nRecent commits:")
    os.system('git log --oneline -3')


def main():
    """Start of session mode."""
    print_header("🚀 SESSION BOOTSTRAP - START")
    
    # 1. Check files
    if not check_files_exist():
        print("❌ Setup incomplete. Files missing in .project/\n")
        return
    
    # 2. Show time
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"📍 Session Start: {now}\n")
    
    # 3. Show critical issues
    print_header("🔴 CRITICAL ISSUES TO KNOW")
    critical = extract_critical_issues()
    if critical:
        for i, issue in enumerate(critical, 1):
            print(f"{i}. {issue}")
    else:
        print("✅ No critical issues")
    
    # 4. Show next session goals
    print_header("🎯 NEXT SESSION PRIORITIES")
    goals = extract_next_session_goals()
    if goals:
        for i, goal in enumerate(goals, 1):
            print(f"{i}. {goal}")
    else:
        print("No priorities defined")
    
    # 5. Show roadmap
    print_header("📈 ROADMAP STATUS")
    show_roadmap_status()


    # Show progress
    print_header("📊 PROJECT PROGRESS")
    show_progress_status()

def show_progress_status():
    """Show project progress and burndown."""
    content = read_file('.project/PROGRESS_LOG.md')
    if not content:
        return
    
    lines = content.split('\n')
    in_metrics = False
    
    for line in lines:
        if 'Week 1 Metrics' in line:
            in_metrics = True
            print(line)
            continue
        if in_metrics and line.startswith('---'):
            break
        if in_metrics and line:
            print(line)

    
    # 6. Show recent commits
    print_header("📝 RECENT COMMITS")
    get_git_status()
    
    # 7. Quick commands
    print_header("⚡ QUICK COMMANDS")
    print("""
# Test everything
python performance_test.py

# Run main report
python generate_final_report.py sample_data/amazon.csv

# Start Streamlit
streamlit run app.py

# Check git status
git status

# View issues backlog
type .project/ISSUES_BACKLOG.md

# View session checklist
type .project/SESSION_CHECKLIST.md
    """)
    
        # 8. Instructions
    print_header("📋 SESSION WORKFLOW")
    print("""
✅ DURING SESSION:
1. Work on tasks from NEXT SESSION PRIORITIES above
2. When task done: git commit + push
3. Log any new issues in .project/ISSUES_BACKLOG.md

✅ AT END OF SESSION:
Run: python session_bootstrap.py --end
    """)

    # 9. Show full workflow file
    print_header("📖 FULL WORKFLOW REFERENCE")
    workflow = read_file('.project/WORKFLOW.md')
    if workflow:
        print(workflow)


def end_session_mode():
    """End of session mode."""
    print_header("🏁 SESSION END CHECKLIST")
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Session End: {now}\n")
    
    print("""
BEFORE YOU LEAVE - CHECK THESE:

🧪 Testing (15 min):
  [ ] python performance_test.py (all datasets OK?)
  [ ] streamlit run app.py (app loads?)
  [ ] python generate_final_report.py (report generates?)
  [ ] Any console errors/warnings?

📝 Documentation (10 min):
  [ ] Updated .project/ISSUES_BACKLOG.md?
  [ ] Updated .project/SESSION_CHECKLIST.md?
  [ ] Clear git commit message ready?

📤 Git (5 min):
  [ ] git add -A
  [ ] git commit -m "Your message"
  [ ] git push

Then you're done! See you next session. 🎉
    """)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--end':
        end_session_mode()
    else:
        main()
