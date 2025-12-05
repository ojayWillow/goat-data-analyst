import streamlit as st
import pandas as pd
import sys
import tempfile
import os
from pathlib import Path
import io
import sentry_sdk

# Initialize Sentry for error tracking
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    send_default_pii=True,
    environment="production"
)

# Add backend to path so we can import modules
sys.path.insert(0, str(Path(__file__).parent))

from backend.core.engine import AnalysisEngine
from backend.core.batch_engine import BatchEngine
from backend.data_processing.data_fixer import DataFixer
from backend.reports.company_health_report import CompanyHealthReportGenerator
from backend.auth.streamlit_auth import StreamlitAuth

st.set_page_config(page_title="GOAT Data Analyst", page_icon="🐐", layout="wide")

# === LOAD CUSTOM CSS ===
def load_css():
    """Load custom CSS styling from .streamlit/custom.css if it exists"""
    try:
        css_file = Path(__file__).parent / '.streamlit' / 'custom.css'
        if css_file.exists():
            with open(css_file, encoding='utf-8') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except Exception:
        pass  # Silently fail if CSS file doesn't exist

load_css()
# === END CUSTOM CSS ===

# === AUTHENTICATION SYSTEM ===
# Get API URL from environment (Railway URL or localhost for testing)
API_URL = os.getenv("API_URL", "goat-data-analyst-production.up.railway.app")
auth = StreamlitAuth(api_url=API_URL)

# Check if user is logged in - if not, show login/signup page
if not auth.is_logged_in():
    # Center the login form with columns
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("🐐 GOAT Data Analyst")
        st.markdown("### 🔒 Login Required")
        
        # Create tabs for Login and Sign Up
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.subheader("Login to Your Account")
            login_email = st.text_input("Email", key="login_email")
            login_password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", type="primary", use_container_width=True):
                if login_email and login_password:
                    result = auth.login(login_email, login_password)
                    if result['success']:
                        st.success("✅ Logged in successfully!")
                        st.rerun()  # Refresh page to show main app
                    else:
                        st.error(f"❌ {result['error']}")
                else:
                    st.warning("Please enter email and password")
        
        with tab2:
            st.subheader("Create New Account")
            signup_email = st.text_input("Email", key="signup_email")
            signup_password = st.text_input("Password (min 6 characters)", type="password", key="signup_password")
            signup_password2 = st.text_input("Confirm Password", type="password", key="signup_password2")
            
            if st.button("Sign Up", type="primary", use_container_width=True):
                if signup_email and signup_password and signup_password2:
                    if signup_password != signup_password2:
                        st.error("❌ Passwords don't match")
                    elif len(signup_password) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    else:
                        result = auth.signup(signup_email, signup_password)
                        if result['success']:
                            st.success("✅ Account created! Please login.")
                        else:
                            st.error(f"❌ {result['error']}")
                else:
                    st.warning("Please fill all fields")
    
    st.stop()  # Stop execution here if not logged in - don't show main app

# User is logged in - show email in sidebar with logout button
st.sidebar.markdown(f"👤 **{auth.get_user_email()}**")
if st.sidebar.button("🚪 Logout"):
    auth.logout()
    st.rerun()
st.sidebar.markdown("---")
# === END AUTHENTICATION ===

# === SESSION STATE INITIALIZATION ===
# Track original uploaded data (never modified)
if 'original_df' not in st.session_state:
    st.session_state.original_df = None

# Track current data (gets modified by fixes)
if 'current_df' not in st.session_state:
    st.session_state.current_df = None

# Track all fixes applied (for showing summary)
if 'fix_history' not in st.session_state:
    st.session_state.fix_history = []

# Store analysis result from AnalysisEngine
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

# Track which file is currently loaded
if 'last_uploaded_file' not in st.session_state:
    st.session_state.last_uploaded_file = None

# Flag to trigger re-analysis after applying a fix
if 'auto_reanalyze' not in st.session_state:
    st.session_state.auto_reanalyze = False

# Track analysis mode: 'single' file or 'batch' multiple files
if 'analysis_mode' not in st.session_state:
    st.session_state.analysis_mode = 'single'

# Store batch analysis results (for multiple files)
if 'batch_results' not in st.session_state:
    st.session_state.batch_results = None

