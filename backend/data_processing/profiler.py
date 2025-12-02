"""
Data Profiler - Auto-detect column types and generate data quality reports
"""

import pandas as pd
import warnings
import numpy as np
from typing import Dict, List, Any
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProfiler:
    """Profiles datasets and generates quality reports"""
    
    def __init__(self):
        self._profile_data = {}  # 🔴 CHANGED: Renamed from self.profile to avoid conflict
    
    def detect_column_type(self, series: pd.Series) -> str:
        """
        Detect the semantic type of a column
        
        Returns: 'numeric', 'categorical', 'datetime', 'text', 'boolean', 'id'
        """
        # Check if boolean
        if series.dtype == bool or set(series.dropna().unique()) <= {0, 1, True, False, 'True', 'False', 'true', 'false'}:
            return 'boolean'
        
        # Check if numeric
        if pd.api.types.is_numeric_dtype(series):
            unique_ratio = series.nunique() / len(series)
            
            # If almost all unique and looks like an ID
            if unique_ratio > 0.95 and '_id' in series.name.lower():
                return 'id'
            
            return 'numeric'
        
        # Check if datetime
        if pd.api.types.is_datetime64_any_dtype(series):
            return 'datetime'

        # Try to parse as datetime (suppress noisy pandas UserWarning)
        if series.dtype == object:
            sample = series.dropna().head(100)
            try:
                with warnings.catch_warnings():
                    warnings.filterwarnings('ignore', category=UserWarning)
                    pd.to_datetime(sample, errors='raise', infer_datetime_format=True)
                return 'datetime'
            except Exception:
                pass

        
        # Check if it's an ID column (high uniqueness)
        if series.dtype == object:
            unique_ratio = series.nunique() / len(series)
            if unique_ratio > 0.95 and ('id' in series.name.lower() or 'key' in series.name.lower()):
                return 'id'
        
        # Check if categorical (low unique values relative to size)
        unique_ratio = series.nunique() / len(series)
        if unique_ratio < 0.05:  # Less than 5% unique
            return 'categorical'
        
        # Check average text length
        if series.dtype == object:
            avg_length = series.dropna().astype(str).str.len().mean()
            if avg_length > 50:  # Long text
                return 'text'
            else:
                return 'categorical'
        
        return 'unknown'
    
    def profile_column(self, series: pd.Series) -> Dict[str, Any]:
        """Generate detailed profile for a single column"""
        
        col_type = self.detect_column_type(series)
        
        profile = {
            'name': series.name,
            'type': col_type,
            'dtype': str(series.dtype),
            'count': len(series),
            'missing': series.isnull().sum(),
            'missing_pct': (series.isnull().sum() / len(series)) * 100,
            'unique': series.nunique(),
            'unique_pct': (series.nunique() / len(series)) * 100,
        }
        
        # Type-specific profiling
        if col_type == 'numeric':
            profile.update({
                'min': series.min(),
                'max': series.max(),
                'mean': series.mean(),
                'median': series.median(),
                'std': series.std(),
                'zeros': (series == 0).sum(),
                'negatives': (series < 0).sum(),
            })
            
            # Check for outliers (IQR method)
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((series < (Q1 - 1.5 * IQR)) | (series > (Q3 + 1.5 * IQR))).sum()
            profile['outliers'] = outliers
            profile['outliers_pct'] = (outliers / len(series)) * 100
        
        elif col_type == 'categorical':
            value_counts = series.value_counts()
            profile.update({
                'top_values': value_counts.head(10).to_dict(),
                'most_common': value_counts.index[0] if len(value_counts) > 0 else None,
                'most_common_freq': value_counts.iloc[0] if len(value_counts) > 0 else 0,
            })
        
        elif col_type == 'datetime':
            try:
                dt_series = pd.to_datetime(series, errors='coerce')
                profile.update({
                    'min_date': dt_series.min(),
                    'max_date': dt_series.max(),
                    'range_days': (dt_series.max() - dt_series.min()).days if dt_series.min() and dt_series.max() else None,
                })
            except:
                pass
        
        elif col_type == 'text':
            lengths = series.dropna().astype(str).str.len()
            profile.update({
                'min_length': lengths.min(),
                'max_length': lengths.max(),
                'avg_length': lengths.mean(),
            })
        
        # Data quality flags
        profile['quality_issues'] = []
        
        if profile['missing_pct'] > 50:
            profile['quality_issues'].append('HIGH_MISSING_DATA')
        elif profile['missing_pct'] > 20:
            profile['quality_issues'].append('MODERATE_MISSING_DATA')
        
        if col_type == 'numeric' and profile.get('outliers_pct', 0) > 5:
            profile['quality_issues'].append('MANY_OUTLIERS')
        
        if profile['unique'] == 1:
            profile['quality_issues'].append('CONSTANT_VALUE')
        
        if col_type == 'categorical' and profile['unique'] > 100:
            profile['quality_issues'].append('HIGH_CARDINALITY')
        
        return profile
    
    def profile(self, df: pd.DataFrame) -> Dict[str, Any]:  # 🔴 CHANGED: This is the method engine.py calls
        """Generate comprehensive profile for entire dataframe - main entry point"""
        return self.profile_dataframe(df)
    
    def profile_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive profile for entire dataframe"""
        
        logger.info(f"Profiling dataframe: {df.shape[0]} rows × {df.shape[1]} columns")
        
        # Overall stats
        overall_profile = {
            'rows': df.shape[0],
            'columns': df.shape[1],
            'memory_mb': df.memory_usage(deep=True).sum() / (1024 ** 2),
            'total_missing': df.isnull().sum().sum(),
            'total_missing_pct': (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100,
        }
        
        # Profile each column
        column_profiles = []
        for col in df.columns:
            col_profile = self.profile_column(df[col])
            column_profiles.append(col_profile)
        
        # Detect potential relationships
        numeric_cols = [col for col in df.columns if self.detect_column_type(df[col]) == 'numeric']
        
        # Correlation for numeric columns (if more than 1)
        correlations = {}
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            # Find high correlations
            for i in range(len(corr_matrix.columns)):
                for j in range(i + 1, len(corr_matrix.columns)):
                    corr_val = corr_matrix.iloc[i, j]
                    if abs(corr_val) > 0.7:  # High correlation threshold
                        correlations[f"{corr_matrix.columns[i]} vs {corr_matrix.columns[j]}"] = corr_val
        
        # Identify column types summary
        type_summary = {}
        for col_profile in column_profiles:
            col_type = col_profile['type']
            type_summary[col_type] = type_summary.get(col_type, 0) + 1
        
        self._profile_data = {  # 🔴 CHANGED: Use _profile_data
            'overall': overall_profile,
            'columns': column_profiles,
            'type_summary': type_summary,
            'correlations': correlations,
        }
        
        # Calculate and add quality metrics
        quality_report = self.get_quality_report()
        self._profile_data['quality_score'] = quality_report['score']
        self._profile_data['quality_status'] = quality_report['status']
        self._profile_data['quality_metrics'] = {
            'issues': quality_report['issues'],
            'warnings': quality_report['warnings']
        }
        
        logger.info("✅ Profiling complete")
        
        return self._profile_data
    
    def get_quality_report(self) -> Dict[str, Any]:
        """Generate data quality report"""
        
        if not self._profile_data:  # 🔴 CHANGED: Use _profile_data
            raise ValueError("No profile available. Run profile_dataframe first.")
        
        issues = []
        warnings = []
        
        # Check overall quality
        if self._profile_data['overall']['total_missing_pct'] > 20:
            issues.append(f"High overall missing data: {self._profile_data['overall']['total_missing_pct']:.1f}%")
        
        # Check column-specific issues
        for col_profile in self._profile_data['columns']:
            if col_profile['quality_issues']:
                for issue in col_profile['quality_issues']:
                    warnings.append(f"{col_profile['name']}: {issue}")
        
        # Check for constant columns
        constant_cols = [col['name'] for col in self._profile_data['columns'] if col['unique'] == 1]
        if constant_cols:
            warnings.append(f"Constant columns (no variation): {', '.join(constant_cols)}")
        
        return {
            'status': 'GOOD' if len(issues) == 0 else 'NEEDS_ATTENTION',
            'issues': issues,
            'warnings': warnings,
            'score': max(0, 100 - len(issues) * 10 - len(warnings) * 2),
        }
    
    def print_summary(self):
        """Print human-readable summary"""
        
        if not self._profile_data:  # 🔴 CHANGED: Use _profile_data
            print("No profile available. Run profile_dataframe first.")
            return
        
        print("=" * 80)
        print("📊 DATA PROFILE SUMMARY")
        print("=" * 80)
        
        print(f"\n📏 Size: {self._profile_data['overall']['rows']:,} rows × {self._profile_data['overall']['columns']} columns")
        print(f"💾 Memory: {self._profile_data['overall']['memory_mb']:.2f} MB")
        print(f"❓ Missing: {self._profile_data['overall']['total_missing']:,} cells ({self._profile_data['overall']['total_missing_pct']:.1f}%)")
        
        print(f"\n📋 Column Types:")
        for col_type, count in self._profile_data['type_summary'].items():
            print(f"  • {col_type}: {count}")
        
        # Quality report
        quality = self.get_quality_report()
        print(f"\n✅ Quality Score: {quality['score']}/100 ({quality['status']})")
        
        if quality['issues']:
            print(f"\n🚨 Issues:")
            for issue in quality['issues']:
                print(f"  • {issue}")
        
        if quality['warnings']:
            print(f"\n⚠️  Warnings:")
            for warning in quality['warnings'][:5]:  # Show first 5
                print(f"  • {warning}")
            if len(quality['warnings']) > 5:
                print(f"  ... and {len(quality['warnings']) - 5} more")
        
        if self._profile_data['correlations']:
            print(f"\n🔗 High Correlations:")
            for pair, corr in list(self._profile_data['correlations'].items())[:5]:
                print(f"  • {pair}: {corr:.3f}")
        
        print("\n" + "=" * 80)


# Convenience function
def profile_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """Quick function to profile a dataframe"""
    profiler = DataProfiler()
    return profiler.profile_dataframe(df)
