"""
Test: Generate enhanced quality report with domain intelligence
"""

from backend.connectors.csv_handler import CSVHandler
from backend.data_processing.profiler import DataProfiler
from backend.export_engine.enhanced_quality_report import EnhancedQualityReportGenerator
from datetime import datetime

print("=" * 70)
print("🎨 ENHANCED QUALITY REPORT GENERATION TEST")
print("=" * 70)

# Step 1: Load Data
print("\n📂 Step 1: Loading train.csv...")
handler = CSVHandler()
df = handler.load_csv('sample_data/train.csv')
print(f"   ✅ Loaded {len(df):,} rows × {len(df.columns)} columns")

# Step 2: Profile Data
print("\n📊 Step 2: Profiling data quality...")
profiler = DataProfiler()
profile = profiler.profile_dataframe(df)
quality = profiler.get_quality_report()
print(f"   ✅ Quality Score: {quality['score']}/100")

# Step 3: Generate Enhanced Report
print("\n🎨 Step 3: Generating enhanced report with domain detection...")
generator = EnhancedQualityReportGenerator(profile, quality)
output_file = f"enhanced_quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
report_path = generator.generate_html(output_file, df=df)
print(f"   ✅ Report generated: {report_path}")

# Step 4: Show Results
print("\n" + "=" * 70)
print("📋 REPORT GENERATION COMPLETE!")
print("=" * 70)

if generator.domain_result:
    domain = generator.domain_result['primary_domain']
    confidence = generator.domain_result['confidence']
    entities = len(generator.domain_result['detected_entities'])
    recommendations = len(generator.domain_result['recommendations'])
    
    print(f"\n🎯 Domain Detected: {domain.upper()} ({confidence:.0%} confidence)")
    print(f"📊 Quality Score: {quality['score']}/100")
    print(f"🔍 Domain Entities: {entities}")
    print(f"💡 Recommendations: {recommendations}")
    print(f"\n📄 Report saved to: {output_file}")
    print(f"\n🌐 Open in browser to see the enhanced report!")
else:
    print("\n⚠️ No domain detected")

print("\n" + "=" * 70)
print("✅ TEST COMPLETE!")
print("=" * 70)

