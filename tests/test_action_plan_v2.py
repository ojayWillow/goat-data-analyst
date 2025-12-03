import sys
sys.path.insert(0, '.')

import pandas as pd
import numpy as np
from backend.narrative.narrative_generator import NarrativeGenerator

print("\n" + "="*70)
print("DAY 9: ACTION PLAN OUTPUT TEST")
print("="*70)

gen = NarrativeGenerator()

# Test with sales data
print("\n" + "="*70)
print("TEST 1: Sales Data with Issues")
print("="*70)

np.random.seed(42)
df = pd.DataFrame({
    'transaction_id': range(100),
    'amount': np.random.uniform(10, 500, 100),
    'category': np.random.choice(['Electronics', 'Clothing', 'Food'], 100)
})
df.iloc[::10, 1] = None  # 10% missing
df = pd.concat([df, df.iloc[:5]], ignore_index=True)  # Duplicates

domain = {'type': 'sales', 'confidence': 0.85}
profile = {'rows': len(df), 'columns': len(df.columns)}
quality = {
    'missing_pct': 10.0,
    'duplicates': 5,
    'overall_score': 85,
    'missing_by_column': df.isnull().sum().to_dict()
}

# Generate action plan directly
action_plan_html = gen.generate_action_plan(
    domain=domain,
    quality=quality,
    analytics={},
    profile=profile,
    pain_points=None  # Will use fallback
)

print("\n🎯 ACTION PLAN OUTPUT:")
print(action_plan_html)

print("\n" + "="*70)
print("TEST 2: Clean Data (No Issues)")
print("="*70)

df_clean = pd.DataFrame({
    'id': range(100),
    'value': range(100)
})

quality_clean = {
    'missing_pct': 0,
    'duplicates': 0,
    'overall_score': 100,
    'missing_by_column': {}
}

action_plan_clean = gen.generate_action_plan(
    domain={'type': 'finance', 'confidence': 0.9},
    quality=quality_clean,
    analytics={},
    profile={'rows': 100, 'columns': 2},
    pain_points=None
)

print("\n🎯 ACTION PLAN FOR CLEAN DATA:")
print(action_plan_clean)

print("\n" + "="*70)
print("✅ TEST COMPLETE")
print("="*70)
