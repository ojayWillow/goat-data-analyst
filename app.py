import os
os.environ.setdefault('GROQ_API_KEY', 'dummy')

import streamlit as st
import requests
from datetime import datetime
import time

st.set_page_config(page_title="GOAT Data Analyst", page_icon="🐐", layout="wide")

# Use local API during development
RAILWAY_API_URL = "http://127.0.0.1:8000"

st.title("🐐 GOAT Data Analyst")
st.markdown(
    "Turn raw CSV files into **AI-powered reports** with data quality, domain detection, "
    "analytics, visualizations, and insights."
)

# ===== LAYOUT: SIDEBAR + MAIN =====
with st.sidebar:
    st.header("Upload & Settings")

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    st.markdown("---")
    st.subheader("Or use a sample dataset")

    sample_choice = st.selectbox(
        "Quick start with:",
        [
            "None (only use uploaded file)",
            "Sample: E-commerce orders",
            "Sample: Customers 50K",
            "Sample: Spotify tracks",
        ],
        index=0,
    )

    mode = st.radio("Analysis mode:", ["Quick", "Full with AI"])

    run_button = st.button("Run Analysis", type="primary", use_container_width=True)

placeholder_info = st.empty()
metrics_container = st.container()
results_container = st.container()

if not uploaded_file and sample_choice == "None (only use uploaded file)":
    placeholder_info.info("Upload a CSV file in the sidebar or select a sample dataset to begin.")
    st.stop()


def get_file_to_send():
    if sample_choice != "None (only use uploaded file)":
        sample_map = {
            "Sample: E-commerce orders": "sample_data/sample_ecommerce.csv",
            "Sample: Customers 50K": "sample_data/20251127_084222_customers_50k.csv",
            "Sample: Spotify tracks": "sample_data/20251126_170320_spotify_data_clean.csv",
        }
        sample_path = sample_map.get(sample_choice)
        if sample_path and os.path.exists(sample_path):
            with open(sample_path, "rb") as f:
                data = f.read()
            filename = os.path.basename(sample_path)
            return data, filename
        else:
            st.error("Sample file not found on server.")
            st.stop()
    else:
        data = uploaded_file.getvalue()
        filename = uploaded_file.name
        return data, filename


if run_button:
    start_time = time.time()

    file_bytes, file_name = get_file_to_send()

    # ========== QUICK MODE ==========
    if mode == "Quick":
        try:
            with st.spinner("Analyzing (Quick mode)..."):
                response = requests.post(
                    f"{RAILWAY_API_URL}/analyze",
                    files={"file": (file_name, file_bytes, "text/csv")},
                    timeout=60,
                )

            elapsed = time.time() - start_time

            if response.status_code == 200:
                data = response.json()

                # ===== METRICS DASHBOARD =====
                with metrics_container:
                    st.subheader("Dataset Summary")
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Rows", f"{data.get('row_count', 0):,}")
                    col2.metric("Columns", str(data.get("column_count", 0)))

                    quality = data.get("quality", {})
                    quality_score = quality.get("quality_score", None)
                    if quality_score is not None:
                        score_val = round(float(quality_score), 1)
                        score_text = f"{score_val}/10"
                    else:
                        score_text = "N/A"

                    col3.metric("Quality Score", score_text)
                    col4.metric("Processing Time", f"{elapsed:.1f}s")

                # ===== RAW SUMMARY / PROFILE PREVIEW =====
                with results_container:
                    st.success("Quick analysis complete.")
                    st.write("Basic profile preview:")
                    profile = data.get("profile", {})
                    st.json(
                        {
                            "columns_profiled": list(profile.keys())[:10],
                            "quality_issues": quality.get(
                                "issues_summary",
                                "See full HTML report for detailed issues.",
                            ),
                        }
                    )
            else:
                st.error(f"API Error: {response.status_code}")
                st.write(response.text)

        except Exception as e:
            st.error(f"Error during quick analysis: {str(e)}")

    # ========== FULL WITH AI MODE ==========
    else:
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

                # ===== METRICS PLACEHOLDER =====
                with metrics_container:
                    st.subheader("Run Summary")
                    col1, col2 = st.columns(2)
                    col1.metric("Mode", "Full with AI")
                    col2.metric("Processing Time", f"{elapsed:.1f}s")

                # ===== ATTEMPT PDF GENERATION IMMEDIATELY =====
                pdf_bytes = None
                pdf_error = None
                try:
                    pdf_response = requests.post(
                        f"{RAILWAY_API_URL}/analyze/pdf",
                        files={"file": (file_name, file_bytes, "text/csv")},
                        timeout=240,
                    )
                    if pdf_response.status_code == 200:
                        pdf_bytes = pdf_response.content
                    else:
                        pdf_error = f"PDF API error: {pdf_response.status_code}"
                except Exception as e:
                    pdf_error = f"PDF generation failed: {str(e)}"

                # ===== DOWNLOAD BUTTONS + PREVIEW =====
                with results_container:
                    st.success("Full AI report ready.")

                    if pdf_bytes is not None:
                        col_html, col_pdf = st.columns(2)

                        col_html.download_button(
                            label="⬇️ Download HTML Report",
                            data=html_report.encode("utf-8"),
                            file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                            mime="text/html",
                            use_container_width=True,
                        )

                        col_pdf.download_button(
                            label="⬇️ Download PDF Report",
                            data=pdf_bytes,
                            file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                        )
                    else:
                        st.download_button(
                            label="⬇️ Download HTML Report",
                            data=html_report.encode("utf-8"),
                            file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                            mime="text/html",
                            use_container_width=True,
                        )
                        if pdf_error:
                            st.warning(pdf_error)

                    # Render HTML inline
                    st.markdown("### Report Preview")
                    st.components.v1.html(html_report, height=900, scrolling=True)

            else:
                st.error(f"API Error: {response.status_code}")
                st.write(response.text)

        except Exception as e:
            st.error(f"Error during full AI analysis: {str(e)}")
