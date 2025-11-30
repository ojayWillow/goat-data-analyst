from datetime import datetime
import io
import os

import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from backend.data_processing.profiler import DataProfiler
from backend.export_engine.ultimate_report import UltimateReportGenerator
from backend.analytics.visualizations import DataVisualizer

import pdfkit

app = FastAPI(
    title="GOAT Data Analyst API",
    description="API for profiling CSV files and generating reports",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PDF configuration - wkhtmltopdf path (installed earlier)
pdfkit_config = pdfkit.configuration(
    wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
)


@app.get("/")
async def root():
    return {
        "name": "GOAT Data Analyst API",
        "version": "1.0.0",
        "status": "ok",
        "endpoints": {
            "health": "/health",
            "analyze_json": "/analyze",
            "analyze_html": "/analyze/html",
            "analyze_pdf": "/analyze/pdf",
            "docs": "/docs",
        },
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
    }


def make_json_safe(obj):
    """
    Recursively convert pandas / numpy / complex objects into JSON-serializable
    Python types (dict, list, int, float, str, bool, None).
    """
    import numpy as np
    import pandas as pd

    if isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient="list")
    if isinstance(obj, pd.Series):
        return obj.to_list()
    if isinstance(obj, pd.Index):
        return obj.tolist()
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if isinstance(obj, (np.ndarray,)):
        return obj.tolist()
    if isinstance(obj, dict):
        return {str(k): make_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [make_json_safe(v) for v in obj]
    return obj


@app.post("/analyze")
async def analyze_csv(file: UploadFile = File(...)):
    """
    Analyze uploaded CSV and return a JSON-safe profile + quality report.
    """
    import traceback

    try:
        if not file.filename.lower().endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")

        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="CSV file is empty")

        df = pd.read_csv(io.BytesIO(contents))

        profiler = DataProfiler()
        profile = profiler.profile_dataframe(df)
        quality = profiler.get_quality_report()

        safe_profile = make_json_safe(profile)
        safe_quality = make_json_safe(quality)

        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "row_count": int(len(df)),
            "column_count": int(len(df.columns)),
            "profile": safe_profile,
            "quality": safe_quality,
        }

    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except pd.errors.ParserError as e:
        raise HTTPException(status_code=400, detail=f"CSV parsing error: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        print("❌ ERROR in /analyze:", repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/analyze/html")
async def analyze_csv_html(file: UploadFile = File(...)):
    """
    Analyze uploaded CSV and return the full HTML report with AI insights.
    """
    import traceback

    try:
        if not file.filename.lower().endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")

        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="CSV file is empty")

        df = pd.read_csv(io.BytesIO(contents))

        profiler = DataProfiler()
        profile = profiler.profile_dataframe(df)
        quality = profiler.get_quality_report()

        # Domain detection + AI insights
        from backend.domain_detection.domain_detector import DomainDetector
        from backend.analytics.simple_analytics import SimpleAnalytics
        from backend.analytics.ai_insights import AIInsightsEngine

        detector = DomainDetector()
        domain_result = detector.detect_domain(df)
        domain = domain_result.get("primary_domain") if domain_result else None

        analytics = SimpleAnalytics()
        analytics_summary = analytics.analyze_dataset(df)

        ai_engine = AIInsightsEngine()
        ai_results = ai_engine.generate_insights(df, domain, analytics_summary)

        generator = UltimateReportGenerator(profile, quality, df)
        generator.domain = domain
        generator.analytics_summary = analytics_summary
        generator.ai_insights = ai_results["ai_insights"]

        # Charts
        visualizer = DataVisualizer(df)
        generator.charts = visualizer.generate_all_charts()

        html = generator.generate_html()

        return HTMLResponse(content=html)

    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except pd.errors.ParserError as e:
        raise HTTPException(status_code=400, detail=f"CSV parsing error: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        print("❌ ERROR in /analyze/html:", repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


@app.post("/analyze/pdf")
async def analyze_csv_pdf(file: UploadFile = File(...)):
    """
    Analyze uploaded CSV and return the full PDF report with AI insights.
    Implementation: reuse HTML generation, then convert to PDF with pdfkit.
    """
    import traceback

    try:
        if not file.filename.lower().endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")

        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="CSV file is empty")

        df = pd.read_csv(io.BytesIO(contents))

        profiler = DataProfiler()
        profile = profiler.profile_dataframe(df)
        quality = profiler.get_quality_report()

        # Domain detection + AI insights
        from backend.domain_detection.domain_detector import DomainDetector
        from backend.analytics.simple_analytics import SimpleAnalytics
        from backend.analytics.ai_insights import AIInsightsEngine

        detector = DomainDetector()
        domain_result = detector.detect_domain(df)
        domain = domain_result.get("primary_domain") if domain_result else None

        analytics = SimpleAnalytics()
        analytics_summary = analytics.analyze_dataset(df)

        ai_engine = AIInsightsEngine()
        ai_results = ai_engine.generate_insights(df, domain, analytics_summary)

        generator = UltimateReportGenerator(profile, quality, df)
        generator.domain = domain
        generator.analytics_summary = analytics_summary
        generator.ai_insights = ai_results["ai_insights"]

        # Charts
        visualizer = DataVisualizer(df)
        generator.charts = visualizer.generate_all_charts()

        html = generator.generate_html()

        # HTML -> PDF
        pdf_bytes = pdfkit.from_string(html, False, configuration=pdfkit_config)

        filename_root = os.path.splitext(file.filename)[0] or "report"

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename_root}_report.pdf"'
            },
        )

    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except pd.errors.ParserError as e:
        raise HTTPException(status_code=400, detail=f"CSV parsing error: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        print("❌ ERROR in /analyze/pdf:", repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
