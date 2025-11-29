"""Ultimate Report - Original + Our Features"""

from backend.export_engine.quality_report import QualityReportGenerator as OriginalGen
from backend.domain_detection.domain_detector import DomainDetector
from backend.analytics.simple_analytics import SimpleAnalytics
from backend.analytics.insights_engine import InsightsEngine
import pandas as pd
from typing import Dict, Any, List


class UltimateReportGenerator:
    """Combines original + domain + insights + analytics + AI."""
    
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
        
        # NEW: AI insights attributes
        self.domain = None
        self.analytics_summary = None
        self.ai_insights = []
        
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
        if self.ai_insights:  # NEW: Add AI insights section
            our_html += self._ai_insights_html()
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
        
        # Compact card styling
        html = '<div class="card" style="padding: 20px; margin-bottom: 20px;">'
        html += '<h2 style="margin-bottom: 16px; font-size: 20px;">🎯 Domain Intelligence</h2>'
        
        # Compact header - side by side
        html += f'<div style="display: flex; gap: 20px; margin-bottom: 16px;">'
        html += f'<div style="flex: 1; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 16px; border-radius: 8px; color: white; text-align: center;">'
        html += f'<div style="font-size: 12px; opacity: 0.9; margin-bottom: 4px;">Domain</div>'
        html += f'<div style="font-size: 24px; font-weight: bold;">{domain}</div>'
        html += f'</div>'
        html += f'<div style="flex: 1; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 16px; border-radius: 8px; color: white; text-align: center;">'
        html += f'<div style="font-size: 12px; opacity: 0.9; margin-bottom: 4px;">Confidence</div>'
        html += f'<div style="font-size: 24px; font-weight: bold;">{confidence:.0%}</div>'
        html += f'</div>'
        html += f'</div>'
        
        # Top 3 confidence scores only (compact)
        if all_scores:
            html += '<div style="background: #f8f9fa; padding: 12px; border-radius: 6px; margin-bottom: 12px;">'
            sorted_scores = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)[:3]
            for d_name, score_val in sorted_scores:
                pct = score_val * 100
                bar_color = '#667eea' if score_val > 0 else '#e0e0e0'
                html += f'<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">'
                html += f'<div style="min-width: 100px; font-size: 11px; font-weight: 600;">{d_name.title()}</div>'
                html += f'<div style="flex: 1; background: #e0e0e0; height: 4px; border-radius: 2px;"><div style="background: {bar_color}; height: 100%; width: {pct}%;"></div></div>'
                html += f'<div style="min-width: 40px; text-align: right; font-size: 11px; font-weight: 600;">{score_val:.0%}</div>'
                html += f'</div>'
            html += '</div>'
        
        # Entities - compact badges
        if entities:
            html += '<div style="display: flex; flex-wrap: wrap; gap: 6px;">'
            for entity in entities[:8]:  # Limit to 8 entities
                html += f'<span style="background: #667eea; color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px;">{entity}</span>'
            if len(entities) > 8:
                html += f'<span style="background: #e0e0e0; color: #666; padding: 4px 10px; border-radius: 12px; font-size: 11px;">+{len(entities) - 8} more</span>'
            html += '</div>'
        
        html += '</div>'
        return html
    
    def _insights_html(self) -> str:
        # Compact insights (rule-based)
        html = '<div class="card" style="padding: 20px; margin-bottom: 20px;">'
        html += '<h2 style="margin-bottom: 12px; font-size: 20px;">💡 Rule-Based Insights</h2>'
        
        # Show max 3 insights, compact format
        for i, insight in enumerate(self.insights[:3], 1):
            html += f'<div style="background: #fff4e6; padding: 10px; margin-bottom: 8px; border-left: 3px solid #ff9800; border-radius: 4px; font-size: 13px;">'
            html += f'<strong style="color: #ff9800;">{i}.</strong> {insight}'
            html += f'</div>'
        
        if len(self.insights) > 3:
            html += f'<div style="text-align: center; color: #666; font-size: 12px; margin-top: 8px;">+{len(self.insights) - 3} more insights</div>'
        
        html += '</div>'
        return html
    
    def _ai_insights_html(self) -> str:
        """NEW: AI-generated insights section"""
        html = '<div class="card" style="padding: 20px; margin-bottom: 20px; background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);">'
        html += '<h2 style="margin-bottom: 12px; font-size: 20px;">🤖 AI-Powered Insights</h2>'
        html += '<div style="font-size: 11px; color: #666; margin-bottom: 12px;">Generated by Groq Llama 3.3 70B</div>'
        
        # Show all AI insights
        for i, insight in enumerate(self.ai_insights, 1):
            # Clean up numbered format if AI already added numbers
            clean_insight = insight
            if insight.strip().startswith(f'{i}.'):
                clean_insight = insight.split('.', 1)[1].strip()
            
            html += f'<div style="background: white; padding: 12px; margin-bottom: 10px; border-left: 4px solid #667eea; border-radius: 6px; font-size: 13px; line-height: 1.6;">'
            html += f'<strong style="color: #667eea;">#{i}</strong> {clean_insight}'
            html += f'</div>'
        
        html += '</div>'
        return html
    
    def _analytics_html(self) -> str:
        analytics = self.analytics_result
        summary = analytics.get('summary', {})
        numeric = analytics.get('numeric_analysis', {})
        
        # Compact analytics
        html = '<div class="card" style="padding: 20px; margin-bottom: 20px;">'
        html += '<h2 style="margin-bottom: 12px; font-size: 20px;">📊 Data Analytics</h2>'
        
        # Compact stats grid
        html += '<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 12px;">'
        html += f'<div style="background: #f8f9fa; padding: 10px; border-radius: 6px; text-align: center;">'
        html += f'<div style="font-size: 18px; font-weight: bold; color: #667eea;">{summary.get("rows", 0):,}</div>'
        html += f'<div style="font-size: 10px; color: #666; margin-top: 2px;">Rows</div></div>'
        
        html += f'<div style="background: #f8f9fa; padding: 10px; border-radius: 6px; text-align: center;">'
        html += f'<div style="font-size: 18px; font-weight: bold; color: #667eea;">{summary.get("columns", 0)}</div>'
        html += f'<div style="font-size: 10px; color: #666; margin-top: 2px;">Columns</div></div>'
        
        html += f'<div style="background: #f8f9fa; padding: 10px; border-radius: 6px; text-align: center;">'
        html += f'<div style="font-size: 18px; font-weight: bold; color: #667eea;">{summary.get("missing_percentage", 0):.1f}%</div>'
        html += f'<div style="font-size: 10px; color: #666; margin-top: 2px;">Missing</div></div>'
        
        # Add memory usage
        total_memory = summary.get("memory_usage_mb", 0)
        html += f'<div style="background: #f8f9fa; padding: 10px; border-radius: 6px; text-align: center;">'
        html += f'<div style="font-size: 18px; font-weight: bold; color: #667eea;">{total_memory:.1f}MB</div>'
        html += f'<div style="font-size: 10px; color: #666; margin-top: 2px;">Memory</div></div>'
        
        html += '</div>'
        
        # Show only 2 columns stats (most compact)
        if numeric:
            for col_name, stats in list(numeric.items())[:2]:
                html += f'<div style="background: #f8f9fa; padding: 10px; margin-bottom: 6px; border-radius: 6px;">'
                html += f'<div style="font-weight: 600; font-size: 11px; margin-bottom: 6px; color: #667eea;">{col_name}</div>'
                html += f'<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; font-size: 10px; color: #666;">'
                html += f'<div>avg: {stats["mean"]:.1f}</div>'
                html += f'<div>min: {stats["min"]:.1f}</div>'
                html += f'<div>max: {stats["max"]:.1f}</div>'
                html += f'<div>std: {stats["std_dev"]:.1f}</div>'
                html += f'</div></div>'
        
        html += '</div>'
        return html
