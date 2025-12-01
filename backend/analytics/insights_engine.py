"""
Insights Engine - Generate actionable business insights from data
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional


class InsightsEngine:
    """Generate business insights from dataset analysis."""

    def generate_insights(self, df: pd.DataFrame, domain: str = None) -> List[str]:
        """
        Generate key insights based on data patterns.
        Returns a small, focused set of insights (up to 10).
        """
        insights: List[str] = []

        # 1) Data quality / structure
        insights.extend(self._quality_insights(df))

        # 2) Numeric patterns (outliers, spread, magnitude)
        insights.extend(self._numeric_insights(df))

        # 3) Categorical patterns (concentration, high cardinality)
        insights.extend(self._categorical_insights(df))

        # 4) Domain-specific insights (if domain is known)
        if domain:
            insights.extend(self._domain_insights(df, domain))

        # De-duplicate while preserving order
        seen = set()
        unique_insights: List[str] = []
        for text in insights:
            if text and text not in seen:
                unique_insights.append(text)
                seen.add(text)

        return unique_insights[:10]

    # -------------- Quality / structure insights -------------- #

    def _quality_insights(self, df: pd.DataFrame) -> List[str]:
        """Insights about data quality and basic structure."""
        insights: List[str] = []
        if df.empty:
            return ["Dataset is empty – no analysis can be performed."]

        total_cells = len(df) * len(df.columns)
        if total_cells == 0:
            return ["Dataset has no usable values – please check the source file."]

        missing_pct = (df.isna().sum().sum() / total_cells) * 100

        if missing_pct > 30:
            insights.append(
                f"Overall data quality is weak: about {missing_pct:.1f}% of all values are missing. "
                f"Any analysis should be treated with caution until key gaps are fixed."
            )
        elif missing_pct > 10:
            insights.append(
                f"Data quality is moderate: {missing_pct:.1f}% of values are missing. "
                f"Some metrics may be biased if missingness is not random."
            )
        else:
            insights.append(
                f"Data quality is strong overall: only {missing_pct:.1f}% of values are missing."
            )

        duplicates = df.duplicated().sum()
        if duplicates > 0:
            share = duplicates / len(df) * 100
            insights.append(
                f"Found {duplicates:,} duplicate rows "
                f"({share:.1f}% of all records). Review whether these are true duplicates or repeated events."
            )

        # Basic shape
        insights.append(
            f"Dataset contains {len(df):,} rows across {df.shape[1]} columns, "
            f"providing a reasonably rich basis for analysis."
        )

        return insights

    # -------------- Numeric insights -------------- #

    def _numeric_insights(self, df: pd.DataFrame) -> List[str]:
        """Insights from numeric columns."""
        insights: List[str] = []
        numeric_df = df.select_dtypes(include=[np.number])

        if numeric_df.empty:
            return insights

        # Focus on up to 5 numeric columns that look like metrics (skip ids)
        metric_cols: List[str] = []
        for col in numeric_df.columns:
            name = col.lower()
            if "id" in name or "code" in name:
                continue
            metric_cols.append(col)
            if len(metric_cols) >= 5:
                break

        if not metric_cols:
            return insights

        # Outlier and spread insights
        for col in metric_cols:
            series = numeric_df[col].dropna()
            if series.empty:
                continue

            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1 if Q3 is not None and Q1 is not None else None
            if IQR is None or IQR == 0:
                continue

            outliers = ((series < Q1 - 1.5 * IQR) | (series > Q3 + 1.5 * IQR)).sum()
            if outliers <= 0:
                continue

            outlier_pct = (outliers / len(series)) * 100
            if outlier_pct >= 10:
                insights.append(
                    f"Column '{col}' shows a wide spread with approx. {outlier_pct:.1f}% of values "
                    f"flagged as statistical outliers. These may indicate exceptional cases or data errors."
                )
            elif outlier_pct >= 3:
                insights.append(
                    f"Column '{col}' contains about {outlier_pct:.1f}% outliers. "
                    f"These extreme values can materially impact averages and totals."
                )

        # Magnitude / skew on the main metric
        main_col = metric_cols[0]
        series_main = numeric_df[main_col].dropna()
        if not series_main.empty:
            p10 = series_main.quantile(0.10)
            p90 = series_main.quantile(0.90)
            avg = series_main.mean()
            if p10 is not None and p90 is not None:
                if p90 > 0 and p10 >= 0 and p90 / max(p10, 1e-9) > 10:
                    insights.append(
                        f"Values in '{main_col}' are highly uneven: the top 10% are more than 10x larger "
                        f"than the bottom 10%. This suggests a heavy concentration at the top end."
                    )
            insights.append(
                f"For the key metric '{main_col}', the average value is approximately {avg:,.2f}. "
                f"Use this as a benchmark when comparing individual records or segments."
            )

        return insights[:3]

    # -------------- Categorical insights -------------- #

    def _categorical_insights(self, df: pd.DataFrame) -> List[str]:
        """Insights from categorical columns."""
        insights: List[str] = []
        cat_df = df.select_dtypes(include=["object", "category", "string"])

        if cat_df.empty:
            return insights

        # Consider only columns with a reasonable number of unique values
        for col in cat_df.columns:
            series = cat_df[col].dropna()
            if series.empty:
                continue

            unique_count = series.nunique()
            total = len(series)
            if total == 0:
                continue

            most_common = series.value_counts().iloc[0]
            most_common_pct = (most_common / total) * 100

            if most_common_pct > 85 and unique_count <= 10:
                insights.append(
                    f"Column '{col}' is heavily concentrated: about {most_common_pct:.0f}% of records "
                    f"share the same value. This may limit its usefulness for segmentation."
                )
            elif most_common_pct < 40 and unique_count <= 50:
                insights.append(
                    f"Column '{col}' shows a relatively balanced distribution across {unique_count} categories, "
                    f"which is useful for comparing performance by '{col}'."
                )

            if unique_count > 500:
                insights.append(
                    f"Column '{col}' has {unique_count:,} distinct values. "
                    f"Consider grouping or focusing on the top categories to keep analysis manageable."
                )

        return insights[:3]

    # -------------- Domain-specific insights -------------- #

    def _domain_insights(self, df: pd.DataFrame, domain: str) -> List[str]:
        """Domain-specific insights."""
        insights: List[str] = []
        domain_lower = domain.lower()

        if "e-commerce" in domain_lower or "commerce" in domain_lower or "retail" in domain_lower:
            insights.extend(self._ecommerce_insights(df))

        elif "finance" in domain_lower or "financial" in domain_lower:
            insights.extend(self._finance_insights(df))

        elif "marketing" in domain_lower or "campaign" in domain_lower:
            insights.extend(self._marketing_insights(df))

        else:
            # Generic fallback
            insights.append(
                f"Domain '{domain}' detected, but no specific rules are yet defined. "
                f"Generic structural insights have been applied."
            )

        return insights

    # ---- Specific domain helpers ---- #

    def _ecommerce_insights(self, df: pd.DataFrame) -> List[str]:
        insights: List[str] = []
        # Product dimension
        product_col = self._first_existing(df, ["Product_ID", "product_id", "sku", "SKU"])
        if product_col:
            unique_products = df[product_col].nunique(dropna=True)
            insights.append(
                f"E‑commerce: catalog contains approximately {unique_products:,} unique products "
                f"based on '{product_col}'."
            )

        # Customer dimension
        customer_col = self._first_existing(df, ["User_ID", "user_id", "customer_id", "Customer_ID"])
        if customer_col:
            unique_customers = df[customer_col].nunique(dropna=True)
            insights.append(
                f"E‑commerce: dataset includes around {unique_customers:,} unique customers "
                f"based on '{customer_col}'."
            )

        # Order dimension
        order_col = self._first_existing(df, ["order_id", "Order_ID"])
        if order_col:
            order_count = df[order_col].nunique(dropna=True)
            insights.append(
                f"E‑commerce: there are {order_count:,} distinct orders in this dataset."
            )

        return insights

    def _finance_insights(self, df: pd.DataFrame) -> List[str]:
        insights: List[str] = []
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        if numeric_cols:
            insights.append(
                f"Finance: {len(numeric_cols)} numeric metrics are available for analysis, "
                f"including columns such as {', '.join(numeric_cols[:5])}."
            )

        # Look for typical finance columns
        amount_col = self._first_matching(df, ["amount", "balance", "value", "exposure", "limit"])
        if amount_col:
            series = df[amount_col].dropna()
            if not series.empty:
                total = series.sum()
                avg = series.mean()
                insights.append(
                    f"Finance: total '{amount_col}' across all records is approximately {total:,.2f}, "
                    f"with an average per record of {avg:,.2f}."
                )

        return insights

    def _marketing_insights(self, df: pd.DataFrame) -> List[str]:
        insights: List[str] = []
        spend_col = self._first_matching(df, ["spend", "cost", "budget"])
        clicks_col = self._first_matching(df, ["click", "clicks"])
        impressions_col = self._first_matching(df, ["impression", "impressions", "views"])

        if spend_col and impressions_col:
            spend = df[spend_col].replace({np.inf: np.nan, -np.inf: np.nan}).dropna()
            imps = df[impressions_col].replace({np.inf: np.nan, -np.inf: np.nan}).dropna()
            if not spend.empty and not imps.empty:
                total_spend = spend.sum()
                total_imps = imps.sum()
                if total_imps > 0:
                    cpm = (total_spend / total_imps) * 1000
                    insights.append(
                        f"Marketing: overall CPM (cost per 1,000 impressions) is approximately {cpm:,.2f} "
                        f"based on '{spend_col}' and '{impressions_col}'."
                    )

        if spend_col and clicks_col:
            spend = df[spend_col].replace({np.inf: np.nan, -np.inf: np.nan}).dropna()
            clicks = df[clicks_col].replace({np.inf: np.nan, -np.inf: np.nan}).dropna()
            if not spend.empty and not clicks.empty and clicks.sum() > 0:
                total_spend = spend.sum()
                total_clicks = clicks.sum()
                cpc = total_spend / total_clicks
                insights.append(
                    f"Marketing: overall CPC (cost per click) is approximately {cpc:,.2f} "
                    f"based on '{spend_col}' and '{clicks_col}'."
                )

        return insights

    # -------------- Helper methods -------------- #

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
