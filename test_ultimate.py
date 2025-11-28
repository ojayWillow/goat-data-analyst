from backend.connectors.csv_handler import CSVHandler
from backend.data_processing.profiler import DataProfiler
from backend.export_engine.ultimate_report import UltimateReportGenerator
from datetime import datetime

print("[1/4] Loading...")
handler = CSVHandler()
df = handler.load_csv('sample_data/train.csv')
print(f"[OK] {len(df):,} rows")

print("[2/4] Profiling...")
profiler = DataProfiler()
profile = profiler.profile_dataframe(df)
quality = profiler.get_quality_report()

print("[3/4] Generating ULTIMATE...")
generator = UltimateReportGenerator(profile, quality, df=df)
html = generator.generate_html()

output = f"ULTIMATE_REPORT_{datetime.now().strftime('%H%M%S')}.html"
with open(output, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"[OK] {output}")
print(f"[SIZE] {len(html):,} chars")

has_domain = "Domain Intelligence" in html
has_insights = "AI Insights" in html
has_analytics = "Data Analytics" in html
has_original = "Dataset Summary" in html

print("\n[SECTIONS]:")
print(f"  {'✓' if has_original else '✗'} Original (Dataset Summary)")
print(f"  {'✓' if has_domain else '✗'} Domain Intelligence")
print(f"  {'✓' if has_insights else '✗'} AI Insights")
print(f"  {'✓' if has_analytics else '✗'} Data Analytics")

if all([has_original, has_domain, has_insights, has_analytics]):
    print("\n[SUCCESS] 🎉 ULTIMATE REPORT COMPLETE!")
