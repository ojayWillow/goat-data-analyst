import sys
sys.path.insert(0, '.')

import pandas as pd
from backend.core.engine import AnalysisEngine

print("\n" + "="*70)
print("GOAT TEST: amazon.csv FULL PIPELINE")
print("="*70)

csv_path = "amazon.csv"
try:
    df = pd.read_csv(csv_path)
except Exception as e:
    print(f"❌ Failed to load {csv_path}: {e}")
    raise SystemExit(1)

print(f"📄 Loaded {csv_path}: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Columns: {list(df.columns)}")

engine = AnalysisEngine()
result = engine.analyze(df)

print("\n✅ Analysis complete")
print(f"- Domain detected: {result.domain}")
print(f"- Quality score: {result.quality.get('overall_score')}")
print(f"- Narrative length: {len(result.narrative)} chars")
print(f"- Report HTML length: {len(result.report_html)} chars")

out_path = "amazon_report.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(result.report_html)

print(f"\n📄 Report saved to {out_path}")
print("="*70)
print("✅ DONE")
print("="*70)
