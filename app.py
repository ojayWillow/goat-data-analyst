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
        pass

load_css()
# === END CUSTOM CSS ===

# === AUTHENTICATION SYSTEM ===
API_URL = os.getenv("API_URL", "goat-data-analyst-production.up.railway.app")
auth = StreamlitAuth(api_url=API_URL)

if not auth.is_logged_in():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🐐 GOAT Data Analyst")
        st.markdown("### 🔒 Login Required")
        
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
    
    st.stop()

st.sidebar.markdown(f"👤 **{auth.get_user_email()}**")
if st.sidebar.button("🚪 Logout"):
    auth.logout()
    st.rerun()
st.sidebar.markdown("---")
# === END AUTHENTICATION ===

# === SESSION STATE INITIALIZATION ===
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
if 'analysis_mode' not in st.session_state:
    st.session_state.analysis_mode = 'single'
if 'batch_results' not in st.session_state:
    st.session_state.batch_results = None
if 'selected_file' not in st.session_state:
    st.session_state.selected_file = None
if 'show_simple_report' not in st.session_state:
    st.session_state.show_simple_report = False
if 'show_fix_preview' not in st.session_state:
    st.session_state.show_fix_preview = False
if 'fix_choices' not in st.session_state:
    st.session_state.fix_choices = {}
if 'preview_data' not in st.session_state:
    st.session_state.preview_data = None
# === END SESSION STATE ===

# === HELPER FUNCTIONS ===

def prepare_fix_preview(quality, current_df):
    """
    Prepare preview data categorizing fixes into auto (safe) and manual (needs decision).
    
    Args:
        quality: Quality report from analysis
        current_df: Current dataframe
        
    Returns:
        Dict with 'auto_fixes' and 'manual_fixes' lists
    """
    auto_fixes = []
    manual_fixes = []
    total_rows = len(current_df)
    
    # AUTO-FIXES (Safe operations that don't need user input)
    if quality.get('duplicates', 0) > 0:
        auto_fixes.append(f"Remove {quality['duplicates']} duplicate rows")
    
    if quality.get('date_format_issues', {}):
        auto_fixes.append(f"Standardize date formats in {len(quality['date_format_issues'])} columns")
    
    # MANUAL FIXES (Risky operations that need user decision)
    missing_by_col = quality.get('missing_by_column', {})
    for col, missing_count in missing_by_col.items():
        if missing_count > 0:
            missing_pct = (missing_count / total_rows * 100)
            col_type = current_df[col].dtype
            
            if pd.api.types.is_numeric_dtype(col_type):
                median = current_df[col].median()
                mean = current_df[col].mean()
                manual_fixes.append({
                    'column': col,
                    'type': 'missing',
                    'description': f'{missing_count} missing values ({missing_pct:.1f}%)',
                    'is_numeric': True,
                    'info': {
                        'count': missing_count,
                        'percentage': missing_pct,
                        'median': median,
                        'mean': mean
                    }
                })
            else:
                mode_values = current_df[col].mode()
                mode = mode_values[0] if len(mode_values) > 0 else 'Unknown'
                manual_fixes.append({
                    'column': col,
                    'type': 'missing',
                    'description': f'{missing_count} missing values ({missing_pct:.1f}%)',
                    'is_numeric': False,
                    'info': {
                        'count': missing_count,
                        'percentage': missing_pct,
                        'mode': mode
                    }
                })
    
    outlier_cols = quality.get('outliers', {})
    for col, info in outlier_cols.items():
        manual_fixes.append({
            'column': col,
            'type': 'outliers',
            'description': f"{info['count']} outliers",
            'count': info['count'],
            'extreme_values': str(info['extreme_values'][:3])
        })
    
    return {
        'auto_fixes': auto_fixes,
        'manual_fixes': manual_fixes
    }

