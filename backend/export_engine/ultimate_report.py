"""Ultimate Report - Original + Our Features"""

from backend.export_engine.quality_report import QualityReportGenerator as OriginalGen
from backend.domain_detection.domain_detector import DomainDetector
from backend.analytics.simple_analytics import SimpleAnalytics
from backend.analytics.insights_engine import InsightsEngine
import pandas as pd
from typing import Dict, Any


class UltimateReportGenerator:
    """Combines original + domain + insights + analytics."""
    
    def __init__(self, profile: Dict[str, Any], quality_report: Dict[str, Any], df: pd.DataFrame = None):
        self.profile = profile
        self.quality_report = quality_report
        self.df = df
        self.original_gen = OriginalGen(profile, quality_report)
        self.domain_detector = DomainDetector()
        self.analytics_engine = SimpleAnalytics()
        self.insights_engine = InsightsEngine()
        self.domain_result = None
        self.analytics_result = None
        self.insights = []
        
        if df is not None:
            self.domain_result = self.domain_detector.detect_domain(df)
            self.analytics_result = self.analytics_engine.analyze_dataset(df)
            domain_name = self.domain_result.get('primary_domain') if self.domain_result else None
            self.insights = self.insights_engine.generate_insights(df, domain_name)
    
    def generate_html(self) -> str:
        """Generate original + inject our sections."""
        original_html = self.original_gen.generate_html()
        
        # Find the CLOSING body tag
        body_close_idx = original_html.rfind('</body>')
        
        if body_close_idx < 0:
            return original_html
        
        # Build all our sections
        our_html = ""
        
        if self.domain_result:
            our_html += self._domain_html()
        if self.insights:
            our_html += self._insights_html()
        if self.analytics_result:
            our_html += self._analytics_html()
        
        # Insert BEFORE </body>
        if our_html:
            result = original_html[:body_close_idx] + our_html + original_html[body_close_idx:]
            return result
        
        return original_html
    
    def _domain_html(self) -> str:
        domain = self.domain_result.get('primary_domain', 'Unknown').upper()
        confidence = self.domain_result.get('confidence', 0)
        entities = self.domain_result.get('detected_entities', [])
        all_scores = self.domain_result.get('all_scores', {})
        
        html = '<section><h2>🎯 Domain Intelligence</h2>'
        html += f'<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; color: white; margin-bottom: 20px;"><div style="display: flex; justify-content: space-between;"><div><div style="opacity: 0.9;">Domain</div><div style="font-size: 32px; font-weight: bold;">{domain}</div></div><div style="text-align: right;"><div style="opacity: 0.9;">Confidence</div><div style="font-size: 32px; font-weight: bold;">{confidence:.0%}</div></div></div></div>'
        
        if all_scores:
            html += '<h3>Confidence Scores</h3><div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">'
            for d_name, score_val in sorted(all_scores.items(), key=lambda x: x[1], reverse=True):
                pct = score_val * 100
                bar_color = '#667eea' if score_val > 0 else '#e0e0e0'
                html += f'<div style="margin-bottom: 10px;"><div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 3px;"><span>{d_name.title()}</span><span>{score_val:.1%}</span></div><div style="background: #e0e0e0; height: 6px; border-radius: 3px;"><div style="background: {bar_color}; height: 100%; width: {pct}%;"></div></div></div>'
            html += '</div>'
        
        html += '<h3>Entities</h3><div style="display: flex; flex-wrap: wrap; gap: 10px;">'
        for entity in entities:
            html += f'<span style="background: #667eea; color: white; padding: 6px 12px; border-radius: 16px; font-size: 12px;">{entity}</span>'
        html += '</div></section>'
        
        return html
    
    def _insights_html(self) -> str:
        html = '<section><h2>💡 AI Insights</h2>'
        for i, insight in enumerate(self.insights, 1):
            html += f'<div style="background: #f0f7ff; padding: 12px; margin-bottom: 10px; border-left: 4px solid #667eea; border-radius: 4px;"><strong style="color: #667eea;">Insight {i}:</strong> {insight}</div>'
        html += '</section>  '
        return html
    
    def _analytics_html(self) -> str:
        analytics = self.analytics_result
        summary = analytics.get('summary', {})
        numeric = analytics.get('numeric_analysis', {})
        
        html = '<section><h2>📊 Data Analytics</h2>'
        html += '<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 20px;">'
        html += f'<div style="background: #f8f9fa; padding: 12px; border-radius: 8px; text-align: center;"><div style="font-size: 20px; font-weight: bold; color: #667eea;">{summary.get("rows", 0):,}</div><div style="font-size: 12px; color: #666;">Rows</div></div>'
        html += f'<div style="background: #f8f9fa; padding: 12px; border-radius: 8px; text-align: center;"><div style="font-size: 20px; font-weight: bold; color: #667eea;">{summary.get("columns", 0)}</div><div style="font-size: 12px; color: #666;">Columns</div></div>'
        html += f'<div style="background: #f8f9fa; padding: 12px; border-radius: 8px; text-align: center;"><div style="font-size: 20px; font-weight: bold; color: #667eea;">{summary.get("missing_percentage", 0):.1f}%</div><div style="font-size: 12px; color: #666;">Missing</div></div>'
        html += '</div>'
        
        html += '<h3>Column Statistics</h3>'
        for col_name, stats in list(numeric.items())[:3]:
            html += f'<div style="background: #f8f9fa; padding: 12px; margin-bottom: 8px; border-radius: 8px;"><div style="font-weight: bold; font-size: 12px; margin-bottom: 8px;">{col_name}</div><div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; font-size: 11px;"><div>Mean: {stats["mean"]:.2f}</div><div>Min: {stats["min"]:.2f}</div><div>Max: {stats["max"]:.2f}</div><div>Std: {stats["std_dev"]:.2f}</div></div></div>'
        
        html += '</section>  '
        return html

