from backend.connectors.csv_handler import CSVHandler
from backend.data_processing.profiler import DataProfiler
from backend.export_engine.enhanced_quality_report import EnhancedQualityReportGenerator
from datetime import datetime

print("[1/3] Loading data...")
handler = CSVHandler()
df = handler.load_csv('sample_data/train.csv')
print(f"[OK] Loaded {len(df):,} rows")

print("[2/3] Profiling...")
profiler = DataProfiler()
profile = profiler.profile_dataframe(df)
quality = profiler.get_quality_report()

print("[3/3] Generating report...")
generator = EnhancedQualityReportGenerator(profile, quality)
output_file = f"COMPLETE_REPORT_{datetime.now().strftime('%H%M%S')}.html"
report_path = generator.generate_html(output_file, df=df)

print(f"\n[SUCCESS] Report generated: {output_file}")
print(f"\nReport Contents:")
print(f"  Quality Score: {quality['score']}/100")
print(f"  Domain: {generator.domain_result['primary_domain'].upper()} ({generator.domain_result['confidence']:.0%})")
print(f"  Insights: {len(generator.insights)} findings")
print(f"  Rows: {len(df):,}")
print(f"  Columns: {len(df.columns)}")

print(f"\n[AI Insights Generated:]")
for i, insight in enumerate(generator.insights, 1):
    print(f"  {i}. {insight}")
