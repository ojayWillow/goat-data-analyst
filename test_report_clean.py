from backend.connectors.csv_handler import CSVHandler
from backend.data_processing.profiler import DataProfiler
from backend.export_engine.enhanced_quality_report import EnhancedQualityReportGenerator
from datetime import datetime

print("[LOAD] Loading train.csv...")
handler = CSVHandler()
df = handler.load_csv('sample_data/train.csv')
print(f"[OK] Loaded {len(df):,} rows x {len(df.columns)} columns")

print("[PROFILE] Profiling data...")
profiler = DataProfiler()
profile = profiler.profile_dataframe(df)
quality = profiler.get_quality_report()
print(f"[OK] Quality Score: {quality['score']}/100")

print("[GENERATE] Creating report...")
generator = EnhancedQualityReportGenerator(profile, quality)
output_file = f"enhanced_quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
report_path = generator.generate_html(output_file, df=df)

if generator.domain_result:
    domain = generator.domain_result['primary_domain']
    confidence = generator.domain_result['confidence']
    row_count = generator.domain_result.get('row_count', 0)
    
    print(f"[OK] Report saved: {output_file}")
    print(f"[INFO] Domain: {domain.upper()} ({confidence:.0%})")
    print(f"[INFO] Rows in domain_result: {row_count:,}")
    print(f"[SUCCESS] Report generated successfully!")
else:
    print("[WARNING] No domain detected")
