import streamlit as st
import pandas as pd
import sys
import tempfile
import os
from pathlib import Path
import io

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.core.engine import AnalysisEngine
from backend.core.batch_engine import BatchEngine
from backend.data_processing.data_fixer import DataFixer
from backend.reports.company_health_report import CompanyHealthReportGenerator
from backend.auth.streamlit_auth import StreamlitAuth

st.set_page_config(page_title="GOAT Data Analyst", page_icon="🐐", layout="wide")

# === DAY 17: LOAD CUSTOM CSS ===
def load_css():
    try:
        css_file = Path(__file__).parent / '.streamlit' / 'custom.css'
        if css_file.exists():
            with open(css_file, encoding='utf-8') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except Exception:
        pass

load_css()

# === END DAY 17 ===


# === DAY 23: AUTHENTICATION ===
API_URL = os.getenv("API_URL", "goat-data-analyst-production.up.railway.app")
auth = StreamlitAuth(api_url=API_URL)

# Check if logged in
if not auth.is_logged_in():
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("🐐 GOAT Data Analyst")
        st.markdown("### 🔐 Login Required")
        
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
                        st.rerun()
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
    
    st.stop()  # Stop here if not logged in

# User is logged in - show email in sidebar
st.sidebar.markdown(f"👤 **{auth.get_user_email()}**")
if st.sidebar.button("🚪 Logout"):
    auth.logout()
    st.rerun()
st.sidebar.markdown("---")
# === END DAY 23 ===



# Session state for tracking fixed data
if 'original_df' not in st.session_state:
    st.session_state.original_df = None
if 'current_df' not in st.session_state:
    st.session_state.current_df = None
if 'fix_history' not in st.session_state:
    st.session_state.fix_history = []
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'last_uploaded_file' not in st.session_state:
    st.session_state.last_uploaded_file = None
if 'auto_reanalyze' not in st.session_state:
    st.session_state.auto_reanalyze = False

# DAY 15/16: MODE + BATCH STATE
if 'analysis_mode' not in st.session_state:
    st.session_state.analysis_mode = 'single'
if 'batch_results' not in st.session_state:
    st.session_state.batch_results = None
if 'selected_file' not in st.session_state:
    st.session_state.selected_file = None

st.title("🐐 GOAT Data Analyst")
st.markdown("*The AI analyst that understands context, identifies pain points, and provides clear guidance*")

# Mode selector
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("📄 Single File Analysis", use_container_width=True,
                 type="primary" if st.session_state.analysis_mode == 'single' else "secondary"):
        st.session_state.analysis_mode = 'single'
        st.session_state.batch_results = None
        st.session_state.selected_file = None
        st.rerun()
with col2:
    if st.button("📁 Multiple Files Analysis", use_container_width=True,
                 type="primary" if st.session_state.analysis_mode == 'batch' else "secondary"):
        st.session_state.analysis_mode = 'batch'
        st.session_state.analysis_result = None
        st.session_state.original_df = None
        st.session_state.current_df = None
        st.session_state.fix_history = []
        st.session_state.last_uploaded_file = None
        st.rerun()

st.markdown("---")

