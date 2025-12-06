"""
Insights Engine - Generate structured business insights from data
Returns facts (dict) instead of strings, ready for LLM narrative wrapping.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional


class InsightsEngine:
    """Generate structured business insights from dataset analysis."""

    def generate_insights(self, df: pd.DataFrame, domain: str = None) -> Dict[str, Any]:
        """
        Generate structured insights as facts (not strings).
        Returns a dict that can be passed to a narrator for prose conversion.
        
        Example return:
        {
            "quality": {"missing_pct": 12.5, "duplicates": 0, "rows": 1000},
            "concentration": [{"column": "customer", "top_pct": 65, "top_n": 10}],
            "outliers": [{"column": "price", "count": 45, "pct": 3.2}],
            "domain": "ecommerce",
            "key_metrics": [{"name": "revenue", "avg": 150.5, "total": 150500}]
        }
        """
        facts: Dict[str, Any] = {}

        # 1) Quality facts
        facts["quality"] = self._quality_facts(df)

        # 2) Concentration facts (top customers, products, etc)
        facts["concentration"] = self._concentration_facts(df)

        # 3) Outlier facts
        facts["outliers"] = self._outlier_facts(df)

        # 4) Numeric metrics facts
        facts["metrics"] = self._metric_facts(df)

        # 5) Domain-specific facts
        facts["domain"] = domain.lower() if domain else "generic"
        if domain:
            facts["domain_facts"] = self._domain_facts(df, domain)

        return facts

    # -------------- Fact generators -------------- #

    def _quality_facts(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Return data quality facts."""
        if df.empty:
            return {"rows": 0, "columns": 0, "missing_pct": 100, "duplicates": 0}

        total_cells = len(df) * len(df.columns)
        missing_pct = (df.isna().sum().sum() / total_cells) * 100 if total_cells > 0 else 0
        duplicates = df.duplicated().sum()

        return {
            "rows": len(df),
            "columns": len(df.columns),
            "missing_pct": round(missing_pct, 1),
            "duplicates": int(duplicates),
            "duplicate_pct": round(duplicates / len(df) * 100, 1) if len(df) > 0 else 0,
        }

    def _concentration_facts(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect concentration: what % of value comes from top N items."""
        facts: List[Dict[str, Any]] = []

        # Look for potential "customer", "product", "category" columns
        cat_cols = df.select_dtypes(include=["object", "category"]).columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        for cat_col in cat_cols:
            # Look for a value column (revenue, sales, amount)
            value_col = None
            for num_col in numeric_cols:
                name = num_col.lower()
                if any(kw in name for kw in ["revenue", "sales", "amount", "total", "value"]):
                    value_col = num_col
                    break

            if value_col is None:
                continue

            # Calculate concentration
            grouped = df.groupby(cat_col)[value_col].sum().sort_values(ascending=False)
            total = grouped.sum()

            if total == 0:
                continue

            top_10_pct = grouped.head(10).sum() / total * 100 if len(grouped) >= 10 else grouped.sum() / total * 100
            top_count = min(10, len(grouped))

            facts.append({
                "column": cat_col,
                "value_metric": value_col,
                "top_n": int(top_count),
                "top_pct": round(top_10_pct, 1),
            })

        return facts[:3]  # Limit to 3

    def _outlier_facts(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect outliers in numeric columns."""
        facts: List[Dict[str, Any]] = []
        numeric_df = df.select_dtypes(include=[np.number])

        for col in numeric_df.columns:
            if "id" in col.lower() or "code" in col.lower():
                continue

            series = numeric_df[col].dropna().replace({np.inf: np.nan, -np.inf: np.nan}).dropna()
            if series.empty:
                continue

            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1

            if IQR == 0:
                continue

            outliers = ((series < Q1 - 1.5 * IQR) | (series > Q3 + 1.5 * IQR)).sum()
            outlier_pct = outliers / len(series) * 100 if len(series) > 0 else 0

            if outlier_pct >= 3:
                facts.append({
                    "column": col,
                    "count": int(outliers),
                    "pct": round(outlier_pct, 1),
                })

        return facts[:3]  # Limit to 3

    def _metric_facts(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Extract key numeric metrics."""
        facts: List[Dict[str, Any]] = []
        numeric_df = df.select_dtypes(include=[np.number])

        for col in numeric_df.columns:
            if "id" in col.lower() or "code" in col.lower():
                continue

            series = numeric_df[col].dropna().replace({np.inf: np.nan, -np.inf: np.nan}).dropna()
            if series.empty:
                continue

            facts.append({
                "name": col,
                "total": round(series.sum(), 2),
                "avg": round(series.mean(), 2),
                "min": round(series.min(), 2),
                "max": round(series.max(), 2),
            })

            if len(facts) >= 3:
                break

        return facts

    def _domain_facts(self, df: pd.DataFrame, domain: str) -> Dict[str, Any]:
        """Extract domain-specific facts."""
        domain_lower = domain.lower()

        if "ecommerce" in domain_lower or "commerce" in domain_lower or "retail" in domain_lower:
            return self._ecommerce_facts(df)
        elif "finance" in domain_lower or "financial" in domain_lower:
            return self._finance_facts(df)
        elif "marketing" in domain_lower or "campaign" in domain_lower:
            return self._marketing_facts(df)
        else:
            return {}

    def _ecommerce_facts(self, df: pd.DataFrame) -> Dict[str, Any]:
        """E-commerce specific facts."""
        facts: Dict[str, Any] = {}

        product_col = self._first_existing(df, ["product_id", "Product_ID", "sku", "SKU"])
        if product_col:
            facts["unique_products"] = int(df[product_col].nunique(dropna=True))

        customer_col = self._first_existing(df, ["customer_id", "Customer_ID", "user_id", "User_ID"])
        if customer_col:
            facts["unique_customers"] = int(df[customer_col].nunique(dropna=True))

        order_col = self._first_existing(df, ["order_id", "Order_ID"])
        if order_col:
            facts["unique_orders"] = int(df[order_col].nunique(dropna=True))

        return facts

    def _finance_facts(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Finance specific facts."""
        facts: Dict[str, Any] = {}

        amount_col = self._first_matching(df, ["amount", "balance", "value", "exposure"])
        if amount_col:
            series = df[amount_col].dropna()
            if not series.empty:
                facts["total_amount"] = round(series.sum(), 2)
                facts["avg_amount"] = round(series.mean(), 2)

        return facts

    def _marketing_facts(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Marketing specific facts."""
        facts: Dict[str, Any] = {}

        spend_col = self._first_matching(df, ["spend", "cost", "budget"])
        clicks_col = self._first_matching(df, ["click", "clicks"])
        impressions_col = self._first_matching(df, ["impression", "impressions", "views"])

        if spend_col and impressions_col:
            spend = df[spend_col].replace({np.inf: np.nan, -np.inf: np.nan}).dropna()
            imps = df[impressions_col].replace({np.inf: np.nan, -np.inf: np.nan}).dropna()
            if not spend.empty and not imps.empty and imps.sum() > 0:
                cpm = (spend.sum() / imps.sum()) * 1000
                facts["cpm"] = round(cpm, 2)

        if spend_col and clicks_col:
            spend = df[spend_col].replace({np.inf: np.nan, -np.inf: np.nan}).dropna()
            clicks = df[clicks_col].replace({np.inf: np.nan, -np.inf: np.nan}).dropna()
            if not spend.empty and not clicks.empty and clicks.sum() > 0:
                cpc = spend.sum() / clicks.sum()
                facts["cpc"] = round(cpc, 2)

        return facts
    

    def analyze(self, df: pd.DataFrame, domain: str = None) -> Dict[str, Any]:
        """Wrapper for generate_insights - called by engine.py"""
        return self.generate_insights(df, domain)


    # -------------- Helpers -------------- #

    def _first_existing(self, df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
        for col in candidates:
            if col in df.columns:
                return col
        return None

    def _first_matching(self, df: pd.DataFrame, keywords: List[str]) -> Optional[str]:
        for col in df.select_dtypes(include=[np.number]).columns:
            name = col.lower()
            for kw in keywords:
                if kw in name:
                    return col
        return None
