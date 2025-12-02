"""
Streamlit Frontend for GOAT Data Analyst - Day 2 Refactor

Purpose:
- Let users upload a CSV
- Call AnalysisEngine (the ONE brain)
- Display the HTML report

No duplicate logic. Clean and simple.
"""

import streamlit as st
import pandas as pd
from backend.core.engine import AnalysisEngine


st.set_page_config(page_title="GOAT Data Analyst", layout="wide")


def main():
    st.title("🐐 GOAT Data Analyst")
    st.write("Upload a CSV file and get an instant analyst-grade report.")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Loaded {len(df):,} rows × {len(df.columns)} columns")

            if st.button("🚀 Run Analysis", type="primary"):
                with st.spinner("Analyzing data..."):
                    # The ONE brain does everything
                    engine = AnalysisEngine()
                    result = engine.analyze(df)
                    
                    # Show any errors or warnings
                    if result.errors:
                        st.error("❌ Errors occurred:")
                        for error in result.errors:
                            st.error(f"  • {error}")
                    
                    if result.warnings:
                        with st.expander("⚠️ Warnings"):
                            for warning in result.warnings:
                                st.warning(warning)
                
                # Display the report
                st.success(f"✅ Analysis complete in {result.execution_time_seconds:.2f}s")
                st.components.v1.html(result.report_html, height=5000, scrolling=True)

        except Exception as e:
            st.error(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
