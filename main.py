from datetime import datetime
import io
import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from backend.core.engine import AnalysisEngine

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

@app.post("/analyze/html")
async def analyze_csv_html(file: UploadFile = File(...)):
    """Upload CSV and get full HTML report"""
    import traceback

    try:
        # Validate
        if not file.filename.lower().endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")

        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="CSV file is empty")

        # Load CSV
        df = pd.read_csv(io.BytesIO(contents))

        # THE ONE BRAIN does everything
        engine = AnalysisEngine()
        result = engine.analyze(df)

        # Return HTML report
        return HTMLResponse(content=result.report_html)

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
