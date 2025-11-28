from backend.connectors.csv_handler import CSVHandler
from backend.data_processing.profiler import DataProfiler
from backend.export_engine.ultimate_report import UltimateReportGenerator
from datetime import datetime

print('[1/3] Loading data...')
handler = CSVHandler()
df = handler.load_csv('sample_data/train.csv')
print(f'[OK] {len(df):,} rows')

print('[2/3] Profiling...')
profiler = DataProfiler()
profile = profiler.profile_dataframe(df)
quality = profiler.get_quality_report()

print('[3/3] Generating ultimate report...')
generator = UltimateReportGenerator(profile, quality, df)
output_file = f'ULTIMATE_REPORT_{datetime.now().strftime('%H%M%S')}.html'
html = generator.generate_html()
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\n✅ SUCCESS: {output_file} created!')
