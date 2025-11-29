import time
import pandas as pd
from pathlib import Path
from backend.connectors.csv_handler import CSVHandler
from backend.data_processing.profiler import DataProfiler
from backend.domain_detection.domain_detector import DomainDetector
from backend.analytics.simple_analytics import SimpleAnalytics
from backend.analytics.ai_insights import AIInsightsEngine


def test_pipeline(csv_file):
    """Test full pipeline on a CSV file and measure performance."""
    print(f"\n{'='*60}")
    print(f"Testing: {csv_file}")
    print(f"{'='*60}")
    
    start = time.time()
    
    # Load
    handler = CSVHandler()
    df = handler.load_csv(csv_file)
    load_time = time.time() - start
    print(f"✅ Load: {load_time:.2f}s ({len(df)} rows, {len(df.columns)} cols)")
    
    # Profile
    start = time.time()
    profiler = DataProfiler()
    profile = profiler.profile_dataframe(df)
    profile_time = time.time() - start
    print(f"✅ Profile: {profile_time:.2f}s")
    
    # Domain detect
    start = time.time()
    detector = DomainDetector()
    domain = detector.detect_domain(df)
    domain_time = time.time() - start
    print(f"✅ Domain: {domain_time:.2f}s -> {domain['primary_domain']} ({domain['confidence']:.1%})")
    
    # Analytics
    start = time.time()
    analytics = SimpleAnalytics()
    analytics_summary = analytics.analyze_dataset(df)
    analytics_time = time.time() - start
    print(f"✅ Analytics: {analytics_time:.2f}s")
    
    # AI Insights
    start = time.time()
    ai_engine = AIInsightsEngine()
    ai_results = ai_engine.generate_insights(df, domain, analytics_summary)
    ai_time = time.time() - start
    print(f"✅ AI Insights: {ai_time:.2f}s ({len(ai_results['ai_insights'])} insights)")
    
    total_time = load_time + profile_time + domain_time + analytics_time + ai_time
    print(f"\n📊 TOTAL: {total_time:.2f}s")
    
    return {
        'file': csv_file,
        'rows': len(df),
        'cols': len(df.columns),
        'load_time': load_time,
        'profile_time': profile_time,
        'domain_time': domain_time,
        'domain': domain['primary_domain'],
        'confidence': domain['confidence'],
        'analytics_time': analytics_time,
        'ai_time': ai_time,
        'total_time': total_time,
    }


# Test all CSVs in sample_data/test
results = []
base_dir = Path('sample_data') / 'test'
csv_files = list(base_dir.glob('*.csv'))

for csv_file in csv_files[:5]:  # Test first 5 files in test folder
    try:
        result = test_pipeline(str(csv_file))
        results.append(result)
    except Exception as e:
        print(f"❌ ERROR: {e}")

# Summary table
print(f"\n{'='*60}")
print("PERFORMANCE SUMMARY")
print(f"{'='*60}")
for r in results:
    print(f"{r['file']:50} | {r['rows']:6} rows | {r['total_time']:6.2f}s | {r['domain']:15} ({r['confidence']:.0%})")
