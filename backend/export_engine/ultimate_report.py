import pandas as pd
from backend.export_engine.quality_report import QualityReportGenerator
from backend.domain_detection.domain_detector import DomainDetector
from backend.analytics.simple_analytics import SimpleAnalytics
from backend.analytics.insights_engine import InsightsEngine
from backend.analytics.ai_insights import AIInsightsEngine
from backend.visualizations.universal_charts import UniversalChartGenerator
from backend.reports.sections.domain_section import DomainSection
from backend.reports.sections.ai_section import AISection


class UltimateReportGenerator:
    """
    The Grand Unifier - orchestrates all analysis components
    and generates a cohesive, beautiful HTML report.
    """
    
    def __init__(self):
        self.quality_gen = QualityReportGenerator()
        self.domain_section = DomainSection()
        self.ai_section = AISection()
        
        # Data containers
        self.df = None
        self.profile = None
        self.domain_result = None
        self.analytics = None
        self.ai_insights = None
        self.charts = {}
    
    def generate_report(
        self,
        df: pd.DataFrame,
        profile: dict,
        domain_result: dict = None,
        analytics: dict = None,
        ai_insights: dict = None,
        include_charts: bool = True
    ) -> str:
        """
        Generate the ultimate analysis report.
        
        Args:
            df: The dataset
            profile: Data profile from DataProfiler
            domain_result: Domain detection results
            analytics: Analytics from SimpleAnalytics
            ai_insights: AI-generated insights
            include_charts: Whether to include visualizations
        
        Returns:
            Complete HTML report as string
        """
        self.df = df
        self.profile = profile
        self.domain_result = domain_result
        self.analytics = analytics
        self.ai_insights = ai_insights
        
        # Generate charts if requested
        if include_charts:
            self._generate_charts()
        
        # Build the report
        html = self._build_html()
        
        return html
    
    def _generate_charts(self):
        """Generate all visualizations."""
        chart_gen = UniversalChartGenerator()
        
        try:
            # Try to generate various chart types
            self.charts['time_series'] = chart_gen.create_time_series_chart(
                self.df, 
                self.profile
            )
        except:
            pass
        
        try:
            self.charts['top_n'] = chart_gen.create_top_n_chart(
                self.df,
                self.profile
            )
        except:
            pass
        
        try:
            self.charts['distribution'] = chart_gen.create_distribution_chart(
                self.df,
                self.profile
            )
        except:
            pass
        
        try:
            self.charts['correlation'] = chart_gen.create_correlation_heatmap(
                self.df,
                self.profile
            )
        except:
            pass
    
    def _build_html(self) -> str:
        """Build the complete HTML report."""
        quality_score = self.profile.get('quality_score', 0)
        
        # Determine layout based on quality
        if quality_score < 60:
            main_sections = self._build_poor_data_layout()
        else:
            main_sections = self._build_good_data_layout()
        
        # Wrap everything in HTML structure
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Data Analysis Report</title>
            <style>
                {self._get_styles()}
            </style>
        </head>
        <body>
            <div class="container">
                {self._header()}
                {main_sections}
                {self._footer()}
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _build_poor_data_layout(self) -> str:
        """Layout for poor quality data - quality issues first."""
        html = ""
        html += self._quality_html()
        if self.charts:
            html += self._charts_html()
        if self.ai_insights or self.analytics:
            html += self._combined_insights_html(focus_on_quality=True)
        return html
    
    def _build_good_data_layout(self) -> str:
        """Layout for good quality data - insights first."""
        html = ""
        html += self._executive_summary()
        if self.charts:
            html += self._charts_html()
        if self.ai_insights or self.analytics:
            html += self._combined_insights_html(focus_on_quality=False)
        if self.domain_result:
            html += self._domain_html()
        return html
    
    def _header(self) -> str:
        """Report header."""
        dataset_name = self.profile.get('dataset_name', 'Unknown Dataset')
        total_rows = self.profile.get('total_rows', 0)
        total_cols = self.profile.get('total_columns', 0)
        quality_score = self.profile.get('quality_score', 0)
        
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
    
    def _executive_summary(self) -> str:
        """Executive summary card."""
        quality_score = self.profile.get('quality_score', 0)
        total_rows = self.profile.get('total_rows', 0)
        
        summary_text = f"This dataset contains {total_rows:,} rows with a quality score of {quality_score}/100. "
        
        if quality_score >= 80:
            summary_text += "Data quality is excellent and ready for analysis."
        elif quality_score >= 60:
            summary_text += "Data quality is good with minor issues to address."
        else:
            summary_text += "Data quality needs attention before detailed analysis."
        
        return f"""
        <div class="card">
            <h2 style="margin-bottom: 16px; font-size: 20px;">📋 Executive Summary</h2>
            <p style="line-height: 1.6; color: #333;">{summary_text}</p>
        </div>
        """
    
    def _quality_html(self) -> str:
        """Quality report section."""
        return self.quality_gen.generate_html_report(self.profile)
    
    def _combined_insights_html(self, focus_on_quality: bool = False) -> str:
        """Combine AI and rule-based insights - using modular approach."""
        insights_list = []
        
        # Get AI insights
        if self.ai_insights:
            ai_text = self.ai_insights.get("insights", "")
            if ai_text:
                # Split into numbered list if it's a string
                if isinstance(ai_text, str):
                    insights_list = [line.strip() for line in ai_text.split('\n') if line.strip()]
                else:
                    insights_list = ai_text
        
        # Get rule-based insights
        if self.analytics and not focus_on_quality:
            rule_insights = self.analytics.get("insights", [])
            if rule_insights:
                insights_list.extend(rule_insights[:3])  # Add top 3 rule-based
        
        if not insights_list:
            return ""
        
        # Prepare data for AI section
        insights_data = {
            "insights": insights_list,
            "model": "Groq Llama",
            "timestamp": ""
        }
        
        # Use modular section
        return self.ai_section.generate(insights_data)
    
    def _domain_html(self):
        """Domain intelligence section - using modular approach."""
        if not self.domain_result:
            return ""
        
        # Prepare data for domain section
        domain_data = {
            "detected_domain": self.domain_result.get("primary_domain", "Unknown"),
            "confidence": self.domain_result.get("confidence", 0),
            "key_entities": self.domain_result.get("key_entities", []),
            "top_domains": self.domain_result.get("top_domains", [])
        }
        
        # Use modular section
        return self.domain_section.generate(domain_data)
    
    def _charts_html(self) -> str:
        """Visualizations section."""
        if not self.charts:
            return ""
        
        html = '<div class="card">'
        html += '<h2 style="margin-bottom: 16px; font-size: 20px;">📈 Visualizations</h2>'
        
        for chart_type, chart_html in self.charts.items():
            if chart_html:
                html += f'<div style="margin-bottom: 24px;">{chart_html}</div>'
        
        html += '</div>'
        return html
    
    def _footer(self) -> str:
        """Report footer."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return f"""
        <div class="footer">
            <p>Generated by GOAT Data Analyst • {timestamp}</p>
        </div>
        """
    
    def _get_styles(self) -> str:
        """CSS styles for the report."""
        return """
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
        
        .footer {
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 14px;
        }
        """
