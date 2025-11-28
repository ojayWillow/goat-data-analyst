"""
Insights Engine - Generate actionable business insights from data
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any


class InsightsEngine:
    """Generate business insights from dataset analysis."""
    
    def generate_insights(self, df: pd.DataFrame, domain: str = None) -> List[str]:
        """Generate key insights based on data patterns."""
        insights = []
        
        # Basic data quality insights
        insights.extend(self._quality_insights(df))
        
        # Numeric column insights
        insights.extend(self._numeric_insights(df))
        
        # Categorical insights
        insights.extend(self._categorical_insights(df))
        
        # Domain-specific insights
        if domain:
            insights.extend(self._domain_insights(df, domain))
        
        return insights[:10]  # Return top 10 insights
    
    def _quality_insights(self, df: pd.DataFrame) -> List[str]:
        """Insights about data quality."""
        insights = []
        
        missing_pct = (df.isna().sum().sum() / (len(df) * len(df.columns))) * 100
        if missing_pct > 20:
            insights.append(f"Dataset has {missing_pct:.1f}% missing data - consider data cleaning")
        elif missing_pct > 5:
            insights.append(f"Minor data quality issue: {missing_pct:.1f}% missing values")
        else:
            insights.append(f"Excellent data quality: Only {missing_pct:.1f}% missing data")
        
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            insights.append(f"Found {duplicates:,} duplicate rows - review for data integrity")
        
        return insights
    
    def _numeric_insights(self, df: pd.DataFrame) -> List[str]:
        """Insights from numeric columns."""
        insights = []
        numeric_df = df.select_dtypes(include=[np.number])
        
        for col in numeric_df.columns:
            if "id" in col.lower():
                continue
            
            series = numeric_df[col].dropna()
            if series.empty:
                continue
            
            # Outlier detection
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((series < Q1 - 1.5 * IQR) | (series > Q3 + 1.5 * IQR)).sum()
            
            if outliers > 0:
                outlier_pct = (outliers / len(series)) * 100
                if outlier_pct > 5:
                    insights.append(f"Column '{col}' has {outlier_pct:.1f}% outliers - investigate anomalies")
        
        return insights[:2]
    
    def _categorical_insights(self, df: pd.DataFrame) -> List[str]:
        """Insights from categorical columns."""
        insights = []
        cat_df = df.select_dtypes(include=['object', 'category', 'string'])
        
        for col in cat_df.columns:
            series = cat_df[col].dropna()
            if series.empty:
                continue
            
            unique_count = series.nunique()
            most_common_pct = (series.value_counts().iloc[0] / len(series)) * 100
            
            if most_common_pct > 80:
                insights.append(f"Column '{col}' is heavily skewed - {most_common_pct:.0f}% is single value")
            
            if unique_count > 1000:
                insights.append(f"Column '{col}' has {unique_count:,} unique values - consider grouping")
        
        return insights[:2]
    
    def _domain_insights(self, df: pd.DataFrame, domain: str) -> List[str]:
        """Domain-specific insights."""
        insights = []
        
        if domain.lower() == 'e-commerce':
            if 'Product_ID' in df.columns or 'product_id' in df.columns:
                product_col = 'Product_ID' if 'Product_ID' in df.columns else 'product_id'
                unique_products = df[product_col].nunique()
                insights.append(f"E-commerce: Catalog has {unique_products:,} unique products")
            
            if 'User_ID' in df.columns or 'user_id' in df.columns:
                user_col = 'User_ID' if 'User_ID' in df.columns else 'user_id'
                unique_users = df[user_col].nunique()
                insights.append(f"E-commerce: {unique_users:,} unique customers in dataset")
        
        elif domain.lower() == 'finance':
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                insights.append(f"Finance: {len(numeric_cols)} numeric metrics available for analysis")
        
        return insights
