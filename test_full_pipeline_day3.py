from backend.connectors.csv_handler import CSVHandler
from backend.data_processing.profiler import DataProfiler
from backend.export_engine.enhanced_quality_report import EnhancedQualityReportGenerator
from datetime import datetime

print("[LOAD] Loading train.csv...")
handler = CSVHandler()
df = handler.load_csv('sample_data/train.csv')
print(f"[OK] Loaded {len(df):,} rows")

print("[PROFILE] Profiling data...")
profiler = DataProfiler()
profile = profiler.profile_dataframe(df)
quality = profiler.get_quality_report()
print(f"[OK] Quality: {quality['score']}/100")

print("[GENERATE] Creating enhanced report...")
generator = EnhancedQualityReportGenerator(profile, quality)
output_file = f"enhanced_report_day3_{datetime.now().strftime('%H%M%S')}.html"
report_path = generator.generate_html(output_file, df=df)

print(f"[OK] Report saved: {output_file}")

if generator.domain_result:
    print(f"[OK] Domain: {generator.domain_result['primary_domain'].upper()} ({generator.domain_result['confidence']:.0%})")

if generator.analytics_result:
    summary = generator.analytics_result['summary']
    print(f"[OK] Analytics: {summary['rows']:,} rows, {summary['missing_percentage']:.1f}% missing")

print("\n[SUCCESS] Full pipeline working!")
