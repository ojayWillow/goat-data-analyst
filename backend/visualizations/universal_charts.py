"""Universal Charts - Domain-agnostic visualizations using Plotly"""

import pandas as pd
import plotly.graph_objects as go
from typing import Dict, List, Optional, Any
import numpy as np


class UniversalChartGenerator:
    """Generate adaptive charts that work with any domain."""

    def __init__(self, df: pd.DataFrame, domain: str = None):
        self.df = df
        self.domain = (domain or "").lower()
        self.charts: Dict[str, str] = {}

    def generate_all_charts(self) -> Dict[str, str]:
        """Generate all applicable charts for the dataset."""

        # 1. Time series trend (if date column exists)
        time_chart = self._create_time_series()
        if time_chart:
            self.charts["time_series"] = time_chart

        # 2. Top N bar chart (categorical + numeric)
        top_n_chart = self._create_top_n_bar()
        if top_n_chart:
            self.charts["top_n"] = top_n_chart

        # 3. Distribution chart (numeric columns)
        dist_chart = self._create_distribution()
        if dist_chart:
            self.charts["distribution"] = dist_chart

        # 4. Correlation heatmap (numeric columns)
        corr_chart = self._create_correlation()
        if corr_chart:
            self.charts["correlation"] = corr_chart

        return self.charts

    # -------- Column detection helpers -------- #

    def _detect_date_column(self) -> Optional[str]:
        """Find the best date/datetime column based on type + name patterns."""
        if self.df.empty:
            return None

        # 1) Already datetime dtypes
        datetime_cols = [
            col
            for col in self.df.columns
            if pd.api.types.is_datetime64_any_dtype(self.df[col])
        ]

        # 2) Name-based preference among datetime cols
        date_keywords = ["date", "time", "created", "updated", "timestamp", "order"]
        for keyword in date_keywords:
            for col in datetime_cols:
                if keyword in col.lower():
                    return col
        if datetime_cols:
            return datetime_cols[0]

        # 3) Try to parse textual columns if they look like dates
        candidate_cols: List[str] = []
        for col in self.df.columns:
            if pd.api.types.is_object_dtype(self.df[col]) or pd.api.types.is_string_dtype(
                self.df[col]
            ):
                candidate_cols.append(col)

        for col in candidate_cols:
            try:
                sample = self.df[col].dropna().head(10)
                if sample.empty:
                    continue
                parsed = pd.to_datetime(sample, errors="coerce", infer_datetime_format=True)
                if parsed.notna().mean() >= 0.7:  # at least 70% parse success
                    return col
            except Exception:
                continue

        return None

    def _detect_value_column(self) -> Optional[str]:
        """Find the best numeric column for values (revenue, amount, etc)."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        if not numeric_cols:
            return None

        value_keywords = [
            "revenue",
            "amount",
            "sale",
            "sales",
            "total",
            "value",
            "price",
            "cost",
            "profit",
            "margin",
            "qty",
            "quantity",
            "volume",
        ]

        # 1) Prefer columns matching value keywords
        for keyword in value_keywords:
            for col in numeric_cols:
                name = col.lower()
                if keyword in name and not name.endswith("id") and "code" not in name:
                    return col

        # 2) If domain hints say "finance" or "sales", try to avoid obvious id-like cols
        if self.domain in {"sales", "finance", "retail", "ecommerce"}:
            filtered = [
                c
                for c in numeric_cols
                if not c.lower().endswith("id")
                and "code" not in c.lower()
                and "zip" not in c.lower()
            ]
            if filtered:
                return filtered[0]

        # 3) Fallback: first numeric, but avoid pure index/id if possible
        safe_numeric = [
            c
            for c in numeric_cols
            if not c.lower().endswith("id") and "index" not in c.lower()
        ]
        if safe_numeric:
            return safe_numeric[0]

        return numeric_cols[0]

    def _detect_category_column(self) -> Optional[str]:
        """Find the best categorical column (customer, product, category)."""
        categorical_cols = self.df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()
        if not categorical_cols:
            return None

        # Remove columns with very high cardinality (too many uniques)
        filtered: List[str] = []
        for col in categorical_cols:
            nunique = self.df[col].nunique(dropna=True)
            if 1 < nunique <= 200:  # avoid single-value or extreme high-card
                filtered.append(col)
        if not filtered:
            filtered = categorical_cols

        cat_keywords = [
            "customer",
            "client",
            "account",
            "product",
            "item",
            "sku",
            "category",
            "segment",
            "name",
            "type",
            "region",
            "country",
            "city",
            "state",
            "brand",
        ]

        # 1) Prefer columns matching keywords
        for keyword in cat_keywords:
            for col in filtered:
                if keyword in col.lower():
                    return col

        # 2) Fallback: the text column with "reasonable" cardinality
        return filtered[0] if filtered else categorical_cols[0]

    # -------- Chart creators -------- #

    def _create_time_series(self) -> Optional[str]:
        """Create time series trend chart."""
        date_col = self._detect_date_column()
        value_col = self._detect_value_column()

        if not date_col or not value_col:
            return None

        try:
            df_temp = self.df[[date_col, value_col]].copy()
            df_temp[date_col] = pd.to_datetime(df_temp[date_col], errors="coerce")
            df_temp = df_temp.dropna(subset=[date_col])
            if df_temp.empty:
                return None

            df_temp = df_temp.sort_values(date_col)

            # Group by date
            df_grouped = df_temp.groupby(date_col, as_index=False)[value_col].sum()

            if df_grouped.empty:
                return None

            fig = go.Figure()
            fig.add_scatter(
                x=df_grouped[date_col],
                y=df_grouped[value_col],
                mode="lines+markers",
                name=value_col,
                line=dict(color="#667eea", width=3),
                marker=dict(size=6),
            )

            fig.update_layout(
                title=f"{value_col} Over Time",
                xaxis_title=date_col,
                yaxis_title=value_col,
                template="plotly_white",
                height=400,
                hovermode="x unified",
            )

            return fig.to_html(include_plotlyjs="cdn", full_html=False, div_id="time_series_chart")

        except Exception as e:
            print(f"Time series chart error: {e}")
            return None

    def _create_top_n_bar(self, n: int = 10) -> Optional[str]:
        """Create Top N bar chart (customers, products, etc)."""
        cat_col = self._detect_category_column()
        value_col = self._detect_value_column()

        if not cat_col or not value_col:
            return None

        try:
            df_temp = self.df[[cat_col, value_col]].dropna(subset=[cat_col])
            if df_temp.empty:
                return None

            df_agg = df_temp.groupby(cat_col, as_index=False)[value_col].sum()
            if df_agg.empty:
                return None

            df_top = df_agg.nlargest(n, value_col)

            fig = go.Figure()
            fig.add_bar(
                x=df_top[value_col],
                y=df_top[cat_col],
                orientation="h",
                marker=dict(
                    color=df_top[value_col],
                    colorscale="Viridis",
                    showscale=True,
                ),
            )

            fig.update_layout(
                title=f"Top {min(n, len(df_top))} {cat_col} by {value_col}",
                xaxis_title=value_col,
                yaxis_title=cat_col,
                template="plotly_white",
                height=400,
                yaxis=dict(autorange="reversed"),
            )

            return fig.to_html(include_plotlyjs="cdn", full_html=False, div_id="top_n_chart")

        except Exception as e:
            print(f"Top N chart error: {e}")
            return None

    def _create_distribution(self) -> Optional[str]:
        """Create distribution histogram for main numeric column."""
        value_col = self._detect_value_column()
        if not value_col:
            return None

        try:
            series = self.df[value_col].dropna()
            if series.empty:
                return None

            fig = go.Figure()
            fig.add_histogram(
                x=series,
                nbinsx=30,
                marker=dict(color="#667eea"),
                name=value_col,
            )

            fig.update_layout(
                title=f"Distribution of {value_col}",
                xaxis_title=value_col,
                yaxis_title="Frequency",
                template="plotly_white",
                height=400,
            )

            return fig.to_html(include_plotlyjs="cdn", full_html=False, div_id="distribution_chart")

        except Exception as e:
            print(f"Distribution chart error: {e}")
            return None

    def _create_correlation(self) -> Optional[str]:
        """Create correlation heatmap for numeric columns."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) < 2:
            return None

        try:
            cols_to_use = numeric_cols[:10]
            df_num = self.df[cols_to_use].dropna(how="all")
            if df_num.empty:
                return None

            corr_matrix = df_num.corr()
            if corr_matrix.isna().all().all():
                return None

            z = corr_matrix.values
            x = corr_matrix.columns.tolist()
            y = corr_matrix.index.tolist()

            fig = go.Figure(
                data=go.Heatmap(
                    z=z,
                    x=x,
                    y=y,
                    colorscale="RdBu",
                    zmid=0,
                    text=np.round(z, 2),
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

            return fig.to_html(include_plotlyjs="cdn", full_html=False, div_id="correlation_chart")

        except Exception as e:
            print(f"Correlation chart error: {e}")
            return None
