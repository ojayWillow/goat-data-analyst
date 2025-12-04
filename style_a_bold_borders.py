# Style A: Bold Accent Borders
# Each section gets a unique colored top border (4px thick)

from typing import Dict, List, Optional
from backend.core.models import AnalysisResult


class UltimateReportGenerator:
    def __init__(self):
        print("✅ Style A: Bold Accent Borders")

    def generate(self, result: AnalysisResult) -> str:
        header = self._build_header(result)
        summary = self._build_summary(result)
        narrative = result.narrative if result.narrative else self._placeholder_narrative()
        quality_dashboard = self._build_quality_dashboard(result)
        profile_section = self._build_profile_section(result)
        charts_section = self._build_charts_section(result)
        footer = self._build_footer(result)

        return f""\"
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>GOAT Data Analysis Report - Style A</title>
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
        ""\"

    def _build_header(self, result: AnalysisResult) -> str:
        domain_type = result.domain.get('type', 'unknown')
        domain_emoji = self._get_domain_emoji(domain_type)
        return f""\"
        <header class="report-header">
            <div class="logo">
                <h1>🐐 GOAT Data Analyst</h1>
                <p class="tagline">Style A: Bold Accent Borders</p>
            </div>
            <div class="domain-badge">
                <span class="domain-emoji">{domain_emoji}</span>
                <span class="domain-type">{domain_type.replace('_', ' ').title()}</span>
            </div>
        </header>
        ""\"

    def _build_summary(self, result: AnalysisResult) -> str:
        rows = result.profile.get('overall', {}).get('rows', result.profile.get('rows', 0))
        cols = result.profile.get('overall', {}).get('columns', result.profile.get('columns', 0))
        quality_score = result.quality.get('overall_score', 0)
        score_class = "excellent" if quality_score >= 80 else "good" if quality_score >= 60 else "needs-work"

        return f""\"
        <section class="section-bordered section-purple">
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
        ""\"

    def _build_quality_dashboard(self, result: AnalysisResult) -> str:
        missing_pct = result.quality.get('missing_pct', 0)
        duplicates = result.quality.get('duplicates', 0)
        return f""\"
        <section class="section-bordered section-green">
            <h2 class="section-title">Data Quality Dashboard</h2>
            <div class="metrics-grid">
                <div class="metric-card card-elevated">
                    <div class="metric-header">
                        <span class="metric-icon">{"🟢" if missing_pct < 5 else "🟡" if missing_pct < 20 else "🔴"}</span>
                        <h4>Missing Data</h4>
                    </div>
                    <p class="metric-value">{missing_pct:.1f}%</p>
                    <p class="metric-status">{self._get_missing_status(missing_pct)}</p>
                </div>
                <div class="metric-card card-elevated">
                    <div class="metric-header">
                        <span class="metric-icon">{"🟢" if duplicates == 0 else "🟡" if duplicates < 100 else "🔴"}</span>
                        <h4>Duplicates</h4>
                    </div>
                    <p class="metric-value">{duplicates:,}</p>
                    <p class="metric-status">{self._get_duplicate_status(duplicates)}</p>
                </div>
            </div>
        </section>
        ""\"

    def _build_profile_section(self, result: AnalysisResult) -> str:
        columns = result.profile.get('columns', [])
        if not columns:
            return ""
        columns_html = ""
        for col in columns[:10]:
            col_name = col.get('name', 'Unknown')
            col_type = col.get('type', 'unknown')
            missing = col.get('missing', 0)
            columns_html += f""\"
            <tr>
                <td><strong>{col_name}</strong></td>
                <td><span class="type-badge type-{col_type}">{col_type}</span></td>
                <td>{missing}</td>
            </tr>
            ""\"
        return f""\"
        <section class="section-bordered section-blue">
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
        ""\"

    def _build_charts_section(self, result: AnalysisResult) -> str:
        if not result.charts or len(result.charts) == 0:
            return ""
        return f""\"
        <section class="section-bordered section-orange">
            <h2 class="section-title">Visualizations</h2>
            <div class="charts-grid card-elevated">
                <p class="placeholder">📊 Charts will be rendered here</p>
                <p class="sub-text">{len(result.charts)} charts generated</p>
            </div>
        </section>
        ""\"

    def _build_footer(self, result: AnalysisResult) -> str:
        import datetime
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f""\"
        <footer class="report-footer">
            <p>Generated by GOAT Data Analyst on {now}</p>
            <p class="footer-note">Style A: Bold Accent Borders</p>
        </footer>
        ""\"

    def _placeholder_narrative(self) -> str:
        return ""\"<div class="goat-narrative section-bordered section-cyan"><p><em>Narrative generation in progress...</em></p></div>""\"

    def _get_domain_emoji(self, domain_type: str) -> str:
        emojis = {'sales': '💰', 'finance': '📈', 'ecommerce': '🛒', 'marketing': '📢', 'healthcare': '🏥', 'hr': '👥', 'inventory': '📦', 'customer': '🤝', 'web_analytics': '🌐', 'logistics': '🚚', 'unknown': '📊'}
        return emojis.get(domain_type, '📊')

    def _get_quality_label(self, score: float) -> str:
        if score >= 90: return "Excellent quality"
        elif score >= 80: return "Very good quality"
        elif score >= 70: return "Good quality"
        elif score >= 60: return "Acceptable quality"
        else: return "Needs improvement"

    def _get_missing_status(self, missing_pct: float) -> str:
        if missing_pct == 0: return "No missing data"
        elif missing_pct < 5: return "Minimal missing data"
        elif missing_pct < 20: return "Some missing data"
        else: return "Significant missing data"

    def _get_duplicate_status(self, duplicates: int) -> str:
        if duplicates == 0: return "No duplicates found"
        elif duplicates < 10: return "Few duplicates"
        elif duplicates < 100: return "Some duplicates"
        else: return "Many duplicates found"

    def _get_styles(self) -> str:
        return ""\"
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: #f5f7fa;
                padding: 20px;
            }
            .report-container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 16px;
                overflow: hidden;
                box-shadow: 0 10px 40px rgba(0,0,0,0.08);
            }
            .report-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 48px 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .logo h1 { font-size: 2.8em; margin-bottom: 8px; font-weight: 700; }
            .tagline { font-size: 1.1em; opacity: 0.95; }
            .domain-badge {
                background: rgba(255,255,255,0.25);
                padding: 20px 30px;
                border-radius: 12px;
                text-align: center;
            }
            .domain-emoji { font-size: 2.5em; display: block; margin-bottom: 8px; }
            .domain-type { font-size: 0.95em; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; }

            /* BOLD BORDER SECTIONS - KEY FEATURE */
            .section-bordered {
                margin: 50px 40px;
                padding: 35px;
                background: white;
                border-radius: 12px;
                border-top: 5px solid #ccc;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            }
            .section-purple { border-top-color: #667eea; }
            .section-green { border-top-color: #10b981; }
            .section-blue { border-top-color: #3b82f6; }
            .section-orange { border-top-color: #f59e0b; }
            .section-cyan { border-top-color: #06b6d4; }

            .section-title {
                font-size: 1.9em;
                margin-bottom: 30px;
                color: #2c3e50;
                font-weight: 700;
            }
            .card-elevated {
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                transition: all 0.3s ease;
            }
            .card-elevated:hover {
                box-shadow: 0 8px 24px rgba(0,0,0,0.12);
                transform: translateY(-2px);
            }
            .summary-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 24px;
            }
            .summary-card {
                padding: 28px;
                display: flex;
                align-items: center;
                gap: 20px;
                border: 1px solid #e8ecf1;
            }
            .card-icon { font-size: 3.5em; }
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
            .big-number.score-excellent { color: #10b981; }
            .big-number.score-good { color: #f59e0b; }
            .big-number.score-needs-work { color: #ef4444; }
            .sub-text { font-size: 0.95em; color: #8492a6; font-weight: 500; }

            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                gap: 24px;
            }
            .metric-card { padding: 24px; }
            .metric-header {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 18px;
            }
            .metric-icon { font-size: 1.8em; }
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
            .metric-status { font-size: 0.95em; color: #8492a6; font-weight: 500; }

            .profile-table-container { overflow-x: auto; padding: 24px; }
            .profile-table {
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
            }
            .profile-table th, .profile-table td {
                padding: 16px 20px;
                text-align: left;
            }
            .profile-table thead tr { background: #f8f9fb; }
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
            .profile-table tbody tr:hover { background: #fafbfc; }
            .type-badge {
                display: inline-block;
                padding: 6px 14px;
                border-radius: 6px;
                font-size: 0.85em;
                font-weight: 600;
            }
            .type-badge.type-numeric { background: #dbeafe; color: #1e40af; }
            .type-badge.type-categorical { background: #f3e8ff; color: #6b21a8; }
            .type-badge.type-datetime { background: #d1fae5; color: #065f46; }

            .charts-grid {
                text-align: center;
                padding: 48px;
                background: #f8f9fb;
            }
            .charts-grid .placeholder {
                font-size: 1.3em;
                color: #6b7280;
                margin-bottom: 12px;
                font-weight: 500;
            }

            .goat-narrative { padding: 35px; }
            .goat-narrative h3 {
                color: #2c3e50;
                font-size: 1.5em;
                margin: 32px 0 20px 0;
            }
            .goat-narrative p {
                color: #4b5563;
                margin-bottom: 16px;
                line-height: 1.8;
                font-size: 1.05em;
            }

            /* ========================================
               NARRATIVE SECTIONS - BOLD BORDER THEME
               ======================================== */
            
            .goat-narrative {
                margin: 50px 40px;
                padding: 0;
            }

            .narrative-section {
                margin-bottom: 40px;
                padding: 30px;
                background: white;
                border-radius: 12px;
                border-top: 5px solid;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            }

            .context-section {
                border-top-color: #06b6d4;
            }

            .pain-points-section {
                border-top-color: #f59e0b;
            }

            .action-plan-section {
                border-top-color: #10b981;
            }

            .narrative-heading {
                font-size: 1.7em;
                margin-bottom: 20px;
                color: #2c3e50;
                font-weight: 700;
            }

            .narrative-content p {
                color: #4b5563;
                margin-bottom: 14px;
                line-height: 1.7;
                font-size: 1.02em;
            }

            .narrative-content strong {
                color: #2c3e50;
                font-weight: 600;
            }

            .quality-score-display {
                margin-bottom: 20px;
                padding: 15px 20px;
                background: #f8f9fb;
                border-radius: 10px;
                border: 1px solid #e5e7eb;
            }

            .quality-score {
                font-size: 1.3em;
                font-weight: 700;
            }

            .quality-score.score-good { color: #10b981; }
            .quality-score.score-okay { color: #f59e0b; }
            .quality-score.score-poor { color: #ef4444; }

            .pain-points-list {
                display: flex;
                flex-direction: column;
                gap: 16px;
            }

            .pain-point {
                background: white;
                border-left: 4px solid;
                border-radius: 8px;
                padding: 16px 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.06);
                transition: all 0.3s ease;
            }

            .pain-point:hover {
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                transform: translateX(4px);
            }

            .pain-point-critical {
                border-left-color: #ef4444;
                background: #fef2f2;
            }

            .pain-point-high {
                border-left-color: #f59e0b;
                background: #fffbeb;
            }

            .pain-point-medium {
                border-left-color: #fbbf24;
                background: #fefce8;
            }

            .pain-point-low {
                border-left-color: #10b981;
                background: #f0fdf4;
            }

            .pain-point-header {
                margin-bottom: 12px;
                display: flex;
                align-items: center;
                gap: 10px;
                flex-wrap: wrap;
            }

            .severity-badge {
                display: inline-block;
                padding: 4px 10px;
                border-radius: 6px;
                font-size: 0.75em;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }

            .severity-critical {
                background: #fee2e2;
                color: #991b1b;
                border: 1px solid #ef4444;
            }

            .severity-high {
                background: #fef3c7;
                color: #92400e;
                border: 1px solid #f59e0b;
            }

            .severity-medium {
                background: #fef9c3;
                color: #854d0e;
                border: 1px solid #fbbf24;
            }

            .severity-low {
                background: #d1fae5;
                color: #065f46;
                border: 1px solid #10b981;
            }

            .pain-point-title {
                color: #2c3e50;
                font-size: 1.05em;
            }

            .pain-point-body {
                font-size: 0.95em;
                color: #6b7280;
                line-height: 1.6;
            }

            .pain-point-body p {
                margin: 8px 0;
            }

            .pain-impact { color: #dc2626; }
            .pain-fix { color: #059669; }

            .action-intro {
                font-size: 1.05em;
                margin-bottom: 20px;
                padding: 12px 16px;
                background: #f0fdf4;
                border-radius: 8px;
                border-left: 3px solid #10b981;
            }

            .action-steps-list {
                list-style: none;
                counter-reset: action-counter;
                padding: 0;
            }

            .action-step {
                counter-increment: action-counter;
                position: relative;
                padding: 14px 14px 14px 50px;
                margin-bottom: 12px;
                background: #f8f9fb;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
                transition: all 0.3s ease;
                line-height: 1.6;
            }

            .action-step:hover {
                background: white;
                border-color: #10b981;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                transform: translateX(4px);
            }

            .action-step::before {
                content: counter(action-counter);
                position: absolute;
                left: 14px;
                top: 50%;
                transform: translateY(-50%);
                width: 28px;
                height: 28px;
                background: linear-gradient(135deg, #10b981, #059669);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
                font-size: 0.9em;
                color: white;
                box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
            }

            .report-footer {
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                color: white;
                padding: 40px;
                text-align: center;
                margin-top: 60px;
            }
            .footer-note { font-size: 0.95em; opacity: 0.8; margin-top: 12px; }

            @media (max-width: 768px) {
                .report-header { flex-direction: column; gap: 24px; padding: 36px 24px; }
                .section-bordered { margin: 30px 20px; }
                .goat-narrative { margin: 30px 20px; }
                .logo h1 { font-size: 2.2em; }
                .summary-grid, .metrics-grid { grid-template-columns: 1fr; }
                .action-step { padding-left: 45px; }
            }
        </style>
        ""\"
