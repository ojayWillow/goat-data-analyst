import time
from datetime import datetime

import pandas as pd
import streamlit as st

from backend.data_processing.profiler import DataProfiler
from backend.export_engine.ultimate_report import UltimateReportGenerator


def load_csv(file) -> pd.DataFrame:
    return pd.read_csv(file)


def run_full_pipeline(df: pd.DataFrame):
    profiler = DataProfiler()
    profile = profiler.profile_dataframe(df)
    quality = profiler.get_quality_report()
    generator = UltimateReportGenerator(profile, quality, df)
    html_report = generator.generate_html()
    return profile, quality, html_report


def run_quick_pipeline(df: pd.DataFrame):
    # Quick mode: basic info only, no heavy report
    summary = {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "column_names": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
    }
    return summary


def main():
    st.set_page_config(
        page_title="GOAT Data Analyst",
        page_icon="🐐",
        layout="wide",
    )

    st.title("🐐 GOAT Data Analyst")
    st.write(
        "Upload a CSV file and let GOAT analyze it for you. "
        "For large files, this can take some time—especially in the free cloud environment."
    )

    st.markdown("---")

    st.subheader("1. Upload your CSV")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Supported format: .csv. For very large files, consider starting with Quick analysis.",
    )

    if uploaded_file is None:
        st.info("Upload a CSV file to begin.")
        return

    st.markdown("---")

    st.subheader("2. Choose analysis mode")

    mode = st.radio(
        "Select the analysis mode:",
        options=["Quick analysis (faster, lighter)", "Full analysis (slower, detailed report)"],
        index=0,
        help=(
            "Quick analysis: basic dataset info and structure.\n\n"
            "Full analysis: complete profiling and HTML report; may be slow for large files."
        ),
    )

    st.markdown("---")

    st.subheader("3. Run analysis")

    if mode.startswith("Quick"):
        analyze_button_label = "Run quick analysis"
    else:
        analyze_button_label = "Run full analysis"

    if st.button(analyze_button_label, type="primary"):
        start_time = time.time()

        try:
            with st.spinner("Reading CSV file..."):
                df = load_csv(uploaded_file)

            st.success(f"Loaded dataset with {len(df):,} rows and {len(df.columns):,} columns.")
            st.write("Here is a small sample of your data:")
            st.dataframe(df.head())

            if mode.startswith("Quick"):
                with st.spinner("Running quick analysis..."):
                    summary = run_quick_pipeline(df)
                elapsed = time.time() - start_time

                st.markdown("### Quick analysis results")
                st.json(
                    {
                        "rows": summary["rows"],
                        "columns": summary["columns"],
                        "column_names": summary["column_names"],
                        "dtypes": summary["dtypes"],
                        "analysis_mode": "quick",
                        "completed_at": datetime.now().isoformat(),
                        "elapsed_seconds": round(elapsed, 2),
                    }
                )

                st.info(
                    "Quick analysis finished. "
                    "Run a Full analysis if you want the complete HTML report and deep profiling "
                    "(it may take longer, especially for big files)."
                )

            else:
                st.warning(
                    "Full analysis can be slow on large files in the free cloud environment. "
                    "Please be patient; the app is working even if it feels stuck."
                )

                with st.spinner("Running full analysis and generating report..."):
                    profile, quality, html_report = run_full_pipeline(df)

                elapsed = time.time() - start_time

                st.success(
                    f"Full analysis completed in {round(elapsed, 2)} seconds "
                    f"({int(elapsed // 60)} min {int(elapsed % 60)} sec)."
                )

                st.markdown("### Dataset overview")
                st.write(f"Rows: {len(df):,}")
                st.write(f"Columns: {len(df.columns):,}")
                st.write("Columns:", list(df.columns))

                st.markdown("### Download full HTML report")
                st.download_button(
                    label="Download HTML report",
                    data=html_report.encode("utf-8"),
                    file_name=f"goat_data_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html",
                )

        except Exception as e:
            st.error(f"An error occurred during analysis: {str(e)}")


if __name__ == "__main__":
    main()
