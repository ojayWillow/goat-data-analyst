"""Ultimate Report - adaptive structure based on data quality."""

from backend.export_engine.quality_report import QualityReportGenerator as OriginalGen
from backend.domain_detection.domain_detector import DomainDetector
from backend.analytics.simple_analytics import SimpleAnalytics
from backend.analytics.insights_engine import InsightsEngine
from backend.analytics.ai_insights import AIInsightsEngine
from backend.visualizations.universal_charts import UniversalChartGenerator
import pandas as pd
from typing import Dict, Any, List


class UltimateReportGenerator:
    """
    Adaptive report generator:
    - Bad data (score < 70): Quality issues first, minimal analytics
    - Good data (score ≥ 70): Charts first, quality details at bottom
    """

    def __init__(self, profile: Dict[str, Any], quality_report: Dict[str, Any], df: pd.DataFrame = None):
        self.profile = profile
        self.quality_report = quality_report
        self.df = df
        self.quality_score = quality_report.get('score', 100)

        # Original generator
        self.original_gen = OriginalGen(profile, quality_report)

        # Engines
        self.domain_detector = DomainDetector()
        self.analytics_engine = SimpleAnalytics()
        self.insights_engine = InsightsEngine()
        self.ai_insights_engine = AIInsightsEngine()

        # Data holders
        self.domain_result: Dict[str, Any] = None
        self.analytics_result: Dict[str, Any] = None
        self.insights: List[str] = []
        self.ai_insights: List[str] = []
        self.charts: Dict[str, str] = {}

        # Backward compatibility
        if df is not None:
            keyword_domain = self.domain_detector.detect_domain(df)
            if self.domain_result is None:
                self.domain_result = keyword_domain

            self.analytics_result = self.analytics_engine.analyze_dataset(df)
            primary_domain = None
            if self.domain_result:
                primary_domain = self.domain_result.get("primary_domain")

            # Generate rule-based insights (structured facts)
            insights_facts = self.insights_engine.generate_insights(df, primary_domain)

            # Convert to AI prose
            try:
                dataset_summary = self._build_dataset_summary_for_ai(df, insights_facts, primary_domain)
                self.ai_insights = self.ai_insights_engine._call_groq(dataset_summary)
            except Exception as e:
                print(f"AI insights error: {e}")
                self.ai_insights = []

            # Charts
            if not self.charts:
                try:
                    chart_gen = UniversalChartGenerator(df)
                    self.charts = chart_gen.generate_all_universal_charts()
                except Exception as e:
                    print(f"Chart generation error: {e}")

    def _build_dataset_summary_for_ai(self, df: pd.DataFrame, insights_facts: Dict[str, Any], domain: str) -> str:
        """Build a concise dataset summary for the AI engine."""
        lines = [f"Dataset Analysis for {domain or 'Unknown'} Domain"]
        
        quality = insights_facts.get("quality", {})
        lines.append(f"\nDataset Size: {quality.get('rows', 0):,} rows, {quality.get('columns', 0)} columns")
        lines.append(f"Data Quality: {100 - quality.get('missing_pct', 0):.1f}% complete, {quality.get('duplicates', 0)} duplicates")
        
        lines.append(f"\nColumns: {', '.join(df.columns.tolist()[:10])}")
        
        concentration = insights_facts.get("concentration", [])
        if concentration:
            lines.append("\nKey Concentrations:")
            for c in concentration:
                lines.append(f"- Top {c['top_n']} {c['column']}: {c['top_pct']:.1f}% of {c['value_metric']}")
        
        outliers = insights_facts.get("outliers", [])
        if outliers:
            lines.append("\nOutliers Detected:")
            for o in outliers:
                lines.append(f"- {o['column']}: {o['count']} outliers ({o['pct']:.1f}%)")
        
        metrics = insights_facts.get("metrics", [])
        if metrics:
            lines.append("\nKey Metrics:")
            for m in metrics:
                lines.append(f"- {m['name']}: total={m['total']}, avg={m['avg']}, range=[{m['min']}, {m['max']}]")
        
        domain_facts = insights_facts.get("domain_facts", {})
        if domain_facts:
            lines.append(f"\n{domain.title()} Insights:")
            for key, val in domain_facts.items():
                lines.append(f"- {key}: {val}")
        
        return "\n".join(lines)

    def generate_html(self) -> str:
        """
        Build the report so that our new summary, charts, insights, and domain come FIRST,
        and the entire quality report appears below as its own section.
        """
        # Get the full quality report HTML from the original generator
        quality_html = self.original_gen.generate_html()

        # Build our new top sections
        if self.quality_score < 70:
            # Bad data: alert + domain + quality-focused insights
            main_sections = self._quality_alert_banner()
            if self.domain_result:
                main_sections += self._domain_html()
            if self.ai_insights or self.insights:
                main_sections += self._combined_insights_html(focus_on_quality=True)
        else:
            # Good/excellent data: exec summary → charts → insights → domain
            main_sections = self._executive_summary()
            if self.charts:
                main_sections += self._charts_html()
            if self.ai_insights or self.insights:
                main_sections += self._combined_insights_html(focus_on_quality=False)
            if self.domain_result:
                main_sections += self._domain_html()

        # Compose entire HTML page, with quality report at the end
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Data Analysis Report</title>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f5f6fa; color: #181818; margin: 0; padding: 0; }}
        .card {{ background: #fff; border-radius: 10px; box-shadow: 0 2px 10px 0 #0001; margin: 20px auto; max-width: 950px; padding: 36px 44px 30px 44px; }}
        h2 {{ font-weight: 700; color: #5039d4; margin-bottom: 14px; }}
        h3 {{ font-weight: 700; color: #181830; margin-bottom: 10px; font-size: 19px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 24px 0 16px 0; }}
        th, td {{ border: 1px solid #e4e8ef; padding: 7px 10px; text-align: left; }}
        tr:hover {{ background: #f0f4ff; }}
    </style>
</head>
<body>
    {main_sections}
    <div class="card" style="padding:32px 44px 24px 44px; background:#fafafc; box-shadow:none; margin-top: 30px;">
        <h2 style="font-size:24px;color:#675fd3;font-weight:900;margin-top:0;">Full Data Quality Report</h2>
        {quality_html}
    </div>
</body>
</html>
"""

    def _build_bad_data_layout(self) -> str:
        """(Unused by new generate_html, kept for compatibility if needed elsewhere)."""
        html = ""
        html += self._quality_alert_banner()
        if self.domain_result:
            html += self._domain_html()
        if self.ai_insights or self.insights:
            html += self._combined_insights_html(focus_on_quality=True)
        return html

    def _build_good_data_layout(self) -> str:
        """(Unused by new generate_html, kept for compatibility if needed elsewhere)."""
        html = ""
        html += self._executive_summary()
        if self.charts:
            html += self._charts_html()
        if self.ai_insights or self.insights:
            html += self._combined_insights_html(focus_on_quality=False)
        if self.domain_result:
            html += self._domain_html()
        return html

    def _quality_alert_banner(self) -> str:
        """Red banner for bad data quality."""
        score = self.quality_score
        issues = self.quality_report.get('issues', [])

        html = '<div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); padding: 24px; margin-bottom: 20px; border-radius: 8px; color: white;">'
        html += '<h2 style="margin: 0 0 12px 0; font-size: 24px;">⚠️ Data Quality Issues Detected</h2>'
        html += f'<div style="font-size: 18px; margin-bottom: 16px;">Quality Score: <strong>{score}/100</strong></div>'

        if issues:
            html += '<div style="background: rgba(255,255,255,0.1); padding: 12px; border-radius: 6px;">'
            html += '<div style="font-weight: 600; margin-bottom: 8px;">Critical Issues:</div>'
            for issue in issues[:3]:
                html += f'<div style="margin-bottom: 4px;">• {issue}</div>'
            if len(issues) > 3:
                html += f'<div style="margin-top: 8px; opacity: 0.8;">+{len(issues) - 3} more issues</div>'
            html += '</div>'

        html += '<div style="margin-top: 16px; font-size: 14px; opacity: 0.9;">⚡ Fix these issues before running analysis. Charts and insights may be unreliable.</div>'
        html += '</div>'
        return html

    def _executive_summary(self) -> str:
        """Quick 30-second summary for good data."""
        summary = self.analytics_result.get("summary", {}) if self.analytics_result else {}
        domain = self.domain_result.get("primary_domain", "Unknown").title() if self.domain_result else "Unknown"
        confidence = self.domain_result.get("confidence", 0) if self.domain_result else 0

        # Normalize confidence
        if confidence > 1:
            confidence = confidence / 100.0
        confidence = max(0.0, min(1.0, confidence))

        html = '<div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; margin-bottom: 20px; border-radius: 8px; color: white;">'
        html += '<h2 style="margin: 0 0 16px 0; font-size: 20px;">✅ Executive Summary</h2>'

        html += '<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;">'

        html += '<div style="background: rgba(255,255,255,0.15); padding: 12px; border-radius: 6px; text-align: center;">'
        html += f'<div style="font-size: 24px; font-weight: bold;">{summary.get("rows", 0):,}</div>'
        html += '<div style="font-size: 11px; opacity: 0.9; margin-top: 4px;">Rows</div></div>'

        html += '<div style="background: rgba(255,255,255,0.15); padding: 12px; border-radius: 6px; text-align: center;">'
        html += f'<div style="font-size: 24px; font-weight: bold;">{summary.get("columns", 0)}</div>'
        html += '<div style="font-size: 11px; opacity: 0.9; margin-top: 4px;">Columns</div></div>'

        html += '<div style="background: rgba(255,255,255,0.15); padding: 12px; border-radius: 6px; text-align: center;">'
        html += f'<div style="font-size: 24px; font-weight: bold;">{self.quality_score}</div>'
        html += '<div style="font-size: 11px; opacity: 0.9; margin-top: 4px;">Quality Score</div></div>'

        html += '<div style="background: rgba(255,255,255,0.15); padding: 12px; border-radius: 6px; text-align: center;">'
        html += f'<div style="font-size: 16px; font-weight: bold;">{domain}</div>'
        html += f'<div style="font-size: 11px; opacity: 0.9; margin-top: 4px;">{confidence*100:.0f}% confidence</div></div>'

        html += '</div></div>'
        return html

    def _charts_html(self) -> str:
        """Visual analytics section."""
        html = '<div class="card" style="padding: 20px; margin-bottom: 20px;">'
        html += '<h2 style="margin-bottom: 16px; font-size: 20px;">📈 Visual Analytics</h2>'

        chart_count = 0
        for chart_name in ["distribution", "categories", "correlation", "volume_trend"]:
            if chart_name in self.charts:
                html += f'<div style="margin-bottom: 24px;">{self.charts[chart_name]}</div>'
                chart_count += 1

        if chart_count == 0:
            html += '<div style="padding: 20px; text-align: center; color: #666;">No charts available for this dataset</div>'

        html += '</div>'
        return html

    def _combined_insights_html(self, focus_on_quality: bool = False) -> str:
        """Combine AI and rule-based insights into one section."""
        html = '<div class="card" style="padding: 20px; margin-bottom: 20px;">'
        html += '<h2 style="margin-bottom: 16px; font-size: 20px;">💡 Analyst Insights</h2>'

        if focus_on_quality:
            html += '<div style="background: #fef3c7; padding: 12px; margin-bottom: 16px; border-left: 4px solid #f59e0b; border-radius: 4px; font-size: 13px;">'
            html += '⚠️ These insights focus on data quality issues. Fix critical issues before business analysis.'
            html += '</div>'
        else:
            html += '<div style="font-size: 12px; color: #666; margin-bottom: 12px;">AI-powered observations</div>'

        insight_num = 1

        if self.ai_insights:
            for insight in self.ai_insights[:7]:
                clean = insight.strip()
                if clean and clean[0].isdigit() and '.' in clean[:3]:
                    clean = clean.split('.', 1)[1].strip()

                if clean:
                    html += '<div style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); padding: 14px; margin-bottom: 10px; border-left: 4px solid #667eea; border-radius: 6px; font-size: 14px; line-height: 1.6;">'
                    html += f'<strong style="color: #667eea;">#{insight_num}</strong> {clean}'
                    html += '</div>'
                    insight_num += 1

        if insight_num == 1:
            html += '<div style="padding: 20px; text-align: center; color: #666;">No insights available</div>'

        html += '</div>'
        return html

    def _domain_html(self) -> str:
        """Domain intelligence section."""
        domain = self.domain_result.get("primary_domain", "Unknown").upper()
        confidence = self.domain_result.get("confidence", 0)

        if confidence > 1:
            confidence = confidence / 100.0
        confidence = max(0.0, min(1.0, confidence))

        entities = self.domain_result.get("detected_entities", []) or self.domain_result.get("entities", [])

        html = '<div class="card" style="padding: 20px; margin-bottom: 20px;">'
        html += '<h2 style="margin-bottom: 16px; font-size: 20px;">🎯 Domain Intelligence</h2>'
        html += '<div style="font-size: 12px; color: #666; margin-bottom: 12px;">Best guess based on column names and patterns</div>'

        html += '<div style="display: flex; gap: 20px; margin-bottom: 16px;">'
        html += '<div style="flex: 1; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 16px; border-radius: 8px; color: white; text-align: center;">'
        html += '<div style="font-size: 12px; opacity: 0.9; margin-bottom: 4px;">Detected Domain</div>'
        html += f'<div style="font-size: 24px; font-weight: bold;">{domain}</div>'
        html += '</div>'

        html += '<div style="flex: 1; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 16px; border-radius: 8px; color: white; text-align: center;">'
        html += '<div style="font-size: 12px; opacity: 0.9; margin-bottom: 4px;">Confidence</div>'
        html += f'<div style="font-size: 24px; font-weight: bold;">{confidence*100:.0f}%</div>'
        html += '</div>'
        html += '</div>'

        if entities:
            html += '<div style="background: #f8f9fa; padding: 12px; border-radius: 6px;">'
            html += '<div style="font-size: 11px; font-weight: 600; margin-bottom: 8px; color: #666;">Key Entities Detected:</div>'
            html += '<div style="display: flex; flex-wrap: wrap; gap: 6px;">'
            for entity in entities[:10]:
                html += f'<span style="background: #667eea; color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px;">{entity}</span>'
            if len(entities) > 10:
                html += f'<span style="background: #e0e0e0; color: #666; padding: 4px 10px; border-radius: 12px; font-size: 11px;">+{len(entities) - 10} more</span>'
            html += '</div></div>'

        html += '</div>'
        return html