# ============================================================================
# SINGLE FILE MODE
# ============================================================================
if st.session_state.analysis_mode == 'single':
    # === DAY 17: SAMPLE DATA GALLERY ===
    st.write("**📊 Try Sample Data:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔴 Messy Data", use_container_width=True, help="Duplicates, missing values, outliers"):
            sample_path = Path(__file__).parent / 'sample_data' / 'demo_messy.csv'
            if sample_path.exists():
                df = pd.read_csv(sample_path)
                st.session_state.original_df = df.copy()
                st.session_state.current_df = df.copy()
                st.session_state.last_uploaded_file = 'demo_messy.csv'
                st.session_state.analysis_result = None
                st.session_state.fix_history = []
                progress_bar = st.progress(0, text="Analyzing messy data...")
                progress_bar.progress(30, text="Finding issues...")
                engine = AnalysisEngine()
                progress_bar.progress(70, text="Generating report...")
                result = engine.analyze(df)
                progress_bar.progress(100, text="Complete!")
                st.session_state.analysis_result = result
                progress_bar.empty()
                st.rerun()
    
    with col2:
        if st.button("🟡 Medium Data", use_container_width=True, help="Some missing values"):
            sample_path = Path(__file__).parent / 'sample_data' / 'demo_medium.csv'
            if sample_path.exists():
                df = pd.read_csv(sample_path)
                st.session_state.original_df = df.copy()
                st.session_state.current_df = df.copy()
                st.session_state.last_uploaded_file = 'demo_medium.csv'
                st.session_state.analysis_result = None
                st.session_state.fix_history = []
                progress_bar = st.progress(0, text="Analyzing medium data...")
                progress_bar.progress(30, text="Finding issues...")
                engine = AnalysisEngine()
                progress_bar.progress(70, text="Generating report...")
                result = engine.analyze(df)
                progress_bar.progress(100, text="Complete!")
                st.session_state.analysis_result = result
                progress_bar.empty()
                st.rerun()
    
    with col3:
        if st.button("🟢 Clean Data", use_container_width=True, help="Perfect data"):
            sample_path = Path(__file__).parent / 'sample_data' / 'demo_clean.csv'
            if sample_path.exists():
                df = pd.read_csv(sample_path)
                st.session_state.original_df = df.copy()
                st.session_state.current_df = df.copy()
                st.session_state.last_uploaded_file = 'demo_clean.csv'
                st.session_state.analysis_result = None
                st.session_state.fix_history = []
                progress_bar = st.progress(0, text="Analyzing clean data...")
                progress_bar.progress(30, text="Finding issues...")
                engine = AnalysisEngine()
                progress_bar.progress(70, text="Generating report...")
                result = engine.analyze(df)
                progress_bar.progress(100, text="Complete!")
                st.session_state.analysis_result = result
                progress_bar.empty()
                st.rerun()
    
    st.markdown("---")
    uploaded_file = st.file_uploader("Or upload your own CSV file", type=['csv'])

    if uploaded_file:
        if st.session_state.last_uploaded_file != uploaded_file.name:
            st.session_state.last_uploaded_file = uploaded_file.name
            st.session_state.original_df = None
            st.session_state.current_df = None
            st.session_state.analysis_result = None
            st.session_state.fix_history = []
            st.session_state.auto_reanalyze = False
        
        df = pd.read_csv(uploaded_file)

        if st.session_state.original_df is None:
            st.session_state.original_df = df.copy()
            st.session_state.current_df = df.copy()

        st.success(f"✅ Loaded {len(df)} rows × {len(df.columns)} columns")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Current Rows", len(st.session_state.current_df))
        with col2:
            st.metric("Fixes Applied", len(st.session_state.fix_history))

        # === DAY 17: PROGRESS BAR ===
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

        if st.button("🚀 Run Analysis", type="primary"):
            progress_bar = st.progress(0, text="Starting analysis...")
            progress_bar.progress(20, text="Profiling data...")
            engine = AnalysisEngine()
            progress_bar.progress(50, text="Analyzing quality...")
            progress_bar.progress(70, text="Generating charts...")
            result = engine.analyze(st.session_state.current_df)
            progress_bar.progress(100, text="Complete!")
            st.session_state.analysis_result = result
            progress_bar.empty()

        if st.session_state.analysis_result is not None:
            st.markdown("---")
            
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
            
            st.components.v1.html(st.session_state.analysis_result.report_html, height=2000, scrolling=True)

        if st.session_state.analysis_result is not None:
            st.sidebar.title("🔧 Quick Fixes")

            result = st.session_state.analysis_result
            quality = result.quality

            fixer = DataFixer()

            if quality.get('duplicates', 0) > 0:
                st.sidebar.subheader("🔄 Remove Duplicates")
                st.sidebar.write(f"Found: **{quality['duplicates']}** duplicate rows")
                if st.sidebar.button("Remove Duplicates", key="fix_duplicates"):
                    df_fixed, report = fixer.remove_duplicates(st.session_state.current_df)
                    st.session_state.current_df = df_fixed
                    st.session_state.fix_history.append(report)
                    st.session_state.auto_reanalyze = True
                    st.sidebar.success(f"✅ Removed {report['removed_rows']} duplicates")
                    st.rerun()

            missing_cols = [col for col, count in quality.get('missing_by_column', {}).items() if count > 0]
            if missing_cols:
                st.sidebar.subheader("📝 Fill Missing Values")
                for col in missing_cols[:3]:
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

            outliers = quality.get('outliers', {})
            if outliers:
                st.sidebar.subheader("🎯 Remove Outliers")
                for col, info in list(outliers.items())[:2]:
                    st.sidebar.write(f"**{col}**: {info['count']} outliers")
                    st.sidebar.write(f"Extreme values: {info['extreme_values'][:2]}")
                    if st.sidebar.button(f"Remove {col} outliers", key=f"outlier_{col}"):
                        df_fixed, report = fixer.remove_outliers(st.session_state.current_df, col, method='iqr')
                        st.session_state.current_df = df_fixed
                        st.session_state.fix_history.append(report)
                        st.session_state.auto_reanalyze = True
                        st.sidebar.success(f"✅ Removed {report['removed_rows']} outlier rows")
                        st.rerun()

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

                if st.sidebar.button("↩️ Reset to Original"):
                    st.session_state.current_df = st.session_state.original_df.copy()
                    st.session_state.fix_history = []
                    st.session_state.auto_reanalyze = True
                    st.sidebar.success("Reset to original data")
                    st.rerun()

    # === DAY 17: SHOW INFO IF SAMPLE DATA LOADED ===
    elif st.session_state.original_df is not None:
        st.success(f"✅ Loaded {len(st.session_state.current_df)} rows × {len(st.session_state.current_df.columns)} columns (Sample Data)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Current Rows", len(st.session_state.current_df))
        with col2:
            st.metric("Fixes Applied", len(st.session_state.fix_history))

        if st.button("🚀 Run Analysis", type="primary"):
            progress_bar = st.progress(0, text="Starting analysis...")
            progress_bar.progress(20, text="Profiling data...")
            engine = AnalysisEngine()
            progress_bar.progress(50, text="Analyzing quality...")
            progress_bar.progress(70, text="Generating charts...")
            result = engine.analyze(st.session_state.current_df)
            progress_bar.progress(100, text="Complete!")
            st.session_state.analysis_result = result
            progress_bar.empty()

        if st.session_state.analysis_result is not None:
            st.markdown("---")
            
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
            
            st.components.v1.html(st.session_state.analysis_result.report_html, height=2000, scrolling=True)

    else:
        st.info("👆 Upload a CSV file or try example data to get started")

