import sys
sys.path.insert(0, '.')

import pandas as pd
import numpy as np
from backend.narrative.narrative_generator import NarrativeGenerator

print("\n" + "="*70)
print("DAY 9 TESTING: ACTION PLAN QUALITY CHECK")
print("="*70)

# Create test data with different domains
np.random.seed(42)

test_cases = [
    {
        'name': 'Sales Data',
        'domain': {'type': 'sales', 'confidence': 0.85},
        'df': pd.DataFrame({
            'transaction_id': range(100),
            'amount': np.random.uniform(10, 500, 100),
            'category': np.random.choice(['Electronics', 'Clothing', 'Food'], 100)
        })
    },
    {
        'name': 'Finance Data',
        'domain': {'type': 'finance', 'confidence': 0.75},
        'df': pd.DataFrame({
            'account_id': range(100),
            'revenue': np.random.uniform(1000, 50000, 100),
            'expense': np.random.uniform(500, 40000, 100)
        })
    }
]

gen = NarrativeGenerator()

for test in test_cases:
    print(f"\n{'='*70}")
    print(f"TEST: {test['name']}")
    print('='*70)
    
    df = test['df']
    # Add some issues
    df.iloc[::10, 1] = None  # 10% missing
    df = pd.concat([df, df.iloc[:5]], ignore_index=True)  # 5 dupes
    
    domain = test['domain']
    profile = {'rows': len(df), 'columns': len(df.columns)}
    quality = {
        'missing_pct': 10.0,
        'duplicates': 5,
        'overall_score': 85,
        'missing_by_column': df.isnull().sum().to_dict()
    }
    
    # Get pain points
    pain_points = gen._fallback_pain_points(quality, profile, df)
    
    print(f"\n📊 Pain Points Found: {len(pain_points)}")
    for p in pain_points:
        print(f"   [{p['severity'].upper()}] {p['issue']}")
    
    # Generate action plan
    action_plan = gen.generate_action_plan(
        domain=domain,
        quality=quality,
        analytics={},
        profile=profile,
        pain_points=pain_points
    )
    
    print(f"\n🎯 Action Plan Generated:")
    # Extract just the text from HTML
    import re
    steps = re.findall(r'<li>(.*?)</li>', action_plan, re.DOTALL)
    for i, step in enumerate(steps, 1):
        # Remove HTML tags
        clean_step = re.sub('<[^<]+?>', '', step).strip()
        print(f"   {i}. {clean_step}")

print("\n" + "="*70)
print("✅ ACTION PLAN QUALITY CHECK COMPLETE")
print("="*70)
