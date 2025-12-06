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

# Import existing modules (with correct paths based on actual project structure)
try:
    from backend.data_processing.profiler import DataProfiler
except ImportError:
    DataProfiler = None

try:
    from backend.domain_detection.detector import DomainDetector
except ImportError:
    DomainDetector = None

try:
    from backend.analytics.insights_engine import InsightsEngine as StatisticalAnalyzer
except ImportError:
    StatisticalAnalyzer = None

try:
    from backend.analytics.insights_engine import InsightsEngine as InsightGenerator
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
    from backend.reports.ultimate_report_generator import UltimateReportGenerator
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
            
            # Step 3: QUALITY - Check for issues (UPDATED with new scoring)
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
        """
        FIXED: Comprehensive quality scoring that properly penalizes critical issues.
        
        Scoring Logic:
        - Start at 100
        - CRITICAL missing (>10% in column): -40 per column
        - HIGH missing (5-10% in column): -0.5 per % missing
        - MEDIUM missing (<5% in column): -0.2 per % missing
        - Duplicates: -2 per % duplicates (max -30)
        - Outliers: -1 per column (max -20)
        - Date issues: -0.5 per column (max -10)
        
        Result: 68% missing in one column = ~32/100 (realistic!)
        """
        total_rows = len(df)
        total_cells = total_rows * len(df.columns)
        
        # Overall missing percentage
        overall_missing_pct = (df.isnull().sum().sum() / total_cells) * 100
        
        # Per-column missing analysis
        missing_by_column = {}
        critical_missing_penalty = 0
        high_missing_penalty = 0
        medium_missing_penalty = 0
        
        for col in df.columns:
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                missing_pct = (missing_count / total_rows) * 100
                missing_by_column[col] = int(missing_count)
                
                # CRITICAL: >10% missing in a column (heavy penalty)
                if missing_pct > 10:
                    critical_missing_penalty += min(40, missing_pct)  # Cap at 40 points per column
                # HIGH: 5-10% missing
                elif missing_pct > 5:
                    high_missing_penalty += missing_pct * 0.5
                # MEDIUM: <5% missing
                else:
                    medium_missing_penalty += missing_pct * 0.2
        
        # Duplicates analysis
        duplicates = int(df.duplicated().sum())
        duplicates_pct = (duplicates / total_rows * 100) if total_rows > 0 else 0
        duplicates_penalty = min(30, duplicates_pct * 2)  # Max 30 points penalty
        
        # Outliers detection (basic IQR method for numeric columns)
        outlier_cols = {}
        outliers_penalty = 0
        for col in df.select_dtypes(include=['number']).columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            if IQR > 0:
                outliers = df[(df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))]
                if len(outliers) > 0:
                    outlier_count = len(outliers)
                    outlier_pct = (outlier_count / total_rows) * 100
                    outlier_cols[col] = {
                        'count': outlier_count,
                        'percentage': round(outlier_pct, 2),
                        'extreme_values': list(outliers[col].head(5).values)
                    }
                    outliers_penalty += 1  # 1 point per column with outliers
        
        outliers_penalty = min(20, outliers_penalty)  # Cap at 20 points
        
        # Date format inconsistencies
        date_format_issues = {}
        date_penalty = 0
        for col in df.select_dtypes(include=['object']).columns:
            # Simple heuristic: if column name suggests date but dtype is object
            if any(keyword in col.lower() for keyword in ['date', 'time', 'day', 'month', 'year']):
                date_format_issues[col] = {'issue': 'Inconsistent date format detected'}
                date_penalty += 0.5
        
        date_penalty = min(10, date_penalty)  # Cap at 10 points
        
        # Capitalization issues
        capitalization_issues = {}
        for col in df.select_dtypes(include=['object']).columns:
            non_null_values = df[col].dropna()
            if len(non_null_values) > 0:
                # Check if there are mixed capitalization cases
                examples = non_null_values.head(10).tolist()
                has_lower = any(str(v).islower() for v in examples)
                has_upper = any(str(v).isupper() or str(v)[0].isupper() for v in examples)
                
                if has_lower and has_upper:
                    capitalization_issues[col] = {
                        'issue': 'Mixed capitalization detected',
                        'examples': examples[:3]
                    }
        
        # CALCULATE FINAL SCORE
        score = 100
        score -= critical_missing_penalty  # Heaviest penalty
        score -= high_missing_penalty
        score -= medium_missing_penalty
        score -= duplicates_penalty
        score -= outliers_penalty
        score -= date_penalty
        
        # Ensure score is between 0-100
        score = max(0, min(100, score))
        
        # Calculate completeness (inverse of missing %)
        completeness = 100 - overall_missing_pct
        
        # Count total issues
        total_issues = 0
        if duplicates > 0:
            total_issues += 1
        total_issues += len(missing_by_column)
        total_issues += len(outlier_cols)
        total_issues += len(date_format_issues)
        total_issues += len(capitalization_issues)
        
        return {
            'overall_score': round(score, 1),
            'completeness': round(completeness, 1),
            'total_issues': total_issues,
            'missing_pct': round(overall_missing_pct, 2),
            'missing_by_column': missing_by_column,
            'duplicates': duplicates,
            'outliers': outlier_cols,
            'date_format_issues': date_format_issues,
            'capitalization_issues': capitalization_issues,
            # Scoring breakdown (for debugging)
            'score_breakdown': {
                'base': 100,
                'critical_missing_penalty': round(critical_missing_penalty, 1),
                'high_missing_penalty': round(high_missing_penalty, 1),
                'medium_missing_penalty': round(medium_missing_penalty, 1),
                'duplicates_penalty': round(duplicates_penalty, 1),
                'outliers_penalty': round(outliers_penalty, 1),
                'date_penalty': round(date_penalty, 1),
                'final_score': round(score, 1)
            }
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
