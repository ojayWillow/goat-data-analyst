import os
os.environ.setdefault('GROQ_API_KEY', 'dummy')

import streamlit as st
import requests
from datetime import datetime
import time

st.set_page_config(page_title="GOAT Data Analyst", page_icon="🐐", layout="wide")

st.title("🐐 GOAT Data Analyst")
st.write("Upload a CSV file for AI-powered analysis.")

RAILWAY_API_URL = "https://goat-data-analyst-production.up.railway.app"

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is None:
    st.info("Upload a CSV file to begin.")
    st.stop()

mode = st.radio("Analysis mode:", ["Quick", "Full with AI"])

if st.button("Run Analysis", type="primary"):
    start_time = time.time()
    
    try:
        if mode == "Quick":
            with st.spinner("Analyzing..."):
                response = requests.post(
                    f"{RAILWAY_API_URL}/analyze",
                    files={"file": uploaded_file},
                    timeout=60
                )
            
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                st.success(f"Done in {elapsed:.1f}s")
                st.json({
                    "rows": data.get("row_count"),
                    "columns": data.get("column_count"),
                })
            else:
                st.error(f"API Error: {response.status_code}")
        
        else:
            with st.spinner("Generating full report with AI..."):
                response = requests.post(
                    f"{RAILWAY_API_URL}/analyze/html",
                    files={"file": uploaded_file},
                    timeout=120
                )
            
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                html_report = response.text
                st.success(f"Done in {elapsed:.1f}s")
                st.download_button(
                    label="Download Report",
                    data=html_report.encode("utf-8"),
                    file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html"
                )
                st.components.v1.html(html_report, height=800, scrolling=True)
            else:
                st.error(f"API Error: {response.status_code}")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