def apply_quick_fix(quality, current_df):
    """
    Apply ONLY safe auto-fixes (duplicates and dates).
    NO missing values, NO outliers - those need user decision.
    
    Args:
        quality: Quality report
        current_df: Current dataframe
        
    Returns:
        Tuple of (fixed_df, fixes_applied_list)
    """
    fixer = DataFixer()
    df_working = current_df.copy()
    fixes_applied = []
    
    # ONLY SAFE FIXES
    # 1. Remove duplicates (always safe)
    if quality.get('duplicates', 0) > 0:
        df_working, report = fixer.remove_duplicates(df_working)
        fixes_applied.append(report)
    
    # 2. Normalize dates (always safe)
    for col in quality.get('date_format_issues', {}).keys():
        df_working, report = fixer.normalize_dates(df_working, col)
        fixes_applied.append(report)
    
    # DO NOT touch missing values - user needs to decide
    # DO NOT touch outliers - user needs to decide
    
    return df_working, fixes_applied

def apply_fixes_with_choices(quality, current_df, fix_choices):
    """
    Apply fixes based on user choices from preview modal.
    
    Args:
        quality: Quality report
        current_df: Current dataframe
        fix_choices: Dict of user choices {column: choice}
        
    Returns:
        Tuple of (fixed_df, fixes_applied_list)
    """
    fixer = DataFixer()
    df_working = current_df.copy()
    fixes_applied = []
    
    # Apply auto-fixes first
    if quality.get('duplicates', 0) > 0:
        df_working, report = fixer.remove_duplicates(df_working)
        fixes_applied.append(report)
    
    for col in quality.get('date_format_issues', {}).keys():
        df_working, report = fixer.normalize_dates(df_working, col)
        fixes_applied.append(report)
    
    # Apply manual choices
    missing_by_col = quality.get('missing_by_column', {})
    outlier_cols = quality.get('outliers', {})
    
    for col, choice in fix_choices.items():
        if col in missing_by_col:
            col_type = df_working[col].dtype
            if pd.api.types.is_numeric_dtype(col_type):
                if choice == 'Median':
                    df_working, report = fixer.fill_missing_numeric(df_working, col, 'median')
                    fixes_applied.append(report)
                elif choice == 'Mean':
                    df_working, report = fixer.fill_missing_numeric(df_working, col, 'mean')
                    fixes_applied.append(report)
                elif choice == 'Remove rows':
                    rows_before = len(df_working)
                    df_working = df_working.dropna(subset=[col])
                    fixes_applied.append({'operation': 'remove_rows', 'column': col, 'removed_rows': rows_before - len(df_working)})
            else:
                if choice == 'Most common':
                    df_working, report = fixer.fill_missing_categorical(df_working, col, 'mode')
                    fixes_applied.append(report)
                elif choice == 'Unknown':
                    df_working, report = fixer.fill_missing_categorical(df_working, col, 'Unknown')
                    fixes_applied.append(report)
                elif choice == 'Remove rows':
                    rows_before = len(df_working)
                    df_working = df_working.dropna(subset=[col])
                    fixes_applied.append({'operation': 'remove_rows', 'column': col, 'removed_rows': rows_before - len(df_working)})
        
        if col in outlier_cols:
            if choice == 'Remove':
                df_working, report = fixer.remove_outliers(df_working, col)
                fixes_applied.append(report)
            # 'Keep' means do nothing
    
    return df_working, fixes_applied

