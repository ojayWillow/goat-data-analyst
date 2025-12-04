import pandas as pd
import pytest
from pathlib import Path

# Test data directory
FIXTURES_DIR = Path(__file__).parent / 'fixtures'

@pytest.fixture
def clean_csv():
    """Clean CSV with valid data"""
    data = {
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, 28, 32],
        'salary': [50000, 60000, 75000, 55000, 65000],
        'department': ['Sales', 'Engineering', 'Marketing', 'Sales', 'Engineering']
    }
    return pd.DataFrame(data)

@pytest.fixture
def messy_csv():
    """CSV with data quality issues"""
    data = {
        'name': ['Alice', 'Bob', None, 'David', 'Eve', 'Bob'],  # Null + duplicate
        'age': [25, 30, 999, 28, 32, 30],  # Outlier
        'salary': [50000, 60000, -1000, 55000, None, 60000],  # Negative + null
        'department': ['Sales', 'Engineering', 'Marketing', '', 'Engineering', 'Engineering']  # Empty string
    }
    return pd.DataFrame(data)

@pytest.fixture
def empty_csv():
    """Empty CSV"""
    return pd.DataFrame()

@pytest.fixture
def large_csv():
    """Large CSV (10k rows)"""
    import numpy as np
    data = {
        'id': range(10000),
        'value': np.random.randn(10000),
        'category': np.random.choice(['A', 'B', 'C'], 10000)
    }
    return pd.DataFrame(data)
