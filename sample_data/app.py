import io
from datetime import datetime
import pandas as pd
import streamlit as st

from backend.data_processing.profiler import DataProfiler
from backend.export_engine.ultimate_report import UltimateReportGenerator

def load_uploaded_csv(uploaded_file) -> pd.DataFrame:
    uploaded_file.seek(0)
    return pd.read_csv(uploaded_file)

def main():
    st.set_page_config(page_title="Data Quality Dashboard", layout="wide")
    st.title("Data Quality & Profiling Dashboard")
    st.write("Upload a CSV file to generate a detailed report.")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if not uploaded_file:
        st.info("Awaiting CSV file upload.")
        return

    st.write(f"**File name:** {uploaded_file.name}")
    st.write(f"**Size:** {uploaded_file.size / 1024:.1f} KB")

    if st.button("Generate Report"):
        with st.spinner("Loading data..."):
            try:
                df = load_uploaded_csv(uploaded_file)
            except Exception as e:
                st.error(f"Failed to read CSV: {e}")
                return
        st.success(f"Loaded {len(df):,} rows and {len(df.columns)} columns.")

        with st.spinner("Profiling data and computing quality metrics..."):
            profiler = DataProfiler()
            profile = profiler.profile_dataframe(df)
            quality = profiler.get_quality_report()
        st.success(f"Profiling complete. Quality score: {quality.get('score', 'N/A')}/100")

        with st.spinner("Generating HTML report..."):
            generator = UltimateReportGenerator(profile, quality, df)
            html = generator.generate_html()

        st.success("Report generated successfully.")

        # Download button for HTML
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.download_button("Download HTML Report", html, file_name=f"DATA_REPORT_{timestamp}.html", mime="text/html")

        # Optional inline preview
        st.markdown("### Report Preview")
        st.components.v1.html(html, height=800, scrolling=True)

if __name__ == "__main__":
    main()
