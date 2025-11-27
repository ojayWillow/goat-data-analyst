"""
Quick data profiling - understand your datasets
"""

from backend.connectors.csv_handler import CSVHandler
import pandas as pd

files = [
    "20251126_170320_spotify_data_clean.csv",
    "20251127_084222_customers_50k.csv", 
    "test.csv",
    "train.csv"
]

print("="*80)
print("📊 DATASET PROFILES")
print("="*80)

for filename in files:
    print(f"\n{'='*80}")
    print(f"📁 {filename}")
    print('='*80)
    
    handler = CSVHandler()
    df = handler.load_csv(f"sample_data/{filename}")
    
    print(f"\n📏 Size: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"💾 Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    print(f"\n📋 Columns:")
    for col in df.columns:
        dtype = df[col].dtype
        unique = df[col].nunique()
        missing = df[col].isnull().sum()
        missing_pct = (missing / len(df)) * 100
        
        print(f"  • {col}")
        print(f"    Type: {dtype}, Unique: {unique:,}, Missing: {missing} ({missing_pct:.1f}%)")
    
    print(f"\n🔍 Sample Data:")
    print(df.head(2).to_string())
    
    print(f"\n")

print("="*80)
print("✅ PROFILING COMPLETE")
print("="*80)
