"""Report Assembler - Orchestrates sections into final HTML report."""

from typing import Dict, Any, List
from datetime import datetime
from backend.reports.sections.quality_section import QualitySection
from backend.reports.sections.domain_section import DomainSection
from backend.reports.sections.ai_section import AISection
from backend.reports.sections.charts_section import ChartsSection


class ReportAssembler:
    """
    Assembles independent sections into a cohesive HTML report.
    
    This is the final orchestrator - each section is independent,
    and the assembler decides:
    1. Which sections to include
    2. In what order
    3. How to wrap them in HTML
    """
    
    def __init__(self):
        """Initialize all section generators."""
        self.quality = QualitySection()
        self.domain = DomainSection()
        self.ai = AISection()
        self.charts = ChartsSection()
    
    def generate_report(
        self,
        profile: Dict[str, Any],
        domain_data: Dict[str, Any] = None,
        insights_data: Dict[str, Any] = None,
        charts_data: Dict[str, Any] = None,
        config: Dict[str, bool] = None
    ) -> str:
        """
        Generate complete HTML report by assembling sections.
        
        Args:
            profile: Data quality profile from DataProfiler
            domain_data: Domain detection results
            insights_data: AI insights
            charts_data: Visualization HTML snippets
            config: Dict of section inclusion flags:
                - include_header: bool (default: True)
                - include_quality: bool (default: True)
                - include_domain: bool (default: True)
                - include_ai: bool (default: True)
                - include_charts: bool (default: True)
                - include_footer: bool (default: True)
        
        Returns:
            Complete HTML report as string
        """
        
        # Default config - include everything
        if config is None:
            config = {
                "include_header": True,
                "include_quality": True,
                "include_domain": True,
                "include_ai": True,
                "include_charts": True,
                "include_footer": True
            }
        
        # Build sections array (in order)
        sections = []
        
        # Header
        if config.get("include_header", True):
            sections.append(self._build_header(profile))
        
        # Quality section (usually first)
        if config.get("include_quality", True) and profile:
            quality_html = self.quality.generate(profile)
            if quality_html:
                sections.append(quality_html)
        
        # Charts section
        if config.get("include_charts", True) and charts_data:
            charts_html = self.charts.generate(charts_data)
            if charts_html:
                sections.append(charts_html)
        
        # AI Insights section
        if config.get("include_ai", True) and insights_data:
            ai_html = self.ai.generate(insights_data)
            if ai_html:
                sections.append(ai_html)
        
        # Domain section
        if config.get("include_domain", True) and domain_data:
            domain_html = self.domain.generate(domain_data)
            if domain_html:
                sections.append(domain_html)
        
        # Footer
        if config.get("include_footer", True):
            sections.append(self._build_footer())
        
        # Wrap everything in HTML
        html = self._wrap_html("\n".join(sections))
        
        return html
    
    def _build_header(self, profile: Dict[str, Any]) -> str:
        """Build report header."""
        dataset_name = profile.get('dataset_name', 'Unknown Dataset')
        total_rows = profile.get('total_rows', 0)
        total_cols = profile.get('total_columns', 0)
        quality_score = profile.get('quality_score', 0)
        
        quality_color = '#10b981' if quality_score >= 80 else '#f59e0b' if quality_score >= 60 else '#ef4444'
        
        return f"""
        <div class="header">
            <h1>📊 Data Analysis Report</h1>
            <div style="display: flex; gap: 20px; margin-top: 16px; flex-wrap: wrap;">
                <div class="metric-badge">
                    <span class="metric-label">Dataset</span>
                    <span class="metric-value">{dataset_name}</span>
                </div>
                <div class="metric-badge">
                    <span class="metric-label">Rows</span>
                    <span class="metric-value">{total_rows:,}</span>
                </div>
                <div class="metric-badge">
                    <span class="metric-label">Columns</span>
                    <span class="metric-value">{total_cols}</span>
                </div>
                <div class="metric-badge">
                    <span class="metric-label">Quality Score</span>
                    <span class="metric-value" style="color: {quality_color};">{quality_score}/100</span>
                </div>
            </div>
        </div>
        """
    
    def _build_footer(self) -> str:
        """Build report footer."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return f"""
        <div class="footer">
            <p>Generated by GOAT Data Analyst • {timestamp}</p>
            <p style="font-size: 12px; color: #999; margin-top: 8px;">
                This report combines data quality checks, domain detection, 
                AI insights, and visualizations for comprehensive analysis.
            </p>
        </div>
        """
    
    def _wrap_html(self, content: str) -> str:
        """Wrap sections in complete HTML document."""
        
        styles = """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .header h1 {
            font-size: 28px;
            margin-bottom: 8px;
        }
        
        .metric-badge {
            background: #f9fafb;
            padding: 12px 16px;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        
        .metric-label {
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .metric-value {
            font-size: 18px;
            font-weight: 600;
            color: #333;
        }
        
        .card {
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .card h2 {
            font-size: 20px;
            margin-bottom: 16px;
        }
        
        .card h3 {
            font-size: 16px;
            margin-bottom: 12px;
        }
        
        .card-header {
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 16px;
            margin-bottom: 20px;
        }
        
        .card-body {
            line-height: 1.8;
        }
        
        .footer {
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 14px;
            margin-top: 40px;
            border-top: 1px solid #e0e0e0;
        }
        """
        
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>GOAT Data Analysis Report</title>
            <style>
                {styles}
            </style>
        </head>
        <body>
            <div class="container">
                {content}
            </div>
        </body>
        </html>
        """
        
        return html
