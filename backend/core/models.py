"""
Core data models for GOAT Data Analyst
Contains the AnalysisResult dataclass that standardizes all analysis outputs
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import pandas as pd


@dataclass
class AnalysisResult:
    """
    Standardized container for all analysis outputs
    
    The "one truth" object that flows through the entire system:
    CSV → AnalysisEngine.analyze() → AnalysisResult → UI/API
    """
    
    # Core data
    dataframe: pd.DataFrame
    
    # Profile: Basic statistics about the dataset
    profile: Dict[str, Any] = field(default_factory=dict)
    # Example: {"rows": 1000, "columns": 5, "memory_mb": 0.5}
    
    # Domain: What kind of data is this?
    domain: Dict[str, Any] = field(default_factory=dict)
    # Example: {"type": "sales", "confidence": 0.85, "indicators": ["transaction_id", "amount"]}
    
    # Quality: Data health check
    quality: Dict[str, Any] = field(default_factory=dict)
    # Example: {"missing_pct": 12.5, "duplicates": 47, "outliers": 3}
    
    # Analytics: Statistical insights
    analytics: Dict[str, Any] = field(default_factory=dict)
    # Example: {"correlations": {...}, "distributions": {...}}
    
    # AI Insights: LLM-generated observations
    ai_insights: Dict[str, Any] = field(default_factory=dict)
    # Example: {"summary": "Revenue trending down...", "anomalies": [...]}
    
    # Charts: Visualization data (JSON or base64)
    charts: Dict[str, Any] = field(default_factory=dict)
    # Example: {"revenue_trend": "<plotly_json>", "distribution": "<plotly_json>"}
    
    # Report: Final HTML output
    report_html: str = ""
    
    # Metadata
    execution_time_seconds: float = 0.0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate required fields"""
        if self.dataframe is None or self.dataframe.empty:
            raise ValueError("AnalysisResult requires a non-empty DataFrame")
    
    def has_errors(self) -> bool:
        """Check if any errors occurred during analysis"""
        return len(self.errors) > 0
    
    def summary(self) -> Dict[str, Any]:
        """Quick summary of the analysis"""
        return {
            "rows": len(self.dataframe),
            "columns": len(self.dataframe.columns),
            "domain_type": self.domain.get("type", "unknown"),
            "quality_score": self.quality.get("overall_score", 0),
            "charts_generated": len(self.charts),
            "has_errors": self.has_errors(),
            "execution_time": self.execution_time_seconds
        }
