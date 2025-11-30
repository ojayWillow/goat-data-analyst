import sys
from datetime import datetime

from backend.connectors.csv_handler import CSVHandler
from backend.data_processing.profiler import DataProfiler
from backend.export_engine.ultimate_report import UltimateReportGenerator
from backend.analytics.simple_analytics import SimpleAnalytics
from backend.analytics.ai_insights import AIInsightsEngine
from backend.domain_detection.domain_detector import DomainDetector
from backend.analytics.visualizations import DataVisualizer


def main():
    # 1) Load data
    print("[1/5] Loading data...")
    handler = CSVHandler()
    csv_file = sys.argv[1] if len(sys.argv) > 1 else "sample_data/amazon.csv"
    df = handler.load_csv(csv_file)
    print(f"[OK] Loaded dataset: {csv_file} ({len(df):,} rows, {len(df.columns)} columns)")

    # 2) Profile
    print("[2/5] Profiling dataset...")
    profiler = DataProfiler()
    profile = profiler.profile_dataframe(df)
    quality = profiler.get_quality_report()
    print("[OK] Profiling complete")

    # 3) Domain detection
    print("[3/5] Detecting domain...")
    detector = DomainDetector()
    domain = detector.detect_domain(df)
    primary = domain.get("primary_domain")
    confidence = domain.get("confidence", 0)
    print(f"[OK] Domain detected: {primary} ({confidence:.1%})")

    # 4) Analytics + AI insights
    print("[4/5] Running analytics and AI insights...")
    analytics = SimpleAnalytics()
    analytics_summary = analytics.analyze_dataset(df)

    ai_engine = AIInsightsEngine()
    ai_results = ai_engine.generate_insights(df, domain, analytics_summary)
    ai_count = len(ai_results.get("ai_insights", []))
    print(f"[OK] Generated {ai_count} AI insights")

    # 5) Generate ultimate report
    print("[5/5] Generating ultimate report...")
    generator = UltimateReportGenerator(profile, quality, df)
    generator.domain = domain
    generator.analytics_summary = analytics_summary
    generator.ai_insights = ai_results["ai_insights"]

    # NEW: Generate charts
    visualizer = DataVisualizer(df)
    generator.charts = visualizer.generate_all_charts()

    output_file = f"ULTIMATE_REPORT_{datetime.now().strftime('%H%M%S')}.html"
    html = generator.generate_html()
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n✅ SUCCESS: {output_file} created with AI insights!")


if __name__ == "__main__":
    main()