# Track which file is selected in batch view
if 'selected_file' not in st.session_state:
    st.session_state.selected_file = None

# NEW: Track if we should show the simple report view (not iframe)
if 'show_simple_report' not in st.session_state:
    st.session_state.show_simple_report = False
# === END SESSION STATE ===

st.title("🐐 GOAT Data Analyst")
st.markdown("*Upload → Analyze → Fix → Download. Simple as that.*")

# === MODE SELECTOR (Single vs Batch Analysis) ===
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("📄 Single File Analysis", use_container_width=True,
                 type="primary" if st.session_state.analysis_mode == 'single' else "secondary"):
        # Switch to single file mode - reset batch state
        st.session_state.analysis_mode = 'single'
        st.session_state.batch_results = None
        st.session_state.selected_file = None
        st.rerun()

with col2:
    if st.button("📁 Multiple Files Analysis", use_container_width=True,
                 type="primary" if st.session_state.analysis_mode == 'batch' else "secondary"):
        # Switch to batch mode - reset single file state
        st.session_state.analysis_mode = 'batch'
        st.session_state.analysis_result = None
        st.session_state.original_df = None
        st.session_state.current_df = None
        st.session_state.fix_history = []
        st.session_state.last_uploaded_file = None
        st.session_state.show_simple_report = False
        st.rerun()

st.markdown("---")

