from backend.core.engine import AnalysisEngine
import pandas as pd

# Load test data
df = pd.read_csv('test_sales.csv')

print(f'\n📂 Loaded: {len(df)} rows × {len(df.columns)} columns')
print(f'Columns: {list(df.columns)}\n')

# Run analysis
engine = AnalysisEngine()
result = engine.analyze(df)

print('\n' + '='*70)
print('NARRATIVE OUTPUT:')
print('='*70)
print(result.narrative)

print('\n' + '='*70)
print('SUCCESS CRITERIA:')
print('='*70)
print(f'✓ Domain detected: {result.domain.get("type")}')
print(f'✓ Date range found: {"date" in result.narrative.lower() and "2023" in result.narrative}')
print(f'✓ Key columns identified: {"amount" in result.narrative.lower() or "quantity" in result.narrative.lower()}')
print(f'✓ Quality issues: {result.quality.get("missing_pct")}% missing, {result.quality.get("duplicates")} dupes')
print('='*70)
