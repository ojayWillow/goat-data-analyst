"""
Unit tests for CSV Handler
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
import os

from backend.connectors.csv_handler import CSVHandler, load_csv


class TestCSVHandler:
    """Test cases for CSVHandler class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.handler = CSVHandler()
        self.temp_dir = tempfile.mkdtemp()
    
    def create_test_csv(self, filename: str, content: str, encoding: str = 'utf-8') -> str:
        """Helper to create test CSV files"""
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, 'w', encoding=encoding) as f:
            f.write(content)
        return filepath
    
    def test_load_simple_csv(self):
        """Test loading a simple CSV file"""
        content = "name,age,city\nAlice,30,NYC\nBob,25,LA\n"
        filepath = self.create_test_csv("simple.csv", content)
        
        df = self.handler.load_csv(filepath)
        
        assert df.shape == (2, 3)
        assert list(df.columns) == ['name', 'age', 'city']
        assert df['name'].tolist() == ['Alice', 'Bob']
    
    def test_load_semicolon_delimiter(self):
        """Test loading CSV with semicolon delimiter"""
        content = "name;age;city\nAlice;30;NYC\nBob;25;LA\n"
        filepath = self.create_test_csv("semicolon.csv", content)
        
        df = self.handler.load_csv(filepath)
        
        assert df.shape == (2, 3)
        assert list(df.columns) == ['name', 'age', 'city']
    
    def test_load_tab_delimiter(self):
        """Test loading CSV with tab delimiter"""
        content = "name\tage\tcity\nAlice\t30\tNYC\nBob\t25\tLA\n"
        filepath = self.create_test_csv("tab.csv", content)
        
        df = self.handler.load_csv(filepath)
        
        assert df.shape == (2, 3)
        assert list(df.columns) == ['name', 'age', 'city']
    
    def test_metadata_stored(self):
        """Test that metadata is stored correctly"""
        content = "name,age\nAlice,30\n"
        filepath = self.create_test_csv("meta.csv", content)
        
        df = self.handler.load_csv(filepath)
        metadata = self.handler.get_metadata()
        
        assert metadata['rows'] == 1
        assert metadata['columns'] == 2
        assert 'encoding' in metadata
        assert 'delimiter' in metadata
    
    def test_convenience_function(self):
        """Test the convenience load_csv function"""
        content = "name,age\nAlice,30\n"
        filepath = self.create_test_csv("convenience.csv", content)
        
        df = load_csv(filepath)
        
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (1, 2)
