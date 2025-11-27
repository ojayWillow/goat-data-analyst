"""
Unit tests for Data Profiler
"""

import pytest
import pandas as pd
import numpy as np
from backend.data_processing.profiler import DataProfiler, profile_dataframe


class TestDataProfiler:
    """Test cases for DataProfiler class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.profiler = DataProfiler()
    
    def test_detect_numeric_type(self):
        """Test detection of numeric columns"""
        series = pd.Series([1, 2, 3, 4, 5], name='test_col')
        col_type = self.profiler.detect_column_type(series)
        assert col_type == 'numeric'
    
    def test_detect_categorical_type(self):
        """Test detection of categorical columns"""
        series = pd.Series(['A', 'B', 'A', 'C', 'B'] * 20, name='category')
        col_type = self.profiler.detect_column_type(series)
        assert col_type == 'categorical'
    
    def test_detect_boolean_type(self):
        """Test detection of boolean columns"""
        series = pd.Series([True, False, True, False, True], name='flag')
        col_type = self.profiler.detect_column_type(series)
        assert col_type == 'boolean'
    
    def test_detect_id_type(self):
        """Test detection of ID columns"""
        series = pd.Series([f'ID_{i}' for i in range(1000)], name='customer_id')
        col_type = self.profiler.detect_column_type(series)
        assert col_type == 'id'
    
    def test_detect_datetime_type(self):
        """Test detection of datetime columns"""
        series = pd.Series(pd.date_range('2024-01-01', periods=100), name='date')
        col_type = self.profiler.detect_column_type(series)
        assert col_type == 'datetime'
    
    def test_detect_text_type(self):
        """Test detection of text columns"""
        # Create truly unique long text strings
        series = pd.Series([
            f'This is a unique long text description with many words number {i} and lots of content'
            for i in range(100)
        ], name='description')
        col_type = self.profiler.detect_column_type(series)
        assert col_type == 'text'
    
    def test_profile_numeric_column(self):
        """Test profiling of numeric column"""
        series = pd.Series([1, 2, 3, 4, 5, 100], name='values')  # 100 is outlier
        profile = self.profiler.profile_column(series)
        
        assert profile['name'] == 'values'
        assert profile['type'] == 'numeric'
        assert profile['count'] == 6
        assert profile['missing'] == 0
        assert 'mean' in profile
        assert 'median' in profile
        assert 'std' in profile
        assert 'outliers' in profile
    
    def test_profile_categorical_column(self):
        """Test profiling of categorical column"""
        series = pd.Series(['A', 'B', 'A', 'C', 'B', 'A'] * 10, name='category')
        profile = self.profiler.profile_column(series)
        
        assert profile['name'] == 'category'
        assert profile['type'] == 'categorical'
        assert 'top_values' in profile
        assert 'most_common' in profile
    
    def test_profile_with_missing_data(self):
        """Test profiling handles missing data correctly"""
        series = pd.Series([1, 2, np.nan, 4, np.nan, 6], name='values')
        profile = self.profiler.profile_column(series)
        
        assert profile['missing'] == 2
        assert profile['missing_pct'] == pytest.approx(33.33, rel=0.1)
        assert 'MODERATE_MISSING_DATA' in profile['quality_issues']
    
    def test_profile_with_high_missing_data(self):
        """Test detection of high missing data"""
        series = pd.Series([1, np.nan, np.nan, np.nan, np.nan, np.nan], name='values')
        profile = self.profiler.profile_column(series)
        
        assert profile['missing_pct'] > 50
        assert 'HIGH_MISSING_DATA' in profile['quality_issues']
    
    def test_profile_constant_column(self):
        """Test detection of constant columns"""
        series = pd.Series([5, 5, 5, 5, 5], name='constant')
        profile = self.profiler.profile_column(series)
        
        assert profile['unique'] == 1
        assert 'CONSTANT_VALUE' in profile['quality_issues']
    
    def test_profile_dataframe(self):
        """Test profiling entire dataframe"""
        df = pd.DataFrame({
            'id': range(100),
            'category': ['A', 'B', 'C'] * 33 + ['A'],
            'value': np.random.randn(100),
            'flag': [True, False] * 50,
        })
        
        profile = self.profiler.profile_dataframe(df)
        
        assert 'overall' in profile
        assert 'columns' in profile
        assert 'type_summary' in profile
        assert profile['overall']['rows'] == 100
        assert profile['overall']['columns'] == 4
        assert len(profile['columns']) == 4
    
    def test_quality_report(self):
        """Test quality report generation"""
        df = pd.DataFrame({
            'good_col': range(100),
            'missing_col': [1, np.nan] * 50,
            'constant_col': [5] * 100,
        })
        
        self.profiler.profile_dataframe(df)
        quality = self.profiler.get_quality_report()
        
        assert 'status' in quality
        assert 'issues' in quality
        assert 'warnings' in quality
        assert 'score' in quality
        assert isinstance(quality['score'], (int, float))
    
    def test_high_cardinality_detection(self):
        """Test detection of high cardinality categorical columns"""
        series = pd.Series([f'value_{i}' for i in range(150)], name='high_card')
        profile = self.profiler.profile_column(series)
        
        assert 'HIGH_CARDINALITY' in profile['quality_issues']
    
    def test_outlier_detection(self):
        """Test outlier detection in numeric columns"""
        # Normal data with clear outliers
        normal_data = list(range(1, 100))
        outliers = [1000, 2000, 3000]
        series = pd.Series(normal_data + outliers, name='with_outliers')
        
        profile = self.profiler.profile_column(series)
        
        assert profile['outliers'] > 0
    
    def test_convenience_function(self):
        """Test convenience profile_dataframe function"""
        df = pd.DataFrame({
            'a': range(10),
            'b': ['x', 'y'] * 5,
        })
        
        profile = profile_dataframe(df)
        
        assert profile is not None
        assert 'overall' in profile
        assert profile['overall']['rows'] == 10
    
    def test_empty_dataframe(self):
        """Test profiling empty dataframe"""
        df = pd.DataFrame()
        profile = self.profiler.profile_dataframe(df)
        
        assert profile['overall']['rows'] == 0
        assert profile['overall']['columns'] == 0
    
    def test_single_row_dataframe(self):
        """Test profiling dataframe with single row"""
        df = pd.DataFrame({'a': [1], 'b': ['x']})
        profile = self.profiler.profile_dataframe(df)
        
        assert profile['overall']['rows'] == 1
        assert len(profile['columns']) == 2
    
    def test_memory_calculation(self):
        """Test memory usage calculation"""
        df = pd.DataFrame({
            'a': range(1000),
            'b': ['test'] * 1000,
        })
        
        profile = self.profiler.profile_dataframe(df)
        
        assert profile['overall']['memory_mb'] > 0
        assert isinstance(profile['overall']['memory_mb'], float)