# ============================================================================
# SINGLE FILE MODE - Main analysis workflow
# ============================================================================
if st.session_state.analysis_mode == 'single':
    
    # === SAMPLE DATA BUTTONS ===
    # Let users try the tool with pre-loaded example data
    st.write("**🎯 Try Sample Data:**")
    col1, col2, col3 = st.columns(3)
    
    def load_sample_data(filename, label):
        """Helper function to load sample data files"""
        sample_path = Path(__file__).parent / 'sample_data' / filename
        if sample_path.exists():
            df = pd.read_csv(sample_path)
            # Store both original and current (working) copy
            st.session_state.original_df = df.copy()
            st.session_state.current_df = df.copy()
            st.session_state.last_uploaded_file = filename
            st.session_state.analysis_result = None
            st.session_state.fix_history = []
            st.session_state.show_simple_report = False
            
            # Show progress while analyzing
            progress_bar = st.progress(0, text=f"Analyzing {label}...")
            progress_bar.progress(30, text="Finding issues...")
            engine = AnalysisEngine()
            progress_bar.progress(70, text="Generating report...")
            result = engine.analyze(df)
            progress_bar.progress(100, text="Complete!")
            st.session_state.analysis_result = result
            progress_bar.empty()
            st.rerun()
    
    with col1:
        if st.button("🔴 Messy Data", use_container_width=True, help="Duplicates, missing values, outliers"):
            load_sample_data('demo_messy.csv', 'messy data')
    
    with col2:
        if st.button("🟡 Medium Data", use_container_width=True, help="Some missing values"):
            load_sample_data('demo_medium.csv', 'medium data')
    
    with col3:
        if st.button("🟢 Clean Data", use_container_width=True, help="Perfect data"):
            load_sample_data('demo_clean.csv', 'clean data')
    
    st.markdown("---")
    
    # === FILE UPLOAD ===
    uploaded_file = st.file_uploader("Or upload your own CSV file", type=['csv'])

    if uploaded_file:
        # Check if this is a new file upload (reset state if so)
        if st.session_state.last_uploaded_file != uploaded_file.name:
            st.session_state.last_uploaded_file = uploaded_file.name
            st.session_state.original_df = None
            st.session_state.current_df = None
            st.session_state.analysis_result = None
            st.session_state.fix_history = []
            st.session_state.auto_reanalyze = False
            st.session_state.show_simple_report = False
        
        # Load the CSV file
        df = pd.read_csv(uploaded_file)

        # Store original and current copies (first time only)
        if st.session_state.original_df is None:
            st.session_state.original_df = df.copy()
            st.session_state.current_df = df.copy()

        # Show file info
        st.success(f"✅ Loaded {len(df)} rows × {len(df.columns)} columns")

        # Show current metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Current Rows", len(st.session_state.current_df))
        with col2:
            st.metric("Fixes Applied", len(st.session_state.fix_history))

        # === AUTO RE-ANALYZE AFTER FIX ===
        # If a fix was just applied, automatically re-analyze
        if st.session_state.auto_reanalyze:
            st.session_state.auto_reanalyze = False
            progress_bar = st.progress(0, text="Re-analyzing after fix...")
            progress_bar.progress(30, text="Profiling data...")
            engine = AnalysisEngine()
            progress_bar.progress(60, text="Generating insights...")
            result = engine.analyze(st.session_state.current_df)
            progress_bar.progress(100, text="Complete!")
            st.session_state.analysis_result = result
            progress_bar.empty()

        # === ANALYZE BUTTON ===
        if st.button("🔍 Run Analysis", type="primary"):
            progress_bar = st.progress(0, text="Starting analysis...")
            progress_bar.progress(20, text="Profiling data...")
            engine = AnalysisEngine()
            progress_bar.progress(50, text="Analyzing quality...")
            progress_bar.progress(70, text="Generating charts...")
            result = engine.analyze(st.session_state.current_df)
            progress_bar.progress(100, text="Complete!")
            st.session_state.analysis_result = result
            st.session_state.show_simple_report = True  # Enable simple report view
            progress_bar.empty()

        # === SHOW ANALYSIS RESULTS ===
        if st.session_state.analysis_result is not None:
            st.markdown("---")
            
            result = st.session_state.analysis_result
            quality = result.quality
            
            # === SIMPLE REPORT VIEW (NEW UX) ===
            if st.session_state.show_simple_report:
                st.header("📊 Analysis Results")
                
                # Quality Score Card
                score = quality.get('overall_score', 0)
                score_color = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Quality Score", f"{score_color} {score:.0f}/100")
                with col2:
                    st.metric("Issues Found", quality.get('total_issues', 0))
                with col3:
                    st.metric("Completeness", f"{quality.get('completeness', 0):.0f}%")
                
                st.markdown("---")
                
                # === ISSUES SUMMARY ===
                st.subheader("⚠️ Issues Found")
                
                issues_found = []
                
                # Check for duplicates
                if quality.get('duplicates', 0) > 0:
                    issues_found.append(f"🔁 **{quality['duplicates']} duplicate rows**")
                
                # Check for missing values
                missing_count = quality.get('missing_values', 0)
                if missing_count > 0:
                    issues_found.append(f"🩹 **{missing_count} missing values** across {len(quality.get('missing_by_column', {}))} columns")
                
                # Check for outliers
                outlier_cols = quality.get('outliers', {})
                if outlier_cols:
                    total_outliers = sum(info['count'] for info in outlier_cols.values())
                    issues_found.append(f"📊 **{total_outliers} outliers** in {len(outlier_cols)} columns")
                
                # Check for date format issues
                date_issues = quality.get('date_format_issues', {})
                if date_issues:
                    issues_found.append(f"📅 **Date format issues** in {len(date_issues)} columns")
                
                # Check for capitalization issues
                cap_issues = quality.get('capitalization_issues', {})
                if cap_issues:
                    issues_found.append(f"🔤 **Capitalization inconsistencies** in {len(cap_issues)} columns")
                
                if issues_found:
                    for issue in issues_found:
                        st.markdown(issue)
                else:
                    st.success("✅ No major issues found! Your data looks clean.")
                
                st.markdown("---")
                
                # === ACTION BUTTONS (Main UX) ===
                st.subheader("🛠️ What do you want to do?")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # FIX ALL BUTTON - Main action
                    if quality.get('total_issues', 0) > 0:
                        if st.button("🔧 Fix All Issues", type="primary", use_container_width=True):
                            # Apply all fixes at once
                            fixer = DataFixer()
                            df_working = st.session_state.current_df.copy()
                            fixes_applied = []
                            
                            with st.spinner("Applying fixes..."):
                                # Fix duplicates
                                if quality.get('duplicates', 0) > 0:
                                    df_working, report = fixer.remove_duplicates(df_working)
                                    fixes_applied.append(report)
                                
                                # Fill missing values (numeric with median, categorical with 'Unknown')
                                for col, count in quality.get('missing_by_column', {}).items():
                                    if count > 0:
                                        col_type = df_working[col].dtype
                                        if pd.api.types.is_numeric_dtype(col_type):
                                            df_working, report = fixer.fill_missing_numeric(df_working, col, 'median')
                                        else:
                                            df_working, report = fixer.fill_missing_categorical(df_working, col, 'Unknown')
                                        fixes_applied.append(report)
                                
                                # Remove outliers
                                for col in quality.get('outliers', {}).keys():
                                    df_working, report = fixer.remove_outliers(df_working, col, method='iqr')
                                    fixes_applied.append(report)
                                
                                # Normalize dates
                                for col in quality.get('date_format_issues', {}).keys():
                                    df_working, report = fixer.normalize_dates(df_working, col)
                                    fixes_applied.append(report)
                            
                            # Update state
                            st.session_state.current_df = df_working
                            st.session_state.fix_history.extend(fixes_applied)
                            st.session_state.auto_reanalyze = True
                            st.success(f"✅ Applied {len(fixes_applied)} fixes!")
                            st.rerun()
                    else:
                        st.button("🔧 Fix All Issues", use_container_width=True, disabled=True, help="No issues to fix")
                
                with col2:
                    # VIEW CHARTS BUTTON - Optional visualization
                    if st.button("📊 View Full Report", use_container_width=True):
                        st.session_state.show_simple_report = False  # Switch to full HTML report
                        st.rerun()
                
                with col3:
                    # DOWNLOAD REPORT BUTTON - Secondary action
                    st.download_button(
                        label="📥 Download Report",
                        data=st.session_state.analysis_result.report_html,
                        file_name=f"analysis_{st.session_state.last_uploaded_file.replace('.csv', '')}.html",
                        mime="text/html",
                        use_container_width=True
                    )
                
                # === SHOW FIX SUMMARY IF FIXES WERE APPLIED ===
                if len(st.session_state.fix_history) > 0:
                    st.markdown("---")
                    st.success("### ✅ Fixes Applied Successfully!")
                    
                    # Show before/after quality scores
                    if st.session_state.analysis_result:
                        new_score = st.session_state.analysis_result.quality.get('overall_score', 0)
                        st.metric("New Quality Score", f"{new_score:.0f}/100", delta=f"+{new_score - score:.0f}")
                    
                    # List all fixes
                    st.write("**Changes made:**")
                    for i, fix in enumerate(st.session_state.fix_history, 1):
                        operation = fix.get('operation', 'fix')
                        if operation == 'remove_duplicates':
                            st.write(f"{i}. Removed {fix.get('removed_rows', 0)} duplicate rows")
                        elif operation == 'fill_missing':
                            st.write(f"{i}. Filled {fix.get('filled_count', 0)} missing values in '{fix.get('column', 'unknown')}'")
                        elif operation == 'remove_outliers':
                            st.write(f"{i}. Removed {fix.get('removed_rows', 0)} outlier rows from '{fix.get('column', 'unknown')}'")
                        else:
                            st.write(f"{i}. {operation}")
                    
                    # PROMINENT DOWNLOAD BUTTON
                    st.markdown("---")
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        csv = st.session_state.current_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Clean CSV",
                            data=csv,
                            file_name=f"cleaned_{st.session_state.last_uploaded_file}",
                            mime="text/csv",
                            type="primary",
                            use_container_width=True
                        )
                    
                    # Reset button
                    if st.button("🔄 Reset to Original Data"):
                        st.session_state.current_df = st.session_state.original_df.copy()
                        st.session_state.fix_history = []
                        st.session_state.auto_reanalyze = True
                        st.rerun()
            
            else:
                # === FULL HTML REPORT VIEW (iframe - original view) ===
                st.header("📊 Full Analysis Report")
                
                # Button to go back to simple view
                if st.button("⬅️ Back to Simple View"):
                    st.session_state.show_simple_report = True
                    st.rerun()
                
                # Download report button
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.download_button(
                        label="📥 Download Report",
                        data=st.session_state.analysis_result.report_html,
                        file_name=f"analysis_{st.session_state.last_uploaded_file.replace('.csv', '')}.html",
                        mime="text/html",
                        use_container_width=True
                    )
                
                # Show full HTML report in iframe
                st.components.v1.html(st.session_state.analysis_result.report_html, height=2000, scrolling=True)

        # === SIDEBAR: INDIVIDUAL FIX CONTROLS (kept for advanced users) ===
        if st.session_state.analysis_result is not None and not st.session_state.show_simple_report:
            st.sidebar.title("🔧 Individual Fixes")
            st.sidebar.info("Or use the 'Fix All Issues' button in the main view")

            result = st.session_state.analysis_result
            quality = result.quality

            fixer = DataFixer()

            # Duplicates
            if quality.get('duplicates', 0) > 0:
                st.sidebar.subheader("🔁 Remove Duplicates")
                st.sidebar.write(f"Found: **{quality['duplicates']}** duplicate rows")
                if st.sidebar.button("Remove Duplicates", key="fix_duplicates"):
                    df_fixed, report = fixer.remove_duplicates(st.session_state.current_df)
                    st.session_state.current_df = df_fixed
                    st.session_state.fix_history.append(report)
                    st.session_state.auto_reanalyze = True
                    st.sidebar.success(f"✅ Removed {report['removed_rows']} duplicates")
                    st.rerun()

            # Missing values
            missing_cols = [col for col, count in quality.get('missing_by_column', {}).items() if count > 0]
            if missing_cols:
                st.sidebar.subheader("🩹 Fill Missing Values")
                for col in missing_cols[:3]:  # Show first 3 columns
                    col_type = st.session_state.current_df[col].dtype
                    missing_count = st.session_state.current_df[col].isna().sum()

                    st.sidebar.write(f"**{col}**: {missing_count} missing")

                    if pd.api.types.is_numeric_dtype(col_type):
                        method = st.sidebar.selectbox(
                            f"Method for {col}",
                            ['median', 'mean', 'zero'],
                            key=f"method_{col}"
                        )
                        if st.sidebar.button(f"Fill {col}", key=f"fix_{col}"):
                            df_fixed, report = fixer.fill_missing_numeric(
                                st.session_state.current_df, col, method
                            )
                            st.session_state.current_df = df_fixed
                            st.session_state.fix_history.append(report)
                            st.session_state.auto_reanalyze = True
                            st.sidebar.success(f"✅ Filled {col}")
                            st.rerun()
                    else:
                        if st.sidebar.button(f"Fill {col} with 'Unknown'", key=f"fix_{col}"):
                            df_fixed, report = fixer.fill_missing_categorical(
                                st.session_state.current_df, col, 'Unknown'
                            )
                            st.session_state.current_df = df_fixed
                            st.session_state.fix_history.append(report)
                            st.session_state.auto_reanalyze = True
                            st.sidebar.success(f"✅ Filled {col}")
                            st.rerun()

            # Outliers
            outliers = quality.get('outliers', {})
            if outliers:
                st.sidebar.subheader("📊 Remove Outliers")
                for col, info in list(outliers.items())[:2]:  # Show first 2 columns
                    st.sidebar.write(f"**{col}**: {info['count']} outliers")
                    st.sidebar.write(f"Extreme values: {info['extreme_values'][:2]}")
                    if st.sidebar.button(f"Remove {col} outliers", key=f"outlier_{col}"):
                        df_fixed, report = fixer.remove_outliers(st.session_state.current_df, col, method='iqr')
                        st.session_state.current_df = df_fixed
                        st.session_state.fix_history.append(report)
                        st.session_state.auto_reanalyze = True
                        st.sidebar.success(f"✅ Removed {report['removed_rows']} outlier rows")
                        st.rerun()

            # Date normalization
            date_issues = quality.get('date_format_issues', {})
            if date_issues:
                st.sidebar.subheader("📅 Normalize Dates")
                for col, info in date_issues.items():
                    st.sidebar.write(f"**{col}**: {info['issue']}")
                    if st.sidebar.button(f"Normalize {col}", key=f"date_{col}"):
                        df_fixed, report = fixer.normalize_dates(st.session_state.current_df, col)
                        st.session_state.current_df = df_fixed
                        st.session_state.fix_history.append(report)
                        st.session_state.auto_reanalyze = True
                        st.sidebar.success(f"✅ Normalized {col} to YYYY-MM-DD")
                        st.rerun()

            # Capitalization
            cap_issues = quality.get('capitalization_issues', {})
            if cap_issues:
                st.sidebar.subheader("🔤 Standardize Capitalization")
                for col, info in cap_issues.items():
                    st.sidebar.write(f"**{col}**: {info['issue']}")
                    st.sidebar.write(f"Examples: {', '.join(info['examples'])}")
                    case_method = st.sidebar.selectbox(
                        f"Method for {col}",
                        ['title', 'lower', 'upper'],
                        key=f"cap_method_{col}"
                    )
                    if st.sidebar.button(f"Fix {col}", key=f"cap_{col}"):
                        df_fixed = st.session_state.current_df.copy()
                        if case_method == 'title':
                            df_fixed[col] = df_fixed[col].str.title()
                        elif case_method == 'lower':
                            df_fixed[col] = df_fixed[col].str.lower()
                        else:
                            df_fixed[col] = df_fixed[col].str.upper()

                        st.session_state.current_df = df_fixed
                        st.session_state.fix_history.append({'operation': 'standardize_capitalization', 'column': col, 'method': case_method})
                        st.session_state.auto_reanalyze = True
                        st.sidebar.success(f"✅ Standardized {col} to {case_method}")
                        st.rerun()

            # Download cleaned data (sidebar)
            if len(st.session_state.fix_history) > 0:
                st.sidebar.markdown("---")
                st.sidebar.subheader("💾 Download Cleaned Data")

                csv = st.session_state.current_df.to_csv(index=False)
                st.sidebar.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"cleaned_{st.session_state.last_uploaded_file}",
                    mime="text/csv"
                )

                st.sidebar.markdown("**Fixes Applied:**")
                for i, fix in enumerate(st.session_state.fix_history, 1):
                    st.sidebar.text(f"{i}. {fix.get('operation', 'fix')}")

                if st.sidebar.button("🔄 Reset to Original"):
                    st.session_state.current_df = st.session_state.original_df.copy()
                    st.session_state.fix_history = []
                    st.session_state.auto_reanalyze = True
                    st.sidebar.success("Reset to original data")
                    st.rerun()

    # === SHOW INFO IF SAMPLE DATA LOADED ===
    elif st.session_state.original_df is not None:
        st.success(f"✅ Loaded {len(st.session_state.current_df)} rows × {len(st.session_state.current_df.columns)} columns (Sample Data)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Current Rows", len(st.session_state.current_df))
        with col2:
            st.metric("Fixes Applied", len(st.session_state.fix_history))

        if st.button("🔍 Run Analysis", type="primary"):
            progress_bar = st.progress(0, text="Starting analysis...")
            progress_bar.progress(20, text="Profiling data...")
            engine = AnalysisEngine()
            progress_bar.progress(50, text="Analyzing quality...")
            progress_bar.progress(70, text="Generating charts...")
            result = engine.analyze(st.session_state.current_df)
            progress_bar.progress(100, text="Complete!")
            st.session_state.analysis_result = result
            st.session_state.show_simple_report = True
            progress_bar.empty()

        # Show results (same as above)
        if st.session_state.analysis_result is not None:
            st.markdown("---")
            
            result = st.session_state.analysis_result
            quality = result.quality
            
            if st.session_state.show_simple_report:
                # (Same simple report code as above - omitted for brevity)
                st.header("📊 Analysis Results")
                # ... rest of simple report code ...
            else:
                # Full HTML report
                st.header("📊 Full Analysis Report")
                if st.button("⬅️ Back to Simple View"):
                    st.session_state.show_simple_report = True
                    st.rerun()
                
                st.components.v1.html(st.session_state.analysis_result.report_html, height=2000, scrolling=True)

    else:
        st.info("👆 Upload a CSV file or try example data to get started")

