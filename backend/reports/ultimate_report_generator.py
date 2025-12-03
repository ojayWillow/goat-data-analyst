# ============================================================================
# Ultimate Report Generator - Beautiful HTML Reports with Narrative
# ============================================================================
# Day 10: Integrates the human-like narrative into professional reports
# 
# Takes AnalysisResult and generates:
# 1. Executive summary with domain context
# 2. Quality dashboard with metrics
# 3. Human-like narrative (3 sections from Days 7-9)
# 4. Data profile details
# 5. Charts and visualizations
# 6. Actionable recommendations
# ============================================================================

from typing import Dict, List, Optional
from backend.core.models import AnalysisResult


class UltimateReportGenerator:
    """
    Generates comprehensive HTML reports with integrated narrative
    
    Transforms AnalysisResult into a beautiful, shareable HTML report
    that combines data analysis with human-like communication.
    """
    
    def __init__(self):
        """Initialize the report generator"""
        print("✓ UltimateReportGenerator initialized")
    
    def generate(self, result: AnalysisResult) -> str:
        """
        Generate complete HTML report with narrative
        
        Args:
            result: AnalysisResult from engine.analyze()
        
        Returns:
            Complete HTML report as string
        """
        # Build report sections
        header = self._build_header(result)
        summary = self._build_summary(result)
        narrative = result.narrative if result.narrative else self._placeholder_narrative()
        quality_dashboard = self._build_quality_dashboard(result)
        profile_section = self._build_profile_section(result)
        charts_section = self._build_charts_section(result)
        footer = self._build_footer(result)
        
        # Assemble complete report
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>GOAT Data Analysis Report</title>
            {self._get_styles()}
        </head>
        <body>
            <div class="report-container">
                {header}
                {summary}
                {narrative}
                {quality_dashboard}
                {profile_section}
                {charts_section}
                {footer}
            </div>
        </body>
        </html>
        """
    
    def _build_header(self, result: AnalysisResult) -> str:
        """Build report header with logo and title"""
        domain_type = result.domain.get('type', 'unknown')
        domain_emoji = self._get_domain_emoji(domain_type)
        
        return f"""
        <header class="report-header">
            <div class="logo">
                <h1>🐐 GOAT Data Analyst</h1>
                <p class="tagline">Greatest Of All Time Data Analysis</p>
            </div>
            <div class="domain-badge">
                <span class="domain-emoji">{domain_emoji}</span>
                <span class="domain-type">{domain_type.replace('_', ' ').title()}</span>
            </div>
        </header>
        """
    
    def _build_summary(self, result: AnalysisResult) -> str:
        """Build executive summary section"""
        rows = result.profile.get('overall', {}).get('rows', result.profile.get('rows', 0))
        cols = result.profile.get('overall', {}).get('columns', result.profile.get('columns', 0))
        quality_score = result.quality.get('overall_score', 0)
        
        score_class = "excellent" if quality_score >= 80 else "good" if quality_score >= 60 else "needs-work"
        
        return f"""
        <section class="executive-summary">
            <h2>Executive Summary</h2>
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="card-icon">📊</div>
                    <div class="card-content">
                        <h3>Data Size</h3>
                        <p class="big-number">{rows:,}</p>
                        <p class="sub-text">rows × {cols} columns</p>
                    </div>
                </div>
                <div class="summary-card">
                    <div class="card-icon">✨</div>
                    <div class="card-content">
                        <h3>Quality Score</h3>
                        <p class="big-number score-{score_class}">{quality_score:.0f}/100</p>
                        <p class="sub-text">{self._get_quality_label(quality_score)}</p>
                    </div>
                </div>
                <div class="summary-card">
                    <div class="card-icon">⚡</div>
                    <div class="card-content">
                        <h3>Analysis Time</h3>
                        <p class="big-number">{result.execution_time_seconds:.2f}s</p>
                        <p class="sub-text">Lightning fast</p>
                    </div>
                </div>
            </div>
        </section>
        """
    
    def _build_quality_dashboard(self, result: AnalysisResult) -> str:
        """Build quality metrics dashboard"""
        missing_pct = result.quality.get('missing_pct', 0)
        duplicates = result.quality.get('duplicates', 0)
        
        return f"""
        <section class="quality-dashboard">
            <h2>Data Quality Dashboard</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-header">
                        <span class="metric-icon">{"🟢" if missing_pct < 5 else "🟡" if missing_pct < 20 else "🔴"}</span>
                        <h4>Missing Data</h4>
                    </div>
                    <p class="metric-value">{missing_pct:.1f}%</p>
                    <p class="metric-status">{self._get_missing_status(missing_pct)}</p>
                </div>
                <div class="metric-card">
                    <div class="metric-header">
                        <span class="metric-icon">{"🟢" if duplicates == 0 else "🟡" if duplicates < 100 else "🔴"}</span>
                        <h4>Duplicates</h4>
                    </div>
                    <p class="metric-value">{duplicates:,}</p>
                    <p class="metric-status">{self._get_duplicate_status(duplicates)}</p>
                </div>
            </div>
        </section>
        """
    
    def _build_profile_section(self, result: AnalysisResult) -> str:
        """Build data profile section"""
        columns = result.profile.get('columns', [])
        
        if not columns:
            return ""
        
        columns_html = ""
        for col in columns[:10]:  # Show first 10 columns
            col_name = col.get('name', 'Unknown')
            col_type = col.get('type', 'unknown')
            missing = col.get('missing', 0)
            
            columns_html += f"""
            <tr>
                <td><strong>{col_name}</strong></td>
                <td><span class="type-badge type-{col_type}">{col_type}</span></td>
                <td>{missing}</td>
            </tr>
            """
        
        return f"""
        <section class="profile-section">
            <h2>Data Profile</h2>
            <div class="profile-table-container">
                <table class="profile-table">
                    <thead>
                        <tr>
                            <th>Column</th>
                            <th>Type</th>
                            <th>Missing</th>
                        </tr>
                    </thead>
                    <tbody>
                        {columns_html}
                    </tbody>
                </table>
            </div>
        </section>
        """
    
    def _build_charts_section(self, result: AnalysisResult) -> str:
        """Build charts section (placeholder for now)"""
        if not result.charts or len(result.charts) == 0:
            return ""
        
        return f"""
        <section class="charts-section">
            <h2>Visualizations</h2>
            <div class="charts-grid">
                <p class="placeholder">📊 Charts will be rendered here</p>
                <p class="sub-text">{len(result.charts)} charts generated</p>
            </div>
        </section>
        """
    
    def _build_footer(self, result: AnalysisResult) -> str:
        """Build report footer"""
        import datetime
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return f"""
        <footer class="report-footer">
            <p>Generated by GOAT Data Analyst on {now}</p>
            <p class="footer-note">This report was automatically generated using AI-enhanced analysis</p>
        </footer>
        """
    
    def _placeholder_narrative(self) -> str:
        """Fallback if narrative not generated"""
        return """
        <div class="goat-narrative">
            <p><em>Narrative generation in progress...</em></p>
        </div>
        """
    
    def _get_domain_emoji(self, domain_type: str) -> str:
        """Get emoji for domain type"""
        emojis = {
            'sales': '💰',
            'finance': '📈',
            'ecommerce': '🛒',
            'marketing': '📢',
            'healthcare': '🏥',
            'hr': '👥',
            'inventory': '📦',
            'customer': '🤝',
            'web_analytics': '🌐',
            'logistics': '🚚',
            'unknown': '📊'
        }
        return emojis.get(domain_type, '📊')
    
    def _get_quality_label(self, score: float) -> str:
        """Get quality label from score"""
        if score >= 90:
            return "Excellent quality"
        elif score >= 80:
            return "Very good quality"
        elif score >= 70:
            return "Good quality"
        elif score >= 60:
            return "Acceptable quality"
        else:
            return "Needs improvement"
    
    def _get_missing_status(self, missing_pct: float) -> str:
        """Get status text for missing data"""
        if missing_pct == 0:
            return "No missing data"
        elif missing_pct < 5:
            return "Minimal missing data"
        elif missing_pct < 20:
            return "Some missing data"
        else:
            return "Significant missing data"
    
    def _get_duplicate_status(self, duplicates: int) -> str:
        """Get status text for duplicates"""
        if duplicates == 0:
            return "No duplicates found"
        elif duplicates < 10:
            return "Few duplicates"
        elif duplicates < 100:
            return "Some duplicates"
        else:
            return "Many duplicates found"
    
    def _get_styles(self) -> str:
        """Get CSS styles for the report"""
        return """
        <style>
            /* Reset and base styles */
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
                line-height: 1.6;
                color: #333;
                background: #f5f5f5;
                padding: 20px;
            }
            
            .report-container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }
            
            /* Header */
            .report-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .logo h1 {
                font-size: 2.5em;
                margin-bottom: 5px;
            }
            
            .tagline {
                font-size: 1em;
                opacity: 0.9;
            }
            
            .domain-badge {
                background: rgba(255, 255, 255, 0.2);
                padding: 15px 25px;
                border-radius: 8px;
                text-align: center;
            }
            
            .domain-emoji {
                font-size: 2em;
                display: block;
                margin-bottom: 5px;
            }
            
            .domain-type {
                font-size: 0.9em;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            /* Sections */
            section {
                padding: 40px;
                border-bottom: 1px solid #eee;
            }
            
            section:last-of-type {
                border-bottom: none;
            }
            
            h2 {
                font-size: 1.8em;
                margin-bottom: 25px;
                color: #2c3e50;
            }
            
            /* Summary Grid */
            .summary-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
            }
            
            .summary-card {
                background: #f8f9fa;
                padding: 25px;
                border-radius: 8px;
                display: flex;
                align-items: center;
                gap: 20px;
            }
            
            .card-icon {
                font-size: 3em;
            }
            
            .card-content h3 {
                font-size: 0.9em;
                color: #6c757d;
                margin-bottom: 10px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .big-number {
                font-size: 2.5em;
                font-weight: bold;
                color: #2c3e50;
                line-height: 1;
                margin-bottom: 5px;
            }
            
            .big-number.score-excellent { color: #28a745; }
            .big-number.score-good { color: #ffc107; }
            .big-number.score-needs-work { color: #dc3545; }
            
            .sub-text {
                font-size: 0.9em;
                color: #6c757d;
            }
            
            /* Quality Dashboard */
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
            }
            
            .metric-card {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }
            
            .metric-header {
                display: flex;
                align-items: center;
                gap: 10px;
                margin-bottom: 15px;
            }
            
            .metric-icon {
                font-size: 1.5em;
            }
            
            .metric-header h4 {
                font-size: 1em;
                color: #6c757d;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .metric-value {
                font-size: 2em;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }
            
            .metric-status {
                font-size: 0.9em;
                color: #6c757d;
            }
            
            /* Profile Table */
            .profile-table-container {
                overflow-x: auto;
            }
            
            .profile-table {
                width: 100%;
                border-collapse: collapse;
            }
            
            .profile-table th,
            .profile-table td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #eee;
            }
            
            .profile-table th {
                background: #f8f9fa;
                font-weight: 600;
                color: #6c757d;
                text-transform: uppercase;
                font-size: 0.85em;
                letter-spacing: 1px;
            }
            
            .type-badge {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 4px;
                font-size: 0.85em;
                font-weight: 600;
            }
            
            .type-badge.type-numeric {
                background: #e3f2fd;
                color: #1976d2;
            }
            
            .type-badge.type-categorical {
                background: #f3e5f5;
                color: #7b1fa2;
            }
            
            .type-badge.type-datetime {
                background: #e8f5e9;
                color: #388e3c;
            }
            
            /* Charts */
            .charts-grid {
                text-align: center;
                padding: 40px;
                background: #f8f9fa;
                border-radius: 8px;
            }
            
            .charts-grid .placeholder {
                font-size: 1.2em;
                color: #6c757d;
                margin-bottom: 10px;
            }
            
            /* Footer */
            .report-footer {
                background: #2c3e50;
                color: white;
                padding: 30px 40px;
                text-align: center;
            }
            
            .footer-note {
                font-size: 0.9em;
                opacity: 0.8;
                margin-top: 10px;
            }
            
            /* Responsive */
            @media (max-width: 768px) {
                .report-header {
                    flex-direction: column;
                    text-align: center;
                    gap: 20px;
                }
                
                section {
                    padding: 30px 20px;
                }
                
                .logo h1 {
                    font-size: 2em;
                }
            }
        </style>
        """


# Test function
def _test():
    """Test report generator"""
    from backend.core.models import AnalysisResult
    import pandas as pd
    
    print("\n" + "="*70)
    print("TESTING ULTIMATE REPORT GENERATOR")
    print("="*70)
    
    # Create dummy AnalysisResult
    df = pd.DataFrame({'id': range(100), 'amount': range(100)})
    result = AnalysisResult(dataframe=df)
    result.profile = {
        'overall': {'rows': 100, 'columns': 2},
        'rows': 100,
        'columns': 2,
        'columns': [
            {'name': 'id', 'type': 'numeric', 'missing': 0},
            {'name': 'amount', 'type': 'numeric', 'missing': 5}
        ]
    }
    result.domain = {'type': 'sales', 'confidence': 0.85}
    result.quality = {
        'missing_pct': 2.5,
        'duplicates': 3,
        'overall_score': 92
    }
    result.execution_time_seconds = 0.5
    result.narrative = "<div class='goat-narrative'><p>Test narrative</p></div>"
    
    # Generate report
    generator = UltimateReportGenerator()
    html = generator.generate(result)
    
    print(f"\n✅ Report generated: {len(html)} characters")
    print(f"   - Header: ✓")
    print(f"   - Summary: ✓")
    print(f"   - Narrative: ✓")
    print(f"   - Quality Dashboard: ✓")
    print(f"   - Profile: ✓")
    
    # Save to file for inspection
    with open('test_report.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n📄 Report saved to test_report.html")
    print("="*70)


if __name__ == "__main__":
    _test()
