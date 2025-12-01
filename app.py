import os
os.environ.setdefault('GROQ_API_KEY', 'dummy')

import streamlit as st
import requests
from datetime import datetime
import time

st.set_page_config(page_title="GOAT Data Analyst", page_icon="🐐", layout="wide")

RAILWAY_API_URL = "http://localhost:8000"

st.title("🐐 GOAT Data Analyst")
st.markdown(
    "Turn raw CSV files into **AI-powered reports** with data quality, domain detection, "
    "analytics, visualizations, and insights."
)

# ===== SIDEBAR =====
with st.sidebar:
    st.header("Upload CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    run_button = st.button("Run Analysis", type="primary", use_container_width=True)

placeholder_info = st.empty()
metrics_container = st.container()
results_container = st.container()

if not uploaded_file:
    placeholder_info.info("Upload a CSV file in the sidebar to begin.")
    st.stop()

if run_button:
    start_time = time.time()
    file_bytes = uploaded_file.getvalue()
    file_name = uploaded_file.name

    try:
        with st.spinner("Generating full report with AI..."):
            response = requests.post(
                f"{RAILWAY_API_URL}/analyze/html",
                files={"file": (file_name, file_bytes, "text/csv")},
                timeout=180,
            )

        elapsed = time.time() - start_time

        if response.status_code == 200:
            html_report = response.text

            # ===== METRICS =====
            with metrics_container:
                st.subheader("Run Summary")
                col1, col2 = st.columns(2)
                col1.metric("Mode", "Full with AI")
                col2.metric("Processing Time", f"{elapsed:.1f}s")

            # ===== DOWNLOAD + PREVIEW =====
            with results_container:
                st.success("Full AI report ready.")

                st.download_button(
                    label="⬇️ Download HTML Report",
                    data=html_report.encode("utf-8"),
                    file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html",
                    use_container_width=True,
                )

                # Render HTML inline
                st.markdown("### Report Preview")
                st.components.v1.html(html_report, height=900, scrolling=True)

        else:
            st.error(f"API Error: {response.status_code}")
            st.write(response.text)

    except Exception as e:
        st.error(f"Error during full AI analysis: {str(e)}")
