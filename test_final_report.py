from backend.connectors.csv_handler import CSVHandler
from backend.data_processing.profiler import DataProfiler
from backend.export_engine.enhanced_quality_report import EnhancedQualityReportGenerator
from datetime import datetime

print("[1/3] Loading data...")
handler = CSVHandler()
df = handler.load_csv('sample_data/train.csv')
print(f"[OK] {len(df):,} rows loaded")

print("[2/3] Profiling...")
profiler = DataProfiler()
profile = profiler.profile_dataframe(df)
quality = profiler.get_quality_report()

print("[3/3] Generating COMPLETE report...")
generator = EnhancedQualityReportGenerator(profile, quality)
output_file = f"FINAL_COMPLETE_REPORT_{datetime.now().strftime('%H%M%S')}.html"
report_path = generator.generate_html(output_file, df=df)

print(f"\n[SUCCESS] Report: {output_file}")
print(f"[INFO] All sections should be included:")
print(f"  - Quality Score: {quality['score']}/100")
print(f"  - Domain: {generator.domain_result['primary_domain'].upper()} ({generator.domain_result['confidence']:.0%})")
print(f"  - Chart: Domain Confidence Scores (ALL 7 domains)")
print(f"  - Insights: {len(generator.insights)} findings")
print(f"  - Analytics: {len(df):,} rows analyzed")
