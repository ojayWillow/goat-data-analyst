import os
os.environ.setdefault('GROQ_API_KEY', 'dummy')

import time
from datetime import datetime

import requests
import streamlit as st

# Railway API URL
RAILWAY_API_URL = "https://goat-data-analyst-production.up.railway.app"



def main():
    st.set_page_config(
        page_title="GOAT Data Analyst",
        page_icon="🐐",
        layout="wide",
    )

    st.title("🐐 GOAT Data Analyst")
    st.write(
        "Upload a CSV file and let GOAT analyze it for you. "
        "AI-powered insights + cloud backend."
    )

    st.markdown("---")

    st.subheader("1. Upload your CSV")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Supported format: .csv",
    )

    if uploaded_file is None:
        st.info("Upload a CSV file to begin.")
        return

    st.markdown("---")

    st.subheader("2. Choose analysis mode")

    mode = st.radio(
        "Select the analysis mode:",
        options=["Quick analysis (faster, lighter)", "Full analysis (slower, detailed report + AI insights)"],
        index=0,
        help=(
            "Quick analysis: basic dataset info and structure.\n\n"
            "Full analysis: complete profiling, HTML report, and AI-powered insights."
        ),
    )

    st.markdown("---")

    st.subheader("3. Run analysis")

    if mode.startswith("Quick"):
        analyze_button_label = "Run quick analysis"
    else:
        analyze_button_label = "Run full analysis with AI"

    if st.button(analyze_button_label, type="primary"):
        start_time = time.time()

        try:
            if mode.startswith("Quick"):
                with st.spinner("Running quick analysis..."):
                    files = {"file": uploaded_file}
                    response = requests.post(
                        f"{RAILWAY_API_URL}/analyze",
                        files=files,
                        timeout=60,
                    )

                elapsed = time.time() - start_time

                if response.status_code == 200:
                    data = response.json()
                    st.success(
                        f"Quick analysis completed in {round(elapsed, 2)} seconds."
                    )
                    st.markdown("### Results")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Rows", f"{data.get('row_count', 0):,}")
                    with col2:
                        st.metric("Columns", data.get('column_count', 0))
                    with col3:
                        quality_score = data.get('quality', {}).get('overall_score', 0)
                        st.metric("Quality Score", f"{quality_score:.1f}/10")
                    
                    st.json(
                        {
                            "profile": data.get("profile"),
                            "quality": data.get("quality"),
                        }
                    )
                else:
                    st.error(
                        f"Error from API: {response.status_code} - {response.text}"
                    )

            else:
                with st.spinner("🤖 Running full analysis with AI insights..."):
                    files = {"file": uploaded_file}
                    response = requests.post(
                        f"{RAILWAY_API_URL}/analyze/html",
                        files=files,
                        timeout=120,
                    )

                elapsed = time.time() - start_time

                if response.status_code == 200:
                    html_report = response.text
                    st.success(
                        f"✅ Full analysis completed in {round(elapsed, 2)} seconds "
                        f"({int(elapsed // 60)} min {int(elapsed % 60)} sec)."
                    )
                    
                    # Display AI insights hint
                    st.info("🤖 **AI Insights included in the report!** Look for the 'AI-Powered Insights' section in the preview below.")
                    
                    st.markdown("### Download full HTML report")
                    st.download_button(
                        label="📥 Download HTML report",
                        data=html_report.encode("utf-8"),
                        file_name=f"goat_data_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                        mime="text/html",
                    )
                    
                    st.markdown("### Report preview")
                    st.components.v1.html(html_report, height=800, scrolling=True)
                else:
                    st.error(
                        f"Error from API: {response.status_code} - {response.text}"
                    )

        except requests.exceptions.Timeout:
            st.error("Request timed out. The analysis took too long.")
        except requests.exceptions.ConnectionError:
            st.error(
                f"Could not connect to API at {RAILWAY_API_URL}. Is the backend running?"
            )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
