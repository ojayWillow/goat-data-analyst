"""
Streamlit Frontend for GOAT Data Analyst

Purpose:
- Let users upload a CSV
- Call the backend analysis pipeline directly in-process
- Generate and display the full HTML report (including charts)

Connections:
- Uses DataProfiler for profiling + quality score
- Uses SimpleAnalytics for basic stats
- Uses UniversalChartGenerator for charts
- Uses ReportAssembler to build the final HTML report
"""

import streamlit as st
import pandas as pd

from backend.data_processing.profiler import DataProfiler
from backend.analytics.simple_analytics import SimpleAnalytics
from backend.visualizations.universal_charts import UniversalChartGenerator
from backend.reports.assembler import ReportAssembler


st.set_page_config(page_title="GOAT Data Analyst", layout="wide")


def run_analysis(df: pd.DataFrame) -> str:
    """Run the full in-process analysis pipeline and return HTML report."""
    # 1) Profile
    profiler = DataProfiler()
    profile = profiler.profile_dataframe(df)

    # 2) Basic analytics
    analytics_engine = SimpleAnalytics()
    analytics_result = analytics_engine.analyze_dataset(df)

    # 3) Domain placeholder (for now)
    domain_info = {
        "domain": "unknown",
        "confidence": 0.0,
        "reason": "Domain detection not wired in Streamlit yet.",
    }

    # 4) Charts
    chart_gen = UniversalChartGenerator(df)
    raw_charts = chart_gen.generate_all_universal_charts()
    charts_data = {
        "time_series": raw_charts.get("time_series"),
        "distribution": raw_charts.get("distribution"),
        "correlation": raw_charts.get("correlation"),
        "top_n": raw_charts.get("category"),  # category -> top_n
    }

    # 5) Assemble HTML report
    assembler = ReportAssembler()
    html_report = assembler.generate_report(
        profile=profile,
        domain_data=domain_info,
        insights_data=None,   # AI optional
        charts_data=charts_data,
        config={
            "include_header": True,
            "include_quality": True,
            "include_domain": True,
            "include_ai": False,
            "include_charts": True,
            "include_footer": True,
        },
    )
    return html_report


def main():
    st.title("GOAT Data Analyst")
    st.write("Upload a CSV file and get an instant analyst-grade report.")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"Loaded {len(df)} rows, {len(df.columns)} columns")

            if st.button("Run Analysis"):
                with st.spinner("Analyzing data..."):
                    html_report = run_analysis(df)

                st.success("Analysis complete. Full report below:")
                st.components.v1.html(html_report, height=900, scrolling=True)

        except Exception as e:
            st.error(f"Error reading or analyzing file: {e}")


if __name__ == "__main__":
    main()
