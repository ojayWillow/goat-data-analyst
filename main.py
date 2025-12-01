from datetime import datetime
import io
import os

import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from backend.data_processing.profiler import DataProfiler
from backend.export_engine.ultimate_report import UltimateReportGenerator

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
            "docs": "/docs",
        },
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


def make_json_safe(obj):
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
        print("ERROR in /analyze:", repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/analyze/html")
async def analyze_csv_html(file: UploadFile = File(...)):
    import traceback

    try:
        # 1. Basic validation
        if not file.filename.lower().endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")

        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="CSV file is empty")

        # 2. Load CSV into DataFrame
        df = pd.read_csv(io.BytesIO(contents))

        # 3. Profile and quality report
        profiler = DataProfiler()
        profile = profiler.profile_dataframe(df)
        quality = profiler.get_quality_report()

        # 4. Domain detection: keyword + AI enhancement
        from backend.domain_detection.domain_detector import DomainDetector
        from backend.domain_detection.ai_domain_detector import AIDomainDetector
        from backend.analytics.simple_analytics import SimpleAnalytics
        from backend.analytics.ai_insights import AIInsightsEngine
        from backend.visualizations.universal_charts import UniversalChartGenerator
        from backend.export_engine.ultimate_report import UltimateReportGenerator

        # 4.1 Keyword-based detection
        keyword_detector = DomainDetector()
        keyword_result = keyword_detector.detect_domain(df)

        # 4.2 AI-enhanced detection (takes keyword_result as hint)
        ai_detector = AIDomainDetector()
        domain_result = ai_detector.enhance_detection(df, keyword_result)
        domain = domain_result.get("primary_domain") if domain_result else None

        # 5. Analytics
        analytics = SimpleAnalytics()
        analytics_summary = analytics.analyze_dataset(df)

        # 6. AI insights
        ai_engine = AIInsightsEngine()
        ai_results = ai_engine.generate_insights(df, domain, analytics_summary)
        ai_insights = ai_results.get("ai_insights", [])

        # 7. Build ultimate report
        generator = UltimateReportGenerator(profile, quality, df)

        # Inject AI-related context into generator
        generator.domain_result = domain_result          # AI + keyword combined
        generator.analytics_result = analytics_summary
        generator.ai_insights = ai_insights

        # 8. Charts
        chart_gen = UniversalChartGenerator(df, domain)
        generator.charts = chart_gen.generate_all_charts()

        # 9. Generate final HTML
        html = generator.generate_html()

        return HTMLResponse(content=html)

    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except pd.errors.ParserError as e:
        raise HTTPException(status_code=400, detail=f"CSV parsing error: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        print("ERROR in /analyze/html:", repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