def render_fix_preview_modal(preview_data, quality):
    """
    Render the smart fix preview modal with user choices.
    
    Args:
        preview_data: Dict with auto_fixes and manual_fixes
        quality: Quality report
    """
    st.markdown("---")
    st.markdown("### 🔍 Smart Fix Preview")
    st.markdown("Review what will be fixed and make your choices:")
    
    # AUTO-FIXES SECTION
    if preview_data['auto_fixes']:
        st.success("✅ **AUTO-FIXED** (safe, no confirmation needed):")
        for fix in preview_data['auto_fixes']:
            st.markdown(f"  • {fix}")
    
    # MANUAL CHOICES SECTION
    if preview_data['manual_fixes']:
        st.warning(f"⚠️ **NEEDS YOUR DECISION** ({len(preview_data['manual_fixes'])} items):")
        
        for i, fix_item in enumerate(preview_data['manual_fixes']):
            st.markdown(f"**{i+1}. {fix_item['column']}** - {fix_item['description']}")
            
            if fix_item['type'] == 'missing':
                col_info = fix_item['info']
                st.markdown(f"  Missing: {col_info['count']} values ({col_info['percentage']:.1f}%)")
                
                if fix_item['is_numeric']:
                    st.markdown(f"  📊 Median: **{col_info['median']:.2f}** | Mean: **{col_info['mean']:.2f}**")
                    choice = st.selectbox(
                        f"How to fill missing values in {fix_item['column']}?",
                        ['Median', 'Mean', 'Remove rows'],
                        key=f"fix_choice_{i}",
                        help="Median is safer for data with outliers. Mean is better for normally distributed data."
                    )
                else:
                    st.markdown(f"  📊 Most common value: **{col_info['mode']}**")
                    choice = st.selectbox(
                        f"How to fill missing values in {fix_item['column']}?",
                        ['Most common', 'Unknown', 'Remove rows'],
                        key=f"fix_choice_{i}",
                        help="Most common uses the mode. Unknown is safer if you're unsure."
                    )
                
                st.session_state.fix_choices[fix_item['column']] = choice
            
            elif fix_item['type'] == 'outliers':
                st.markdown(f"  📊 Outlier count: **{fix_item['count']}**")
                st.markdown(f"  🔍 Extreme values: {fix_item['extreme_values']}")
                choice = st.selectbox(
                    f"How to handle outliers in {fix_item['column']}?",
                    ['Remove', 'Keep'],
                    key=f"fix_choice_{i}",
                    index=0,
                    help="Remove: Delete rows with outliers. Keep: Leave data as-is."
                )
                st.session_state.fix_choices[fix_item['column']] = choice
            
            st.markdown("")  # Spacing
    
    # ACTION BUTTONS
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Apply Fixes", type="primary", use_container_width=True, key="apply_fixes_modal"):
            with st.spinner("Applying your fixes..."):
                df_working, fixes_applied = apply_fixes_with_choices(
                    quality, 
                    st.session_state.current_df, 
                    st.session_state.fix_choices
                )
                
                st.session_state.current_df = df_working
                st.session_state.fix_history.extend(fixes_applied)
                st.session_state.auto_reanalyze = True
                st.session_state.show_fix_preview = False
                st.session_state.preview_data = None
                st.session_state.fix_choices = {}
                st.success(f"✅ Applied {len(fixes_applied)} fixes!")
                st.rerun()
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True, key="cancel_fixes_modal"):
            st.session_state.show_fix_preview = False
            st.session_state.preview_data = None
            st.session_state.fix_choices = {}
            st.rerun()

def render_sidebar_fixes(quality, current_df):
    """
    Render individual fix controls in sidebar (only in full report view).
    
    Args:
        quality: Quality report
        current_df: Current dataframe
    """
    st.sidebar.title("🔧 Individual Fixes")
    st.sidebar.info("Fix specific issues one at a time")
    
    fixer = DataFixer()
    
    # Duplicates
    if quality.get('duplicates', 0) > 0:
        st.sidebar.subheader("🔁 Remove Duplicates")
        st.sidebar.write(f"Found: **{quality['duplicates']}** duplicate rows")
        if st.sidebar.button("Remove Duplicates", key="fix_duplicates_sidebar"):
            df_fixed, report = fixer.remove_duplicates(current_df)
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
            col_type = current_df[col].dtype
            missing_count = current_df[col].isna().sum()
            st.sidebar.write(f"**{col}**: {missing_count} missing")
            
            if pd.api.types.is_numeric_dtype(col_type):
                method = st.sidebar.selectbox(
                    f"Method for {col}",
                    ['median', 'mean', 'zero'],
                    key=f"method_sidebar_{col}"
                )
                if st.sidebar.button(f"Fill {col}", key=f"fix_sidebar_{col}"):
                    df_fixed, report = fixer.fill_missing_numeric(current_df, col, method)
                    st.session_state.current_df = df_fixed
                    st.session_state.fix_history.append(report)
                    st.session_state.auto_reanalyze = True
                    st.sidebar.success(f"✅ Filled {col}")
                    st.rerun()
            else:
                if st.sidebar.button(f"Fill {col} with 'Unknown'", key=f"fix_sidebar_{col}"):
                    df_fixed, report = fixer.fill_missing_categorical(current_df, col, 'Unknown')
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
            if st.sidebar.button(f"Remove {col} outliers", key=f"outlier_sidebar_{col}"):
                df_fixed, report = fixer.remove_outliers(current_df, col, method='iqr')
                st.session_state.current_df = df_fixed
                st.session_state.fix_history.append(report)
                st.session_state.auto_reanalyze = True
                st.sidebar.success(f"✅ Removed {report['removed_rows']} outlier rows")
                st.rerun()
    
    # Date normalization
    date_issues = quality.get('date_format_issues', {})
    if date_issues:
        st.sidebar.subheader("📅 Normalize Dates")
        for col in date_issues.keys():
            if st.sidebar.button(f"Normalize {col}", key=f"date_sidebar_{col}"):
                df_fixed, report = fixer.normalize_dates(current_df, col)
                st.session_state.current_df = df_fixed
                st.session_state.fix_history.append(report)
                st.session_state.auto_reanalyze = True
                st.sidebar.success(f"✅ Normalized {col}")
                st.rerun()
    
    # Download + Reset
    if len(st.session_state.fix_history) > 0:
        st.sidebar.markdown("---")
        st.sidebar.subheader("💾 Download & Reset")
        csv = current_df.to_csv(index=False)
        st.sidebar.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"cleaned_{st.session_state.last_uploaded_file}",
            mime="text/csv"
        )
        
        if st.sidebar.button("🔄 Reset to Original"):
            st.session_state.current_df = st.session_state.original_df.copy()
            st.session_state.fix_history = []
            st.session_state.auto_reanalyze = True
            st.sidebar.success("✅ Reset to original data")
            st.rerun()

