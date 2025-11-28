"""
Simple Analytics Engine
Calculates basic statistics, distributions, and aggregations for datasets.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional

class SimpleAnalytics:
    """
    Performs basic statistical analysis on DataFrames.
    """
    
    def analyze_dataset(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Run full basic analysis on dataset."""
        if df is None or df.empty:
            return {}
            
        return {
            "summary": self._get_summary_stats(df),
            "numeric_analysis": self._analyze_numeric_columns(df),
            "categorical_analysis": self._analyze_categorical_columns(df)
        }
    
    def _get_summary_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get high-level dataset statistics."""
        return {
            "rows": len(df),
            "columns": len(df.columns),
            "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
            "missing_cells": int(df.isna().sum().sum()),
            "missing_percentage": round((df.isna().sum().sum() / (len(df) * len(df.columns))) * 100, 2),
            "duplicate_rows": int(df.duplicated().sum())
        }
        
    def _analyze_numeric_columns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate stats for numeric columns (mean, median, min, max)."""
        numeric_df = df.select_dtypes(include=[np.number])
        stats = {}
        
        for col in numeric_df.columns:
            # Skip if column is likely an ID (all unique or very high cardinality integers)
            if "id" in col.lower() and numeric_df[col].nunique() == len(df):
                continue
                
            series = numeric_df[col].dropna()
            if series.empty:
                continue
                
            stats[col] = {
                "mean": float(series.mean()),
                "median": float(series.median()),
                "min": float(series.min()),
                "max": float(series.max()),
                "std_dev": float(series.std()),
                "zeros": int((series == 0).sum()),
                "negatives": int((series < 0).sum())
            }
        return stats
        
    def _analyze_categorical_columns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze text/categorical columns (top values, cardinality)."""
        cat_df = df.select_dtypes(include=['object', 'category', 'string'])
        stats = {}
        
        for col in cat_df.columns:
            series = cat_df[col].dropna()
            if series.empty:
                continue
                
            # Get top 5 most frequent values
            value_counts = series.value_counts().head(5)
            top_values = {str(k): int(v) for k, v in value_counts.items()}
            
            stats[col] = {
                "unique_count": int(series.nunique()),
                "top_values": top_values,
                "most_common": str(series.mode()[0]) if not series.mode().empty else None
            }
        return stats