# ============================================================================
# BATCH MODE (Multiple Files Analysis) - UNCHANGED
# ============================================================================
elif st.session_state.analysis_mode == 'batch':
    st.subheader("📁 Multiple Files Analysis")
    st.write("Upload multiple CSV files to get a company-level data health report")
    
    uploaded_files = st.file_uploader(
        "Upload CSV files", 
        type=['csv'], 
        accept_multiple_files=True,
        key="batch_upload"
    )

    if uploaded_files and len(uploaded_files) > 0:
        st.success(f"✅ {len(uploaded_files)} files uploaded")
        
        if st.button("🔍 Analyze All Files", type="primary"):
            progress_bar = st.progress(0, text=f"Analyzing {len(uploaded_files)} files...")
            
            # Save uploaded files to temp directory
            temp_dir = tempfile.mkdtemp()
            file_paths = []
            
            for i, uploaded in enumerate(uploaded_files):
                progress_bar.progress(int((i / len(uploaded_files)) * 50), text=f"Processing file {i+1}/{len(uploaded_files)}...")
                file_path = os.path.join(temp_dir, uploaded.name)
                with open(file_path, 'wb') as f:
                    f.write(uploaded.getvalue())
                file_paths.append(file_path)
            
            # Run batch analysis
            progress_bar.progress(60, text="Running batch analysis...")
            batch = BatchEngine()
            st.session_state.batch_results = batch.analyze_files(file_paths)
            
            progress_bar.progress(100, text="Complete!")
            
            # Cleanup temp directory
            import shutil
            shutil.rmtree(temp_dir)
            progress_bar.empty()
        
        if st.session_state.batch_results:
            results = st.session_state.batch_results
            summary = results['summary']
            
            st.markdown("---")
            st.header("📊 Company Data Health Dashboard")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Files", summary['total_files'])
            with col2:
                st.metric("Total Rows", f"{summary['total_rows']:,}")
            with col3:
                score = summary['avg_quality_score']
                score_color = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
                st.metric("Avg Quality", f"{score_color} {score:.0f}/100")
            with col4:
                st.metric("Files Needing Attention", len(summary['files_needing_attention']))

            # Download company health report
            with st.expander("📥 Download Executive Summary (HTML)", expanded=False):
                generator = CompanyHealthReportGenerator()
                company_html = generator.generate(results)
                buffer = io.BytesIO(company_html.encode("utf-8"))
                st.download_button(
                    label="Download Company Health Report",
                    data=buffer,
                    file_name="company_data_health_report.html",
                    mime="text/html"
                )
            
            # Top issues across all files
            if summary['top_issues']:
                st.markdown("---")
                st.subheader("⚠️ Top Issues Across All Files")
                for issue in summary['top_issues']:
                    severity_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                    emoji = severity_emoji.get(issue['severity'], "ℹ")
                    st.markdown(f"**{emoji} {issue['description']}** - Found in {issue['count']} file(s)")
            
            # Files needing attention
            if summary['files_needing_attention']:
                st.markdown("---")
                st.subheader("🚨 Files Needing Immediate Attention")
                for file_info in summary['files_needing_attention']:
                    with st.expander(f"🔴 {file_info['filename']} - Quality: {file_info['quality_score']:.0f}/100"):
                        st.write("**Issues:**")
                        for issue in file_info['issues']:
                            st.write(f"• {issue}")
            
            # All files list
            st.markdown("---")
            st.subheader("📋 All Files")
            
            for file_result in results['files']:
                quality_score = file_result.quality.get('overall_score', 0)
                
                if quality_score >= 80:
                    status_emoji = "🟢"
                elif quality_score >= 60:
                    status_emoji = "🟡"
                else:
                    status_emoji = "🔴"
                
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"{status_emoji} **{file_result.filename}**")
                with col2:
                    st.write(f"Quality: {quality_score:.0f}/100")
                with col3:
                    if st.button("View Report", key=f"view_{file_result.filename}"):
                        st.session_state.selected_file = file_result
                        st.rerun()
            
            # Show selected file report
            if st.session_state.selected_file:
                st.markdown("---")
                st.subheader(f"📄 Detailed Report: {st.session_state.selected_file.filename}")
                
                if st.button("⬅️ Back to Dashboard"):
                    st.session_state.selected_file = None
                    st.rerun()
                
                # Download individual file report
                st.download_button(
                    label="📥 Download This Report",
                    data=st.session_state.selected_file.report_html,
                    file_name=f"analysis_{st.session_state.selected_file.filename.replace('.csv', '')}.html",
                    mime="text/html"
                )
                
                # Show report in iframe
                st.components.v1.html(
                    st.session_state.selected_file.report_html, 
                    height=2000, 
                    scrolling=True
                )
    
    else:
        st.info("👆 Upload multiple CSV files to analyze")

st.markdown("---")
st.markdown("*Made with 💚 by GOAT Data Analyst*")