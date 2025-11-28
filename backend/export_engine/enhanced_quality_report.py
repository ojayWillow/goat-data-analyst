"""
Enhanced Quality Report - Complete with Domain Confidence Chart
"""

from typing import Dict
import pandas as pd
from backend.domain_detection.domain_detector import DomainDetector
from backend.analytics.simple_analytics import SimpleAnalytics
from backend.analytics.insights_engine import InsightsEngine


class EnhancedQualityReportGenerator:
    """Complete report generator."""
    
    def __init__(self, profile: Dict, quality_report: Dict):
        self.profile = profile
        self.quality_report = quality_report
        self.domain_detector = DomainDetector()
        self.analytics_engine = SimpleAnalytics()
        self.insights_engine = InsightsEngine()
        self.domain_result = None
        self.analytics_result = None
        self.insights = []
    
    def generate_html(self, output_path: str, df: pd.DataFrame = None) -> str:
        if df is not None:
            self.domain_result = self.domain_detector.detect_domain(df)
            self.analytics_result = self.analytics_engine.analyze_dataset(df)
            domain_name = self.domain_result.get('primary_domain') if self.domain_result else None
            self.insights = self.insights_engine.generate_insights(df, domain_name)
        
        html = self._build_html()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return output_path
    
    def _build_html(self) -> str:
        score = self.quality_report.get('score', 0)
        score_color = '#10b981' if score >= 90 else '#f59e0b' if score >= 70 else '#ef4444'
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enhanced Data Quality Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; min-height: 100vh; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: #f8fafc; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }}
        .header h1 {{ font-size: 36px; margin-bottom: 10px; }}
        .content {{ padding: 30px; }}
        .section {{ background: white; border-radius: 12px; padding: 25px; margin-bottom: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .section h2 {{ font-size: 24px; margin-bottom: 20px; color: #333; border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
        .section h3 {{ font-size: 18px; margin: 20px 0 15px 0; color: #555; }}
        .stat-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 20px; border-radius: 8px; text-align: center; }}
        .stat-value {{ font-size: 32px; font-weight: bold; color: #667eea; }}
        .stat-label {{ color: #666; margin-top: 8px; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Enhanced Data Quality Report</h1>
            <p>Comprehensive analysis with AI intelligence</p>
        </div>
        
        <div class="content">
            <!-- Quality Score -->
            <div class="section">
                <h2>Overall Quality Score</h2>
                <div style="text-align: center; padding: 30px;">
                    <div style="font-size: 72px; font-weight: bold; color: {score_color};">{score}/100</div>
                </div>
            </div>
'''
        
        # Domain section with chart
        if self.domain_result:
            html += self._domain_section_html()
        
        # AI Insights
        if self.insights:
            html += self._insights_section_html()
        
        # Analytics
        if self.analytics_result:
            html += self._analytics_section_html()
        
        # Dataset Overview
        html += self._dataset_overview_html()
        
        html += '''
        </div>
    </div>
</body>
</html>'''
        return html
    
    def _domain_section_html(self) -> str:
        domain = self.domain_result['primary_domain']
        confidence = self.domain_result['confidence']
        entities = self.domain_result.get('detected_entities', [])
        all_scores = self.domain_result.get('all_scores', {})
        
        html = f'''
            <div class="section">
                <h2>Domain Intelligence</h2>
                
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 12px; color: white; margin-bottom: 25px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 16px; opacity: 0.9;">Detected Domain</div>
                            <div style="font-size: 42px; font-weight: bold; margin-top: 8px;">{domain.upper()}</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 16px; opacity: 0.9;">Confidence</div>
                            <div style="font-size: 42px; font-weight: bold; margin-top: 8px;">{confidence:.0%}</div>
                        </div>
                    </div>
                </div>
                
                <h3>Domain Confidence Scores</h3>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
'''
        
        # Add bars
        if all_scores:
            for d_name, score_val in sorted(all_scores.items(), key=lambda x: x[1], reverse=True):
                pct = score_val * 100
                bar_color = '#667eea' if score_val > 0 else '#e0e0e0'
                weight = 'bold' if d_name.lower() == domain.lower() else 'normal'
                
                html += f'''
                    <div style="margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                            <span style="font-weight: {weight};">{d_name.replace("-", " ").title()}</span>
                            <span style="font-weight: bold;">{score_val:.1%}</span>
                        </div>
                        <div style="background: #e0e0e0; border-radius: 4px; height: 8px;">
                            <div style="background: {bar_color}; height: 100%; width: {pct}%;"></div>
                        </div>
                    </div>
'''
        
        html += '''
                </div>
                
                <h3>Detected Entities</h3>
                <div style="display: flex; flex-wrap: wrap; gap: 10px;">
'''
        
        for entity in entities:
            html += f'<span style="background: #667eea; color: white; padding: 8px 16px; border-radius: 20px; font-size: 14px;">{entity}</span>'
        
        html += '''
                </div>
            </div>
'''
        return html
    
    def _insights_section_html(self) -> str:
        html = '''
            <div class="section">
                <h2>AI Insights</h2>
'''
        for i, insight in enumerate(self.insights, 1):
            html += f'''
                <div style="background: #f0f7ff; padding: 15px; margin-bottom: 12px; border-left: 4px solid #667eea; border-radius: 4px;">
                    <span style="font-weight: bold; color: #667eea;">Insight {i}:</span> {insight}
                </div>
'''
        html += '''
            </div>
'''
        return html
    
    def _analytics_section_html(self) -> str:
        analytics = self.analytics_result
        summary = analytics.get('summary', {})
        numeric = analytics.get('numeric_analysis', {})
        
        html = f'''
            <div class="section">
                <h2>Data Analytics</h2>
                
                <div class="stat-grid">
                    <div class="stat-card">
                        <div class="stat-value">{summary.get('rows', 0):,}</div>
                        <div class="stat-label">Total Rows</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{summary.get('columns', 0)}</div>
                        <div class="stat-label">Total Columns</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{summary.get('missing_percentage', 0):.1f}%</div>
                        <div class="stat-label">Missing Data</div>
                    </div>
                </div>
                
                <h3>Numeric Columns (Sample)</h3>
'''
        
        for col_name, stats in list(numeric.items())[:3]:
            html += f'''
                <div style="background: #f8f9fa; padding: 15px; margin-bottom: 10px; border-radius: 8px;">
                    <div style="font-weight: bold; margin-bottom: 10px;">{col_name}</div>
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; font-size: 14px;">
                        <div>Mean: {stats['mean']:.2f}</div>
                        <div>Min: {stats['min']:.2f}</div>
                        <div>Max: {stats['max']:.2f}</div>
                        <div>Std Dev: {stats['std_dev']:.2f}</div>
                    </div>
                </div>
'''
        
        html += '''
            </div>
'''
        return html
    
    def _dataset_overview_html(self) -> str:
        row_count = self.domain_result.get('row_count', 0) if self.domain_result else 0
        col_count = len(self.profile.get('columns', {}))
        
        return f'''
            <div class="section">
                <h2>Dataset Overview</h2>
                <div class="stat-grid">
                    <div class="stat-card">
                        <div class="stat-value">{row_count:,}</div>
                        <div class="stat-label">Total Rows</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{col_count}</div>
                        <div class="stat-label">Total Columns</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{self.quality_report.get('score', 0)}</div>
                        <div class="stat-label">Quality Score</div>
                    </div>
                </div>
            </div>
'''
