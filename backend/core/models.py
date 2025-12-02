"""
Data models for GOAT Data Analyst

AnalysisResult: The standard output format for all analysis
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
import pandas as pd


@dataclass
class AnalysisResult:
    """
    Standard output container for all analysis results
    
    This is what AnalysisEngine returns. Every UI/API consumes this format.
    
    Attributes:
        dataframe: Original input data
        profile: Basic stats (rows, columns, types, memory)
        domain: Domain detection (sales, finance, etc.)
        quality: Quality metrics (missing, dupes, outliers)
        analytics: Statistical analysis results
        ai_insights: LLM-generated insights
        charts: Generated chart objects
        narrative: Human-like communication sections
        report_html: Final assembled HTML report
        execution_time_seconds: How long analysis took
        errors: Fatal errors (if any)
        warnings: Non-fatal warnings
    """
    
    dataframe: pd.DataFrame
    profile: Dict[str, Any] = field(default_factory=dict)
    domain: Dict[str, Any] = field(default_factory=dict)
    quality: Dict[str, Any] = field(default_factory=dict)
    analytics: Dict[str, Any] = field(default_factory=dict)
    ai_insights: Dict[str, Any] = field(default_factory=dict)
    charts: Dict[str, Any] = field(default_factory=dict)
    narrative: str = ""
    report_html: str = ""
    execution_time_seconds: float = 0.0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
