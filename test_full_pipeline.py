import sys
sys.path.insert(0, '.')

import pandas as pd
import numpy as np
from backend.core.engine import AnalysisEngine

# Create MESSY sales data
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
df = pd.concat([df, df.iloc[:5]], ignore_index=True)  # Add duplicates

print(f"📊 Test data: {len(df)} rows, {df.isnull().sum().sum()} missing, 5 duplicates")

# Run FULL analysis
engine = AnalysisEngine()
result = engine.analyze(df)

# Save report
with open('full_test_report.html', 'w', encoding='utf-8') as f:
    f.write(result.report_html)

print(f"\n✅ Full report saved to full_test_report.html")
print(f"   Narrative length: {len(result.narrative)} chars")
print(f"   Report length: {len(result.report_html)} chars")
