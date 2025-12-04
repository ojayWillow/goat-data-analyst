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

# DAY 15/16: MODE + BATCH STATE
if 'analysis_mode' not in st.session_state:
    st.session_state.analysis_mode = 'single'  # 'single' or 'batch'
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
# SINGLE FILE MODE (existing)
# ============================================================================
if st.session_state.analysis_mode == 'single':
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

# ============================================================================
# BATCH MODE (Day 15 + 16)
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
            with st.spinner(f"Analyzing {len(uploaded_files)} files..."):
                # Save files to temp directory
                temp_dir = tempfile.mkdtemp()
                file_paths = []
                
                for uploaded in uploaded_files:
                    file_path = os.path.join(temp_dir, uploaded.name)
                    with open(file_path, 'wb') as f:
                        f.write(uploaded.getvalue())
                    file_paths.append(file_path)
                
                # Run batch analysis
                batch = BatchEngine()
                st.session_state.batch_results = batch.analyze_files(file_paths)
                
                # Cleanup temp files
                import shutil
                shutil.rmtree(temp_dir)
        
        # Display batch results
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

            # === DAY 16: DOWNLOAD COMPANY HEALTH REPORT ===
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
                    emoji = severity_emoji.get(issue['severity'], "⚪")
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
            st.subheader("📄 All Files")
            
            for file_result in results['files']:
                quality_score = file_result.quality.get('overall_score', 0)
                
                # Color code by quality
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
                st.subheader(f"📊 Detailed Report: {st.session_state.selected_file.filename}")
                
                if st.button("⬅️ Back to Dashboard"):
                    st.session_state.selected_file = None
                    st.rerun()
                
                st.components.v1.html(
                    st.session_state.selected_file.report_html, 
                    height=2000, 
                    scrolling=True
                )
    
    else:
        st.info("👆 Upload multiple CSV files to analyze")

# Footer
st.markdown("---")
st.markdown("*Made with 🐐 by GOAT Data Analyst*")
