from backend.connectors.csv_handler import CSVHandler
from backend.data_processing.profiler import DataProfiler
from backend.export_engine.quality_report import QualityReportGenerator
from datetime import datetime

print("[1/3] Loading data...")
handler = CSVHandler()
df = handler.load_csv('sample_data/train.csv')
print(f"[OK] {len(df):,} rows")

print("[2/3] Profiling...")
profiler = DataProfiler()
profile = profiler.profile_dataframe(df)
quality = profiler.get_quality_report()

print("[3/3] Generating report with ORIGINAL generator...")
generator = QualityReportGenerator(profile, quality)
output_file = f"ORIGINAL_REPORT_{datetime.now().strftime('%H%M%S')}.html"
report_path = generator.generate_html(output_file)

print(f"\n[SUCCESS] {output_file}")
print(f"[INFO] Using original QualityReportGenerator")
