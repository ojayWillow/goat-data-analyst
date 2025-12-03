import sys
sys.path.insert(0, '.')

import pandas as pd
from backend.core.engine import AnalysisEngine

print("\n" + "="*70)
print("QUALITY DEBUG TEST")
print("="*70)

csv_path = "Sales Transaction v.4a.csv"  # or your big dataset with 5200 duplicates if different file
df = pd.read_csv(csv_path)

engine = AnalysisEngine()
result = engine.analyze(df)

print("\nRaw quality dict from engine:")
print(result.quality)

print("\nProfile overall (if available):")
profile_overall = None
try:
    profile_overall = result.profile.get('overall', result.profile)
except Exception:
    profile_overall = result.profile
print(profile_overall)

print("\nDone.")
print("="*70)
