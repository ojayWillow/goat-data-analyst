"""
Data Profiler - Auto-detect column types and generate data quality reports
"""

import logging
from typing import Dict, List, Any

import numpy as np
import pandas as pd
import warnings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProfiler:
    """Profiles datasets and generates quality reports"""

    def __init__(self):
        # Use an internal attribute to store the last profile
        self._profile_data: Dict[str, Any] = {}

    def detect_column_type(self, series: pd.Series) -> str:
        """
        Detect the semantic type of a column.

        Returns: 'numeric', 'categorical', 'datetime', 'text', 'boolean', 'id', or 'unknown'.
        """
        # Check if boolean-like
        non_null = series.dropna()
        if (
            series.dtype == bool
            or set(non_null.unique()) <= {0, 1, True, False, "True", "False", "true", "false"}
        ):
            return "boolean"

        # Check if numeric
        if pd.api.types.is_numeric_dtype(series):
            unique_ratio = non_null.nunique() / len(non_null) if len(non_null) else 0.0
            if unique_ratio > 0.95 and series.name and "_id" in str(series.name).lower():
                return "id"
            return "numeric"

        # Check if datetime dtype
        if pd.api.types.is_datetime64_any_dtype(series):
            return "datetime"

        # Try to parse as datetime from object/string
        if series.dtype == object:
            sample = non_null.head(100)
            try:
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=UserWarning)
                    pd.to_datetime(sample, errors="raise", infer_datetime_format=True)
                return "datetime"
            except Exception:
                pass

        # High-uniqueness ID-like object column
        if series.dtype == object:
            unique_ratio = non_null.nunique() / len(non_null) if len(non_null) else 0.0
            if unique_ratio > 0.95 and series.name and (
                "id" in str(series.name).lower() or "key" in str(series.name).lower()
            ):
                return "id"

        # Categorical: low unique ratio
        unique_ratio = non_null.nunique() / len(non_null) if len(non_null) else 0.0
        if unique_ratio < 0.05:
            return "categorical"

        # Text vs categorical: based on average length
        if series.dtype == object:
            lengths = non_null.astype(str).str.len()
            avg_length = lengths.mean() if len(lengths) else 0.0
            if avg_length > 50:
                return "text"
            return "categorical"

        return "unknown"

    def profile_column(self, series: pd.Series) -> Dict[str, Any]:
        """Generate detailed profile for a single column."""
        col_type = self.detect_column_type(series)
        non_null = series.dropna()

        count = len(series)
        missing = int(series.isnull().sum())
        missing_pct = (missing / count) * 100 if count else 0.0
        unique = int(series.nunique())
        unique_pct = (unique / count) * 100 if count else 0.0

        profile: Dict[str, Any] = {
            "name": series.name,
            "type": col_type,
            "dtype": str(series.dtype),
            "count": count,
            "missing": missing,
            "missing_pct": missing_pct,
            "unique": unique,
            "unique_pct": unique_pct,
        }

        # Type-specific profiling
        if col_type == "numeric":
            profile.update(self._profile_numeric(series, non_null))
        elif col_type == "categorical":
            profile.update(self._profile_categorical(series, non_null))
        elif col_type == "datetime":
            profile.update(self._profile_datetime(series))
        elif col_type == "text":
            profile.update(self._profile_text(series, non_null))

        # Data quality flags
        profile["quality_issues"] = []

        if profile["missing_pct"] > 50:
            profile["quality_issues"].append("HIGH_MISSING_DATA")
        elif profile["missing_pct"] > 20:
            profile["quality_issues"].append("MODERATE_MISSING_DATA")

        if col_type == "numeric" and profile.get("outliers_pct", 0) > 5:
            profile["quality_issues"].append("MANY_OUTLIERS")

        if profile["unique"] == 1:
            profile["quality_issues"].append("CONSTANT_VALUE")

        if col_type == "categorical" and profile["unique"] > 100:
            profile["quality_issues"].append("HIGH_CARDINALITY")

        return profile

    def _profile_numeric(self, series: pd.Series, non_null: pd.Series) -> Dict[str, Any]:
        """Profile numeric column-specific stats."""
        result: Dict[str, Any] = {
            "min": float(non_null.min()) if len(non_null) else None,
            "max": float(non_null.max()) if len(non_null) else None,
            "mean": float(non_null.mean()) if len(non_null) else None,
            "median": float(non_null.median()) if len(non_null) else None,
            "std": float(non_null.std()) if len(non_null) else None,
            "zeros": int((series == 0).sum()),
            "negatives": int((series < 0).sum()),
        }

        # Outliers via IQR
        if len(non_null) >= 4:
            Q1 = non_null.quantile(0.25)
            Q3 = non_null.quantile(0.75)
            IQR = Q3 - Q1
            if IQR > 0:
                outliers = ((non_null < (Q1 - 1.5 * IQR)) | (non_null > (Q3 + 1.5 * IQR))).sum()
            else:
                outliers = 0
        else:
            outliers = 0

        outliers_pct = (outliers / len(non_null)) * 100 if len(non_null) else 0.0
        result["outliers"] = int(outliers)
        result["outliers_pct"] = float(outliers_pct)

        return result

    def _profile_categorical(self, series: pd.Series, non_null: pd.Series) -> Dict[str, Any]:
        """Profile categorical column-specific stats."""
        value_counts = non_null.value_counts()
        top_values = value_counts.head(10).to_dict()
        most_common = value_counts.index[0] if len(value_counts) > 0 else None
        most_common_freq = int(value_counts.iloc[0]) if len(value_counts) > 0 else 0

        return {
            "top_values": top_values,
            "most_common": most_common,
            "most_common_freq": most_common_freq,
        }

    def _profile_datetime(self, series: pd.Series) -> Dict[str, Any]:
        """Profile datetime column-specific stats."""
        try:
            dt_series = pd.to_datetime(series, errors="coerce")
            dt_series = dt_series.dropna()
            if len(dt_series) == 0:
                return {"min_date": None, "max_date": None, "range_days": None}

            min_date = dt_series.min()
            max_date = dt_series.max()
            range_days = (max_date - min_date).days if min_date and max_date else None

            return {
                "min_date": min_date,
                "max_date": max_date,
                "range_days": range_days,
            }
        except Exception:
            return {"min_date": None, "max_date": None, "range_days": None}

    def _profile_text(self, series: pd.Series, non_null: pd.Series) -> Dict[str, Any]:
        """Profile text column-specific stats."""
        lengths = non_null.astype(str).str.len()
        if len(lengths) == 0:
            return {"min_length": None, "max_length": None, "avg_length": None}

        return {
            "min_length": int(lengths.min()),
            "max_length": int(lengths.max()),
            "avg_length": float(lengths.mean()),
        }

    def profile(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Main entry point used by engine.py: profile the dataframe."""
        return self.profile_dataframe(df)

    def profile_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive profile for entire dataframe."""
        logger.info(f"Profiling dataframe: {df.shape[0]} rows � {df.shape[1]} columns")

        total_cells = int(df.shape[0] * df.shape[1]) if df.shape[0] and df.shape[1] else 0
        total_missing = int(df.isnull().sum().sum())
        total_missing_pct = (total_missing / total_cells) * 100 if total_cells else 0.0

        overall_profile = {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "memory_mb": float(df.memory_usage(deep=True).sum() / (1024 ** 2)),
            "total_missing": total_missing,
            "total_missing_pct": float(total_missing_pct),
        }

        # Profile each column
        column_profiles: List[Dict[str, Any]] = []
        for col in df.columns:
            col_profile = self.profile_column(df[col])
            column_profiles.append(col_profile)

        # Detect potential relationships (correlations) for numeric columns
        numeric_cols = [
            col for col in df.columns if self.detect_column_type(df[col]) == "numeric"
        ]
        correlations: Dict[str, float] = {}
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            for i in range(len(corr_matrix.columns)):
                for j in range(i + 1, len(corr_matrix.columns)):
                    col_i = corr_matrix.columns[i]
                    col_j = corr_matrix.columns[j]
                    corr_val = corr_matrix.iloc[i, j]
                    if not np.isnan(corr_val) and abs(corr_val) > 0.7:
                        correlations[f"{col_i} vs {col_j}"] = float(corr_val)

        # Column types summary
        type_summary: Dict[str, int] = {}
        for col_profile in column_profiles:
            col_type = col_profile["type"]
            type_summary[col_type] = type_summary.get(col_type, 0) + 1

        # Store profile in instance
        self._profile_data = {
            "overall": overall_profile,
            "columns": column_profiles,
            "type_summary": type_summary,
            "correlations": correlations,
        }

        # Calculate and add quality metrics
        quality_report = self.get_quality_report()
        self._profile_data["quality_score"] = quality_report["score"]
        self._profile_data["quality_status"] = quality_report["status"]
        self._profile_data["quality_metrics"] = {
            "issues": quality_report["issues"],
            "warnings": quality_report["warnings"],
        }

        logger.info("? Profiling complete")
        return self._profile_data

    def get_quality_report(self) -> Dict[str, Any]:
        """Generate data quality report based on the last profile."""
        if not self._profile_data:
            raise ValueError("No profile available. Run profile_dataframe first.")

        issues: List[str] = []
        warnings: List[str] = []

        overall = self._profile_data["overall"]
        columns = self._profile_data["columns"]

        # Overall missingness
        total_missing_pct = overall.get("total_missing_pct", 0.0)
        if total_missing_pct > 20:
            issues.append(f"High overall missing data: {total_missing_pct:.1f}%")

        # Column-specific issues
        for col_profile in columns:
            col_name = col_profile["name"]
            for issue in col_profile.get("quality_issues", []):
                warnings.append(f"{col_name}: {issue}")

        # Constant columns
        constant_cols = [col["name"] for col in columns if col.get("unique", 0) == 1]
        if constant_cols:
            warnings.append(
                f"Constant columns (no variation): {', '.join(map(str, constant_cols))}"
            )

        # Base score: 100 minus penalties
        score = 100
        score -= len(issues) * 10
        score -= len(warnings) * 2
        if score < 0:
            score = 0

        status = "GOOD" if len(issues) == 0 else "NEEDS_ATTENTION"

        return {
            "status": status,
            "issues": issues,
            "warnings": warnings,
            "score": score,
        }

    def print_summary(self) -> None:
        """Print a human-readable summary to stdout."""
        if not self._profile_data:
            print("No profile available. Run profile_dataframe first.")
            return

        overall = self._profile_data["overall"]
        type_summary = self._profile_data["type_summary"]
        correlations = self._profile_data["correlations"]

        print("=" * 80)
        print("?? DATA PROFILE SUMMARY")
        print("=" * 80)

        print(
            f"\n?? Size: {overall['rows']:,} rows � {overall['columns']} columns"
        )
        print(f"?? Memory: {overall['memory_mb']:.2f} MB")
        print(
            f"? Missing: {overall['total_missing']:,} cells ({overall['total_missing_pct']:.1f}%)"
        )

        print(f"\n?? Column Types:")
        for col_type, count in type_summary.items():
            print(f"  � {col_type}: {count}")

        quality = self.get_quality_report()
        print(f"\n? Quality Score: {quality['score']}/100 ({quality['status']})")

        if quality["issues"]:
            print(f"\n?? Issues:")
            for issue in quality["issues"]:
                print(f"  � {issue}")

        if quality["warnings"]:
            print(f"\n??  Warnings:")
            for warning in quality["warnings"][:5]:
                print(f"  � {warning}")
            if len(quality["warnings"]) > 5:
                print(f"  ... and {len(quality['warnings']) - 5} more")

        if correlations:
            print(f"\n?? High Correlations:")
            for pair, corr in list(correlations.items())[:5]:
                print(f"  � {pair}: {corr:.3f}")

        print("\n" + "=" * 80)


def profile_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """Convenience function to profile a dataframe."""
    profiler = DataProfiler()
    return profiler.profile_dataframe(df)
