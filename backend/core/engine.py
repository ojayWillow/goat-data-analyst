# ============================================================================
# GOAT Data Analyst - Analysis Engine
# ============================================================================
# This is the HEART of the system. All analysis flows through this file.
# 
# Key Rules:
# 1. ONE function does everything: analyze(df) → AnalysisResult
# 2. All modules are PLUGINS - they're optional and gracefully degrade
# 3. Add new features by adding plugins, not parallel code paths
# 4. Never duplicate logic - if it analyzes data, it belongs here
#
# Flow: CSV → engine.analyze(df) → AnalysisResult → UI/API
# ============================================================================




"""
AnalysisEngine: The ONE brain that orchestrates everything

This is the heart of GOAT. All analysis flows through this single function:
    df → engine.analyze(df) → AnalysisResult

No duplicate logic. No parallel paths. One truth.
"""

import pandas as pd
import time
from typing import Optional
from backend.core.models import AnalysisResult

# Import existing modules (you'll wire these in as they exist)
try:
    from backend.data_processing.profiler import DataProfiler
except ImportError:
    DataProfiler = None

try:
    from backend.domain_detection.detector import DomainDetector
except ImportError:
    DomainDetector = None

try:
    from backend.analytics.statistical_analyzer import StatisticalAnalyzer
except ImportError:
    StatisticalAnalyzer = None

try:
    from backend.ai.insight_generator import InsightGenerator
except ImportError:
    InsightGenerator = None

try:
    from backend.ai.ai_engine import AIEngine
except ImportError:
    AIEngine = None

try:
    from backend.visualizations.chart_orchestrator import ChartOrchestrator
except ImportError:
    ChartOrchestrator = None

try:
    from backend.reports.style_c_color_coded import UltimateReportGenerator
except ImportError:
    UltimateReportGenerator = None

try:
    from backend.narrative.narrative_generator import NarrativeGenerator
except ImportError:
    NarrativeGenerator = None


