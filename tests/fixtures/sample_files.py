"""
CSV test fixtures for pytest
"""
import pandas as pd
from pathlib import Path

SAMPLE_DATA_DIR = Path(__file__).parent.parent.parent / 'sample_data'

def get_sample_csv(filename):
    """Load a sample CSV file"""
    filepath = SAMPLE_DATA_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f'Sample file not found: {filename}')
    return pd.read_csv(filepath)

# Small files (< 100KB) - fast tests
CLEAN_SMALL = 'demo_clean.csv'
MESSY_SMALL = 'demo_messy.csv'
MEDIUM_SMALL = 'demo_medium.csv'

# Medium files (100KB - 5MB) - normal tests
ECOMMERCE = 'messy_ecommerce.csv'
NBA_STATS = 'nba_player_stats.csv'
STUDENTS = 'StudentsPerformance.csv'
COUNTRIES = 'countries.csv'

# Large files (> 5MB) - performance tests
AMAZON = 'amazon.csv'  # 4.6MB, 1466 rows
SPOTIFY = '20251126_170320_spotify_data_clean.csv'  # 1.4MB, 8583 rows
CUSTOMERS_50K = '20251127_084222_customers_50k.csv'  # 4.7MB, 50k rows

# Very large (> 10MB) - stress tests
FIFA = 'fifa21_raw_data.csv'  # 8.5MB, 94k rows
COVID = 'covid_19_data.csv'  # 22MB, 306k rows
TRAIN = 'train.csv'  # 25MB, 550k rows
TRANSACTIONS = 'transactions.csv'  # 25MB, 300k rows
