
from datetime import datetime
import io
import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, EmailStr
from typing import Optional


from backend.core.engine import AnalysisEngine
from backend.auth.auth_manager import AuthManager
from middleware.rate_limiter import rate_limit_middleware
from middleware.file_validator import file_validator


# Initialize FastAPI
app = FastAPI(
    title="GOAT Data Analyst API",
    description="API for profiling CSV files and generating reports - Now with Authentication, Rate Limiting & File Validation",
    version="1.5.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "https://*.streamlit.app"],  # Restricted for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add rate limiting middleware
app.middleware("http")(rate_limit_middleware)


# Initialize services
auth_manager = AuthManager()



# ========================
# Authentication Models
# ========================


class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str



# ========================
# Authentication Dependency
# ========================


async def get_current_user(authorization: Optional[str] = Header(None)):
    """
    Dependency to verify JWT token and get current user
    Raises 401 if token is missing or invalid
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing. Please login."
        )
    
    # Extract token from "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication scheme. Use 'Bearer <token>'"
            )
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header format"
        )
    
    # Verify token
    result = auth_manager.verify_token(token)
    
    if not result.get("success"):
        raise HTTPException(
            status_code=401,
            detail=result.get("error", "Invalid or expired token")
        )
    
    return result["user"]



# ========================
# Public Endpoints (No Auth)
# ========================


@app.get("/")
async def root():
    return {
        "name": "GOAT Data Analyst API",
        "version": "1.5.0",
        "status": "ok",
        "authentication": "enabled",
        "rate_limiting": "enabled",
        "file_validation": "enabled",
        "endpoints": {
            "health": "/health",
            "signup": "/auth/signup",
            "login": "/auth/login",
            "analyze_html": "/analyze/html (requires auth)",
            "docs": "/docs",
        },
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.5.0",
        "auth": "enabled",
        "rate_limiting": "enabled",
        "file_validation": "enabled"
    }



# ========================
# Authentication Endpoints
# ========================


@app.post("/auth/signup", tags=["Authentication"])
async def signup(request: SignupRequest):
    """
    Register a new user
    
    Returns user data and session tokens
    """
    result = auth_manager.signup(request.email, request.password)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result



@app.post("/auth/login", tags=["Authentication"])
async def login(request: LoginRequest):
    """
    Authenticate existing user
    
    Returns user data and JWT tokens (access_token, refresh_token)
    """
    result = auth_manager.login(request.email, request.password)
    
    if not result.get("success"):
        raise HTTPException(status_code=401, detail=result.get("error"))
    
    return result



@app.post("/auth/logout", tags=["Authentication"])
async def logout(user: dict = Depends(get_current_user)):
    """
    Sign out current user
    
    Requires: Valid JWT token in Authorization header
    """
    return {"success": True, "message": "Logged out successfully"}



@app.get("/auth/me", tags=["Authentication"])
async def get_me(user: dict = Depends(get_current_user)):
    """
    Get current authenticated user info
    
    Requires: Valid JWT token in Authorization header
    """
    return {"success": True, "user": user}



# ========================
# Protected Analysis Endpoint
# ========================


@app.post("/analyze/html", tags=["Analysis"])
async def analyze_csv_html(
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user)  # AUTH REQUIRED HERE
):
    """
    Upload CSV and get full HTML report
    
    **PROTECTED**: Requires valid JWT token in Authorization header
    **RATE LIMITED**: 10 requests per minute for authenticated users
    **FILE VALIDATION**: Only CSV files, max 100MB
    """
    import traceback


    try:
        # Validate file with file_validator
        user_id = user.get("id") if user else None
        is_valid, error_msg = file_validator.validate_file(file.file, file.filename, user_id)
        
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)


        # Read file
        contents = await file.read()
        
        # Load CSV with encoding handling
        try:
            df = pd.read_csv(io.BytesIO(contents))
        except UnicodeDecodeError:
            # Try with latin-1 encoding
            try:
                df = pd.read_csv(io.BytesIO(contents), encoding='latin-1')
            except:
                raise HTTPException(
                    status_code=400, 
                    detail="File encoding issue. Please save as UTF-8 CSV."
                )
        
        # Validate CSV structure
        is_valid, error_msg = file_validator.validate_csv_structure(df)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)


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



# ========================
# Error Handlers
# ========================


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Return consistent error format"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

