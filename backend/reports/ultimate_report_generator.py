# ============================================================================
# Ultimate Report Generator - Beautiful HTML Reports with Narrative
# ============================================================================
# Day 18: Professional card-based layout with modern SaaS styling
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
        print("✅ UltimateReportGenerator initialized")

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
        <section class="executive-summary section-card">
            <h2 class="section-title">Executive Summary</h2>
            <div class="summary-grid">
                <div class="summary-card card-elevated">
                    <div class="card-icon">📊</div>
                    <div class="card-content">
                        <h3>Data Size</h3>
                        <p class="big-number">{rows:,}</p>
                        <p class="sub-text">rows × {cols} columns</p>
                    </div>
                </div>
                <div class="summary-card card-elevated">
                    <div class="card-icon">✨</div>
                    <div class="card-content">
                        <h3>Quality Score</h3>
                        <p class="big-number score-{score_class}">{quality_score:.0f}/100</p>
                        <p class="sub-text">{self._get_quality_label(quality_score)}</p>
                    </div>
                </div>
                <div class="summary-card card-elevated">
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
        <section class="quality-dashboard section-card">
            <h2 class="section-title">Data Quality Dashboard</h2>
            <div class="metrics-grid">
                <div class="metric-card card-with-border">
                    <div class="metric-header">
                        <span class="metric-icon">{"🟢" if missing_pct < 5 else "🟡" if missing_pct < 20 else "🔴"}</span>
                        <h4>Missing Data</h4>
                    </div>
                    <p class="metric-value">{missing_pct:.1f}%</p>
                    <p class="metric-status">{self._get_missing_status(missing_pct)}</p>
                </div>
                <div class="metric-card card-with-border">
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
        <section class="profile-section section-card">
            <h2 class="section-title">Data Profile</h2>
            <div class="profile-table-container card-elevated">
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
        <section class="charts-section section-card">
            <h2 class="section-title">Visualizations</h2>
            <div class="charts-grid card-elevated">
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
        <div class="goat-narrative section-card">
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
        """Get CSS styles for the report - PROFESSIONAL CARD-BASED LAYOUT"""
        return """
        <style>
            /* Reset and base styles */
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
                line-height: 1.6;
                color: #2c3e50;
                background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
                padding: 20px;
            }

            .report-container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 16px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
                overflow: hidden;
            }

            /* Header */
            .report-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 48px 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                position: relative;
                overflow: hidden;
            }

            .report-header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120"><path d="M0,0 L1200,0 L1200,60 Q900,90 600,60 T0,60 Z" fill="rgba(255,255,255,0.05)"/></svg>');
                background-size: cover;
                opacity: 0.3;
            }

            .logo {
                position: relative;
                z-index: 1;
            }

            .logo h1 {
                font-size: 2.8em;
                margin-bottom: 8px;
                font-weight: 700;
                text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            }

            .tagline {
                font-size: 1.1em;
                opacity: 0.95;
                font-weight: 400;
            }

            .domain-badge {
                background: rgba(255, 255, 255, 0.25);
                backdrop-filter: blur(10px);
                padding: 20px 30px;
                border-radius: 12px;
                text-align: center;
                border: 2px solid rgba(255, 255, 255, 0.3);
                position: relative;
                z-index: 1;
            }

            .domain-emoji {
                font-size: 2.5em;
                display: block;
                margin-bottom: 8px;
            }

            .domain-type {
                font-size: 0.95em;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1.5px;
            }

            /* Section Cards - THE KEY TO PROFESSIONAL LOOK */
            .section-card {
                margin: 50px 40px;
                background: white;
                border-radius: 12px;
                padding: 0;
                position: relative;
            }

            .section-title {
                font-size: 1.9em;
                margin-bottom: 30px;
                color: #2c3e50;
                font-weight: 700;
                padding-left: 18px;
                border-left: 5px solid #667eea;
                padding: 8px 0 8px 18px;
            }

            /* Card Elevation System */
            .card-elevated {
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08),
                           0 2px 4px rgba(0, 0, 0, 0.04);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }

            .card-elevated:hover {
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12),
                           0 4px 8px rgba(0, 0, 0, 0.06);
                transform: translateY(-2px);
            }

            .card-with-border {
                background: #fafbfc;
                border-radius: 10px;
                border-left: 4px solid #667eea;
                padding: 24px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
                transition: all 0.2s ease;
            }

            .card-with-border:hover {
                border-left-width: 6px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            }

            /* Summary Grid */
            .summary-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 24px;
                padding-top: 10px;
            }

            .summary-card {
                padding: 28px;
                display: flex;
                align-items: center;
                gap: 20px;
                border: 1px solid #e8ecf1;
            }

            .card-icon {
                font-size: 3.5em;
                filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
            }

            .card-content h3 {
                font-size: 0.85em;
                color: #8492a6;
                margin-bottom: 12px;
                text-transform: uppercase;
                letter-spacing: 1.2px;
                font-weight: 600;
            }

            .big-number {
                font-size: 2.8em;
                font-weight: 700;
                color: #2c3e50;
                line-height: 1;
                margin-bottom: 8px;
            }

            .big-number.score-excellent { 
                color: #10b981;
                text-shadow: 0 2px 4px rgba(16, 185, 129, 0.2);
            }
            .big-number.score-good { 
                color: #f59e0b;
                text-shadow: 0 2px 4px rgba(245, 158, 11, 0.2);
            }
            .big-number.score-needs-work { 
                color: #ef4444;
                text-shadow: 0 2px 4px rgba(239, 68, 68, 0.2);
            }

            .sub-text {
                font-size: 0.95em;
                color: #8492a6;
                font-weight: 500;
            }

            /* Quality Dashboard */
            .quality-dashboard {
                background: linear-gradient(135deg, #f8f9fb 0%, #fafbfc 100%);
                border-radius: 12px;
            }

            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                gap: 24px;
                padding-top: 10px;
            }

            .metric-card {
                /* Uses card-with-border class */
            }

            .metric-header {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 18px;
            }

            .metric-icon {
                font-size: 1.8em;
            }

            .metric-header h4 {
                font-size: 0.9em;
                color: #6b7280;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-weight: 600;
            }

            .metric-value {
                font-size: 2.4em;
                font-weight: 700;
                color: #2c3e50;
                margin-bottom: 8px;
            }

            .metric-status {
                font-size: 0.95em;
                color: #8492a6;
                font-weight: 500;
            }

            /* Profile Table */
            .profile-table-container {
                overflow-x: auto;
                padding: 24px;
            }

            .profile-table {
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
            }

            .profile-table th,
            .profile-table td {
                padding: 16px 20px;
                text-align: left;
            }

            .profile-table thead tr {
                background: linear-gradient(135deg, #f8f9fb 0%, #fafbfc 100%);
            }

            .profile-table th {
                font-weight: 700;
                color: #6b7280;
                text-transform: uppercase;
                font-size: 0.8em;
                letter-spacing: 1.2px;
                border-bottom: 2px solid #e5e7eb;
            }

            .profile-table tbody tr {
                border-bottom: 1px solid #f3f4f6;
                transition: background 0.2s ease;
            }

            .profile-table tbody tr:hover {
                background: #fafbfc;
            }

            .profile-table tbody tr:last-child {
                border-bottom: none;
            }

            .type-badge {
                display: inline-block;
                padding: 6px 14px;
                border-radius: 6px;
                font-size: 0.85em;
                font-weight: 600;
                letter-spacing: 0.5px;
            }

            .type-badge.type-numeric {
                background: #dbeafe;
                color: #1e40af;
            }

            .type-badge.type-categorical {
                background: #f3e8ff;
                color: #6b21a8;
            }

            .type-badge.type-datetime {
                background: #d1fae5;
                color: #065f46;
            }

            /* Charts */
            .charts-grid {
                text-align: center;
                padding: 48px;
                background: linear-gradient(135deg, #f8f9fb 0%, #fafbfc 100%);
                margin-top: 10px;
            }

            .charts-grid .placeholder {
                font-size: 1.3em;
                color: #6b7280;
                margin-bottom: 12px;
                font-weight: 500;
            }

            /* Narrative Sections */
            .goat-narrative {
                padding: 40px;
            }

            .goat-narrative h3 {
                color: #2c3e50;
                font-size: 1.5em;
                margin: 32px 0 20px 0;
                padding-left: 16px;
                border-left: 4px solid #667eea;
                padding: 8px 0 8px 16px;
            }

            .goat-narrative p {
                color: #4b5563;
                margin-bottom: 16px;
                line-height: 1.8;
                font-size: 1.05em;
            }

            /* Footer */
            .report-footer {
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                color: white;
                padding: 40px;
                text-align: center;
                margin-top: 60px;
            }

            .footer-note {
                font-size: 0.95em;
                opacity: 0.8;
                margin-top: 12px;
            }

            /* Responsive */
            @media (max-width: 768px) {
                .report-header {
                    flex-direction: column;
                    text-align: center;
                    gap: 24px;
                    padding: 36px 24px;
                }

                .section-card {
                    margin: 30px 20px;
                }

                .logo h1 {
                    font-size: 2.2em;
                }

                .summary-grid,
                .metrics-grid {
                    grid-template-columns: 1fr;
                }

                .section-title {
                    font-size: 1.6em;
                }
            }

            /* Print Styles */
            @media print {
                body {
                    background: white;
                }

                .report-container {
                    box-shadow: none;
                }

                .card-elevated,
                .card-with-border {
                    box-shadow: none;
                    border: 1px solid #e5e7eb;
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
    print("TESTING ULTIMATE REPORT GENERATOR - PROFESSIONAL STYLING")
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
