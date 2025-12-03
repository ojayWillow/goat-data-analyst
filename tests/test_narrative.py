import sys
sys.path.insert(0, '.')

import pandas as pd
import numpy as np
from backend.core.engine import AnalysisEngine

print("\n" + "="*70)
print("TESTING DAY 8-9: NARRATIVE WITH ACTION PLAN")
print("="*70)

# Create messy test data
np.random.seed(42)
dates = pd.date_range('2023-06-01', periods=100, freq='D')
amount = np.random.uniform(10, 500, 100)
amount[::10] = None  # 10% missing

df = pd.DataFrame({
    'transaction_id': range(100),
    'date': dates,
    'amount': amount,
    'category': np.random.choice(['Electronics', 'Clothing', 'Food'], 100),
    'customer_id': np.random.randint(1, 50, 100)
})

# Add duplicates
df = pd.concat([df, df.iloc[:5]], ignore_index=True)

print(f"\n📊 Test Data: {len(df)} rows, {df.isnull().sum().sum()} missing values, 5 duplicates")

# Run analysis
engine = AnalysisEngine()
result = engine.analyze(df)

print(f"\n✅ Analysis Complete:")
print(f"   - Execution time: {result.execution_time_seconds:.2f}s")
print(f"   - Quality score: {result.quality.get('overall_score', 0):.0f}/100")
print(f"   - Narrative length: {len(result.narrative)} chars")

# Check narrative sections
if "I See You" in result.narrative:
    print("   ✅ Context section present")
if "What Hurts" in result.narrative:
    print("   ✅ Pain points section present")
if "Your Path Forward" in result.narrative:
    print("   ✅ Action plan section present")

print("\n" + "="*70)
print("NARRATIVE OUTPUT:")
print("="*70)
# Print first 1000 chars of narrative
print(result.narrative[:1000] + "..." if len(result.narrative) > 1000 else result.narrative)

print("\n" + "="*70)
print("✅ TEST COMPLETE")
print("="*70)
