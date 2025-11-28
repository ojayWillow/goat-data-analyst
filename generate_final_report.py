from backend.connectors.csv_handler import CSVHandler
from backend.data_processing.profiler import DataProfiler
from backend.export_engine.enhanced_quality_report import EnhancedQualityReportGenerator
from datetime import datetime

print("[1/3] Loading data...")
handler = CSVHandler()
df = handler.load_csv('sample_data/train.csv')
print(f"[OK] {len(df):,} rows")

print("[2/3] Profiling...")
profiler = DataProfiler()
profile = profiler.profile_dataframe(df)
quality = profiler.get_quality_report()

print("[3/3] Generating final report...")
generator = EnhancedQualityReportGenerator(profile, quality)
output_file = f"FINAL_REPORT_{datetime.now().strftime('%H%M%S')}.html"
generator.generate_html(output_file, df=df)

print(f"\n[SUCCESS] {output_file} created!")

# Verify all 7 sections
content = open(output_file).read()
sections = [
    "Overall Quality Score",
    "Domain Intelligence",
    "Domain Confidence Scores",
    "Detected Entities",
    "AI Insights",
    "Data Analytics",
    "Dataset Overview"
]

print("\n[VERIFY] Report sections:")
for section in sections:
    status = "[OK]" if section in content else "[MISSING]"
    print(f"  {status} {section}")
