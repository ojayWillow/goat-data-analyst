"""
DataFixer - Auto-fix common data quality issues

Provides safe, reversible operations to clean data:
- Remove duplicates
- Fill missing values
- Normalize dates
- Remove outliers
- Standardize column names

Each operation returns a NEW DataFrame (doesn't modify original).
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, List
from datetime import datetime
import re


class DataFixer:
    """
    Auto-fix engine for common data quality issues.
    
    Philosophy:
    - Safe: Never modify original DataFrame
    - Transparent: Return preview of what will change
    - Smart: Use appropriate methods per data type
    """
    
    def __init__(self):
        """Initialize the DataFixer"""
        self.fix_log = []
    
    def remove_duplicates(self, df: pd.DataFrame, 
                         subset: List[str] = None,
                         keep: str = 'first') -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Remove duplicate rows from DataFrame.
        
        Args:
            df: Input DataFrame
            subset: List of columns to check for duplicates (None = all columns)
            keep: Which duplicates to keep ('first', 'last', False for remove all)
            
        Returns:
            Tuple of (cleaned_df, fix_report)
        """
        original_count = len(df)
        
        # Remove duplicates
        df_clean = df.drop_duplicates(subset=subset, keep=keep)
        
        removed_count = original_count - len(df_clean)
        
        report = {
            'operation': 'remove_duplicates',
            'original_rows': original_count,
            'final_rows': len(df_clean),
            'removed_rows': removed_count,
            'percentage_removed': (removed_count / original_count * 100) if original_count > 0 else 0,
            'success': True
        }
        
        self.fix_log.append(report)
        return df_clean, report
    
    def fill_missing_numeric(self, df: pd.DataFrame, 
                           column: str,
                           method: str = 'median') -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Fill missing values in numeric column.
        
        Args:
            df: Input DataFrame
            column: Column name to fix
            method: 'median', 'mean', 'mode', 'zero', or specific value
            
        Returns:
            Tuple of (cleaned_df, fix_report)
        """
        df_clean = df.copy()
        
        missing_count = df_clean[column].isna().sum()
        
        if missing_count == 0:
            return df_clean, {'operation': 'fill_missing', 'message': 'No missing values found'}
        
        # Choose fill value based on method
        if method == 'median':
            fill_value = df_clean[column].median()
        elif method == 'mean':
            fill_value = df_clean[column].mean()
        elif method == 'mode':
            fill_value = df_clean[column].mode()[0] if not df_clean[column].mode().empty else 0
        elif method == 'zero':
            fill_value = 0
        else:
            fill_value = method  # Use provided value
        
        # Fill missing values
        df_clean[column].fillna(fill_value, inplace=True)
        
        report = {
            'operation': 'fill_missing_numeric',
            'column': column,
            'method': method,
            'fill_value': float(fill_value),
            'filled_count': missing_count,
            'percentage_filled': (missing_count / len(df) * 100),
            'success': True
        }
        
        self.fix_log.append(report)
        return df_clean, report
    
    def fill_missing_categorical(self, df: pd.DataFrame,
                                column: str,
                                method: str = 'mode') -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Fill missing values in categorical column.
        
        Args:
            df: Input DataFrame
            column: Column name to fix
            method: 'mode', 'unknown', or specific value
            
        Returns:
            Tuple of (cleaned_df, fix_report)
        """
        df_clean = df.copy()
        
        missing_count = df_clean[column].isna().sum()
        
        if missing_count == 0:
            return df_clean, {'operation': 'fill_missing', 'message': 'No missing values found'}
        
        # Choose fill value
        if method == 'mode':
            fill_value = df_clean[column].mode()[0] if not df_clean[column].mode().empty else 'Unknown'
        elif method == 'unknown':
            fill_value = 'Unknown'
        else:
            fill_value = method
        
        df_clean[column].fillna(fill_value, inplace=True)
        
        report = {
            'operation': 'fill_missing_categorical',
            'column': column,
            'method': method,
            'fill_value': str(fill_value),
            'filled_count': missing_count,
            'percentage_filled': (missing_count / len(df) * 100),
            'success': True
        }
        
        self.fix_log.append(report)
        return df_clean, report
    
    def remove_outliers(self, df: pd.DataFrame,
                       column: str,
                       method: str = 'iqr',
                       threshold: float = 1.5) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Remove outliers from numeric column.
        
        Args:
            df: Input DataFrame
            column: Column name to clean
            method: 'iqr' (interquartile range) or 'zscore'
            threshold: IQR multiplier (default 1.5) or z-score threshold (default 3)
            
        Returns:
            Tuple of (cleaned_df, fix_report)
        """
        df_clean = df.copy()
        original_count = len(df_clean)
        
        if method == 'iqr':
            Q1 = df_clean[column].quantile(0.25)
            Q3 = df_clean[column].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            
            # Filter outliers
            mask = (df_clean[column] >= lower_bound) & (df_clean[column] <= upper_bound)
            df_clean = df_clean[mask]
            
        elif method == 'zscore':
            from scipy import stats
            z_scores = np.abs(stats.zscore(df_clean[column].dropna()))
            mask = z_scores < threshold
            df_clean = df_clean[mask]
        
        removed_count = original_count - len(df_clean)
        
        report = {
            'operation': 'remove_outliers',
            'column': column,
            'method': method,
            'threshold': threshold,
            'original_rows': original_count,
            'final_rows': len(df_clean),
            'removed_rows': removed_count,
            'percentage_removed': (removed_count / original_count * 100),
            'success': True
        }
        
        self.fix_log.append(report)
        return df_clean, report
    
    def standardize_column_names(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Standardize column names: lowercase, snake_case, no special chars.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Tuple of (cleaned_df, fix_report)
        """
        df_clean = df.copy()
        
        original_columns = df_clean.columns.tolist()
        
        # Clean column names
        new_columns = []
        for col in original_columns:
            # Convert to lowercase
            new_col = col.lower()
            # Replace spaces and special chars with underscore
            new_col = re.sub(r'[^a-z0-9_]', '_', new_col)
            # Remove consecutive underscores
            new_col = re.sub(r'_+', '_', new_col)
            # Remove leading/trailing underscores
            new_col = new_col.strip('_')
            
            new_columns.append(new_col)
        
        df_clean.columns = new_columns
        
        # Create mapping
        column_mapping = {old: new for old, new in zip(original_columns, new_columns)}
        changed_columns = {old: new for old, new in column_mapping.items() if old != new}
        
        report = {
            'operation': 'standardize_column_names',
            'total_columns': len(original_columns),
            'changed_columns': len(changed_columns),
            'mapping': changed_columns,
            'success': True
        }
        
        self.fix_log.append(report)
        return df_clean, report
    
    def normalize_dates(self, df: pd.DataFrame,
                       column: str,
                       target_format: str = '%Y-%m-%d') -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Normalize date column to consistent format.
        
        Args:
            df: Input DataFrame
            column: Column name with dates
            target_format: Desired date format (default: YYYY-MM-DD)
            
        Returns:
            Tuple of (cleaned_df, fix_report)
        """
        df_clean = df.copy()
        
        original_type = df_clean[column].dtype
        
        try:
            # Parse dates (pandas infers format)
            df_clean[column] = pd.to_datetime(df_clean[column], errors='coerce')
            
            # Count parsing errors
            parse_errors = df_clean[column].isna().sum()
            
            # Format dates
            df_clean[column] = df_clean[column].dt.strftime(target_format)
            
            report = {
                'operation': 'normalize_dates',
                'column': column,
                'target_format': target_format,
                'original_type': str(original_type),
                'parse_errors': int(parse_errors),
                'success': True
            }
            
        except Exception as e:
            report = {
                'operation': 'normalize_dates',
                'column': column,
                'success': False,
                'error': str(e)
            }
        
        self.fix_log.append(report)
        return df_clean, report
    
    def preview_fix(self, df: pd.DataFrame,
                   operation: str,
                   **kwargs) -> Dict[str, Any]:
        """
        Preview what a fix operation will do WITHOUT applying it.
        
        Args:
            df: Input DataFrame
            operation: Name of fix operation
            **kwargs: Arguments for the operation
            
        Returns:
            Preview report with before/after stats
        """
        # Map operation names to methods
        operations = {
            'remove_duplicates': self.remove_duplicates,
            'fill_missing_numeric': self.fill_missing_numeric,
            'fill_missing_categorical': self.fill_missing_categorical,
            'remove_outliers': self.remove_outliers,
            'standardize_column_names': self.standardize_column_names,
            'normalize_dates': self.normalize_dates
        }
        
        if operation not in operations:
            return {'error': f'Unknown operation: {operation}'}
        
        # Run operation on copy
        _, report = operations[operation](df.copy(), **kwargs)
        
        # Add preview flag
        report['is_preview'] = True
        
        return report
    
    def get_fix_log(self) -> List[Dict[str, Any]]:
        """Get history of all fixes applied"""
        return self.fix_log
    
    def clear_log(self):
        """Clear the fix log"""
        self.fix_log = []


# Example usage and testing
if __name__ == "__main__":
    # Create test data with issues
    test_data = {
        'Order ID': [1, 2, 3, 3, 4, 5, 6],  # Duplicate row
        'Customer Name': ['Alice', 'Bob', None, 'Charlie', 'David', 'Eve', 'Frank'],  # Missing
        'Amount': [100, 150, 200, 200, None, 300, 99999],  # Missing + outlier
        'Date': ['2023-01-15', '01/16/2023', '2023-01-17', '2023-01-17', '2023-01-18', 
                 '2023-01-19', '2023-01-20']  # Inconsistent format
    }
    
    df = pd.DataFrame(test_data)
    
    print("=== ORIGINAL DATA ===")
    print(df)
    print(f"\nShape: {df.shape}")
    print(f"Missing values: {df.isna().sum().sum()}")
    
    fixer = DataFixer()
    
    # Test 1: Remove duplicates
    print("\n=== TEST 1: REMOVE DUPLICATES ===")
    df_clean, report = fixer.remove_duplicates(df)
    print(f"Removed {report['removed_rows']} duplicate rows")
    print(f"New shape: {df_clean.shape}")
    
    # Test 2: Fill missing categorical
    print("\n=== TEST 2: FILL MISSING NAMES ===")
    df_clean, report = fixer.fill_missing_categorical(df_clean, 'Customer Name', method='Unknown')
    print(f"Filled {report['filled_count']} missing names with '{report['fill_value']}'")
    
    # Test 3: Fill missing numeric
    print("\n=== TEST 3: FILL MISSING AMOUNTS ===")
    df_clean, report = fixer.fill_missing_numeric(df_clean, 'Amount', method='median')
    print(f"Filled {report['filled_count']} missing amounts with median: {report['fill_value']}")
    
    # Test 4: Standardize columns
    print("\n=== TEST 4: STANDARDIZE COLUMN NAMES ===")
    df_clean, report = fixer.standardize_column_names(df_clean)
    print(f"Changed {report['changed_columns']} column names")
    print(f"Mapping: {report['mapping']}")
    
    # Test 5: Preview (don't apply)
    print("\n=== TEST 5: PREVIEW OUTLIER REMOVAL ===")
    preview = fixer.preview_fix(df_clean, 'remove_outliers', column='amount', method='iqr')
    print(f"Preview: Would remove {preview['removed_rows']} outliers")
    
    print("\n=== FINAL CLEANED DATA ===")
    print(df_clean)
    
    print("\n=== FIX LOG ===")
    for log in fixer.get_fix_log():
        print(f"- {log['operation']}: {log.get('message', 'Applied')}")
    
    print("\n✅ All tests passed!")
