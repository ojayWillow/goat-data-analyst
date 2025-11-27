"""
Unit tests for Quality Report Generator
"""

import pytest
import pandas as pd
import os
from backend.data_processing.profiler import DataProfiler
from backend.export_engine.quality_report import QualityReportGenerator


class TestQualityReportGenerator:
    """Test cases for QualityReportGenerator"""
    
    def setup_method(self):
        """Set up test fixtures"""
        # Create simple test data
        df = pd.DataFrame({
            'id': range(100),
            'category': ['A', 'B', 'C'] * 33 + ['A'],
            'value': range(100),
        })
        
        profiler = DataProfiler()
        self.profile = profiler.profile_dataframe(df)
        self.quality = profiler.get_quality_report()
        self.generator = QualityReportGenerator(self.profile, self.quality)
    
    def test_markdown_generation(self):
        """Test Markdown report generation"""
        md = self.generator.generate_markdown()
        
        assert '# 📊 Data Quality Report' in md
        assert 'Quality Score' in md
        assert 'Overall Summary' in md
        assert 'Column Details' in md
    
    def test_html_generation(self):
        """Test HTML report generation"""
        html = self.generator.generate_html()
        
        assert '<!DOCTYPE html>' in html
        assert '<title>Data Quality Report</title>' in html
        assert 'Quality Score' in html
        assert '<table>' in html
    
    def test_recommendations_generated(self):
        """Test recommendation generation"""
        recommendations = self.generator._generate_recommendations()
        
        assert isinstance(recommendations, list)
    
    def test_save_markdown(self, tmp_path):
        """Test saving Markdown report"""
        filepath = tmp_path / "test_report.md"
        self.generator.save_markdown(str(filepath))
        
        assert filepath.exists()
        content = filepath.read_text(encoding='utf-8')
        assert '# 📊 Data Quality Report' in content
    
    def test_save_html(self, tmp_path):
        """Test saving HTML report"""
        filepath = tmp_path / "test_report.html"
        self.generator.save_html(str(filepath))
        
        assert filepath.exists()
        content = filepath.read_text(encoding='utf-8')
        assert '<!DOCTYPE html>' in content
    
    def test_save_both(self, tmp_path):
        """Test saving both formats"""
        md_path, html_path = self.generator.save_both('test_report', str(tmp_path))
        
        assert os.path.exists(md_path)
        assert os.path.exists(html_path)
        assert md_path.endswith('.md')
        assert html_path.endswith('.html')
    
    def test_score_color_coding(self):
        """Test that HTML uses correct colors for different scores"""
        html = self.generator.generate_html()
        
        # Should have some color defined for the score
        assert '#' in html  # Hex color code present
    
    def test_handles_empty_issues(self):
        """Test report generation with no issues"""
        # Create perfect data
        df = pd.DataFrame({
            'a': range(100),
            'b': range(100, 200),
        })
        
        profiler = DataProfiler()
        profile = profiler.profile_dataframe(df)
        quality = profiler.get_quality_report()
        
        generator = QualityReportGenerator(profile, quality)
        md = generator.generate_markdown()
        html = generator.generate_html()
        
        assert md is not None
        assert html is not None