class AnalysisEngine:
    """
    The central brain of GOAT Data Analyst
    
    Orchestrates all analysis steps in correct order:
    1. Profile: What IS this data?
    2. Domain: What TYPE of data is this?
    3. Quality: What's WRONG with this data?
    4. Analytics: What PATTERNS exist?
    5. AI Insights: What does it MEAN?
    6. Charts: SHOW me visually
    7. Narrative: COMMUNICATE like a human (AI-enhanced Day 8)
    8. Report: Package it all BEAUTIFULLY
    """
    
    def __init__(self):
        """Initialize all plugins/modules"""
        # Each module is a "plugin" to the engine
        self.profiler = DataProfiler() if DataProfiler else None
        self.domain_detector = DomainDetector() if DomainDetector else None
        self.statistical_analyzer = StatisticalAnalyzer() if StatisticalAnalyzer else None
        self.insight_generator = InsightGenerator() if InsightGenerator else None
        
        # Day 8: Initialize AIEngine for narrative enhancement
        self.ai_engine = AIEngine() if AIEngine else None
        
        # Pass AIEngine to NarrativeGenerator for AI-enhanced pain points
        self.narrative_generator = NarrativeGenerator(ai_engine=self.ai_engine) if NarrativeGenerator else None
        
        # ChartOrchestrator will be initialized in analyze() with the actual df
        self.report_generator = UltimateReportGenerator() if UltimateReportGenerator else None
        
        print("✓ AnalysisEngine initialized" + (" (AI-enhanced)" if self.ai_engine and self.ai_engine.enabled else ""))
    
    def analyze(self, df: pd.DataFrame, options: Optional[dict] = None) -> AnalysisResult:
        """
        THE master function that does everything
        
        Args:
            df: Input DataFrame to analyze
            options: Optional config (e.g., {"skip_ai": True, "chart_limit": 5})
        
        Returns:
            AnalysisResult with all outputs populated
        
        Example:
            engine = AnalysisEngine()
            result = engine.analyze(df)
            print(result.report_html)  # Full HTML report ready to display
        """
        start_time = time.time()
        options = options or {}
        
        print(f"\n🚀 Starting analysis on {len(df)} rows × {len(df.columns)} columns...")
        
        # Initialize result container
        result = AnalysisResult(dataframe=df)
        
        try:
            # Step 1: PROFILE - Basic statistics
            if self.profiler:
                print("  → Profiling data...")
                result.profile = self.profiler.profile(df)
            else:
                result.warnings.append("DataProfiler not available - using basic stats")
                result.profile = self._basic_profile(df)
            
            # Step 2: DOMAIN - Detect what type of data this is
            if self.domain_detector:
                print("  → Detecting domain...")
                result.domain = self.domain_detector.detect(df)
                print(f"[DEBUG] Engine domain detection: {result.domain}")
            else:
                result.warnings.append("DomainDetector not available")
                result.domain = {"type": "unknown", "confidence": 0.0}
            
            # Step 3: QUALITY - Check for issues
            print("  → Analyzing data quality...")
            result.quality = self._analyze_quality(df)
            
            # Step 4: ANALYTICS - Statistical analysis
            if self.statistical_analyzer:
                print("  → Running statistical analysis...")
                result.analytics = self.statistical_analyzer.analyze(df)
            else:
                result.warnings.append("StatisticalAnalyzer not available")
                result.analytics = {}
            
            # Step 5: AI INSIGHTS - LLM-generated insights (optional, can be slow)
            if self.insight_generator and not options.get("skip_ai", False):
                print("  → Generating AI insights...")
                result.ai_insights = self.insight_generator.generate(df, result.profile, result.domain)
            else:
                result.ai_insights = {"summary": "AI insights disabled or unavailable"}
            
            # Step 6: CHARTS - Generate visualizations (initialize ChartOrchestrator here with df)
            if ChartOrchestrator:
                print("  → Creating charts...")
                chart_orch = ChartOrchestrator(df, result.domain.get('type'), result.profile)
                result.charts = chart_orch.generate_all_charts()
            else:
                result.warnings.append("ChartOrchestrator not available")
                result.charts = {}
            
            # Step 7: NARRATIVE - Human-like communication (Day 8: AI-enhanced pain points)
            if self.narrative_generator:
                print("  → Generating narrative..." + (" (AI-enhanced)" if self.ai_engine and self.ai_engine.enabled else ""))
                result.narrative = self.narrative_generator.generate_full_narrative(
                    domain=result.domain,
                    profile=result.profile,
                    quality=result.quality,
                    analytics=result.analytics,
                    df=df
                )
            else:
                result.warnings.append("NarrativeGenerator not available")
                result.narrative = ""
            
            # Step 8: REPORT - Assemble everything into HTML
            if self.report_generator:
                print("  → Assembling final report...")
                result.report_html = self.report_generator.generate(result)
            else:
                result.warnings.append("ReportGenerator not available")
                result.report_html = self._fallback_report(result)
            
            # Done!
            result.execution_time_seconds = time.time() - start_time
            print(f"✅ Analysis complete in {result.execution_time_seconds:.2f}s")
            
        except Exception as e:
            result.errors.append(f"Analysis failed: {str(e)}")
            result.execution_time_seconds = time.time() - start_time
            print(f"❌ Analysis failed: {str(e)}")
        
        return result
    
    def _basic_profile(self, df: pd.DataFrame) -> dict:
        """Fallback profiling if DataProfiler isn't available"""
        return {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "memory_mb": df.memory_usage(deep=True).sum() / 1024 / 1024
        }
    
    def _analyze_quality(self, df: pd.DataFrame) -> dict:
        """Basic quality checks (always available)"""
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        duplicates = df.duplicated().sum()
        
        return {
            "missing_pct": round(missing_pct, 2),
            "duplicates": int(duplicates),
            "missing_by_column": df.isnull().sum().to_dict(),
            "overall_score": max(0, 100 - missing_pct - (duplicates / len(df) * 100 * 2))
        }
    
    def _fallback_report(self, result: AnalysisResult) -> str:
        """Minimal HTML report if ReportGenerator isn't available"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #333; }}
                .metric {{ margin: 10px 0; }}
            </style>
        </head>
        <body>
            <h1>GOAT Data Analysis Report</h1>
            <div class="metric"><strong>Rows:</strong> {result.profile.get('rows', 'N/A')}</div>
            <div class="metric"><strong>Columns:</strong> {result.profile.get('columns', 'N/A')}</div>
            <div class="metric"><strong>Domain:</strong> {result.domain.get('type', 'unknown')}</div>
            <div class="metric"><strong>Quality Score:</strong> {result.quality.get('overall_score', 0):.1f}/100</div>
            <div class="metric"><strong>Missing Data:</strong> {result.quality.get('missing_pct', 0):.1f}%</div>
            <div class="metric"><strong>Duplicates:</strong> {result.quality.get('duplicates', 0)}</div>
            
            <h2>Warnings</h2>
            <ul>
                {''.join(f'<li>{w}</li>' for w in result.warnings)}
            </ul>
        </body>
        </html>
        """


# Quick test function
def _test():
    """Test the engine with dummy data"""
    df = pd.DataFrame({
        "id": range(100),
        "amount": [100 + i * 5 for i in range(100)],
        "category": ["A", "B", "C"] * 33 + ["A"]
    })
    
    engine = AnalysisEngine()
    result = engine.analyze(df)
    
    print("\n" + "="*50)
    print("TEST RESULTS:")
    print("="*50)
    print(f"Profile: {result.profile}")
    print(f"Domain: {result.domain}")
    print(f"Quality: {result.quality}")
    print(f"Narrative length: {len(result.narrative)} chars")
    print(f"Execution time: {result.execution_time_seconds:.2f}s")
    print(f"Report HTML length: {len(result.report_html)} chars")
    print("="*50)


if __name__ == "__main__":
    _test()
