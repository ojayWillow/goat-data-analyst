import pandas as pd
from backend.core.engine import AnalysisEngine

# Create test data
df = pd.DataFrame({
    'product': ['A', 'B', 'C', 'A', 'B'],
    'sales': [100, 200, 150, 120, 180],
    'region': ['East', 'West', 'East', 'West', 'East']
})

# Run analysis
engine = AnalysisEngine()
result = engine.analyze(df)

# Check charts
print(f'Charts generated: {len(result.charts)}')
print(f'Chart IDs: {list(result.charts.keys())}')

# Check if charts have HTML
for chart_id, html in result.charts.items():
    print(f'{chart_id}: {len(html)} chars')
    has_plotly = 'plotly' in html.lower()
    print(f'Contains plotly: {has_plotly}')
