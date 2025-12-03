import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.core.engine import AnalysisEngine
from backend.data_processing.data_fixer import DataFixer

st.set_page_config(page_title="GOAT Data Analyst", page_icon="🐐", layout="wide")

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

st.title("🐐 GOAT Data Analyst")
st.markdown("*The AI analyst that understands context, identifies pain points, and provides clear guidance*")

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file:
    # Check if this is a NEW file (different from last uploaded)
    if st.session_state.last_uploaded_file != uploaded_file.name:
        # New file detected - reset everything
        st.session_state.last_uploaded_file = uploaded_file.name
        st.session_state.original_df = None
        st.session_state.current_df = None
        st.session_state.analysis_result = None
        st.session_state.fix_history = []
        st.session_state.auto_reanalyze = False
    
    # Load data
    df = pd.read_csv(uploaded_file)

    # Store original if first load of THIS file
    if st.session_state.original_df is None:
        st.session_state.original_df = df.copy()
        st.session_state.current_df = df.copy()

    st.success(f"✅ Loaded {len(df)} rows × {len(df.columns)} columns")

    # Show current data state
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Current Rows", len(st.session_state.current_df))
    with col2:
        st.metric("Fixes Applied", len(st.session_state.fix_history))

    # Auto-reanalyze after fix
    if st.session_state.auto_reanalyze:
        st.session_state.auto_reanalyze = False
        with st.spinner("Re-analyzing after fix..."):
            engine = AnalysisEngine()
            result = engine.analyze(st.session_state.current_df)
            st.session_state.analysis_result = result

    # Analyze button
    if st.button("🚀 Run Analysis", type="primary"):
        with st.spinner("Analyzing your data..."):
            engine = AnalysisEngine()
            result = engine.analyze(st.session_state.current_df)
            st.session_state.analysis_result = result

    # Display report if available
    if st.session_state.analysis_result is not None:
        st.markdown("---")
        st.components.v1.html(st.session_state.analysis_result.report_html, height=2000, scrolling=True)

    # Fix actions sidebar (only show if analysis has run)
    if st.session_state.analysis_result is not None:
        st.sidebar.title("🔧 Quick Fixes")

        result = st.session_state.analysis_result
        quality = result.quality

        fixer = DataFixer()

        # Fix 1: Remove duplicates
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

        # Fix 2: Fill missing values
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

        # Fix 3: Remove outliers
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

        # Fix 4: Normalize dates
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

        # Fix 5: Fix capitalization
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

        # Download cleaned data
        if len(st.session_state.fix_history) > 0:
            st.sidebar.markdown("---")
            st.sidebar.subheader("💾 Download Cleaned Data")

            csv = st.session_state.current_df.to_csv(index=False)
            st.sidebar.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"cleaned_{uploaded_file.name}",
                mime="text/csv"
            )

            # Show fix history
            st.sidebar.markdown("**Fixes Applied:**")
            for i, fix in enumerate(st.session_state.fix_history, 1):
                st.sidebar.text(f"{i}. {fix.get('operation', 'fix')}")

            # Reset button
            if st.sidebar.button("↩️ Reset to Original"):
                st.session_state.current_df = st.session_state.original_df.copy()
                st.session_state.fix_history = []
                st.session_state.auto_reanalyze = True
                st.sidebar.success("Reset to original data")
                st.rerun()

else:
    st.info("👆 Upload a CSV file to get started")

# Footer
st.markdown("---")
st.markdown("*Made with 🐐 by GOAT Data Analyst*")
