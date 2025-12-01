"""
Full end-to-end test of the GOAT Data Analyst pipeline.
Tests: CSV Load → Profile → Domain Detection → Analytics → AI Insights → Report Generation
"""

import pandas as pd
import traceback
from pathlib import Path

print("=" * 70)
print("🚀 GOAT Data Analyst - Full Pipeline Test")
print("=" * 70)

try:
    # ===== STEP 1: Load CSV =====
    print("\n[1/7] Loading CSV file...")
    df = pd.read_csv("test_data.csv")
    print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
    print(f"    Columns: {', '.join(df.columns.tolist())}")

    # ===== STEP 2: Profile =====
    print("\n[2/7] Profiling data...")
    from backend.data_processing.profiler import DataProfiler
    profiler = DataProfiler()
    profile = profiler.profile_dataframe(df)
    quality_score = profile.get("quality_score", 0)
    print(f"✅ Quality Score: {quality_score}/100")

    # ===== STEP 3: Domain Detection (Keyword) =====
    print("\n[3/7] Domain detection (keyword-based)...")
    from backend.domain_detection.domain_detector import DomainDetector
    keyword_detector = DomainDetector()
    keyword_result = keyword_detector.detect_domain(df)
    print(f"✅ Keyword detected: {keyword_result.get('primary_domain', 'Unknown')}")

    # ===== STEP 4: Domain Detection (AI-enhanced) =====
    print("\n[4/7] Domain detection (AI-enhanced)...")
    from backend.domain_detection.ai_domain_detector import AIDomainDetector
    ai_detector = AIDomainDetector()
    domain_result = ai_detector.enhance_detection(df, keyword_result)
    final_domain = domain_result.get("primary_domain", "Unknown")
    print(f"✅ AI-enhanced domain: {final_domain}")

    # ===== STEP 5: Analytics =====
    print("\n[5/7] Running analytics...")
    from backend.analytics.simple_analytics import SimpleAnalytics
    analytics = SimpleAnalytics()
    analytics_summary = analytics.analyze_dataset(df)
    print(f"✅ Analytics complete")

    # ===== STEP 6: AI Insights =====
    print("\n[6/7] Generating AI insights...")
    from backend.analytics.ai_insights import AIInsightsEngine
    ai_engine = AIInsightsEngine()
    ai_results = ai_engine.generate_insights(df, final_domain, analytics_summary)
    ai_insights = ai_results.get("ai_insights", [])
    print(f"✅ Generated {len(ai_insights)} AI insights")
    for i, insight in enumerate(ai_insights[:3], 1):
        print(f"   {i}. {insight[:60]}...")

    # ===== STEP 7: Generate Report =====
    print("\n[7/7] Generating HTML report...")
    from backend.export_engine.ultimate_report import UltimateReportGenerator
    
    # Prepare data
    insights_data = {
        "insights": ai_insights,
        "model": "Groq Llama 3"
    }

    charts_data = {
        "time_series": "<div style='padding:20px;'>📈 Time Series Visualization</div>",
        "distribution": "<div style='padding:20px;'>📊 Distribution Analysis</div>"
    }

    # Generate
    generator = UltimateReportGenerator()
    html = generator.generate_report(
        df=df,
        profile=profile,
        domain_result=domain_result,
        analytics=analytics_summary,
        ai_insights=insights_data,
        include_charts=True
    )

    # Save
    output_file = "test_full_report.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Report generated: {len(html):,} bytes")
    print(f"✅ Saved to: {output_file}")

    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED - FULL PIPELINE WORKING!")
    print("=" * 70)
    print(f"\n📄 Open 'test_full_report.html' in your browser to see the report")

except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print("\nFull traceback:")
    traceback.print_exc()
    exit(1)