# === END HELPER FUNCTIONS ===

st.title("🐐 GOAT Data Analyst")
st.markdown("*Upload → Analyze → Fix → Download. Simple as that.*")

# === MODE SELECTOR ===
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
        st.session_state.show_simple_report = False
        st.rerun()

st.markdown("---")

# ============================================================================
# SINGLE FILE MODE
# ============================================================================
if st.session_state.analysis_mode == 'single':
    
    # === SAMPLE DATA BUTTONS (FIXED) ===
    st.write("**🎯 Try Sample Data:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔴 Messy Data", use_container_width=True, help="Duplicates, missing values, outliers", key="btn_messy"):
            try:
                sample_path = Path(__file__).parent / 'sample_data' / 'demo_messy.csv'
                if sample_path.exists():
                    df = pd.read_csv(sample_path)
                    st.session_state.original_df = df.copy()
                    st.session_state.current_df = df.copy()
                    st.session_state.last_uploaded_file = 'demo_messy.csv'
                    st.session_state.analysis_result = None
                    st.session_state.fix_history = []
                    st.session_state.show_simple_report = True
                    
                    with st.spinner("Analyzing messy data..."):
                        engine = AnalysisEngine()
                        result = engine.analyze(df)
                        st.session_state.analysis_result = result
                    
                    st.rerun()
                else:
                    st.error("Sample file not found: demo_messy.csv")
            except Exception as e:
                st.error(f"Error loading sample data: {str(e)}")
    
    with col2:
        if st.button("🟡 Medium Data", use_container_width=True, help="Some missing values", key="btn_medium"):
            try:
                sample_path = Path(__file__).parent / 'sample_data' / 'demo_medium.csv'
                if sample_path.exists():
                    df = pd.read_csv(sample_path)
                    st.session_state.original_df = df.copy()
                    st.session_state.current_df = df.copy()
                    st.session_state.last_uploaded_file = 'demo_medium.csv'
                    st.session_state.analysis_result = None
                    st.session_state.fix_history = []
                    st.session_state.show_simple_report = True
                    
                    with st.spinner("Analyzing medium data..."):
                        engine = AnalysisEngine()
                        result = engine.analyze(df)
                        st.session_state.analysis_result = result
                    
                    st.rerun()
                else:
                    st.error("Sample file not found: demo_medium.csv")
            except Exception as e:
                st.error(f"Error loading sample data: {str(e)}")
    
    with col3:
        if st.button("🟢 Clean Data", use_container_width=True, help="Perfect data", key="btn_clean"):
            try:
                sample_path = Path(__file__).parent / 'sample_data' / 'demo_clean.csv'
                if sample_path.exists():
                    df = pd.read_csv(sample_path)
                    st.session_state.original_df = df.copy()
                    st.session_state.current_df = df.copy()
                    st.session_state.last_uploaded_file = 'demo_clean.csv'
                    st.session_state.analysis_result = None
                    st.session_state.fix_history = []
                    st.session_state.show_simple_report = True
                    
                    with st.spinner("Analyzing clean data..."):
                        engine = AnalysisEngine()
                        result = engine.analyze(df)
                        st.session_state.analysis_result = result
                    
                    st.rerun()
                else:
                    st.error("Sample file not found: demo_clean.csv")
            except Exception as e:
                st.error(f"Error loading sample data: {str(e)}")
    
    st.markdown("---")
    
    # === FILE UPLOAD ===
    uploaded_file = st.file_uploader("Or upload your own CSV file", type=['csv'])
    
    if uploaded_file:
        # Handle new file upload
        if st.session_state.last_uploaded_file != uploaded_file.name:
            st.session_state.last_uploaded_file = uploaded_file.name
            st.session_state.original_df = None
            st.session_state.current_df = None
            st.session_state.analysis_result = None
            st.session_state.fix_history = []
            st.session_state.auto_reanalyze = False
            st.session_state.show_simple_report = False
        
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
        
        # Auto re-analyze after fix
        if st.session_state.auto_reanalyze:
            st.session_state.auto_reanalyze = False
            with st.spinner("Re-analyzing..."):
                engine = AnalysisEngine()
                result = engine.analyze(st.session_state.current_df)
                st.session_state.analysis_result = result
        
        # Analyze button
        if st.button("🔍 Run Analysis", type="primary"):
            with st.spinner("Analyzing..."):
                engine = AnalysisEngine()
                result = engine.analyze(st.session_state.current_df)
                st.session_state.analysis_result = result
                st.session_state.show_simple_report = True
    
    # === SHOW ANALYSIS RESULTS (for both uploaded and sample data) ===
    if st.session_state.analysis_result is not None:
        st.markdown("---")
        result = st.session_state.analysis_result
        quality = result.quality
        
        # === RENDER FIX PREVIEW MODAL (if active) ===
        if st.session_state.show_fix_preview and st.session_state.preview_data:
            render_fix_preview_modal(st.session_state.preview_data, quality)
        
        # === SIMPLE REPORT VIEW ===
        elif st.session_state.show_simple_report:
            st.header("📊 Analysis Results")
            
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
            
            # === SEVERITY CATEGORIZATION ===
            st.subheader("⚠️ Issues Found")
            
            critical_issues = []
            high_issues = []
            medium_issues = []
            total_rows = len(st.session_state.current_df)
            
            # Duplicates
            duplicates_count = quality.get('duplicates', 0)
            duplicates_pct = (duplicates_count / total_rows * 100) if total_rows > 0 else 0
            if duplicates_count > 0:
                if duplicates_pct > 15:
                    critical_issues.append(f"🔁 **{duplicates_count} duplicate rows** ({duplicates_pct:.1f}%)")
                elif duplicates_pct > 5:
                    high_issues.append(f"🔁 **{duplicates_count} duplicate rows** ({duplicates_pct:.1f}%)")
                else:
                    medium_issues.append(f"🔁 **{duplicates_count} duplicate rows** ({duplicates_pct:.1f}%)")
            
            # Missing values
            missing_by_col = quality.get('missing_by_column', {})
            for col, missing_count in missing_by_col.items():
                if missing_count > 0:
                    missing_pct = (missing_count / total_rows * 100) if total_rows > 0 else 0
                    if missing_pct > 10:
                        critical_issues.append(f"🩹 **{col}**: {missing_count} missing values ({missing_pct:.1f}%)")
                    elif missing_pct > 5:
                        high_issues.append(f"🩹 **{col}**: {missing_count} missing values ({missing_pct:.1f}%)")
                    else:
                        medium_issues.append(f"🩹 **{col}**: {missing_count} missing values ({missing_pct:.1f}%)")
            
            # Outliers
            outlier_cols = quality.get('outliers', {})
            for col, info in outlier_cols.items():
                high_issues.append(f"📊 **{col}**: {info.get('count', 0)} outliers detected")
            
            # Date issues
            date_issues = quality.get('date_format_issues', {})
            for col in date_issues.keys():
                medium_issues.append(f"📅 **{col}**: Date format inconsistencies")
            
            # Capitalization
            cap_issues = quality.get('capitalization_issues', {})
            for col in cap_issues.keys():
                medium_issues.append(f"🔤 **{col}**: Capitalization inconsistencies")
            
            # Display by severity - THREE COLUMNS
            col1, col2, col3 = st.columns(3)

            with col1:
                if critical_issues:
                    with st.expander(f"🔴 CRITICAL ({len(critical_issues)} issues)"):
                        for issue in critical_issues:
                            st.markdown(f"  {issue}")
                else:
                    st.success("✅ No critical issues")

            with col2:
                if high_issues:
                    with st.expander(f"🟡 HIGH ({len(high_issues)} issues)", expanded=True):
                        for issue in high_issues:
                            st.markdown(f"  {issue}")
                else:
                    st.success("✅ No high issues")

            with col3:
                if medium_issues:
                    with st.expander(f"🟢 MEDIUM ({len(medium_issues)} issues)"):
                        for issue in medium_issues:
                            st.markdown(f"  {issue}")
                else:
                    st.success("✅ No medium issues")

            
            if not critical_issues and not high_issues and not medium_issues:
                st.success("✅ No major issues found! Your data looks clean.")
            
            st.markdown("---")
            
            # === ACTION BUTTONS (TWO OPTIONS) ===
            st.subheader("🛠️ What do you want to do?")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                # QUICK FIX - Only safe auto-fixes (duplicates + dates)
                has_safe_fixes = quality.get('duplicates', 0) > 0 or len(quality.get('date_format_issues', {})) > 0
                if has_safe_fixes:
                    if st.button("⚡ Quick Fix", type="primary", use_container_width=True, 
                               help="Auto-fix duplicates and dates (safe operations only)"):
                        with st.spinner("Applying quick fixes..."):
                            df_working, fixes_applied = apply_quick_fix(quality, st.session_state.current_df)
                            
                            st.session_state.current_df = df_working
                            st.session_state.fix_history.extend(fixes_applied)
                            st.session_state.auto_reanalyze = True
                            st.success(f"✅ Applied {len(fixes_applied)} quick fixes!")
                            st.rerun()
                else:
                    st.button("⚡ Quick Fix", use_container_width=True, disabled=True, help="No safe auto-fixes available")
            
            with col2:
                # SMART FIX - Preview with user choices for missing values + outliers
                has_risky_issues = len(missing_by_col) > 0 or len(outlier_cols) > 0
                if has_risky_issues or has_safe_fixes:
                    if st.button("🧠 Smart Fix", use_container_width=True,
                               help="Review and choose how to fix each issue"):
                        preview_data = prepare_fix_preview(quality, st.session_state.current_df)
                        st.session_state.preview_data = preview_data
                        st.session_state.show_fix_preview = True
                        st.rerun()
                else:
                    st.button("🧠 Smart Fix", use_container_width=True, disabled=True)
            
            with col3:
                # VIEW FULL REPORT
                if st.button("📊 View Full Report", use_container_width=True):
                    st.session_state.show_simple_report = False
                    st.rerun()
            
            with col4:
                # DOWNLOAD REPORT
                st.download_button(
                    label="📥 Download Report",
                    data=st.session_state.analysis_result.report_html,
                    file_name=f"analysis_{st.session_state.last_uploaded_file.replace('.csv', '')}.html",
                    mime="text/html",
                    use_container_width=True
                )
            
            # === FIX SUMMARY ===
            if len(st.session_state.fix_history) > 0:
                st.markdown("---")
                st.success("### ✅ Fixes Applied Successfully!")
                
                if st.session_state.analysis_result:
                    new_score = st.session_state.analysis_result.quality.get('overall_score', 0)
                    st.metric("New Quality Score", f"{new_score:.0f}/100", delta=f"+{new_score - score:.0f}")
                
                st.write("**Changes made:**")
                for i, fix in enumerate(st.session_state.fix_history, 1):
                    operation = fix.get('operation', 'fix')
                    if operation == 'remove_duplicates':
                        st.write(f"{i}. Removed {fix.get('removed_rows', 0)} duplicate rows")
                    elif operation in ['fill_missing_numeric', 'fill_missing_categorical']:
                        st.write(f"{i}. Filled {fix.get('filled_count', 0)} missing values in '{fix.get('column', 'unknown')}'")
                    elif operation == 'remove_outliers':
                        st.write(f"{i}. Removed {fix.get('removed_rows', 0)} outlier rows from '{fix.get('column', 'unknown')}'")
                    elif operation == 'remove_rows':
                        st.write(f"{i}. Removed {fix.get('removed_rows', 0)} rows with missing values in '{fix.get('column', 'unknown')}'")
                    elif operation == 'normalize_dates':
                        st.write(f"{i}. Normalized date format in '{fix.get('column', 'unknown')}'")
                    else:
                        st.write(f"{i}. {operation}")
                
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
                
                if st.button("🔄 Reset to Original Data"):
                    st.session_state.current_df = st.session_state.original_df.copy()
                    st.session_state.fix_history = []
                    st.session_state.auto_reanalyze = True
                    st.rerun()
        
        # === FULL REPORT VIEW ===
        else:
            st.header("📊 Full Analysis Report")
            
            # Top action bar
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                if st.button("⬅️ Back to Simple View"):
                    st.session_state.show_simple_report = True
                    st.rerun()
            
            with col2:
                # QUICK FIX in full view
                has_safe_fixes = quality.get('duplicates', 0) > 0 or len(quality.get('date_format_issues', {})) > 0
                if has_safe_fixes:
                    if st.button("⚡ Quick Fix", type="primary", use_container_width=True, key="quick_fix_full"):
                        with st.spinner("Applying quick fixes..."):
                            df_working, fixes_applied = apply_quick_fix(quality, st.session_state.current_df)
                            
                            st.session_state.current_df = df_working
                            st.session_state.fix_history.extend(fixes_applied)
                            st.session_state.auto_reanalyze = True
                            st.success(f"✅ Applied {len(fixes_applied)} quick fixes!")
                            st.rerun()
            
            with col3:
                # SMART FIX in full view
                missing_by_col = quality.get('missing_by_column', {})
                outlier_cols = quality.get('outliers', {})
                has_risky_issues = len(missing_by_col) > 0 or len(outlier_cols) > 0
                
                if has_risky_issues or has_safe_fixes:
                    if st.button("🧠 Smart Fix", use_container_width=True, key="smart_fix_full"):
                        preview_data = prepare_fix_preview(quality, st.session_state.current_df)
                        st.session_state.preview_data = preview_data
                        st.session_state.show_fix_preview = True
                        st.rerun()
            
            with col4:
                # DOWNLOAD
                st.download_button(
                    label="📥 Download",
                    data=st.session_state.analysis_result.report_html,
                    file_name=f"analysis_{st.session_state.last_uploaded_file.replace('.csv', '')}.html",
                    mime="text/html",
                    use_container_width=True
                )
            
            # Show HTML report
            if st.session_state.analysis_result.report_html:
                st.components.v1.html(st.session_state.analysis_result.report_html, height=2000, scrolling=True)
            else:
                st.error("Report HTML is empty. Analysis may have failed.")
                st.write(f"Report generator status: {st.session_state.analysis_result}")

            # === SIDEBAR: INDIVIDUAL FIX CONTROLS (ONLY IN FULL VIEW) ===
            render_sidebar_fixes(quality, st.session_state.current_df)
    
    else:
        st.info("👆 Upload a CSV file or try example data to get started")

# ============================================================================
# BATCH MODE
# ============================================================================
elif st.session_state.analysis_mode == 'batch':
    st.subheader("📁 Multiple Files Analysis")
    st.info("Upload multiple CSV files to get a company-level data health report")
    st.warning("⚠️ Batch mode coming soon...")

st.markdown("---")
st.markdown("*Made with 💚 by GOAT Data Analyst*")
