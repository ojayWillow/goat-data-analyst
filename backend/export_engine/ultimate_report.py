"""Ultimate Report - combines original report, domain detection, AI insights, analytics, and charts."""

from backend.export_engine.quality_report import QualityReportGenerator as OriginalGen
from backend.domain_detection.domain_detector import DomainDetector
from backend.analytics.simple_analytics import SimpleAnalytics
from backend.analytics.insights_engine import InsightsEngine
from backend.visualizations.universal_charts import UniversalChartGenerator
import pandas as pd
from typing import Dict, Any, List


class UltimateReportGenerator:
    """
    Wraps the original HTML report and injects:
      - Domain Intelligence (using self.domain_result, can be AI-enhanced)
      - Rule-based insights
      - AI-powered insights
      - Data analytics summary
      - Universal charts
    """

    def __init__(self, profile: Dict[str, Any], quality_report: Dict[str, Any], df: pd.DataFrame = None):
        self.profile = profile
        self.quality_report = quality_report
        self.df = df

        # Original generator
        self.original_gen = OriginalGen(profile, quality_report)

        # Engines
        self.domain_detector = DomainDetector()
        self.analytics_engine = SimpleAnalytics()
        self.insights_engine = InsightsEngine()

        # Data holders
        self.domain_result: Dict[str, Any] = None   # Will hold AI-enhanced result from main.py
        self.analytics_result: Dict[str, Any] = None
        self.insights: List[str] = []
        self.ai_insights: List[str] = []
        self.charts: Dict[str, str] = {}

        # If df is provided, do basic computation (for backward compatibility)
        if df is not None:
            # Keyword-based domain (used as fallback or for entities)
            keyword_domain = self.domain_detector.detect_domain(df)
            if self.domain_result is None:
                self.domain_result = keyword_domain

            # Rule-based analytics
            self.analytics_result = self.analytics_engine.analyze_dataset(df)
            primary_domain = None
            if self.domain_result:
                primary_domain = self.domain_result.get("primary_domain")

            # Rule-based insights
            self.insights = self.insights_engine.generate_insights(df, primary_domain)

            # Charts (if not already injected)
            if not self.charts:
                try:
                    chart_gen = UniversalChartGenerator(df, primary_domain)
                    self.charts = chart_gen.generate_all_charts()
                except Exception as e:
                    print(f"Chart generation error in UltimateReportGenerator: {e}")

    def generate_html(self) -> str:
        """Generate original HTML and inject our sections before </body>."""
        original_html = self.original_gen.generate_html()
        body_close_idx = original_html.rfind("</body>")
        if body_close_idx < 0:
            return original_html

        our_html = ""

        # Domain Intelligence (AI-enhanced)
        if self.domain_result:
            our_html += self._domain_html()

        # Rule-based insights
        if self.insights:
            our_html += self._insights_html()

        # AI insights (from Groq)
        if self.ai_insights:
            our_html += self._ai_insights_html()

        # Data analytics
        if self.analytics_result:
            our_html += self._analytics_html()

        # Charts
        if self.charts:
            our_html += self._charts_html()

        if our_html:
            return original_html[:body_close_idx] + our_html + original_html[body_close_idx:]

        return original_html

    def _domain_html(self) -> str:
        """Render Domain Intelligence section. Uses self.domain_result (AI-enhanced if available)."""
        domain = self.domain_result.get("primary_domain", "Unknown").upper()
        confidence = self.domain_result.get("confidence", 0)

        # Normalize and cap confidence between 0 and 1
        try:
            # If backend accidentally sends 0–100, convert to 0–1
            if confidence > 1:
                confidence = confidence / 100.0
        except (TypeError, ValueError):
            confidence = 0

        confidence = max(0.0, min(1.0, confidence))
        
        entities = self.domain_result.get("detected_entities", []) or self.domain_result.get("entities", [])
        all_scores = self.domain_result.get("all_scores", {})

        html = '<div class="card" style="padding: 20px; margin-bottom: 20px;">'
        html += '<h2 style="margin-bottom: 16px; font-size: 20px;">🎯 Domain Intelligence</h2>'

        html += '<div style="display: flex; gap: 20px; margin-bottom: 16px;">'
        html += '<div style="flex: 1; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 16px; border-radius: 8px; color: white; text-align: center;">'
        html += '<div style="font-size: 12px; opacity: 0.9; margin-bottom: 4px;">Domain</div>'
        html += f'<div style="font-size: 24px; font-weight: bold;">{domain}</div>'
        html += '</div>'

        html += '<div style="flex: 1; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 16px; border-radius: 8px; color: white; text-align: center;">'
        html += '<div style="font-size: 12px; opacity: 0.9; margin-bottom: 4px;">Confidence</div>'
        html += f'<div style="font-size: 24px; font-weight: bold;">{confidence*100:.0f}%</div>'
        html += '</div>'
        html += '</div>'

        if all_scores:
            html += '<div style="background: #f8f9fa; padding: 12px; border-radius: 6px; margin-bottom: 12px;">'
            sorted_scores = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)[:3]
            for d_name, score_val in sorted_scores:
                # Normalize score_val as well
                try:
                    if score_val > 1:
                        score_val = score_val / 100.0
                except (TypeError, ValueError):
                    score_val = 0
                score_val = max(0.0, min(1.0, score_val))
                
                pct = score_val * 100
                bar_color = "#667eea" if score_val > 0 else "#e0e0e0"
                html += '<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">'
                html += f'<div style="min-width: 100px; font-size: 11px; font-weight: 600;">{d_name.title()}</div>'
                html += '<div style="flex: 1; background: #e0e0e0; height: 4px; border-radius: 2px;">'
                html += f'<div style="background: {bar_color}; height: 100%; width: {pct}%;"></div>'
                html += '</div>'
                html += f'<div style="min-width: 40px; text-align: right; font-size: 11px; font-weight: 600;">{score_val*100:.0f}%</div>'
                html += '</div>'
            html += '</div>'

        if entities:
            html += '<div style="display: flex; flex-wrap: wrap; gap: 6px;">'
            for entity in entities[:8]:
                html += f'<span style="background: #667eea; color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px;">{entity}</span>'
            if len(entities) > 8:
                html += f'<span style="background: #e0e0e0; color: #666; padding: 4px 10px; border-radius: 12px; font-size: 11px;">+{len(entities) - 8} more</span>'
            html += '</div>'

        html += '</div>'
        return html

    def _insights_html(self) -> str:
        html = '<div class="card" style="padding: 20px; margin-bottom: 20px;">'
        html += '<h2 style="margin-bottom: 12px; font-size: 20px;">💡 Rule-Based Insights</h2>'

        for i, insight in enumerate(self.insights[:3], 1):
            html += '<div style="background: #fff4e6; padding: 10px; margin-bottom: 8px; border-left: 3px solid #ff9800; border-radius: 4px; font-size: 13px;">'
            html += f'<strong style="color: #ff9800;">{i}.</strong> {insight}'
            html += '</div>'

        if len(self.insights) > 3:
            html += f'<div style="text-align: center; color: #666; font-size: 12px; margin-top: 8px;">+{len(self.insights) - 3} more insights</div>'

        html += '</div>'
        return html

    def _ai_insights_html(self) -> str:
        html = '<div class="card" style="padding: 20px; margin-bottom: 20px; background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);">'
        html += '<h2 style="margin-bottom: 12px; font-size: 20px;">🤖 AI-Powered Insights</h2>'
        html += '<div style="font-size: 11px; color: #666; margin-bottom: 12px;">Generated by Groq Llama 3.3 70B</div>'

        for i, insight in enumerate(self.ai_insights, 1):
            clean_insight = insight
            if insight.strip().startswith(f"{i}."):
                clean_insight = insight.split(".", 1)[1].strip()

            html += '<div style="background: white; padding: 12px; margin-bottom: 10px; border-left: 4px solid #667eea; border-radius: 6px; font-size: 13px; line-height: 1.6;">'
            html += f'<strong style="color: #667eea;">#{i}</strong> {clean_insight}'
            html += '</div>'

        html += '</div>'
        return html

    def _charts_html(self) -> str:
        html = '<div class="card" style="padding: 20px; margin-bottom: 20px;">'
        html += '<h2 style="margin-bottom: 16px; font-size: 20px;">📈 Visual Analytics</h2>'

        if "time_series" in self.charts:
            html += '<div style="margin-bottom: 24px;">'
            html += self.charts["time_series"]
            html += '</div>'

        if "top_n" in self.charts:
            html += '<div style="margin-bottom: 24px;">'
            html += self.charts["top_n"]
            html += '</div>'

        if "distribution" in self.charts:
            html += '<div style="margin-bottom: 24px;">'
            html += self.charts["distribution"]
            html += '</div>'

        if "correlation" in self.charts:
            html += '<div style="margin-bottom: 24px;">'
            html += self.charts["correlation"]
            html += '</div>'

        html += '</div>'
        return html

    def _analytics_html(self) -> str:
        analytics = self.analytics_result or {}
        summary = analytics.get("summary", {})
        numeric = analytics.get("numeric_analysis", {})

        html = '<div class="card" style="padding: 20px; margin-bottom: 20px;">'
        html += '<h2 style="margin-bottom: 12px; font-size: 20px;">📊 Data Analytics</h2>'

        html += '<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 12px;">'
        html += '<div style="background: #f8f9fa; padding: 10px; border-radius: 6px; text-align: center;">'
        html += f'<div style="font-size: 18px; font-weight: bold; color: #667eea;">{summary.get("rows", 0):,}</div>'
        html += '<div style="font-size: 10px; color: #666; margin-top: 2px;">Rows</div></div>'

        html += '<div style="background: #f8f9fa; padding: 10px; border-radius: 6px; text-align: center;">'
        html += f'<div style="font-size: 18px; font-weight: bold; color: #667eea;">{summary.get("columns", 0)}</div>'
        html += '<div style="font-size: 10px; color: #666; margin-top: 2px;">Columns</div></div>'

        html += '<div style="background: #f8f9fa; padding: 10px; border-radius: 6px; text-align: center;">'
        html += f'<div style="font-size: 18px; font-weight: bold; color: #667eea;">{summary.get("missing_percentage", 0):.1f}%</div>'
        html += '<div style="font-size: 10px; color: #666; margin-top: 2px;">Missing</div></div>'

        total_memory = summary.get("memory_usage_mb", 0)
        html += '<div style="background: #f8f9fa; padding: 10px; border-radius: 6px; text-align: center;">'
        html += f'<div style="font-size: 18px; font-weight: bold; color: #667eea;">{total_memory:.1f}MB</div>'
        html += '<div style="font-size: 10px; color: #666; margin-top: 2px;">Memory</div></div>'

        html += '</div>'

        if numeric:
            for col_name, stats in list(numeric.items())[:2]:
                html += '<div style="background: #f8f9fa; padding: 10px; margin-bottom: 6px; border-radius: 6px;">'
                html += f'<div style="font-weight: 600; font-size: 11px; margin-bottom: 6px; color: #667eea;">{col_name}</div>'
                html += '<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; font-size: 10px; color: #666;">'
                html += f'<div>avg: {stats.get("mean", 0):.1f}</div>'
                html += f'<div>min: {stats.get("min", 0):.1f}</div>'
                html += f'<div>max: {stats.get("max", 0):.1f}</div>'
                html += f'<div>std: {stats.get("std_dev", 0):.1f}</div>'
                html += '</div></div>'

        html += '</div>'
        return html
