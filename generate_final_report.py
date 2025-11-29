from backend.connectors.csv_handler import CSVHandler
from backend.data_processing.profiler import DataProfiler
from backend.export_engine.ultimate_report import UltimateReportGenerator
from backend.analytics.simple_analytics import SimpleAnalytics
from backend.analytics.ai_insights import AIInsightsEngine
from backend.domain_detection.domain_detector import DomainDetector
from datetime import datetime

print('[1/5] Loading data...')
handler = CSVHandler()
import sys
csv_file = sys.argv[1] if len(sys.argv) > 1 else 'sample_data/amazon.csv'
df = handler.load_csv(csv_file)
print(f'[OK] {len(df):,} rows')

print('[2/5] Profiling...')
profiler = DataProfiler()
profile = profiler.profile_dataframe(df)
quality = profiler.get_quality_report()

print('[3/5] Detecting domain...')
detector = DomainDetector()
domain = detector.detect_domain(df)
print(f'[OK] Domain: {domain}')

print('[4/5] Running analytics + AI insights...')
analytics = SimpleAnalytics()
analytics_summary = analytics.analyze_dataset(df)

ai_engine = AIInsightsEngine()
ai_results = ai_engine.generate_insights(df, domain, analytics_summary)
print(f'[OK] Generated {len(ai_results["ai_insights"])} AI insights')

print('[5/5] Generating ultimate report...')
generator = UltimateReportGenerator(profile, quality, df)
generator.domain = domain
generator.analytics_summary = analytics_summary
generator.ai_insights = ai_results['ai_insights']

output_file = f'ULTIMATE_REPORT_{datetime.now().strftime("%H%M%S")}.html'
html = generator.generate_html()
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\n✅ SUCCESS: {output_file} created with AI insights!')
