"""
Universal Charts Module
Domain-agnostic visualizations that work for any dataset
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Optional, List
import numpy as np


class UniversalChartGenerator:
    """
    Creates universal charts that adapt to any dataset structure.
    These charts don't require specific column names - they auto-detect best candidates.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.charts: Dict[str, str] = {}

    def generate_all_universal_charts(self) -> Dict[str, str]:
        """Generate all applicable universal charts."""
        self.charts = {}

        # Chart 1: Smart Distribution
        dist_chart = self.create_smart_distribution()
        if dist_chart:
            self.charts["distribution"] = dist_chart

        # Chart 2: Category Breakdown
        category_chart = self.create_category_breakdown()
        if category_chart:
            self.charts["categories"] = category_chart

        # Chart 3: Correlation Heatmap
        corr_chart = self.create_correlation_heatmap()
        if corr_chart:
            self.charts["correlation"] = corr_chart

        # Chart 4: Volume Over Time
        volume_chart = self.create_volume_over_time()
        if volume_chart:
            self.charts["volume_trend"] = volume_chart

        return self.charts

    def create_smart_distribution(self) -> Optional[str]:
        """
        Create distribution chart for the most interesting numeric column.
        Picks column with highest variance or most data points.
        """
        try:
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) == 0:
                return None

            # Pick column with highest coefficient of variation (interesting data)
            best_col: Optional[str] = None
            best_score = 0.0

            for col in numeric_cols:
                series = self.df[col].replace({np.inf: np.nan, -np.inf: np.nan}).dropna()
                if series.empty:
                    continue

                std = series.std()
                mean = series.mean()
                if std > 0:
                    cv = std / (mean + 1e-10)
                    if cv > best_score:
                        best_score = cv
                        best_col = col

            if not best_col:
                best_col = numeric_cols[0]

            series = self.df[best_col].replace({np.inf: np.nan, -np.inf: np.nan}).dropna()
            if series.empty:
                return None

            fig = go.Figure()

            fig.add_trace(
                go.Histogram(
                    x=series,
                    name="Distribution",
                    marker=dict(color="#2E86AB", line=dict(color="white", width=1)),
                    nbinsx=30,
                )
            )

            fig.update_layout(
                title=f"Distribution of {best_col}",
                xaxis_title=best_col,
                yaxis_title="Count",
                template="plotly_white",
                height=400,
                showlegend=False,
            )

            return fig.to_html(include_plotlyjs="cdn", div_id="distribution_chart")

        except Exception as e:
            print(f"Could not create distribution chart: {e}")
            return None

    def create_category_breakdown(self, top_n: int = 10) -> Optional[str]:
        """
        Create donut chart for the most interesting categorical column.
        """
        try:
            categorical_cols = self.df.select_dtypes(
                include=["object", "category", "string"]
            ).columns

            best_col: Optional[str] = None
            best_score = 0

            for col in categorical_cols:
                series = self.df[col].dropna()
                if series.empty:
                    continue

                unique_count = series.nunique()
                # Prefer columns with 2-50 unique values
                if 2 <= unique_count <= 50:
                    score = min(unique_count, 20)  # Cap score at 20
                    if score > best_score:
                        best_score = score
                        best_col = col

            if not best_col and len(categorical_cols) > 0:
                best_col = categorical_cols[0]

            if not best_col:
                return None

            series = self.df[best_col].dropna()
            if series.empty:
                return None

            top_categories = series.value_counts().head(top_n)
            if top_categories.empty:
                return None

            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=top_categories.index.astype(str),
                        values=top_categories.values,
                        hole=0.4,
                        marker=dict(colors=px.colors.qualitative.Set3),
                    )
                ]
            )

            fig.update_layout(
                title=f"Top {len(top_categories)} Categories: {best_col}",
                template="plotly_white",
                height=400,
            )

            return fig.to_html(include_plotlyjs="cdn", div_id="categories_chart")

        except Exception as e:
            print(f"Could not create category breakdown: {e}")
            return None

    def create_correlation_heatmap(self) -> Optional[str]:
        """
        Create correlation heatmap for numeric columns.
        """
        try:
            numeric_df = self.df.select_dtypes(include=[np.number]).replace(
                {np.inf: np.nan, -np.inf: np.nan}
            )

            if len(numeric_df.columns) < 2:
                return None

            numeric_df = numeric_df.dropna(how="all")
            if numeric_df.empty:
                return None

            corr_matrix = numeric_df.corr()
            if corr_matrix.isna().all().all():
                return None

            fig = go.Figure(
                data=go.Heatmap(
                    z=corr_matrix.values,
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    colorscale="RdBu",
                    zmid=0,
                    text=corr_matrix.values.round(2),
                    texttemplate="%{text}",
                    textfont={"size": 10},
                    colorbar=dict(title="Correlation"),
                )
            )

            fig.update_layout(
                title="Correlation Heatmap",
                template="plotly_white",
                height=500,
                xaxis=dict(tickangle=-45),
            )

            return fig.to_html(include_plotlyjs="cdn", div_id="correlation_chart")

        except Exception as e:
            print(f"Could not create correlation heatmap: {e}")
            return None

    def create_volume_over_time(self) -> Optional[str]:
        """
        Create volume/count trend over time if date column exists.
        """
        try:
            date_col: Optional[str] = None

            # Detect an existing datetime column first
            for col in self.df.columns:
                if pd.api.types.is_datetime64_any_dtype(self.df[col]):
                    date_col = col
                    break

            # If none, try to parse likely date-like text columns
            if not date_col:
                for col in self.df.columns:
                    name = col.lower()
                    if "date" in name or "time" in name or "created" in name or "order" in name:
                        try:
                            parsed = pd.to_datetime(
                                self.df[col], errors="coerce", infer_datetime_format=True
                            )
                            if parsed.notna().sum() > len(self.df) * 0.5:
                                self.df[col] = parsed
                                date_col = col
                                break
                        except Exception:
                            continue

            if not date_col:
                return None

            df_time = self.df.copy()
            df_time[date_col] = pd.to_datetime(df_time[date_col], errors="coerce")
            df_time = df_time.dropna(subset=[date_col])
            if df_time.empty:
                return None

            df_time = df_time.sort_values(date_col)

            daily_counts = (
                df_time.groupby(df_time[date_col].dt.date).size().reset_index()
            )
            if daily_counts.empty:
                return None

            daily_counts.columns = ["date", "count"]

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=daily_counts["date"],
                    y=daily_counts["count"],
                    mode="lines+markers",
                    name="Volume",
                    line=dict(color="#A23B72", width=2),
                    marker=dict(size=4),
                )
            )

            fig.update_layout(
                title="Volume Trend Over Time",
                xaxis_title="Date",
                yaxis_title="Record Count",
                template="plotly_white",
                height=400,
                hovermode="x unified",
            )

            return fig.to_html(include_plotlyjs="cdn", div_id="volume_trend_chart")

        except Exception as e:
            print(f"Could not create volume trend: {e}")
            return None
#   R e b u i l d   t r i g g e r  
 