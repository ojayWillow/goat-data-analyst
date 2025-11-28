from backend.connectors.csv_handler import CSVHandler
from backend.analytics.simple_analytics import SimpleAnalytics
import json

print("[LOAD] Loading train.csv...")
handler = CSVHandler()
df = handler.load_csv('sample_data/train.csv')
print(f"[OK] Loaded {len(df):,} rows x {len(df.columns)} columns")

print("[ANALYZE] Running analytics...")
analyzer = SimpleAnalytics()
results = analyzer.analyze_dataset(df)

print("\n[RESULTS] Analysis Complete:")
print(f"[INFO] Summary: {len(results['summary'])} metrics")
print(f"[INFO] Numeric columns: {len(results['numeric_analysis'])}")
print(f"[INFO] Categorical columns: {len(results['categorical_analysis'])}")

# Show some specific results
summary = results['summary']
print(f"\n[SUMMARY] Dataset Statistics:")
print(f"  Rows: {summary['rows']:,}")
print(f"  Columns: {summary['columns']}")
print(f"  Missing data: {summary['missing_percentage']:.2f}%")
print(f"  Duplicate rows: {summary['duplicate_rows']}")

# Show numeric column analysis
if results['numeric_analysis']:
    print(f"\n[NUMERIC ANALYSIS] Example column:")
    first_numeric = list(results['numeric_analysis'].items())[0]
    col_name, col_stats = first_numeric
    print(f"  Column: {col_name}")
    print(f"  Mean: {col_stats['mean']:.2f}")
    print(f"  Min: {col_stats['min']:.2f}")
    print(f"  Max: {col_stats['max']:.2f}")

# Show categorical analysis
if results['categorical_analysis']:
    print(f"\n[CATEGORICAL ANALYSIS] Example column:")
    first_cat = list(results['categorical_analysis'].items())[0]
    col_name, col_stats = first_cat
    print(f"  Column: {col_name}")
    print(f"  Unique values: {col_stats['unique_count']}")
    print(f"  Top value: {col_stats['most_common']}")

print("\n[OK] Analytics test passed!")
