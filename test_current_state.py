import sys
sys.path.insert(0, '.')

import pandas as pd
import numpy as np
from backend.narrative.narrative_generator import NarrativeGenerator

print("\n" + "="*70)
print("DAY 9: CURRENT ACTION PLAN TEST")
print("="*70)

gen = NarrativeGenerator()

# Test with messy data
np.random.seed(42)
df = pd.DataFrame({
    'transaction_id': range(100),
    'amount': np.random.uniform(10, 500, 100),
    'category': np.random.choice(['Electronics', 'Clothing', 'Food'], 100)
})
df.iloc[::10, 1] = None  # 10% missing
df = pd.concat([df, df.iloc[:5]], ignore_index=True)

domain = {'type': 'sales', 'confidence': 0.85}
profile = {'rows': len(df), 'columns': len(df.columns)}
quality = {
    'missing_pct': 10.0,
    'duplicates': 5,
    'overall_score': 85,
    'missing_by_column': df.isnull().sum().to_dict()
}

# Test with CURRENT signature (no pain_points parameter)
print("\n📊 Testing current generate_action_plan()...")

try:
    action_plan = gen.generate_action_plan(
        domain=domain,
        quality=quality,
        analytics={},
        profile=profile
    )
    print("✅ Success!")
    print("\n🎯 ACTION PLAN OUTPUT:")
    print(action_plan)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("CURRENT STATE ASSESSMENT:")
print("="*70)
print("The current version works but uses simple fallback.")
print("Day 9 polish: Add domain-aware steps and smarter sequencing.")
print("="*70)
