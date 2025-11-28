from backend.connectors.csv_handler import CSVHandler
from backend.data_processing.profiler import DataProfiler
from backend.export_engine.enhanced_quality_report import EnhancedQualityReportGenerator
from datetime import datetime

print("[LOAD] Loading data...")
handler = CSVHandler()
df = handler.load_csv('sample_data/train.csv')
print(f"[OK] {len(df):,} rows loaded")

print("[PROFILE] Profiling...")
profiler = DataProfiler()
profile = profiler.profile_dataframe(df)
quality = profiler.get_quality_report()

print("[GENERATE] Creating report with insights...")
generator = EnhancedQualityReportGenerator(profile, quality)
output_file = f"final_report_day3_{datetime.now().strftime('%H%M%S')}.html"
report_path = generator.generate_html(output_file, df=df)

print(f"[OK] Report: {output_file}")
print(f"[OK] Domain: {generator.domain_result['primary_domain'].upper()} ({generator.domain_result['confidence']:.0%})")
print(f"[OK] Insights generated: {len(generator.insights)}")

for i, insight in enumerate(generator.insights, 1):
    print(f"  {i}. {insight}")

print("\n[SUCCESS] Complete report generated!")
