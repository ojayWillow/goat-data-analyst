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
        "Fast, powered by cloud backend."
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
        options=["Quick analysis (faster, lighter)", "Full analysis (slower, detailed report)"],
        index=0,
        help=(
            "Quick analysis: basic dataset info and structure.\n\n"
            "Full analysis: complete profiling and HTML report."
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
                    st.json(
                        {
                            "rows": data.get("row_count"),
                            "columns": data.get("column_count"),
                            "profile": data.get("profile"),
                            "quality": data.get("quality"),
                        }
                    )
                else:
                    st.error(
                        f"Error from API: {response.status_code} - {response.text}"
                    )

            else:
                with st.spinner("Running full analysis and generating report..."):
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
                        f"Full analysis completed in {round(elapsed, 2)} seconds "
                        f"({int(elapsed // 60)} min {int(elapsed % 60)} sec)."
                    )
                    st.markdown("### Download full HTML report")
                    st.download_button(
                        label="Download HTML report",
                        data=html_report.encode("utf-8"),
                        file_name=f"goat_data_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                        mime="text/html",
                    )
                    st.markdown("### Report preview")
                    st.components.v1.html(html_report, height=600, scrolling=True)
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
