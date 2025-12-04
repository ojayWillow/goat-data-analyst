import pytest
import pandas as pd
from backend.core.engine import AnalysisEngine

class TestAnalysisEngine:
    """Test AnalysisEngine with various inputs"""
    
    def test_analyze_clean_csv(self, clean_csv):
        """Test analysis with clean data"""
        engine = AnalysisEngine()
        result = engine.analyze(clean_csv)
        
        # Should return valid result
        assert result is not None
        assert result.report_html is not None
        assert len(result.report_html) > 1000  # Should be substantial HTML
        assert 'GOAT Data Analyst' in result.report_html
    
    def test_analyze_messy_csv(self, messy_csv):
        """Test analysis with messy data"""
        engine = AnalysisEngine()
        result = engine.analyze(messy_csv)
        
        # Should complete and generate report
        assert result is not None
        assert result.report_html is not None
        # Should detect quality issues
        assert 'quality' in result.report_html.lower() or 'issue' in result.report_html.lower()
    
    def test_analyze_empty_csv(self, empty_csv):
        """Test analysis with empty CSV - should handle gracefully"""
        engine = AnalysisEngine()
        result = engine.analyze(empty_csv)
        
        # Should complete without crashing (graceful handling)
        assert result is not None
        assert result.report_html is not None
    
    def test_analyze_large_csv(self, large_csv):
        """Test analysis with large CSV (10k rows)"""
        engine = AnalysisEngine()
        result = engine.analyze(large_csv)
        
        # Should complete without crashing
        assert result is not None
        assert result.report_html is not None