# ============================================================================
# BATCH MODE
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
        
        if st.button("🚀 Analyze All Files", type="primary"):
            # === DAY 17: PROGRESS BAR FOR BATCH ===
            progress_bar = st.progress(0, text=f"Analyzing {len(uploaded_files)} files...")
            
            temp_dir = tempfile.mkdtemp()
            file_paths = []
            
            for i, uploaded in enumerate(uploaded_files):
                progress_bar.progress(int((i / len(uploaded_files)) * 50), text=f"Processing file {i+1}/{len(uploaded_files)}...")
                file_path = os.path.join(temp_dir, uploaded.name)
                with open(file_path, 'wb') as f:
                    f.write(uploaded.getvalue())
                file_paths.append(file_path)
            
            progress_bar.progress(60, text="Running batch analysis...")
            batch = BatchEngine()
            st.session_state.batch_results = batch.analyze_files(file_paths)
            
            progress_bar.progress(100, text="Complete!")
            import shutil
            shutil.rmtree(temp_dir)
            progress_bar.empty()
        
        if st.session_state.batch_results:
            results = st.session_state.batch_results
            summary = results['summary']
            
            st.markdown("---")
            st.header("📊 Company Data Health Dashboard")
            
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
            
            if summary['top_issues']:
                st.markdown("---")
                st.subheader("⚠️ Top Issues Across All Files")
                for issue in summary['top_issues']:
                    severity_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                    emoji = severity_emoji.get(issue['severity'], "⚪")
                    st.markdown(f"**{emoji} {issue['description']}** - Found in {issue['count']} file(s)")
            
            if summary['files_needing_attention']:
                st.markdown("---")
                st.subheader("🚨 Files Needing Immediate Attention")
                for file_info in summary['files_needing_attention']:
                    with st.expander(f"🔴 {file_info['filename']} - Quality: {file_info['quality_score']:.0f}/100"):
                        st.write("**Issues:**")
                        for issue in file_info['issues']:
                            st.write(f"• {issue}")
            
            st.markdown("---")
            st.subheader("📄 All Files")
            
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
            
            if st.session_state.selected_file:
                st.markdown("---")
                st.subheader(f"📊 Detailed Report: {st.session_state.selected_file.filename}")
                
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
                
                st.components.v1.html(
                    st.session_state.selected_file.report_html, 
                    height=2000, 
                    scrolling=True
                )
    
    else:
        st.info("👆 Upload multiple CSV files to analyze")

st.markdown("---")
st.markdown("*Made with 🐐 by GOAT Data Analyst*")
