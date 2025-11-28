from backend.connectors.csv_handler import CSVHandler
from backend.analytics.insights_engine import InsightsEngine

print("[LOAD] Loading data...")
handler = CSVHandler()
df = handler.load_csv('sample_data/train.csv')
print(f"[OK] Loaded {len(df):,} rows")

print("[GENERATE] Generating insights...")
engine = InsightsEngine()
insights = engine.generate_insights(df, domain='e-commerce')

print(f"\n[INSIGHTS] Found {len(insights)} insights:\n")
for i, insight in enumerate(insights, 1):
    print(f"  {i}. {insight}")

print("\n[OK] Insights test passed!")
