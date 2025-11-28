"""
Enhanced Quality Report Generator with Domain Detection & Analytics
"""

from typing import Dict
import pandas as pd
from backend.data_processing.profiler import DataProfiler
from backend.domain_detection.domain_detector import DomainDetector
from backend.analytics.simple_analytics import SimpleAnalytics


class EnhancedQualityReportGenerator:
    """Enhanced reports with domain + analytics intelligence."""
    
    def __init__(self, profile: Dict, quality_report: Dict):
        """Initialize."""
        self.profile = profile
        self.quality_report = quality_report
        self.domain_detector = DomainDetector()
        self.analytics_engine = SimpleAnalytics()
        self.domain_result = None
        self.analytics_result = None
    
    def generate_html(self, output_path: str, df: pd.DataFrame = None) -> str:
        """Generate enhanced HTML report."""
        if df is not None:
            self.domain_result = self.domain_detector.detect_domain(df)
            self.analytics_result = self.analytics_engine.analyze_dataset(df)
        
        html_content = self._build_complete_html()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def _build_complete_html(self) -> str:
        """Build complete HTML report."""
        
        score = self.quality_report.get('score', 0)
        issues = self.quality_report.get('issues', [])
        
        score_color = '#10b981' if score >= 90 else '#f59e0b' if score >= 70 else '#ef4444'
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enhanced Data Quality Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: #f8fafc;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{ font-size: 36px; margin-bottom: 10px; }}
        .content {{ padding: 30px; }}
        .section {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .section h2 {{ 
            font-size: 24px;
            margin-bottom: 20px;
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        .section h3 {{
            font-size: 18px;
            margin: 20px 0 15px 0;
            color: #555;
        }}
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #666;
            margin-top: 8px;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Enhanced Data Quality Report</h1>
            <p>Comprehensive analysis with domain intelligence</p>
        </div>
        
        <div class="content">
            <!-- Quality Score -->
            <div class="section">
                <h2>Overall Quality Score</h2>
                <div style="text-align: center; padding: 30px;">
                    <div style="font-size: 72px; font-weight: bold; color: {score_color};">{score}/100</div>
                    <div style="color: #666; margin-top: 10px;">Data Quality Score</div>
                </div>
            </div>
'''
        
        # Add domain section if available
        if self.domain_result:
            html += self._get_domain_section()
        
        # Add analytics section if available
        if self.analytics_result:
            html += self._get_analytics_section()
        
        # Add dataset overview
        html += self._get_dataset_overview()
        
        # Add issues section
        if issues:
            html += '''
            <div class="section">
                <h2>Quality Issues</h2>
'''
            for issue in issues:
                html += f'<div style="background: #fff3cd; padding: 15px; margin-bottom: 10px; border-left: 4px solid #ffc107; border-radius: 4px;">{issue}</div>'
            html += '</div>'
        
        html += '''
        </div>
    </div>
</body>
</html>'''
        
        return html
    
    def _get_domain_section(self) -> str:
        """Domain intelligence section."""
        if not self.domain_result or self.domain_result.get('primary_domain') == 'unknown':
            return ""
        
        domain = self.domain_result['primary_domain']
        confidence = self.domain_result['confidence']
        entities = self.domain_result.get('detected_entities', [])
        
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
                
                <div class="stat-grid">
                    <div class="stat-card">
                        <div class="stat-value">{len(entities)}</div>
                        <div class="stat-label">Domain Entities</div>
                    </div>
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
    
    def _get_analytics_section(self) -> str:
        """Analytics insights section."""
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
        
        for i, (col_name, stats) in enumerate(list(numeric.items())[:3]):
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
        
        html += '</div>'
        return html
    
    def _get_dataset_overview(self) -> str:
        """Dataset overview section."""
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
