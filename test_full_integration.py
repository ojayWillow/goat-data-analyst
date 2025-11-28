"""
Full integration test: CSV → Profile → Domain Detection → Quality Report
"""

from backend.connectors.csv_handler import CSVHandler
from backend.data_processing.profiler import DataProfiler
from backend.domain_detection.domain_detector import DomainDetector

print("=" * 70)
print("🎯 FULL INTEGRATION TEST - Day 2")
print("=" * 70)

# Step 1: Load Data
print("\n📂 Step 1: Loading data...")
handler = CSVHandler()
df = handler.load_csv('sample_data/train.csv')
print(f"   ✅ Loaded {len(df):,} rows × {len(df.columns)} columns")

# Step 2: Profile Data
print("\n📊 Step 2: Profiling data...")
profiler = DataProfiler()
profile = profiler.profile_dataframe(df)
quality = profiler.get_quality_report()
print(f"   ✅ Quality Score: {quality['score']}/100")
print(f"   ✅ Profile contains {len(profile['columns'])} column analyses")

# Step 3: Detect Domain
print("\n🔍 Step 3: Detecting domain...")
detector = DomainDetector()
domain_result = detector.detect_domain(df)
print(f"   ✅ Detected: {domain_result['primary_domain'].upper()}")
print(f"   ✅ Confidence: {domain_result['confidence']:.1%}")
print(f"   ✅ Entities found: {len(domain_result['detected_entities'])}")

# Step 4: Show Combined Results
print("\n" + "=" * 70)
print("📋 COMBINED ANALYSIS RESULTS")
print("=" * 70)

print(f"\n🎯 Domain: {domain_result['primary_domain'].upper()} ({domain_result['confidence']:.0%} confidence)")
print(f"⭐ Quality Score: {quality['score']}/100")
print(f"📊 Dataset: {len(df):,} rows × {len(df.columns)} columns")

print(f"\n💡 Top Domain-Specific Recommendations:")
for i, rec in enumerate(domain_result['recommendations'][:3], 1):
    print(f"   {i}. {rec}")

print(f"\n⚠️ Top Quality Issues:")
for i, issue in enumerate(quality['issues'][:3], 1):
    print(f"   {i}. {issue}")

print("\n" + "=" * 70)
print("✅ INTEGRATION TEST COMPLETE!")
print("=" * 70)

# Show what we can do next
print("\n🚀 Next Steps Available:")
print("   1. Generate enhanced quality report with domain insights")
print("   2. Export domain analysis results")
print("   3. Add domain info to HTML reports")
print("   4. Test on multiple different datasets")

